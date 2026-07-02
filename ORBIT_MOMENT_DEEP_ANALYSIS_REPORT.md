# ORBIT MOMENT DEEP Analysis Report

Source: `/Users/alanwillson/orbit-ii-archive/rekordbox/exports/orbit_moment_deep_snapshot.csv`
Playlist analyzed: **ORBIT MOMENT DEEP**

> Live Rekordbox DB playlist `ORBIT MOMENT DEEP` (25 tracks).

## Corpus

- Tracks in playlist: 25
- Unique artists: 22
- Unique labels: 25
- Unique genres (Rekordbox tags): 7
- Unique keys: 15

## BPM (measurable)

- Range: 122.98 – 130.0
- Mean / median: 126.54 / 126.0
- p10 – p90: 124.0 – 130.0
- Stdev: 2.2

## Top genres (Rekordbox field, no reinterpretation)

- House: 7 (28.0%)
- Minimal: 4 (16.0%)
- Tech House: 4 (16.0%)
- Deep House: 4 (16.0%)
- Minimal / Deep Tech: 3 (12.0%)
- Techno: 2 (8.0%)
- Deep Tech: 1 (4.0%)

## Top keys

- Am: 4
- Dbm: 3
- Fm: 3
- Ebm: 2
- Bb: 2
- Gm: 2
- Abm: 1
- Bbm: 1
- A: 1
- E: 1

## Top labels

- BodyParts Vinyl: 1
- Skudge Records: 1
- Constant Sound: 1
- City Boy Music (US): 1
- Phonica Recordings: 1
- All Inn Records: 1
- Freerange Records: 1
- DESSERT: 1
- Rawax: 1
- Afterhours: 1
- Raru Movement: 1
- Bambe: 1
- Opossum Recordings: 1
- Reel People Music: 1
- down2earth: 1

## Top artists

- Silat Beksi: 4
- Oshana: 1
- Skudge: 1
- Burnski: 1
- Eddie Fowlkes: 1
- Mattias El Mansouri: 1
- Halo Varga: 1
- Soul Of Hex: 1
- EyeofPsi: 1
- Bambounou, Priori: 1
- Moritz Piske: 1
- Risk Assessment, KE, Franck Roger: 1
- Philip Chernikov: 1
- Cosmjn: 1
- Stephen Brown: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 124.0 and 130.0 (ORBIT MOMENT DEEP p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent ORBIT MOMENT DEEP genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent ORBIT MOMENT DEEP keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent ORBIT MOMENT DEEP labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 ORBIT MOMENT DEEP artists or exact match in corpus

## Outliers in current ORBIT MOMENT DEEP folder

- Count: 3 / 25

- 55.0% | grad u — Geomagnetic Storm | BPM 123.99 | House | bpm_outside_p10_p90
- 55.0% | Nudge — Howl012.2 VINYL ONLY | BPM 122.98 | Deep House | bpm_outside_p10_p90
- 85.0% | Silat Beksi — Do Or Donut (Original Mix) | BPM 126.0 | Deep Tech | singleton_genre_in_flow

## Usage

Use `orbit_moment_deep_profile_rules.json` + `orbit_moment_deep_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
