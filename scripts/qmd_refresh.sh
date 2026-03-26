#!/usr/bin/env bash
set -euo pipefail

INDEX="${QMD_INDEX:-adrez}"
RUN_EMBED=1

if [ "${1-}" = "--no-embed" ]; then
  RUN_EMBED=0
  shift
fi

if [ "$#" -gt 0 ]; then
  echo "Usage: $0 [--no-embed]" >&2
  exit 1
fi

if ! command -v qmd >/dev/null 2>&1; then
  echo "qmd CLI is not installed or not on PATH." >&2
  exit 1
fi

has_collection() {
  local name="$1"
  qmd --index "${INDEX}" collection list 2>/dev/null | grep -Eq "^${name} "
}

ensure_collection() {
  local name="$1"
  local path="$2"
  local mask="$3"

  if [ ! -d "${path}" ]; then
    return 0
  fi

  if has_collection "${name}"; then
    qmd --index "${INDEX}" collection remove "${name}" >/dev/null
  fi

  qmd --index "${INDEX}" collection add "${path}" --name "${name}" --mask "${mask}" >/dev/null
}

remove_collection_if_exists() {
  local name="$1"
  if has_collection "${name}"; then
    qmd --index "${INDEX}" collection remove "${name}" >/dev/null
  fi
}

remove_collection_if_exists "ada_docs"
remove_collection_if_exists "sql_agent_docs"
remove_collection_if_exists "legacy_agent_docs"

ensure_collection "docs" "/Users/martin/Documents/adrez/docs" "**/*.md"
ensure_collection "dbt_docs" "/Users/martin/Documents/adrez/dbt-cloud/docs" "**/*.md"
ensure_collection "dbt_tasks" "/Users/martin/Documents/adrez/dbt-cloud/docs/tasks" "**/*.md"
ensure_collection "df_docs" "/Users/martin/Documents/adrez/data-factory/docs" "**/*.md"
ensure_collection "dp_docs" "/Users/martin/Documents/adrez/data-platform/docs" "**/*.md"
ensure_collection "es_docs" "/Users/martin/Documents/adrez/extractor-spreadsheets/docs" "**/*.md"
ensure_collection "mb_docs" "/Users/martin/Documents/adrez/metadata-builder/docs" "**/*.md"

qmd --index "${INDEX}" update

if [ "${RUN_EMBED}" -eq 1 ]; then
  qmd --index "${INDEX}" embed -f
fi

qmd --index "${INDEX}" status
