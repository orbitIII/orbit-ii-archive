# Remmex Releases 2026-06-25 — ORBIT Scan

Source: `https://srv.remmex.com/#/media/releases?date=2026-06-25`

## Corpus

- **595 releases**, **1246 tracks** on this date
- Sorted by popularity (default)
- Genre filters available (HOUSE, TECH HOUSE, MINIMAL / DEEP TECH, …)

## Remmex fields (list view)

| Field | Available | Example |
|-------|-----------|---------|
| Release ID | yes | `#7967355` |
| Download ID | yes (in ZIP URL) | `7724969` |
| Release title | yes | Timbalero |
| Label | yes | Stereo Productions |
| Artist — Track | yes | Vidaloca, JB Martinz - Timbalero (Original Mix) |
| Genre tag | yes | house, tech house, afro house |
| BPM | **no** (list view) | — |
| Key | **no** (list view) | — |
| ZIP download | yes | `https://srv.remmex.com/dwnld/release/{id}.zip?mp3` |
| MP3 download | yes | per-track link on detail |

## ORBIT scoring (without BPM/Key)

Scored against `orbit_core_profile_rules.json` with BPM rule disabled (Remmex list has no BPM).

| Threshold | CORE matches | FLOW matches |
|-----------|-------------:|-------------:|
| ≥ 70% | 0 | 0 |
| ≥ 55% | 4 | 0 |

**Top CORE candidates (57%):** Ferrari — Crazy Love / Heavy Duty / Treno Diurno / Worksense (House, artist in CORE corpus)

> Full scoring needs BPM/Key from ZIP import or Rekordbox analysis after download.

## Files

- `releases-2026-06-25.json` — raw export (595 releases)
- `releases-2026-06-25_scored_orbit_core.csv` — all tracks scored
- `releases-2026-06-25_scored_orbit_flow.csv` — all tracks scored

## Next step for pipeline

1. Filter Remmex by genre tags matching ORBIT profiles (HOUSE, TECH HOUSE, DEEP HOUSE, MINIMAL / DEEP TECH)
2. Download ZIP for candidates ≥ 55% pre-score
3. Import to Rekordbox → analyze BPM/Key → final score
4. Add to target playlist (CORE / FLOW / AUSGEsortiert)
