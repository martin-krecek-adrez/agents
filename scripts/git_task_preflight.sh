#!/usr/bin/env bash
set -euo pipefail

repo_path="${1:-.}"
expected_branch="${2:-}"

cd "${repo_path}"

repo_root="$(git rev-parse --show-toplevel)"
branch="$(git branch --show-current)"
status="$(git status --porcelain=v1)"

echo "repo_root=${repo_root}"
echo "branch=${branch}"
if upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null)"; then
  echo "upstream=${upstream}"
else
  echo "upstream="
fi

echo "status:"
git status -sb

if [ -n "${expected_branch}" ] && [ "${branch}" != "${expected_branch}" ]; then
  echo "ERROR: expected branch '${expected_branch}', got '${branch}'." >&2
  exit 2
fi

if [ -n "${status}" ]; then
  echo "WARN: worktree has dirty files. Confirm ownership before editing, switching, staging, committing, pulling, pushing, or opening a PR." >&2
  exit 3
fi

echo "preflight=ok"
