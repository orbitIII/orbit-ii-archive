# Top 50 Panorama Bar Artists Report

## Correction

The prior pass only saw the two placeholder rows in the root CSV inputs. The complete 2024-2026 event archive is present in `berghain/klubnacht_2024_2026.md`, so this iteration rebuilds the Top 50 Panorama Bar artist inputs from that archive file.

## Method

- Parsed every markdown lineup row where `Raum` is exactly `Panorama Bar`.
- Counted 881 Panorama Bar set rows across 2024-2026.
- Found 363 unique Panorama Bar artists after explicit B2B splitting.
- Split explicit `B2B`, `b2b`, `b2bName`, `back to back`, and `face 2 face` listings into individual artist appearances.
- Kept non-B2B artist names as listed, including names with `&`.
- Normalized `PARAMIDA` to `Paramida`.
- Ranked by Panorama Bar appearance count descending, then artist name ascending for ties.

## Outputs updated

- `berghain_2024_2026_artist_frequency.csv` now contains 50 Panorama Bar artists instead of the previous placeholder row.
- `berghain_2024_2026_artists_raw.csv` now contains the same 50 artists with role, label, event examples, and rank notes.
- `berghain_2024_2026_top50_panorama_bar_artists.csv` is a dedicated ranked Top 50 file with counts, years, labels, example event URLs, and counting notes.

## Top 10

| Rank | Artist | Panorama Bar appearances |
|---:|---|---:|
| 1 | nd_baumecker | 18 |
| 2 | Richard Akingbehin | 13 |
| 3 | BASHKKA | 12 |
| 4 | Gerd Janson | 12 |
| 5 | Mike Starr | 12 |
| 6 | Ogazón | 12 |
| 7 | Paramida | 12 |
| 8 | Cinthie | 11 |
| 9 | Gabrielle Kwarteng | 11 |
| 10 | Lakuti | 11 |

## Validation

- Verified the frequency CSV has exactly 50 artist rows.
- Verified all rows have `PrimaryRooms = Panorama Bar`.
- Verified ranks/counts are derived from `berghain/klubnacht_2024_2026.md`.
- Verified every dedicated Top 50 row includes at least one Berghain event URL.

## Notes for track-overlap research

The external track-overlap CSV from the previous pass remains an incomplete seed based on the two artists researched before this Top 50 correction. The next overlap iteration should use the corrected Top 50 files as the act input set and should not treat the current overlap CSV as complete for all 50 artists.
