#!/usr/bin/env python3
"""Create one TrackID set-index CSV per Top 50 Panorama Bar artist.

This uses the repository's TrackID archive
`berghain_2024_2026_top50_artist_sets_trackid.csv`. It does not invent TrackID
detail URLs and does not scrape audio. The output is one CSV per artist with the
TrackID search-result rows currently available in the archive.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOP50 = ROOT / "berghain_2024_2026_top50_panorama_bar_artists.csv"
TRACKID_ARCHIVE = ROOT / "berghain_2024_2026_top50_artist_sets_trackid.csv"
OUT_DIR = ROOT / "data" / "trackid_artist_csv"
MANIFEST = ROOT / "berghain_2024_2026_trackid_artist_csv_manifest.csv"

OUTPUT_FIELDS = [
    "artist_rank",
    "artist",
    "source_platform",
    "source_url",
    "result_count",
    "set_title",
    "channel",
    "duration",
    "created_on",
    "requested_on",
    "requested_by",
    "status",
    "archive_scope",
    "notes",
]

MANIFEST_FIELDS = [
    "artist_rank",
    "artist",
    "local_csv_path",
    "row_count",
    "trackid_result_count",
    "status",
    "notes",
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
        "é": "e",
        "è": "e",
        "ï": "i",
        "ø": "o",
        "ó": "o",
        "á": "a",
        "à": "a",
        "â": "a",
    }
    for src, dst in replacements.items():
        value = value.replace(src, dst)
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "artist"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    top50 = read_csv(TOP50)
    archive = read_csv(TRACKID_ARCHIVE)

    by_artist: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in archive:
        by_artist[row["artist"]].append(row)

    manifest_rows: list[dict[str, str]] = []
    for top_row in top50:
        rank = top_row["Rank"]
        artist = top_row["Artist"]
        rows = by_artist.get(artist, [])
        local_path = OUT_DIR / f"{int(rank):02d}_{slugify(artist)}.csv"

        with local_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
            writer.writeheader()
            for row in rows:
                writer.writerow({field: row.get(field, "") for field in OUTPUT_FIELDS})

        result_counts = sorted({row.get("result_count", "") for row in rows if row.get("result_count", "")})
        manifest_rows.append(
            {
                "artist_rank": rank,
                "artist": artist,
                "local_csv_path": str(local_path.relative_to(ROOT)),
                "row_count": str(len(rows)),
                "trackid_result_count": "; ".join(result_counts),
                "status": "created" if rows else "created_empty",
                "notes": "Created from TrackID visible search archive; not an official TrackID export CSV.",
            }
        )

    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(manifest_rows)

    print(f"artist_csv_files={len(manifest_rows)}")
    print(f"manifest={MANIFEST.relative_to(ROOT)}")
    print(f"output_dir={OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
