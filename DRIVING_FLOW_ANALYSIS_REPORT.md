# DRIVING FLOW (SYSTEM) Analysis Report

Source: `/Users/alanwillson/Documents/rekordbox/CueConv/RB LIBARY TEXT/DRIVING FLOW.txt`
Playlist analyzed: **DRIVING FLOW (SYSTEM)**

## Corpus

- Tracks in playlist: 58
- Unique artists: 52
- Unique labels: 49
- Unique genres (Rekordbox tags): 11
- Unique keys: 18

## BPM (measurable)

- Range: 120.0 – 136.0
- Mean / median: 126.89 / 127.0
- p10 – p90: 124.0 – 130.0
- Stdev: 2.73

## Top genres (Rekordbox field, no reinterpretation)

- Minimal: 13 (22.4%)
- Minimal / Deep Tech: 10 (17.2%)
- House: 9 (15.5%)
- Deep House: 9 (15.5%)
- Tech House: 8 (13.8%)
- Techno (Raw / Deep / Hypnotic): 3 (5.2%)
- Techno: 2 (3.4%)
- Electronica: 1 (1.7%)
- Techno (Peak Time / Driving): 1 (1.7%)
- Tech house: 1 (1.7%)
- Deep Tech: 1 (1.7%)

## Top keys

- Am: 8
- Abm: 7
- Gm: 5
- Cm: 5
- Dm: 4
- F#m: 4
- Bbm: 4
- E: 3
- Em: 2
- Bm: 2

## Top labels

- Sushitech: 3
- Berg Audio: 2
- Bobby Donny: 2
- unknown: 2
- Syncrophone: 2
- Bass Culture Records: 2
- De Vloer: 2
- Repeat: 2
- Certain Circles: 1
- fabric Records (US): 1
- Blind Box Series: 1
- Whiteloops: 1
- Eclipser Chaser: 1
- Biotop: 1
- Plastic City: 1

## Top artists

- Youandewan: 2
- Wax: 2
- Delano Smith, Brawther, D&B Productions: 2
- DJ QU: 2
- D'Julz: 2
- Eddie Richards: 2
- Porter: 1
- Black Jazz Consortium: 1
- Kolter: 1
- A1 Blind Box: 1
- Disk: 1
- Mike Starr: 1
- Terry Lee Brown Junior: 1
- Silverlining: 1
- Malin Genie, Frits Wentink: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 124.0 and 130.0 (DRIVING FLOW (SYSTEM) p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent DRIVING FLOW (SYSTEM) genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent DRIVING FLOW (SYSTEM) keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent DRIVING FLOW (SYSTEM) labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 DRIVING FLOW (SYSTEM) artists or exact match in corpus

## Outliers in current DRIVING FLOW (SYSTEM) folder

- Count: 10 / 58

- 15.0% | Lewis Boardman — Home | BPM 121.0 | Tech house | low_confidence; bpm_outside_p10_p90; singleton_genre_in_flow
- 15.0% | Johnny D — Dream System (Original Mix) | BPM 131.0 | Deep Tech | low_confidence; bpm_outside_p10_p90; singleton_genre_in_flow
- 40.0% | Bruno Pronsato, Richard Rozen — You Don't Say (Original Mix) | BPM 120.0 | Minimal / Deep Tech | low_confidence; bpm_outside_p10_p90
- 55.0% | Silverlining — Pleasures and Treasures (Original Mix) | BPM 132.03 | Deep House | bpm_outside_p10_p90
- 55.0% | Orlando Voorn — Asylum (G-Man Version 2) | BPM 134.0 | Minimal | bpm_outside_p10_p90
- 60.0% | Marco Carola — Pampero (Original Mix) | BPM 124.0 | Techno (Peak Time / Driving) | singleton_genre_in_flow
- 70.0% | Black Jazz Consortium — Blacklight (Original Mix) | BPM 123.33 | House | bpm_outside_p10_p90
- 70.0% | Malin Genie, Frits Wentink — Exopaq (Original Mix) | BPM 136.0 | Minimal / Deep Tech | bpm_outside_p10_p90
- 70.0% | Wax — 50005 B | BPM 131.0 | Techno | bpm_outside_p10_p90
- 85.0% | Youandewan — TV Fury (Original Mix) | BPM 129.0 | Electronica | singleton_genre_in_flow

## Usage

Use `driving_flow_profile_rules.json` + `driving_flow_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
