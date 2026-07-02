import { loadDiggingData, resolveTrackHref } from "./data-loader.js";

const VIEWS = [
  { id: "overview", label: "Überblick" },
  { id: "playlists", label: "Playlists" },
  { id: "curate", label: "Kuratieren" },
  { id: "compare", label: "Vergleiche" },
  { id: "top50", label: "Top 50" },
  { id: "berghain", label: "Berghain" },
  { id: "remmex", label: "Remmex" },
  { id: "scripts", label: "Scripts" },
];

let state = null;
let route = { view: "overview", slug: null, compareSlug: null };
let trackFilter = "all";
let trackSearch = "";
let remmexProfile = "orbit_core";

const app = document.getElementById("app");
const nav = document.getElementById("main-nav");
const statusEl = document.getElementById("status-bar");

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s ?? "";
  return d.innerHTML;
}

function fmtNum(n, digits = 1) {
  if (n == null || Number.isNaN(n)) return "—";
  return Number(n).toFixed(digits);
}

function fmtTime(d) {
  return d.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

function renderTrackIdLink(trackId, artist, title) {
  const id = (trackId || "").trim();
  const href = resolveTrackHref(id, artist, title, state?.trackIdLookup);
  if (!href) {
    return id ? `<span class="track-id mono">${esc(id)}</span>` : `<span class="muted">—</span>`;
  }
  let label = id;
  if (id.startsWith("http")) {
    const slug = id.split("/").filter(Boolean).pop() || "TrackID";
    label = slug.length > 28 ? `${slug.slice(0, 26)}…` : slug;
  } else if (!id) {
    label = "TrackID";
  }
  const titleAttr = id.startsWith("http") ? id : id ? `Rekordbox ${id}` : "TrackID.net";
  return `<a class="track-id-link mono" href="${esc(href)}" target="_blank" rel="noopener noreferrer" title="${esc(titleAttr)}">${esc(label)}</a>`;
}

function renderTrackIdCell(trackId, artist, title) {
  return `<td class="track-id-col">${renderTrackIdLink(trackId, artist, title)}</td>`;
}

function parseRoute() {
  const hash = location.hash.replace(/^#/, "") || "overview";
  const parts = hash.split("/");
  if (parts[0] === "playlist" && parts[1]) {
    route = { view: "playlist", slug: parts[1], compareSlug: null };
  } else if (parts[0] === "compare" && parts[1]) {
    route = { view: "compare", slug: null, compareSlug: parts[1] };
  } else {
    route = { view: parts[0], slug: null, compareSlug: null };
  }
}

function navTo(view, arg = null) {
  if (view === "playlist" && arg) location.hash = `playlist/${arg}`;
  else if (view === "compare" && arg) location.hash = `compare/${arg}`;
  else location.hash = view;
}

function renderNav() {
  const active = route.view === "playlist" ? "playlists" : route.view;
  nav.innerHTML = VIEWS.map(
    (v) =>
      `<button type="button" data-view="${v.id}" class="${v.id === active ? "active" : ""}">${esc(v.label)}</button>`
  ).join("");
  nav.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => navTo(btn.dataset.view));
  });
}

function updateStatus() {
  if (!statusEl || !state) return;
  const missing = state.totals.missing.length;
  statusEl.innerHTML = `
    <span class="status-dot ok"></span>
    ${state.totals.analyzed} Playlists · ${state.totals.tracks} Tracks · ${state.totals.outliers} Outlier
    ${missing ? `<span class="status-warn"> · ${missing} ohne Scores</span>` : ""}
    <span class="status-time"> · ${fmtTime(state.loadedAt)}</span>
  `;
}

function renderView() {
  if (!state) return;
  parseRoute();

  let html;
  if (route.view === "playlist" && route.slug) {
    html = renderPlaylistDetail(route.slug);
  } else if (route.view === "compare" && route.compareSlug) {
    html = renderCompareDetail(route.compareSlug);
  } else {
    html = {
      overview: renderOverview,
      playlists: renderPlaylists,
      curate: renderCurate,
      compare: renderCompare,
      top50: renderTop50,
      berghain: renderBerghain,
      remmex: renderRemmex,
      scripts: renderScripts,
    }[route.view]?.() ?? renderOverview();
  }

  app.innerHTML = `<section class="view active">${html}</section>`;
  bindViewEvents();
  renderNav();
  updateStatus();
}

