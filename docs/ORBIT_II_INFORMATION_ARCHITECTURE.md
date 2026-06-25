# ORBIT II — Informationsarchitektur

## Zweck

Dieses Dokument beschreibt die Informationsarchitektur von Orbit II auf Basis des aktuellen Repository-Zustands.

Es beantwortet:

- Welche Datenobjekte gibt es?
- Wie hängen sie zusammen?
- Welche Ansichten braucht ein DJ?
- Welche Ansichten braucht ein Digging-Workflow?
- Welche Ansichten braucht die Set-Vorbereitung?
- Welche Ansichten braucht die Forschung?

---

# 1. Zentrale Datenobjekte

| Objekt | Bedeutung | Aktuelle Dateien |
|---|---|---|
| Event | Klubnacht / Berghain-Event mit Datum, Räumen, Pressetext | `berghain_2024_2026_events.csv`, `berghain/klubnacht_2024_2026.md` |
| Room | Panorama Bar, Berghain, Säule | in `berghain_2024_2026_events.csv` enthalten |
| Artist | gebuchte Acts / DJs / Live Acts | `berghain_2024_2026_artists_raw.csv` |
| Artist Appearance | Artist X spielt bei Event Y in Raum Z | abgeleitet aus `berghain_2024_2026_events.csv` und `berghain_2024_2026_top50_panorama_bar_artists.csv` |
| Artist Frequency | Häufigkeit pro Artist | `berghain_2024_2026_artist_frequency.csv` |
| Top 50 Artist | meist gebuchte Panorama-Bar-Artists | `berghain_2024_2026_top50_panorama_bar_artists.csv` |
| Set Source | TrackID, MixesDB, RA, YouTube, SoundCloud etc. | `berghain_2024_2026_top50_artist_set_source_index.csv` |
| Artist Set | konkretes Set / Mix eines Artists | `berghain_2024_2026_top50_artist_sets_trackid.csv` |
| Track Evidence | Track wurde in Quelle / Set gefunden | `berghain_2024_2026_top50_track_evidence_normalized.csv` |
| Track Overlap | Track taucht bei mehreren Top-50-Artists auf | `berghain_2024_2026_top50_track_overlaps.csv`, `berghain_2024_2026_top50_trackid_overlaps.csv` |
| Label | Label eines Tracks / Artists / Releases | Track- und Artist-Dateien |
| Community / Aesthetic | Labels, Stores, Szenen, Begriffe | `berghain_2024_2026_labels_communities_aesthetics.md` |
| Report | Forschungs-/Validierungsstand | `*_REPORT.md` |
| Automation | Agenten / Workflows | `docs/automation_plan.md`, `docs/agent_prompts.md` |
| Rekordbox Folder Logic | Flow, Push, Moment etc. | `docs/future_flow.md`, `docs/agent_prompts.md` |

---

# 2. Beziehungen zwischen Objekten

```text
Event
├── has Room
├── has Artist Appearance
└── has Press Text

Artist
├── appears in Event
├── has Frequency
├── may be Top 50 Artist
├── has Set Sources
└── has Artist Sets

Artist Set
├── belongs to Artist
├── comes from Source Provider
└── contains Track Evidence

Track Evidence
├── links Track
├── links played_by_artist
├── links set_source
└── links source_url

Track
├── has Artist
├── has Label
├── may appear in multiple Artist Sets
└── may become Track Overlap

Track Overlap
├── aggregates Track Evidence
├── counts Top 50 Artists
└── feeds Knowledge Graph / Rekordbox Prep
```

---

# 3. Hauptansichten für Orbit II

## A. DJ View

Ziel: schnell verstehen, was musikalisch relevant ist.

### Benötigte Ansichten

| View | Zweck | Daten |
|---|---|---|
| Top Artist Radar | Welche Panorama-Bar-Artists sind zentral? | Top 50, Frequency |
| Track Overlaps | Welche Tracks tauchen bei mehreren Artists auf? | Track Overlaps |
| Artist Profile | Artist + Sets + Track Evidence | Artist, Set Sources, Track Evidence |
| Label Signals | Welche Labels wiederholen sich? | Track Evidence, Labels |
| Folder Candidates | Tracks für Flow / Push / Moment | Track Evidence + Rekordbox Logic |

### DJ-Fragen

- Welche Artists sind Panorama-Bar-Kern?
- Welche Tracks verbinden mehrere Artists?
- Welche Labels tauchen immer wieder auf?
- Welche Tracks könnten in meinen Flow-Ordner?
- Welche Tracks sind Moment- oder Push-Material?

---

## B. Digging Workflow View

Ziel: Quellen systematisch abarbeiten.

### Benötigte Ansichten

| View | Zweck | Daten |
|---|---|---|
| Source Inbox | Alle Quellen pro Artist | Source Index |
| TrackID Queue | TrackID-Sets pro Top-50-Artist | TrackID Set Archive |
| Missing Sources | Artists ohne verwertbare Quellen | TrackID No-result rows |
| Provider Coverage | TrackID / RA / MixesDB / YouTube / SoundCloud Status | Source Index |
| Digging Priority | Welche Artists zuerst weiter diggen? | Top 50 + fehlende Set Tracks |

### Digging-Fragen

- Für welchen Artist gibt es viele TrackID-Sets?
- Wo fehlen Quellen?
- Welche TrackID-Sets müssen als nächstes extrahiert werden?
- Welche Provider fehlen noch?
- Welche Artists haben nur breite / verrauschte Suchergebnisse?

