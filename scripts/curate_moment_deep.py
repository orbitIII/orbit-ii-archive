#!/usr/bin/env python3
"""Backward-compatible wrapper — use curate_to_ausgesortiert.py --slug …"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from curate_to_ausgesortiert import main

if __name__ == "__main__":
    raise SystemExit(main())
