#!/usr/bin/env python3
"""Move playlist outliers into ORBIT II → AUSGEsortiert.

Run analyze_orbit_playlists.py once per slug, then curate once. Do NOT re-analyze
and re-curate in a loop — the BPM p10–p90 window shifts after each removal.
"""

from __future__ import annotations

import argparse
import csv
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
TARGET_PLAYLIST_NAME = "AUSGEsortiert"

CURATIONS: dict[str, dict] = {
    "system_moment_deep": {
        "scores_csv": ROOT / "system_moment_deep_track_scores.csv",
        "playlist_name": "MOMENT DEEP ",
        "parent_name": "SYSTEM",
        "label": "SYSTEM MOMENT DEEP",
    },
    "orbit_moment_deep": {
        "scores_csv": ROOT / "orbit_moment_deep_track_scores.csv",
        "playlist_name": "ORBIT MOMENT DEEP",
        "parent_name": "ORBIT II",
        "label": "ORBIT MOMENT DEEP",
    },
    "system_moment_driving": {
        "scores_csv": ROOT / "system_moment_driving_track_scores.csv",
        "playlist_name": "MOMENT Driving ",
        "parent_name": "SYSTEM",
        "label": "SYSTEM MOMENT Driving",
    },
    "system_warm_hypnotic": {
        "scores_csv": ROOT / "system_warm_hypnotic_track_scores.csv",
        "playlist_name": "WARM HYPNOTIC",
        "parent_name": "SYSTEM",
        "label": "SYSTEM WARM HYPNOTIC",
    },
    "system_warm": {
        "scores_csv": ROOT / "system_warm_track_scores.csv",
        "playlist_name": "WARM",
        "parent_name": "SYSTEM",
        "label": "SYSTEM WARM",
    },
}


def norm(value: str) -> str:
    return " ".join((value or "").strip().casefold().split())


def load_outliers(scores_csv: Path) -> list[dict[str, str]]:
    if not scores_csv.exists():
        raise FileNotFoundError(f"Missing scores file: {scores_csv}")
    rows: list[dict[str, str]] = []
    with scores_csv.open(newline="", encoding="utf-8") as handle:
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


def find_content_by_id(db, track_id: str):
    try:
        return db.get_content(ID=int(track_id))
    except (TypeError, ValueError):
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


def ensure_target_playlist(db, orbit_ii):
    target = find_playlist_by_name(db, TARGET_PLAYLIST_NAME, parent_id=orbit_ii.ID)
    if target is not None and target.Attribute == 0:
        return target
    print(f"Creating playlist '{TARGET_PLAYLIST_NAME}' under ORBIT II...")
    return db.create_playlist(TARGET_PLAYLIST_NAME, parent=orbit_ii)


def move_outliers(db, source_cfg: dict, source_playlist, target_playlist) -> tuple[int, int, list[str]]:
    outliers = load_outliers(source_cfg["scores_csv"])
    moved = 0
    already_there = 0
    missing: list[str] = []

    print(f"\n{source_cfg['label']}: {len(outliers)} outliers")
    for row in outliers:
        content = find_content_by_id(db, row.get("track_id", "")) or find_content(
            db, row["artist"], row["name"]
        )
        if content is None:
            missing.append(f"{row['artist']} — {row['name']}")
            continue

        in_source = find_song_in_playlist(db, source_playlist.ID, content.ID)
        in_target = find_song_in_playlist(db, target_playlist.ID, content.ID)

        if in_source is None and in_target is not None:
            already_there += 1
            continue

        if in_source is not None:
            print(f"  Moving: {content.ArtistName} — {content.Title}")
            db.remove_from_playlist(source_playlist, in_source)
            moved += 1

        if in_target is None:
            db.add_to_playlist(target_playlist, content)

    return moved, already_there, missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Move playlist outliers to AUSGEsortiert")
    parser.add_argument(
        "--slug",
        action="append",
        dest="slugs",
        choices=sorted(CURATIONS),
        help="Playlist slug to curate (repeatable). Default: all configured.",
    )
    args = parser.parse_args()
    slugs = args.slugs or sorted(CURATIONS)

    backup = backup_library()
    print(f"Backup written to {backup}")
    print("Stopping Rekordbox and rekordboxAgent...")
    stop_rekordbox()

    from pyrekordbox import Rekordbox6Database

    db = Rekordbox6Database(path=DB_PATH, db_dir=RB_DIR)

    orbit_ii = find_playlist_by_name(db, ORBIT_II_NAME)
    if orbit_ii is None:
        print("Could not find ORBIT II in Rekordbox.", file=sys.stderr)
        return 1

    target_playlist = ensure_target_playlist(db, orbit_ii)
    db.commit()

    total_moved = 0
    total_already = 0
    all_missing: list[str] = []

    for slug in slugs:
        source_cfg = CURATIONS[slug]
        parent = find_playlist_by_name(db, source_cfg["parent_name"])
        if parent is None:
            print(f"Missing parent playlist: {source_cfg['parent_name']}", file=sys.stderr)
            return 1
        source_playlist = find_playlist_by_name(
            db, source_cfg["playlist_name"], parent_id=parent.ID
        )
        if source_playlist is None:
            print(
                f"Missing source: {source_cfg['parent_name']} → {source_cfg['playlist_name']}",
                file=sys.stderr,
            )
            return 1

        moved, already, missing = move_outliers(db, source_cfg, source_playlist, target_playlist)
        total_moved += moved
        total_already += already
        all_missing.extend(missing)

    db.commit()
    if db.playlist_xml is not None and db.playlist_xml.modified:
        db.playlist_xml.save()
    db.close()

    print(f"\nDone. Moved: {total_moved}, already in AUSGEsortiert: {total_already}")
    print(f"Location: ORBIT II → {TARGET_PLAYLIST_NAME}")
    print("Rekordbox was NOT started — open manually when ready.")
    if all_missing:
        print("\nNot found in library:")
        for item in all_missing:
            print(f"  - {item}")

    return 0 if not all_missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
