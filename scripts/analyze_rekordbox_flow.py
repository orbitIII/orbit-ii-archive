#!/usr/bin/env python3
"""Learn measurable FLOW rules from Rekordbox playlist exports (XML or txt)."""

from __future__ import annotations

import csv
import json
import math
import statistics
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_XML = Path(
    "/Users/alanwillson/Documents/rekordbox/CueConv/Export Log 6.8.1.0042 2026-06-05.xml"
)
DEFAULT_TXT_DIR = Path(
    "/Users/alanwillson/Documents/rekordbox/CueConv/RB LIBARY TEXT"
)
COMPARISON_REPORT_MD = ROOT / "FLOW_COMPARISON_REPORT.md"

PLAYLIST_CANDIDATES = ["FLOW", "flow", "DRIVING FLOW"]

TXT_PLAYLISTS = [
    {"slug": "orbit_flow", "names": ["ORBIT FLOW"], "label": "ORBIT FLOW"},
    {"slug": "driving_flow", "names": ["DRIVING FLOW"], "label": "DRIVING FLOW (SYSTEM)"},
]


@dataclass
class Track:
    track_id: str
    name: str
    artist: str
    label: str
    genre: str
    bpm: float | None
    key: str
    album: str
    mix: str


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def find_txt_export(txt_dir: Path, names: list[str]) -> Path | None:
    if not txt_dir.is_dir():
        return None
    normalized = {name.strip().casefold(): name for name in names}
    for path in txt_dir.glob("*.txt"):
        key = path.stem.strip().casefold()
        if key in normalized:
            return path
    return None


def txt_encoding(path: Path) -> str:
    with path.open("rb") as handle:
        bom = handle.read(2)
    if bom in (b"\xff\xfe", b"\xfe\xff"):
        return "utf-16"
    return "utf-8"


def load_tracks_from_txt(txt_path: Path) -> list[Track]:
    tracks: list[Track] = []
    with txt_path.open(newline="", encoding=txt_encoding(txt_path)) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for idx, row in enumerate(reader, start=1):
            tracks.append(
                Track(
                    track_id=str(idx),
                    name=(row.get("Track Title") or "").strip(),
                    artist=(row.get("Artist") or "").strip(),
                    label=(row.get("Label") or "").strip(),
                    genre=(row.get("Genre") or "").strip(),
                    bpm=parse_float(row.get("BPM")),
                    key=(row.get("Key") or "").strip(),
                    album="",
                    mix="",
                )
            )
    return tracks


def load_tracks(xml_path: Path) -> dict[str, Track]:
    tree = ET.parse(xml_path)
    tracks: dict[str, Track] = {}
    for elem in tree.findall(".//COLLECTION/TRACK"):
        tid = elem.attrib.get("TrackID", "")
        if not tid:
            continue
        tracks[tid] = Track(
            track_id=tid,
            name=elem.attrib.get("Name", ""),
            artist=elem.attrib.get("Artist", ""),
            label=elem.attrib.get("Label", ""),
            genre=elem.attrib.get("Genre", ""),
            bpm=parse_float(elem.attrib.get("AverageBpm")),
            key=elem.attrib.get("Tonality", "").strip(),
            album=elem.attrib.get("Album", ""),
            mix=elem.attrib.get("Mix", ""),
        )
    return tracks


def find_playlist_node(root: ET.Element, names: list[str]) -> tuple[str, ET.Element] | None:
    for name in names:
        for node in root.findall(".//NODE"):
            if node.attrib.get("Name") == name and node.attrib.get("Type") == "1":
                return name, node
    return None


def playlist_track_ids(node: ET.Element) -> list[str]:
    return [t.attrib["Key"] for t in node.findall("./TRACK") if t.attrib.get("Key")]


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = (len(ordered) - 1) * p
    lo = math.floor(idx)
    hi = math.ceil(idx)
    if lo == hi:
        return ordered[int(idx)]
    return ordered[lo] * (hi - idx) + ordered[hi] * (idx - lo)


def top_share(counter: Counter, key: str, top_n: int) -> float:
    if not counter:
        return 0.0
    top = {k for k, _ in counter.most_common(top_n)}
    return 1.0 if key in top else 0.0


