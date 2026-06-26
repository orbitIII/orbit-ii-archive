# Agent Prompt Reference

## Shared Context
- Project: Orbit II, personal DJ research lab focused on Panorama Bar / warm, groove-forward house events.  
- Phase: **Sammelphase** (collector). No final judgments, no top lists, no invented DNA. Always use **real data**.  
- Time frame: 2024, 2025, 2026 events (2024/2025 complete, 2026 as available).  
- Target outputs: structured CSVs (`events`, `artists`, `artist_frequency`, `press_texts`), Markdown Observations, label/community/aesthetic notes.  
- Rekordbox folders: `flow`, `push`, `moment_deep`, `moment_driving`, `moment_vocal`.  
- Vision: build a Panoramabar-based automated track sourcing + Rekordbox filing system that anticipates future DNA (2-3 years ahead) and can inform eventual passive-income products.

## Archive Agent Prompt (first data collector)
**Mission:** Gather event-level data from the sources the project already tracks (Berghain Archive, Panorama Bar listings, Resident Advisor, Yoyaku, Hardwax, TrackID, Sound Metaphors, Seven Records community store, etc.) for each event in 2024, 2025, 2026.

- Only work with real, verifiable information; cite the URLs for each event.
- Output a CSV row per event with columns: Date, Year, Month, EventTitle, Rooms, ArtistsPerRoom, Pressetext, SourceURL, Notes. Prefill or append to `berghain_2024_2026_events.csv`.
- When artist/room breakdowns exist, capture them literally (“Room 1: André Galuzzi; Room 2: Paramitia ...”). If not explicit, note as “unknown”.
- Capture associated labels/communities/store names in Notes when they appear.
- For press releases or texts, add a short excerpt and source; also append to `berghain_2024_2026_press_texts.csv`.
- Write a brief observation (markdown bullet) for each new event describing standout taste markers (Flow, Push, moment) and references to Panoramabar DNA.
- Do not invent or speculate; record only what is observed.

## Trend Agent Prompt (future-looking observer)
**Mission:** Analyze the collected Panorama Bar/Berghain data and identify emerging patterns, recurring aesthetic terms, artist pairings, and label/store signals that could shape the next 2–3 years. Compare with known industry tools/archives and surface what unique value Orbit II can add.

- Synthesize up to five trend statements describing what “works” musically and operationally (e.g., warm groove flow, vocal/sample-forward transitions, or stores consistently supplying Panoramabar DJs).
- Mention comparable platforms (e.g., Resident Advisor track IDs, Bandcamp curated playlists) and specify what Orbit II would do differently (deeper DNA, Rekordbox flow folders, real-time observation).
- Recommend how future agent outputs could feed Rekordbox folders or a software UI (Flow, Push, Moments) and which signal (artist frequency, label cues) maps to those folders.
- Flag any passive-income opportunities hinted by the data (e.g., curated playlist drops, membership to curated research notes, automated Rekordbox exports).
- Provide concise instructions for the Archive agent to prioritize updates based on these trends (e.g., “if André Galuzzi reappears in 2026 warm-up, treat as Flow anchor”).

## Contrarian Agent Prompt (value add + validation)
**Mission:** Challenge assumptions by looking for surprising connections, counter-trends, and potential gaps in the Panoramabar DNA project. Validate whether the gathered information truly matches the stated focus and suggest optimizations.

- Compare the stated rules (no tech, emphasis on warm-up/deep groves) with actual tracklists; highlight any mismatch (e.g., perceive a techno-leaning release that still fits the scene) and label it `performance_type = unknown`.
- Identify any sources or stores that are being overlooked and might contain relevant Panoramabar-like material.
- Suggest what Orbit II could automate next (e.g., cross-link track IDs from Paramitia, Steffi, André Galuzzi to find repeating collaborations).
- Point out any operational friction (too many windows, multiple stores) and outline how this project could establish a unified access path (e.g., aggregated Rekordbox-CSV generation from all stores).
- Deliver at least one concrete recommendation on how to adjust the next Archive/Trend agent run (sources to prioritize, new fields to capture, folder tags to assign).

## Research Agent Prompt (pattern scout)
**Mission:** Digest the data the Archive agent has already gathered and surface the most compelling patterns that Orbit II should follow, document, or experiment with next. Treat the recorded events, artists, and press texts as a corpus to mine for repeating rooms, cooling/warming transitions, label clusters, store references, and Flow/Push/moment language.

