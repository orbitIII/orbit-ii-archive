import { loadOrbitData, buildState } from "./data-loader.js";

const VIEWS = [
  { id: "overview", label: "Funktion" },
  { id: "layers", label: "Schichten" },
  { id: "pillars", label: "Säulen" },
  { id: "principles", label: "Prinzipien" },
  { id: "litmus", label: "Litmus" },
  { id: "werk", label: "Werk" },
];

let state = null;
let currentView = "overview";
let selectedPrinciples = new Set();
let openLayer = 0;

const app = document.getElementById("app");
const nav = document.getElementById("main-nav");

function esc(s) {
  const d = document.createElement("div");
  d.textContent = s ?? "";
  return d.innerHTML;
}

function renderNav() {
  nav.innerHTML = VIEWS.map(
    (v) =>
      `<button type="button" data-view="${v.id}" class="${v.id === currentView ? "active" : ""}">${esc(v.label)}</button>`
  ).join("");
  nav.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => {
      currentView = btn.dataset.view;
      renderNav();
      renderView();
    });
  });
}

function renderView() {
  if (!state) return;
  const html = {
    overview: renderOverview,
    layers: renderLayers,
    pillars: renderPillars,
    principles: renderPrinciples,
    litmus: renderLitmus,
    werk: renderWerk,
  }[currentView]?.() ?? "<p>Unbekannte Ansicht</p>";

  app.innerHTML = `<section class="view active">${html}</section>`;
  bindViewEvents();
}

function renderOverview() {
  const p = state.pflicht;
  const phase2 = state.phases["2_destillieren"];
  return `
    <h1>Was ORBIT tun soll</h1>
    <p class="lead">${esc(state.mission)}</p>

    <div class="card-grid">
      <article class="card highlight">
        <h3>Mittelpunkt</h3>
        <p>Du + <em>Pour Cet Instant</em> — nicht Marquardt, nicht ein Museum, nicht ein Moodboard.</p>
        <span class="tag">Phase 2 · Destillieren</span>
      </article>
      <article class="card">
        <h3>Archiv</h3>
        <p>Referenz ist Rohstoff. Operatoren extrahieren, filtern, in Output überführen.</p>
        <span class="tag">Sammeln ✓ · Destillieren aktiv</span>
      </article>
      <article class="card">
        <h3>Endziel</h3>
        <p>Gelebte Identität — Kleidung, Stimme, Musik, Kunst, Foto, Film aus einem Kern.</p>
        <span class="tag">Phase 5 · Leben</span>
      </article>
    </div>

    <h2>Pflicht vor jedem Output</h2>
    <p class="muted">${esc(p.statement)}</p>
    <ul class="checklist">
      <li><span class="status pass"></span><span>Arbeitsweise im Hinterkopf (immer)</span></li>
      <li><span class="status pass"></span><span>Min. <strong>${p.minimum?.kunst_prinzipien ?? 2}</strong> benannte Kunst-Prinzipien</span></li>
      <li><span class="status warn"></span><span>Affekt im Werk — nur wenn das Werk Stimmung trägt</span></li>
      <li><span class="status pass"></span><span>Ethik-Check · Identität: trägt es DEINEN Kern?</span></li>
    </ul>

    <h2>Persona-Formel</h2>
    <p><strong>Eigenes Werk (Filter) × Affekt × Prinzip (2+ Säulen) × Entscheidung = Persona</strong></p>
    <p class="muted">Nicht: Referenz × Stil × Personenname.</p>

    <h2>Litmus (DNA)</h2>
    <p class="lead" style="font-size:0.95rem;border-left:3px solid var(--accent);padding-left:1rem;">${esc(state.litmus)}</p>

    <h2>Spannungsachse</h2>
    <p>${esc(state.tension.label)} — ${esc(state.tension.rule)}</p>
    <div class="pill-row">
      <span class="pill">${esc(state.tension.pole_a?.mood)} · ${esc(state.tension.pole_a?.visual)}</span>
      <span class="pill">×</span>
      <span class="pill">${esc(state.tension.pole_b?.mood)} · ${esc(state.tension.pole_b?.visual)}</span>
    </div>

    ${phase2 ? `<h2>Aktuelle Phase</h2><p><strong>${esc(phase2.label)}</strong> — ${esc(phase2.regel)}</p><p class="muted">Exit: ${esc(phase2.exit)}</p>` : ""}

    <h2>Workflow (${(p.workflow ?? []).length} Schritte)</h2>
    <ol class="muted">${(p.workflow ?? []).map((s) => `<li>${esc(s)}</li>`).join("")}</ol>
  `;
}

