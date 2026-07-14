#!/usr/bin/env node
/**
 * Starts Restauranttester + a public tunnel (Pinggy, then localtunnel).
 * Cloudflare quick tunnels are intentionally avoided – they often fail for recipients.
 */
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const PORT = process.env.PORT || "3847";
const HOST = process.env.HOST || "0.0.0.0";
const ENABLE_TUNNEL = process.env.ENABLE_TUNNEL !== "0";
const URL_FILE = path.join(__dirname, "PUBLIC_URL.txt");

let publicBaseUrl = (process.env.PUBLIC_BASE_URL || "").trim();
let serverProc = null;
let tunnelProc = null;
let shuttingDown = false;
let restartingServer = false;
let tunnelMode = null;

function writePublicUrl(url) {
  try {
    fs.writeFileSync(URL_FILE, `${url}\n`);
  } catch {
    // ignore
  }
}

function startServer() {
  const env = {
    ...process.env,
    PORT,
    HOST,
    PUBLIC_BASE_URL: publicBaseUrl || process.env.PUBLIC_BASE_URL || "",
  };

  serverProc = spawn(process.execPath, [path.join(__dirname, "server.js")], {
    env,
    stdio: ["ignore", "pipe", "pipe"],
  });

  serverProc.stdout.on("data", (buf) => process.stdout.write(buf));
  serverProc.stderr.on("data", (buf) => process.stderr.write(buf));
  serverProc.on("exit", (code) => {
    if (!shuttingDown && !restartingServer) {
      console.error(`Server beendet (code ${code}). Neustart in 1s…`);
      setTimeout(startServer, 1000);
    }
  });
}

function extractUrl(text) {
  const patterns = [
    /https:\/\/[a-z0-9-]+\.free\.pinggy\.net/i,
    /https:\/\/[a-z0-9-.]+\.run\.pinggy-free\.link/i,
    /https:\/\/[a-z0-9-]+\.loca\.lt/i,
    /your url is:\s*(https:\/\/\S+)/i,
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (!match) continue;
    return (match[1] || match[0]).replace(/[).,]+$/, "").replace(/\/$/, "");
  }
  return null;
}

function applyPublicUrl(url) {
  if (!url || publicBaseUrl === url) return;
  publicBaseUrl = url;
  writePublicUrl(url);
  console.log(`\n========================================`);
  console.log(`TEILBARER LINK (zum Versenden):`);
  console.log(url);
  console.log(`========================================\n`);

  if (!serverProc) {
    startServer();
    return;
  }

  restartingServer = true;
  const old = serverProc;
  old.once("exit", () => {
    restartingServer = false;
    startServer();
  });
  old.kill("SIGTERM");
  setTimeout(() => {
    if (restartingServer) {
      try {
        old.kill("SIGKILL");
      } catch {
        // ignore
      }
    }
  }, 1500);
}

function attachTunnelLogs(proc) {
  const handle = (buf) => {
    const text = buf.toString();
    process.stdout.write(text);
    if (!publicBaseUrl) {
      const url = extractUrl(text);
      if (url) applyPublicUrl(url);
    }
  };
  proc.stdout.on("data", handle);
  proc.stderr.on("data", handle);
}

function startPinggy() {
  tunnelMode = "pinggy";
  console.log("Starte Pinggy-Tunnel…");
  tunnelProc = spawn(
    "ssh",
    [
      "-p",
      "443",
      "-o",
      "StrictHostKeyChecking=no",
      "-o",
      "ServerAliveInterval=30",
      "-o",
      "ServerAliveCountMax=3",
      "-o",
      "ExitOnForwardFailure=yes",
      "-R",
      `0:127.0.0.1:${PORT}`,
      "a.pinggy.io",
    ],
    { env: process.env, stdio: ["ignore", "pipe", "pipe"] }
  );
  attachTunnelLogs(tunnelProc);
  tunnelProc.on("exit", (code) => {
    if (shuttingDown) return;
    console.error(`Pinggy beendet (code ${code}). Fallback: localtunnel…`);
    publicBaseUrl = "";
    setTimeout(startLocaltunnel, 1000);
  });
}

function startLocaltunnel() {
  tunnelMode = "localtunnel";
  console.log("Starte localtunnel…");
  tunnelProc = spawn(
    "npx",
    ["--yes", "localtunnel", "--port", String(PORT)],
    { env: process.env, stdio: ["ignore", "pipe", "pipe"] }
  );
  attachTunnelLogs(tunnelProc);
  tunnelProc.on("exit", (code) => {
    if (shuttingDown) return;
    console.error(`localtunnel beendet (code ${code}). Retry Pinggy in 3s…`);
    publicBaseUrl = "";
    setTimeout(startPinggy, 3000);
  });
}

function shutdown() {
  shuttingDown = true;
  if (tunnelProc && !tunnelProc.killed) tunnelProc.kill("SIGTERM");
  if (serverProc && !serverProc.killed) serverProc.kill("SIGTERM");
  process.exit(0);
}

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

startServer();
if (ENABLE_TUNNEL) {
  // Prefer Pinggy over Cloudflare – more reliable for shared links.
  startPinggy();
} else {
  console.log("Tunnel deaktiviert (ENABLE_TUNNEL=0). Nur lokal erreichbar.");
}
