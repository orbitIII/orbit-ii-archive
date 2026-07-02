# ORBIT FLOW Analysis Report

Source: `/Users/alanwillson/Documents/rekordbox/CueConv/RB LIBARY TEXT/ ORBIT FLOW.txt`
Playlist analyzed: **ORBIT FLOW**

## Corpus

- Tracks in playlist: 36
- Unique artists: 32
- Unique labels: 28
- Unique genres (Rekordbox tags): 12
- Unique keys: 15

## BPM (measurable)

- Range: 121.0 – 131.0
- Mean / median: 126.06 / 126.0
- p10 – p90: 123.0 – 128.5
- Stdev: 2.27

## Top genres (Rekordbox field, no reinterpretation)

- Tech House: 12 (33.3%)
- House: 6 (16.7%)
- Minimal: 6 (16.7%)
- Techno (Peak Time / Driving): 2 (5.6%)
- Minimal / Deep Tech: 2 (5.6%)
- Deep House: 2 (5.6%)
- Minimal  Deep Tech: 1 (2.8%)
- Indie Dance: 1 (2.8%)
- Electronica / Downtempo: 1 (2.8%)
- Classic House: 1 (2.8%)
- Techno: 1 (2.8%)
- Minimal House: 1 (2.8%)

## Top keys

- Bbm: 5
- Abm: 4
- F#m: 3
- Cm: 3
- Fm: 3
- A: 3
- Dm: 2
- Am: 2
- Ebm: 2
- Ab: 2

## Top labels

- Blind Box Series: 4
- Phonogramme: 3
- Repeat: 3
- Convent: 2
- AE Recordings: 1
- Certain Circles: 1
- Thule Records: 1
- One Records: 1
- Permanent Vacation: 1
- Get Physical Music: 1
- All Inn Records: 1
- Purple Print: 1
- Berg Audio: 1
- Deep Moments: 1
- Mulen: 1

## Top artists

- Subb-an: 3
- Eddie Richards: 3
- Anton Kubikov: 1
- Blind Box feat Hector Moralez: 1
- Tecture: 1
- Satoshi Tomiie: 1
- NonniMal: 1
- SOST: 1
- Yamen & EDA: 1
- Rhode & Brown: 1
- Fred P: 1
- Halo Varga: 1
- Zenk: 1
- B1 Floog: 1
- Steve O'Sullivan: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 123.0 and 128.5 (ORBIT FLOW p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent ORBIT FLOW genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent ORBIT FLOW keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent ORBIT FLOW labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 ORBIT FLOW artists or exact match in corpus

## Outliers in current ORBIT FLOW folder

- Count: 11 / 36

- 15.0% | Ani — Love Is The Message (For Those Who Didn't Hear It) | BPM 122.38 | Classic House | low_confidence; bpm_outside_p10_p90; singleton_genre_in_flow
- 40.0% | Ackermann, Vinicius Honorio — Count the dead and wait for morning (129bpm version) | BPM 129.0 | House | low_confidence; bpm_outside_p10_p90
- 55.0% | SOST — Street Walk (Original Mix) | BPM 131.0 | Minimal  Deep Tech | bpm_outside_p10_p90; singleton_genre_in_flow
- 55.0% | Steve O'Sullivan — No Aura (Original Mix) | BPM 130.0 | Minimal / Deep Tech | bpm_outside_p10_p90
- 55.0% | Young Adults — A2 Porcetta (Mf Dub) VINYL ONLY | BPM 130.04 | Minimal | bpm_outside_p10_p90
- 55.0% | Arturo Garces — Just A Little Bit | BPM 121.0 | House | bpm_outside_p10_p90
- 60.0% | Dub Taylor — Concentration | BPM 123.0 | Techno | singleton_genre_in_flow
- 60.0% | Tom Ellis — One Man Riot (Original Mix) | BPM 124.0 | Minimal House | singleton_genre_in_flow
- 70.0% | Anton Kubikov — When Is Deep (Idealist Remix) | BPM 122.0 | Techno (Peak Time / Driving) | bpm_outside_p10_p90
- 75.0% | Fred P — 6AM (Original Mix) | BPM 124.0 | Electronica / Downtempo | singleton_genre_in_flow
- 100.0% | Rhode & Brown — Underwater Bounce (DJ Popup Remix) | BPM 127.0 | Indie Dance | singleton_genre_in_flow

## Usage

Use `orbit_flow_profile_rules.json` + `orbit_flow_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
