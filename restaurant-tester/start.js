#!/usr/bin/env node
/**
 * Starts the Restauranttester app and (by default) a public tunnel
 * so the app is reachable even without local port forwarding.
 */
const { spawn } = require("child_process");
const path = require("path");

const PORT = process.env.PORT || "3847";
const HOST = process.env.HOST || "0.0.0.0";
const ENABLE_TUNNEL = process.env.ENABLE_TUNNEL !== "0";

let publicBaseUrl = (process.env.PUBLIC_BASE_URL || "").trim();
let serverProc = null;
let tunnelProc = null;
let shuttingDown = false;

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

function extractTunnelUrl(text) {
  const match = text.match(/https:\/\/[a-z0-9-]+\.loca\.lt/i)
    || text.match(/https:\/\/[a-z0-9-]+\.trycloudflare\.com/i)
    || text.match(/your url is:\s*(https:\/\/\S+)/i);
  return match ? (match[1] || match[0]).replace(/\/$/, "") : null;
}

let restartingServer = false;

function restartServerWithPublicUrl(url) {
  publicBaseUrl = url;
  console.log(`\nÖffentlicher Link: ${url}\n`);
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

function startLocaltunnel() {
  tunnelProc = spawn(
    "npx",
    ["--yes", "localtunnel", "--port", String(PORT), "--print-requests"],
    { env: process.env, stdio: ["ignore", "pipe", "pipe"] }
  );

  const handle = (buf) => {
    const text = buf.toString();
    process.stdout.write(text);
    if (!publicBaseUrl) {
      const url = extractTunnelUrl(text);
      if (url) restartServerWithPublicUrl(url);
    }
  };

  tunnelProc.stdout.on("data", handle);
  tunnelProc.stderr.on("data", handle);
  tunnelProc.on("exit", (code) => {
    if (!shuttingDown) {
      console.error(`Tunnel beendet (code ${code}). Neustart in 2s…`);
      setTimeout(startLocaltunnel, 2000);
    }
  });
}

function startCloudflared() {
  tunnelProc = spawn(
    "npx",
    ["--yes", "cloudflared", "tunnel", "--url", `http://127.0.0.1:${PORT}`],
    { env: process.env, stdio: ["ignore", "pipe", "pipe"] }
  );

  const handle = (buf) => {
    const text = buf.toString();
    process.stdout.write(text);
    if (!publicBaseUrl) {
      const url = extractTunnelUrl(text);
      if (url) restartServerWithPublicUrl(url);
    }
  };

  tunnelProc.stdout.on("data", handle);
  tunnelProc.stderr.on("data", handle);
  tunnelProc.on("exit", (code) => {
    if (!shuttingDown) {
      console.error(`cloudflared beendet (code ${code}). Fallback localtunnel…`);
      setTimeout(startLocaltunnel, 1000);
    }
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
  // Prefer Cloudflare quick tunnels; fall back to localtunnel on failure.
  startCloudflared();
} else {
  console.log("Tunnel deaktiviert (ENABLE_TUNNEL=0). Nur lokal erreichbar.");
}
