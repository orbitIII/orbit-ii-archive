# ORBIT ↔ Rekordbox Integration

ORBIT reads and writes Pioneer Rekordbox playlists directly on this machine.
This is a core capability: analyze folders, score tracks, move outliers, and (later)
insert purchases from Remmex.

## Library location

| Path | Purpose |
|------|---------|
| `~/Library/Pioneer/rekordbox/master.db` | Encrypted SQLite library (via pyrekordbox) |
| `~/Library/Pioneer/rekordbox/masterPlaylists6.xml` | Playlist tree sync for Rekordbox UI |
| `~/Documents/rekordbox/CueConv/RB LIBARY TEXT/` | Manual txt exports (may be stale) |

Rekordbox app: `/Users/Shared/Previously Relocated Items/Security/Applications/rekordbox 6/rekordbox.app`

## ORBIT II playlist tree

```
ORBIT II
├── CORE              ← reference corpus (essential tracks)
├── ARCHIV            ← broader archive pool
├── ORBIT FLOW        ← flow energy profile
├── ORBIT PUSH
├── ORBIT MOMENT DEEP
└── AUSGEsortiert     ← outliers moved out of FLOW
```

SYSTEM tree (separate world — do not merge with ORBIT):

```
SYSTEM
├── MOMENT DEEP
├── MOMENT Driving
├── DRIVING FLOW
├── DRIVING PUSH
├── WARM / WARM HYPNOTIC
└── WIRED
```

Outliers from any ORBIT or SYSTEM playlist go to **ORBIT II → AUSGEsortiert** for later sorting.
Tracks are **never deleted** from the Rekordbox library — only removed from the source playlist
and added to AUSGEsortiert. Use `sort_ausgesortiert.py` when ready to distribute further.

## Config

`orbit_playlists.json` — slug, Rekordbox name, parent folder, source (`db` or `txt`), role.

Prefer **`source: db`** for live analysis. Txt exports drift quickly (e.g. CORE txt had 43 tracks, DB had 64).

## Scripts

```bash
# Analyze ORBIT CORE (live DB)
python3 scripts/analyze_orbit_playlists.py --slug orbit_core

# Analyze all configured playlists + comparison reports
python3 scripts/analyze_orbit_playlists.py --all

# Move ORBIT FLOW outliers → AUSGEsortiert (closes Rekordbox first)
python3 scripts/curate_orbit_flow.py

# Analyze MOMENT DEEP / MOMENT Driving
python3 scripts/analyze_orbit_playlists.py --slug system_moment_deep --slug orbit_moment_deep
python3 scripts/analyze_orbit_playlists.py --slug system_moment_driving

# Analyze DRIVING PUSH
python3 scripts/analyze_orbit_playlists.py --slug system_driving_push

# One-pass DRIVING PUSH curation → WARM / WIRED (do not loop)
python3 scripts/curate_driving_push.py

# Move outliers → AUSGEsortiert (single pass only — do not loop)
python3 scripts/curate_to_ausgesortiert.py --slug system_moment_driving

# Sort AUSGEsortiert → ARCHIV / SYSTEM folders
python3 scripts/sort_ausgesortiert.py
```

### Outputs (repo root)

| File | Content |
|------|---------|
| `{slug}_profile_rules.json` | BPM/genre/key/label/artist rules derived from corpus |
| `{slug}_track_scores.csv` | Per-track confidence + outlier flags |
| `{slug}_ANALYSIS_REPORT.md` | Human-readable summary |
| `rekordbox/exports/*_snapshot.csv` | Point-in-time DB export for git |

## Curation rules (measurable only)

Tracks are scored against Rekordbox metadata fields — no subjective genre DNA:

- BPM within playlist p10–p90 (30%)
- Genre in top 8 (25%)
- Key in top 8 (15%)
- Label in top 15 (15%)
- Artist in top 25 / corpus (15%)

Outlier if: confidence < 55%, BPM outside p10–p90, genre outside top 15, or singleton genre.

## Direct DB access requirements

1. **Close Rekordbox + rekordboxAgent** before writes (`commit()` fails if running)
2. **Backup** before changes → `rekordbox/backups/`
3. Use **playlists, not folders**, for visible track lists (folders need a child playlist)
4. `pyrekordbox` dependency: `pip3 install pyrekordbox`

## Remmex integration

Base URL: `https://srv.remmex.com/#/media/releases?date=YYYY-MM-DD`

### List view fields

| Field | In list | Notes |
|-------|---------|-------|
| Release ID | `#7967355` | Display ID in UI |
| Download ID | ZIP URL | `/dwnld/release/{id}.zip?mp3` |
| Artist, Title, Label, Genre | yes | Genre lowercase (e.g. `house`) |
| BPM, Key | **no** | Only after download / Rekordbox import |

### Scripts

```bash
# 1. Export releases from open Remmex page (browser automation) → remmex/releases-DATE.json
# 2. Score against ORBIT profile (BPM rule disabled for list view)
python3 scripts/score_remmex_releases.py remmex/releases-2026-06-25.json --profile orbit_core
python3 scripts/score_remmex_releases.py remmex/releases-2026-06-25.json --profile orbit_flow
```

Genre tag mapping Remmex → Rekordbox is handled in `score_remmex_releases.py`.

### Pipeline (planned)

```
Remmex date feed → pre-score (genre/artist/label) → ZIP download → Rekordbox import
→ BPM/Key analysis → final score → add to ORBIT playlist
```

## Git

Analysis artifacts and config are versioned in this repo.
DB backups under `rekordbox/backups/` are **not** committed (large, local-only).
