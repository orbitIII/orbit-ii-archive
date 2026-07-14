const express = require("express");
const fs = require("fs");
const path = require("path");
const { v4: uuidv4 } = require("uuid");

const app = express();
const PORT = Number(process.env.PORT || 3847);
const HOST = process.env.HOST || "0.0.0.0";
const DATA_DIR = path.join(__dirname, "data");

if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

app.use(express.json({ limit: "1mb" }));

// Allow opening/sharing from any origin (tunnel hosts, mobile browsers).
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  next();
});

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

function publicBaseUrl(req) {
  const fromEnv = (process.env.PUBLIC_BASE_URL || "").trim().replace(/\/$/, "");
  if (fromEnv) return fromEnv;
  const proto = req.get("x-forwarded-proto") || req.protocol || "http";
  const host = req.get("x-forwarded-host") || req.get("host");
  return `${proto}://${host}`;
}

app.get("/api/info", (req, res) => {
  res.json({
    port: PORT,
    host: HOST,
    publicBaseUrl: publicBaseUrl(req),
  });
});

app.post("/api/sessions", (req, res) => {
  const requestedId = typeof req.body?.id === "string" ? req.body.id.trim().slice(0, 32) : "";
  const id = requestedId || uuidv4().slice(0, 8);
  const title = (req.body?.title || "Neue Testrunde").trim().slice(0, 120);
  const existing = readSession(id);
  const session = existing || defaultSession(id, title);
  if (!existing) writeSession(session);
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
  const { title, entries, createdAt, upsert } = req.body || {};

  if (!existing && !upsert) {
    return res.status(404).json({ error: "Session nicht gefunden" });
  }

  const base = existing || defaultSession(req.params.id, "Neue Testrunde");
  const session = {
    ...base,
    title: typeof title === "string" ? title.trim().slice(0, 120) : base.title,
    entries: Array.isArray(entries) ? entries : base.entries,
    createdAt: createdAt || base.createdAt,
    updatedAt: new Date().toISOString(),
  };

  writeSession(session);
  res.json(session);
});

app.get("*", (_req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

const server = app.listen(PORT, HOST, () => {
  console.log(`Restauranttester läuft auf http://${HOST}:${PORT}`);
  if (process.env.PUBLIC_BASE_URL) {
    console.log(`Öffentliche URL: ${process.env.PUBLIC_BASE_URL}`);
  }
});

server.on("error", (err) => {
  console.error("Serverfehler:", err.message);
  process.exit(1);
});