function renderLayers() {
  const order = [
    ["schicht_0_mittelpunkt", 0],
    ["schicht_1_werk", 1],
    ["schicht_2_prinzipien", 2],
    ["schicht_3_saeulen", 3],
    ["schicht_4_case_studies", 4],
    ["schicht_5_rohdaten", 5],
  ];
  const desc = state.schichten.description ?? "";

  const layers = order
    .map(([key, num]) => {
      const s = state.schichten[key];
      if (!s) return "";
      const files = s.files ?? (s.file ? [s.file] : []);
      const open = openLayer === num ? " open" : "";
      return `
        <div class="layer${open}" data-layer="${num}">
          <div class="layer-head">
            <span><span class="layer-num">Schicht ${num}</span> · <span class="layer-title">${esc(s.label)}</span></span>
          </div>
          <div class="layer-body">
            <p>${esc(s.regel ?? s.description ?? "")}</p>
            ${s.filter_frage ? `<p><em>${esc(s.filter_frage)}</em></p>` : ""}
            ${files.length ? `<ul>${files.map((f) => `<li><code>${esc(typeof f === "string" ? f : f)}</code></li>`).join("")}</ul>` : ""}
            ${s.saeulen ? `<div class="pill-row">${s.saeulen.map((x) => `<span class="pill">${esc(x)}</span>`).join("")}</div>` : ""}
          </div>
        </div>`;
    })
    .join("");

  return `
    <h1>Schichtenmodell</h1>
    <p class="lead">${esc(desc)}</p>
    <p class="muted">Von innen nach außen — jede Schicht filtert die nächste. Klick zum Aufklappen.</p>
    <div class="stack">${layers}</div>
  `;
}

function renderPillars() {
  const saeulen = state.fundament?.saeulen ?? {};
  const saeulenAnalysis = state.data.fundament?.saeulen_tiefenanalyse ?? {};
  const keys = Object.keys(saeulen);

  const cards = keys
    .map((key) => {
      const s = saeulen[key];
      const deep = saeulenAnalysis[key] ?? {};
      const highlight = key === "eigenes_werk" ? " highlight" : "";
      return `
        <article class="card${highlight}">
          <h3>${esc(s.label)}</h3>
          <p>${esc(deep.was_es_ist ?? s.regel ?? "")}</p>
          ${deep.operatoren_extrahierbar ? `<div class="pill-row">${deep.operatoren_extrahierbar.slice(0, 6).map((o) => `<span class="pill">${esc(o)}</span>`).join("")}</div>` : ""}
          ${deep.nicht_extrahieren ? `<p style="margin-top:0.6rem;font-size:0.8rem;"><strong>Nicht:</strong> ${esc(deep.nicht_extrahieren.join(", "))}</p>` : ""}
          <span class="tag">${esc(s.gewicht ?? "gleich")} · ${esc(s.spatial_anchor ?? key)}</span>
        </article>`;
    })
    .join("");

  const bridgeCards = (state.bridges ?? [])
    .map(
      (b) => `
      <article class="card">
        <h3>${esc(b.id)}</h3>
        <p>${esc(b.spannung ?? b.operatoren?.join(" · ") ?? "")}</p>
        <div class="pill-row">${(b.principles ?? b.operatoren ?? []).map((p) => `<span class="pill">${esc(p)}</span>`).join("")}</div>
      </article>`
    )
    .join("");

  const weaveCards = state.weaves
    .map(
      (w) => `
      <article class="card">
        <h3>${esc(w.label ?? w.id)}</h3>
        <p>${esc(w.summary ?? "")}</p>
        <span class="tag">Berlin Case · ${esc(w.id)}</span>
      </article>`
    )
    .join("");

  const mamCount = Object.keys(state.mamMovements).length;
  const parisBundles = state.data.fundament?.weave_katalog?.paris_case_bundles ?? [];

  return `
    <h1>Referenz-Säulen</h1>
    <p class="lead">Gleichgewichtig — keine Person ist ORBIT. Berlin-Batch ≠ gesamte DNA.</p>
    <div class="card-grid">${cards}</div>

    <h2>Cross-Säulen-Brücken</h2>
    <div class="card-grid">${bridgeCards}</div>

    <h2>Berlin Case Studies (Weaves)</h2>
    <div class="card-grid">${weaveCards}</div>

    <h2>Paris (${mamCount} Bewegungen · ${parisBundles.length} Bundles)</h2>
    <div class="card-grid">
      ${parisBundles.map((b) => `<article class="card"><h3>${esc(b.id)}</h3><p>${esc(b.extrahiere ?? "")}</p></article>`).join("")}
    </div>
  `;
}