function renderOverview() {
  const { totals, berghain, curationQueue } = state;
  const withData = state.playlistList.filter((p) => p.artifact?.stats?.hasScores);

  return `
    <h1>Digging Platform</h1>
    <p class="lead">Test-UI für Rekordbox-Analyse, Outlier-Kuratierung und Sammlung — ohne Identitäts-Schicht.</p>

    <div class="stat-row">
      <article class="stat"><span class="stat-value">${withData.length}</span><span class="stat-label">Playlists analysiert</span></article>
      <article class="stat"><span class="stat-value">${totals.tracks}</span><span class="stat-label">Tracks im Profil</span></article>
      <article class="stat"><span class="stat-value warn">${totals.outliers}</span><span class="stat-label">Outlier gesamt</span></article>
      <article class="stat"><span class="stat-value">${berghain.events.length}</span><span class="stat-label">Berghain-Events</span></article>
    </div>

    ${
      curationQueue.length
        ? `<h2>Nächste Kuratierung</h2>
    <div class="action-list">
      ${curationQueue
        .slice(0, 5)
        .map(
          (p) => `
        <button type="button" class="action-item" data-slug="${esc(p.slug)}">
          <span class="action-title">${esc(p.label)}</span>
          <span class="action-meta warn">${p.artifact.stats.outliers} Outlier · ${fmtNum(p.artifact.stats.outlierPct, 0)}%</span>
        </button>`
        )
        .join("")}
    </div>`
        : `<p class="ok-box">Keine Outlier in analysierten Playlists.</p>`
    }

    ${
      totals.missing.length
        ? `<h2>Fehlende Analyse</h2>
    <p class="muted">Diese Playlists sind in <code>orbit_playlists.json</code>, haben aber noch keine Scores:</p>
    <ul class="chip-list">${totals.missing.map((s) => `<li><code>${esc(s)}</code></li>`).join("")}</ul>`
        : ""
    }

    <h2>ORBIT II · SYSTEM</h2>
    <div class="tree">${renderTree()}</div>

    <h2>Pipeline</h2>
    <ol class="pipeline">
      <li><strong>Sammeln</strong> — Berghain, Tracklists, Remmex</li>
      <li><strong>Messen</strong> — BPM, Genre, Key, Label, Artist</li>
      <li><strong>Sortieren</strong> — Outlier → AUSGEsortiert</li>
      <li><strong>Dokumentieren</strong> — Reports in Git</li>
    </ol>
  `;
}

function renderTree() {
  return Object.entries(state.groups)
    .map(
      ([parent, items]) => `
    <div class="tree-group">
      <h3>${esc(parent)}</h3>
      <ul>
        ${items
          .map((p) => {
            const s = p.artifact?.stats;
            const badge = s?.hasScores
              ? `<span class="badge ${s.outliers ? "warn" : "ok"}">${s.trackCount} · ${s.outliers} out</span>`
              : `<span class="badge muted">—</span>`;
            return `<li>
              <button type="button" class="link-btn" data-slug="${esc(p.slug)}">${esc(p.label)}</button>
              ${badge}
            </li>`;
          })
          .join("")}
      </ul>
    </div>`
    )
    .join("");
}

function renderPlaylists() {
  return `
    <h1>Playlists</h1>
    <p class="muted">Profil, Scoring-Regeln, Track-Tabelle, Analyse-Report.</p>
    ${Object.entries(state.groups)
      .map(
        ([parent, items]) => `
      <h2>${esc(parent)}</h2>
      <div class="card-grid">${items.map((p) => renderPlaylistCard(p)).join("")}</div>`
      )
      .join("")}
  `;
}

