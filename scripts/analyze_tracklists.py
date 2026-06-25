#!/usr/bin/env python3
"""Build first-pass analysis CSVs from imported TrackID tracklists."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKLISTS_CSV = ROOT / "berghain_2024_2026_tracklists.csv"
SETS_CSV = ROOT / "berghain_2024_2026_tracklist_sets.csv"
TOP50_CSV = ROOT / "berghain_2024_2026_top50_panorama_bar_artists.csv"
OVERLAPS_CSV = ROOT / "berghain_2024_2026_track_overlaps.csv"
LABEL_FREQ_CSV = ROOT / "berghain_2024_2026_label_frequency.csv"
SHARED_CSV = ROOT / "berghain_2024_2026_artist_shared_tracks.csv"
REPORT_MD = ROOT / "TRACKID_IMPORT_ANALYSIS_REPORT.md"


def load_top50_artists() -> list[str]:
    with TOP50_CSV.open(newline="", encoding="utf-8") as f:
        return [row["Artist"].strip() for row in csv.DictReader(f) if row["Artist"].strip()]


def normalize_top50_map(artists: list[str]) -> dict[str, str]:
    return {a.strip().lower(): a for a in artists}


def canonical_dj(name: str, top50_map: dict[str, str]) -> str | None:
    key = name.strip().lower()
    return top50_map.get(key)


def track_key(track_artist: str, track_title: str) -> tuple[str, str]:
    return (track_artist.strip().lower(), track_title.strip().lower())


def confidence_label(count: int) -> str:
    if count >= 4:
        return "high"
    if count == 3:
        return "medium"
    return "low"


def build_overlaps(tracks: list[dict], top50_map: dict[str, str]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in tracks:
        dj = canonical_dj(row["Artist"], top50_map)
        if not dj:
            continue
        key = track_key(row["TrackArtist"], row["TrackTitle"])
        grouped[key].append({**row, "CanonicalDJ": dj})

    overlaps: list[dict] = []
    for (ta, tt), rows in sorted(grouped.items()):
        djs = sorted({r["CanonicalDJ"] for r in rows})
        if len(djs) < 2:
            continue
        sample = rows[0]
        label = sample.get("Label", "").strip() or "Unknown Label"
        set_urls = sorted({r["SourceURL"] for r in rows if r.get("SourceURL")})
        overlaps.append(
            {
                "track_artist": sample["TrackArtist"],
                "track_title": sample["TrackTitle"],
                "label": label,
                "top50_artist_count": len(djs),
                "played_by_artists": "; ".join(djs),
                "set_count": len(set_urls),
                "source_urls": "; ".join(set_urls),
                "confidence": confidence_label(len(djs)),
                "notes": "exact title+artist match across top-50 DJ contexts",
            }
        )
    return overlaps


def build_label_frequency(tracks: list[dict]) -> list[dict]:
    by_label: dict[str, list[dict]] = defaultdict(list)
    for row in tracks:
        label = row.get("Label", "").strip()
        if not label:
            label = "Unknown Label"
        by_label[label].append(row)

    rows: list[dict] = []
    for label, items in sorted(by_label.items(), key=lambda x: (-len(x[1]), x[0])):
        djs = sorted({i["Artist"] for i in items})
        sets = sorted({i["SourceURL"] for i in items if i.get("SourceURL")})
        rows.append(
            {
                "label": label,
                "track_count": len(items),
                "set_count": len(sets),
                "played_by_artists": "; ".join(djs),
                "source_count": len(sets),
                "notes": "aggregated from imported tracklist rows",
            }
        )
    return rows


def build_shared_tracks(tracks: list[dict], top50_map: dict[str, str]) -> list[dict]:
    track_to_djs: dict[tuple[str, str], set[str]] = defaultdict(set)
    track_meta: dict[tuple[str, str], dict] = {}

    for row in tracks:
        dj = canonical_dj(row["Artist"], top50_map)
        if not dj:
            continue
        key = track_key(row["TrackArtist"], row["TrackTitle"])
        track_to_djs[key].add(dj)
        track_meta[key] = row

    pair_tracks: dict[tuple[str, str], list[tuple[str, str, str]]] = defaultdict(list)
    pair_labels: dict[tuple[str, str], set[str]] = defaultdict(set)
    pair_urls: dict[tuple[str, str], set[str]] = defaultdict(set)

    for key, djs in track_to_djs.items():
        if len(djs) < 2:
            continue
        meta = track_meta[key]
        label = meta.get("Label", "").strip() or "Unknown Label"
        display = f"{meta['TrackArtist']} — {meta['TrackTitle']}"
        for a, b in combinations(sorted(djs), 2):
            pair_tracks[(a, b)].append((meta["TrackArtist"], meta["TrackTitle"], display))
            pair_labels[(a, b)].add(label)
            if meta.get("SourceURL"):
                pair_urls[(a, b)].add(meta["SourceURL"])

    rows: list[dict] = []
    for (a, b), shared in sorted(pair_tracks.items(), key=lambda x: (-len(x[1]), x[0])):
        rows.append(
            {
                "artist_a": a,
                "artist_b": b,
                "shared_track_count": len(shared),
                "shared_tracks": " | ".join(t[2] for t in shared),
                "shared_labels": "; ".join(sorted(pair_labels[(a, b)])),
                "source_urls": "; ".join(sorted(pair_urls[(a, b)])),
                "notes": "exact shared tracks between top-50 artists",
            }
        )
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_sets_summary() -> list[dict]:
    if not SETS_CSV.exists():
        return []
    with SETS_CSV.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def artists_without_tracklists(top50: list[str], sets: list[dict]) -> list[str]:
    imported = {
        row["Artist"]
        for row in sets
        if row.get("Status") == "imported" and int(row.get("TrackCount") or 0) > 0
    }
    imported_lower = {a.lower() for a in imported}
    return [a for a in top50 if a.lower() not in imported_lower]


def write_report(
    top50: list[str],
    tracks: list[dict],
    sets: list[dict],
    overlaps: list[dict],
    label_freq: list[dict],
    shared: list[dict],
) -> None:
    coverage_counts = Counter(row.get("CoverageStatus", "unknown_coverage") for row in sets)
    imported_sets = [s for s in sets if s.get("Status") == "imported"]
    skipped_sets = [s for s in sets if s.get("Status") == "skipped_no_tracklist"]
    no_data = artists_without_tracklists(top50, sets)

    lines = [
        "# TrackID Import Analysis Report",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Import summary",
        "",
        f"- Top-50 artists processed: {len(top50)}",
        f"- Set pages opened/logged: {len(sets)}",
        f"- Sets imported: {len(imported_sets)}",
        f"- Sets skipped (no tracklist): {len(skipped_sets)}",
        f"- Track rows imported: {len(tracks)}",
        "",
        "## Coverage status (imported sets)",
        "",
    ]
    for status in (
        "good_coverage",
        "partial_coverage",
        "low_coverage",
        "unknown_coverage",
    ):
        lines.append(f"- {status}: {coverage_counts.get(status, 0)}")

    lines.extend(
        [
            "",
            "## Top labels by track count",
            "",
        ]
    )
    for row in label_freq[:15]:
        lines.append(f"- {row['label']}: {row['track_count']} tracks")

    lines.extend(["", "## Track overlaps (exact matches)", ""])
    if overlaps:
        for row in overlaps[:20]:
            lines.append(
                f"- {row['track_artist']} — {row['track_title']} "
                f"({row['top50_artist_count']} DJs: {row['played_by_artists']})"
            )
    else:
        lines.append("- None yet in current import scope.")

    lines.extend(["", "## Artist pairs with shared tracks", ""])
    if shared:
        for row in shared[:20]:
            lines.append(
                f"- {row['artist_a']} + {row['artist_b']}: "
                f"{row['shared_track_count']} shared track(s)"
            )
    else:
        lines.append("- None yet in current import scope.")

    lines.extend(
        [
            "",
            "## Top-50 artists without usable tracklists (so far)",
            "",
        ]
    )
    if no_data:
        for artist in no_data:
            lines.append(f"- {artist}")
    else:
        lines.append("- All top-50 artists have at least one imported set.")

    lines.extend(
        [
            "",
            "## Important limitation",
            "",
            "TrackID provides identified tracks from a set, not guaranteed full set coverage.",
            "Low or partial coverage does not mean the import failed; it reflects TrackID detection limits.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def validate_outputs(overlaps: list[dict], shared: list[dict]) -> None:
    overlap_fields = [
        "track_artist",
        "track_title",
        "label",
        "top50_artist_count",
        "played_by_artists",
        "set_count",
        "source_urls",
        "confidence",
        "notes",
    ]
    for row in overlaps:
        for field in overlap_fields:
            if row.get(field, "") == "":
                raise ValueError(f"Empty overlap field {field}: {row}")
        if row["top50_artist_count"] < 2:
            raise ValueError(f"Overlap must have >=2 artists: {row}")
    for row in shared:
        if row["shared_track_count"] < 1:
            raise ValueError(f"Shared pair must have >=1 track: {row}")


def main() -> int:
    top50 = load_top50_artists()
    top50_map = normalize_top50_map(top50)

    with TRACKLISTS_CSV.open(newline="", encoding="utf-8") as f:
        tracks = list(csv.DictReader(f))

    overlaps = build_overlaps(tracks, top50_map)
    label_freq = build_label_frequency(tracks)
    shared = build_shared_tracks(tracks, top50_map)
    validate_outputs(overlaps, shared)

    write_csv(
        OVERLAPS_CSV,
        [
            "track_artist",
            "track_title",
            "label",
            "top50_artist_count",
            "played_by_artists",
            "set_count",
            "source_urls",
            "confidence",
            "notes",
        ],
        overlaps,
    )
    write_csv(
        LABEL_FREQ_CSV,
        [
            "label",
            "track_count",
            "set_count",
            "played_by_artists",
            "source_count",
            "notes",
        ],
        label_freq,
    )
    write_csv(
        SHARED_CSV,
        [
            "artist_a",
            "artist_b",
            "shared_track_count",
            "shared_tracks",
            "shared_labels",
            "source_urls",
            "notes",
        ],
        shared,
    )

    sets = load_sets_summary()
    write_report(top50, tracks, sets, overlaps, label_freq, shared)

    print(
        f"Analysis written: overlaps={len(overlaps)}, labels={len(label_freq)}, "
        f"shared_pairs={len(shared)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
