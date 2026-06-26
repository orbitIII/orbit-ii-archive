# WARM (SYSTEM) Analysis Report

Source: `rekordbox/exports/warm_snapshot.csv`
Playlist analyzed: **WARM (SYSTEM)**

> Live Rekordbox DB (22 tracks).

## Corpus

- Tracks in playlist: 22
- Unique artists: 21
- Unique labels: 19
- Unique genres (Rekordbox tags): 7
- Unique keys: 14

## BPM (measurable)

- Range: 119.99 – 128.82
- Mean / median: 124.22 / 124.49
- p10 – p90: 121.1 – 126.0
- Stdev: 2.11

## Top genres (Rekordbox field, no reinterpretation)

- Minimal: 7 (31.8%)
- Deep House: 6 (27.3%)
- Tech House: 4 (18.2%)
- Techno (Raw / Deep / Hypnotic): 2 (9.1%)
- unknown: 1 (4.5%)
- House: 1 (4.5%)
- Techno: 1 (4.5%)

## Top keys

- Gm: 4
- Cm: 3
- Eb: 2
- Fm: 2
- Bm: 2
- Dm: 1
- Am: 1
- F#m: 1
- Bbm: 1
- Ebm: 1

## Top labels

- Berg Audio: 3
- unknown: 2
- PURISM Wave: 1
- Gettraum: 1
- BERG AUDIO: 1
- Rutilance Recordings: 1
- Mojuba: 1
- Rawax: 1
- SATYA: 1
- Amam: 1
- Odd Even: 1
- Trelik Records: 1
- Malin Genie: 1
- Van Bonn Records: 1
- Beste Modus: 1

## Top artists

- Ortella: 2
- Daniel Law: 1
- DJ Deep: 1
- Havantepe: 1
- F2 Janeret: 1
- Sven Weisemann: 1
- Janeret: 1
- Powel: 1
- Mr. Statik, Lee Burton, Steampunkd: 1
- A1 Traumer: 1
- Andre Kronert: 1
- Ion Ludwig: 1
- Yaleesa Hall & Malin Genie: 1
- Van Bonn & Luis Baltes: 1
-  Jonathan Ritzmann & Marius Krickow: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 121.1 and 126.0 (WARM (SYSTEM) p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent WARM (SYSTEM) genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent WARM (SYSTEM) keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent WARM (SYSTEM) labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 WARM (SYSTEM) artists or exact match in corpus

## Outliers in current WARM (SYSTEM) folder

- Count: 7 / 22

- 55.0% | Powel — Lullaby For Eyebrights (Original Mix) | BPM 121.0 | Deep House | bpm_outside_p10_p90
- 55.0% | Mr. Statik, Lee Burton, Steampunkd — Peanuts In Love (Ion Ludwig Remix) | BPM 119.99 | Deep House | bpm_outside_p10_p90
- 55.0% | Ortella — B2 Work I VINYL ONLY  | BPM 120.96 | Tech House | bpm_outside_p10_p90
- 70.0% | Yaleesa Hall & Malin Genie — B2 Coronal Loop VINYL ONLY  | BPM 127.01 | Minimal | bpm_outside_p10_p90
- 70.0% |  — Makam - Glacial Valley | BPM 128.82 |  | bpm_outside_p10_p90
- 85.0% | A Psychic Yes — Maze Dream (Sapphire Slows Remix) | BPM 123.0 | House | singleton_genre_in_flow
- 85.0% | Grad_u — B1 Decay VINYL ONLY  | BPM 123.14 | Techno | singleton_genre_in_flow

## Usage

Use `system_warm_profile_rules.json` + `system_warm_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
