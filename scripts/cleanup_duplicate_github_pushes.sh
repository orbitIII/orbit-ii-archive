#!/usr/bin/env bash
# Close duplicate bridge-synthese automation PRs created within the last N days.
# Requires: gh auth login (user token with pull-request write access).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DRY_RUN=false
DAYS=5
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --days) DAYS="$2"; shift 2 ;;
    *) echo "Usage: $0 [--dry-run] [--days N]"; exit 1 ;;
  esac
done

CUTOFF_EPOCH=$(date -u -d "${DAYS} days ago" +%s)

is_recent_bridge_duplicate() {
  local ref="$1" created_at="$2"
  [[ "$ref" == cursor/bridge-synthese-* || "$ref" == cursor/bc-* ]] || return 1
  local created_epoch
  created_epoch=$(date -u -d "$created_at" +%s)
  (( created_epoch >= CUTOFF_EPOCH ))
}

echo "==> Scanning open cursor/* PRs (bridge duplicates from last ${DAYS} days only)"
mapfile -t rows < <(
  gh pr list --state open --limit 500 \
    --json number,headRefName,title,createdAt \
    --jq '.[] | select(.headRefName | startswith("cursor/")) | "\(.number)\t\(.headRefName)\t\(.createdAt)\t\(.title)"'
)

duplicates=()
for row in "${rows[@]}"; do
  num="${row%%$'\t'*}"
  rest="${row#*$'\t'}"
  ref="${rest%%$'\t'*}"
  rest2="${rest#*$'\t'}"
  created_at="${rest2%%$'\t'*}"
  title="${rest2#*$'\t'}"
  if is_recent_bridge_duplicate "$ref" "$created_at"; then
    duplicates+=("$num|$ref|$created_at|$title")
  fi
done

echo "Found ${#duplicates[@]} recent bridge duplicate PR(s)."
for entry in "${duplicates[@]}"; do
  IFS='|' read -r num ref created_at title <<< "$entry"
  echo "  #$num $ref (created $created_at) — ${title:0:70}"
done

if [[ ${#duplicates[@]} -eq 0 ]]; then
  echo "Nothing to do."
  exit 0
fi

if [[ "$DRY_RUN" == true ]]; then
  echo "Dry run — no changes made."
  exit 0
fi

read -r -p "Close all ${#duplicates[@]} recent bridge duplicate PRs? [y/N] " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 1
fi

closed=0
for entry in "${duplicates[@]}"; do
  IFS='|' read -r num ref _ _ <<< "$entry"
  gh pr close "$num" --delete-branch 2>/dev/null || gh pr close "$num" || true
  closed=$((closed + 1))
  echo "Closed #$num"
done

echo "Done. Closed $closed PR(s)."
