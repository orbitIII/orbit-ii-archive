const express = require("express");
const fs = require("fs");
const path = require("path");
const { v4: uuidv4 } = require("uuid");

const app = express();
const PORT = process.env.PORT || 3847;
const DATA_DIR = path.join(__dirname, "data");

if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

app.use(express.json({ limit: "1mb" }));
app.use(express.static(path.join(__dirname, "public")));

function sessionPath(id) {
  return path.join(DATA_DIR, `${id}.json`);
}

function readSession(id) {
  const file = sessionPath(id);
  if (!fs.existsSync(file)) return null;
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return null;
  }
}

function writeSession(session) {
  fs.writeFileSync(sessionPath(session.id), JSON.stringify(session, null, 2));
}

function defaultSession(id, title = "Neue Testrunde") {
  return {
    id,
    title,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    entries: [],
  };
}

app.post("/api/sessions", (req, res) => {
  const id = uuidv4().slice(0, 8);
  const title = (req.body?.title || "Neue Testrunde").trim().slice(0, 120);
  const session = defaultSession(id, title);
  writeSession(session);
  res.json(session);
});

app.get("/api/sessions/:id", (req, res) => {
  const session = readSession(req.params.id);
  if (!session) {
    return res.status(404).json({ error: "Session nicht gefunden" });
  }
  res.json(session);
});

app.put("/api/sessions/:id", (req, res) => {
  const existing = readSession(req.params.id);
  if (!existing) {
    return res.status(404).json({ error: "Session nicht gefunden" });
  }

  const { title, entries } = req.body || {};
  const session = {
    ...existing,
    title: typeof title === "string" ? title.trim().slice(0, 120) : existing.title,
    entries: Array.isArray(entries) ? entries : existing.entries,
    updatedAt: new Date().toISOString(),
  };

  writeSession(session);
  res.json(session);
});

app.get("*", (_req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
  console.log(`Restauranttester läuft auf http://localhost:${PORT}`);
});
