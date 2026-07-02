const ROOT = "/";

export async function fetchJson(path) {
  const res = await fetch(`${ROOT}${path.replace(/^\//, "")}`);
  if (!res.ok) return null;
  return res.json();
}

export async function fetchText(path) {
  const res = await fetch(`${ROOT}${path.replace(/^\//, "")}`);
  if (!res.ok) return null;
  return res.text();
}

/** Minimal CSV parser with quoted fields. */
export function parseCsv(text) {
  if (!text?.trim()) return { headers: [], rows: [] };
  const lines = text.trim().split(/\r?\n/);
  const parseLine = (line) => {
    const out = [];
    let cur = "";
    let q = false;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (c === '"') {
        if (q && line[i + 1] === '"') {
          cur += '"';
          i++;
        } else q = !q;
      } else if (c === "," && !q) {
        out.push(cur);
        cur = "";
      } else cur += c;
    }
    out.push(cur);
    return out;
  };
  const headers = parseLine(lines[0]);
  const rows = lines.slice(1).filter(Boolean).map((line) => {
    const cells = parseLine(line);
    return Object.fromEntries(headers.map((h, i) => [h, cells[i] ?? ""]));
  });
  return { headers, rows };
}

const REPORT_MAP = {
  orbit_core: "ORBIT_CORE_ANALYSIS_REPORT.md",
  orbit_flow: "ORBIT_FLOW_ANALYSIS_REPORT.md",
  orbit_archiv: "ORBIT_ARCHIV_ANALYSIS_REPORT.md",
  orbit_moment_deep: "ORBIT_MOMENT_DEEP_ANALYSIS_REPORT.md",
  driving_flow: "DRIVING_FLOW_ANALYSIS_REPORT.md",
  system_moment_deep: "SYSTEM_MOMENT_DEEP_ANALYSIS_REPORT.md",
  system_moment_driving: "SYSTEM_MOMENT_DRIVING_ANALYSIS_REPORT.md",
  system_driving_push: "SYSTEM_DRIVING_PUSH_ANALYSIS_REPORT.md",
  system_warm: "SYSTEM_WARM_ANALYSIS_REPORT.md",
  system_warm_hypnotic: "SYSTEM_WARM_HYPNOTIC_ANALYSIS_REPORT.md",
};

const REMMEX_SCORED = [
  { profile: "orbit_core", path: "remmex/releases-2026-06-25_scored_orbit_core.csv", date: "2026-06-25" },
  { profile: "orbit_flow", path: "remmex/releases-2026-06-25_scored_orbit_flow.csv", date: "2026-06-25" },
];

async function loadPlaylistArtifact(slug) {
  const [profile, scoresText] = await Promise.all([
    fetchJson(`${slug}_profile_rules.json`),
    fetchText(`${slug}_track_scores.csv`),
  ]);
  const reportMd = REPORT_MAP[slug] ? await fetchText(REPORT_MAP[slug]) : null;
  const scores = scoresText ? parseCsv(scoresText) : { headers: [], rows: [] };
  const outliers = scores.rows.filter((r) => r.is_outlier === "yes").length;
  const trackCount = profile?.profile?.track_count ?? scores.rows.length;
  const outlierPct = trackCount > 0 ? (outliers / trackCount) * 100 : 0;
  const avgConf =
    scores.rows.length > 0
      ? scores.rows.reduce((s, r) => s + parseFloat(r.confidence_score || 0), 0) / scores.rows.length
      : null;

  return {
    slug,
    profile,
    scores,
    reportMd,
    stats: {
      trackCount,
      outliers,
      outlierPct,
      avgConfidence: avgConf,
      hasProfile: !!profile,
      hasScores: scores.rows.length > 0,
      rules: profile?.rules ?? [],
    },
  };
}

async function loadComparisons(comparisons) {
  return Promise.all(
    (comparisons ?? []).map(async (c) => ({
      ...c,
      reportMd: c.report ? await fetchText(c.report) : null,
      playlistA: c.a,
      playlistB: c.b,
    }))
  );
}

async function loadRemmex() {
  const sets = await Promise.all(
    REMMEX_SCORED.map(async (r) => {
      const text = await fetchText(r.path);
      const parsed = text ? parseCsv(text) : { rows: [] };
      const top = parsed.rows
        .map((row) => ({ ...row, confidence: parseFloat(row.confidence_score || 0) }))
        .filter((row) => row.confidence >= 50)
        .sort((a, b) => b.confidence - a.confidence)
        .slice(0, 50);
      return { ...r, total: parsed.rows.length, top };
    })
  );
  return sets;
}

/** Normalize artist+title for TrackID lookup keys. */
export function trackLookupKey(artist, title) {
  return `${(artist || "").trim().toLowerCase()}|${(title || "").trim().toLowerCase()}`;
}

