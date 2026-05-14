#!/usr/bin/env bash
set -euo pipefail

repo_path="${1:-.}"
expected_branch="${2:-}"

cd "${repo_path}"

/Users/martin/Documents/adrez/agents/scripts/git_task_preflight.sh . "${expected_branch}"

echo "recent_commits:"
git log --oneline --decorate --max-count=5

if command -v gh >/dev/null 2>&1; then
  branch="$(git branch --show-current)"
  echo "matching_prs:"
  gh pr list --head "${branch}" --state open --json number,title,isDraft,headRefName,headRefOid,url 2>/dev/null || true
else
  echo "WARN: gh is not on PATH; PR/CI checks must be completed another way." >&2
fi

echo "handoff_check=ok"
