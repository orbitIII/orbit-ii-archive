#!/usr/bin/env python3
"""Collect wrongly direct-routed outliers back into ORBIT II → AUSGEsortiert."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rekordbox_orbit import (  # noqa: E402
    backup_library,
    collect_to_ausgesortiert,
    open_db,
    stop_rekordbox,
)

# Tracks that were sent directly to WARM/WIRED/etc instead of AUSGEsortiert.
TRACKS: list[tuple[str, str, str]] = [
    # DRIVING PUSH curation
    ("224773837", "Steffi", "ACID//SYNTH DOMNANTNightspacer (Original Mix)"),
    ("218398841", "Vinyl Speed ADJust", "Retro"),
    ("87683698", "Tomoki Tamura", "Retro City Vinyl Only"),
    ("243956011", "Echonomist", "Diabolo"),
    ("88065374", "Blind Box feat Hector Moralez", "Thinking Out Loud VINYL ONLY"),
    ("10019205", "D'Julz", "Ze Box"),
    ("37565762", "Mac Declos, Pablo Bozzi", "Cutting Edge (Original Mix)"),
    ("9524448", "Chris Kiser", "Where I've Been (Terry Francis RMX)"),
    ("201340449", "Andrew", "Some Say (Original Mix)"),
    ("3684679", "Mr. G", "Moments (Original Mix)"),
    ("98020315", "Munir Nadir", "A2 Bass Jam VINYL ONLY "),
    # MOMENT VOCAL curation
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
    ok = 0
    missing: list[str] = []

    for track_id, artist, title in TRACKS:
        result = collect_to_ausgesortiert(db, track_id, artist, title, from_parents=("SYSTEM",))
        if result == "ok":
            print(f"  → AUSGEsortiert: {artist} — {title[:45]}")
            ok += 1
        else:
            missing.append(f"{artist} — {title}")

    db.commit()
    if db.playlist_xml is not None and db.playlist_xml.modified:
        db.playlist_xml.save()
    db.close()

    print(f"\nDone. {ok} tracks now in AUSGEsortiert (library content untouched).")
    print("Rekordbox was NOT started — open manually when ready.")
    if missing:
        print("\nNot found:")
        for item in missing:
            print(f"  - {item}")
    return 0 if not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
