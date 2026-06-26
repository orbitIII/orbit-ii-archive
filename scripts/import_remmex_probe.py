#!/usr/bin/env python3
"""Import downloaded Remmex probe MP3s into Rekordbox playlist."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_DIR = ROOT / "remmex" / "downloads" / "probe-2026-06-25"
RB_DIR = Path.home() / "Library/Pioneer/rekordbox"
PLAYLIST_NAME = "REMMEX Probe"
PARENT_NAME = "ORBIT II"
RB_APP = "/Users/Shared/Previously Relocated Items/Security/Applications/rekordbox 6/rekordbox.app"


def stop_rekordbox() -> None:
    subprocess.run(["osascript", "-e", 'tell application "rekordbox" to quit'], check=False)
    for proc in ("rekordbox", "rekordboxAgent"):
        subprocess.run(["pkill", "-x", proc], check=False)
    for _ in range(45):
        if not any(
            subprocess.run(["pgrep", "-x", p], capture_output=True).returncode == 0
            for p in ("rekordbox", "rekordboxAgent")
        ):
            time.sleep(2)
            return
        time.sleep(1)
    raise RuntimeError("Rekordbox did not quit")


def parse_filename(path: Path) -> tuple[str, str]:
    name = path.stem
    if " - " in name:
        artist, title = name.split(" - ", 1)
        title = title.split(" [", 1)[0]
        return artist.strip(), title.strip()
    return "", name


def main() -> int:
    sys.path.insert(0, str(ROOT / "scripts"))
    from rekordbox_orbit import find_playlist_db

    files = sorted(DOWNLOAD_DIR.glob("*.mp3"))
    if len(files) < 4:
        print(f"Expected 4 mp3 in {DOWNLOAD_DIR}, found {len(files)}", file=sys.stderr)
        return 1

    print("Stopping Rekordbox...")
    stop_rekordbox()

    from pyrekordbox import Rekordbox6Database
    from pyrekordbox.db6 import tables

    db = Rekordbox6Database(path=RB_DIR / "master.db", db_dir=RB_DIR)
    orbit_ii = find_playlist_db(db, PARENT_NAME)
    if orbit_ii is None:
        print(f"{PARENT_NAME} not found", file=sys.stderr)
        return 1

    playlist = find_playlist_db(db, PLAYLIST_NAME, parent_name=PARENT_NAME)
    if playlist is None:
        print(f"Creating playlist '{PLAYLIST_NAME}' under {PARENT_NAME}...")
        playlist = db.create_playlist(PLAYLIST_NAME, parent=orbit_ii)
        db.commit()

    added = 0
    for path in files[:4]:
        path = path.resolve()
        artist, title = parse_filename(path)
        try:
            content = db.add_content(str(path), Title=title)
        except ValueError:
            content = db.query(tables.DjmdContent).filter_by(FolderPath=str(path)).one()

        existing = db.get_playlist_songs(PlaylistID=playlist.ID)
        if not any(str(s.ContentID) == str(content.ID) for s in existing):
            db.add_to_playlist(playlist, content)
        print(f"  ✓ {artist} — {title}")
        added += 1

    db.commit()
    db.close()

    print(f"\nDone: {added} tracks in {PARENT_NAME} → {PLAYLIST_NAME}")
    if Path(RB_APP).exists():
        subprocess.run(["open", RB_APP], check=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