function renderPlaylistCard(p) {
  const s = p.artifact?.stats;
  const prof = p.artifact?.profile?.profile;
  const bpm = prof?.bpm;
  return `
    <article class="card clickable" data-slug="${esc(p.slug)}">
      <div class="card-head">
        <h3>${esc(p.label)}</h3>
        <span class="tag">${esc(p.source)} · ${esc(p.role)}</span>
      </div>
      <p class="card-desc">${esc(p.description)}</p>
      ${
        s?.hasScores
          ? `<dl class="mini-stats">
          <div><dt>Tracks</dt><dd>${s.trackCount}</dd></div>
          <div><dt>Outlier</dt><dd class="${s.outliers ? "warn" : "ok"}">${s.outliers} (${fmtNum(s.outlierPct, 0)}%)</dd></div>
          <div><dt>Ø Conf.</dt><dd>${fmtNum(s.avgConfidence, 0)}%</dd></div>
          ${bpm ? `<div><dt>BPM</dt><dd>${fmtNum(bpm.p10, 0)}–${fmtNum(bpm.p90, 0)}</dd></div>` : ""}
        </dl>`
          : `<p class="muted"><code>analyze_orbit_playlists.py --slug ${esc(p.slug)}</code></p>`
      }
    </article>`;
}

function renderCurate() {
  const queue = state.curationQueue;
  return `
    <h1>Kuratieren</h1>
    <p class="lead">Playlists nach Outlier-Anteil — höchste zuerst. Ziel: messbare Regeln, kein Vibe-Scoring.</p>

    ${
      queue.length
        ? `<div class="table-wrap">
      <table class="track-table">
        <thead><tr><th>Playlist</th><th>Parent</th><th>Tracks</th><th>Outlier</th><th>Anteil</th><th>Ø Conf.</th><th></th></tr></thead>
        <tbody>
          ${queue
            .map(
              (p) => `
            <tr>
              <td>${esc(p.label)}</td>
              <td class="muted">${esc(p.parent)}</td>
              <td class="mono">${p.artifact.stats.trackCount}</td>
              <td class="mono warn">${p.artifact.stats.outliers}</td>
              <td class="mono">${fmtNum(p.artifact.stats.outlierPct, 1)}%</td>
              <td class="mono">${fmtNum(p.artifact.stats.avgConfidence, 0)}%</td>
              <td><button type="button" class="link-btn" data-slug="${esc(p.slug)}">öffnen</button></td>
            </tr>`
            )
            .join("")}
        </tbody>
      </table>
    </div>`
        : `<p class="ok-box">Alle analysierten Playlists sind outlier-frei.</p>`
    }

    <h2>Workflow</h2>
    <ol class="pipeline">
      <li>Outlier in Detail-Ansicht prüfen (Gründe lesen)</li>
      <li><code>curate_orbit_flow.py</code> oder <code>curate_to_ausgesortiert.py --slug …</code></li>
      <li>Re-Analyse: <code>analyze_orbit_playlists.py --slug …</code></li>
      <li><code>sort_ausgesortiert.py</code> wenn AUSGEsortiert voll</li>
    </ol>
  `;
}

function renderCompare() {
  return `
    <h1>Vergleiche</h1>
    <p class="muted">Playlist-Paare aus <code>orbit_playlists.json → comparisons</code></p>
    <div class="card-grid">
      ${state.comparisons
        .map(
          (c) => `
        <article class="card clickable" data-compare="${esc(c.slug)}">
          <h3>${esc(c.label)}</h3>
          <p class="card-desc">${esc(c.a)} ↔ ${esc(c.b)}</p>
          <span class="tag">${c.reportMd ? "Report geladen" : "Kein Report"}</span>
        </article>`
        )
        .join("")}
    </div>
  `;
}

function renderCompareDetail(slug) {
  const c = state.comparisons.find((x) => x.slug === slug);
  if (!c) return `<p>Vergleich nicht gefunden.</p>`;
  const labelA = state.playlistList.find((p) => p.slug === c.a)?.label ?? c.a;
  const labelB = state.playlistList.find((p) => p.slug === c.b)?.label ?? c.b;

  return `
    <nav class="breadcrumb"><button type="button" class="link-btn" data-view="compare">← Vergleiche</button></nav>
    <h1>${esc(c.label)}</h1>
    <p class="muted">${esc(labelA)} vs ${esc(labelB)}</p>
    <div class="split-actions">
      <button type="button" class="link-btn" data-slug="${esc(c.a)}">${esc(labelA)}</button>
      <button type="button" class="link-btn" data-slug="${esc(c.b)}">${esc(labelB)}</button>
    </div>
    ${
      c.reportMd
        ? `<pre class="report-md">${esc(c.reportMd)}</pre>`
        : `<p class="warn-box">Report <code>${esc(c.report)}</code> nicht gefunden.</p>`
    }
  `;
}

