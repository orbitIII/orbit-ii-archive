#!/usr/bin/env python3
"""Merge raw following export into marquardt_aesthetic_profiles.csv with cluster heuristics."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES_CSV = ROOT / "marquardt_aesthetic_profiles.csv"
CLUSTERS_JSON = ROOT / "marquardt_aesthetic_clusters.json"
RAW_JSON = ROOT / "marquardt_following_raw.json"

# Handles always skipped (noise / system)
SKIP_HANDLES = {
    "svenmarquardt",
    "instagram",
    "meta",
    "threads",
}

# Known handle -> cluster (explicit overrides from research)
KNOWN: dict[str, tuple[str, str | None, int, str]] = {
    "ingegrognard": ("fashion_pfw", "gallery_photo", 90, "makeup_artist;margiela;balenciaga;dark-beauty"),
    "soderbergofficial": ("fashion_berlin", None, 86, "avant-garde;leather;berlin-design"),
    "richertbeil": ("fashion_berlin", None, 85, "inclusive-fashion;gender-fluid;berlin"),
    "sabine_roethig": ("fashion_pfw", "pr_editorial", 84, "fashion-journalist;pfw;street-style"),
    "iamlucaeck": ("music_model", "club_techno", 82, "industrial-techno;leather;berlin"),
    "korbinianglacier": ("music_model", None, 72, "drummer;berlin"),
    "salty.nacho": ("music_model", "fashion_berlin", 80, "metal;rockstar-fashion;berlin"),
    "numero_netherlands": ("fashion_pfw", "fashion_berlin", 82, "numero;editorial;berlin-events"),
    "studioxnoire": ("gallery_photo", None, 78, "la-gallery;c24;marquardt-event"),
    "flieder_und_beton": ("weak_signal", None, 62, "softmotiv;berlin-events"),
    "kaiser_ksr": ("weak_signal", None, 60, "needs_review"),
}

RULES: list[tuple[str, str, str | None, int, str]] = [
    (r"berghain|ostgut|techno|klubnacht|weeeirdos|khidi|griessm", "club_techno", None, 80, "berlin-club"),
    (r"galerie|gallery|museum|deschler|deichtor|exhibition|photo(graph)?", "gallery_photo", None, 78, "gallery-photo"),
    (r"pfw|paris.?fashion|street.?style|runway|antonioli|styleograph|numero", "fashion_pfw", None, 76, "fashion-pfw"),
    (r"platte|voostore|concept.?store|berlin.?fashion|atelier|raufaser|richert|soderberg", "fashion_berlin", None, 76, "berlin-fashion"),
    (r"bold|kinfolk|editorial|magazine|pr\b|agency", "pr_editorial", None, 74, "editorial"),
    (r"dj\b|producer|musician|band\b|model", "music_model", None, 72, "music-model"),
    (r"studio.?1111|immersive|nachts", "art_club", "club_techno", 82, "art-club"),
]


def classify(handle: str, name: str, bio: str) -> tuple[str, str | None, int, str]:
    h = handle.lower()
    if h in KNOWN:
        primary, secondary, score, tags = KNOWN[h]
        return primary, secondary, score, tags

    text = f"{handle} {name} {bio}".lower()
    for pattern, primary, secondary, score, tags in RULES:
        if re.search(pattern, text):
            return primary, secondary, score, tags

    return "weak_signal", None, 60, "needs_review"


def load_existing(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return {row["handle"]: row for row in csv.DictReader(f)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=RAW_JSON)
    parser.add_argument("--min-score", type=int, default=70, help="Skip weak_signal below this score")
    parser.add_argument("--include-weak", action="store_true", help="Also add weak_signal rows")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Missing {args.input}. Run extract_marquardt_following.py first.")
        return 1

    raw = json.loads(args.input.read_text(encoding="utf-8"))
    existing = load_existing(PROFILES_CSV)
    fieldnames = list(next(csv.DictReader(PROFILES_CSV.open(encoding="utf-8"))).keys()) if PROFILES_CSV.exists() else [
        "handle", "name", "cluster_primary", "cluster_secondary", "source", "role", "cities",
        "photo_aesthetic", "video_aesthetic", "fashion_aesthetic", "mood",
        "connection_to_marquardt", "proximity_score", "match_tags", "notes", "url",
    ]

    added = 0
    updated = 0
    for item in raw.get("handles", []):
        handle = item["handle"]
        if handle.lower() in SKIP_HANDLES:
            continue

        primary, secondary, score, tags = classify(handle, item.get("name", ""), item.get("bio", ""))
        if primary == "weak_signal" and score < args.min_score and not args.include_weak:
            continue

        row = existing.get(handle, {})
        is_new = handle not in existing
        row.setdefault("handle", handle)
        row["name"] = item.get("name") or row.get("name", handle)
        row["cluster_primary"] = primary
        if secondary:
            row["cluster_secondary"] = secondary
        row["source"] = "following" if is_new else (row.get("source", "") + ";following").strip(";")
        row["connection_to_marquardt"] = "marquardt_following"
        row["proximity_score"] = str(score)
        row["match_tags"] = tags
        row["notes"] = row.get("notes") or f"From following export ({raw.get('extracted', '')})"
        row["url"] = f"https://www.instagram.com/{handle}/"
        existing[handle] = row
        added += int(is_new)
        updated += int(not is_new)

    rows = sorted(existing.values(), key=lambda r: (-int(r.get("proximity_score") or 0), r["handle"]))
    with PROFILES_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    # refresh cluster handle lists
    if CLUSTERS_JSON.exists():
        clusters = json.loads(CLUSTERS_JSON.read_text(encoding="utf-8"))
        for c in clusters.get("clusters", {}).values():
            c["handles"] = []
        for row in rows:
            primary = row.get("cluster_primary")
            secondary = row.get("cluster_secondary")
            if primary in clusters.get("clusters", {}):
                clusters["clusters"][primary]["handles"].append(row["handle"])
            if secondary in clusters.get("clusters", {}):
                clusters["clusters"][secondary]["handles"].append(row["handle"])
        for c in clusters.get("clusters", {}).values():
            c["handles"] = sorted(set(c["handles"]))
        clusters["updated"] = raw.get("extracted", clusters.get("updated"))
        CLUSTERS_JSON.write_text(json.dumps(clusters, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Profiles: {len(rows)} total, +{added} new, ~{updated} updated from following")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
