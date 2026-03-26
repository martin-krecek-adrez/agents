#!/usr/bin/env bash
set -euo pipefail

failures=0

ok() {
  echo "[OK] $1"
}

fail() {
  echo "[FAIL] $1" >&2
  failures=$((failures + 1))
}

ROOT_AGENTS="/Users/martin/Documents/adrez/AGENTS.md"
AGENTS_REPO="/Users/martin/Documents/adrez/agents"
SKILLS_DIR="${AGENTS_REPO}/skills"
README_PATH="${AGENTS_REPO}/README.md"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

if [ -L "${CODEX_HOME}/AGENTS.md" ] && [ "$(readlink "${CODEX_HOME}/AGENTS.md")" = "${ROOT_AGENTS}" ]; then
  ok "~/.codex/AGENTS.md points to the Adrez workspace bootstrap"
else
  fail "~/.codex/AGENTS.md does not point to ${ROOT_AGENTS}"
fi

style_hits="$(rg -n "Zaruba|Voracek|NHL commentators|hockey game \"Czechia vs Canada\"" \
  /Users/martin/AGENTS.md \
  /Users/martin/Documents/adrez \
  /Users/martin/Documents/live/agent \
  -g 'AGENTS.md' 2>/dev/null || true)"

if [ -z "${style_hits}" ]; then
  ok "No banned hockey-style phrasing remains in AGENTS.md files"
else
  fail "Banned hockey-style phrasing still exists:\n${style_hits}"
fi

actual_skills="$(find "${SKILLS_DIR}" -mindepth 1 -maxdepth 1 -type d | while IFS= read -r dir; do
  if [ -f "${dir}/SKILL.md" ]; then
    basename "${dir}"
  fi
done | LC_ALL=C sort)"

readme_skills="$(awk '
  /^Current business skills:/ { flag=1; next }
  flag && /^$/ { flag=0 }
  flag && /^- / { sub(/^- /, ""); print }
' "${README_PATH}" | LC_ALL=C sort)"

if [ "${actual_skills}" = "${readme_skills}" ]; then
  ok "agents/README.md skill list matches actual business skills"
else
  fail "agents/README.md skill list is out of sync with skills/ directory"
fi

while IFS= read -r skill_file; do
  [ -n "${skill_file}" ] || continue
  for field in name description status owner last_reviewed; do
    if ! grep -Eq "^${field}:" "${skill_file}"; then
      fail "Missing '${field}' in ${skill_file}"
    fi
  done
done < <(find "${SKILLS_DIR}" -mindepth 2 -maxdepth 2 -name SKILL.md | LC_ALL=C sort)

if [ "${failures}" -eq 0 ]; then
  ok "All skill frontmatter includes required maintenance metadata"
fi

while IFS= read -r skill_name; do
  [ -n "${skill_name}" ] || continue
  if [ -f "${CODEX_HOME}/skills/${skill_name}/SKILL.md" ]; then
    :
  else
    fail "Managed skill missing from ~/.codex/skills: ${skill_name}"
  fi
done <<< "${actual_skills}"

if command -v qmd >/dev/null 2>&1; then
  collection_list="$(qmd --index adrez collection list 2>/dev/null || true)"
  if echo "${collection_list}" | grep -q '^ada_docs '; then
    fail "Legacy qmd collection ada_docs is still present"
  else
    ok "Legacy qmd collection drift check passed"
  fi

  for name in docs dbt_docs dbt_tasks df_docs dp_docs es_docs mb_docs; do
    if echo "${collection_list}" | grep -q "^${name} "; then
      :
    else
      fail "Missing qmd collection: ${name}"
    fi
  done
else
  fail "qmd is not installed or not on PATH"
fi

if [ "${failures}" -gt 0 ]; then
  echo
  echo "AI setup check failed with ${failures} issue(s)." >&2
  exit 1
fi

echo
echo "AI setup check passed."
