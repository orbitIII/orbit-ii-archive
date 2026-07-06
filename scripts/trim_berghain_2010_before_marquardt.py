#!/usr/bin/env python3
"""Remove Berghain 2010 archive entries from first Sven Marquardt appearance onward."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BERGHAIN_2010 = ROOT / "berghain" / "2010"
CUTOFF = datetime(2010, 4, 1)
DATE_RE = re.compile(r"(\d{2})\.(\d{2})\.(\d{4})")


def parse_date(text: str) -> datetime | None:
    m = DATE_RE.search(text)
    if not m:
        return None
    day, month, year = map(int, m.groups())
    return datetime(year, month, day)


def on_or_after_cutoff(text: str) -> bool:
    d = parse_date(text)
    return d is not None and d >= CUTOFF


def trim_events_merged() -> tuple[int, int]:
    path = BERGHAIN_2010 / "events_merged.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    removed = 0
    kept = 0
    for section, events in data.items():
        if not isinstance(events, dict):
            continue
        to_delete = []
        for eid, ev in events.items():
            if on_or_after_cutoff(ev.get("date", "")) or "Marquardt" in json.dumps(ev, ensure_ascii=False):
                to_delete.append(eid)
        for eid in to_delete:
            del events[eid]
            removed += 1
        kept += len(events)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return kept, removed


def trim_sammelphase_md(filename: str) -> None:
    path = BERGHAIN_2010 / filename
    text = path.read_text(encoding="utf-8")
    marker = "### April 2010"
    if marker in text:
        text = text[: text.index(marker)].rstrip() + "\n"
    else:
        blocks = re.split(r"\n(?=### )", text)
        kept_blocks = []
        for block in blocks:
            if "Marquardt" in block:
                break
            if on_or_after_cutoff(block):
                break
            kept_blocks.append(block)
        text = "\n".join(kept_blocks).rstrip() + "\n"
    path.write_text(text, encoding="utf-8")


def trim_sammelphase_full() -> None:
    path = BERGHAIN_2010 / "sammelphase_2010_full.md"
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=### )", text)
    kept = []
    for block in blocks:
        if "Marquardt" in block:
            continue
        if on_or_after_cutoff(block):
            continue
        kept.append(block)
    path.write_text("\n".join(kept).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    kept, removed = trim_events_merged()
    trim_sammelphase_md("sammelphase_2010.md")
    trim_sammelphase_full()
    print(f"events_merged.json: kept {kept}, removed {removed}")
    print(f"Cutoff: first Sven Marquardt event (>= {CUTOFF.date()})")


if __name__ == "__main__":
    main()
