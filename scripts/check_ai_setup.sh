#!/usr/bin/env bash
set -euo pipefail

failures=0
warnings=0

ok() {
  echo "[OK] $1"
}

warn() {
  echo "[WARN] $1" >&2
  warnings=$((warnings + 1))
}

fail() {
  echo "[FAIL] $1" >&2
  failures=$((failures + 1))
}

ROOT_AGENTS="/Users/martin/Documents/adrez/AGENTS.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
AGENTS_REPO="$(cd "${SCRIPT_DIR}/.." && pwd -P)"
SKILLS_DIR="${AGENTS_REPO}/skills"
README_PATH="${AGENTS_REPO}/README.md"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
PERSONAL_SKILLS_DIR="${PERSONAL_SKILLS_DIR:-/Users/martin/Documents/live/agent/skills}"
MAX_AGENTS_WARN_BYTES=8000
MAX_AGENTS_FAIL_BYTES=12000
MAX_SKILL_REVIEW_AGE_DAYS=90
AGENTS_SCOPE_LISTER="${SCRIPT_DIR}/list_managed_agents.py"

if managed_agents="$(python3 "${AGENTS_SCOPE_LISTER}" /Users/martin/Documents/adrez)"; then
  :
else
  fail "Could not resolve the managed AGENTS.md scope"
  managed_agents=""
fi

if [ -L "${CODEX_HOME}/AGENTS.md" ] && [ "$(readlink "${CODEX_HOME}/AGENTS.md")" = "${ROOT_AGENTS}" ]; then
  ok "~/.codex/AGENTS.md points to the Adrez workspace bootstrap"
else
  fail "~/.codex/AGENTS.md does not point to ${ROOT_AGENTS}"
fi

style_hits="$(
  rg -Hn "Zaruba|Voracek|NHL commentators|hockey game \"Czechia vs Canada\"" \
    /Users/martin/AGENTS.md 2>/dev/null || true
  rg -Hn "Zaruba|Voracek|NHL commentators|hockey game \"Czechia vs Canada\"" \
    /Users/martin/Documents/live/agent -g 'AGENTS.md' 2>/dev/null || true
  while IFS= read -r agents_file; do
    [ -n "${agents_file}" ] || continue
    rg -Hn "Zaruba|Voracek|NHL commentators|hockey game \"Czechia vs Canada\"" \
      "${agents_file}" 2>/dev/null || true
  done <<< "${managed_agents}"
)"

if [ -z "${style_hits}" ]; then
  ok "No banned hockey-style phrasing remains in AGENTS.md files"
else
  fail "Banned hockey-style phrasing still exists:\n${style_hits}"
fi

required_agents=(
  "/Users/martin/Documents/adrez/AGENTS.md"
  "${AGENTS_REPO}/AGENTS.md"
  "/Users/martin/Documents/adrez/dbt-cloud/AGENTS.md"
  "/Users/martin/Documents/adrez/data-factory/AGENTS.md"
  "/Users/martin/Documents/adrez/extractor-spreadsheets/AGENTS.md"
  "/Users/martin/Documents/adrez/data-platform/AGENTS.md"
  "/Users/martin/Documents/adrez/metadata-builder/AGENTS.md"
  "/Users/martin/Documents/adrez/avalanche-mcp/AGENTS.md"
  "/Users/martin/Documents/adrez/docs/AGENTS.md"
  "/Users/martin/Documents/adrez/powerbi/AGENTS.md"
  "/Users/martin/Documents/adrez/reporting/AGENTS.md"
)

for agents_file in "${required_agents[@]}"; do
  if [ -f "${agents_file}" ]; then
    ok "Required AGENTS.md exists: ${agents_file}"
  else
    fail "Missing required AGENTS.md: ${agents_file}"
  fi
done

while IFS= read -r agents_file; do
  [ -n "${agents_file}" ] || continue
  size_bytes="$(wc -c < "${agents_file}" | tr -d ' ')"
  if [ "${size_bytes}" -gt "${MAX_AGENTS_FAIL_BYTES}" ]; then
    fail "AGENTS.md exceeds ${MAX_AGENTS_FAIL_BYTES} bytes (${size_bytes}): ${agents_file}"
  elif [ "${size_bytes}" -gt "${MAX_AGENTS_WARN_BYTES}" ]; then
    warn "AGENTS.md exceeds ${MAX_AGENTS_WARN_BYTES} bytes (${size_bytes}): ${agents_file}"
  fi
done <<< "${managed_agents}"

if grep -q "/Users/martin/Documents/adrez/docs/data-platform" /Users/martin/Documents/adrez/dbt-cloud/AGENTS.md; then
  ok "dbt-cloud AGENTS.md routes durable data-platform docs"
else
  fail "dbt-cloud AGENTS.md does not route agents to /Users/martin/Documents/adrez/docs/data-platform"
fi

if grep -q "dedicated task branch" "${AGENTS_REPO}/AGENTS.md" \
  && grep -q "dedicated task branch" /Users/martin/Documents/adrez/dbt-cloud/AGENTS.md; then
  ok "Dedicated branch defaults are explicit in shared and dbt-cloud guidance"