function renderPrinciples() {
  const pills = state.principles
    .map(
      (p) =>
        `<span class="pill selectable ${selectedPrinciples.has(p.id) ? "selected" : ""}" data-principle="${esc(p.id)}">${esc(p.label)}</span>`
    )
    .join("");

  const comboMatches = Object.entries(state.combinations).filter(([, ids]) => {
    const sel = [...selectedPrinciples];
    return sel.length >= 2 && ids.every((id) => selectedPrinciples.has(id));
  });

  const detailId = [...selectedPrinciples][0];
  const detail = state.principles.find((p) => p.id === detailId);

  return `
    <h1>Kunst-Prinzipien</h1>
    <p class="lead">Operatoren, nicht Stil-Wörter. Wähle min. 2 für einen Litmus-Check.</p>
    <p class="muted">${state.principles.length} Prinzipien geladen · ${Object.keys(state.combinations).length} Kombinationen</p>

    <div class="pill-row" id="principle-pills">${pills}</div>

    ${selectedPrinciples.size > 0 ? `<p style="margin-top:1rem;"><strong>${selectedPrinciples.size}</strong> gewählt: ${[...selectedPrinciples].map(esc).join(", ")}</p>` : ""}

    ${comboMatches.length ? `<h2>Passende Kombinationen</h2><ul>${comboMatches.map(([k, v]) => `<li><code>${esc(k)}</code>: ${v.map(esc).join(" · ")}</li>`).join("")}</ul>` : ""}

    ${detail ? renderPrincipleDetail(detail) : ""}

    <h2>MAM-Operatoren (Paris)</h2>
    <div class="pill-row">${Object.entries(state.mamPrinciples).map(([id, p]) => `<span class="pill" title="${esc(p.definition)}">${esc(p.label ?? id)}</span>`).join("")}</div>
  `;
}

function renderPrincipleDetail(p) {
  return `
    <div class="principle-detail">
      <h3>${esc(p.label)} <code style="font-size:0.75rem;color:var(--muted)">${esc(p.id)}</code></h3>
      <dl>
        <dt>Definition</dt><dd>${esc(p.definition)}</dd>
        <dt>ORBIT</dt><dd>${esc(p.orbit_meaning)}</dd>
        ${p.exemplars.length ? `<dt>Exemplare</dt><dd>${p.exemplars.slice(0, 4).map(esc).join(" · ")}</dd>` : ""}
        ${p.forbidden.length ? `<dt>Forbidden</dt><dd>${p.forbidden.map(esc).join(" · ")}</dd>` : ""}
      </dl>
    </div>`;
}

