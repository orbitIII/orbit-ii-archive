#!/usr/bin/env python3
"""Collect publicly available TrackID CSV exports from the Orbit II archive.

The source archive currently contains TrackID search result rows and a small
number of TrackID audiostream detail URLs in overlap evidence. This collector
does not invent detail or CSV URLs: it only follows URLs already present in the
repository and only records CSV exports if an accessible TrackID page exposes a
CSV link.
"""

from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests


ROOT = Path(__file__).resolve().parents[1]
SET_ARCHIVE = ROOT / "berghain_2024_2026_top50_artist_sets_trackid.csv"
INVENTORY = ROOT / "berghain_2024_2026_trackid_csv_inventory.csv"
MASTER = ROOT / "berghain_2024_2026_trackid_tracks_master.csv"
RAW_DIR = ROOT / "data" / "trackid_csv_raw"

INVENTORY_FIELDS = [
    "top50_artist",
    "set_title",
    "set_url",
    "csv_url",
    "local_csv_path",
    "row_count",
    "status",
    "notes",
]

MASTER_FIELDS = [
    "top50_artist",
    "set_title",
    "set_url",
    "pos",
    "start",
    "end",
    "track_artist",
    "track_title",
    "label",
    "source_csv",
    "confidence",
    "notes",
]

TRACKID_DETAIL_RE = re.compile(r"https://trackid\.net/audiostreams/[A-Za-z0-9_./%+\-]+")
CSV_HREF_RE = re.compile(r"""href=["']([^"']+\.csv(?:\?[^"']*)?)["']""", re.IGNORECASE)
REQUIRED_EXPORT_COLUMNS = ["Pos", "Start", "End", "Artist", "Title", "Label"]


@dataclass(frozen=True)
class SetCandidate:
    top50_artist: str
    set_title: str
    set_url: str
    notes: str


def read_set_archive() -> list[dict[str, str]]:
    with SET_ARCHIVE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def detail_urls_from_repo() -> set[str]:
    urls: set[str] = set()
    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".csv", ".md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        urls.update(match.rstrip(".,);") for match in TRACKID_DETAIL_RE.findall(text))
    return urls


def candidates() -> list[SetCandidate]:
    """Return archive candidates without inventing new set/detail URLs."""
    rows = read_set_archive()
    out: list[SetCandidate] = []

    # The main set archive stores TrackID search URLs, not per-set detail URLs.
    for row in rows:
        out.append(
            SetCandidate(
                top50_artist=row["artist"],
                set_title=row["set_title"],
                set_url=row["source_url"],
                notes="TrackID search result row; no set detail URL stored in archive row.",
            )
        )

    # Add actual TrackID audiostream detail URLs already present elsewhere.
    known_detail_urls = sorted(detail_urls_from_repo())
    title_by_url = {
        "https://trackid.net/audiostreams/answer-code-request-x-gerd-janson-live-ostgut-ton-aus-der-halle-am-berghain-arte-concert": "Answer Code Request X Gerd Janson (live) - Ostgut Ton aus der Halle am Berghain - ARTE Concert",
        "https://trackid.net/audiostreams/nick-hoppner-x-klon-dump-live-ostgut-ton-aus-der-halle-am-berghain-arte-concert": "Nick Höppner X Klon Dump (live) - Ostgut Ton aus der Halle am Berghain - ARTE Concert",
        "https://trackid.net/audiostreams/paramida-x-massimiliano-pagliara-ostgut-ton-halle-am-berghain-live-arteconcert": "Paramida X Massimiliano Pagliara - Ostgut Ton, Halle am Berghain (live) - @arteconcert",
        "https://trackid.net/audiostreams/barker-x-baumecker-live-halle-am-berghain-arte-concert": "Barker X Baumecker (live) - Halle am Berghain - ARTE Concert",
    }
    artist_by_url = {
        "https://trackid.net/audiostreams/answer-code-request-x-gerd-janson-live-ostgut-ton-aus-der-halle-am-berghain-arte-concert": "Gerd Janson",
        "https://trackid.net/audiostreams/nick-hoppner-x-klon-dump-live-ostgut-ton-aus-der-halle-am-berghain-arte-concert": "Nick Höppner",
        "https://trackid.net/audiostreams/paramida-x-massimiliano-pagliara-ostgut-ton-halle-am-berghain-live-arteconcert": "Paramida; Massimiliano Pagliara",
        "https://trackid.net/audiostreams/barker-x-baumecker-live-halle-am-berghain-arte-concert": "nd_baumecker",
    }
    for url in known_detail_urls:
        out.append(
            SetCandidate(
                top50_artist=artist_by_url.get(url, ""),
                set_title=title_by_url.get(url, ""),
                set_url=url,
                notes="TrackID audiostream detail URL found in repository evidence.",
            )
        )

    # De-duplicate exact candidate keys.
    seen: set[tuple[str, str, str]] = set()
    unique: list[SetCandidate] = []
    for candidate in out:
        key = (candidate.top50_artist, candidate.set_title, candidate.set_url)
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
    return unique


def fetch(url: str) -> requests.Response | None:
    try:
        return requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0 (Orbit II research archive)"},
        )
    except requests.RequestException:
        return None


def exposed_csv_urls(page_url: str, html: str) -> list[str]:
    urls: list[str] = []
    for href in CSV_HREF_RE.findall(html):
        absolute = urljoin(page_url, href)
        if urlparse(absolute).netloc.endswith("trackid.net"):
            urls.append(absolute)
    return sorted(set(urls))


