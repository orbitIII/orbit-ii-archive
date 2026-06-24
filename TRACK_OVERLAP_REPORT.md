# Berghain / Panorama Bar Top 50 Track Overlap Report

## Scope

The required archive inputs were read from:

- `berghain_2024_2026_artist_frequency.csv`
- `berghain_2024_2026_artists_raw.csv`
- `berghain_2024_2026_events.csv`

Those files currently expose only two Panorama Bar / Berghain acts:

1. Paramida
2. André Galuzzi

Because the archive does not contain 50 distinct acts, this iteration processes the complete available act set rather than inventing missing artists. Public sources often spell the second artist as **André Galluzzi**; the CSV keeps the archive spelling in `top50_acts` and notes the public spelling where relevant.

## Counts

- Top 50 acts processed: 2 available archive acts
- Source pages searched: 11
- Targeted overlap searches run: 6
- Verified tracks written to CSV: 86
- Verified multi-act overlaps discovered: 0
- Low-confidence rows retained: 0

## Sources searched

### Paramida

- Resident Advisor: `https://ra.co/podcast/723`
- MixesDB RA.723 mirror: `https://www.mixesdb.com/w/2020-04-06_-_Paramida_-_Resident_Advisor_(RA.723)`
- MixesDB Essential Mix: `https://www.mixesdb.com/w/2024-03-09_-_Paramida_-_Essential_Mix`
- DJ Tracklists Essential Mix: `https://tracklists.thomaslaupstad.com/paramida-essential-mix-2024-03-09-tracklist/`
- MixesDB BBC Radio 1 Residency: `https://www.mixesdb.com/w/2023-01-06_-_Paramida_-_Residency,_BBC_Radio_1`
- DJ Tracklists BBC Radio 1 Residency: `https://tracklists.thomaslaupstad.com/paramida-residency-2023-01-06-tracklist/`
- DJ Tracklists R1s Wind Down Presents: `https://tracklists.thomaslaupstad.com/ostgut-ton-paramida-r1s-wind-down-presents-2021-04-17-tracklist-playlist/`

### André Galuzzi / André Galluzzi

- MixesDB Boiler Room Berlin: `https://www.mixesdb.com/w/2013-10-16_-_Andr%C3%A9_Galluzzi_@_Boiler_Room_Berlin`
- Discogs Berghain 01: `https://www.discogs.com/release/586244-Andr%C3%A9-Galluzzi-Berghain-01`
- se7en.ws Berghain 01 listing: `https://se7en.ws/andre-galluzzi-berghain-01/`
- MixesDB Berghain 01 listing: `https://www.mixesdb.com/w/2005-11-07_-_Andr%C3%A9_Galluzzi_-_Berghain_01`

### Targeted overlap searches

Targeted searches checked likely candidates from the two act source sets, including:

- Paramida + André Galluzzi same track
- Paramida + Âme - Rej
- Paramida + La Fleur - Nightflow (Kenny Larkin Drama Mix)
- Paramida + Ian Pooley - CompuRhythm (Baikal Remix)
- André Galluzzi + Alex Kassian
- André Galluzzi + Tornado Wallace

No targeted search returned reproducible evidence that the same track was played or referenced by both available archive acts.

## Strongest overlaps discovered

No verified multi-act track overlap was discovered in this iteration.

The strongest evidence clusters are single-act confirmations:

- Paramida RA.723: 15 tracks verified by Resident Advisor and MixesDB.
- André Galuzzi / André Galluzzi Berghain 01: 13 tracks verified by Discogs and se7en.ws release listings.
- Paramida Essential Mix 2024-03-09: 23 tracks verified by MixesDB.
- Paramida BBC Radio 1 Residency 2023-01-06: 13 tracks verified by MixesDB and DJ Tracklists.
- Paramida R1s Wind Down Presents 2021-04-17: 13 tracks verified by DJ Tracklists.
- André Galuzzi / André Galluzzi Boiler Room Berlin 2013-10-16: 9 identified tracks verified by MixesDB.

All CSV rows are therefore `Medium` confidence: each has at least one public source and one URL, but no row is confirmed across multiple Top 50 acts.

## Weak evidence removed

The following evidence was excluded from the CSV:

- Unknown / unidentified slots from the André Galluzzi Boiler Room tracklist.
- Search-result synthesis that described stylistic similarity but did not identify a shared track.
- Candidate overlaps where only one of the two available archive acts had a verified source.
- The conflicting MixesDB Berghain 01 track 3 variant; the CSV uses the Discogs and se7en.ws release-listing consensus instead.
- Any track without a public URL, source platform, and explicit act association.

## Missing sources and limitations

- The archive inputs contain two acts, not 50, so the output cannot represent a true Top 50 matrix yet.
- No confirmed 1001Tracklists pages were found for the two available acts during this pass.
- TrackID.net and SoundCloud comment evidence was searched conceptually but no reproducible, row-level source URL was found for a shared track.
- Some pages use the public spelling "André Galluzzi" while the archive uses "André Galuzzi"; this should be normalized in a future archive pass.

## Recommendations for the next research iteration

1. Expand the archive event data so the Top 50 selection is based on a meaningful ranked list rather than the current two-act subset.
2. Add a normalized artist alias table before matching external sources, especially for diacritics and spelling variants.
3. Store source snapshots or extracted tracklist text alongside the CSV to make future audits easier.
4. Prioritize official mix pages, TrackID.net pages, 1001Tracklists pages, and source pages with stable URLs before using mirrored databases.
5. Add an overlap-only filtered view once more acts are available, keeping the evidence matrix as the auditable raw layer.