function renderPlaylistDetail(slug) {
  const meta = state.playlistList.find((p) => p.slug === slug);
  const art = state.bySlug[slug];
  if (!meta) return `<p>Playlist nicht gefunden.</p>`;

  const prof = art?.profile?.profile;
  const scores = art?.scores?.rows ?? [];
  const q = trackSearch.trim().toLowerCase();
  let filtered = scores;
  if (trackFilter === "outliers") filtered = filtered.filter((r) => r.is_outlier === "yes");
  if (trackFilter === "inliers") filtered = filtered.filter((r) => r.is_outlier !== "yes");
  if (q) {
    filtered = filtered.filter(
      (r) =>
        r.name?.toLowerCase().includes(q) ||
        r.artist?.toLowerCase().includes(q) ||
        r.genre?.toLowerCase().includes(q) ||
        r.label?.toLowerCase().includes(q) ||
        r.track_id?.includes(q)
    );
  }
  const displayLimit = q || trackFilter !== "all" ? 200 : 50;

  return `
    <nav class="breadcrumb"><button type="button" class="link-btn" data-view="playlists">← Playlists</button></nav>
    <h1>${esc(meta.label)}</h1>
    <p class="muted">${esc(meta.parent)} · ${esc(meta.source)} · ${esc(meta.description)}</p>

    ${
      prof
        ? `
    <div class="stat-row compact">
      <article class="stat"><span class="stat-value">${prof.track_count}</span><span class="stat-label">Tracks</span></article>
      <article class="stat"><span class="stat-value">${fmtNum(prof.bpm?.mean)}</span><span class="stat-label">BPM Ø</span></article>
      <article class="stat"><span class="stat-value">${fmtNum(prof.bpm?.p10, 0)}–${fmtNum(prof.bpm?.p90, 0)}</span><span class="stat-label">p10–p90</span></article>
      <article class="stat"><span class="stat-value warn">${art.stats.outliers}</span><span class="stat-label">Outlier</span></article>
    </div>
    ${renderBpmBar(prof.bpm)}
    <div class="split">
      <div><h2>Genres</h2>${renderRankList(prof.genres_top15?.slice(0, 8))}</div>
      <div><h2>Keys</h2>${renderRankList(prof.keys_top10?.slice(0, 8))}</div>
      <div><h2>Labels</h2>${renderRankList(prof.labels_top20?.slice(0, 8))}</div>
    </div>
    ${renderRules(art.stats.rules)}`
        : `<p class="warn-box">Kein Profil — <code>analyze_orbit_playlists.py --slug ${esc(slug)}</code></p>`
    }

    <h2>Tracks</h2>
    <div class="filter-row">
      <input type="search" class="search-input" id="track-search" placeholder="Suche Track, Artist, Genre…" value="${esc(trackSearch)}" />
      <button type="button" class="filter-btn ${trackFilter === "all" ? "active" : ""}" data-filter="all">Alle (${scores.length})</button>
      <button type="button" class="filter-btn ${trackFilter === "outliers" ? "active" : ""}" data-filter="outliers">Outlier (${art?.stats?.outliers ?? 0})</button>
      <button type="button" class="filter-btn ${trackFilter === "inliers" ? "active" : ""}" data-filter="inliers">Im Profil</button>
    </div>

    ${
      filtered.length
        ? `<div class="table-wrap"><table class="track-table">
        <thead><tr><th>Track</th><th>Artist</th><th>Track ID</th><th>BPM</th><th>Genre</th><th>Conf.</th><th>Gründe</th></tr></thead>
        <tbody>
          ${filtered
            .slice(0, displayLimit)
            .map(
              (r) => `
            <tr class="${r.is_outlier === "yes" ? "outlier" : ""}">
              <td class="track-name">${esc(r.name?.trim())}</td>
              <td>${esc(r.artist)}</td>
              ${renderTrackIdCell(r.track_id, r.artist, r.name)}
              <td class="mono">${esc(r.bpm)}</td>
              <td>${esc(r.genre)}</td>
              <td class="mono">${esc(r.confidence_score)}</td>
              <td class="reasons muted">${esc(r.outlier_reasons || "—")}</td>
            </tr>`
            )
            .join("")}
        </tbody>
      </table>
      ${filtered.length > displayLimit ? `<p class="muted">${filtered.length - displayLimit} weitere — Suche nutzen oder Filter ändern</p>` : ""}
    </div>`
        : `<p class="muted">Keine Treffer.</p>`
    }

    ${art?.reportMd ? `<h2>Report</h2><details class="report-details"><summary>Analyse-Report</summary><pre class="report-md">${esc(art.reportMd.slice(0, 12000))}</pre></details>` : ""}
  `;
}

