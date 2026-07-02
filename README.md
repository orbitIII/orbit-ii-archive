# orbit-ii-archive

**ORBIT Digging Platform** — Rekordbox-Integration, Playlist-Analyse, Kuratierung und Berghain-Sammlung.

Identität, Film, Marquardt und Künstler-Mood liegen **pausiert** unter [`archiv/identitaet_layer/`](archiv/identitaet_layer/) — damit sich Errungenschaften nicht mit Ästhetik-Schichten vermischen.

## Steuerung

| Was | Datei |
|-----|-------|
| Plattform-Überblick | [`docs/digging_platform.md`](docs/digging_platform.md) |
| Rekordbox ↔ ORBIT | [`docs/rekordbox_orbit.md`](docs/rekordbox_orbit.md) |
| Playlist-Konfig | [`orbit_playlists.json`](orbit_playlists.json) |
| Schicht-Index | [`orbit_index.json`](orbit_index.json) |
| Berghain-Automatisierung | [`docs/automation_plan.md`](docs/automation_plan.md) |

## Schnellstart

```bash
# Browser-UI (Playlists, Scores, Berghain)
python3 scripts/serve_orbit_digging.py
# → http://127.0.0.1:8766/app/orbit-digging/

# ORBIT CORE analysieren (live Rekordbox-DB)
python3 scripts/analyze_orbit_playlists.py --slug orbit_core

# Alle konfigurierten Playlists
python3 scripts/analyze_orbit_playlists.py --all

# Outlier aus ORBIT FLOW → AUSGEsortiert (Rekordbox vorher schließen)
python3 scripts/curate_orbit_flow.py
```

## Repo-Schichten

```
orbit-ii-archive/
├── orbit_playlists.json          # Digging-Kern
├── orbit_index.json              # Was aktiv vs. archiviert
├── app/orbit-digging/            # Browser-UI
├── scripts/                      # Analyse & Kuratierung
├── rekordbox/                    # Snapshots & Backups
├── berghain/ + berghain_*.csv    # Event-Sammlung
├── remmex/                       # Release-Scoring
├── *_profile_rules.json          # Pro-Playlist-Regeln
├── *_track_scores.csv            # Track-Scores
└── archiv/identitaet_layer/      # Pausiert: Film, Identität, Referenzen
```
