# WARM HYPNOTIC (SYSTEM) Analysis Report

Source: `rekordbox/exports/warm_hypnotic_snapshot.csv`
Playlist analyzed: **WARM HYPNOTIC (SYSTEM)**

> Live Rekordbox DB (56 tracks).

## Corpus

- Tracks in playlist: 56
- Unique artists: 51
- Unique labels: 40
- Unique genres (Rekordbox tags): 10
- Unique keys: 17

## BPM (measurable)

- Range: 120.0 – 133.31
- Mean / median: 126.01 / 125.99
- p10 – p90: 123.0 – 129.0
- Stdev: 2.46

## Top genres (Rekordbox field, no reinterpretation)

- Minimal: 23 (41.1%)
- Deep House: 10 (17.9%)
- Tech House: 8 (14.3%)
- Techno (Raw / Deep / Hypnotic): 3 (5.4%)
- Minimal / Deep Tech: 3 (5.4%)
- Minimal  Deep Tech: 3 (5.4%)
- House: 2 (3.6%)
- unknown: 2 (3.6%)
- Techno: 1 (1.8%)
- Electronica: 1 (1.8%)

## Top keys

- Ebm: 7
- Fm: 6
- Gm: 5
- Bbm: 5
- Dm: 4
- Am: 4
- Em: 4
- Abm: 4
- Cm: 3
- Bm: 2

## Top labels

- Afterhours: 7
- In Dust We Trust: 3
- unknown: 3
- Certain Circles: 3
- Freeborn Records: 2
- Eclipser Chaser: 2
- Berg Audio: 2
- Dreams On Wax: 2
- SECRET SOCIETY CHILE: 1
- Blind Box Series: 1
- Assemble Music: 1
- SCKT: 1
- Morris Audio: 1
- Sushitech: 1
- PURISM Wave: 1

## Top artists

- Silat Beksi: 3
- RQZ: 2
- Nick Beringer & Philipp Boston: 2
- Karcelen: 2
- Rh.cher: 1
- Jon Sable, Kenny Sterling: 1
- A1 Blind Box: 1
- Altitude: 1
- Markus Suckut: 1
- Camiel Daamen: 1
- Youandewan: 1
- IZA: 1
- Mr. Lady: 1
- Tikiman, Rhauder, Paul St. Hilaire: 1
- Daniel Law: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 123.0 and 129.0 (WARM HYPNOTIC (SYSTEM) p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent WARM HYPNOTIC (SYSTEM) genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent WARM HYPNOTIC (SYSTEM) keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent WARM HYPNOTIC (SYSTEM) labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 WARM HYPNOTIC (SYSTEM) artists or exact match in corpus

## Outliers in current WARM HYPNOTIC (SYSTEM) folder

- Count: 10 / 56

- 30.0% | fleet.dreams — Semioptila | BPM 133.0 | Electronica | low_confidence; bpm_outside_p10_p90; singleton_genre_in_flow
- 40.0% | Aleqs Notal — Hands On (Original Mix) | BPM 122.0 | House | low_confidence; bpm_outside_p10_p90
- 40.0% | Levi Verspeek — A2 Octo VINYL ONLY  | BPM 122.0 | Minimal | low_confidence; bpm_outside_p10_p90
- 55.0% | Nesta — Light Tower | BPM 122.0 |  | bpm_outside_p10_p90
- 55.0% | SOST — Hidden Skeleton (Original Mix) | BPM 130.0 | Minimal  Deep Tech | bpm_outside_p10_p90
- 55.0% | Minimal Man — B1 Stay On (A.M. Edit) VINYL ONLY  | BPM 133.31 | Minimal | bpm_outside_p10_p90
- 55.0% | Ortella — Let's Go To The Bitch Vinyl Only | BPM 122.99 | Minimal | bpm_outside_p10_p90
- 60.0% | Audio Werner — High | BPM 125.0 | Techno | singleton_genre_in_flow
- 70.0% | Mr. Lady — The Game (Originalmix) | BPM 121.99 | Minimal / Deep Tech | bpm_outside_p10_p90
- 70.0% | Daniel Law — Futile Needs  | BPM 120.0 | Minimal | bpm_outside_p10_p90

## Usage

Use `system_warm_hypnotic_profile_rules.json` + `system_warm_hypnotic_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