/** Build map: artist|title → trackid.net URL from Berghain tracklists. */
export function buildTrackIdLookup(tracklistRows) {
  const map = new Map();
  for (const row of tracklistRows) {
    const url = row.TrackID?.trim();
    if (!url || !url.startsWith("http")) continue;
    const key = trackLookupKey(row.TrackArtist, row.TrackTitle);
    if (!map.has(key)) map.set(key, url);
    const key2 = trackLookupKey(row.TrackArtist, row.TrackTitle?.replace(/\s*\([^)]*\)\s*/g, " ").trim());
    if (!map.has(key2)) map.set(key2, url);
  }
  return map;
}

export function resolveTrackHref(trackId, artist, title, lookup) {
  const id = (trackId || "").trim();
  if (id.startsWith("http")) return id;
  const fromLookup = lookup?.get(trackLookupKey(artist, title));
  if (fromLookup) return fromLookup;
  const q = encodeURIComponent(`${artist || ""} ${title || ""}`.trim());
  if (q) return `https://trackid.net/search?query=${q}`;
  return id ? `https://trackid.net/search?query=${encodeURIComponent(id)}` : null;
}

export async function loadDiggingData() {
  if (location.protocol === "file:") {
    throw new Error("App muss über den lokalen Server laufen (file:// blockiert fetch).");
  }

  const [
    index,
    playlists,
    artistFreqText,
    eventsText,
    observationsMd,
    top50Text,
    overlapsText,
    tracklistsText,
  ] = await Promise.all([
    fetchJson("orbit_index.json"),
    fetchJson("orbit_playlists.json"),
    fetchText("berghain_2024_2026_artist_frequency.csv"),
    fetchText("berghain_2024_2026_events.csv"),
    fetchText("berghain_2024_2026_observations.md"),
    fetchText("berghain_2024_2026_top50_panorama_bar_artists.csv"),
    fetchText("berghain_2024_2026_track_overlaps.csv"),
    fetchText("berghain_2024_2026_tracklists.csv"),
  ]);

  if (!playlists) throw new Error("orbit_playlists.json nicht geladen — Server aus Repo-Root starten.");

  const slugs = playlists.playlists.map((p) => p.slug);
  const artifacts = await Promise.all(slugs.map((slug) => loadPlaylistArtifact(slug)));
  const bySlug = Object.fromEntries(artifacts.map((a) => [a.slug, a]));
  const comparisons = await loadComparisons(playlists.comparisons);
  const remmex = await loadRemmex();

  const tracklistRows = tracklistsText ? parseCsv(tracklistsText).rows : [];
  const trackIdLookup = buildTrackIdLookup(tracklistRows);

  const berghain = {
    artists: artistFreqText ? parseCsv(artistFreqText).rows : [],
    events: eventsText ? parseCsv(eventsText).rows : [],
    observations: observationsMd ?? "",
    top50: top50Text ? parseCsv(top50Text).rows : [],
    overlaps: overlapsText ? parseCsv(overlapsText).rows : [],
    tracklists: tracklistRows.slice(0, 50),
  };

  return buildState({
    index,
    playlists,
    bySlug,
    berghain,
    comparisons,
    remmex,
    trackIdLookup,
    loadedAt: new Date(),
  });
}

export function buildState({ index, playlists, bySlug, berghain, comparisons, remmex, trackIdLookup, loadedAt }) {
  const playlistList = playlists.playlists.map((p) => ({
    ...p,
    artifact: bySlug[p.slug] ?? null,
  }));

  const groups = {};
  for (const p of playlistList) {
    const parent = p.parent || "OTHER";
    if (!groups[parent]) groups[parent] = [];
    groups[parent].push(p);
  }

  const totals = playlistList.reduce(
    (acc, p) => {
      const s = p.artifact?.stats;
      if (!s?.hasScores) {
        acc.missing.push(p.slug);
        return acc;
      }
      acc.analyzed++;
      acc.tracks += s.trackCount || 0;
      acc.outliers += s.outliers || 0;
      return acc;
    },
    { analyzed: 0, tracks: 0, outliers: 0, missing: [] }
  );

  const curationQueue = playlistList
    .filter((p) => p.artifact?.stats?.hasScores && p.artifact.stats.outliers > 0)
    .sort((a, b) => b.artifact.stats.outlierPct - a.artifact.stats.outlierPct);

  return {
    index,
    playlists,
    playlistList,
    groups,
    bySlug,
    berghain,
    comparisons,
    remmex,
    totals,
    curationQueue,
    trackIdLookup,
    loadedAt,
    scripts: index?.layers?.digging_platform?.scripts ?? [],
    reports: index?.layers?.digging_platform?.analysis_reports ?? [],
  };
}
