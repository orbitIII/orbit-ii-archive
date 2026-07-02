# MOMENT DEEP (SYSTEM) Analysis Report

Source: `/Users/alanwillson/orbit-ii-archive/rekordbox/exports/moment_deep_snapshot.csv`
Playlist analyzed: **MOMENT DEEP (SYSTEM)**

> Live Rekordbox DB playlist `MOMENT DEEP ` (33 tracks).

## Corpus

- Tracks in playlist: 33
- Unique artists: 32
- Unique labels: 32
- Unique genres (Rekordbox tags): 6
- Unique keys: 14

## BPM (measurable)

- Range: 121.0 – 130.0
- Mean / median: 125.95 / 125.01
- p10 – p90: 123.2 – 129.8
- Stdev: 2.48

## Top genres (Rekordbox field, no reinterpretation)

- Deep House: 13 (39.4%)
- House: 10 (30.3%)
- Minimal / Deep Tech: 6 (18.2%)
- Tech House: 2 (6.1%)
- Minimal  Deep Tech: 1 (3.0%)
- House, Deep House/Deep Tech: 1 (3.0%)

## Top keys

- Gm: 7
- Am: 4
- Fm: 4
- Em: 3
- F#m: 3
- Bm: 2
- Bbm: 2
- A: 2
- Ab: 1
- Ebm: 1

## Top labels

- Large Music: 2
- Undergroove: 1
- Nina Kraviz Music: 1
- Biotop: 1
- Silat Beksi Music: 1
- House of Tucci: 1
- Kolour Recordings: 1
- Defected: 1
- Seasons Limited: 1
- Big Love Music: 1
- Syncrophone: 1
- I'm In Love: 1
- Bass Culture Records: 1
- Stoned Pilot: 1
- Robsoul Recordings: 1

## Top artists

- Chris Stussy: 2
- Jake Childs, Paul Dyne: 1
- Nina Kraviz: 1
- Mike Starr: 1
- Silat Beksi: 1
- Tuccillo, Kindbud: 1
- Daniel Solar, Delano Smith: 1
- Jody Watley: 1
- Franck Roger: 1
- Saison: 1
- DJ QU: 1
- DJ Merci: 1
- Oleg Poliakov: 1
- Shonky & Alexander Skancke: 1
- Phil Weeks: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 123.2 and 129.8 (MOMENT DEEP (SYSTEM) p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent MOMENT DEEP (SYSTEM) genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent MOMENT DEEP (SYSTEM) keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent MOMENT DEEP (SYSTEM) labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 MOMENT DEEP (SYSTEM) artists or exact match in corpus

## Outliers in current MOMENT DEEP (SYSTEM) folder

- Count: 10 / 33

- 40.0% | Francesco Forgione — I Feel It (Original Mix) | BPM 130.0 | Minimal / Deep Tech | low_confidence; bpm_outside_p10_p90
- 40.0% | A1 Lazer Man — Que vas tu faire VINYL ONLY  | BPM 130.0 | Deep House | low_confidence; bpm_outside_p10_p90
- 55.0% | Da Rebels — House Nation Under a Groove | BPM 121.66 | House | bpm_outside_p10_p90
- 55.0% | Mike Starr & Mama — Love Away (Douglas Greed Remix) | BPM 123.0 | Tech House | bpm_outside_p10_p90
- 55.0% | Wiremü — The Subtle Hustle | BPM 130.0 | Minimal / Deep Tech | bpm_outside_p10_p90
- 55.0% | Alkalino — Seven Sisters (Original Mix) | BPM 130.0 | Deep House | bpm_outside_p10_p90
- 70.0% | Chris Stussy — Never Tell Me | BPM 121.0 | House | bpm_outside_p10_p90
- 70.0% | Chris Stussy — Soul Patrol | BPM 121.0 | House | bpm_outside_p10_p90
- 85.0% | Traumer, Anton, antraum — Fukai (Original Mix) | BPM 125.0 | Minimal  Deep Tech | singleton_genre_in_flow
- 85.0% | Lump — U Need Me (Original Mix) | BPM 124.0 | House, Deep House/Deep Tech | singleton_genre_in_flow

## Usage

Use `system_moment_deep_profile_rules.json` + `system_moment_deep_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