else
  fail "Dedicated branch defaults are missing from shared or dbt-cloud guidance"
fi

if grep -q "Branches are delivery units; worktrees are concurrency units" "${AGENTS_REPO}/AGENTS.md" \
  && grep -q "repo-worktree-safety" "${AGENTS_REPO}/AGENTS.md"; then
  ok "Concurrent same-repo worktree policy is explicit in shared git guidance"
else
  fail "Concurrent same-repo worktree policy is missing from shared git guidance"
fi

if grep -q "This repository is Martin's local control hub" "${README_PATH}" \
  && grep -q "Team members must not run this" "${README_PATH}" \
  && grep -q "repository's sync" "${README_PATH}" \
  && grep -q "adrez-com/tech-plugins/README.md" "${README_PATH}"; then
  ok "agents README marks the sync as Martin-only and routes team onboarding"
else
  fail "agents README is missing the Martin-only or team-plugin onboarding boundary"
fi

if rg -n "commission-tier-monitoring" "${AGENTS_REPO}/ops" >/dev/null 2>&1; then
  fail "Active agents ops state must not route work to commission-tier-monitoring"
else
  ok "Active agents ops state excludes commission-tier-monitoring"
fi

ownership_args=(--check-runtime)
if [ -n "${ADREZ_TECH_PLUGINS_ROOT:-}" ]; then
  ownership_args+=(--require-plugin-source)
fi
if bash "${SCRIPT_DIR}/check_skill_ownership.sh" "${ownership_args[@]}"; then
  ok "Plugin runtime is complete and skill ownership is disjoint"
else
  fail "Plugin runtime or skill ownership check failed"
fi

if grep -q "Never use \`git stash\`, \`git reset\`, \`git checkout --\`, \`git clean\`" "${AGENTS_REPO}/AGENTS.md"; then
  ok "No implicit stash/reset/checkout/clean rule is explicit"
else
  fail "No implicit stash/reset/checkout/clean rule is missing from git guidance"
fi

if grep -q "GitHub connector \`404\` can mean connector scope" "${AGENTS_REPO}/AGENTS.md"; then
  ok "GitHub connector 404 and sandbox gh fallback guidance is explicit"
else
  fail "GitHub connector 404 and sandbox gh fallback guidance is missing"
fi

if grep -q "Asana is retired" "${AGENTS_REPO}/AGENTS.md" \
  && grep -q "Do not query Asana in routine briefs" "${AGENTS_REPO}/ops/README.md" \
  && grep -q "create one only with explicit Martin" "${AGENTS_REPO}/ops/README.md" \
  && grep -q "Never change assignee, title, due/start dates, notes" "${AGENTS_REPO}/skills/asana/SKILL.md" \
  && grep -q 'archival comment or `completed=true`' "${AGENTS_REPO}/skills/asana/SKILL.md" \
  && grep -q "create or update Linear only" "${AGENTS_REPO}/skills/asana/SKILL.md" \
  && grep -q "Linear is the only active Adrez task tracker" "${AGENTS_REPO}/ops/decisions.md"; then
  ok "Asana retirement and Linear-only active tracking are explicit"
else
  fail "Asana retirement policy is missing from shared or morning-brief guidance"
fi

if [ -d "${AGENTS_REPO}/feedback/inbox" ] \
  && [ -d "${AGENTS_REPO}/feedback/promoted" ] \
  && [ -d "${AGENTS_REPO}/feedback/rejected" ] \
  && [ -f "${AGENTS_REPO}/feedback/TEMPLATE.md" ] \
  && grep -q "sensitive_data_checked" "${AGENTS_REPO}/feedback/TEMPLATE.md" \
  && grep -q "agent-feedback-capture" "${AGENTS_REPO}/skills/ai-context-maintenance/SKILL.md" \
  && grep -q "feedback/inbox" "${AGENTS_REPO}/skills/agent-feedback-capture/SKILL.md"; then
  ok "Agent feedback inbox and capture workflow are configured"
else
  fail "Agent feedback inbox or capture workflow is missing"
fi

AVALANCHE_METADATA_SKILL="${AGENTS_REPO}/skills/avalanche-metadata-update/SKILL.md"
if grep -q -- "--product-key l2_base_output" "${AVALANCHE_METADATA_SKILL}" \
  && grep -q "profiles_output_ai/l2_base_output" "${AVALANCHE_METADATA_SKILL}" \
  && grep -q "mcp_metadata_bundle/catalog.json" "${AVALANCHE_METADATA_SKILL}" \
  && grep -q "mcp_metadata_bundle_ai/catalog_ai.json" "${AVALANCHE_METADATA_SKILL}" \
  && grep -q "scripts/run_ai_metadata_refresh.sh" "${AVALANCHE_METADATA_SKILL}" \
  && grep -q "npm run validate-catalog -- --file" "${AVALANCHE_METADATA_SKILL}" \
  && grep -q "rsync -ani --delete" "${AVALANCHE_METADATA_SKILL}"; then
  ok "Avalanche metadata skill uses product-scoped build, both catalogs, validation, and sync dry-run guidance"
