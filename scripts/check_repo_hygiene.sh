#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-/Users/martin/Documents/adrez}"

repos=(
  "agents"
  "dbt-cloud"
  "data-factory"
  "extractor-documents"
  "extractor-spreadsheets"
  "data-platform"
  "metadata-builder"
  "avalanche-mcp"
  "docs"
  "powerbi"
  "reporting"
)

failures=0
warnings=0
strict="${REPO_HYGIENE_STRICT:-0}"

is_junk_path() {
  case "$1" in
    .DS_Store|*/.DS_Store|Thumbs.db|*/Thumbs.db|desktop.ini|*/desktop.ini|.secrets/*|*/.secrets/*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

check_repo() {
  local repo_path="$1"
  local rel_path
  local tracked_junk=()
  local visible_untracked_junk=()

  [ -d "${repo_path}/.git" ] || [ -f "${repo_path}/.git" ] || return 0

  while IFS= read -r rel_path; do
    if is_junk_path "${rel_path}"; then
      tracked_junk+=("${rel_path}")
    fi
  done < <(git -C "${repo_path}" ls-files)

  while IFS= read -r rel_path; do
    if is_junk_path "${rel_path}"; then
      visible_untracked_junk+=("${rel_path}")
    fi
  done < <(git -C "${repo_path}" ls-files --others --exclude-standard)

  if [ "${#tracked_junk[@]}" -gt 0 ]; then
    if [ "${strict}" = "1" ]; then
      printf '[FAIL] %s tracks junk file(s):\n' "${repo_path}" >&2
      failures=$((failures + 1))
    else
      printf '[WARN] %s tracks junk file(s):\n' "${repo_path}" >&2
      warnings=$((warnings + 1))
    fi
    printf '  - %s\n' "${tracked_junk[@]}" >&2
  fi

  if [ "${#visible_untracked_junk[@]}" -gt 0 ]; then
    if [ "${strict}" = "1" ]; then
      printf '[FAIL] %s has unignored junk file(s):\n' "${repo_path}" >&2
      failures=$((failures + 1))
    else
      printf '[WARN] %s has unignored junk file(s):\n' "${repo_path}" >&2
      warnings=$((warnings + 1))
    fi
    printf '  - %s\n' "${visible_untracked_junk[@]}" >&2
  fi
}

for repo in "${repos[@]}"; do
  check_repo "${ROOT}/${repo}"
done

if [ "${failures}" -gt 0 ]; then
  echo "Repo hygiene check failed with ${failures} issue(s)." >&2
  exit 1
fi

if [ "${warnings}" -gt 0 ]; then
  echo "Repo hygiene check passed with ${warnings} warning(s)."
  exit 0
fi

echo "[OK] Repo hygiene check passed for ${#repos[@]} active repo(s)."
