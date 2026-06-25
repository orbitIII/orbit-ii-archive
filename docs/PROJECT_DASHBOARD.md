# ORBIT II

## Project Health

| Metric | Value | Evidence |
| --- | --- | --- |
| Repository status | Clean at scan time | `git status --short` at dashboard scan time |
| Current branch | cursor/top-50-act-track-overlaps-4046 | `git branch --show-current` |
| Last commit | 2444a9c — Add normalized top 50 track evidence schema | 2026-06-25T08:24:29+00:00 |
| Last archive update | 2026-06-25T08:24:29+00:00 | Latest git update among `berghain_*` and `berghain/` files |
| Last automation run | 2026-06-25T08:16:16+00:00 | Latest git update among report / automation docs |

## Archive

### Available datasets

| Dataset | Status | Rows | Last Update | Source | File | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 2010 Events JSON Archive | Available | 3 | 2026-06-23T12:31:58+02:00 | berghain/ archive | `berghain/2010/events_merged.json` | 3af91a0 |
| Artist Frequency | Available | 50 | 2026-06-24T21:15:58+00:00 | Repository root archive | `berghain_2024_2026_artist_frequency.csv` | 573eaed |
| Artists | Available | 50 | 2026-06-24T21:15:58+00:00 | Repository root archive | `berghain_2024_2026_artists_raw.csv` | 573eaed |
| Berghain Klubnacht JSON Archive | Available | 134 | 2026-06-23T12:31:58+02:00 | berghain/ archive | `berghain/klubnacht_2024_2026.json` | 3af91a0 |
| berghain_2024_2026_top50_artist_sets_trackid_part01.csv | Available | 197 | 2026-06-25T08:16:16+00:00 | TrackID.net archive output | `berghain_2024_2026_top50_artist_sets_trackid_part01.csv` | d378c87 |
| berghain_2024_2026_top50_artist_sets_trackid_part02.csv | Available | 172 | 2026-06-25T08:11:57+00:00 | TrackID.net archive output | `berghain_2024_2026_top50_artist_sets_trackid_part02.csv` | fcaa99e |
| berghain_2024_2026_top50_artist_sets_trackid_part03.csv | Available | 172 | 2026-06-25T08:12:35+00:00 | TrackID.net archive output | `berghain_2024_2026_top50_artist_sets_trackid_part03.csv` | 44d6d40 |
| berghain_2024_2026_top50_artist_sets_trackid_part04.csv | Available | 151 | 2026-06-25T08:11:42+00:00 | TrackID.net archive output | `berghain_2024_2026_top50_artist_sets_trackid_part04.csv` | b14c36d |
| berghain_2024_2026_top50_artist_sets_trackid_part05.csv | Available | 146 | 2026-06-25T08:13:24+00:00 | TrackID.net archive output | `berghain_2024_2026_top50_artist_sets_trackid_part05.csv` | 18f7147 |
| Events | Available | 131 | 2026-06-24T21:15:58+00:00 | Repository root archive | `berghain_2024_2026_events.csv` | 573eaed |
| Labels / Communities / Aesthetics | Available | 21 lines | 2026-06-23T12:31:58+02:00 | Repository root archive | `berghain_2024_2026_labels_communities_aesthetics.md` | 3af91a0 |
| Observations | Available | 20 lines | 2026-06-23T12:31:58+02:00 | Repository root archive | `berghain_2024_2026_observations.md` | 3af91a0 |
| Press Texts | Available | 1 | 2026-06-23T12:31:58+02:00 | Repository root archive | `berghain_2024_2026_press_texts.csv` | 3af91a0 |
| Top 50 Panorama Bar Artists | Available | 50 | 2026-06-24T21:15:58+00:00 | Repository root archive | `berghain_2024_2026_top50_panorama_bar_artists.csv` | 573eaed |
| Track Evidence | Available | 98 | 2026-06-25T08:24:29+00:00 | Track evidence / overlap research | `berghain_2024_2026_top50_track_evidence_normalized.csv` | 2444a9c |
| Track Overlaps | Available | 89 | 2026-06-24T23:01:26+00:00 | Track evidence / overlap research | `berghain_2024_2026_top50_track_overlaps.csv` | 901d568 |
| TrackID Artist CSV Manifest | Available | 50 | Current branch update | TrackID.net archive output | `berghain_2024_2026_trackid_artist_csv_manifest.csv` | Current branch update |
| Track Sources / Provider Index | Available | 300 | 2026-06-25T08:16:16+00:00 | Repository root archive | `berghain_2024_2026_top50_artist_set_source_index.csv` | d378c87 |
| TrackID Artist Set Archive | Available | 838 | 2026-06-25T08:16:16+00:00 | TrackID.net archive output | `berghain_2024_2026_top50_artist_sets_trackid.csv` | d378c87 |
| TrackID Overlaps | Available | 3 | 2026-06-24T23:01:26+00:00 | TrackID.net archive output | `berghain_2024_2026_top50_trackid_overlaps.csv` | 901d568 |

