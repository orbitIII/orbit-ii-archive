#!/usr/bin/env python3
"""Sort tracks from ORBIT II → AUSGEsortiert into target playlists."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rekordbox_orbit import (  # noqa: E402
    backup_library,
    find_playlist_db,
    norm,
    open_db,
    stop_rekordbox,
)

# (artist, title, parent, playlist) — artist=None matches by title only
SORT_PLAN: list[tuple[str | None, str, str, str]] = [
    # ORBIT → ARCHIV
    ("Andrew", "Some Say (Original Mix)", "ORBIT II", "ARCHIV "),
    # SYSTEM → WARM (slow / opening)
    ("Jade Cox", "Want You All", "SYSTEM", "WARM"),
    ("Blind Box feat Hector Moralez", "Thinking Out Loud VINYL ONLY", "SYSTEM", "WARM"),
    ("Mr. Statik, Lee Burton, Steampunkd", "Peanuts In Love (Ion Ludwig Remix)", "SYSTEM", "WARM"),
    ("Daniel Law", "Futile Needs ", "SYSTEM", "WARM"),
    ("Powel", "Lullaby For Eyebrights (Original Mix)", "SYSTEM", "WARM"),
    ("Ortella", "B2 Work I VINYL ONLY ", "SYSTEM", "WARM"),
    ("Nesta", "Light Tower", "SYSTEM", "WARM"),
    ("Steffi", "ACID//SYNTH DOMNANTNightspacer (Original Mix)", "SYSTEM", "WARM"),
    ("Vinyl Speed ADJust", "Retro", "SYSTEM", "WARM"),
    ("D\u2019Julz", "Ze Box", "SYSTEM", "WARM"),
    ("Sidney Charles", "The Duke (Jesse Perez Remix)", "SYSTEM", "WARM"),
    ("A Psychic Yes", "Maze Dream (Sapphire Slows Remix)", "SYSTEM", "WARM"),
    ("Aleqs Notal", "Hands On (Original Mix)", "SYSTEM", "WARM"),
    # SYSTEM → WARM HYPNOTIC (minimal / hypnotic groove)
    ("Tomoki Tamura", "Retro City Vinyl Only", "SYSTEM", "WARM HYPNOTIC"),
    ("Echonomist", "Diabolo", "SYSTEM", "WARM HYPNOTIC"),
    ("Levi Verspeek", "A2 Octo VINYL ONLY ", "SYSTEM", "WARM HYPNOTIC"),
    ("Ortella", "Let's Go To The Bitch Vinyl Only", "SYSTEM", "WARM HYPNOTIC"),
    ("Mr. Lady", "The Game (Originalmix)", "SYSTEM", "WARM HYPNOTIC"),
    ("Yaleesa Hall & Malin Genie", "B2 Coronal Loop VINYL ONLY ", "SYSTEM", "WARM HYPNOTIC"),
    # SYSTEM → MOMENT DEEP / MOMENT Driving
    ("Tree Threes", "Coast 2 Coast", "SYSTEM", "MOMENT DEEP "),
    ("Sally C", "All Love (Original Mix)", "SYSTEM", "MOMENT Driving "),
    ("SOST", "Hidden Skeleton (Original Mix)", "SYSTEM", "MOMENT Driving "),
    # SYSTEM → DRIVING PUSH (peak)
    ("Christoph Faust, CRYME", "Things We Used To Say (Original Mix)", "SYSTEM", "DRIVING PUSH"),
    # SYSTEM → WIRED (genre / energy mismatch)
    ("Mac Declos, Pablo Bozzi", "Cutting Edge (Original Mix)", "SYSTEM", "WIRED "),
    ("Chris Kiser", "Where I've Been (Terry Francis RMX)", "SYSTEM", "WIRED "),
    ("Mr. G", "Moments (Original Mix)", "SYSTEM", "WIRED "),
    ("Munir Nadir", "A2 Bass Jam VINYL ONLY ", "SYSTEM", "WIRED "),
    ("Adryiano", "The Sturdy Track", "SYSTEM", "WIRED "),
    ("Katermurr", "PEAK TIM//CONGO BONGOHere To Stay", "SYSTEM", "WIRED "),
    ("fleet.dreams", "Semioptila", "SYSTEM", "WIRED "),
    ("Minimal Man", "B1 Stay On (A.M. Edit) VINYL ONLY ", "SYSTEM", "WIRED "),
    ("Audio Werner", "High", "SYSTEM", "WIRED "),
    ("Grad_u", "B1 Decay VINYL ONLY ", "SYSTEM", "WIRED "),
    (None, "Makam - Glacial Valley", "SYSTEM", "WIRED "),
]


def find_in_ausgesortiert(db, aus_playlist, artist: str | None, title: str):
    title_n = norm(title)
    for song in db.get_playlist_songs(PlaylistID=aus_playlist.ID):
        content = db.get_content(ID=song.ContentID)
        if norm(content.Title) != title_n:
            continue
        if artist is None:
            return song, content
        if norm(content.ArtistName or "") == norm(artist):
            return song, content
    return None, None


def find_song_in_playlist(db, playlist_id: str, content_id: str):
    for song in db.get_playlist_songs(PlaylistID=playlist_id):
        if str(song.ContentID) == str(content_id):
            return song
    return None


def move_track(db, aus_playlist, target_playlist, artist: str | None, title: str) -> str:
    song, content = find_in_ausgesortiert(db, aus_playlist, artist, title)
    if content is None:
        return "missing"

    if song is not None:
        db.remove_from_playlist(aus_playlist, song)
    if find_song_in_playlist(db, str(target_playlist.ID), str(content.ID)) is None:
        db.add_to_playlist(target_playlist, content)
    return "moved"


def main() -> int:
    backup = backup_library()
    print(f"Backup written to {backup}")
    print("Stopping Rekordbox and rekordboxAgent...")
    stop_rekordbox()

    db = open_db()

    orbit_ii = find_playlist_db(db, "ORBIT II")
    system = find_playlist_db(db, "SYSTEM")
    aus = find_playlist_db(db, "AUSGEsortiert", "ORBIT II")
    if not all([orbit_ii, system, aus]):
        print("Missing ORBIT II, SYSTEM, or AUSGEsortiert.", file=sys.stderr)
        return 1

    parents = {"ORBIT II": orbit_ii, "SYSTEM": system}
    moved = 0
    missing: list[str] = []

    for artist, title, parent_name, playlist_name in SORT_PLAN:
        parent = parents[parent_name]
        target = find_playlist_db(db, playlist_name, parent_name)
        if target is None:
            print(f"Missing target: {parent_name} → {playlist_name!r}", file=sys.stderr)
            return 1

        label = artist or title[:30]
        result = move_track(db, aus, target, artist, title)
        if result == "moved":
            print(f"  → {parent_name} / {playlist_name.strip()}: {label} — {title[:35]}")
            moved += 1
        else:
            missing.append(f"{label} — {title}")

    db.commit()
    if db.playlist_xml is not None and db.playlist_xml.modified:
        db.playlist_xml.save()
    db.close()

    print(f"\nDone. Moved {moved} tracks from AUSGEsortiert.")
    if missing:
        print(f"Not found ({len(missing)}):")
        for item in missing:
            print(f"  - {item}")
    print("Rekordbox was NOT started — open manually when ready.")
    return 0 if not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