def safe_local_name(csv_url: str, content: bytes) -> str:
    parsed = urlparse(csv_url)
    name = Path(parsed.path).name
    if not name.lower().endswith(".csv"):
        digest = hashlib.sha1(csv_url.encode("utf-8")).hexdigest()[:12]
        name = f"trackid_export_{digest}.csv"
    if not name or name == ".csv":
        digest = hashlib.sha1(content).hexdigest()[:12]
        name = f"trackid_export_{digest}.csv"
    return name


def compatible_header(path: Path) -> tuple[bool, list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)
    normalized = {field.strip().lower(): field for field in fields}
    required = [column.lower() for column in REQUIRED_EXPORT_COLUMNS]
    return all(column in normalized for column in required), fields, rows


def canonical_row(row: dict[str, str]) -> dict[str, str]:
    by_lower = {key.strip().lower(): value for key, value in row.items()}
    return {
        "pos": by_lower.get("pos", ""),
        "start": by_lower.get("start", ""),
        "end": by_lower.get("end", ""),
        "track_artist": by_lower.get("artist", ""),
        "track_title": by_lower.get("title", ""),
        "label": by_lower.get("label", ""),
    }


def write_outputs() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    inventory_rows: list[dict[str, str]] = []
    master_rows: list[dict[str, str]] = []

    for candidate in candidates():
        set_url = candidate.set_url.strip()
        is_detail_url = bool(TRACKID_DETAIL_RE.fullmatch(set_url))

        if not is_detail_url:
            inventory_rows.append(
                {
                    "top50_artist": candidate.top50_artist,
                    "set_title": candidate.set_title,
                    "set_url": set_url,
                    "csv_url": "",
                    "local_csv_path": "",
                    "row_count": "",
                    "status": "no_csv_found",
                    "notes": candidate.notes,
                }
            )
            continue

        response = fetch(set_url)
        if response is None:
            inventory_rows.append(
                {
                    "top50_artist": candidate.top50_artist,
                    "set_title": candidate.set_title,
                    "set_url": set_url,
                    "csv_url": "",
                    "local_csv_path": "",
                    "row_count": "",
                    "status": "blocked",
                    "notes": "TrackID detail URL request failed.",
                }
            )
            continue

        if response.status_code in {401, 403, 429} or "Just a moment" in response.text:
            inventory_rows.append(
                {
                    "top50_artist": candidate.top50_artist,
                    "set_title": candidate.set_title,
                    "set_url": set_url,
                    "csv_url": "",
                    "local_csv_path": "",
                    "row_count": "",
                    "status": "blocked",
                    "notes": f"TrackID detail URL blocked or rate-limited; HTTP {response.status_code}.",
                }
            )
            continue

        csv_urls = exposed_csv_urls(set_url, response.text)
        if not csv_urls:
            inventory_rows.append(
                {
                    "top50_artist": candidate.top50_artist,
                    "set_title": candidate.set_title,
                    "set_url": set_url,
                    "csv_url": "",
                    "local_csv_path": "",
                    "row_count": "",
                    "status": "no_csv_found",
                    "notes": "TrackID detail page accessible but no public CSV href found.",
                }
            )
            continue

        for csv_url in csv_urls:
            csv_response = fetch(csv_url)
            if csv_response is None or csv_response.status_code != 200:
                inventory_rows.append(
                    {
                        "top50_artist": candidate.top50_artist,
                        "set_title": candidate.set_title,
                        "set_url": set_url,
                        "csv_url": csv_url,
                        "local_csv_path": "",
                        "row_count": "",
                        "status": "blocked",
                        "notes": "CSV URL was exposed but could not be downloaded.",
                    }
                )
                continue

            local_name = safe_local_name(csv_url, csv_response.content)
            local_path = RAW_DIR / local_name
            if local_path.exists():
                digest = hashlib.sha1(csv_url.encode("utf-8")).hexdigest()[:8]
                local_path = RAW_DIR / f"{local_path.stem}_{digest}{local_path.suffix}"
            local_path.write_bytes(csv_response.content)

            compatible, fields, track_rows = compatible_header(local_path)
            if not compatible:
                inventory_rows.append(
                    {
                        "top50_artist": candidate.top50_artist,
                        "set_title": candidate.set_title,
                        "set_url": set_url,
                        "csv_url": csv_url,
                        "local_csv_path": str(local_path.relative_to(ROOT)),
                        "row_count": "",
                        "status": "invalid_schema",
                        "notes": f"Downloaded CSV header not compatible with {', '.join(REQUIRED_EXPORT_COLUMNS)}. Found: {', '.join(fields)}",
                    }
                )
                continue

            inventory_rows.append(
                {
                    "top50_artist": candidate.top50_artist,
                    "set_title": candidate.set_title,
                    "set_url": set_url,
                    "csv_url": csv_url,
                    "local_csv_path": str(local_path.relative_to(ROOT)),
                    "row_count": str(len(track_rows)),
                    "status": "downloaded",
                    "notes": "Downloaded public TrackID CSV export and validated schema.",
                }
            )

            for track in track_rows:
                canonical = canonical_row(track)
                master_rows.append(
                    {
                        "top50_artist": candidate.top50_artist,
                        "set_title": candidate.set_title,
                        "set_url": set_url,
                        **canonical,
                        "source_csv": str(local_path.relative_to(ROOT)),
                        "confidence": "Medium",
                        "notes": "Imported from public TrackID CSV export.",
                    }
                )

    with INVENTORY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=INVENTORY_FIELDS)
        writer.writeheader()
        writer.writerows(inventory_rows)

    with MASTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MASTER_FIELDS)
        writer.writeheader()
        writer.writerows(master_rows)

    print(f"inventory_rows={len(inventory_rows)}")
    print(f"master_rows={len(master_rows)}")
    print(f"raw_dir={RAW_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    write_outputs()
