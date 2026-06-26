#!/usr/bin/env python3
"""One-pass curation: move MOMENT VOCAL outliers to ORBIT II → AUSGEsortiert."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rekordbox_orbit import (  # noqa: E402
    backup_library,
    find_playlist_db,
    move_to_ausgesortiert,
    open_db,
    stop_rekordbox,
    find_content_by_id,
    find_content_by_name,
)

SOURCE_PARENT = "SYSTEM"
SOURCE_PLAYLIST = "MOMENT VOCAL//CINTHIE"

OUTLIERS: list[tuple[str, str, str]] = [
    ("198144679", "Jade Cox", "Want You All"),
    ("107969902", "Tree Threes", "Coast 2 Coast"),
    ("257926706", "Sidney Charles", "The Duke (Jesse Perez Remix)"),
    ("162325787", "Adryiano", "The Sturdy Track"),
    ("180511117", "Katermurr", "PEAK TIM//CONGO BONGOHere To Stay"),
    ("232039658", "Christoph Faust, CRYME", "Things We Used To Say (Original Mix)"),
    ("214559970", "Sally C", "All Love (Original Mix)"),
]


def main() -> int:
    backup = backup_library()
    print(f"Backup written to {backup}")
    print("Stopping Rekordbox and rekordboxAgent...")
    stop_rekordbox()

    db = open_db()
    source = find_playlist_db(db, SOURCE_PLAYLIST, SOURCE_PARENT)
    if source is None:
        print(f"{SOURCE_PLAYLIST} not found.", file=sys.stderr)
        return 1

    moved = 0
    missing: list[str] = []
    for track_id, artist, title in OUTLIERS:
        content = find_content_by_id(db, track_id) or find_content_by_name(db, artist, title)
        if content is None:
            missing.append(f"{artist} — {title}")
            continue
        if move_to_ausgesortiert(db, content, source_playlist=source):
            print(f"  → AUSGEsortiert: {artist} — {title[:45]}")
            moved += 1

    db.commit()
    if db.playlist_xml is not None and db.playlist_xml.modified:
        db.playlist_xml.save()
    db.close()

    print(f"\nDone. Moved {moved} tracks to AUSGEsortiert (not deleted from library).")
    print("Rekordbox was NOT started.")
    return 0 if not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
