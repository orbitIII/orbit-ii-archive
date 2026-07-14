const $ = (id) => document.getElementById(id);

const STORAGE_KEY = "restaurant-tester:sessions:v1";
const STORAGE_META_KEY = "restaurant-tester:meta:v1";

const state = {
  sessionId: null,
  session: null,
  editingId: null,
  saveTimer: null,
  pollTimer: null,
  lastRemoteUpdate: null,
  dirty: false,
  online: navigator.onLine,
  publicBaseUrl: window.location.origin,
  deferredInstall: null,
};

const ratingFields = [
  ["ratingFood", "ratingFoodOut", "food"],
  ["ratingService", "ratingServiceOut", "service"],
  ["ratingAmbience", "ratingAmbienceOut", "ambience"],
  ["ratingValue", "ratingValueOut", "value"],
];

function showToast(message) {
  const toast = $("toast");
  toast.textContent = message;
  toast.classList.remove("hidden");
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => toast.classList.add("hidden"), 2600);
}

function setSyncStatus(kind, text) {
  const el = $("syncStatus");
  el.className = `sync ${kind}`;
  el.textContent = text;
}

function updateOnlineBadge() {
  const badge = $("onlineBadge");
  badge.textContent = state.online ? "Online" : "Offline";
  badge.className = `online-badge ${state.online ? "online" : "offline"}`;
}

function formatDate(value) {
  if (!value) return "–";
  return new Date(value).toLocaleString("de-DE", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function average(entries, key) {
  if (!entries.length) return "–";
  const sum = entries.reduce((acc, entry) => acc + Number(entry[key] || 0), 0);
  return (sum / entries.length).toFixed(1);
}

function shortId() {
  if (crypto.randomUUID) return crypto.randomUUID().slice(0, 8);
  return Math.random().toString(36).slice(2, 10);
}

function getSessionIdFromUrl() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  return parts[0] === "s" && parts[1] ? parts[1] : null;
}

function setUrlForSession(id) {
  const next = `/s/${id}`;
  if (window.location.pathname !== next) {
    history.replaceState({}, "", next);
  }
}

function showSessionView() {
  $("homeView").classList.add("hidden");
  $("sessionView").classList.remove("hidden");
}

function showHomeView() {
  $("homeView").classList.remove("hidden");
  $("sessionView").classList.add("hidden");
  renderArchive();
}

/* ---------- Local long-term storage ---------- */

function readStore() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function writeStore(store) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
}

function listLocalSessions() {
  return Object.values(readStore()).sort(
    (a, b) => new Date(b.updatedAt || b.createdAt) - new Date(a.updatedAt || a.createdAt)
  );
}

function getLocalSession(id) {
  return readStore()[id] || null;
}

function saveLocalSession(session) {
  const store = readStore();
  store[session.id] = session;
  writeStore(store);
  try {
    localStorage.setItem(
      STORAGE_META_KEY,
      JSON.stringify({ lastSavedAt: new Date().toISOString(), count: Object.keys(store).length })
    );
  } catch {
    // ignore quota metadata errors
  }
}

function deleteLocalSession(id) {
  const store = readStore();
  delete store[id];
  writeStore(store);
}

function defaultSession(id, title = "Neue Testrunde") {
  const now = new Date().toISOString();
  return {
    id,
    title,
    createdAt: now,
    updatedAt: now,
    entries: [],
  };
}

function mergeSessions(local, remote) {
  if (!local) return remote;
  if (!remote) return local;

  const localTime = new Date(local.updatedAt || 0).getTime();
  const remoteTime = new Date(remote.updatedAt || 0).getTime();
  const newer = localTime >= remoteTime ? local : remote;
  const older = newer === local ? remote : local;

  const byId = new Map();
  for (const entry of older.entries || []) byId.set(entry.id, entry);
  for (const entry of newer.entries || []) {
    const existing = byId.get(entry.id);
    if (!existing) {
      byId.set(entry.id, entry);
      continue;
    }
    const eNew = new Date(entry.updatedAt || entry.createdAt || 0).getTime();
    const eOld = new Date(existing.updatedAt || existing.createdAt || 0).getTime();
    byId.set(entry.id, eNew >= eOld ? entry : existing);
  }

  return {
    ...older,
    ...newer,
    title: newer.title || older.title,
    entries: Array.from(byId.values()),
    updatedAt: newer.updatedAt || older.updatedAt,
  };
}

