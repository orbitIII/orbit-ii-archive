const $ = (id) => document.getElementById(id);

const state = {
  sessionId: null,
  session: null,
  editingId: null,
  saveTimer: null,
  pollTimer: null,
  lastRemoteUpdate: null,
  dirty: false,
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
  showToast._timer = setTimeout(() => toast.classList.add("hidden"), 2400);
}

function setSyncStatus(kind, text) {
  const el = $("syncStatus");
  el.className = `sync ${kind}`;
  el.textContent = text;
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
}

async function createSession(title) {
  const res = await fetch("/api/sessions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (!res.ok) throw new Error("Session konnte nicht erstellt werden");
  return res.json();
}

async function fetchSession(id) {
  const res = await fetch(`/api/sessions/${id}`);
  if (!res.ok) return null;
  return res.json();
}

async function saveSession() {
  if (!state.sessionId || !state.session) return;

  setSyncStatus("saving", "Speichert…");
  const res = await fetch(`/api/sessions/${state.sessionId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: state.session.title,
      entries: state.session.entries,
    }),
  });

  if (!res.ok) {
    setSyncStatus("error", "Fehler beim Speichern");
    return;
  }

  const saved = await res.json();
  state.session = saved;
  state.lastRemoteUpdate = saved.updatedAt;
  state.dirty = false;
  setSyncStatus("saved", "Gespeichert");
  $("updatedAt").textContent = `Zuletzt: ${formatDate(saved.updatedAt)}`;
}

function scheduleSave() {
  state.dirty = true;
  clearTimeout(state.saveTimer);
  state.saveTimer = setTimeout(() => saveSession(), 500);
}

function renderSummary() {
  const entries = state.session?.entries || [];
  const summary = $("summary");
  summary.innerHTML = `
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

async function loadSession(id) {
  const session = await fetchSession(id);
  if (!session) {
    showHomeView();
    showToast("Link ungültig oder Runde gelöscht");
    return;
  }

  state.sessionId = id;
  state.session = session;
  state.lastRemoteUpdate = session.updatedAt;
  $("sessionTitle").value = session.title;
  setUrlForSession(id);
  showSessionView();
  renderEntries();
  $("updatedAt").textContent = `Zuletzt: ${formatDate(session.updatedAt)}`;
  setSyncStatus("saved", "Verbunden");
  startPolling();
}

function startPolling() {
  clearInterval(state.pollTimer);
  state.pollTimer = setInterval(async () => {
    if (!state.sessionId || state.dirty) return;
    const remote = await fetchSession(state.sessionId);
    if (!remote) return;
    if (remote.updatedAt !== state.lastRemoteUpdate) {
      state.session = remote;
      state.lastRemoteUpdate = remote.updatedAt;
      $("sessionTitle").value = remote.title;
      renderEntries();
      $("updatedAt").textContent = `Zuletzt: ${formatDate(remote.updatedAt)}`;
      setSyncStatus("saved", "Aktualisiert");
    }
  }, 3000);
}

function bindEvents() {
  $("createSessionBtn").addEventListener("click", async () => {
    const title = $("newTitleInput").value.trim() || "Neue Testrunde";
    try {
      const session = await createSession(title);
      await loadSession(session.id);
      showToast("Runde erstellt – Link kann geteilt werden");
    } catch {
      showToast("Fehler beim Erstellen");
    }
  });

  $("newSessionBtn").addEventListener("click", () => {
    history.replaceState({}, "", "/");
    state.sessionId = null;
    state.session = null;
    clearInterval(state.pollTimer);
    showHomeView();
  });

  $("shareBtn").addEventListener("click", async () => {
    const url = window.location.href;
    try {
      await navigator.clipboard.writeText(url);
      showToast("Link kopiert!");
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
        id: crypto.randomUUID(),
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
}

async function init() {
  bindRatingOutputs();
  bindEvents();
  resetForm();

  const id = getSessionIdFromUrl();
  if (id) {
    await loadSession(id);
  } else {
    showHomeView();
  }
}

init();