function renderLitmus() {
  const mediumOptions = ["film", "foto", "musik", "kunst", "marketing", "mode"].map(
    (m) => `<option value="${m}">${m}</option>`
  );

  const principlePills = state.principles
    .map(
      (p) =>
        `<span class="pill selectable litmus-pill ${selectedPrinciples.has(p.id) ? "selected" : ""}" data-principle="${esc(p.id)}">${esc(p.id)}</span>`
    )
    .join("");

  return `
    <h1>Litmus-Check</h1>
    <p class="lead">Teste eine Projektidee gegen ORBIT-Regeln — bevor du produzierst.</p>

    <div class="form-block">
      <label for="project-idea">Projektidee (1–3 Sätze)</label>
      <textarea id="project-idea" placeholder="z.B. Galerie-Nacht mit SW-Porträts und reduced Set — kein Peak-Techno …"></textarea>
    </div>

    <div class="form-block">
      <label for="project-medium">Lead-Medium</label>
      <select id="project-medium">${mediumOptions}</select>
    </div>

    <div class="form-block">
      <label>Prinzipien (min. 2)</label>
      <div class="pill-row" id="litmus-principles">${principlePills}</div>
    </div>

    <button type="button" class="btn" id="run-litmus">Check ausführen</button>

    <div id="litmus-result"></div>
  `;
}

function runLitmusCheck() {
  const idea = document.getElementById("project-idea")?.value?.trim() ?? "";
  const medium = document.getElementById("project-medium")?.value ?? "film";
  const minPrinciples = state.pflicht.minimum?.kunst_prinzipien ?? 2;

  const checks = [];

  checks.push({
    ok: idea.length >= 20,
    warn: idea.length > 0 && idea.length < 20,
    text: "Projektidee konkret formuliert (min. 20 Zeichen)",
  });

  checks.push({
    ok: selectedPrinciples.size >= minPrinciples,
    text: `Min. ${minPrinciples} Kunst-Prinzipien benannt (${selectedPrinciples.size} gewählt)`,
  });

  const ideaLower = idea.toLowerCase();
  const forbiddenHits = state.forbidden.filter((f) => ideaLower.includes(f.replace(/-/g, " ")) || ideaLower.includes(f));
  checks.push({
    ok: forbiddenHits.length === 0,
    text: forbiddenHits.length ? `Forbidden-Signal erkannt: ${forbiddenHits.join(", ")}` : "Kein DNA-forbidden Signal im Text",
  });

  const personCopy = /\b(marquardt|berghain.?bouncer.?cosplay|kopie von)\b/i.test(idea);
  checks.push({
    ok: !personCopy,
    text: personCopy ? "Warnung: Personen-Kopie-Signal im Text" : "Kein Personen-Kopie-Signal",
  });

  const werkOverlap = state.werkPrinciples.filter((p) => selectedPrinciples.has(p));
  checks.push({
    ok: werkOverlap.length >= 1 || selectedPrinciples.size === 0,
    warn: selectedPrinciples.size > 0 && werkOverlap.length === 0,
    text:
      werkOverlap.length > 0
        ? `Pour Cet Instant trägt: ${werkOverlap.join(", ")}`
        : "Optional: min. 1 Prinzip overlap mit Pour Cet Instant",
  });

  const canExplain = selectedPrinciples.size >= 2 && idea.length >= 20;
  checks.push({
    ok: canExplain,
    warn: !canExplain,
    text: state.pflicht.litmus ?? "Prinzipien in einem Satz erklärbar — ohne Stil-Wörter?",
  });

  const failCount = checks.filter((c) => c.ok === false).length;
  const warnCount = checks.filter((c) => c.warn && c.ok !== false).length;
  const verdict = failCount > 0 ? "fail" : warnCount > 0 ? "warn" : "pass";
  const verdictLabel = { pass: "ORBIT-tauglich", warn: "Nachschärfen", fail: "Noch nicht ORBIT" }[verdict];

  const summary =
    selectedPrinciples.size >= 2
      ? `Aktive Operatoren: ${[...selectedPrinciples].join(" + ")} — Medium: ${medium}.`
      : "Wähle Prinzipien und beschreibe die Idee.";

  return `
    <div class="result-box verdict-${verdict}">
      <h2 style="margin:0 0 0.5rem;color:var(--text);font-size:1rem;">${verdictLabel}</h2>
      <p class="muted">${esc(summary)}</p>
      <ul class="checklist">
        ${checks
          .map((c) => {
            const cls = c.ok ? "pass" : c.warn ? "warn" : "fail";
            return `<li><span class="status ${cls}"></span><span>${esc(c.text)}</span></li>`;
          })
          .join("")}
      </ul>
      ${verdict !== "fail" ? `<p style="margin-top:1rem;font-size:0.85rem;">Nächster Schritt: Prinzipien in Werk-JSON eintragen → dann produzieren.</p>` : ""}
    </div>`;
}

