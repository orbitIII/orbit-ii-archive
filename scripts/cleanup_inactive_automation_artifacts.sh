#!/usr/bin/env bash
# Cleanup artifacts from inactive Cursor automations.
# Run locally with full GitHub + Cursor access (cloud agent token cannot close PRs).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "==> Open draft PRs from automations"
gh pr list --state open --json number,title,headRefName,isDraft \
  | python3 -c "
import json, sys
prs = json.load(sys.stdin)
drafts = [p for p in prs if p.get('isDraft')]
print(f'Found {len(drafts)} open draft PRs')
for p in drafts[:10]:
    print(f\"  #{p['number']}: {p['headRefName']}\")
if len(drafts) > 10:
    print(f'  ... and {len(drafts) - 10} more')
"

read -r -p "Close all open draft PRs? [y/N] " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
  gh pr list --state open --json number --jq '.[].number' | while read -r n; do
    gh pr close "$n" || true
  done
fi

echo "==> Remote cursor/* branches"
mapfile -t branches < <(git ls-remote --heads origin 'cursor/*' | awk '{print $2}' | sed 's|refs/heads/||')
echo "Found ${#branches[@]} branches"

read -r -p "Delete all remote cursor/* branches? [y/N] " confirm2
if [[ "$confirm2" =~ ^[Yy]$ ]]; then
  for branch in "${branches[@]}"; do
    git push origin --delete "$branch" || true
  done
fi

cat <<'EOF'

==> Cursor automations (manual step)
There is no public API to delete automations. In the dashboard:
  https://cursor.com/automations

Delete or disable inactive automations, e.g.:
  - ORBIT Bridge — Best of Both Worlds (hourly cron)
  - ORBIT Prinzipien Research (daily)
  - Orbit II Archive / Trend / Contrarian agents (see docs/automation_plan.md)

Repo hook removed: .cursor/hooks.json (sessionStart bridge synthesis).
EOF