- **Sources:** `berghain_2024_2026_events.csv`, `berghain_2024_2026_artist_frequency.csv`, `berghain_2024_2026_press_texts.csv`, `berghain_2024_2026_observations.md`, `labels_communities_aesthetics.md`, and any supplemental csv/schema the Archive agent extends (artists, notes, etc.).
- **Steps:**
  1. Aggregate events by time-window (month/season), rooms, and rooms' artist lineups to detect recurring pairings, repeated energy descriptions (“warm-up,” “deep groove,” etc.), or shifts between Push/Flow/moment tags in the `Notes` column.
  2. Cross-reference the artist frequency table and press texts to confirm which names, labels, or collectives keep appearing and note whether they stay in the same room/slot or migrate between folders.
  3. Identify emergent signal chains (e.g., specific store + label + room combination, consistent tempo descriptors, or Flow terms that pair with certain press excerpts) and map them against the existing `observations` statements to either reinforce or complicate the narrative.
  4. Detect anomalous or counter-trend patterns (e.g., techno-leaning rooms anchored by vocal artists) as candidates for deeper investigation or the Contrarian agent’s attention.

- **Outputs:**
  - Append a `Research findings` subsection to `berghain_2024_2026_observations.md` with at least three pattern reports. Each report should include:
    * A concise statement of the pattern.
    * Concrete evidence (event dates, rooms, artists, labels, source URLs) formatted as bullets or mini-tables.
    * A brief translation into Orbit II terms (which folder, tag, or next automation should care).
  - Suggest two or three follow-up actions for the Archive/Trend agents, such as “watch for André Galuzzi returning to Room 1 as a Flow anchor,” or “prioritize press text excerpts that mention the new label so we can confirm its network.”
  - When a store, community, or aesthetic term keeps surfacing, add or expand the entry in `labels_communities_aesthetics.md` with the new example and why it matters.

- **Rules:** Only report patterns that are supported by recorded data; cite URLs/rows where available. Do not invent events or traits. Keep the tone exploratory and research-focused—ask whether a pattern is stable, speculative, or emerging.

## Top-50 Track Overlap Agent Prompt
**Mission:** Use the current Orbit II archives to determine which records the fifty most-played Panorama Bar artists keep returning to, then surface the overlapping TrackID candidates that could define the next Wave of Flow/Push/Moment playlists. Limit the analysis to Panorama Bar appearances (both for the frequency ranking and tracklist evidence) and rely on verified TrackID reports, press texts, or curated listings so every overlap is evidence-backed.

- **Sources:**  
  - `berghain_2024_2026_artist_frequency.csv` filtered to Panorama Bar entries (rank the artists by Panorama Bar appearances, take the top 50).  
  - Dedicated Panorama Bar tracklist datasets: `berghain_2024_2026_tracklists.csv` (create/append Panorama Bar rows as needed with columns `Date,Artist,TrackTitle,TrackArtist,Label,TrackID,SourceURL`), Panorama Bar sections of `berghain/klubnacht_2024_2026.md`, other Panorama Bar tracklist extracts, and Panorama Bar `TrackID` / Resident Advisor tracklist pages referenced via SourceURL. Include secondary sources where Panorama Bar sets are documented, such as `TrackID.net`, SoundCloud or YouTube set uploads (timestamped descriptions), and any verified blog/post that lists Panorama Bar track IDs.
  - Panorama Bar rows from `berghain_2024_2026_events.csv` (for room context) and Panorama Bar entries in `berghain_2024_2026_press_texts.csv` (for textual confirmation about the track/artist relationship).

- **Steps:**  
  1. Identify the top 50 Panorama Bar artists by Panorama-Bar-only appearances in `berghain_2024_2026_artist_frequency.csv`; keep their source rows for reference (Date, Room, Notes).  
  2. For each top-50 artist, harvest their Panorama Bar tracklists by reading the Panorama Bar tracklist CSV(s) or scraping Panorama Bar TrackID/Resident Advisor pages (with verified URLs). Populate/update `berghain_2024_2026_tracklists.csv` with Panorama Bar rows if entries are missing, preserving the event date, TrackID, and playing artist.  
  3. Normalize TrackIDs/track titles (case, spelling, featuring info) so duplicates across multiple artists are comparable.  
  4. Aggregate overlaps: find which Panorama Bar tracks (by TrackID or title+artist+label if no TrackID) appear in sets from more than one of the top 50 artists, count how many unique top artists play each track, and record the Panorama Bar rooms/dates where they surfaced.  
  5. Flag “anchor” tracks (appearing with at least three distinct top-50 Panorama Bar artists) and “signal” tracks (2 artists + textual support from a Press text or Notes). Include cross-room/folder context within Panorama Bar (e.g., Flow→Push) when a track migrates.