/* ---------- Network sync (optional) ---------- */

async function apiCreateSession(title, id) {
  const res = await fetch("/api/sessions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, id }),
  });
  if (!res.ok) throw new Error("create failed");
  return res.json();
}

async function apiFetchSession(id) {
  const res = await fetch(`/api/sessions/${id}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new Error("fetch failed");
  return res.json();
}

async function apiUpsertSession(session) {
  const res = await fetch(`/api/sessions/${session.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: session.title,
      entries: session.entries,
      createdAt: session.createdAt,
      upsert: true,
    }),
  });
  if (!res.ok) throw new Error("upsert failed");
  return res.json();
}

async function persistAndSync() {
  if (!state.sessionId || !state.session) return;

  state.session.updatedAt = new Date().toISOString();
  saveLocalSession(state.session);
  $("updatedAt").textContent = `Lokal: ${formatDate(state.session.updatedAt)}`;
  setSyncStatus("saved", "Lokal gespeichert");

  if (!state.online) {
    setSyncStatus("saving", "Offline gespeichert");
    state.dirty = false;
    return;
  }

  setSyncStatus("saving", "Synchronisiert…");
  try {
    const saved = await apiUpsertSession(state.session);
    state.session = mergeSessions(state.session, saved);
    saveLocalSession(state.session);
    state.lastRemoteUpdate = saved.updatedAt;
    state.dirty = false;
    setSyncStatus("saved", "Gespeichert + Sync");
    $("updatedAt").textContent = `Zuletzt: ${formatDate(state.session.updatedAt)}`;
  } catch {
    state.dirty = false;
    setSyncStatus("error", "Nur lokal (Sync später)");
  }
}

function scheduleSave() {
  state.dirty = true;
  clearTimeout(state.saveTimer);
  state.saveTimer = setTimeout(() => persistAndSync(), 350);
}

/* ---------- Export / Import ---------- */

function downloadBlob(filename, blob) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function exportSessionJson(session) {
  const payload = {
    app: "restaurant-tester",
    version: 1,
    exportedAt: new Date().toISOString(),
    session,
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const safe = (session.title || "runde").replace(/[^\w\-]+/g, "_").slice(0, 40);
  downloadBlob(`${safe || "runde"}-${session.id}.json`, blob);
}

function exportSessionCsv(session) {
  const header = [
    "restaurant",
    "visitDate",
    "food",
    "service",
    "ambience",
    "value",
    "overall",
    "tester",
    "notes",
  ];
  const rows = (session.entries || []).map((entry) =>
    header
      .map((key) => {
        const raw = entry[key] == null ? "" : String(entry[key]);
        return `"${raw.replaceAll('"', '""')}"`;
      })
      .join(",")
  );
  const csv = [header.join(","), ...rows].join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const safe = (session.title || "runde").replace(/[^\w\-]+/g, "_").slice(0, 40);
  downloadBlob(`${safe || "runde"}-${session.id}.csv`, blob);
}

function normalizeImportedSession(raw) {
  const session = raw?.session || raw;
  if (!session || typeof session !== "object") throw new Error("Ungültiges Backup");
  const id = String(session.id || shortId()).slice(0, 32);
  return {
    id,
    title: String(session.title || "Importierte Runde").slice(0, 120),
    createdAt: session.createdAt || new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    entries: Array.isArray(session.entries) ? session.entries : [],
  };
}

async function importFromFile(file) {
  const text = await file.text();
  const data = JSON.parse(text);
  const session = normalizeImportedSession(data);
  const existing = getLocalSession(session.id);
  const merged = existing ? mergeSessions(existing, session) : session;
  merged.updatedAt = new Date().toISOString();
  saveLocalSession(merged);
  await openSession(merged.id, { preferLocal: true });
  showToast("Backup importiert und lokal gespeichert");
  if (state.online) {
    try {
      await apiUpsertSession(merged);
    } catch {
      // keep local copy
    }
  }
}

/* ---------- Rendering ---------- */

function renderArchive() {
  const sessions = listLocalSessions();
  $("archiveCount").textContent = String(sessions.length);
  $("archiveEmpty").classList.toggle("hidden", sessions.length > 0);

  const list = $("archiveList");
  list.innerHTML = sessions
    .map(
      (session) => `
      <article class="archive-item">
        <div>
          <strong>${escapeHtml(session.title || "Ohne Titel")}</strong>
          <div class="entry-meta">${session.entries?.length || 0} Einträge · ${escapeHtml(formatDate(session.updatedAt))}</div>
        </div>
        <div class="archive-actions">
          <button class="btn btn-primary open-btn" type="button" data-id="${session.id}">Öffnen</button>
          <button class="btn btn-secondary export-btn" type="button" data-id="${session.id}">Export</button>
          <button class="btn btn-danger delete-archive-btn" type="button" data-id="${session.id}">Löschen</button>
        </div>
      </article>
    `
    )
    .join("");

  list.querySelectorAll(".open-btn").forEach((btn) => {
    btn.addEventListener("click", () => openSession(btn.dataset.id, { preferLocal: true }));
  });
  list.querySelectorAll(".export-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const session = getLocalSession(btn.dataset.id);
      if (session) {
        exportSessionJson(session);
        showToast("JSON-Backup heruntergeladen");
      }
    });
  });
  list.querySelectorAll(".delete-archive-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (!confirm("Lokale Runde wirklich löschen?")) return;
      deleteLocalSession(btn.dataset.id);
      renderArchive();
      showToast("Lokale Runde gelöscht");
    });
  });
}

