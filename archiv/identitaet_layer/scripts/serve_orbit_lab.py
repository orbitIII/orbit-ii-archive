#!/usr/bin/env python3
"""Serve ORBIT Lab test app + repo JSON from repository root."""

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = os.environ.get("ORBIT_LAB_HOST", "0.0.0.0")
PORT = int(os.environ.get("ORBIT_LAB_PORT", "8765"))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    os.chdir(ROOT)
    url = f"http://{HOST}:{PORT}/app/orbit-lab/"
    print(f"ORBIT Lab → {url}")
    print(f"Serving repo root: {ROOT}")
    print("Ctrl+C to stop")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
