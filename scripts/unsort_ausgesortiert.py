#!/usr/bin/env python3
"""Undo sort_ausgesortiert: move tracks back from targets → AUSGEsortiert."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from rekordbox_orbit import (  # noqa: E402
    backup_library,
    ensure_ausgesortiert,
    find_playlist_db,
    norm,
    open_db,
    stop_rekordbox,
)
from sort_ausgesortiert import SORT_PLAN, find_song_in_playlist  # noqa: E402


def find_in_playlist(db, playlist, artist: str | None, title: str):
    title_n = norm(title)
    for song in db.get_playlist_songs(PlaylistID=playlist.ID):
        content = db.get_content(ID=song.ContentID)
        if norm(content.Title) != title_n:
            continue
        if artist is None:
            return song, content
        if norm(content.ArtistName or "") == norm(artist):
            return song, content
    return None, None


def main() -> int:
    backup = backup_library()
    print(f"Backup written to {backup}")
    print("Stopping Rekordbox and rekordboxAgent...")
    stop_rekordbox()

    db = open_db()
    aus = ensure_ausgesortiert(db)

    moved = 0
    missing: list[str] = []

    for artist, title, parent_name, playlist_name in SORT_PLAN:
        source = find_playlist_db(db, playlist_name, parent_name)
        if source is None:
            print(f"Missing source: {parent_name} → {playlist_name!r}", file=sys.stderr)
            return 1

        song, content = find_in_playlist(db, source, artist, title)
        label = artist or title[:30]
        if content is None:
            missing.append(f"{label} — {title}")
            continue

        if song is not None:
            db.remove_from_playlist(source, song)
        if find_song_in_playlist(db, str(aus.ID), str(content.ID)) is None:
            db.add_to_playlist(aus, content)
        print(f"  ← AUSGEsortiert: {label} — {title[:35]} (from {playlist_name.strip()})")
        moved += 1

    db.commit()
    if db.playlist_xml is not None and db.playlist_xml.modified:
        db.playlist_xml.save()
    db.close()

    print(f"\nDone. Restored {moved} tracks to AUSGEsortiert.")
    print("Rekordbox was NOT started.")
    if missing:
        print(f"Not found in target playlists ({len(missing)}):")
        for item in missing:
            print(f"  - {item}")
    return 0 if not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
