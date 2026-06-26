#!/usr/bin/env python3
"""Restore wrongly sorted MOMENT DEEP tracks from AUSGEsortiert back to source playlists."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RB_DIR = Path.home() / "Library/Pioneer/rekordbox"
DB_PATH = RB_DIR / "master.db"
PLAYLIST_XML = RB_DIR / "masterPlaylists6.xml"
BACKUP_DIR = ROOT / "rekordbox" / "backups"

ORBIT_II_NAME = "ORBIT II"
SYSTEM_NAME = "SYSTEM"
AUSGESORTIERT_NAME = "AUSGEsortiert"

# Tracks removed by over-aggressive iterative curation — belong in SYSTEM MOMENT DEEP.
RESTORE_SYSTEM = [
    ("Chris Stussy", "Never Tell Me"),
    ("Chris Stussy", "Soul Patrol"),
    ("Phil Weeks", "Nasty Girl (Original Mix)"),
    ("Soul Of Hex", "Nobody ft Cromie"),
    ("Wreal", "Feels Good (Joss Moog Funky Remix)"),
    ("Mihai Popoviciu", "Waitin' (Original Mix)"),
    ("Gemini", "Take Your Time (Original)"),
    ("Alexander East", "Jest 4 Me (BHQ Instrumental)"),
    ("Ackermann", "Alter (Simon Hinter Remix)"),
    ("Da Rebels", "House Nation Under a Groove"),
    ("Mike Starr & Mama", "Love Away (Douglas Greed Remix)"),
    ("Dano, Joeski", "Chikko Vox (Vocal Mix)"),
    ("Adam Collins & Mister Ali", "Neptunes Android"),
    ("Kerouac", "A2 Active Meditation VINYL ONLY "),
    ("Traumer, Anton, antraum", "Fukai (Original Mix)"),
    ("Lump", "U Need Me (Original Mix)"),
    ("Francesco Forgione", "I Feel It (Original Mix)"),
    ("Wiremü", "The Subtle Hustle"),
    ("Alkalino", "Seven Sisters (Original Mix)"),
    ("A1 Lazer Man", "Que vas tu faire VINYL ONLY "),
]

RESTORE_ORBIT = [
    ("Silat Beksi", "Do Or Donut (Original Mix)"),
    ("grad u", "Geomagnetic Storm"),
    ("Nudge", "Howl012.2 VINYL ONLY"),
]

# Remove duplicate playlist rows (same artist+title twice in AUSGEsortiert).
DEDUPE_IN_AUSGESORTIERT = [
    ("D'Julz", "Give Me Your Hand (Original Mix)"),
    ("GusGus", "Your Moves Are Mine (Sanasol Remix)"),
]


def norm(value: str) -> str:
    return " ".join((value or "").strip().casefold().split())


def stop_rekordbox(timeout_s: int = 45) -> None:
    subprocess.run(
        ["osascript", "-e", 'tell application "rekordbox" to quit'],
        check=False,
    )
    for proc in ("rekordbox", "rekordboxAgent"):
        subprocess.run(["pkill", "-x", proc], check=False)
    for _ in range(timeout_s):
        running = any(
            subprocess.run(["pgrep", "-x", proc], capture_output=True).returncode == 0
            for proc in ("rekordbox", "rekordboxAgent")
        )
        if not running:
            time.sleep(2)
            return
        time.sleep(1)
    raise RuntimeError("Rekordbox did not fully quit. Close it manually and retry.")


def backup_library() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    target = BACKUP_DIR / stamp
    target.mkdir()
    shutil.copy2(DB_PATH, target / "master.db")
    shutil.copy2(PLAYLIST_XML, target / "masterPlaylists6.xml")
    return target


def find_playlist_by_name(db, name: str, *, parent_id: str | None = None):
    wanted = norm(name)
    for playlist in db.get_playlist():
        if not playlist.Name or norm(playlist.Name) != wanted:
            continue
        if parent_id is not None and str(playlist.ParentID) != str(parent_id):
            continue
        return playlist
    return None


def find_song_in_playlist(db, playlist_id: str, content_id: str):
    for song in db.get_playlist_songs(PlaylistID=playlist_id):
        if str(song.ContentID) == str(content_id):
            return song
    return None


def find_in_playlist_by_name(db, playlist_id: str, artist: str, title: str):
    artist_n = norm(artist)
    title_n = norm(title)
    for song in db.get_playlist_songs(PlaylistID=playlist_id):
        content = db.get_content(ID=song.ContentID)
        if norm(content.ArtistName) == artist_n and norm(content.Title) == title_n:
            return song, content
    return None, None


def restore_track(db, aus_playlist, target_playlist, artist: str, title: str) -> str:
    song, content = find_in_playlist_by_name(db, aus_playlist.ID, artist, title)
    if content is None:
        return "missing"

    in_target = find_song_in_playlist(db, target_playlist.ID, content.ID)
    if song is not None:
        db.remove_from_playlist(aus_playlist, song)
    if in_target is None:
        db.add_to_playlist(target_playlist, content)
        return "restored"
    return "already_in_target"


def dedupe_playlist_entry(db, aus_playlist, artist: str, title: str) -> int:
    artist_n = norm(artist)
    title_n = norm(title)
    matches = []
    for song in db.get_playlist_songs(PlaylistID=aus_playlist.ID):
        content = db.get_content(ID=song.ContentID)
        if norm(content.ArtistName) == artist_n and norm(content.Title) == title_n:
            matches.append(song)
    removed = 0
    for song in matches[1:]:
        db.remove_from_playlist(aus_playlist, song)
        removed += 1
    return removed


def main() -> int:
    backup = backup_library()
    print(f"Backup written to {backup}")
    print("Stopping Rekordbox and rekordboxAgent...")
    stop_rekordbox()

    from pyrekordbox import Rekordbox6Database

    db = Rekordbox6Database(path=DB_PATH, db_dir=RB_DIR)

    orbit_ii = find_playlist_by_name(db, ORBIT_II_NAME)
    system = find_playlist_by_name(db, SYSTEM_NAME)
    aus = find_playlist_by_name(db, AUSGESORTIERT_NAME, parent_id=orbit_ii.ID)
    system_md = find_playlist_by_name(db, "MOMENT DEEP ", parent_id=system.ID)
    orbit_md = find_playlist_by_name(db, "ORBIT MOMENT DEEP", parent_id=orbit_ii.ID)

    if not all([orbit_ii, system, aus, system_md, orbit_md]):
        print("Missing required playlists.", file=sys.stderr)
        return 1

    restored_system = 0
    for artist, title in RESTORE_SYSTEM:
        result = restore_track(db, aus, system_md, artist, title)
        if result == "restored":
            print(f"  → SYSTEM: {artist} — {title}")
            restored_system += 1
        elif result == "missing":
            print(f"  ? not in AUSGEsortiert: {artist} — {title}")

    restored_orbit = 0
    for artist, title in RESTORE_ORBIT:
        result = restore_track(db, aus, orbit_md, artist, title)
        if result == "restored":
            print(f"  → ORBIT: {artist} — {title}")
            restored_orbit += 1
        elif result == "missing":
            print(f"  ? not in AUSGEsortiert: {artist} — {title}")

    deduped = 0
    for artist, title in DEDUPE_IN_AUSGESORTIERT:
        n = dedupe_playlist_entry(db, aus, artist, title)
        if n:
            print(f"  deduped AUSGEsortiert: {artist} — {title} ({n} extra row(s))")
        deduped += n

    db.commit()
    if db.playlist_xml is not None and db.playlist_xml.modified:
        db.playlist_xml.save()
    db.close()

    print(f"\nDone. Restored {restored_system} → SYSTEM MOMENT DEEP, {restored_orbit} → ORBIT MOMENT DEEP.")
    print(f"Removed {deduped} duplicate row(s) from AUSGEsortiert.")
    print("Rekordbox was NOT started — open manually when ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