function renderSummary() {
  const entries = state.session?.entries || [];
  $("summary").innerHTML = `
    <div class="summary-item"><span>Restaurants</span><strong>${entries.length}</strong></div>
    <div class="summary-item"><span>Ø Essen</span><strong>${average(entries, "food")}</strong></div>
    <div class="summary-item"><span>Ø Service</span><strong>${average(entries, "service")}</strong></div>
    <div class="summary-item"><span>Ø Gesamt</span><strong>${average(entries, "overall")}</strong></div>
  `;
}

function renderEntries() {
  const entries = [...(state.session?.entries || [])].sort(
    (a, b) => new Date(b.visitDate || b.createdAt) - new Date(a.visitDate || a.createdAt)
  );

  $("entryCount").textContent = String(entries.length);
  $("emptyState").classList.toggle("hidden", entries.length > 0);

  const list = $("entriesList");
  list.innerHTML = entries
    .map((entry) => {
      const pills = [
        ["Essen", entry.food],
        ["Service", entry.service],
        ["Ambiente", entry.ambience],
        ["Preis", entry.value],
        ["Gesamt", entry.overall],
      ]
        .map(([label, value]) => `<span class="pill">${label}: <strong>${value}</strong></span>`)
        .join("");

      return `
        <article class="entry-card" data-id="${entry.id}">
          <div class="entry-top">
            <div>
              <div class="entry-title">${escapeHtml(entry.restaurant)}</div>
              <div class="entry-meta">${escapeHtml(entry.visitDate || "Kein Datum")} · ${escapeHtml(entry.tester || "Unbekannt")}</div>
            </div>
          </div>
          <div class="score-pills">${pills}</div>
          ${entry.notes ? `<div class="entry-notes">${escapeHtml(entry.notes)}</div>` : ""}
          <div class="entry-actions">
            <button class="btn btn-secondary edit-btn" type="button" data-id="${entry.id}">Bearbeiten</button>
            <button class="btn btn-danger delete-btn" type="button" data-id="${entry.id}">Löschen</button>
          </div>
        </article>
      `;
    })
    .join("");

  list.querySelectorAll(".edit-btn").forEach((btn) => {
    btn.addEventListener("click", () => startEdit(btn.dataset.id));
  });
  list.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", () => deleteEntry(btn.dataset.id));
  });

  renderSummary();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function resetForm() {
  state.editingId = null;
  $("entryForm").reset();
  $("visitDate").value = new Date().toISOString().slice(0, 10);
  ratingFields.forEach(([inputId, outputId]) => {
    $(inputId).value = "4";
    $(outputId).textContent = "4";
  });
  $("submitEntryBtn").textContent = "Eintrag speichern";
  $("cancelEditBtn").classList.add("hidden");
}

