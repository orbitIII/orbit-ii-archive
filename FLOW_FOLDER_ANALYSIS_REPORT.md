# FLOW Folder Analysis Report

Source: `/Users/alanwillson/Documents/rekordbox/CueConv/Export Log 6.8.1.0042 2026-06-05.xml`
Playlist analyzed: **DRIVING FLOW**

> Note: No Rekordbox playlist named exactly `FLOW` was found in the export.
> Analysis uses the closest match `DRIVING FLOW` (Orbit II `flow` folder equivalent).

## Corpus

- Tracks in playlist: 75
- Unique artists: 64
- Unique labels: 58
- Unique genres (Rekordbox tags): 10
- Unique keys: 20

## BPM (measurable)

- Range: 120.0 – 136.0
- Mean / median: 127.18 / 127.0
- p10 – p90: 124.0 – 130.02
- Stdev: 2.85

## Top genres (Rekordbox field, no reinterpretation)

- Tech House: 14 (18.7%)
- Minimal: 14 (18.7%)
- House: 12 (16.0%)
- Minimal / Deep Tech: 12 (16.0%)
- Deep House: 10 (13.3%)
- Techno (Raw / Deep / Hypnotic): 5 (6.7%)
- Techno (Peak Time / Driving): 4 (5.3%)
- Techno: 2 (2.7%)
- Electronica: 1 (1.3%)
- Minimal  Deep Tech: 1 (1.3%)

## Top keys

- Abm: 11
- Am: 9
- Gm: 6
- Bbm: 6
- Cm: 6
- Dm: 4
- A: 4
- E: 4
- F#m: 3
- Dbm: 3

## Top labels

- Phonogramme: 4
- Sushitech: 3
- Syncrophone: 3
- Repeat: 3
- Certain Circles: 2
- Berg Audio: 2
- SCKT: 2
- Bobby Donny: 2
- unknown: 2
- Bass Culture Records: 2
- De Vloer: 2
- Rawax: 2
- fabric Records (US): 1
- Blind Box Series: 1
- Whiteloops: 1

## Top artists

- Markus Suckut: 3
- Youandewan: 2
- Silverlining: 2
- Wax: 2
- Delano Smith, Brawther, D&B Productions: 2
- Satoshi Tomiie: 2
- Silat Beksi: 2
- D'Julz: 2
- Marco Carola: 2
- Skudge: 2
- Porter: 1
- Black Jazz Consortium: 1
- Kolter: 1
- A1 Blind Box: 1
- Disk: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 124.0 and 130.02 (FLOW p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent FLOW genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent FLOW keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent FLOW labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 FLOW artists or exact match in corpus

## Outliers in current FLOW folder

- Count: 14 / 75

- 30.0% | SOST — Street Walk (Original Mix) | BPM 131.0 | Minimal  Deep Tech | low_confidence; bpm_outside_p10_p90; singleton_genre_in_flow
- 40.0% | Bruno Pronsato, Richard Rozen — You Don't Say (Original Mix) | BPM 120.0 | Minimal / Deep Tech | low_confidence; bpm_outside_p10_p90
- 40.0% | Dan Ghenacia & Chris Carrier — B2 Blue Stick VINYL ONLY  | BPM 123.89 | Tech House | low_confidence; bpm_outside_p10_p90
- 55.0% | Silverlining — Pleasures and Treasures (Original Mix) | BPM 132.03 | Deep House | bpm_outside_p10_p90
- 55.0% | Orlando Voorn — Asylum (G-Man Version 2)  | BPM 134.0 | Minimal | bpm_outside_p10_p90
- 55.0% | Arturo Garces — Just A Little Bit | BPM 121.0 | House | bpm_outside_p10_p90
- 55.0% | Satoshi Tomiie — Hauz Muzik (Original Mix) | BPM 122.0 | House | bpm_outside_p10_p90
- 55.0% | Young Adults — A2 Porcetta (Mf Dub) VINYL ONLY  | BPM 130.04 | Minimal | bpm_outside_p10_p90
- 60.0% | Youandewan — TV Fury (Original Mix) | BPM 129.0 | Electronica | singleton_genre_in_flow
- 70.0% | Black Jazz Consortium — Blacklight (Original Mix) | BPM 123.33 | House | bpm_outside_p10_p90
- 70.0% | Malin Genie, Frits Wentink — Exopaq (Original Mix) | BPM 136.0 | Minimal / Deep Tech | bpm_outside_p10_p90
- 70.0% | Wax — 50005 B | BPM 131.0 | Techno | bpm_outside_p10_p90
- 70.0% | Skudge — Wander  | BPM 134.0 | Techno (Peak Time / Driving) | bpm_outside_p10_p90
- 70.0% | Skudge — Hidden Location  | BPM 134.0 | Techno (Peak Time / Driving) | bpm_outside_p10_p90

## Usage

Use `flow_profile_rules.json` + `flow_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
