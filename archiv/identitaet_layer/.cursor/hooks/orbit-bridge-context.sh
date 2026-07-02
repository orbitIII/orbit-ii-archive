#!/usr/bin/env bash
# Session start: refresh bridge synthesis + inject Masterplan + Bridge context.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

python3 scripts/orbit_bridge_synthesis.py --markdown 2>/dev/null || true

echo "--- ORBIT Masterplan (Steuerung) ---"
if [[ -f docs/orbit_masterplan.md ]]; then
  sed -n '1,16p' docs/orbit_masterplan.md
  echo ""
  sed -n '/^## 8\./,/^## 9\./p' docs/orbit_masterplan.md | head -n 8
fi

echo ""
echo "--- Bridge Synthesis (Auszug) ---"
if [[ -f docs/orbit_bridge_synthesis_latest.md ]]; then
  sed -n '1,35p' docs/orbit_bridge_synthesis_latest.md
fi
