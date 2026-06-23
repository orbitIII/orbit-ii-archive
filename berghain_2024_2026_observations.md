# Berghain 2024–2026 Observations

## Status
- Project: Orbit II (DJ research archive)
- Phase: Sammlung
- Focus: Panorama Bar, warm-up/deep grooves, minimal house, groove, closing sets
- No judgments, no top lists, no final DNA yet

## What we have
- Berghain 2010 archive completed (events, artists, press texts, labels, communities, aesthetics)
- Current task: Process 2024–2026 events with full coverage for 2024/2025, partial 2026
- Folder-based output (flow, push, moment variation) to match Rekordbox workflow

## Next moves
- Create CSV templates for events, artists, press texts, label/community/aesthetic mapping
- Define agent prompts for Archive/Trend/Contrarian to collect new sources and validate DNA
- Surface emerging terms from Panoramabar sets and associated stores/labels

## Immediate note
- Keep human-in-the-loop decisions (e.g., keep/delete tracks) but automate tagging, folder suggestions, and Rekordbox exports based on Panorama bar DNA.

### Archive handoff 2026-06-23
- Added events: 134 source-linked Klubnacht rows generated from `berghain/klubnacht_2024_2026.json` (2024: 52, 2025: 51, 2026: 31); 126 rows include Panorama Bar.
- Added artists/frequency updates: 660 literal artist entries and 1957 sourced artist slots. Top repeated literal entries: nd_baumecker (19), Steffi (18), Virginia (18), Fadi Mohem (17), Ben Klock (15), Efdemin (15), Fiedel (15), Massimiliano Pagliara (14), Mike Starr (14), Norman Nodge (14).
- Press/source excerpts captured: 128 event press texts with Berghain event URLs in `berghain_2024_2026_press_texts.csv`.
- Unresolved gaps: archive import is Klubnacht-only; non-Klubnacht Panorama Bar nights, RA pages, TrackID pages, store charts, and release catalogs are not yet cross-linked. Some lineup labels are source metadata, not verified release affiliations.
- Recommended next sources: spot-check selected Berghain event URLs, then enrich Panorama Bar artists through Resident Advisor event pages, TrackID, Hardwax, Yoyaku, Sound Metaphors, Seven Records Community Store, and Bandcamp.

### Trend note 2026-06-23
- Signal 1: Panorama Bar is present in 126/134 Klubnacht rows, with room slot counts of Berghain: 960, Panorama Bar: 881, Garten: 58, Säule: 35, XXX-Floor: 14, Elektroakustischer Salon: 9. This supports using Panorama Bar as the primary filter while retaining Berghain/Garten context.
- Signal 2: Repeated lineup metadata labels include Ostgut Ton (126), Funnuvojere (33), Running Back (21), Candy Mountain (19), candy mountain (18), Klockworks (18), MOHEM (17), Love On The Rocks (14), Mord (13), Soundstream (13), WSNWG (12), Mute (12), Faith Beat (12), Public Possession (11), BAD MANNERS (11). Treat these as source-visible routing hints until release catalogs confirm artist-label relationships.
- Signal 3: Repeated press-language terms include techno (106), house (105), groove (31), disco (30), dub (24), acid (22), electro (22), minimal (18), vocal (17), percussion (12), breaks (12), garage (9), trance (7). These are collection-phase signals for folder routing, not final genre DNA.
- Folder routing implications: use `flow` when press text or lineup context references house, disco, groove, or Panorama Bar continuity; use `push` for percussive, techno, electro, breaks, or acid pressure; use `moment_deep` for dub/deep-house language; use `moment_driving` for techno/trance/electro momentum; use `moment_vocal` only when vocal/gesang language or hook-led source text appears.
- Comparable tools and Orbit II difference: Resident Advisor, TrackID, store charts, and Bandcamp can identify tracks and releases, while this archive now adds source-linked room/date context and can connect those external finds to Rekordbox folder decisions.
- Product/passive-income hints: source-linked Panorama Bar research notes and Rekordbox-ready routing exports are plausible only after TrackID/store enrichment confirms actual tracks, labels, and availability.
- Archive instructions for next run: prioritize non-Klubnacht Panorama Bar events and external track/release sources for the highest-frequency Panorama Bar artists before adding interpretive weight.

### Contrarian note 2026-06-23
- Evidence check: the canonical CSVs now replace placeholder `example.com` seed rows with Berghain-sourced event URLs, but the import still depends on the existing structured extraction rather than a fresh page-by-page scrape.
- Counter-signals or mismatches: 8 imported Klubnacht rows do not include Panorama Bar, and Berghain/Garten/Säule slots can skew frequency counts away from the Panorama Bar focus if not filtered during analysis.
- Missing sources: Resident Advisor, TrackID, Hardwax, Yoyaku, Sound Metaphors, Seven Records Community Store, and Bandcamp are referenced in the prompt but remain unenriched in the generated CSVs.
- Operational friction: `events.csv` compresses all room schedules into one `ArtistsPerRoom` cell, so later Rekordbox automation may need normalized event-slot rows with event id, room, artist, time, live flag, and label.
- Contrarian note: Keep frequency counts literal and source-bound; do not treat repeated appearances or lineup labels as Panorama Bar DNA until room-filtered and track-level evidence is added.
- Next Archive adjustment: add a normalized `event_artist_slots` artifact or equivalent fields before external store enrichment, so room-specific artist counts can be computed without parsing a prose cell.
- Next Trend adjustment: produce separate Panorama Bar-only and all-room trend summaries to avoid confusing adjacent Berghain context with the intended folder-routing signal.

