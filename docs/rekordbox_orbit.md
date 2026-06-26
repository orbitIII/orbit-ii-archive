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

SYSTEM tree (separate reference): `DRIVING FLOW`, `DRIVING PUSH`, etc.

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

## Roadmap: Remmex → Rekordbox pipeline

Information still needed before auto-download:

| Field | Source today | Needed for Remmex |
|-------|--------------|-------------------|
| Artist + Title | Rekordbox / scores | Search query |
| Label | Rekordbox | Filter / verify match |
| BPM + Key | Rekordbox | Pre-check against profile rules |
| Confidence score | ORBIT analysis | Accept / reject threshold |
| Playlist target | `orbit_playlists.json` | Which folder to file under |
| File format | TBD | WAV / FLAC / MP3 preference |
| Duplicate detection | Content ID | Avoid double imports |

Planned flow:

1. Candidate track scored against `orbit_core_profile_rules.json` (or FLOW/PUSH profile)
2. If score ≥ threshold → search Remmex
3. Download audio → import to Rekordbox collection
4. Add to target playlist via `pyrekordbox` (`add_to_playlist`)
5. Re-run analysis to refresh outliers

## Git

Analysis artifacts and config are versioned in this repo.
DB backups under `rekordbox/backups/` are **not** committed (large, local-only).