---

## C. Set Preparation View

Ziel: aus Research spielbare DJ-Struktur bauen.

### Benötigte Ansichten

| View | Zweck | Daten |
|---|---|---|
| Flow Pool | Warm, groovy, transition-friendly | Rekordbox Logic + Track Evidence |
| Push Pool | Percussive / floor-nudging | Rekordbox Logic + Track Evidence |
| Moment Pool | Deep / Driving / Vocal Momente | Rekordbox Logic |
| Overlap Anchors | Tracks mit mehreren Artist-Bezügen | Track Overlaps |
| Set Skeleton | Reihenfolge / Energie / Layer | künftig aus Track Tags |

### Set-Fragen

- Welche Tracks sind verlässlich, weil mehrere Artists sie spielen?
- Welche Tracks sind eher Warm-up / Flow?
- Welche Tracks funktionieren als Push?
- Welche Tracks sind Moment-Tracks?
- Welche Artists liefern Set-DNA für bestimmte Phasen?

---

## D. Research View

Ziel: Archiv, Beweise, Quellen und Fortschritt prüfen.

### Benötigte Ansichten

| View | Zweck | Daten |
|---|---|---|
| Project Dashboard | Gesamtstatus | `docs/PROJECT_DASHBOARD.md` |
| Archive Coverage | Welche Datasets existieren? | Dashboard + CSVs |
| Evidence Matrix | Welche Behauptung hat welche Quelle? | Track Evidence |
| Reports Index | Forschungsstand / Entscheidungen | Reports |
| Knowledge Graph Progress | Welche Nodes/Edges existieren? | Dashboard |
| Missing Dataset Monitor | Was fehlt noch? | Dashboard |

### Research-Fragen

- Welche Daten sind belegt?
- Welche Daten fehlen?
- Welche Quellen wurden genutzt?
- Welche Overlaps sind echt?
- Welche Module sind abgeschlossen?
- Was ist nur teilweise vorhanden?

---

# 4. Empfohlene Navigationsstruktur

```text
ORBIT II
├── Dashboard
│   └── Project Health / Archive / Priorities
│
├── Archive
│   ├── Events
│   ├── Artists
│   ├── Top 50 Artists
│   ├── Frequencies
│   └── Press Texts
│
├── Digging
│   ├── Source Index
│   ├── TrackID Sets
│   ├── Missing Sources
│   └── Provider Coverage
│
├── Tracks
│   ├── Track Evidence
│   ├── Track Overlaps
│   ├── TrackID Overlaps
│   └── Canonical Tracks
│
├── Set Prep
│   ├── Flow
│   ├── Push
│   ├── Moment Deep
│   ├── Moment Driving
│   └── Moment Vocal
│
├── Research
│   ├── Reports
│   ├── Observations
│   ├── Labels / Communities
│   └── Knowledge Graph Progress
│
└── Automation
    ├── Archive Agent
    ├── Trend Agent
    ├── Contrarian Agent
    └── Rekordbox Agent
```

---

# 5. Fehlende Schlüsselobjekte

Diese fehlen noch als echte Datasets:

| Fehlendes Objekt | Datei | Warum wichtig |
|---|---|---|
| Canonical Track | `canonical_tracks.csv` | gleiche Tracks / Schreibweisen zusammenführen |
| Artist Alias | `artist_aliases.csv` | Victor, Âme, Naomi, Chloé etc. disambiguieren |
| Artist Set Tracks | `artist_set_tracks.csv` | Tracklisten aus Sets normalisieren |
| Knowledge Graph | `knowledge_graph.*` | Events, Artists, Tracks, Labels verbinden |
| Rekordbox Export | `rekordbox_exports/*.csv` | Flow / Push / Moment exportieren |
| Store Catalog | `stores.csv` | Hardwax, Yoyaku, Bandcamp etc. strukturiert einbinden |

---

# 6. Nächste Architektur-Priorität

Als nächstes sollte Orbit II diese Reihenfolge bekommen:

1. `artist_aliases.csv`
2. `canonical_tracks.csv`
3. `artist_set_tracks.csv`
4. Knowledge Graph
5. Rekordbox Export Views

Danach wird aus dem Archiv ein nutzbares DJ-Research-System:

```text
Archive Data
→ Set Sources
→ Track Evidence
→ Canonical Tracks
→ Overlap Graph
→ Digging Queue
→ Rekordbox / Set Prep Views
```

---

# 7. Kurzfassung zum Weiterleiten

Orbit II ist ein Panorama-Bar-/Berghain-Research-System.

Das Projekt sammelt:

- Events
- Artists
- Top-50-Panorama-Bar-Artists
- Set-Quellen
- TrackID-Sets
- Track-Evidence
- Overlaps
- Labels / Communities / Aesthetics
- Reports
- Automations

Die Architektur trennt vier Hauptbedürfnisse:

1. **DJ View** — Was ist musikalisch relevant?
2. **Digging View** — Wo finde ich Quellen und Sets?
3. **Set Preparation View** — Welche Tracks helfen beim Bauen eines Sets?
4. **Research View** — Welche Daten sind belegt, welche fehlen?

Die nächsten fehlenden Kernobjekte sind:

- `artist_aliases.csv`
- `canonical_tracks.csv`
- `artist_set_tracks.csv`
- `knowledge_graph.*`
- `rekordbox_exports/*.csv`

Diese Objekte machen aus dem aktuellen Archiv ein vollständiges, filterbares DJ-Research- und Set-Vorbereitungs-System.
