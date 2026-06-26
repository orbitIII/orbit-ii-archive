# MOMENT Driving (SYSTEM) Analysis Report

Source: `/Users/alanwillson/orbit-ii-archive/rekordbox/exports/moment_driving_snapshot.csv`
Playlist analyzed: **MOMENT Driving (SYSTEM)**

> Live Rekordbox DB playlist `MOMENT Driving ` (37 tracks).

## Corpus

- Tracks in playlist: 37
- Unique artists: 34
- Unique labels: 33
- Unique genres (Rekordbox tags): 5
- Unique keys: 15

## BPM (measurable)

- Range: 127.0 – 133.0
- Mean / median: 130.09 / 130.0
- p10 – p90: 127.84 – 133.0
- Stdev: 1.88

## Top genres (Rekordbox field, no reinterpretation)

- House: 21 (56.8%)
- Tech House: 5 (13.5%)
- Minimal / Deep Tech: 5 (13.5%)
- Minimal: 4 (10.8%)
- Deep House: 2 (5.4%)

## Top keys

- Am: 6
- Ebm: 6
- Gm: 4
- Abm: 4
- Bbm: 3
- Fm: 3
- Dbm: 2
- Cm: 2
- Dm: 1
- Em: 1

## Top labels

- Happiness Therapy: 2
- Creatures Of The Night: 2
- Koltrax: 2
- Limousine Dream: 2
- Dekmantel: 1
- One Trip To Avyon: 1
- Cecille: 1
- Evasive Records: 1
- neXup recz: 1
- BienAimer Music: 1
- Signatune Records: 1
- Dennis Quin: 1
- Duality Trax: 1
- Seduction Records: 1
- We Are Pyramid: 1

## Top artists

- Munir Nadir: 2
- Kolter: 2
- CRYME: 2
- Steffi, Virginia: 1
- Big Miz: 1
- Zombies in Miami: 1
- Giammarco Orsini, Pancratio: 1
- Easttown: 1
- Rob Pearson & Robin Ball: 1
- Ozzie Guven: 1
- Guest (UK): 1
- Big Miz, Bessa (Sco): 1
- Dennis Quin: 1
- Voodoos & Taboos: 1
- Dafs: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 127.84 and 133.0 (MOMENT Driving (SYSTEM) p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent MOMENT Driving (SYSTEM) genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent MOMENT Driving (SYSTEM) keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent MOMENT Driving (SYSTEM) labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 MOMENT Driving (SYSTEM) artists or exact match in corpus

## Outliers in current MOMENT Driving (SYSTEM) folder

- Count: 4 / 37

- 40.0% | Philip Chernikov — I Don't Like Bugs (Original Mix) | BPM 127.0 | House | low_confidence; bpm_outside_p10_p90
- 55.0% | Paul Cut, Aline Umber — Memorize Your Face (Aline Umber Rework) | BPM 127.0 | House | bpm_outside_p10_p90
- 70.0% | Rob Pearson & Robin Ball — B1 The Right Vibes VINYL ONLY  | BPM 127.6 | Tech House | bpm_outside_p10_p90
- 70.0% | Dafs — Don't Stop (Extended)  | BPM 127.0 | House | bpm_outside_p10_p90

## Usage

Use `system_moment_driving_profile_rules.json` + `system_moment_driving_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
