# ORBIT Digging Platform

## Was ORBIT hier ist

ORBIT ist ein **Digging- und Kuratierungssystem** für deine Rekordbox-Bibliothek:

1. **Sammeln** — Berghain-Events, Tracklists, Remmex-Releases
2. **Messen** — BPM, Genre, Key, Label, Artist gegen Playlist-Profile
3. **Sortieren** — Outlier raus, passende Tracks rein, nie löschen
4. **Dokumentieren** — Reports, Snapshots, reproduzierbare Scripts

Keine subjektive „DNA“ in der Messung — nur Rekordbox-Metadaten und klare Regeln (`docs/rekordbox_orbit.md`).

## Was hier nicht hingehört (pausiert)

Alles zu **Identität, Film, Marquardt, Künstler-Mood, Prinzipien, Bridge-Synthese** liegt in:

`archiv/identitaet_layer/`

Dort bleibt die Arbeit erhalten, mischt sich aber nicht mehr mit der Digging-Schicht.

## Errungenschaften (Digging)

| Bereich | Status | Artefakte |
|---------|--------|-----------|
| Rekordbox-Integration | live | `scripts/rekordbox_orbit.py`, `orbit_playlists.json` |
| ORBIT CORE Profil | analysiert | `ORBIT_CORE_ANALYSIS_REPORT.md`, `orbit_core_*` |
| ORBIT FLOW | analysiert + Kuratierung | `ORBIT_FLOW_ANALYSIS_REPORT.md`, `curate_orbit_flow.py` |
| ORBIT ARCHIV | analysiert | `ORBIT_ARCHIV_ANALYSIS_REPORT.md` |
| ORBIT MOMENT DEEP | analysiert | `ORBIT_MOMENT_DEEP_ANALYSIS_REPORT.md` |
| SYSTEM MOMENT DEEP / Driving | analysiert | `SYSTEM_MOMENT_*`, `SYSTEM_DRIVING_*` |
| DRIVING FLOW / PUSH / WARM | analysiert | `DRIVING_*`, `SYSTEM_WARM_*` |
| AUSGEsortiert-Pipeline | live | `curate_to_ausgesortiert.py`, `sort_ausgesortiert.py` |
| Berghain 2024–2026 | Sammelphase | `berghain_2024_2026_*.csv`, `berghain/` |
| TrackID-Import-Analyse | abgeschlossen | `TRACKID_IMPORT_ANALYSIS_REPORT.md` |
| Remmex Pre-Scoring | Script bereit | `scripts/score_remmex_releases.py`, `remmex/` |

Details und Pfade: `orbit_index.json`.

## Browser-UI

```bash
python3 scripts/serve_orbit_digging.py
```

→ http://127.0.0.1:8766/app/orbit-digging/ — Playlists, Outlier, Berghain, Scripts.

## Nächste sinnvolle Schritte (Digging)

1. Offene Kuratierungs-Pässe abschließen (FLOW, MOMENT, AUSGEsortiert sortieren)
2. Berghain-Frequenzen → Playlist-Hinweise (Artist/Label aus CSV)
3. Remmex-Pipeline: List-Score → Download → Rekordbox → Final-Score
4. Identitäts-Schicht **erst wieder** anfassen, wenn Digging-Fundament stabil steht
