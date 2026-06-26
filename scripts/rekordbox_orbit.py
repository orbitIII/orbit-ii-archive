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
