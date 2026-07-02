#!/usr/bin/env python3
"""Shared ORBIT ↔ Rekordbox helpers (read, analyze, curate playlists)."""

from __future__ import annotations

import csv
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RB_DIR = Path.home() / "Library/Pioneer/rekordbox"
DB_PATH = RB_DIR / "master.db"
PLAYLIST_CONFIG = ROOT / "orbit_playlists.json"
BACKUP_DIR = ROOT / "rekordbox" / "backups"
ORBIT_II_NAME = "ORBIT II"
AUSGESORTIERT_NAME = "AUSGEsortiert"


def norm(value: str) -> str:
    return " ".join((value or "").strip().casefold().split())


def load_config() -> dict:
    return json.loads(PLAYLIST_CONFIG.read_text(encoding="utf-8"))


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


def open_db():
    from pyrekordbox import Rekordbox6Database

    return Rekordbox6Database(path=DB_PATH, db_dir=RB_DIR)


def find_playlist_db(db, name: str, parent_name: str | None = None):
    wanted = norm(name)
    parent_id = None
    if parent_name:
        parent = find_playlist_db(db, parent_name)
        if parent is None:
            return None
        parent_id = str(parent.ID)
    for playlist in db.get_playlist():
        if not playlist.Name or norm(playlist.Name) != wanted:
            continue
        if parent_id is not None and str(playlist.ParentID) != parent_id:
            continue
        return playlist
    return None


def playlist_specs() -> list[dict]:
    return load_config()["playlists"]


def spec_by_slug(slug: str) -> dict:
    for spec in playlist_specs():
        if spec["slug"] == slug:
            return spec
    raise KeyError(f"Unknown playlist slug: {slug}")


def export_playlist_snapshot(db, playlist, export_dir: Path) -> Path:
    export_dir.mkdir(parents=True, exist_ok=True)
    slug = norm(playlist.Name).replace(" ", "_")
    path = export_dir / f"{slug}_snapshot.csv"
    rows = []
    for song in sorted(db.get_playlist_songs(PlaylistID=playlist.ID), key=lambda s: s.TrackNo):
        content = db.get_content(ID=song.ContentID)
        rows.append(
            {
                "track_no": song.TrackNo,
                "content_id": content.ID,
                "artist": content.ArtistName,
                "title": content.Title,
                "label": content.LabelName or "",
                "genre": content.GenreName or "",
                "bpm": round(content.BPM / 100, 2) if content.BPM else "",
                "key": content.KeyName or "",
            }
        )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)
    return path


def backup_library() -> Path:
    import shutil

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    target = BACKUP_DIR / stamp
    target.mkdir()
    shutil.copy2(DB_PATH, target / "master.db")
    shutil.copy2(RB_DIR / "masterPlaylists6.xml", target / "masterPlaylists6.xml")
    return target


def find_content_by_id(db, track_id: str):
    try:
        return db.get_content(ID=int(track_id))
    except (TypeError, ValueError):
        return None


def find_content_by_name(db, artist: str, title: str):
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


def ensure_ausgesortiert(db):
    orbit_ii = find_playlist_db(db, ORBIT_II_NAME)
    if orbit_ii is None:
        raise RuntimeError(f"Missing playlist: {ORBIT_II_NAME}")
    target = find_playlist_db(db, AUSGESORTIERT_NAME, ORBIT_II_NAME)
    if target is not None and target.Attribute == 0:
        return target
    return db.create_playlist(AUSGESORTIERT_NAME, parent=orbit_ii)


def move_to_ausgesortiert(db, content, source_playlist=None) -> bool:
    """Remove from source playlist and add to AUSGEsortiert. Never deletes library content."""
    target = ensure_ausgesortiert(db)
    removed = False
    if source_playlist is not None:
        song = find_song_in_playlist(db, str(source_playlist.ID), str(content.ID))
        if song is not None:
            db.remove_from_playlist(source_playlist, song)
            removed = True
    if find_song_in_playlist(db, str(target.ID), str(content.ID)) is None:
        db.add_to_playlist(target, content)
    return removed or find_song_in_playlist(db, str(target.ID), str(content.ID)) is not None


def collect_to_ausgesortiert(db, track_id: str, artist: str, title: str, *, from_parents: tuple[str, ...] = ("SYSTEM",)) -> str:
    """Find track in playlists under given parents, move to AUSGEsortiert."""
    content = find_content_by_id(db, track_id) or find_content_by_name(db, artist, title)
    if content is None:
        return "missing"

    target = ensure_ausgesortiert(db)
    moved_from = 0
    for parent_name in from_parents:
        parent = find_playlist_db(db, parent_name)
        if parent is None:
            continue
        for playlist in db.get_playlist():
            if str(playlist.ParentID) != str(parent.ID):
                continue
            if norm(playlist.Name) == norm(AUSGESORTIERT_NAME):
                continue
            song = find_song_in_playlist(db, str(playlist.ID), str(content.ID))
            if song is not None:
                db.remove_from_playlist(playlist, song)
                moved_from += 1

    if find_song_in_playlist(db, str(target.ID), str(content.ID)) is None:
        db.add_to_playlist(target, content)

    return "ok" if moved_from or find_song_in_playlist(db, str(target.ID), str(content.ID)) else "not_found"