def build_profile(tracks: list[Track]) -> dict:
    bpms = [t.bpm for t in tracks if t.bpm is not None]
    keys = Counter(t.key or "unknown" for t in tracks)
    genres = Counter(t.genre or "unknown" for t in tracks)
    artists = Counter(t.artist or "unknown" for t in tracks)
    labels = Counter(t.label or "unknown" for t in tracks)

    profile = {
        "track_count": len(tracks),
        "bpm": {
            "min": min(bpms) if bpms else None,
            "max": max(bpms) if bpms else None,
            "mean": round(statistics.mean(bpms), 2) if bpms else None,
            "median": round(statistics.median(bpms), 2) if bpms else None,
            "stdev": round(statistics.pstdev(bpms), 2) if len(bpms) > 1 else 0.0,
            "p10": round(percentile(bpms, 0.10), 2) if bpms else None,
            "p90": round(percentile(bpms, 0.90), 2) if bpms else None,
        },
        "keys_top10": keys.most_common(10),
        "genres_top15": genres.most_common(15),
        "artists_top20": artists.most_common(20),
        "labels_top20": labels.most_common(20),
        "key_unique": len(keys),
        "genre_unique": len(genres),
        "artist_unique": len(artists),
        "label_unique": len(labels),
    }
    return profile


def derive_rules(profile: dict, playlist_label: str) -> list[dict]:
    bpm = profile["bpm"]
    rules: list[dict] = []
    if bpm["p10"] is not None and bpm["p90"] is not None:
        rules.append(
            {
                "id": "bpm_within_p10_p90",
                "type": "numeric_range",
                "field": "bpm",
                "min": bpm["p10"],
                "max": bpm["p90"],
                "weight": 0.30,
                "description": (
                    f"BPM between {bpm['p10']} and {bpm['p90']} ({playlist_label} p10–p90)"
                ),
            }
        )
    top_genres = [g for g, _ in profile["genres_top15"][:8]]
    rules.append(
        {
            "id": "genre_in_top8",
            "type": "categorical_set",
            "field": "genre",
            "allowed": top_genres,
            "weight": 0.25,
            "description": f"Genre matches one of the 8 most frequent {playlist_label} genres",
        }
    )
    top_keys = [k for k, _ in profile["keys_top10"][:8]]
    rules.append(
        {
            "id": "key_in_top8",
            "type": "categorical_set",
            "field": "key",
            "allowed": top_keys,
            "weight": 0.15,
            "description": f"Tonality matches one of the 8 most frequent {playlist_label} keys",
        }
    )
    top_labels = [label for label, _ in profile["labels_top20"][:15]]
    rules.append(
        {
            "id": "label_in_top15",
            "type": "categorical_set",
            "field": "label",
            "allowed": top_labels,
            "weight": 0.15,
            "description": f"Label matches one of the 15 most frequent {playlist_label} labels",
        }
    )
    top_artists = {artist for artist, _ in profile["artists_top20"][:25]}
    rules.append(
        {
            "id": "artist_in_flow_corpus",
            "type": "artist_membership",
            "field": "artist",
            "allowed": sorted(top_artists),
            "weight": 0.15,
            "description": (
                f"Artist appears among top-25 {playlist_label} artists or exact match in corpus"
            ),
        }
    )
    return rules


def score_track(track: Track, profile: dict, rules: list[dict], all_artists: set[str]) -> dict:
    matched: list[str] = []
    failed: list[str] = []
    weighted = 0.0
    total_weight = sum(r["weight"] for r in rules)

    for rule in rules:
        rid = rule["id"]
        weight = rule["weight"]
        ok = False
        if rule["type"] == "numeric_range":
            if track.bpm is not None and rule["min"] <= track.bpm <= rule["max"]:
                ok = True
        elif rule["type"] == "categorical_set":
            val = getattr(track, rule["field"]) or "unknown"
            ok = val in rule["allowed"]
        elif rule["type"] == "artist_membership":
            val = track.artist or "unknown"
            ok = val in rule["allowed"] or val in all_artists
        if ok:
            matched.append(rid)
            weighted += weight
        else:
            failed.append(rid)

    confidence = round(100 * weighted / total_weight, 1) if total_weight else 0.0
    bpm = profile["bpm"]
    outlier_reasons: list[str] = []
    if confidence < 55:
        outlier_reasons.append("low_confidence")
    if track.bpm is not None and bpm["min"] is not None:
        if track.bpm < bpm["p10"] or track.bpm > bpm["p90"]:
            outlier_reasons.append("bpm_outside_p10_p90")
    genre_counts = dict(profile["genres_top15"])
    if track.genre and track.genre not in {g for g, _ in profile["genres_top15"]}:
        outlier_reasons.append("genre_outside_top15")
    if track.genre and genre_counts.get(track.genre, 0) == 1:
        outlier_reasons.append("singleton_genre_in_flow")

    return {
        "track_id": track.track_id,
        "name": track.name,
        "artist": track.artist,
        "label": track.label,
        "genre": track.genre,
        "bpm": track.bpm if track.bpm is not None else "",
        "key": track.key,
        "confidence_score": confidence,
        "is_outlier": "yes" if outlier_reasons else "no",
        "outlier_reasons": "; ".join(outlier_reasons),
        "rules_matched": "; ".join(matched),
        "rules_failed": "; ".join(failed),
    }