function renderRules(rules) {
  if (!rules?.length) return "";
  return `
    <h2>Scoring-Regeln</h2>
    <div class="rules-grid">
      ${rules
        .map(
          (r) => `
        <article class="rule-card">
          <span class="rule-weight mono">${Math.round((r.weight || 0) * 100)}%</span>
          <strong>${esc(r.id)}</strong>
          <p class="muted">${esc(r.description)}</p>
        </article>`
        )
        .join("")}
    </div>`;
}

function renderBpmBar(bpm) {
  if (!bpm) return "";
  const min = bpm.min;
  const max = bpm.max;
  const span = max - min || 1;
  const pct = (v) => `${((v - min) / span) * 100}%`;
  return `
    <div class="bpm-bar">
      <div class="bpm-track">
        <span class="bpm-mark" style="left:${pct(bpm.p10)}" title="p10"></span>
        <span class="bpm-mark median" style="left:${pct(bpm.median)}" title="Median"></span>
        <span class="bpm-mark" style="left:${pct(bpm.p90)}" title="p90"></span>
        <span class="bpm-range" style="left:${pct(bpm.p10)};width:calc(${pct(bpm.p90)} - ${pct(bpm.p10)})"></span>
      </div>
      <div class="bpm-labels mono">
        <span>${fmtNum(min, 0)}</span>
        <span>p10 ${fmtNum(bpm.p10, 0)} · med ${fmtNum(bpm.median, 0)} · p90 ${fmtNum(bpm.p90, 0)}</span>
        <span>${fmtNum(max, 0)}</span>
      </div>
    </div>`;
}

function renderRankList(items) {
  if (!items?.length) return `<p class="muted">—</p>`;
  const max = items[0][1];
  return `<ul class="rank-list">${items
    .map(
      ([name, count]) => `
    <li><span class="rank-name">${esc(name)}</span><span class="rank-bar"><span style="width:${(count / max) * 100}%"></span></span><span class="rank-count mono">${count}</span></li>`
    )
    .join("")}</ul>`;
}