### Missing datasets

| Dataset | Expected File | Status | Derived From |
| --- | --- | --- | --- |
| Track Canonicalization | canonical_tracks.csv | Not yet available. | Needed by TRACKID_OVERLAP_REPORT.md and TOP50_ARTIST_SET_ARCHIVE_REPORT.md for alias/canonical track handling. |
| Artist Alias / Disambiguation | artist_aliases.csv | Not yet available. | Needed for broad names flagged in TOP50_ARTIST_SET_ARCHIVE_REPORT.md. |
| Artist Set Tracks | artist_set_tracks.csv | Not yet available. | Recommended next normalized table in TOP50_ARTIST_SET_ARCHIVE_REPORT.md. |
| Knowledge Graph | knowledge_graph.* | Not yet available. | Requested module has no graph file in repository. |
| Rekordbox Exports | rekordbox_exports/*.csv | Not yet available. | docs/future_flow.md describes future export script; no export files exist. |
| Stores / Shop Catalog | stores.csv | Not yet available. | Store/source digging is mentioned in docs/agent_prompts.md; no dedicated catalog exists. |

### File dependencies

| File | Depends on / References |
| --- | --- |
| `berghain_2024_2026_top50_panorama_bar_artists.csv` | `berghain/klubnacht_2024_2026.md` |
| `berghain_2024_2026_artist_frequency.csv` | `berghain/klubnacht_2024_2026.md` |
| `berghain_2024_2026_events.csv` | `berghain/klubnacht_2024_2026.md` |
| `berghain_2024_2026_top50_artist_sets_trackid.csv` | `berghain_2024_2026_top50_panorama_bar_artists.csv`, `berghain_2024_2026_top50_artist_sets_trackid_part01.csv`, `berghain_2024_2026_top50_artist_sets_trackid_part02.csv`, `berghain_2024_2026_top50_artist_sets_trackid_part03.csv`, `berghain_2024_2026_top50_artist_sets_trackid_part04.csv`, `berghain_2024_2026_top50_artist_sets_trackid_part05.csv` |
| `berghain_2024_2026_top50_artist_set_source_index.csv` | `berghain_2024_2026_top50_panorama_bar_artists.csv` |
| `berghain_2024_2026_top50_track_overlaps.csv` | `berghain_2024_2026_top50_panorama_bar_artists.csv`, `berghain_2024_2026_top50_artist_sets_trackid.csv` |
| `berghain_2024_2026_top50_track_evidence_normalized.csv` | `berghain_2024_2026_top50_track_overlaps.csv` |
| `TOP50_ARTIST_SET_ARCHIVE_REPORT.md` | `berghain/klubnacht_2024_2026.md`, `berghain_2024_2026_artist_frequency.csv`, `berghain_2024_2026_artists_raw.csv`, `berghain_2024_2026_top50_artist_set_source_index.csv`, `berghain_2024_2026_top50_artist_sets_trackid.csv`, `berghain_2024_2026_top50_artist_sets_trackid_part01.csv`, `berghain_2024_2026_top50_artist_sets_trackid_part02.csv`, `berghain_2024_2026_top50_artist_sets_trackid_part03.csv` |
| `TOP50_PANORAMA_BAR_ARTISTS_REPORT.md` | `berghain/klubnacht_2024_2026.md`, `berghain_2024_2026_artist_frequency.csv`, `berghain_2024_2026_artists_raw.csv`, `berghain_2024_2026_top50_panorama_bar_artists.csv` |
| `TRACKID_OVERLAP_REPORT.md` | `berghain_2024_2026_top50_panorama_bar_artists.csv`, `berghain_2024_2026_top50_track_overlaps.csv`, `berghain_2024_2026_top50_trackid_overlaps.csv` |
| `TRACK_OVERLAP_REPORT.md` | `TOP50_PANORAMA_BAR_ARTISTS_REPORT.md`, `berghain/klubnacht_2024_2026.md`, `berghain_2024_2026_artist_frequency.csv`, `berghain_2024_2026_artists_raw.csv`, `berghain_2024_2026_events.csv`, `berghain_2024_2026_top50_panorama_bar_artists.csv` |
| `docs/agent_prompts.md` | all `berghain_2024_2026` CSVs, `berghain_2024_2026_artist_frequency.csv`, `berghain_2024_2026_artists_raw.csv`, `berghain_2024_2026_events.csv`, `berghain_2024_2026_labels_communities_aesthetics.md`, `berghain_2024_2026_observations.md`, `berghain_2024_2026_press_texts.csv`, `docs/automation_plan.md` |
| `docs/automation_plan.md` | all `berghain_2024_2026` CSVs, `berghain_2024_2026_artist_frequency.csv`, `berghain_2024_2026_artists_raw.csv`, `berghain_2024_2026_events.csv`, `berghain_2024_2026_observations.md`, `berghain_2024_2026_press_texts.csv`, `berghain_2024_2026_labels_communities_aesthetics.md`, `docs/agent_prompts.md` |
| `docs/future_flow.md` | `berghain_2024_2026_artist_frequency.csv`, `berghain_2024_2026_labels_communities_aesthetics.md`, `berghain_2024_2026_observations.md` |

## Research

| Status | Module | Evidence |
| --- | --- | --- |
| ✅ | Berghain Archive | `berghain/klubnacht_2024_2026.md`, `berghain_2024_2026_events.csv` |
| ✅ | Core Questions | `docs/ORBIT_II_CORE_QUESTIONS.md` |
| ✅ | Top 50 Artists | `berghain_2024_2026_top50_panorama_bar_artists.csv` |
| ✅ | TrackID Sources | `berghain_2024_2026_top50_artist_sets_trackid.csv`, `berghain_2024_2026_top50_artist_set_source_index.csv` |
| 🟡 | Track Canonicalization | `berghain_2024_2026_top50_track_evidence_normalized.csv`; `canonical_tracks.csv` not yet available. |
| ⬜ | Knowledge Graph | Not yet available. |
| ⬜ | Rekordbox Integration | Not yet available. |

## Knowledge Graph Progress

| Node / Edge Type | Rows / Evidence | Status | File |
| --- | --- | --- | --- |
| Events | 131 | Available | berghain_2024_2026_events.csv |
| Artists | 50 | Available | berghain_2024_2026_artists_raw.csv |
| Tracks | 98 | Partial | berghain_2024_2026_top50_track_evidence_normalized.csv |
| Labels | 21 | Partial | berghain_2024_2026_labels_communities_aesthetics.md |
| Stores | 0 | Not yet available. | Not yet available. |
| Communities | 21 | Partial | berghain_2024_2026_labels_communities_aesthetics.md |
| Relationships | 3 | Partial | berghain_2024_2026_top50_trackid_overlaps.csv |
| Track Evidence | 98 | Partial | berghain_2024_2026_top50_track_evidence_normalized.csv |
| Canonical Tracks | 0 | Not yet available. | Not yet available. |

## Digging Engine

| Input | Status | Evidence |
| --- | --- | --- |
| TrackID.net | Available | 50 source-index rows in berghain_2024_2026_top50_artist_set_source_index.csv |
| Discogs | Partial | Referenced in track overlap evidence |
| Bandcamp | Missing | Mentioned in docs/agent_prompts.md but no dedicated dataset rows found. |
| Hardwax | Missing | Mentioned in docs/agent_prompts.md but no dedicated dataset rows found. |
| Yoyaku | Missing | Mentioned in docs/agent_prompts.md but no dedicated dataset rows found. |
| Resident Advisor | Available | 50 source-index rows in berghain_2024_2026_top50_artist_set_source_index.csv |
| MixesDB | Available | 50 source-index rows in berghain_2024_2026_top50_artist_set_source_index.csv |
| SoundCloud | Available | 50 source-index rows in berghain_2024_2026_top50_artist_set_source_index.csv |
| YouTube | Available | 50 source-index rows in berghain_2024_2026_top50_artist_set_source_index.csv |
| HÖR Berlin YouTube | Available | 50 source-index rows in berghain_2024_2026_top50_artist_set_source_index.csv |

## Rekordbox

| Area | Current State | Evidence |
| --- | --- | --- |
| Current Folder Logic | Available in docs | `docs/agent_prompts.md`, `docs/future_flow.md` |
| Flow | Defined as warm, groovy, patient, transition-friendly material | `docs/agent_prompts.md` |
| Push | Defined as percussive, drum-forward, floor-nudging material | `docs/agent_prompts.md` |
| Moment | Defined through moment_deep / moment_driving / moment_vocal | `docs/agent_prompts.md` |
| Layer | Not yet available. | Not yet available. |
| Atmosphere | Not yet available. | Not yet available. |
| Export capability | Not yet available. | `docs/future_flow.md` describes future script only |

## Automation Overview

| Automation | Purpose | Status | Latest execution | Output / Files |
| --- | --- | --- | --- | --- |
| Archive Agent | Collect/update event, press, artist, and source data | Defined | Not yet available. | berghain_2024_2026_events.csv; berghain_2024_2026_press_texts.csv; berghain_2024_2026_artists_raw.csv |
| Trend Agent | Append observations and labels/community/aesthetic notes | Defined | Not yet available. | berghain_2024_2026_observations.md; berghain_2024_2026_labels_communities_aesthetics.md |
| Contrarian Agent | Validate gaps, mismatches, and next archive refinements | Defined | Not yet available. | berghain_2024_2026_observations.md |
| Rekordbox Agent | Future playlist/folder export automation | Not yet available. | Not yet available. | Not yet available. |
| Top 50 Artist Rebuild | Rebuild Panorama Bar Top 50 from berghain markdown archive | Completed | 2026-06-24T21:15:58+00:00 | berghain_2024_2026_top50_panorama_bar_artists.csv; TOP50_PANORAMA_BAR_ARTISTS_REPORT.md |
| TrackID Overlap Agent | Find TrackID-supported overlaps between Top 50 artists | Completed | 2026-06-24T23:01:26+00:00 | berghain_2024_2026_top50_trackid_overlaps.csv; TRACKID_OVERLAP_REPORT.md |
| Top 50 Set Archive Builder | Archive visible TrackID set rows and provider indexes | Completed | 2026-06-25T08:16:16+00:00 | berghain_2024_2026_top50_artist_sets_trackid.csv; berghain_2024_2026_top50_artist_set_source_index.csv |
| Normalized Track Evidence Export | Export track evidence to requested normalized schema | Completed | 2026-06-25T08:24:29+00:00 | berghain_2024_2026_top50_track_evidence_normalized.csv |

## Reports

| Type | Report | Size | Last Update | Commit |
| --- | --- | --- | --- | --- |
| Archive/Coverage Report | `TOP50_ARTIST_SET_ARCHIVE_REPORT.md` | 101 lines | 2026-06-25T08:16:16+00:00 | d378c87 |
| Archive/Coverage Report | `TOP50_PANORAMA_BAR_ARTISTS_REPORT.md` | 47 lines | 2026-06-24T21:15:58+00:00 | 573eaed |
| Track Report | `TRACK_OVERLAP_REPORT.md` | 97 lines | 2026-06-24T21:15:58+00:00 | 573eaed |
| Track Report | `TRACKID_OVERLAP_REPORT.md` | 94 lines | 2026-06-24T23:01:26+00:00 | 901d568 |

## Repository Map

```text
/workspace
├── berghain/
│   ├── 2010/
│   │   ├── events_merged.json
│   │   ├── sammelphase_2010.md
│   │   └── sammelphase_2010_full.md
│   ├── klubnacht_2024_2026.json
│   └── klubnacht_2024_2026.md
├── docs/
│   ├── agent_prompts.md
│   ├── automation_plan.md
│   ├── future_flow.md
│   ├── ORBIT_II_CORE_QUESTIONS.md
│   ├── ORBIT_II_INFORMATION_ARCHITECTURE.md
│   └── PROJECT_DASHBOARD.md
├── berghain_2024_2026_artist_frequency.csv
├── berghain_2024_2026_artists_raw.csv
├── berghain_2024_2026_events.csv
├── berghain_2024_2026_labels_communities_aesthetics.md
├── berghain_2024_2026_observations.md
├── berghain_2024_2026_press_texts.csv
├── berghain_2024_2026_top50_artist_set_source_index.csv
├── berghain_2024_2026_top50_artist_sets_trackid.csv
├── berghain_2024_2026_top50_artist_sets_trackid_part01.csv
├── berghain_2024_2026_top50_artist_sets_trackid_part02.csv
├── berghain_2024_2026_top50_artist_sets_trackid_part03.csv
├── berghain_2024_2026_top50_artist_sets_trackid_part04.csv
├── berghain_2024_2026_top50_artist_sets_trackid_part05.csv
├── berghain_2024_2026_top50_panorama_bar_artists.csv
├── berghain_2024_2026_top50_track_evidence_normalized.csv
├── berghain_2024_2026_top50_track_overlaps.csv
├── berghain_2024_2026_top50_trackid_overlaps.csv
├── berghain_2024_2026_trackid_artist_csv_manifest.csv
├── data/
│   ├── trackid_artist_csv/
│   │   └── 50 per-artist TrackID CSV files
│   └── trackid_csv_raw/
├── README.md
├── TOP50_ARTIST_SET_ARCHIVE_REPORT.md
├── TOP50_PANORAMA_BAR_ARTISTS_REPORT.md
├── TRACK_OVERLAP_REPORT.md
└── TRACKID_OVERLAP_REPORT.md
```

## Next Priorities

### High Priority

| Priority | Datasets requiring work | Reason |
| --- | --- | --- |
| Align every dataset to core questions | `docs/ORBIT_II_CORE_QUESTIONS.md`, `docs/PROJECT_DASHBOARD.md` | New datasets should answer at least one core question: digging, musical context, collection management, set preparation, research, or graph relationships. |
| Canonicalize tracks | `berghain_2024_2026_top50_track_evidence_normalized.csv`, `berghain_2024_2026_top50_track_overlaps.csv` | Missing `canonical_tracks.csv`; required to merge variants and recompute overlaps. |
| Create artist alias/disambiguation table | `berghain_2024_2026_top50_artist_sets_trackid.csv`, `TOP50_ARTIST_SET_ARCHIVE_REPORT.md` | Broad-name searches flagged for Victor, Âme, Naomi, Chloé, Loren. |
| Extract TrackID set tracklists into normalized table | `berghain_2024_2026_top50_artist_sets_trackid.csv` | Report recommends `artist_set_tracks.csv`; not yet available. |

### Medium Priority

| Priority | Datasets requiring work | Reason |
| --- | --- | --- |
| Build overlap graph from normalized evidence | `berghain_2024_2026_top50_track_evidence_normalized.csv`, `berghain_2024_2026_top50_trackid_overlaps.csv` | Graph/relationship file not yet available. |
| Add store/catalog enrichment | `berghain_2024_2026_top50_artist_set_source_index.csv`, `docs/agent_prompts.md` | Bandcamp, Hardwax, Yoyaku mentioned but no dedicated datasets exist. |

### Low Priority

| Priority | Datasets requiring work | Reason |
| --- | --- | --- |
| Implement Rekordbox export | `docs/future_flow.md`, `docs/agent_prompts.md` | Folder logic exists; export files/scripts not yet available. |

## Validation Notes

- All row counts are generated from current CSV/JSON/Markdown files in the repository.
- Missing items are shown as `Not yet available.` when no corresponding repository file exists.
- Broad-name TrackID search noise is not treated as canonical data; see `TOP50_ARTIST_SET_ARCHIVE_REPORT.md`.
- Dashboard generated from repository state at scan time; this file itself is the dashboard output.
