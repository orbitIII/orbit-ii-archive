#!/usr/bin/env python3
"""Move ORBIT FLOW outliers into AUSGEsortiert in Rekordbox."""

from __future__ import annotations

import csv
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORES_CSV = ROOT / "orbit_flow_track_scores.csv"
RB_DIR = Path.home() / "Library/Pioneer/rekordbox"
DB_PATH = RB_DIR / "master.db"
PLAYLIST_XML = RB_DIR / "masterPlaylists6.xml"
BACKUP_DIR = ROOT / "rekordbox" / "backups"

ORBIT_II_NAME = "ORBIT II"
ORBIT_FLOW_NAME = "ORBIT FLOW"
TARGET_PLAYLIST_NAME = "AUSGEsortiert"
LEGACY_FOLDER_NAME = "AUSGEsortiert"
LEGACY_PLAYLIST_NAME = "ORBIT FLOW AUSREISSER"


def norm(value: str) -> str:
    return " ".join((value or "").strip().casefold().split())


def load_outliers() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with SCORES_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("is_outlier") == "yes":
                rows.append(row)
    return rows


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
    raise RuntimeError("Rekordbox did not fully quit. Please close it manually and rerun.")


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


def find_content(db, artist: str, title: str):
    artist_n = norm(artist)
    title_n = norm(title)
    for content in db.get_content():
        if norm(content.ArtistName) == artist_n and norm(content.Title) == title_n:
            return content
    return None


def find_song_in_playlist(db, playlist_id: str, content_id: str):
    for song in db.get_playlist_songs(PlaylistID=playlist_id):
        if str(song.ContentID) == str(content_id):
            return song
    return None


def playlist_track_count(db, playlist_id: str) -> int:
    return db.get_playlist_songs(PlaylistID=playlist_id).count()


def ensure_target_playlist(db, orbit_ii):
    target = find_playlist_by_name(db, TARGET_PLAYLIST_NAME, parent_id=orbit_ii.ID)
    if target is not None and target.Attribute == 0:
        return target

    print(f"Creating playlist '{TARGET_PLAYLIST_NAME}' under ORBIT II...")
    return db.create_playlist(TARGET_PLAYLIST_NAME, parent=orbit_ii)


def migrate_legacy_playlists(db, target_playlist, orbit_ii):
    legacy_folder = find_playlist_by_name(db, LEGACY_FOLDER_NAME, parent_id=orbit_ii.ID)
    if legacy_folder is None or legacy_folder.Attribute != 1:
        return

    legacy_playlist = find_playlist_by_name(db, LEGACY_PLAYLIST_NAME, parent_id=legacy_folder.ID)
    if legacy_playlist is not None:
        for song in list(db.get_playlist_songs(PlaylistID=legacy_playlist.ID)):
            content = db.get_content(ID=song.ContentID)
            if find_song_in_playlist(db, target_playlist.ID, content.ID) is None:
                db.add_to_playlist(target_playlist, content)
            db.remove_from_playlist(legacy_playlist, song)
        db.delete_playlist(legacy_playlist)
        print(f"Removed legacy playlist '{LEGACY_PLAYLIST_NAME}'")

    if playlist_track_count(db, legacy_folder.ID) == 0:
        children = [p for p in db.get_playlist() if str(p.ParentID) == str(legacy_folder.ID)]
        if not children:
            db.delete_playlist(legacy_folder)
            print(f"Removed legacy folder '{LEGACY_FOLDER_NAME}'")


def main() -> int:
    if not SCORES_CSV.exists():
        print(f"Missing scores file: {SCORES_CSV}", file=sys.stderr)
        return 1

    outliers = load_outliers()
    if not outliers:
        print("No ORBIT FLOW outliers found in scores CSV.", file=sys.stderr)
        return 1

    print(f"Outliers to ensure in AUSGEsortiert: {len(outliers)}")
    backup = backup_library()
    print(f"Backup written to {backup}")

    print("Stopping Rekordbox and rekordboxAgent...")
    stop_rekordbox()

    from pyrekordbox import Rekordbox6Database

    db = Rekordbox6Database(path=DB_PATH, db_dir=RB_DIR)

    orbit_ii = find_playlist_by_name(db, ORBIT_II_NAME)
    orbit_flow = find_playlist_by_name(db, ORBIT_FLOW_NAME)
    if not orbit_ii or not orbit_flow:
        print("Could not find ORBIT II or ORBIT FLOW in Rekordbox.", file=sys.stderr)
        return 1

    target_playlist = ensure_target_playlist(db, orbit_ii)
    db.commit()

    moved = 0
    already_there = 0
    missing = []

    for row in outliers:
        content = find_content(db, row["artist"], row["name"])
        if content is None:
            missing.append(f"{row['artist']} — {row['name']}")
            continue

        in_target = find_song_in_playlist(db, target_playlist.ID, content.ID)
        in_flow = find_song_in_playlist(db, orbit_flow.ID, content.ID)

        if in_target is not None and in_flow is None:
            already_there += 1
            continue

        if in_flow is not None:
            print(f"Moving from ORBIT FLOW: {content.ArtistName} — {content.Title}")
            db.remove_from_playlist(orbit_flow, in_flow)
            if in_target is None:
                db.add_to_playlist(target_playlist, content)
            moved += 1
        elif in_target is None:
            print(f"Adding to AUSGEsortiert: {content.ArtistName} — {content.Title}")
            db.add_to_playlist(target_playlist, content)
            moved += 1

    migrate_legacy_playlists(db, target_playlist, orbit_ii)
    db.commit()
    if db.playlist_xml is not None and db.playlist_xml.modified:
        db.playlist_xml.save()
    db.close()

    print(f"\nDone.")
    print(f"Moved now: {moved}")
    print(f"Already in AUSGEsortiert: {already_there}")
    print(f"ORBIT FLOW should have: {36 - len(outliers)} tracks")
    print(f"Location: ORBIT II → {TARGET_PLAYLIST_NAME} (direct playlist, 1 click)")
    if missing:
        print("\nNot found in library:")
        for item in missing:
            print(f"  - {item}")

    rb_app = "/Users/Shared/Previously Relocated Items/Security/Applications/rekordbox 6/rekordbox.app"
    if Path(rb_app).exists():
        subprocess.run(["open", rb_app], check=False)

    return 0 if not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