function renderTop50() {
  const { top50, overlaps, tracklists } = state.berghain;

  return `
    <h1>Top 50 · Panorama Bar</h1>
    <p class="lead">50 meistgespielte Panorama-Bar-Artists · Track-Overlaps · Tracklist-Sample mit TrackID-Links.</p>

    <div class="stat-row compact">
      <article class="stat"><span class="stat-value">${top50.length}</span><span class="stat-label">Artists</span></article>
      <article class="stat"><span class="stat-value">${overlaps.length}</span><span class="stat-label">Overlaps</span></article>
      <article class="stat"><span class="stat-value">${tracklists.length}</span><span class="stat-label">Tracks (Sample)</span></article>
    </div>

    <h2>Panorama Bar · Top 50 Artists</h2>
    ${
      top50.length
        ? `<div class="table-wrap"><table class="track-table">
        <thead><tr><th>#</th><th>Artist</th><th>Appearances</th><th>Room</th></tr></thead>
        <tbody>${top50
          .map(
            (a) => `
          <tr>
            <td class="mono">${esc(a.Rank)}</td>
            <td>${esc(a.Artist)}</td>
            <td class="mono">${esc(a.Appearances)}</td>
            <td>${esc(a.PrimaryRoom)}</td>
          </tr>`
          )
          .join("")}</tbody>
      </table></div>`
        : `<p class="warn-box">Keine Top-50-Daten — <code>berghain_2024_2026_top50_panorama_bar_artists.csv</code></p>`
    }

    <h2>Track-Overlaps (Top-50-Kontext)</h2>
    ${
      overlaps.length
        ? `<div class="table-wrap"><table class="track-table">
        <thead><tr><th>Track</th><th>Artist</th><th>Track ID</th><th>Label</th><th># DJs</th><th>Played by</th></tr></thead>
        <tbody>${overlaps
          .map((o) => {
            const firstUrl = (o.source_urls || "").split(";")[0]?.trim();
            const trackHref = firstUrl || resolveTrackHref("", o.track_artist, o.track_title, state.trackIdLookup);
            return `
          <tr>
            <td>${trackHref ? `<a class="track-id-link" href="${esc(trackHref)}" target="_blank" rel="noopener">${esc(o.track_title)}</a>` : esc(o.track_title)}</td>
            <td>${esc(o.track_artist)}</td>
            ${renderTrackIdCell("", o.track_artist, o.track_title)}
            <td class="muted">${esc(o.label)}</td>
            <td class="mono warn">${esc(o.top50_artist_count)}</td>
            <td class="muted">${esc(o.played_by_artists)}</td>
          </tr>`;
          })
          .join("")}</tbody>
      </table></div>`
        : `<p class="muted">Noch keine Overlaps aggregiert.</p>`
    }

    <h2>Tracklist-Sample (50) · TrackID-Links</h2>
    ${
      tracklists.length
        ? `<div class="table-wrap"><table class="track-table">
        <thead><tr><th>Datum</th><th>DJ</th><th>Track</th><th>Artist</th><th>Track ID</th><th>Label</th></tr></thead>
        <tbody>${tracklists
          .map(
            (t) => `
          <tr>
            <td class="mono">${esc(t.Date)}</td>
            <td>${esc(t.Artist)}</td>
            <td>${esc(t.TrackTitle)}</td>
            <td>${esc(t.TrackArtist)}</td>
            ${renderTrackIdCell(t.TrackID, t.TrackArtist, t.TrackTitle)}
            <td class="muted">${esc(t.Label)}</td>
          </tr>`
          )
          .join("")}</tbody>
      </table></div>`
        : ""
    }
  `;
}

function renderBerghain() {
  const { artists, events, observations } = state.berghain;
  const topArtists = [...artists].sort(
    (a, b) => parseInt(b.Appearances || 0, 10) - parseInt(a.Appearances || 0, 10)
  );

  return `
    <h1>Berghain</h1>
    <p class="lead">Sammlung 2024–2026 — Events, Artists, Observations.</p>
    <div class="stat-row compact">
      <article class="stat"><span class="stat-value">${events.length}</span><span class="stat-label">Events</span></article>
      <article class="stat"><span class="stat-value">${artists.length}</span><span class="stat-label">Artists</span></article>
    </div>
    <h2>Top Artists</h2>
    ${
      topArtists.length
        ? `<div class="table-wrap"><table class="track-table">
        <thead><tr><th>Artist</th><th>#</th><th>Rooms</th><th>Notes</th></tr></thead>
        <tbody>${topArtists
          .slice(0, 40)
          .map(
            (a) => `<tr><td>${esc(a.Artist)}</td><td class="mono">${esc(a.Appearances)}</td><td>${esc(a.PrimaryRooms)}</td><td class="muted">${esc(a.Notes)}</td></tr>`
          )
          .join("")}</tbody>
      </table></div>`
        : `<p class="muted">Keine Daten — Archive Agent starten.</p>`
    }
    ${observations ? `<h2>Observations</h2><pre class="report-md compact">${esc(observations.slice(0, 5000))}</pre>` : ""}
  `;
}

function renderRemmex() {
  const set = state.remmex.find((r) => r.profile === remmexProfile) ?? state.remmex[0];
  return `
    <h1>Remmex Pre-Score</h1>
    <p class="muted">Genre/Artist/Label gegen ORBIT-Profil — BPM fehlt in List-View.</p>
    <div class="filter-row">
      ${state.remmex
        .map(
          (r) =>
            `<button type="button" class="filter-btn ${r.profile === remmexProfile ? "active" : ""}" data-remmex="${esc(r.profile)}">${esc(r.profile)} (${r.total})</button>`
        )
        .join("")}
    </div>
    ${
      set?.top?.length
        ? `<div class="table-wrap"><table class="track-table">
        <thead><tr><th>Artist</th><th>Track ID</th><th>Title</th><th>Genre</th><th>Conf.</th><th>Match</th></tr></thead>
        <tbody>${set.top
          .map(
            (r) => `
          <tr>
            <td>${esc(r.artist)}</td>
            ${renderTrackIdCell(r.display_id, r.artist, r.title)}
            <td>${esc(r.title)}</td>
            <td>${esc(r.genre)}</td>
            <td class="mono">${esc(r.confidence_score)}</td>
            <td>${esc(r.is_match || "—")}</td>
          </tr>`
          )
          .join("")}</tbody>
      </table></div>
      <p class="muted">Top 50 mit Confidence ≥ 50 · ${set.date} · ID-Link = Remmex/TrackID-Suche</p>`
        : `<p class="warn-box">Keine Remmex-Scores — <code>score_remmex_releases.py</code></p>`
    }
  `;
}

