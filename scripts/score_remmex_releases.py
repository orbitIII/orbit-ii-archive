#!/usr/bin/env python3
"""Score Remmex release export against ORBIT playlist profiles."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_rekordbox_flow import Track, derive_rules, score_track  # noqa: E402

GENRE_RE = re.compile(
    r"\b(afro house|tech house|deep house|minimal / deep tech|melodic house/techno|"
    r"progressive|indie dance|house|techno \(peak time/driving/hard\)|"
    r"techno \(raw/deep/hypnotic\)|minimal|deep tech|electronica|garage|"
    r"electro house|organic house / downtempo|dj tools|nu disco|jackin house|"
    r"amapiano|hard techno|trance|breaks|drum & bass|dubstep|pop / dance|chill out)\b",
    re.I,
)
TRACK_RE = re.compile(r"^(.+?) - (.+)$")


def parse_release_row(raw: str, zip_url: str = "", display_id: str = "") -> dict:
    text = " ".join(raw.split())
    if not display_id:
        m = re.search(r"#(\d+)", text)
        display_id = m.group(1) if m else ""

    tail = text
    release_title = ""
    label = ""
    if " F ZIP " in text:
        head, tail = text.split(" F ZIP ", 1)
        head_clean = re.sub(r"^#\d+REPORT ISSUE \d+ \w+ ", "", head)
        # label is usually last chunk before F ZIP; title before label
        m = re.match(r"^(.+?)\s+([A-Za-z0-9][A-Za-z0-9 &'().-]+)$", head_clean)
        if m:
            release_title, label = m.group(1).strip(), m.group(2).strip()
    elif " ZIP " in text:
        parts = text.split(" ZIP ", 1)
        tail = parts[1] if len(parts) > 1 else text

    segments = [s.strip() for s in tail.split(" MP3 ") if s.strip()]
    tracks: list[dict] = []
    genres: list[str] = []

    for segment in segments:
        genre_match = None
        for gm in GENRE_RE.finditer(segment):
            genre_match = gm
        genre = genre_match.group(1).lower() if genre_match else ""
        if genre:
            genres.append(genre)
        body = segment[: genre_match.start()].strip() if genre_match else segment.strip()
        tm = TRACK_RE.match(body)
        if tm:
            tracks.append(
                {
                    "artist": tm.group(1).strip(),
                    "title": tm.group(2).strip(),
                    "genre": genre,
                }
            )

    return {
        "display_id": display_id,
        "zip_url": zip_url,
        "release_title": release_title,
        "label": label,
        "tracks": tracks,
        "genres": sorted(set(genres)),
        "raw": text,
    }


def load_profile(slug: str) -> tuple[dict, list[dict], set[str]]:
    data = json.loads((ROOT / f"{slug}_profile_rules.json").read_text(encoding="utf-8"))
    profile = data["profile"]
    rules = data["rules"]
    artists = {artist for artist, _ in profile["artists_top20"]}
    return profile, rules, artists


def score_releases(releases: list[dict], profile_slug: str, *, ignore_bpm: bool = True) -> list[dict]:
    profile, rules, corpus_artists = load_profile(profile_slug)
    if ignore_bpm:
        rules = [r for r in rules if r["id"] != "bpm_within_p10_p90"]
        total = sum(r["weight"] for r in rules)
        rules = [{**r, "weight": r["weight"] / total} for r in rules]

    rows: list[dict] = []
    for release in releases:
        for track in release["tracks"]:
            genre = track.get("genre", "")
            genre_norm = genre.title() if genre == genre.lower() else genre
            # Remmex lowercase tags → Rekordbox-style casing for rule match
            genre_map = {
                "house": "House",
                "tech house": "Tech House",
                "deep house": "Deep House",
                "minimal / deep tech": "Minimal / Deep Tech",
                "minimal": "Minimal",
                "techno (raw/deep/hypnotic)": "Techno (Raw / Deep / Hypnotic)",
                "techno (peak time/driving/hard)": "Techno (Peak Time / Driving)",
            }
            genre_rek = genre_map.get(genre.lower(), genre_norm)

            t = Track(
                track_id=release.get("display_id", ""),
                name=track["title"],
                artist=track["artist"],
                label=release.get("label", ""),
                genre=genre_rek,
                bpm=None,
                key="",
                album=release.get("release_title", ""),
                mix="",
            )
            scored = score_track(t, profile, rules, corpus_artists)
            rows.append(
                {
                    "display_id": release.get("display_id", ""),
                    "zip_url": release.get("zip_url", ""),
                    "artist": track["artist"],
                    "title": track["title"],
                    "genre": genre,
                    "confidence_score": scored["confidence_score"],
                    "is_match": "yes" if scored["confidence_score"] >= 70 else "maybe"
                    if scored["confidence_score"] >= 55
                    else "no",
                    "outlier_reasons": scored["outlier_reasons"],
                    "profile": profile_slug,
                }
            )
    rows.sort(key=lambda r: (-r["confidence_score"], r["artist"], r["title"]))
    return rows


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: score_remmex_releases.py RELEASES.json [--profile orbit_core]", file=sys.stderr)
        return 1

    src = Path(sys.argv[1])
    profile_slug = "orbit_core"
    if "--profile" in sys.argv:
        profile_slug = sys.argv[sys.argv.index("--profile") + 1]

    payload = json.loads(src.read_text(encoding="utf-8"))
    releases = payload if isinstance(payload, list) else payload.get("releases", [])
    parsed = []
    for row in releases:
        if "tracks" in row and row["tracks"]:
            parsed.append(row)
        else:
            parsed.append(
                parse_release_row(
                    row.get("raw", ""),
                    row.get("zip_url", ""),
                    row.get("display_id", ""),
                )
            )

    scored = score_releases(parsed, profile_slug)
    out_csv = src.with_name(src.stem + f"_scored_{profile_slug}.csv")
    out_json = src.with_name(src.stem + f"_top_{profile_slug}.json")

    fieldnames = [
        "display_id",
        "zip_url",
        "artist",
        "title",
        "genre",
        "confidence_score",
        "is_match",
        "outlier_reasons",
        "profile",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scored)

    top = [r for r in scored if r["confidence_score"] >= 70][:50]
    out_json.write_text(json.dumps(top, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Scored {len(scored)} tracks from {len(parsed)} releases.")
    print(f"Matches ≥70%: {sum(1 for r in scored if r['confidence_score'] >= 70)}")
    print(f"Wrote {out_csv.name}, {out_json.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