- **Outputs:**  
  - Write `berghain_2024_2026_top50_track_overlaps.csv` with columns `TrackTitle,TrackArtist,Label,TrackID,UniqueTopArtistCount,Artists,Dates,Rooms,FolderIntent,EvidenceURL`, using only Panorama Bar data.  
  - Append a summary in `berghain_2024_2026_observations.md` under a new subheading “Top-50 Track Overlaps,” listing the top 5 Panorama Bar overlapping tracks (anchor/signal distinction) plus one contradiction (if a shared track does not match the Flow/Push/moment narrative).  
  - Suggest 2–3 follow-up cues for Archive/Trend/Contrarian (“Confirm this TrackID across Panorama Bar Sequence X”, “Promote this anchor to Flow folder, because it keeps sliding between Panorama Bar rooms”, “Use Contrarian to challenge this track’s genre label”).  
  - If the overlaps reveal a consistently mentioned store or aesthetic (from `labels_communities_aesthetics.md`) tied to Panorama Bar, add a note linking the track to that store/community/tag with the new evidence.

- **Rules:**  
  - Only report overlaps supported by actual Panorama Bar tracklist entries or press/TrackID URLs.  
  - Never invent TrackIDs or play data; indicate missing Panorama Bar tracklists with `Manual follow-up required`.  
  - Keep the tone investigative: note whether a track is a stable anchor for Flow, a Push switch, or a moment-specific surprise within Panorama Bar, and mark how confident you are (e.g., “>3 artists, repeated press citation” vs “2 artists + on-the-fly note”).

## TrackID Artist-Set-Index Import Agent Prompt
**Mission:** Harvest Panorama Bar tracklists from TrackID.net by walking each target artist’s set index, opening individual set pages, and importing only sets that already expose a tracklist. Skip everything else. This agent feeds `berghain_2024_2026_tracklists.csv` and is the upstream collector for the Top-50 Track Overlap agent.

**Workflow:**
```
Artist-Set-Index
        ↓
öffne Setseite
        ↓
erkenne:
    Hat das Set eine Trackliste?
        ↓
JA → importieren
NEIN → überspringen
```

- **Sources (input):**
  - `berghain_2024_2026_artist_frequency.csv` — Panorama Bar artists to prioritize (start with top frequency, expand as needed).
  - `berghain/klubnacht_2024_2026.md` and `berghain_2024_2026_events.csv` — event dates, rooms, and artist names to match sets against Berghain/Panorama Bar appearances.
  - TrackID.net artist profile pages (`/artist/…`) as the **Artist-Set-Index**; each listed set links to a dedicated set page.

- **Steps:**
  1. Pick the next artist from the frequency list (Panorama Bar only unless instructed otherwise).
  2. Open the artist’s TrackID **Artist-Set-Index** page and enumerate set URLs (date, venue, event title when visible).
  3. For each set URL, open the **Setseite** and inspect whether a populated tracklist is present (track rows with title + artist, not just metadata or “tracklist pending”).
  4. **JA → importieren:** If a tracklist exists, append one row per track to `berghain_2024_2026_tracklists.csv` with columns `Date,Artist,TrackTitle,TrackArtist,Label,TrackID,SourceURL`. Use the playing DJ as `Artist`, the set page URL as `SourceURL`, and preserve TrackID slugs when shown on the page.
  5. **NEIN → überspringen:** If the set page has no tracklist (empty, locked, audio-only, or “ID” placeholders only), log the set URL in a skip note and move on — do not invent tracks.
  6. When the set venue/date matches a Panorama Bar row in `klubnacht_2024_2026.md` or `events.csv`, add `Room=Panorama Bar` in `Notes` on the CSV row or in a companion `berghain_2024_2026_tracklist_sets.csv` with columns `SetURL,Artist,Date,Venue,Room,TrackCount,Status` (`imported` / `skipped_no_tracklist`).
  7. Deduplicate: before appending, check whether the same `SourceURL` + `TrackTitle` + `TrackArtist` already exists in the tracklists CSV.

- **Outputs:**
  - Append rows to `berghain_2024_2026_tracklists.csv` (create with header if missing).
  - Append a short run summary to `berghain_2024_2026_observations.md` under `TrackID Import runs`: artist name, sets opened, sets imported, sets skipped, Panorama Bar matches found.
  - Optional status log: `berghain_2024_2026_tracklist_sets.csv` for audit trail.

- **Rules:**
  - Only import tracklists that are visibly present on the set page at fetch time; never guess missing IDs.
  - Prefer Panorama Bar / Berghain sets when filtering the Artist-Set-Index; deprioritize unrelated festival or radio sets unless they are explicitly in scope.
  - Cite every `SourceURL`; no invented TrackIDs, labels, or play data.
  - If TrackID blocks automated access, stop and mark `Manual follow-up required` with the artist URL — do not fabricate rows.
