#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-/Users/martin/Documents/adrez}"
MIN_AGE_DAYS="${MIN_AGE_DAYS:-30}"
MAX_CANDIDATES="${MAX_CANDIDATES:-25}"

if ! command -v rg >/dev/null 2>&1; then
  echo "ripgrep is required for this report." >&2
  exit 1
fi

echo "Task note promotion candidates"
echo "Root: ${ROOT}"
echo "Minimum age: ${MIN_AGE_DAYS} days"
echo "Maximum candidates: ${MAX_CANDIDATES}"
echo

candidate_count=0

while IFS= read -r note; do
  matches="$(rg -n -i \
    "business rule|current state|operating rule|policy|canonical|source of truth|durable|decision|architecture|runbook|process|workflow|contract|semantic|definition" \
    "${note}" 2>/dev/null || true)"

  if [ -n "${matches}" ]; then
    candidate_count=$((candidate_count + 1))
    echo "## ${note}"
    echo "${matches}" | sed -n '1,8p'
    echo

    if [ "${candidate_count}" -ge "${MAX_CANDIDATES}" ]; then
      echo "Reached MAX_CANDIDATES=${MAX_CANDIDATES}; stop here for a reviewable report."
      echo
      break
    fi
  fi
done < <(find "${ROOT}" \
  \( -type d \( \
    -name 'commission-tier-monitoring' -o \
    -name 'old' -o \
    -name '_worktrees' -o \
    -name 'node_modules' -o \
    -name 'adrez-data-assistant' -o \
    -name 'adrez-metadata-sql-agent' -o \
    -name 'extractor-documents' \
  \) \) -prune -o \
  -path '*/docs/tasks/*.md' \
  -type f \
  -mtime +"${MIN_AGE_DAYS}" \
  -not -name 'TEMPLATE_TASK.md' \
  -print \
  | LC_ALL=C sort)

if [ "${candidate_count}" -eq 0 ]; then
  echo "No candidates found."
fi
