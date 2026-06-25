#!/usr/bin/env python3
"""TrackID Artist-Set-Index import for Orbit II Panorama Bar research.

Workflow:
  Artist-Set-Index (TrackID search) -> open set page -> tracklist? -> import/skip
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://trackid.net/api/public/audiostreams"
TRACKLISTS_CSV = ROOT / "berghain_2024_2026_tracklists.csv"
SETS_CSV = ROOT / "berghain_2024_2026_tracklist_sets.csv"
TOP50_CSV = ROOT / "berghain_2024_2026_top50_panorama_bar_artists.csv"
KLUBNACHT_JSON = ROOT / "berghain" / "klubnacht_2024_2026.json"
OBSERVATIONS_MD = ROOT / "berghain_2024_2026_observations.md"

SET_FIELDNAMES = [
    "SetURL",
    "Artist",
    "Date",
    "Venue",
    "Room",
    "TrackCount",
    "Duration",
    "CoverageStatus",
    "CoverageNote",
    "Status",
]

USER_AGENT = "OrbitII-Archive/1.0 (+research; contact: local)"
REQUEST_DELAY_SEC = 0.35
LOW_TRACK_THRESHOLD = 3
GOOD_TRACKS_PER_HOUR = 8.0
GOOD_MIN_TRACKS = 10


@dataclass
class RunStats:
    artists_processed: int = 0
    sets_opened: int = 0
    sets_imported: int = 0
    sets_skipped: int = 0
    tracks_written: int = 0
    panorama_matches: int = 0
    artist_rows: list[tuple[str, int, int, int]] = field(default_factory=list)


def fetch_json(url: str) -> dict:
    proc = subprocess.run(
        [
            "curl",
            "-sL",
            "-A",
            USER_AGENT,
            "-H",
            "Accept: application/json",
            url,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def quote(value: str) -> str:
    from urllib.parse import quote as urlquote

    return urlquote(value)


def load_top50_artists(limit: int | None = None) -> list[str]:
    if TOP50_CSV.exists():
        with TOP50_CSV.open(newline="", encoding="utf-8") as f:
            artists = [row["Artist"].strip() for row in csv.DictReader(f) if row["Artist"].strip()]
        if limit is not None:
            return artists[:limit]
        return artists

    data = json.loads(KLUBNACHT_JSON.read_text(encoding="utf-8"))
    counts: Counter[str] = Counter()
    for ev in data.values() if isinstance(data, dict) else data:
        for room, sets in ev.get("rooms", {}).items():
            if "panorama" in room.lower():
                for s in sets:
                    name = (s.get("artist") or "").strip()
                    if name:
                        counts[name] += 1
    ranked = [name for name, _ in counts.most_common(limit or 50)]
    return ranked


def search_sets(keywords: str, page_size: int = 50) -> list[dict]:
    params = "&".join(
        [
            f"keywords={quote(keywords)}",
            "page=0",
            f"size={page_size}",
        ]
    )
    payload = fetch_json(f"{API_BASE}?{params}")
    return payload.get("result", {}).get("audiostreams", []) or []


def latest_tracks(detail: dict) -> list[dict]:
    processes = detail.get("detectionProcesses") or []
    if not processes:
        return []

    best: list[dict] = []
    for process in processes:
        tracks = [
            t
            for t in (process.get("detectionProcessMusicTracks") or [])
            if (t.get("title") or "").strip()
        ]
        if len(tracks) > len(best):
            best = tracks
    return best


def parse_duration_minutes(value: str | None) -> float | None:
    if not value:
        return None
    text = value.split(".")[0].strip()
    parts = text.split(":")
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        return None
    if len(nums) == 3:
        hours, minutes, seconds = nums
    elif len(nums) == 2:
        hours = 0
        minutes, seconds = nums
    elif len(nums) == 1:
        return nums[0] / 60.0
    else:
        return None
    return hours * 60 + minutes + seconds / 60.0


def assess_coverage(track_count: int, duration_raw: str | None) -> tuple[str, str, str]:
    duration_display = (duration_raw or "").split(".")[0] or ""
    duration_min = parse_duration_minutes(duration_raw)

    if track_count <= LOW_TRACK_THRESHOLD:
        note = (
            f"{track_count} tracks identified"
            + (f" over {duration_display}" if duration_display else "")
            + "; very few identified tracks"
        )
        return duration_display, "low_coverage", note

    if duration_min is None or duration_min <= 0:
        note = f"{track_count} tracks identified; duration unavailable from TrackID"
        return duration_display, "unknown_coverage", note

    tph = track_count / (duration_min / 60.0)
    note = (
        f"{track_count} tracks over {duration_display} "
        f"(~{tph:.1f} identified tracks/hour)"
    )
    if track_count >= GOOD_MIN_TRACKS or tph >= GOOD_TRACKS_PER_HOUR:
        return duration_display, "good_coverage", note
    return duration_display, "partial_coverage", note


def infer_room(title: str) -> str:
    lower = title.lower()
    if "panorama bar" in lower or "panoramabar" in lower:
        return "Panorama Bar"
    if "berghain" in lower or "halle am berghain" in lower:
        return "Berghain"
    return ""


def infer_venue(title: str) -> str:
    return infer_room(title)


def is_venue_relevant(title: str, slug: str) -> bool:
    blob = f"{title} {slug}".lower()
    markers = (
        "berghain",
        "panorama bar",
        "panoramabar",
        "klubnacht",
        "halle am berghain",
        "ostgut ton",
    )
    return any(marker in blob for marker in markers)


def parse_created_on(value: str | None) -> str:
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.date().isoformat()
    except ValueError:
        return value[:10] if value else ""


def load_existing_keys(path: Path) -> set[tuple[str, str, str]]:
    if not path.exists():
        return set()
    keys: set[tuple[str, str, str]] = set()
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            keys.add(
                (
                    row.get("SourceURL", ""),
                    row.get("TrackTitle", ""),
                    row.get("TrackArtist", ""),
                )
            )
    return keys


def load_existing_set_urls(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with path.open(newline="", encoding="utf-8") as f:
        return {row.get("SetURL", "") for row in csv.DictReader(f)}


def ensure_csv_headers() -> None:
    if not TRACKLISTS_CSV.exists():
        with TRACKLISTS_CSV.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(
                [
                    "Date",
                    "Artist",
                    "TrackTitle",
                    "TrackArtist",
                    "Label",
                    "TrackID",
                    "SourceURL",
                    "Room",
                ]
            )
    if not SETS_CSV.exists():
        with SETS_CSV.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=SET_FIELDNAMES).writeheader()


def artist_search_queries(artist: str) -> list[str]:
    return [
        f"{artist} Panorama Bar",
        f"{artist} Berghain",
        f"{artist} Klubnacht",
    ]


def slug_matches_artist(slug: str, title: str, artist: str) -> bool:
    norm = re.sub(r"[^a-z0-9]+", "", artist.lower())
    blob = f"{slug} {title}".lower()
    blob_norm = re.sub(r"[^a-z0-9]+", "", blob)
    return norm in blob_norm


def set_row_from_detail(
    set_url: str,
    artist: str,
    title: str,
    detail: dict,
    tracks: list[dict],
    status: str,
) -> list[str]:
    track_count = len(tracks)
    duration_raw = detail.get("duration")
    duration, coverage_status, coverage_note = assess_coverage(track_count, duration_raw)
    date = parse_created_on(detail.get("createdOn"))
    room = infer_room(title)
    venue = infer_venue(title) or room
    return [
        set_url,
        artist,
        date,
        venue,
        room,
        str(track_count),
        duration,
        coverage_status,
        coverage_note,
        status,
    ]


def import_artist(
    artist: str,
    track_keys: set[tuple[str, str, str]],
    known_set_urls: set[str],
    track_rows: list[list[str]],
    set_rows: list[list[str]],
    stats: RunStats,
) -> None:
    seen_slugs: set[str] = set()
    imported_for_artist = 0
    skipped_for_artist = 0
    opened_for_artist = 0

    for query in artist_search_queries(artist):
        try:
            results = search_sets(query)
        except Exception as exc:  # noqa: BLE001
            print(f"  search failed ({query}): {exc}", file=sys.stderr)
            continue
        time.sleep(REQUEST_DELAY_SEC)

        results = sorted(
            results,
            key=lambda item: (
                0 if is_venue_relevant(item.get("title") or "", item.get("slug") or "") else 1,
                item.get("title") or "",
            ),
        )

        for item in results:
            slug = item.get("slug") or ""
            title = item.get("title") or ""
            if not slug or slug in seen_slugs:
                continue
            if not slug_matches_artist(slug, title, artist):
                continue
            if not is_venue_relevant(title, slug):
                continue
            seen_slugs.add(slug)
            opened_for_artist += 1
            stats.sets_opened += 1

            set_url = f"https://trackid.net/audiostreams/{slug}"
            try:
                detail_payload = fetch_json(f"{API_BASE}/{slug}")
            except Exception as exc:  # noqa: BLE001
                print(f"  set open failed ({slug}): {exc}", file=sys.stderr)
                continue
            time.sleep(REQUEST_DELAY_SEC)

            detail = detail_payload.get("result") or {}
            tracks = latest_tracks(detail)
            room = infer_room(title)

            if not tracks:
                status = "skipped_no_tracklist"
                skipped_for_artist += 1
                stats.sets_skipped += 1
            else:
                status = "imported"
                imported_for_artist += 1
                stats.sets_imported += 1
                if room == "Panorama Bar":
                    stats.panorama_matches += 1

                for track in tracks:
                    track_artist = (track.get("artist") or "").strip()
                    track_title = (track.get("title") or "").strip()
                    label = (track.get("label") or "").strip()
                    track_slug = (track.get("slug") or "").strip()
                    trackid_url = (
                        f"https://trackid.net/musictracks/{track_slug}"
                        if track_slug
                        else ""
                    )
                    key = (set_url, track_title, track_artist)
                    if key in track_keys:
                        continue
                    track_keys.add(key)
                    track_rows.append(
                        [
                            parse_created_on(detail.get("createdOn")),
                            artist,
                            track_title,
                            track_artist,
                            label,
                            trackid_url,
                            set_url,
                            room,
                        ]
                    )
                    stats.tracks_written += 1

            if set_url not in known_set_urls:
                known_set_urls.add(set_url)
                set_rows.append(
                    set_row_from_detail(set_url, artist, title, detail, tracks, status)
                )

    stats.artists_processed += 1
    stats.artist_rows.append(
        (artist, opened_for_artist, imported_for_artist, skipped_for_artist)
    )


def migrate_sets_csv() -> None:
    if not SETS_CSV.exists():
        return
    with SETS_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return
    if all(field in rows[0] for field in SET_FIELDNAMES):
        return

    migrated: list[dict] = []
    for row in rows:
        set_url = row.get("SetURL", "")
        slug = set_url.rsplit("/", 1)[-1] if set_url else ""
        track_count = int(row.get("TrackCount") or 0)
        duration = row.get("Duration", "")
        coverage_status = row.get("CoverageStatus", "")
        coverage_note = row.get("CoverageNote", "")
        if slug and (not duration or not coverage_status):
            try:
                detail = fetch_json(f"{API_BASE}/{slug}").get("result") or {}
                duration, coverage_status, coverage_note = assess_coverage(
                    track_count, detail.get("duration")
                )
                time.sleep(REQUEST_DELAY_SEC)
            except Exception:
                duration = duration or ""
                coverage_status = coverage_status or "unknown_coverage"
                coverage_note = coverage_note or "migration backfill failed"
        migrated.append(
            {
                "SetURL": set_url,
                "Artist": row.get("Artist", ""),
                "Date": row.get("Date", ""),
                "Venue": row.get("Venue", ""),
                "Room": row.get("Room", ""),
                "TrackCount": row.get("TrackCount", "0"),
                "Duration": duration,
                "CoverageStatus": coverage_status or "unknown_coverage",
                "CoverageNote": coverage_note,
                "Status": row.get("Status", ""),
            }
        )
    with SETS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SET_FIELDNAMES)
        writer.writeheader()
        writer.writerows(migrated)


def append_observations(stats: RunStats, artist_count: int) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "",
        f"### TrackID Import run — {stamp}",
        f"- Artists processed: {stats.artists_processed} (top {artist_count} Panorama Bar)",
        f"- Sets opened: {stats.sets_opened}",
        f"- Sets imported: {stats.sets_imported}",
        f"- Sets skipped (no tracklist): {stats.sets_skipped}",
        f"- Tracks written: {stats.tracks_written}",
        f"- Panorama Bar title matches: {stats.panorama_matches}",
        "- Per artist:",
    ]
    for artist, opened, imported, skipped in stats.artist_rows:
        lines.append(
            f"  - {artist}: opened={opened}, imported={imported}, skipped={skipped}"
        )

    text = OBSERVATIONS_MD.read_text(encoding="utf-8") if OBSERVATIONS_MD.exists() else ""
    if "## TrackID Import runs" not in text:
        text += "\n\n## TrackID Import runs\n"
    text += "\n".join(lines) + "\n"
    OBSERVATIONS_MD.write_text(text, encoding="utf-8")


def main() -> int:
    artist_limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    ensure_csv_headers()
    migrate_sets_csv()

    artists = load_top50_artists(artist_limit)
    track_keys = load_existing_keys(TRACKLISTS_CSV)
    known_set_urls = load_existing_set_urls(SETS_CSV)

    track_rows: list[list[str]] = []
    set_rows: list[list[str]] = []
    stats = RunStats()

    print(f"Importing TrackID sets for top {len(artists)} Panorama Bar artists...")
    for artist in artists:
        print(f"- {artist}")
        import_artist(
            artist, track_keys, known_set_urls, track_rows, set_rows, stats
        )

    if track_rows:
        with TRACKLISTS_CSV.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(track_rows)
    if set_rows:
        with SETS_CSV.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=SET_FIELDNAMES)
            for row in set_rows:
                writer.writerow(dict(zip(SET_FIELDNAMES, row)))

    append_observations(stats, len(artists))

    print(
        f"Done: artists={stats.artists_processed}, opened={stats.sets_opened}, "
        f"imported={stats.sets_imported}, skipped={stats.sets_skipped}, "
        f"tracks={stats.tracks_written}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
