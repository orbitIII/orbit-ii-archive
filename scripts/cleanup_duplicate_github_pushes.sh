#!/usr/bin/env bash
# Close and delete duplicate Cursor automation pushes on GitHub.
# Requires: gh auth login (user token with pull-request write access).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

KEEP_REFS=(
  cursor/orbit-physics-prompt-0450
)

is_keep() {
  local ref="$1"
  for k in "${KEEP_REFS[@]}"; do
    [[ "$ref" == "$k" ]] && return 0
  done
  return 1
}

is_duplicate() {
  local ref="$1"
  is_keep "$ref" && return 1
  [[ "$ref" == cursor/bridge-synthese-* ]] && return 0
  [[ "$ref" == cursor/bc-* ]] && return 0
  return 1
}

echo "==> Scanning open cursor/* PRs"
mapfile -t rows < <(gh pr list --state open --limit 500 --json number,headRefName,title --jq '.[] | select(.headRefName | startswith("cursor/")) | "\(.number)\t\(.headRefName)\t\(.title)"')

duplicates=()
for row in "${rows[@]}"; do
  num="${row%%$'\t'*}"
  rest="${row#*$'\t'}"
  ref="${rest%%$'\t'*}"
  title="${rest#*$'\t'}"
  if is_duplicate "$ref"; then
    duplicates+=("$num|$ref|$title")
  fi
done

echo "Found ${#duplicates[@]} duplicate PR(s) to close."
for entry in "${duplicates[@]}"; do
  IFS='|' read -r num ref title <<< "$entry"
  echo "  #$num $ref — ${title:0:70}"
done

if [[ ${#duplicates[@]} -eq 0 ]]; then
  echo "Nothing to do."
  exit 0
fi

if [[ "$DRY_RUN" == true ]]; then
  echo "Dry run — no changes made."
  exit 0
fi

read -r -p "Close all ${#duplicates[@]} duplicate PRs and delete their branches? [y/N] " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 1
fi

closed=0
for entry in "${duplicates[@]}"; do
  IFS='|' read -r num ref _ <<< "$entry"
  gh pr close "$num" --delete-branch 2>/dev/null || gh pr close "$num" || true
  closed=$((closed + 1))
  echo "Closed #$num"
done

echo "Done. Closed $closed PR(s)."