else
  fail "Avalanche metadata skill is missing product-scoped build, both-catalog validation, or sync dry-run guidance"
fi

dbt_nested_agents=(
  "/Users/martin/Documents/adrez/dbt-cloud/models/l1_raw/AGENTS.md"
  "/Users/martin/Documents/adrez/dbt-cloud/models/l2_base/AGENTS.md"
  "/Users/martin/Documents/adrez/dbt-cloud/models/l2_base/base_input/AGENTS.md"
  "/Users/martin/Documents/adrez/dbt-cloud/models/l2_base/base/AGENTS.md"
  "/Users/martin/Documents/adrez/dbt-cloud/models/l2_base/base_output/AGENTS.md"
  "/Users/martin/Documents/adrez/dbt-cloud/models/l3_product/finance/AGENTS.md"
)

for agents_file in "${dbt_nested_agents[@]}"; do
  if [ -f "${agents_file}" ]; then
    ok "dbt-cloud nested AGENTS.md exists: ${agents_file}"
  else
    fail "Missing dbt-cloud nested AGENTS.md: ${agents_file}"
  fi
done

actual_skills="$(find "${SKILLS_DIR}" -mindepth 1 -maxdepth 1 -type d | while IFS= read -r dir; do
  if [ -f "${dir}/SKILL.md" ]; then
    basename "${dir}"
  fi
done | LC_ALL=C sort)"

readme_skills="$(awk '
  /^Current directly managed Adrez skills:/ { flag=1; next }
  flag && /^$/ { flag=0 }
  flag && /^- / { sub(/^- /, ""); print }
' "${README_PATH}" | LC_ALL=C sort)"

if [ "${actual_skills}" = "${readme_skills}" ]; then
  ok "agents/README.md skill list matches actual business skills"
else
  fail "agents/README.md skill list is out of sync with skills/ directory"
fi

inventory_skills="$(awk -F'\`' '/^\| `[^`]+` / { print $2 }' "${AGENTS_REPO}/ops/skills-inventory.md" | LC_ALL=C sort)"

if [ "${actual_skills}" = "${inventory_skills}" ]; then
  ok "skills inventory matches actual business skills"
else
  fail "skills inventory is out of sync with skills/ directory"
fi

while IFS= read -r skill_file; do
  [ -n "${skill_file}" ] || continue
  for field in name description status owner last_reviewed; do
    if ! grep -Eq "^${field}:" "${skill_file}"; then
      fail "Missing '${field}' in ${skill_file}"
    fi
  done

  last_reviewed="$(awk -F': *' '/^last_reviewed:/ { print $2; exit }' "${skill_file}")"
  if [ -n "${last_reviewed}" ]; then
    if reviewed_epoch="$(date -j -f "%Y-%m-%d" "${last_reviewed}" "+%s" 2>/dev/null)"; then
      now_epoch="$(date "+%s")"
      age_days="$(( (now_epoch - reviewed_epoch) / 86400 ))"
      if [ "${age_days}" -gt "${MAX_SKILL_REVIEW_AGE_DAYS}" ]; then
        warn "Skill last_reviewed is older than ${MAX_SKILL_REVIEW_AGE_DAYS} days (${age_days}): ${skill_file}"
      fi
    else
      fail "Invalid last_reviewed date in ${skill_file}: ${last_reviewed}"
    fi
  fi
done < <(find "${SKILLS_DIR}" -mindepth 2 -maxdepth 2 -name SKILL.md | LC_ALL=C sort)

if [ "${failures}" -eq 0 ]; then
  ok "All skill frontmatter includes required maintenance metadata"
fi

if python3 "${SCRIPT_DIR}/validate_business_skills.py" "${SKILLS_DIR}"; then
  ok "Business skill validator passed"
else
  fail "Business skill validator failed"
fi

if bash "${SCRIPT_DIR}/check_repo_hygiene.sh"; then
  ok "Repo hygiene validator passed"
else
  fail "Repo hygiene validator failed"
fi

if CODEX_HOME="${CODEX_HOME}" PERSONAL_SKILLS_DIR="${PERSONAL_SKILLS_DIR}" \
  python3 "${SCRIPT_DIR}/check_managed_skill_runtime.py"; then
  ok "All directly managed skills match source, manifest, and runtime"
else
  fail "Directly managed skill source/runtime check failed"
fi

if [ -e "${CODEX_HOME}/skills/qmd" ]; then
  fail "Retired managed skill still present in ~/.codex/skills: qmd"
else
  ok "Retired managed skill qmd is absent from ~/.codex/skills"
fi

if command -v qmd >/dev/null 2>&1; then
  fail "Retired qmd CLI is still installed or on PATH"
else
  ok "Retired qmd CLI is absent from PATH"
fi

if [ "${failures}" -gt 0 ]; then
  echo
  echo "AI setup check failed with ${failures} issue(s)." >&2
  exit 1
fi

if [ "${warnings}" -gt 0 ]; then
  echo
  echo "AI setup check passed with ${warnings} warning(s)."
  exit 0
fi

echo
echo "AI setup check passed."