function readForm() {
  const food = Number($("ratingFood").value);
  const service = Number($("ratingService").value);
  const ambience = Number($("ratingAmbience").value);
  const value = Number($("ratingValue").value);
  const overall = Number(((food + service + ambience + value) / 4).toFixed(1));

  return {
    restaurant: $("restaurantName").value.trim(),
    visitDate: $("visitDate").value,
    food,
    service,
    ambience,
    value,
    overall,
    notes: $("notes").value.trim(),
    tester: $("testerName").value.trim() || "Unbekannt",
  };
}

function startEdit(id) {
  const entry = state.session.entries.find((item) => item.id === id);
  if (!entry) return;

  state.editingId = id;
  $("restaurantName").value = entry.restaurant;
  $("visitDate").value = entry.visitDate || "";
  $("notes").value = entry.notes || "";
  $("testerName").value = entry.tester || "";
  $("ratingFood").value = entry.food;
  $("ratingService").value = entry.service;
  $("ratingAmbience").value = entry.ambience;
  $("ratingValue").value = entry.value;
  ratingFields.forEach(([inputId, outputId]) => {
    $(outputId).textContent = $(inputId).value;
  });
  $("submitEntryBtn").textContent = "Änderung speichern";
  $("cancelEditBtn").classList.remove("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function deleteEntry(id) {
  if (!confirm("Eintrag wirklich löschen?")) return;
  state.session.entries = state.session.entries.filter((entry) => entry.id !== id);
  renderEntries();
  scheduleSave();
}

function bindRatingOutputs() {
  ratingFields.forEach(([inputId, outputId]) => {
    $(inputId).addEventListener("input", () => {
      $(outputId).textContent = $(inputId).value;
    });
  });
}

async function openSession(id, { preferLocal = false } = {}) {
  const local = getLocalSession(id);
  let remote = null;

  // When opening a known local archive offline-first, skip network if offline already handled.
  if (state.online && !(preferLocal && !navigator.onLine)) {
    try {
      remote = await apiFetchSession(id);
    } catch {
      remote = null;
    }
  }

  const session = mergeSessions(local, remote);
  if (!session) {
    showHomeView();
    showToast("Runde nicht gefunden (lokal/online)");
    return;
  }

  saveLocalSession(session);
  state.sessionId = id;
  state.session = session;
  state.lastRemoteUpdate = remote?.updatedAt || session.updatedAt;
  $("sessionTitle").value = session.title;
  setUrlForSession(id);
  showSessionView();
  renderEntries();
  $("updatedAt").textContent = `Lokal: ${formatDate(session.updatedAt)}`;
  setSyncStatus(state.online ? "saved" : "saving", state.online ? "Bereit" : "Offline-Modus");
  startPolling();

  if (state.online && (!remote || new Date(session.updatedAt) > new Date(remote.updatedAt || 0))) {
    persistAndSync();
  }
}

function startPolling() {
  clearInterval(state.pollTimer);
  state.pollTimer = setInterval(async () => {
    if (!state.sessionId || state.dirty || !state.online) return;
    try {
      const remote = await apiFetchSession(state.sessionId);
      if (!remote) return;
      if (remote.updatedAt !== state.lastRemoteUpdate) {
        const merged = mergeSessions(state.session, remote);
        state.session = merged;
        state.lastRemoteUpdate = remote.updatedAt;
        saveLocalSession(merged);
        $("sessionTitle").value = merged.title;
        renderEntries();
        $("updatedAt").textContent = `Zuletzt: ${formatDate(merged.updatedAt)}`;
        setSyncStatus("saved", "Aktualisiert");
      }
    } catch {
      // ignore poll errors
    }
  }, 4000);
}

async function createSessionOfflineFirst(title) {
  const id = shortId();
  const session = defaultSession(id, title);
  saveLocalSession(session);

  if (state.online) {
    try {
      const remote = await apiCreateSession(title, id);
      const merged = mergeSessions(session, remote);
      saveLocalSession(merged);
      return merged;
    } catch {
      return session;
    }
  }
  return session;
}

function triggerImportPicker() {
  $("importFileInput").value = "";
  $("importFileInput").click();
}

function bindEvents() {
  $("createSessionBtn").addEventListener("click", async () => {
    const title = $("newTitleInput").value.trim() || "Neue Testrunde";
    const session = await createSessionOfflineFirst(title);
    await openSession(session.id, { preferLocal: true });
    showToast(state.online ? "Runde erstellt" : "Runde lokal erstellt (offline)");
  });

  $("newSessionBtn").addEventListener("click", () => {
    history.replaceState({}, "", "/");
    state.sessionId = null;
    state.session = null;
    clearInterval(state.pollTimer);
    showHomeView();
  });

  $("shareBtn").addEventListener("click", async () => {
    if (!state.sessionId) {
      showToast("Zuerst eine Runde öffnen");
      return;
    }
    const url = `${state.publicBaseUrl}/s/${state.sessionId}`;
    try {
      await navigator.clipboard.writeText(url);
      showToast(state.online ? "Link kopiert!" : "Lokaler Link kopiert (Online zum Teilen)");
    } catch {
      prompt("Link kopieren:", url);
    }
  });

  $("sessionTitle").addEventListener("input", (event) => {
    if (!state.session) return;
    state.session.title = event.target.value;
    scheduleSave();
  });

  $("entryForm").addEventListener("submit", (event) => {
    event.preventDefault();
    const data = readForm();
    if (!data.restaurant) {
      showToast("Bitte Restaurantname eingeben");
      return;
    }

    const wasEditing = Boolean(state.editingId);

    if (wasEditing) {
      state.session.entries = state.session.entries.map((entry) =>
        entry.id === state.editingId
          ? { ...entry, ...data, updatedAt: new Date().toISOString() }
          : entry
      );
    } else {
      state.session.entries.push({
        id: crypto.randomUUID ? crypto.randomUUID() : shortId(),
        ...data,
        createdAt: new Date().toISOString(),
      });
    }

    renderEntries();
    scheduleSave();
    resetForm();
    showToast(wasEditing ? "Eintrag aktualisiert" : "Eintrag gespeichert");
  });

  $("cancelEditBtn").addEventListener("click", resetForm);

  $("exportJsonBtn").addEventListener("click", () => {
    if (!state.session) return;
    exportSessionJson(state.session);
    showToast("JSON-Backup gespeichert");
  });

  $("exportCsvBtn").addEventListener("click", () => {
    if (!state.session) return;
    exportSessionCsv(state.session);
    showToast("CSV exportiert");
  });

  $("importHomeBtn").addEventListener("click", triggerImportPicker);
  $("importSessionBtn").addEventListener("click", triggerImportPicker);
  $("importFileInput").addEventListener("change", async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      await importFromFile(file);
    } catch {
      showToast("Import fehlgeschlagen – ungültige Datei");
    }
  });

  $("installBtn").addEventListener("click", async () => {
    if (!state.deferredInstall) return;
    state.deferredInstall.prompt();
    await state.deferredInstall.userChoice;
    state.deferredInstall = null;
    $("installBtn").classList.add("hidden");
  });

  window.addEventListener("online", async () => {
    state.online = true;
    updateOnlineBadge();
    showToast("Wieder online – synchronisiere…");
    if (state.session) await persistAndSync();
  });

  window.addEventListener("offline", () => {
    state.online = false;
    updateOnlineBadge();
    setSyncStatus("saving", "Offline-Modus");
    showToast("Offline – Speicherung läuft lokal weiter");
  });

  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    state.deferredInstall = event;
    $("installBtn").classList.remove("hidden");
  });
}

async function loadPublicInfo() {
  if (!state.online) return;
  try {
    const res = await fetch("/api/info");
    if (!res.ok) return;
    const info = await res.json();
    if (info.publicBaseUrl) {
      state.publicBaseUrl = info.publicBaseUrl.replace(/\/$/, "");
    }
  } catch {
    // ignore
  }
}

function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) return;
  navigator.serviceWorker.register("/sw.js").catch(() => {
    // ignore registration failures
  });
}

async function init() {
  updateOnlineBadge();
  bindRatingOutputs();
  bindEvents();
  resetForm();
  registerServiceWorker();
  await loadPublicInfo();

  const id = getSessionIdFromUrl();
  if (id) {
    await openSession(id);
  } else {
    showHomeView();
  }
}

init();