function renderScripts() {
  const cmds = [
    { label: "Server (diese App)", cmd: "python3 scripts/serve_orbit_digging.py" },
    { label: "ORBIT CORE", cmd: "python3 scripts/analyze_orbit_playlists.py --slug orbit_core" },
    { label: "Alle Playlists", cmd: "python3 scripts/analyze_orbit_playlists.py --all" },
    { label: "FLOW kuratieren", cmd: "python3 scripts/curate_orbit_flow.py" },
    { label: "AUSGEsortiert", cmd: "python3 scripts/sort_ausgesortiert.py" },
  ];

  return `
    <h1>Scripts</h1>
    <p class="muted">Rekordbox schließen vor Writes. Docs: <code>docs/rekordbox_orbit.md</code></p>
    <div class="cmd-list">
      ${cmds
        .map(
          (c) => `
        <div class="cmd-item">
          <span class="cmd-label">${esc(c.label)}</span>
          <code class="cmd-code" data-copy="${esc(c.cmd)}">${esc(c.cmd)}</code>
        </div>`
        )
        .join("")}
    </div>
    <h2>Alle Scripts</h2>
    <ul class="script-list">${state.scripts.map((s) => `<li><code>${esc(s)}</code></li>`).join("")}</ul>
  `;
}

function bindViewEvents() {
  app.querySelectorAll("[data-slug]").forEach((el) => {
    el.addEventListener("click", () => {
      trackFilter = "all";
      trackSearch = "";
      navTo("playlist", el.dataset.slug);
    });
  });
  app.querySelectorAll("[data-compare]").forEach((el) => {
    el.addEventListener("click", () => navTo("compare", el.dataset.compare));
  });
  app.querySelectorAll("[data-view]").forEach((el) => {
    el.addEventListener("click", () => navTo(el.dataset.view));
  });
  app.querySelectorAll(".filter-btn[data-filter]").forEach((btn) => {
    btn.addEventListener("click", () => {
      trackFilter = btn.dataset.filter;
      renderView();
    });
  });
  app.querySelectorAll(".filter-btn[data-remmex]").forEach((btn) => {
    btn.addEventListener("click", () => {
      remmexProfile = btn.dataset.remmex;
      renderView();
    });
  });
  const search = app.querySelector("#track-search");
  if (search) {
    search.addEventListener("input", (e) => {
      trackSearch = e.target.value;
      renderView();
      const next = app.querySelector("#track-search");
      if (next) {
        next.focus();
        next.setSelectionRange(next.value.length, next.value.length);
      }
    });
  }
  app.querySelectorAll("[data-copy]").forEach((el) => {
    el.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(el.dataset.copy);
        el.classList.add("copied");
        setTimeout(() => el.classList.remove("copied"), 1200);
      } catch {
        /* ignore */
      }
    });
  });
}

async function reload() {
  app.innerHTML = `<section class="view active"><p class="loading">Lade …</p></section>`;
  state = await loadDiggingData();
  renderView();
}

async function init() {
  document.getElementById("btn-reload")?.addEventListener("click", reload);
  try {
    state = await loadDiggingData();
    window.addEventListener("hashchange", renderView);
    parseRoute();
    renderView();
  } catch (err) {
    app.innerHTML = `<section class="view active">
      <p class="error">${esc(err.message)}</p>
      <pre class="report-md">python3 scripts/serve_orbit_digging.py
→ http://127.0.0.1:8766/app/orbit-digging/</pre>
    </section>`;
  }
}

init();
