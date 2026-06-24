# TrackID.net Top 50 Panorama Bar Overlap Report

## Scope

This pass used `berghain_2024_2026_top50_panorama_bar_artists.csv` as the artist universe and checked TrackID.net search, audiostream, and musictrack pages for reproducible track overlap evidence.

The output is:

- `berghain_2024_2026_top50_trackid_overlaps.csv`
- appended TrackID overlap rows in `berghain_2024_2026_top50_track_overlaps.csv`

## Validation rules used

- A row is included only when a TrackID.net page identifies the track and one or more TrackID set titles connect it to Top 50 artists.
- TrackID-only rows are capped at `Medium` confidence because they are verified on one platform, even when several Top 50 artist sets are listed.
- B2B-only or joint-set-only evidence was not treated as a strong independent overlap unless the same TrackID musictrack page also showed the track in another Top 50 set context.
- Unfetched, timed-out, or search-result-only candidates were excluded from the CSV.

## Verified TrackID overlaps

### 1. Barker - Utility

Top 50 acts:

- Gerd Janson
- Nick Höppner
- Paramida
- Massimiliano Pagliara
- Ogazón
- nd_baumecker

TrackID evidence:

- `https://trackid.net/musictracks/barker-utility`
- `https://trackid.net/audiostreams/answer-code-request-x-gerd-janson-live-ostgut-ton-aus-der-halle-am-berghain-arte-concert`
- `https://trackid.net/audiostreams/nick-hoppner-x-klon-dump-live-ostgut-ton-aus-der-halle-am-berghain-arte-concert`
- `https://trackid.net/audiostreams/paramida-x-massimiliano-pagliara-ostgut-ton-halle-am-berghain-live-arteconcert`
- `https://trackid.net/audiostreams/barker-x-baumecker-live-halle-am-berghain-arte-concert`

Notes: The TrackID musictrack page lists additional set-title evidence for `LOTR x RWW - Ogazón - 30 Mar 2022`; the directly fetched Ogazón audiostream URL did not expose a full track table, so the musictrack page is the cited evidence for Ogazón.

### 2. St. David - C'mon let me see

Top 50 acts:

- Paramida
- Massimiliano Pagliara
- Cinthie
- nd_baumecker

TrackID evidence:

- `https://trackid.net/musictracks/st-david-cmon-let-me-see`
- `https://trackid.net/audiostreams/paramida-x-massimiliano-pagliara-ostgut-ton-halle-am-berghain-live-arteconcert`

Notes: The TrackID musictrack page lists `Paramida X Massimiliano Pagliara`, `Cinthie & Meat B2B`, and `DORA TANZT B2B ZUM CSD 2021 MIT MASSIMILIANO PAGLIARA UND ND_BAUMECKER`.

### 3. East Coast Love Affair - Shake

Top 50 acts:

- Cinthie
- Gerd Janson

TrackID evidence:

- `https://trackid.net/musictracks/east-coast-love-affair-shake`
- `https://trackid.net/audiostreams/answer-code-request-x-gerd-janson-live-ostgut-ton-aus-der-halle-am-berghain-arte-concert`

Notes: The TrackID musictrack page lists `Cinthie & Finn Johannsen live at Power House, Paloma, Berlin, June 17th 2022` and `Answer Code Request X Gerd Janson`.

## Weak evidence removed

The following candidate groups were investigated but excluded from the TrackID overlap CSV:

- Ogazón B2B Ryan Elliott rows from a single joint set, because the directly fetched audiostream URL did not expose the full track table in this environment.
- Tama Sumo & Lakuti rows from `Tama Sumo & Lakuti 200226`, because the evidence was a single joint set only.
- André Galluzzi X Ryan Elliott rows from one joint ARTE set, because they were not independent overlaps across separate sets.
- Cevin Fisher - `Mas Groove`, because Natalie Robinson was verified but the Kikelomo evidence could not be reproduced with a fetched TrackID page.
- Alex Kassian / Running Hot / Surco's Groove - `The Love Theme (Edit)`, because the TrackID musictrack page and Alinka set evidence could not be reproduced with fetched pages.
- All candidates returned only by TrackID search snippets, timed-out pages, or blank TrackID pages.

## Coverage limitations

- TrackID.net uses dynamic pages and some URLs returned blank or timed out when fetched.
- TrackID musictrack pages often expose only the first page of tracklist appearances; additional pagination may hide more Top 50 occurrences.
- Several strong-looking matches were joint-set-only. These should be tracked separately from independent multi-artist overlaps.

## Next iteration

1. Use a browser session or approved TrackID export workflow to capture paginated musictrack appearances.
2. Build a normalized alias table for Top 50 artist names, especially `nd_baumecker` / `Baumecker` and diacritics such as `Ogazón`.
3. Separate future output into two categories: independent overlaps and joint/B2B set evidence.
4. Re-run the full 50-artist pass with per-artist TrackID exports so every candidate can be validated mechanically.
