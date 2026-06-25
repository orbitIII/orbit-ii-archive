# Top 50 Panorama Bar Artist Set Archive Report

## Zweck

Dieses Archiv definiert die 50 meist gebuchten Panorama-Bar-Artists aus `berghain_2024_2026_top50_panorama_bar_artists.csv` und legt öffentlich auffindbare Set-Quellen für diese Artists ab, damit spätere Track-ID- und Overlap-Analysen reproduzierbar auf dieselben Quellen zugreifen können.

## Top-50-Definition

Die Top 50 werden weiterhin über Panorama-Bar-Auftritte im Archiv `berghain/klubnacht_2024_2026.md` definiert:

- gezählt werden nur Zeilen mit `Raum = Panorama Bar`
- explizite B2B-/Back-to-back-Sets werden pro beteiligtem Artist gezählt
- sortiert wird nach Anzahl der Panorama-Bar-Auftritte, danach alphabetisch

Der aktuelle Top-50-Input liegt in:

- `berghain_2024_2026_top50_panorama_bar_artists.csv`
- `berghain_2024_2026_artist_frequency.csv`
- `berghain_2024_2026_artists_raw.csv`

## Neue Archivdateien

### TrackID.net Set-Archiv

- `berghain_2024_2026_top50_artist_sets_trackid.csv`
- Segmentdateien:
  - `berghain_2024_2026_top50_artist_sets_trackid_part01.csv`
  - `berghain_2024_2026_top50_artist_sets_trackid_part02.csv`
  - `berghain_2024_2026_top50_artist_sets_trackid_part03.csv`
  - `berghain_2024_2026_top50_artist_sets_trackid_part04.csv`
  - `berghain_2024_2026_top50_artist_sets_trackid_part05.csv`

Schema:

- `artist_rank`
- `artist`
- `source_platform`
- `source_url`
- `result_count`
- `set_title`
- `channel`
- `duration`
- `created_on`
- `requested_on`
- `requested_by`
- `status`
- `archive_scope`
- `notes`

### Provider Source Index

- `berghain_2024_2026_top50_artist_set_source_index.csv`

Dieser Index enthält pro Top-50-Artist reproduzierbare Einstiegspunkte für:

- TrackID.net
- MixesDB
- SoundCloud
- YouTube
- Resident Advisor
- HÖR Berlin / YouTube

## Coverage

- Top-50-Artists abgedeckt: 50
- TrackID.net sichtbare Archivzeilen: 838
- TrackID.net sichtbare Set-Zeilen: 836
- TrackID.net No-result-Zeilen: 2
- Artists mit sichtbaren TrackID-Set-Zeilen: 48
- TrackID.net gemeldete Treffer über alle Top-50-Suchen: 2.978
- Provider-Index-Zeilen: 300

Die beiden Artists ohne sichtbare TrackID-Set-Zeilen in dieser Erfassung:

- Zombies In Miami
- DJ Holographic

## Wichtige Einschränkungen

TrackID.net liefert öffentlich zwar Trefferzahlen, die Textansicht zeigt aber meist nur die erste sichtbare Ergebnisseite. Deshalb ist das aktuelle CSV ein reproduzierbarer **sichtbarer TrackID-Index**, nicht zwingend ein kompletter Dump aller paginierten TrackID-Treffer.

Einige Namen erzeugen breite oder verrauschte Suchergebnisse:

- `Victor`
- `Âme`
- `Naomi`
- `Chloé`
- `Loren`

Diese Zeilen bleiben im Archiv, sind aber in `notes` als alias-/filterbedürftig markiert, wenn sie nicht eindeutig zum Top-50-Artist passen.

## Empfehlungen für die nächste Iteration

1. TrackID.net-Pagination oder Export-Funktion nutzen, um alle gemeldeten 2.978 Treffer vollständig abzulegen.
2. Alias-/Disambiguation-Tabelle für kurze oder mehrdeutige Artist-Namen erstellen.
3. Pro Set eine stabile Detail-URL ergänzen, sobald diese per TrackID-Export oder Browser-Scrape reproduzierbar verfügbar ist.
4. Aus `berghain_2024_2026_top50_artist_sets_trackid.csv` anschließend Tracklisten extrahieren und in eine separate `artist_set_tracks`-Tabelle normalisieren.
5. Track-Overlap-Matrix danach aus den normalisierten Tracklisten neu berechnen, getrennt nach:
   - unabhängigen Set-Overlaps
   - B2B-/Joint-set-Evidence
   - source-only oder low-confidence Evidence
