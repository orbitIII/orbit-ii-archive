# Orbit II Automation Plan

## Overview
We run three collaborating automations during the current collection phase:

| Agent | Trigger | Primary Output | Notes |
| --- | --- | --- | --- |
| Archive Agent | Manual start / scheduled once per week | Updates `berghain_2024_2026_events.csv`, `press_texts.csv`, optionally imports new artists to `artists_raw.csv` | Uses Browser/MCP tools to scrape source pages, ensures rules (no invented DNA) are honored. Saves URLs, rooms, artist lists. |
| Trend Agent | Follows each Archive run | Appends summary to `observations.md`, generates new Markdown entry in `labels_communities_aesthetics.md`, optionally writes a short vision snippet | Examines collected data for recurring rooms/artists/labels, cross-checks known tools, identifies future-looking signals. |
| Contrarian Agent | Runs after Trend | Updates `observations.md` with validations, notes gaps, and proposes next Archive refinements | Checks for mismatches, missing sources, automation friction and records a recommendation line (preface with `Contrarian note:`). |


## Triggering the First Run
1. **Manual initiation** – run the Archive Agent once to index events for 2024. Launch the automation from Cursor’s Automations tab and select the newly drafted prompt (see `docs/agent_prompts.md`).
2. **Tools** – give the Archive Agent access to:
   - Browser tab or MCP tool that can fetch HTML for Berghain/Panorama event pages.
   - File writes to the CSVs under `berghain_2024_2026_*.csv`.
   - Memory: include the `env` (Orbit II rules) so it remembers not to invent data.
3. **Outputs** – instruct the agent to:
   - Append new rows with Date, Year, Month, EventTitle, Rooms, ArtistsPerRoom, Pressetext, SourceURL, Notes.
   - Add press text snapshots to `berghain_2024_2026_press_texts.csv`.
   - If the agent finds new artists, note them in `artists_raw.csv` with Role/Labels/NotableEvents and log frequency glimpses in `artist_frequency`.

## Follow-up Sequence
- Once the Archive run completes, manually trigger the Trend Agent with the same dataset to produce a 2–3-year forecast note and highlight any possible passive income tie-ins (curated lists, shop partnerships, Rekordbox folder automation).
- Run the Contrarian Agent to look for missing data, conflicting evidence, and operational improvements (e.g., unify store windows, feed new folder tags).
- Review generated Markdown sections and adjust triggers for next cycle (e.g., schedule weekly if data volume justifies it).

## Visibility & Outputs
- Keep the CSV files in the project root so they are visible in the UI – they document every event/artist/press snippet and give you “something tangible.”
- Use `berghain_2024_2026_observations.md` to capture highlights, including Trend + Contrarian messages. This serves as the narrative board you'd describe.
- As data accumulates, convert CSV snippets into Rekordbox playlists (Flow/Push/Moment) by linking frequencies in `berghain_2024_2026_artist_frequency.csv` to your folder structure. Then run a small script (future automation) to emit Rekordbox-compatible CSVs for import.

## Next Automation Enhancements
- Later, add a `Rekordbox Agent` that reads artist tags and assigns each track to one of the `AI-LAB` subfolders (flow/push/moments) and writes the corresponding Playlist export.
- Add `Label`, `Community`, or `Structure` agents to keep catalogs of stores/collectives and annotate aesthetics for each event.
