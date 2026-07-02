# ORBIT Digging — Test App

Browser-UI zum Testen der Digging-Plattform: Playlists, Outlier, Vergleiche, Berghain, Remmex.

## Start

```bash
python3 scripts/serve_orbit_digging.py
```

**http://127.0.0.1:8766/app/orbit-digging/**

> Nicht per `file://` öffnen — fetch braucht den lokalen Server.

## Tabs

| Tab | Zweck |
|-----|--------|
| Überblick | Stats, Kuratierungs-Queue, fehlende Analysen |
| Playlists | Karten → Detail mit Profil, Regeln, Tracks |
| Kuratieren | Outlier-Ranking nach Anteil |
| Vergleiche | FLOW vs DRIVING FLOW, CORE vs ARCHIV |
| Berghain | Artist-Frequenz, Events |
| Remmex | Pre-Score gegen ORBIT-Profile |
| Scripts | Befehle (klick = kopieren) |

## Datenquellen

Alles aus Repo-Root: `orbit_playlists.json`, `*_profile_rules.json`, `*_track_scores.csv`, Berghain-CSV, Remmex-Scores.

Nach neuer Analyse: **↻** in der App oder Seite neu laden.
