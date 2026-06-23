#!/usr/bin/env python3
"""Generate Orbit II archive CSV and note artifacts from the raw Berghain markdown."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "berghain" / "klubnacht_2024_2026.md"

MONTHS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}
STOP_KEYWORDS = {"", "DJ", "Live", "live", "ja", "nein", "[BP]"}
PANORAMA_TERMS = {
    "house",
    "deephouse",
    "deep",
    "groove",
    "grooves",
    "groovig",
    "groovigen",
    "warm",
    "soul",
    "disco",
    "funk",
    "vocal",
    "garage",
    "minimal",
    "dub",
    "chords",
    "closing",
    "warm-up",
    "piano",
    "sample",
}
PUSH_TERMS = {
    "techno",
    "percussive",
    "percussion",
    "tribal",
    "driving",
    "rollend",
    "rolling",
    "acid",
    "electro",
    "breaks",
    "breakbeat",
    "trance",
}
COMMUNITY_TERMS = {
    "collective",
    "kollektiv",
    "community",
    "store",
    "records",
    "recordings",
    "partyreihe",
    "partys",
    "label",
    "labels",
    "resident",
    "residency",
}
TOKEN_RE = re.compile(r"\s*[,;/]\s*")
HEADING_RE = re.compile(
    r"^##[ \t]+(.+?)[ \t]+—[ \t]+(.+?)[ \t]+\|[ \t]+beginn[ \t]+(.+)$",
    re.M,
)


def split_tokens(value: str) -> list[str]:
    """Split multi-value label fields without breaking literal label characters."""
    return [token for token in (part.strip() for part in TOKEN_RE.split(value)) if token not in STOP_KEYWORDS]


def parse_events() -> list[dict]:
    text = SOURCE.read_text(encoding="utf-8")
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        raise ValueError(f"No event headings found in {SOURCE}")

    events: list[dict] = []
    for index, match in enumerate(matches):
        block_start = match.start()
        block_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[block_start:block_end]
        event_title = match.group(1).strip()
        date_label = match.group(2).strip()
        begin = match.group(3).strip()
        date_match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", date_label)
        if not date_match:
            raise ValueError(f"Could not parse date from heading: {match.group(0)}")

        day, month, year = map(int, date_match.groups())
        iso_date = f"{year:04d}-{month:02d}-{day:02d}"
        url_match = re.search(r"^URL:\s*(\S+)\s*$", block, re.M)
        source_url = url_match.group(1) if url_match else "unknown"
        press_match = re.search(r"\*\*Pressetext:\*\*\s*(.*)", block, re.S)
        press_text = " ".join(press_match.group(1).split()) if press_match else "unknown"

        rows: list[dict] = []
        for line in block.splitlines():
            if not re.match(r"^\|\s*\d+\s*\|", line):
                continue
            parts = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(parts) != 7:
                raise ValueError(f"Unexpected table row format in {iso_date}: {line}")
            _, time, room, artist, live, label, keywords = parts
            rows.append(
                {
                    "time": time,
                    "room": room or "unknown",
                    "artist": artist or "unknown",
                    "live": live.lower() == "ja",
                    "label": label.strip(),
                    "keywords": keywords.strip(),
                }
            )

        room_order: list[str] = []
        by_room: dict[str, list[str]] = defaultdict(list)
        labels_keywords: list[str] = []
        for row in rows:
            if row["room"] not in room_order:
                room_order.append(row["room"])
            artist_display = row["artist"] + (
                " (Live)" if row["live"] and "Live" not in row["artist"] else ""
            )
            by_room[row["room"]].append(f"{row['time']} {artist_display}")
            labels_keywords.extend(split_tokens(row["label"]))
            labels_keywords.extend(split_tokens(row["keywords"]))

        artists_per_room = (
            " | ".join(f"{room}: {'; '.join(by_room[room])}" for room in room_order)
            if rows
            else "unknown"
        )
        rooms = "; ".join(room_order) if room_order else "unknown"
        label_counts = Counter(labels_keywords)
        notes = []
        if "Panorama Bar" in room_order:
            pbar_artists = [row["artist"] for row in rows if row["room"] == "Panorama Bar"]
            suffix = f" (+{len(pbar_artists) - 12} more)" if len(pbar_artists) > 12 else ""
            notes.append("Panorama Bar artists: " + "; ".join(pbar_artists[:12]) + suffix)
        else:
            notes.append("Panorama Bar not listed for this event")
        top_labels = [label for label, _ in label_counts.most_common(8)]
        notes.append("Labels/keywords: " + ("; ".join(top_labels) if top_labels else "unknown"))

        events.append(
            {
                "date": iso_date,
                "year": str(year),
                "month": MONTHS[month],
                "event_title": event_title,
                "rooms": rooms,
                "artists_per_room": artists_per_room,
                "press_text": press_text,
                "source_url": source_url,
                "notes": " | ".join(notes),
                "begin": begin,
                "rows": rows,
                "labels": label_counts,
            }
        )
    return events


def write_events_csv(events: list[dict]) -> None:
    with (ROOT / "berghain_2024_2026_events.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Date", "Year", "Month", "EventTitle", "Rooms", "ArtistsPerRoom", "Pressetext", "SourceURL", "Notes"]
        )
        for event in events:
            writer.writerow(
                [
                    event["date"],
                    event["year"],
                    event["month"],
                    event["event_title"],
                    event["rooms"],
                    event["artists_per_room"],
                    event["press_text"],
                    event["source_url"],
                    event["notes"],
                ]
            )


def write_press_csv(events: list[dict]) -> None:
    with (ROOT / "berghain_2024_2026_press_texts.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Event", "Artist", "Location", "PressText", "SourceURL"])
        for event in events:
            writer.writerow(
                [
                    f"{event['event_title']} {event['date']}",
                    "multiple/see event row",
                    event["rooms"],
                    event["press_text"],
                    event["source_url"],
                ]
            )


def build_artist_indexes(events: list[dict]) -> tuple[dict, dict, dict, dict, dict]:
    artist_events = defaultdict(list)
    artist_labels = defaultdict(Counter)
    artist_keywords = defaultdict(Counter)
    artist_rooms = defaultdict(Counter)
    artist_live = defaultdict(bool)
    for event in events:
        for row in event["rows"]:
            artist = row["artist"]
            artist_events[artist].append(event)
            artist_rooms[artist][row["room"]] += 1
            artist_live[artist] = artist_live[artist] or row["live"] or " Live" in artist
            for token in split_tokens(row["label"]):
                artist_labels[artist][token] += 1
            for token in split_tokens(row["keywords"]):
                artist_keywords[artist][token] += 1
    return artist_events, artist_labels, artist_keywords, artist_rooms, artist_live


def write_artist_csvs(events: list[dict]) -> None:
    artist_events, artist_labels, artist_keywords, artist_rooms, artist_live = build_artist_indexes(events)

    with (ROOT / "berghain_2024_2026_artists_raw.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Artist", "Role", "Labels", "NotableEvents", "Notes"])
        for artist in sorted(artist_events, key=lambda name: name.casefold()):
            appearances = artist_events[artist]
            labels = [label for label, _ in artist_labels[artist].most_common()]
            keywords = [keyword for keyword, _ in artist_keywords[artist].most_common() if keyword not in labels]
            room_summary = "; ".join(f"{room} ({count})" for room, count in artist_rooms[artist].most_common())
            notable = "; ".join(
                f"{event['date']} {event['event_title']}" for event in appearances[:5]
            )
            if len(appearances) > 5:
                notable += f"; +{len(appearances) - 5} more"
            notes = f"Rooms: {room_summary}"
            if keywords:
                notes += " | Keywords: " + "; ".join(keywords[:8])
            writer.writerow(
                [
                    artist,
                    "Live" if artist_live[artist] else "DJ",
                    "; ".join(labels) if labels else "unknown",
                    notable,
                    notes,
                ]
            )

    with (ROOT / "berghain_2024_2026_artist_frequency.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Artist", "Appearances", "Years", "PrimaryRooms", "Notes"])
        for artist, appearances in sorted(
            artist_events.items(), key=lambda item: (-len(item[1]), item[0].casefold())
        ):
            years = sorted({event["year"] for event in appearances})
            primary_rooms = "; ".join(room for room, _ in artist_rooms[artist].most_common())
            labels = [label for label, _ in artist_labels[artist].most_common(5)]
            pbar_count = artist_rooms[artist]["Panorama Bar"]
            notes_parts = ["Live" if artist_live[artist] else "DJ"]
            if pbar_count:
                notes_parts.append(f"Panorama Bar appearances: {pbar_count}")
            if labels:
                notes_parts.append("Labels/keywords: " + "; ".join(labels))
            writer.writerow([artist, len(appearances), "; ".join(years), primary_rooms, " | ".join(notes_parts)])


def event_tags(event: dict) -> list[str]:
    combined = " ".join(
        [event["press_text"].lower()]
        + [row["label"].lower() + " " + row["keywords"].lower() for row in event["rows"]]
    )
    tags = []
    if any(term in combined for term in PANORAMA_TERMS):
        tags.append("Flow")
    if any(term in combined for term in PUSH_TERMS):
        tags.append("Push")
    if "vocal" in combined or "sample" in combined or "soul" in combined:
        tags.append("moment_vocal")
    if "deep" in combined or "dub" in combined or "ambient" in combined:
        tags.append("moment_deep")
    if "driving" in combined or "tribal" in combined or "acid" in combined or "break" in combined:
        tags.append("moment_driving")
    return tags or ["unknown"]


def build_signal_counters(events: list[dict]) -> tuple[Counter, Counter, Counter]:
    pbar_label_counter = Counter()
    room_counter = Counter()
    press_terms = Counter()
    for event in events:
        room_counter.update(row["room"] for row in event["rows"])
        for row in event["rows"]:
            if row["room"] == "Panorama Bar":
                pbar_label_counter.update(split_tokens(row["label"]))
                pbar_label_counter.update(split_tokens(row["keywords"]))
        words = re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'-]+", event["press_text"].lower())
        for word in words:
            if word in PANORAMA_TERMS or word in PUSH_TERMS or word in COMMUNITY_TERMS:
                press_terms[word] += 1
    return pbar_label_counter, room_counter, press_terms


def write_observations(events: list[dict]) -> None:
    pbar_label_counter, room_counter, _ = build_signal_counters(events)
    years = sorted({event["year"] for event in events})
    lines = [
        "# Berghain 2024-2026 Observations",
        "",
        "## Status",
        "- Project: Orbit II (DJ research archive)",
        "- Phase: Sammlung",
        "- Focus: Panorama Bar, warm-up/deep grooves, minimal house, groove, closing sets",
        "- No judgments, no top lists, no final DNA yet",
        "",
        "## What we have",
        "- Berghain 2010 archive completed (events, artists, press texts, labels, communities, aesthetics)",
        f"- Parsed {len(events)} Berghain event blocks from `berghain/klubnacht_2024_2026.md`: "
        + ", ".join(f"{year}={sum(1 for event in events if event['year'] == year)}" for year in years)
        + ".",
        f"- Current 2024-2026 archive contains {sum(len(event['rows']) for event in events)} artist slots across rooms: "
        + "; ".join(f"{room}={count}" for room, count in room_counter.most_common())
        + ".",
        "- Folder-based output (flow, push, moment variation) maps directly to Rekordbox workflow.",
        "",
        "## Immediate note",
        "- Keep human-in-the-loop decisions (e.g., keep/delete tracks) but automate tagging, folder suggestions, and Rekordbox exports based on Panorama Bar DNA.",
        "",
        "## Archive observations generated from current data",
    ]
    for event in events:
        pbar = [row for row in event["rows"] if row["room"] == "Panorama Bar"]
        if pbar:
            pbar_display = "; ".join(row["artist"] for row in pbar[:5])
            if len(pbar) > 5:
                pbar_display += f"; +{len(pbar) - 5} more"
        else:
            pbar_display = "Panorama Bar not listed"
        top_event_labels = [label for label, _ in event["labels"].most_common(4)]
        label_note = "; ".join(top_event_labels) if top_event_labels else "unknown labels/keywords"
        lines.append(
            f"- {event['date']} {event['event_title']} ({event['source_url']}): {pbar_display}. "
            f"Markers: {', '.join(event_tags(event))}; source labels/keywords: {label_note}."
        )
    lines.extend(
        [
            "",
            "## Trend Agent notes",
            "- Flow signal is strongest when Panorama Bar lineups carry recurring house/disco/minimal anchors and press language around deep, groove, funk, soul, or closing-set continuity.",
            "- Push signal appears where Panorama Bar artists are booked beside techno, electro, acid, tribal, or breakbeat cues; keep these as energy nudges rather than final DNA claims.",
            "- Repeated labels/keywords worth watching for folder routing: "
            + "; ".join(label for label, _ in pbar_label_counter.most_common(12))
            + ".",
            "- Comparable public tools remain event listings, RA/TrackID-style identifiers, and store catalogs; Orbit II adds value by preserving source URLs, room context, and Rekordbox folder intent in one dataset.",
            "- Passive-income hypotheses should stay downstream of verified data: curated research notes, playlist exports, and store-to-Rekordbox routing only after track-level validation.",
            "",
            "## Contrarian notes",
            "- Contrarian note: Several press texts and labels skew techno even when Panorama Bar is present; mark performance_type = unknown until track-level evidence proves a warm groove role.",
            "- Contrarian note: The raw source currently captures Berghain, Panorama Bar, Garten, Säule, XXX-Floor, and Elektroakustischer Salon in one flow; future Archive runs should keep room-specific context so Berghain cues do not overwrite Panorama Bar conclusions.",
            "- Contrarian note: `Label` and `Keywords` fields contain both labels and descriptors; use them as discovery signals, not as normalized label metadata.",
            "",
            "## Next moves",
            "- Continue updating 2026 as new Berghain event pages become available.",
            "- Add track-level sources only when real TrackID/store/artist data is cited.",
            "- Keep appending recommendation lines from Trend and Contrarian agents after each Archive refresh.",
        ]
    )
    (ROOT / "berghain_2024_2026_observations.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_label_notes(events: list[dict]) -> None:
    pbar_label_counter, _, press_terms = build_signal_counters(events)
    lines = ["# Labels, Communities, Aesthetics (Berghain 2024-2026)", "", "## Labels & Stores to Watch"]
    for label, count in pbar_label_counter.most_common(25):
        lines.append(f"- {label} ({count} Panorama Bar slot signals)")
    lines.extend(
        [
            "",
            "## Communities & Collectives",
            "- Panorama Bar community (warm-up, closing, groove-focused) remains the primary filter for folder decisions.",
            "- Berghain Klubnacht context is useful, but Berghain-room techno cues must stay separate from Panorama Bar DNA claims.",
            "- Source community/store names should be copied only from verified event, label, TrackID, store, or press data.",
            "",
            "## Aesthetic Signals",
            "- Flow = warm, groovy house for entrancing transitions.",
            "- Push = percussive, driving elements that nudge the dancefloor forward.",
            "- Moment (deep/driving/vocal) = micro-energies for set sections.",
            "- Current repeated press/source terms: "
            + "; ".join(f"{term} ({count})" for term, count in press_terms.most_common(20))
            + ".",
            "",
            "## How to use",
            "- Agent templates should flag these labels/communities when parsing tracklists.",
            "- Observations feed into Rekordbox folder suggestions and the future Vision Agent for passive-income models.",
            "- Treat all entries as Sammlung-phase signals: no top lists, no final DNA, no invented genre proof.",
        ]
    )
    (ROOT / "berghain_2024_2026_labels_communities_aesthetics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    events = parse_events()
    write_events_csv(events)
    write_press_csv(events)
    write_artist_csvs(events)
    write_observations(events)
    write_label_notes(events)
    artist_count = len(build_artist_indexes(events)[0])
    print(f"Generated {len(events)} events and {artist_count} artists from {SOURCE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
