# ORBIT CORE Analysis Report

Source: `/Users/alanwillson/orbit-ii-archive/rekordbox/exports/core_snapshot.csv`
Playlist analyzed: **ORBIT CORE**

> Live Rekordbox DB playlist `CORE ` (64 tracks).

## Corpus

- Tracks in playlist: 64
- Unique artists: 43
- Unique labels: 31
- Unique genres (Rekordbox tags): 12
- Unique keys: 19

## BPM (measurable)

- Range: 122.0 – 138.0
- Mean / median: 128.84 / 128.0
- p10 – p90: 124.3 – 133.7
- Stdev: 3.53

## Top genres (Rekordbox field, no reinterpretation)

- House: 35 (54.7%)
- Deep House: 10 (15.6%)
- Tech House: 4 (6.2%)
- Minimal: 3 (4.7%)
- Techno (Raw / Deep / Hypnotic): 3 (4.7%)
- Deep Tech: 2 (3.1%)
- Minimal / Deep Tech: 2 (3.1%)
- Minimal House: 1 (1.6%)
- Techno: 1 (1.6%)
- Techno (Raw  Deep  Hypnotic): 1 (1.6%)
- Indie Dance: 1 (1.6%)
- Classic House: 1 (1.6%)

## Top keys

- Gm: 10
- Am: 8
- Em: 6
- Fm: 6
- Dm: 5
- Abm: 4
- Ab: 3
- F#m: 3
- Cm: 3
- Bbm: 3

## Top labels

- SEVEN: 12
- Faith Beat: 9
- R.A.N.D. Muzik Recordings: 4
- Major Records NYC: 4
- Talman Records: 4
- X-Kalay: 2
- Safe Space: 2
- Eastenderz: 2
- Surreal: 2
- a.2aum: 2
- Cecille: 1
- SCKT: 1
- Rutilance Recordings: 1
- Rekids: 1
- Love On Cropsey: 1

## Top artists

- Subb-an: 7
- Soul of Hex: 4
- Okain: 4
- Ferrari: 4
- Ground16: 3
- Pancratio: 2
- Davy, stbr: 2
- Baka G: 2
- Coke, Stoned & Baileys: 2
- iO (Mulen): 1
- Markus Suckut: 1
- Christoph Faust: 1
- Asphalt DJ: 1
- Paolo Macrì: 1
- CRYME: 1

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 124.3 and 133.7 (ORBIT CORE p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent ORBIT CORE genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent ORBIT CORE keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent ORBIT CORE labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 ORBIT CORE artists or exact match in corpus

## Outliers in current ORBIT CORE folder

- Count: 18 / 64

- 15.0% | Whitesquare — Hypnophobia (Original Mix)  | BPM 124.0 | Indie Dance | low_confidence; bpm_outside_p10_p90; singleton_genre_in_flow
- 40.0% | Satoshi Tomiie — Hauz Muzik (Original Mix) | BPM 122.0 | House | low_confidence; bpm_outside_p10_p90
- 45.0% | Whiplash, New York Slick — Over Me (Whiplash presents New York Slick) (Londonary Mix) | BPM 125.0 | Classic House | low_confidence; singleton_genre_in_flow
- 55.0% | Baka G — No Breaks All Fun (Retromigration Remix) | BPM 134.0 | House | bpm_outside_p10_p90
- 55.0% | BLANKA (ES) — Fearless (Original Mix) | BPM 124.0 | Minimal / Deep Tech | bpm_outside_p10_p90
- 55.0% | Ackermann — The Feeling That Brought You Here (Confidential Recipe Remix) | BPM 138.0 | Deep House | bpm_outside_p10_p90
- 55.0% | Soul of Hex — Computer Jazz (Original Mix) | BPM 123.0 | House | bpm_outside_p10_p90
- 55.0% | S.A.M. — Got Me Down (Extended Mix) | BPM 135.0 | Deep House | bpm_outside_p10_p90
- 55.0% | YNNY — Take 5 (Original Mix) | BPM 136.0 | Deep House | bpm_outside_p10_p90
- 55.0% | DJ Steaw — Feel (Original Mix) | BPM 124.0 | Tech House | bpm_outside_p10_p90
- 60.0% | Subb-an — Grooves & Tools (Sub Series Tool 007) (Sub Series Tool 007) | BPM 131.0 | Techno (Raw  Deep  Hypnotic) | singleton_genre_in_flow
- 70.0% | Soul of Hex — Power Twice (Original Mix) | BPM 123.0 | House | bpm_outside_p10_p90
- 70.0% | Paolo Macrì — Outbreak (Original Mix) | BPM 124.0 | Deep House | bpm_outside_p10_p90
- 70.0% | CucaRafa & CRYME — Esquerda, Direita (Cryme Remix) | BPM 135.0 | Techno (Raw / Deep / Hypnotic) | bpm_outside_p10_p90
- 70.0% | MARGO (Germany), BRUNA (Germany) — Danca Ritmo (Original Mix) | BPM 138.0 | House | bpm_outside_p10_p90
- 70.0% | Zombies In Miami — Unknown Pleasure (Original Mix) | BPM 135.0 | House | bpm_outside_p10_p90
- 75.0% | Radio Slave — Don't Stop No Sleep  | BPM 128.0 | Techno | singleton_genre_in_flow
- 85.0% | Davy, stbr — Ghost in the Jar (Original Mix) | BPM 128.0 | Minimal House | singleton_genre_in_flow

## Usage

Use `orbit_core_profile_rules.json` + `orbit_core_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
