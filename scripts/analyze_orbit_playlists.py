#!/usr/bin/env python3
"""Analyze ORBIT Rekordbox playlists (live DB or txt exports)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_rekordbox_flow import (  # noqa: E402
    DEFAULT_TXT_DIR,
    Track,
    find_txt_export,
    load_tracks_from_txt,
    overlap_count,
    write_outputs,
)
from rekordbox_orbit import (  # noqa: E402
    export_playlist_snapshot,
    find_playlist_db,
    load_config,
    open_db,
    playlist_specs,
    spec_by_slug,
)


def load_tracks_from_db(spec: dict) -> tuple[list[Track], Path, str | None]:
    db = open_db()
    parent = spec.get("parent")
    playlist = None
    for name in spec["names"]:
        playlist = find_playlist_db(db, name, parent_name=parent)
        if playlist is not None:
            break
    if playlist is None:
        db.close()
        raise FileNotFoundError(
            f"Playlist not found in Rekordbox: {spec['label']} ({spec['names']})"
        )

    export_dir = ROOT / "rekordbox" / "exports"
    snapshot = export_playlist_snapshot(db, playlist, export_dir)

    tracks: list[Track] = []
    for song in sorted(db.get_playlist_songs(PlaylistID=playlist.ID), key=lambda s: s.TrackNo):
        content = db.get_content(ID=song.ContentID)
        tracks.append(
            Track(
                track_id=str(content.ID),
                name=content.Title or "",
                artist=content.ArtistName or "",
                label=content.LabelName or "",
                genre=content.GenreName or "",
                bpm=round(content.BPM / 100, 2) if content.BPM else None,
                key=content.KeyName or "",
                album=content.AlbumName or "",
                mix="",
            )
        )
    note = f"Live Rekordbox DB playlist `{playlist.Name}` ({len(tracks)} tracks)."
    db.close()
    return tracks, snapshot, note


def load_tracks_for_spec(spec: dict, txt_dir: Path) -> tuple[list[Track], Path, str | None]:
    source = spec.get("source", "txt")
    if source == "db":
        return load_tracks_from_db(spec)

    txt_path = None
    for name in spec["names"]:
        txt_path = find_txt_export(txt_dir, [name])
        if txt_path is not None:
            break
    if txt_path is None:
        raise FileNotFoundError(f"Missing txt export for {spec['label']} in {txt_dir}")
    tracks = load_tracks_from_txt(txt_path)
    note = None
    if source == "txt":
        note = (
            f"Txt export may be stale. Prefer source=db for {spec['label']} "
            f"when Rekordbox library is available."
        )
    return tracks, txt_path, note


def write_comparison(a: dict, b: dict, report_path: Path, title: str) -> None:
    ap, bp = a["profile"], b["profile"]
    shared_artists = sorted(
        {
            row["artist"]
            for row in a["scores"]
            if row["artist"].casefold() in {r["artist"].casefold() for r in b["scores"]}
        },
        key=str.casefold,
    )
    lines = [
        f"# {title}",
        "",
        "Measurable Rekordbox metadata only. No subjective DNA claims.",
        "",
        f"- **{a['label']}**: {a['track_count']} tracks",
        f"- **{b['label']}**: {b['track_count']} tracks",
        "",
        "## Corpus",
        "",
        f"| | {a['label']} | {b['label']} |",
        f"|---|---:|---:|",
        f"| Tracks | {ap['track_count']} | {bp['track_count']} |",
        f"| Artists | {ap['artist_unique']} | {bp['artist_unique']} |",
        f"| Labels | {ap['label_unique']} | {bp['label_unique']} |",
        f"| Genres | {ap['genre_unique']} | {bp['genre_unique']} |",
        f"| Keys | {ap['key_unique']} | {bp['key_unique']} |",
        "",
        "## BPM",
        "",
        f"| | {a['label']} | {b['label']} |",
        f"|---|---:|---:|",
    ]
    for key in ("min", "max", "mean", "median", "p10", "p90", "stdev"):
        lines.append(f"| {key} | {ap['bpm'][key]} | {bp['bpm'][key]} |")
    lines.extend(
        [
            "",
            f"- Shared genres (top 8): {overlap_count(ap['genres_top15'], bp['genres_top15'], 8)} / 8",
            f"- Shared keys (top 8): {overlap_count(ap['keys_top10'], bp['keys_top10'], 8)} / 8",
            f"- Shared artists: {len(shared_artists)}",
            "",
            f"## Outliers",
            "",
            f"- {a['label']}: {a['outliers']} / {a['track_count']}",
            f"- {b['label']}: {b['outliers']} / {b['track_count']}",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def analyze_specs(slugs: list[str] | None = None, txt_dir: Path = DEFAULT_TXT_DIR) -> dict[str, dict]:
    results: dict[str, dict] = {}
    specs = playlist_specs()
    if slugs:
        specs = [spec_by_slug(slug) for slug in slugs]

    for spec in specs:
        tracks, source, note = load_tracks_for_spec(spec, txt_dir)
        if not tracks:
            raise RuntimeError(f"No tracks loaded for {spec['label']}")
        result = write_outputs(spec["slug"], spec["label"], source, tracks, note=note)
        results[spec["slug"]] = result
        print(
            f"Analyzed {result['track_count']} tracks from '{result['label']}'. "
            f"Outliers: {result['outliers']}. "
            f"Wrote {result['scores_csv'].name}, {result['rules_json'].name}, {result['report_md'].name}"
        )
    return results


def run_comparisons(results: dict[str, dict]) -> None:
    for comp in load_config().get("comparisons", []):
        if comp["a"] not in results or comp["b"] not in results:
            continue
        report = ROOT / comp["report"]
        write_comparison(results[comp["a"]], results[comp["b"]], report, comp["label"])
        print(f"Wrote {report.name}")


def main() -> int:
    args = sys.argv[1:]
    slugs = None
    txt_dir = DEFAULT_TXT_DIR

    if "--help" in args:
        print("Usage: analyze_orbit_playlists.py [--slug SLUG ...] [--txt-dir PATH] [--all]")
        return 0

    if "--txt-dir" in args:
        txt_dir = Path(args[args.index("--txt-dir") + 1])

    if "--all" in args:
        slugs = [spec["slug"] for spec in playlist_specs()]
    elif "--slug" in args:
        slugs = []
        idx = 0
        while idx < len(args):
            if args[idx] == "--slug":
                slugs.append(args[idx + 1])
                idx += 2
            else:
                idx += 1
    else:
        slugs = ["orbit_core"]

    results = analyze_specs(slugs, txt_dir=txt_dir)
    run_comparisons(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
