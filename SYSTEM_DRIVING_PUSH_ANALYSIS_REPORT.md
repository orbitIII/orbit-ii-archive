# DRIVING PUSH (SYSTEM) Analysis Report

Source: `/Users/alanwillson/orbit-ii-archive/rekordbox/exports/driving_push_snapshot.csv`
Playlist analyzed: **DRIVING PUSH (SYSTEM)**

> Live Rekordbox DB playlist `DRIVING PUSH` (50 tracks).

## Corpus

- Tracks in playlist: 50
- Unique artists: 43
- Unique labels: 37
- Unique genres (Rekordbox tags): 11
- Unique keys: 18

## BPM (measurable)

- Range: 124.88 – 137.0
- Mean / median: 130.15 / 130.0
- p10 – p90: 126.0 – 135.0
- Stdev: 3.2

## Top genres (Rekordbox field, no reinterpretation)

- House: 18 (36.0%)
- Tech House: 11 (22.0%)
- Deep House: 5 (10.0%)
- Minimal / Deep Tech: 5 (10.0%)
- Techno (Raw / Deep / Hypnotic): 4 (8.0%)
- Techno (Peak Time / Driving): 2 (4.0%)
- Deep Tech: 1 (2.0%)
- Techno (Peak Time  Driving): 1 (2.0%)
- Techno: 1 (2.0%)
- Minimal: 1 (2.0%)
- Techno (Peak Time / Driving / Hard): 1 (2.0%)

## Top keys

- Abm: 9
- Am: 5
- Bbm: 5
- Dm: 4
- Gm: 3
- F#m: 3
- Eb: 3
- Fm: 3
- Ebm: 2
- Ab: 2

## Top labels

- SEVEN: 6
- R.A.N.D. Muzik Recordings: 3
- Phoenix G: 2
- Serial Records: 2
- R&S Records: 2
- Happiness Therapy: 2
- Certain Circles: 2
- ...is serving: 2
- Running Back: 1
- BienAimer Music: 1
- Adesso Music: 1
- Dance Trax: 1
- Sous Music: 1
- fabric Records: 1
- UNCAGE: 1

## Top artists

- CRYME: 3
- Subb-an: 3
- Ben Reymann, CRYME: 2
- Mr. G: 2
- Dino Lenny: 2
- Ketiov: 1
- Maco: 1
- Deep Colors: 1
- DJ Haus, Confidential Recipe: 1
- Anja Schneider: 1
- Didier Sinclair, DJ Chris Pi: 1
- Andre Zimmer: 1
- Reformed Society: 1
- Munir Nadir: 1
- SW37: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 126.0 and 135.0 (DRIVING PUSH (SYSTEM) p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent DRIVING PUSH (SYSTEM) genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent DRIVING PUSH (SYSTEM) keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent DRIVING PUSH (SYSTEM) labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 DRIVING PUSH (SYSTEM) artists or exact match in corpus

## Outliers in current DRIVING PUSH (SYSTEM) folder

- Count: 10 / 50

- 45.0% | Lo:za — B1 Mystic Dream (Nu Zau Remix) VINYL ONLY  | BPM 127.0 | Minimal | low_confidence; singleton_genre_in_flow
- 55.0% | Mr. G — I'm Dirty (Original Mix) | BPM 124.99 | Tech House | bpm_outside_p10_p90
- 55.0% | Omni A.M. — Keep Doing That (Mark Ambrose Remix V.1.1) | BPM 124.88 | Deep House | bpm_outside_p10_p90
- 60.0% | Silverlining — A1 Groundhog Rave VINYL ONLY  | BPM 128.0 | Techno | singleton_genre_in_flow
- 60.0% | GusGus — Your Moves Are Mine (Sanasol Remix) | BPM 127.0 | Techno (Peak Time / Driving / Hard) | singleton_genre_in_flow
- 70.0% | Ketiov — JE 125BPM (Original Mix) | BPM 125.01 | Tech House | bpm_outside_p10_p90
- 70.0% | DJ Haus, Confidential Recipe — Chain Reaction  (Original Mix) | BPM 136.0 | House | bpm_outside_p10_p90
- 70.0% | Posture (BER) — 4 Ur Luv (Original Mix) | BPM 137.0 | House | bpm_outside_p10_p90
- 100.0% | Maco — Kissin (Terry Francis Remix) | BPM 130.0 | Deep Tech | singleton_genre_in_flow
- 100.0% | Ben Reymann, CRYME — WTTD (Original Mix) | BPM 135.0 | Techno (Peak Time  Driving) | singleton_genre_in_flow

## Usage

Use `system_driving_push_profile_rules.json` + `system_driving_push_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
