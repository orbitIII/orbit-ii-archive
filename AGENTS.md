# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is

`orbit-ii-archive` (ORBIT) is a personal music/art archive + data-analysis toolkit. It is
**pure Python 3 (standard library only)** plus a small **static browser app**. There is no
`package.json`, no `requirements.txt`/`pyproject.toml`, and no test suite or linter config.
The update script therefore installs nothing — a stock Python 3 is all that is required.

### Main application — ORBIT Lab (web app)

- Start it with `python3 archiv/identitaet_layer/scripts/serve_orbit_lab.py`
  (override the port with `ORBIT_LAB_PORT=<port>`; default is `8765`).
- Open `http://127.0.0.1:8765/app/orbit-lab/`.
- Non-obvious: the server's document root is `archiv/identitaet_layer/` (the parent of the
  script dir), NOT the repo root. The app's `js/data-loader.js` fetches the `orbit_*.json`
  files (e.g. `orbit_fundament.json`, `orbit_kultur_dna.json`) from that directory, so they
  must stay alongside the `app/` folder for the UI to populate.

### CLI analysis / curation scripts (`scripts/`)

- Most scripts (e.g. `analyze_tracklists.py`, `analyze_orbit_playlists.py`,
  `score_remmex_releases.py`) are stdlib-only and read the CSV/JSON data committed at the repo
  root — run them directly with `python3 scripts/<name>.py`.
- Gotcha: several scripts **overwrite committed output files** (e.g. `analyze_tracklists.py`
  rewrites `TRACKID_IMPORT_ANALYSIS_REPORT.md`). Revert unintended regenerated artifacts with
  `git checkout -- <file>` before committing.
- Optional/blocked: scripts that touch Rekordbox (`rekordbox_orbit.py` and callers) require the
  third-party `pyrekordbox` package **and** a real local Rekordbox 6 database, neither of which
  ships with the repo. These are not part of the base dev environment; skip them unless that
  external data is supplied.

### Testing / lint / build

- There are no automated tests, no lint config, and no build step. "Running the app" means
  serving the ORBIT Lab app above; "running the tooling" means invoking the `scripts/*.py`
  files against the in-repo data.
