#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
  echo "Usage: $0 <repo-path> <task-slug> <branch-name> [base-ref]" >&2
  exit 64
fi

repo_path="$1"
task_slug="$2"
branch_name="$3"
base_ref="${4:-origin/main}"

repo_root="$(git -C "${repo_path}" rev-parse --show-toplevel)"
repo_name="$(basename "${repo_root}")"
worktree_path="/Users/martin/Documents/adrez/_worktrees/${repo_name}/${task_slug}"

if [ -e "${worktree_path}" ]; then
  echo "ERROR: worktree path already exists: ${worktree_path}" >&2
  echo "Use the existing worktree only if it belongs to the same task." >&2
  exit 2
fi

git -C "${repo_root}" fetch --prune
mkdir -p "$(dirname "${worktree_path}")"
git -C "${repo_root}" worktree add "${worktree_path}" -b "${branch_name}" "${base_ref}"

echo "worktree=${worktree_path}"
echo "branch=${branch_name}"
git -C "${worktree_path}" status -sb
