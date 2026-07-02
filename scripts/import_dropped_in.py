#!/usr/bin/env python3
"""Import historical Panorama Bar / Berghain tracks from drOpped-iN (2010-2017).

Separate from the TrackID 2021-2026 pipeline. Uses:
  - /api/config
  - /api/search
  - /api/track?track_id=...
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://dropped-in.dievardump.com"
CHECKPOINT_PATH = ROOT / "dropped_in_import_checkpoint.json"
CACHE_PATH = ROOT / "dropped_in_track_cache.jsonl"

TRACKS_CSV = ROOT / "dropped_in_tracks.csv"
POSTS_CSV = ROOT / "dropped_in_posts.csv"
DJ_MENTIONS_CSV = ROOT / "dropped_in_dj_mentions.csv"
TRACK_COUNTS_CSV = ROOT / "dropped_in_track_counts.csv"
TOP_TRACKS_CSV = ROOT / "dropped_in_top_tracks.csv"
ARTIST_FREQ_CSV = ROOT / "dropped_in_artist_frequency.csv"
LABEL_CANDIDATES_CSV = ROOT / "dropped_in_label_candidates.csv"
REPORT_MD = ROOT / "DROPPED_IN_IMPORT_REPORT.md"

USER_AGENT = "OrbitII-Archive/1.0 (+drOpped-iN; contact: local)"
REQUEST_DELAY_SEC = 0.25
SEARCH_PAGE_SIZE = 20
DATE_FROM = "2010-01-13"
DATE_TO = "2017-08-09"

NON_DJ_MARKERS = {"n.n", "nn", "?", "unknown", "id", "id?", "tbc"}


@dataclass
class ImportStats:
    search_pages: int = 0
    tracks_discovered: int = 0
    tracks_detailed: int = 0
    tracks_skipped_cached: int = 0
    posts_written: int = 0
    dj_mentions_written: int = 0
    errors: list[str] = field(default_factory=list)


def fetch_json(path: str, params: dict[str, Any] | None = None) -> dict:
    url = f"{BASE_URL}{path}"
    if params:
        url = f"{url}?{urlencode(params)}"
    proc = subprocess.run(
        ["curl", "-sL", "-A", USER_AGENT, "-H", "Accept: application/json", url],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(proc.stdout)
    if not payload.get("success"):
        raise RuntimeError(f"API error for {url}: {payload}")
    return payload


def load_config() -> dict:
    return fetch_json("/api/config")["data"]


def page_slug(page_id: int, pages: dict[str, dict]) -> str:
    for page in pages.values():
        if page["id"] == page_id:
            return page["name"]
    return f"page_{page_id}"


def parse_track_title(full_title: str) -> tuple[str, str]:
    title = (full_title or "").strip()
    if not title:
        return "", ""
    for sep in (" - ", " – ", " — "):
        if sep in title:
            artist, track = title.split(sep, 1)
            if artist.strip() and track.strip():
                return artist.strip(), track.strip()
    return "", title


def extract_label_candidate(title: str) -> str:
    match = re.search(r"\[([^\]]+)\]\s*$", title or "")
    if match:
        return match.group(1).strip()
    return ""


def normalize_mention(message: str) -> str:
    text = (message or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .,\n\t")


def is_dj_mention(message: str, track_title: str) -> tuple[str, str]:
    mention = normalize_mention(message)
    if not mention:
        return "", ""
    lower = mention.lower()
    if lower in NON_DJ_MARKERS:
        return "", ""
    if "http://" in lower or "https://" in lower or "youtu.be" in lower:
        return "", ""
    if mention.lower() == track_title.lower():
        return "", ""
    if len(mention) > 120:
        return "", ""
    confidence = "high" if len(mention) <= 50 and "(" not in mention else "medium"
    return mention, confidence


def post_source_url(facebook_id: str) -> str:
    return f"https://facebook.com/{facebook_id}"


def track_source_url(track_id: int) -> str:
    return f"{BASE_URL}/#/track/{track_id}"


def load_checkpoint() -> dict:
    if CHECKPOINT_PATH.exists():
        return json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
    return {"search_completed": False, "detailed_track_ids": []}


def save_checkpoint(state: dict) -> None:
    CHECKPOINT_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def load_cache() -> dict[int, dict]:
    cache: dict[int, dict] = {}
    if not CACHE_PATH.exists():
        return cache
    with CACHE_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            cache[int(row["id"])] = row
    return cache


def append_cache(track: dict) -> None:
    with CACHE_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(track, ensure_ascii=False) + "\n")


def search_all_tracks() -> tuple[list[dict], int]:
    summaries: dict[int, dict] = {}
    page = 1
    last_page = 1
    pages_fetched = 0
    while page <= last_page:
        params = {
            "page": page,
            "order": "most_played",
            "order_type": "desc",
            "fb_page": "",
            "content": "",
            "date_from": DATE_FROM,
            "date_to": DATE_TO,
        }
        result = fetch_json("/api/search", params)["data"]
        last_page = int(result.get("lastPage") or 1)
        for item in result.get("data") or []:
            summaries[int(item["id"])] = item
        pages_fetched += 1
        time.sleep(REQUEST_DELAY_SEC)
        page += 1
    return list(summaries.values()), pages_fetched


def fetch_track_detail(track_id: int) -> dict:
    return fetch_json("/api/track", {"track_id": track_id})["data"]


def merge_track(summary: dict, detail: dict | None) -> dict:
    merged = dict(summary)
    if detail:
        merged.update(detail)
        merged["posts"] = detail.get("posts") or []
    else:
        merged.setdefault("posts", [])
    return merged


def post_dates(posts: list[dict]) -> tuple[str, str]:
    dates = sorted(p.get("created_at", "")[:10] for p in posts if p.get("created_at"))
    if not dates:
        return "", ""
    return dates[0], dates[-1]


def build_rows(
    tracks: list[dict], pages: dict[str, dict]
) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    track_rows: list[dict] = []
    post_rows: list[dict] = []
    mention_rows: list[dict] = []
    count_rows: list[dict] = []

    for track in sorted(tracks, key=lambda item: int(item["id"])):
        track_id = int(track["id"])
        full_title = track.get("title") or track.get("name") or ""
        track_artist, track_title = parse_track_title(full_title)
        posts = track.get("posts") or []
        first_seen, last_seen = post_dates(posts)
        if not first_seen:
            first_seen = (track.get("created_at") or "")[:10]
        if not last_seen:
            last_seen = first_seen
        api_count = int(track.get("count") or 0)
        source = track.get("link") or track_source_url(track_id)

        track_rows.append(
            {
                "track_id": str(track_id),
                "track_artist": track_artist,
                "track_title": track_title,
                "count": str(api_count),
                "first_seen": first_seen,
                "last_seen": last_seen,
                "source_url": source,
                "notes": "drOpped-iN historical import (2010-2017)",
            }
        )

        count_rows.append(
            {
                "track_artist": track_artist,
                "track_title": track_title,
                "count": str(api_count),
                "post_count": str(len(posts)),
                "first_seen": first_seen,
                "last_seen": last_seen,
                "source_url": source,
            }
        )

        seen_posts: set[int] = set()
        for post in posts:
            post_id = int(post["id"])
            if post_id in seen_posts:
                continue
            seen_posts.add(post_id)
            page_name = page_slug(int(post.get("fb_page_id") or 0), pages)
            post_date = (post.get("created_at") or "")[:10]
            text = post.get("message") or post.get("fulltext") or ""
            post_rows.append(
                {
                    "track_id": str(track_id),
                    "post_id": str(post_id),
                    "page": page_name,
                    "date": post_date,
                    "text": text.strip(),
                    "source_url": post_source_url(post.get("facebook_id") or ""),
                }
            )

            dj_mention, confidence = is_dj_mention(post.get("message") or "", full_title)
            if dj_mention:
                mention_rows.append(
                    {
                        "track_id": str(track_id),
                        "track_artist": track_artist,
                        "track_title": track_title,
                        "dj_mention": dj_mention,
                        "post_id": str(post_id),
                        "page": page_name,
                        "date": post_date,
                        "text": text.strip(),
                        "confidence": confidence,
                        "notes": "extracted from post message only",
                    }
                )

    return track_rows, post_rows, mention_rows, count_rows


def build_top_tracks(track_rows: list[dict]) -> list[dict]:
    ranked = sorted(track_rows, key=lambda row: (-int(row["count"]), row["track_title"]))
    output = []
    for index, row in enumerate(ranked[:100], start=1):
        output.append(
            {
                "rank": str(index),
                "track_artist": row["track_artist"],
                "track_title": row["track_title"],
                "count": row["count"],
                "first_seen": row["first_seen"],
                "last_seen": row["last_seen"],
                "source_url": row["source_url"],
            }
        )
    return output


def build_artist_frequency(mention_rows: list[dict]) -> list[dict]:
    counts: Counter[str] = Counter()
    tracks: dict[str, set[str]] = defaultdict(set)
    for row in mention_rows:
        mention = row["dj_mention"].strip()
        if not mention:
            continue
        counts[mention] += 1
        tracks[mention].add(row["track_id"])
    rows = []
    for mention, count in counts.most_common():
        rows.append(
            {
                "dj_mention": mention,
                "mention_count": str(count),
                "unique_tracks": str(len(tracks[mention])),
                "notes": "derived from post messages only",
            }
        )
    return rows


def build_label_candidates(track_rows: list[dict]) -> list[dict]:
    counts: Counter[str] = Counter()
    examples: dict[str, str] = {}
    for row in track_rows:
        label = extract_label_candidate(row["track_title"])
        if not label:
            label = extract_label_candidate(
                f"{row['track_artist']} - {row['track_title']}"
            )
        if not label:
            continue
        counts[label] += 1
        examples.setdefault(label, row["source_url"])
    return [
        {
            "label_candidate": label,
            "track_count": str(count),
            "example_source_url": examples[label],
            "notes": "bracket suffix in track title only",
        }
        for label, count in counts.most_common()
    ]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(fieldnames=fieldnames, f=handle, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    config: dict,
    track_rows: list[dict],
    post_rows: list[dict],
    mention_rows: list[dict],
    top_tracks: list[dict],
    artist_freq: list[dict],
    label_candidates: list[dict],
    stats: ImportStats,
) -> None:
    posts_meta = config.get("posts", {})
    first = (posts_meta.get("first") or {}).get("created_at", "")[:10]
    last = (posts_meta.get("last") or {}).get("created_at", "")[:10]
    lines = [
        "# drOpped-iN Import Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Import summary",
        "",
        f"- Unique tracks: {len(track_rows)}",
        f"- Posts: {len(post_rows)}",
        f"- DJ mentions extracted: {len(mention_rows)}",
        f"- Search pages fetched: {stats.search_pages}",
        f"- Track details fetched this run: {stats.tracks_detailed}",
        f"- Track details reused from cache: {stats.tracks_skipped_cached}",
        f"- Configured post range: {first} to {last}",
        "",
        "## Top tracks by count",
        "",
    ]
    for row in top_tracks[:20]:
        artist = row["track_artist"] or "Unknown artist"
        lines.append(
            f"- {artist} — {row['track_title']} ({row['count']} mentions)"
        )

    lines.extend(["", "## Most frequent DJ mentions", ""])
    for row in artist_freq[:20]:
        lines.append(
            f"- {row['dj_mention']}: {row['mention_count']} mentions "
            f"({row['unique_tracks']} tracks)"
        )

    lines.extend(
        [
            "",
            "## Coverage / limitations",
            "",
            "- drOpped-iN data ends in 2017 because Facebook API changes stopped new fetches.",
            "- Tracks are community-identified from Berghain Music / Panorama Bar Music posts.",
            "- DJ mentions come only from post message text; ambiguous markers like `N.N` are excluded.",
            "- Labels are not inferred unless explicitly present in bracket suffixes.",
            "- Track `count` values come directly from the drOpped-iN API.",
            "",
            "## Role in Orbit II",
            "",
            "- Historical Panorama Bar / Berghain backbone (2010-2017).",
            "- Klassiker / overlap signal via `count` and repeated DJ mentions.",
            "- Not a current 2024-2026 data source; keep separate from TrackID imports.",
            "",
        ]
    )
    if label_candidates:
        lines.extend(["## Label candidates (explicit bracket suffixes only)", ""])
        for row in label_candidates[:15]:
            lines.append(
                f"- {row['label_candidate']}: {row['track_count']} track(s)"
            )
        lines.append("")

    if stats.errors:
        lines.extend(["## Errors", ""])
        for err in stats.errors[:20]:
            lines.append(f"- {err}")
        lines.append("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def validate_outputs(
    track_rows: list[dict],
    post_rows: list[dict],
    mention_rows: list[dict],
) -> None:
    track_ids = {row["track_id"] for row in track_rows}
    if len(track_ids) != len(track_rows):
        raise ValueError("Duplicate track_id rows in dropped_in_tracks.csv")

    post_keys = {(row["track_id"], row["post_id"]) for row in post_rows}
    if len(post_keys) != len(post_rows):
        raise ValueError("Duplicate post rows in dropped_in_posts.csv")

    for row in mention_rows:
        if not row["dj_mention"].strip():
            raise ValueError("Empty dj_mention row")
        if row["dj_mention"].strip().lower() in NON_DJ_MARKERS:
            raise ValueError(f"Invalid dj_mention: {row['dj_mention']}")


def import_dropped_in(max_tracks: int | None = None, refresh: bool = False) -> int:
    stats = ImportStats()
    if refresh:
        for path in (CHECKPOINT_PATH, CACHE_PATH):
            if path.exists():
                path.unlink()

    config = load_config()
    pages = config.get("pages") or {}
    checkpoint = load_checkpoint()
    cache = load_cache()

    if not checkpoint.get("search_completed"):
        summaries, stats.search_pages = search_all_tracks()
        checkpoint["search_completed"] = True
        checkpoint["summaries"] = summaries
        save_checkpoint(checkpoint)
    else:
        summaries = checkpoint.get("summaries") or []
        if not summaries:
            summaries, stats.search_pages = search_all_tracks()
            checkpoint["summaries"] = summaries
            save_checkpoint(checkpoint)
        else:
            stats.search_pages = int(len(summaries) / SEARCH_PAGE_SIZE) + 1

    stats.tracks_discovered = len(summaries)

    if max_tracks is not None:
        summaries = summaries[:max_tracks]

    detailed_ids = set(checkpoint.get("detailed_track_ids") or [])
    for summary in summaries:
        track_id = int(summary["id"])
        if track_id in cache and track_id in detailed_ids:
            stats.tracks_skipped_cached += 1
            continue
        try:
            detail = fetch_track_detail(track_id)
            merged = merge_track(summary, detail)
            cache[track_id] = merged
            append_cache(merged)
            detailed_ids.add(track_id)
            stats.tracks_detailed += 1
            checkpoint["detailed_track_ids"] = sorted(detailed_ids)
            if stats.tracks_detailed % 100 == 0:
                save_checkpoint(checkpoint)
            time.sleep(REQUEST_DELAY_SEC)
        except Exception as exc:  # noqa: BLE001
            stats.errors.append(f"track {track_id}: {exc}")

    save_checkpoint(checkpoint)

    tracks = [cache[int(summary["id"])] for summary in summaries if int(summary["id"]) in cache]
    track_rows, post_rows, mention_rows, count_rows = build_rows(tracks, pages)
    top_tracks = build_top_tracks(track_rows)
    artist_freq = build_artist_frequency(mention_rows)
    label_candidates = build_label_candidates(track_rows)

    validate_outputs(track_rows, post_rows, mention_rows)

    write_csv(
        TRACKS_CSV,
        [
            "track_id",
            "track_artist",
            "track_title",
            "count",
            "first_seen",
            "last_seen",
            "source_url",
            "notes",
        ],
        track_rows,
    )
    write_csv(
        POSTS_CSV,
        ["track_id", "post_id", "page", "date", "text", "source_url"],
        post_rows,
    )
    write_csv(
        DJ_MENTIONS_CSV,
        [
            "track_id",
            "track_artist",
            "track_title",
            "dj_mention",
            "post_id",
            "page",
            "date",
            "text",
            "confidence",
            "notes",
        ],
        mention_rows,
    )
    write_csv(
        TRACK_COUNTS_CSV,
        [
            "track_artist",
            "track_title",
            "count",
            "post_count",
            "first_seen",
            "last_seen",
            "source_url",
        ],
        count_rows,
    )
    if top_tracks:
        write_csv(
            TOP_TRACKS_CSV,
            [
                "rank",
                "track_artist",
                "track_title",
                "count",
                "first_seen",
                "last_seen",
                "source_url",
            ],
            top_tracks,
        )
    if artist_freq:
        write_csv(
            ARTIST_FREQ_CSV,
            ["dj_mention", "mention_count", "unique_tracks", "notes"],
            artist_freq,
        )
    if label_candidates:
        write_csv(
            LABEL_CANDIDATES_CSV,
            ["label_candidate", "track_count", "example_source_url", "notes"],
            label_candidates,
        )

    stats.posts_written = len(post_rows)
    stats.dj_mentions_written = len(mention_rows)
    write_report(
        config,
        track_rows,
        post_rows,
        mention_rows,
        top_tracks,
        artist_freq,
        label_candidates,
        stats,
    )

    print(
        f"Done: tracks={len(track_rows)}, posts={len(post_rows)}, "
        f"mentions={len(mention_rows)}, detailed={stats.tracks_detailed}, "
        f"cached={stats.tracks_skipped_cached}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Import drOpped-iN historical tracks")
    parser.add_argument(
        "--max-tracks",
        type=int,
        default=None,
        help="Limit number of tracks (for testing)",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Clear cache/checkpoint and re-import",
    )
    args = parser.parse_args()
    return import_dropped_in(max_tracks=args.max_tracks, refresh=args.refresh)


if __name__ == "__main__":
    raise SystemExit(main())