def write_report(
    playlist_name: str,
    source_path: Path,
    profile: dict,
    rules: list[dict],
    scores: list[dict],
    report_path: Path,
    rules_json_path: Path,
    scores_csv_path: Path,
    note: str | None = None,
) -> None:
    outliers = [s for s in scores if s["is_outlier"] == "yes"]
    lines = [
        f"# {playlist_name} Analysis Report",
        "",
        f"Source: `{source_path}`",
        f"Playlist analyzed: **{playlist_name}**",
        "",
    ]
    if note:
        lines.extend([f"> {note}", ""])
    lines.extend(
        [
            "## Corpus",
            "",
            f"- Tracks in playlist: {profile['track_count']}",
            f"- Unique artists: {profile['artist_unique']}",
            f"- Unique labels: {profile['label_unique']}",
            f"- Unique genres (Rekordbox tags): {profile['genre_unique']}",
            f"- Unique keys: {profile['key_unique']}",
            "",
            "## BPM (measurable)",
            "",
            f"- Range: {profile['bpm']['min']} – {profile['bpm']['max']}",
            f"- Mean / median: {profile['bpm']['mean']} / {profile['bpm']['median']}",
            f"- p10 – p90: {profile['bpm']['p10']} – {profile['bpm']['p90']}",
            f"- Stdev: {profile['bpm']['stdev']}",
            "",
            "## Top genres (Rekordbox field, no reinterpretation)",
            "",
        ]
    )
    for genre, count in profile["genres_top15"]:
        pct = round(100 * count / profile["track_count"], 1)
        lines.append(f"- {genre}: {count} ({pct}%)")
    lines.extend(["", "## Top keys", ""])
    for key, count in profile["keys_top10"]:
        lines.append(f"- {key}: {count}")
    lines.extend(["", "## Top labels", ""])
    for label, count in profile["labels_top20"][:15]:
        lines.append(f"- {label}: {count}")
    lines.extend(["", "## Top artists", ""])
    for artist, count in profile["artists_top20"][:15]:
        lines.append(f"- {artist}: {count}")
    lines.extend(["", "## Derived rules (for auto-scoring new tracks)", ""])
    for rule in rules:
        lines.append(f"- **{rule['id']}** (weight {int(rule['weight']*100)}%): {rule['description']}")
    lines.extend(
        [
            "",
            f"## Outliers in current {playlist_name} folder",
            "",
            f"- Count: {len(outliers)} / {len(scores)}",
            "",
        ]
    )
    for row in sorted(outliers, key=lambda r: r["confidence_score"])[:20]:
        lines.append(
            f"- {row['confidence_score']}% | {row['artist']} — {row['name']} "
            f"| BPM {row['bpm']} | {row['genre']} | {row['outlier_reasons']}"
        )
    lines.extend(
        [
            "",
            "## Usage",
            "",
            f"Use `{rules_json_path.name}` + `{scores_csv_path.name}` to score candidate tracks.",
            "No subjective genre labels are added; only Rekordbox metadata fields are used.",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_outputs(
    slug: str,
    playlist_label: str,
    source_path: Path,
    tracks: list[Track],
    note: str | None = None,
) -> dict:
    profile = build_profile(tracks)
    rules = derive_rules(profile, playlist_label)
    all_artists = {track.artist for track in tracks if track.artist}
    scores = [score_track(track, profile, rules, all_artists) for track in tracks]
    scores.sort(key=lambda r: r["confidence_score"])

    rules_json = ROOT / f"{slug}_profile_rules.json"
    scores_csv = ROOT / f"{slug}_track_scores.csv"
    report_md = ROOT / f"{slug.upper()}_ANALYSIS_REPORT.md"

    rules_json.write_text(
        json.dumps(
            {
                "source": str(source_path),
                "playlist_name": playlist_label,
                "profile": profile,
                "rules": rules,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    fieldnames = [
        "track_id",
        "name",
        "artist",
        "label",
        "genre",
        "bpm",
        "key",
        "confidence_score",
        "is_outlier",
        "outlier_reasons",
        "rules_matched",
        "rules_failed",
    ]
    with scores_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scores)

    write_report(
        playlist_label,
        source_path,
        profile,
        rules,
        scores,
        report_md,
        rules_json,
        scores_csv,
        note=note,
    )

    outliers = sum(1 for row in scores if row["is_outlier"] == "yes")
    return {
        "slug": slug,
        "label": playlist_label,
        "source": source_path,
        "track_count": len(tracks),
        "outliers": outliers,
        "profile": profile,
        "scores": scores,
        "rules_json": rules_json,
        "scores_csv": scores_csv,
        "report_md": report_md,
    }


def overlap_count(items_a: list[tuple[str, int]], items_b: list[tuple[str, int]], top_n: int) -> int:
    set_a = {key for key, _ in items_a[:top_n]}
    set_b = {key for key, _ in items_b[:top_n]}
    return len(set_a & set_b)


def write_comparison_report(results: list[dict]) -> None:
    by_slug = {result["slug"]: result for result in results}
    orbit = by_slug["orbit_flow"]
    driving = by_slug["driving_flow"]
    orbit_profile = orbit["profile"]
    driving_profile = driving["profile"]

    orbit_artists = {row["artist"].casefold() for row in orbit["scores"]}
    driving_artists = {row["artist"].casefold() for row in driving["scores"]}
    shared_artists = sorted(
        {
            row["artist"]
            for row in orbit["scores"]
            if row["artist"].casefold() in driving_artists
        },
        key=str.casefold,
    )

    lines = [
        "# ORBIT FLOW vs DRIVING FLOW — Comparison Report",
        "",
        "Measurable Rekordbox metadata only (BPM, genre tags, keys, labels, artists).",
        "No subjective DNA or vibe claims.",
        "",
        "## Sources",
        "",
        f"- **ORBIT FLOW**: `{orbit['source']}` ({orbit['track_count']} tracks)",
        f"- **DRIVING FLOW (SYSTEM)**: `{driving['source']}` ({driving['track_count']} tracks)",
        "",
        "## Corpus size",
        "",
        f"| | ORBIT FLOW | DRIVING FLOW |",
        f"|---|---:|---:|",
        f"| Tracks | {orbit_profile['track_count']} | {driving_profile['track_count']} |",
        f"| Unique artists | {orbit_profile['artist_unique']} | {driving_profile['artist_unique']} |",
        f"| Unique labels | {orbit_profile['label_unique']} | {driving_profile['label_unique']} |",
        f"| Unique genres | {orbit_profile['genre_unique']} | {driving_profile['genre_unique']} |",
        f"| Unique keys | {orbit_profile['key_unique']} | {driving_profile['key_unique']} |",
        "",
        "## BPM",
        "",
        f"| | ORBIT FLOW | DRIVING FLOW |",
        f"|---|---:|---:|",
    ]
    for key in ("min", "max", "mean", "median", "p10", "p90", "stdev"):
        lines.append(
            f"| {key} | {orbit_profile['bpm'][key]} | {driving_profile['bpm'][key]} |"
        )
    lines.extend(
        [
            "",
            "## Genre overlap (top tags)",
            "",
            f"- Shared genres in top 8: {overlap_count(orbit_profile['genres_top15'], driving_profile['genres_top15'], 8)} / 8",
            f"- Shared genres in top 15: {overlap_count(orbit_profile['genres_top15'], driving_profile['genres_top15'], 15)} / 15",
            "",
            "### ORBIT FLOW top genres",
            "",
        ]
    )
    for genre, count in orbit_profile["genres_top15"][:10]:
        pct = round(100 * count / orbit_profile["track_count"], 1)
        lines.append(f"- {genre}: {count} ({pct}%)")
    lines.extend(["", "### DRIVING FLOW top genres", ""])
    for genre, count in driving_profile["genres_top15"][:10]:
        pct = round(100 * count / driving_profile["track_count"], 1)
        lines.append(f"- {genre}: {count} ({pct}%)")

    lines.extend(
        [
            "",
            "## Key overlap",
            "",
            f"- Shared keys in top 8: {overlap_count(orbit_profile['keys_top10'], driving_profile['keys_top10'], 8)} / 8",
            "",
            "### ORBIT FLOW top keys",
            "",
        ]
    )
    for key, count in orbit_profile["keys_top10"][:8]:
        lines.append(f"- {key}: {count}")
    lines.extend(["", "### DRIVING FLOW top keys", ""])
    for key, count in driving_profile["keys_top10"][:8]:
        lines.append(f"- {key}: {count}")

    lines.extend(
        [
            "",
            "## Artist overlap",
            "",
            f"- Shared artists (exact match): {len(shared_artists)}",
            "",
        ]
    )
    for artist in shared_artists[:20]:
        lines.append(f"- {artist}")

    lines.extend(
        [
            "",
            "## Outliers",
            "",
            f"- ORBIT FLOW: {orbit['outliers']} / {orbit['track_count']}",
            f"- DRIVING FLOW: {driving['outliers']} / {driving['track_count']}",
            "",
            "## Output files",
            "",
            f"- `{orbit['rules_json'].name}`, `{orbit['scores_csv'].name}`, `{orbit['report_md'].name}`",
            f"- `{driving['rules_json'].name}`, `{driving['scores_csv'].name}`, `{driving['report_md'].name}`",
            "",
        ]
    )
    COMPARISON_REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def analyze_txt_playlists(txt_dir: Path) -> int:
    results: list[dict] = []
    for spec in TXT_PLAYLISTS:
        txt_path = find_txt_export(txt_dir, spec["names"])
        if txt_path is None:
            print(f"Missing txt export for {spec['label']} in {txt_dir}", file=sys.stderr)
            return 1
        tracks = load_tracks_from_txt(txt_path)
        if not tracks:
            print(f"No tracks parsed from {txt_path}", file=sys.stderr)
            return 1
        results.append(
            write_outputs(spec["slug"], spec["label"], txt_path, tracks)
        )

    write_comparison_report(results)

    for result in results:
        print(
            f"Analyzed {result['track_count']} tracks from '{result['label']}'. "
            f"Outliers: {result['outliers']}. "
            f"Wrote {result['scores_csv'].name}, {result['rules_json'].name}, {result['report_md'].name}"
        )
    print(f"Wrote {COMPARISON_REPORT_MD.name}")
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("--txt", "--txt-dir"):
        txt_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_TXT_DIR
        return analyze_txt_playlists(txt_dir)

    if DEFAULT_TXT_DIR.is_dir() and find_txt_export(DEFAULT_TXT_DIR, ["ORBIT FLOW"]):
        return analyze_txt_playlists(DEFAULT_TXT_DIR)

    xml_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_XML
    if not xml_path.exists():
        print(f"Missing export: {xml_path}", file=sys.stderr)
        return 1

    tree = ET.parse(xml_path)
    root = tree.getroot()
    all_tracks = load_tracks(xml_path)

    found = find_playlist_node(root, PLAYLIST_CANDIDATES)
    if not found:
        print("No FLOW playlist found", file=sys.stderr)
        return 1
    playlist_name, node = found
    exact_flow = playlist_name == "FLOW"

    ids = playlist_track_ids(node)
    flow_tracks = [all_tracks[i] for i in ids if i in all_tracks]
    missing = len(ids) - len(flow_tracks)
    if missing:
        print(f"Warning: {missing} playlist keys missing from collection", file=sys.stderr)

    note = None
    if not exact_flow:
        note = (
            "No Rekordbox playlist named exactly `FLOW` was found in the export. "
            "Analysis uses the closest match `DRIVING FLOW`."
        )

    result = write_outputs(
        "driving_flow",
        playlist_name,
        xml_path,
        flow_tracks,
        note=note,
    )
    print(
        f"Analyzed {result['track_count']} tracks from '{result['label']}'. "
        f"Outliers: {result['outliers']}. "
        f"Wrote {result['scores_csv'].name}, {result['rules_json'].name}, {result['report_md'].name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
