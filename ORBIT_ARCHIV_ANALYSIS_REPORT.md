# ORBIT ARCHIV Analysis Report

Source: `/Users/alanwillson/orbit-ii-archive/rekordbox/exports/archiv_snapshot.csv`
Playlist analyzed: **ORBIT ARCHIV**

> Live Rekordbox DB playlist `ARCHIV ` (202 tracks).

## Corpus

- Tracks in playlist: 202
- Unique artists: 161
- Unique labels: 110
- Unique genres (Rekordbox tags): 13
- Unique keys: 23

## BPM (measurable)

- Range: 120.0 – 139.0
- Mean / median: 126.33 / 126.0
- p10 – p90: 122.04 – 130.0
- Stdev: 3.39

## Top genres (Rekordbox field, no reinterpretation)

- Tech House: 60 (29.7%)
- House: 45 (22.3%)
- Minimal: 43 (21.3%)
- Deep House: 19 (9.4%)
- Techno: 10 (5.0%)
- Techno (Peak Time / Driving): 6 (3.0%)
- Indie Dance: 6 (3.0%)
- Techno (Raw / Deep / Hypnotic): 5 (2.5%)
- Minimal / Deep Tech: 3 (1.5%)
- Techno (Peak Time / Driving / Hard): 2 (1.0%)
- Leftfield House & Techno: 1 (0.5%)
- Minimal  Deep Tech: 1 (0.5%)
- Trance (Raw / Deep / Hypnotic): 1 (0.5%)

## Top keys

- Am: 25
- Gm: 22
- Abm: 19
- Fm: 18
- F#m: 16
- Ebm: 15
- Em: 13
- Dm: 12
- Bbm: 10
- Cm: 7

## Top labels

- Rekids: 20
- Fabric: 19
- All Inn: 6
- Rawax: 5
- Purple Print: 5
- Certain Circles: 5
- AE Recordings: 4
- Holding Hands Records: 4
- HOWL Label: 3
- Kalahari Oyster Cult: 3
- Repeat: 3
- Blind Box Series: 3
- Echocentric Records: 3
- Baku: 2
- BodyParts Vinyl: 2

## Top artists

- iO (Mulen): 5
- Pola: 4
- Anton Kubikov: 3
- Mathias Kaden: 3
- Subb-an: 3
- WALKER: 3
- Unknown Artist: 3
- Baku: 2
- Oshana: 2
- Varhat: 2
- Los Hermanos: 2
- Mark Broom: 2
- Markus Suckut: 2
- Moodena, Charles Levine: 2
- NDA, Bryan Kessler, Ennio: 2

## Derived rules (for auto-scoring new tracks)

- **bpm_within_p10_p90** (weight 30%): BPM between 122.04 and 130.0 (ORBIT ARCHIV p10–p90)
- **genre_in_top8** (weight 25%): Genre matches one of the 8 most frequent ORBIT ARCHIV genres
- **key_in_top8** (weight 15%): Tonality matches one of the 8 most frequent ORBIT ARCHIV keys
- **label_in_top15** (weight 15%): Label matches one of the 15 most frequent ORBIT ARCHIV labels
- **artist_in_flow_corpus** (weight 15%): Artist appears among top-25 ORBIT ARCHIV artists or exact match in corpus

## Outliers in current ORBIT ARCHIV folder

- Count: 39 / 202

- 15.0% | Sean Deason — RUMSPRINGA 1 | BPM 131.98 | Leftfield House & Techno | low_confidence; bpm_outside_p10_p90; singleton_genre_in_flow
- 30.0% | Mandar — A1 Straight Sneaky VINYL ONLY  | BPM 135.0 | Techno (Peak Time / Driving / Hard) | low_confidence; bpm_outside_p10_p90
- 30.0% | Ciel & CCL — Tilda's Goat Stare (Priori Remix) | BPM 132.0 | Trance (Raw / Deep / Hypnotic) | low_confidence; bpm_outside_p10_p90; singleton_genre_in_flow
- 40.0% | A2 Latent — Groove Rhythm Machine VINYL ONLY  | BPM 121.72 | Indie Dance | low_confidence; bpm_outside_p10_p90
- 40.0% | Kid Only — Recovery | BPM 121.99 | Tech House | low_confidence; bpm_outside_p10_p90
- 40.0% | Demi Riquísimo — Direct Fix (Original Mix) | BPM 138.0 | House | low_confidence; bpm_outside_p10_p90
- 40.0% | Big Zen — Prayer Bass (Original Mix) | BPM 137.02 | Deep House | low_confidence; bpm_outside_p10_p90
- 55.0% | Young Adults — B2 Voicemail VINYL ONLY  | BPM 132.04 | Minimal | bpm_outside_p10_p90
- 55.0% | Anton Kubikov — When Is Deep (Thor & Octal Industries Remix) | BPM 122.0 | Techno (Peak Time / Driving) | bpm_outside_p10_p90
- 55.0% | Phil Asher & James Massiah — Time & Space | BPM 121.0 | Techno | bpm_outside_p10_p90
- 55.0% | Soul Of Hex — Jynmu | BPM 120.0 | Deep House | bpm_outside_p10_p90
- 55.0% | Tuccillo — EVES SKY | BPM 120.0 | Deep House | bpm_outside_p10_p90
- 55.0% | Urulu — Body Drum (Original Mix) | BPM 122.0 | Deep House | bpm_outside_p10_p90
- 55.0% | Anton Kubikov — When Is Deep (Thor & Octal Industries Remix) | BPM 122.0 | Techno (Peak Time / Driving) | bpm_outside_p10_p90
- 55.0% | Phil Asher & James Massiah — Time & Space | BPM 121.0 | Techno | bpm_outside_p10_p90
- 55.0% | Voigtmann — Leftfoot Lover (Original Mix) | BPM 131.0 | Tech House | bpm_outside_p10_p90
- 55.0% | WALKER — Untitled A | BPM 132.85 | House | bpm_outside_p10_p90
- 55.0% | SnPLO — A1 A VINYL ONLY  | BPM 133.0 | Minimal | bpm_outside_p10_p90
- 55.0% | Minimal Man — A1 Chicken Store + Chickapella VINYL ONLY  | BPM 133.06 | Minimal | bpm_outside_p10_p90
- 55.0% | C1 Persound — Conspirators Of Pleasure VINYL ONLY  | BPM 120.0 | Minimal | bpm_outside_p10_p90

## Usage

Use `orbit_archiv_profile_rules.json` + `orbit_archiv_track_scores.csv` to score candidate tracks.
No subjective genre labels are added; only Rekordbox metadata fields are used.