function renderWerk() {
  const w = state.werk;
  if (!w) return "<p>Werk-Daten nicht geladen.</p>";

  const principles = w.kunst_prinzipien?.begruendung ?? {};
  const affekte = w.affekt_analyse?.hauptgefuehle ?? {};

  return `
    <h1>${esc(w.title)}</h1>
    <p class="lead">${esc(w.synopsis?.logline ?? w.role_in_orbit)}</p>
    <p class="muted">${esc(w.role_in_orbit)} · Shoot ${esc(w.source?.shoot)}</p>

    <h2>Synopsis</h2>
    <p>${esc(w.synopsis?.de)}</p>

    <h2>Aktive Prinzipien (${(w.kunst_prinzipien?.aktiv ?? []).length})</h2>
    <dl class="principle-detail" style="padding:0;border:none;background:transparent;">
      ${Object.entries(principles)
        .map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`)
        .join("")}
    </dl>

    <h2>Affekt</h2>
    <div class="card-grid">
      ${Object.entries(affekte)
        .map(([k, v]) => `<article class="card"><h3>${esc(k)}</h3><p>${esc(v)}</p></article>`)
        .join("")}
    </div>

    <h2>Filter-Frage (Fundament)</h2>
    <p class="lead" style="font-size:0.95rem;">Würde Pour Cet Instant diese Operator-Zusage tragen — oder nur ein Moodboard?</p>
    <p class="muted">Jede Referenz-Säule filtert durch dieses Werk — nicht umgekehrt.</p>
  `;
}

function bindViewEvents() {
  app.querySelectorAll(".layer").forEach((el) => {
    el.addEventListener("click", () => {
      openLayer = Number(el.dataset.layer);
      renderView();
    });
  });

  app.querySelectorAll(".pill.selectable[data-principle]").forEach((pill) => {
    pill.addEventListener("click", () => {
      const id = pill.dataset.principle;
      if (selectedPrinciples.has(id)) selectedPrinciples.delete(id);
      else selectedPrinciples.add(id);
      renderView();
    });
  });

  document.getElementById("run-litmus")?.addEventListener("click", () => {
    const box = document.getElementById("litmus-result");
    if (box) box.innerHTML = runLitmusCheck();
  });
}

async function init() {
  renderNav();
  try {
    const data = await loadOrbitData();
    state = buildState(data);
    selectedPrinciples = new Set(state.werkPrinciples.slice(0, 3));
    renderView();
  } catch (err) {
    app.innerHTML = `
      <section class="view active">
        <div class="error-banner">
          <strong>Daten nicht geladen.</strong> Starte den Server aus dem Repo-Root:<br />
          <code>python3 scripts/serve_orbit_lab.py</code><br />
          Dann öffne <a href="http://127.0.0.1:8765/app/orbit-lab/" style="color:var(--accent)">http://127.0.0.1:8765/app/orbit-lab/</a>
        </div>
        <p class="muted">${esc(err.message)}</p>
      </section>`;
  }
}

init();
