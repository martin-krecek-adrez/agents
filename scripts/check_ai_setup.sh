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
AGENTS_REPO="/Users/martin/Documents/adrez/agents"
SKILLS_DIR="${AGENTS_REPO}/skills"
README_PATH="${AGENTS_REPO}/README.md"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
MAX_AGENTS_WARN_BYTES=8000
MAX_AGENTS_FAIL_BYTES=12000
MAX_SKILL_REVIEW_AGE_DAYS=90

if [ -L "${CODEX_HOME}/AGENTS.md" ] && [ "$(readlink "${CODEX_HOME}/AGENTS.md")" = "${ROOT_AGENTS}" ]; then
  ok "~/.codex/AGENTS.md points to the Adrez workspace bootstrap"
else
  fail "~/.codex/AGENTS.md does not point to ${ROOT_AGENTS}"
fi

style_hits="$(rg -n "Zaruba|Voracek|NHL commentators|hockey game \"Czechia vs Canada\"" \
  /Users/martin/AGENTS.md \
  /Users/martin/Documents/adrez \
  /Users/martin/Documents/live/agent \
  -g 'AGENTS.md' \
  -g '!adrez-tools/**' 2>/dev/null || true)"

if [ -z "${style_hits}" ]; then
  ok "No banned hockey-style phrasing remains in AGENTS.md files"
else
  fail "Banned hockey-style phrasing still exists:\n${style_hits}"
fi

required_agents=(
  "/Users/martin/Documents/adrez/AGENTS.md"
  "/Users/martin/Documents/adrez/agents/AGENTS.md"
  "/Users/martin/Documents/adrez/dbt-cloud/AGENTS.md"
  "/Users/martin/Documents/adrez/data-factory/AGENTS.md"
  "/Users/martin/Documents/adrez/extractor-documents/AGENTS.md"
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
done < <(find /Users/martin/Documents/adrez -name AGENTS.md \
  -not -path '*/old/*' \
  -not -path '*/adrez-tools/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  | LC_ALL=C sort)

if grep -q "/Users/martin/Documents/adrez/docs/data-platform" /Users/martin/Documents/adrez/dbt-cloud/AGENTS.md; then
  ok "dbt-cloud AGENTS.md routes durable data-platform docs"
else
  fail "dbt-cloud AGENTS.md does not route agents to /Users/martin/Documents/adrez/docs/data-platform"
fi

if grep -q "dedicated task branch" /Users/martin/Documents/adrez/agents/AGENTS.md \
  && grep -q "make changes in <repo> and push it" /Users/martin/Documents/adrez/agents/skills/repo-pr-handoff/SKILL.md \
  && grep -q "dedicated task branch" /Users/martin/Documents/adrez/dbt-cloud/AGENTS.md; then
  ok "Dedicated branch defaults are explicit in shared and dbt-cloud guidance"
else
  fail "Dedicated branch defaults are missing from shared, repo-pr-handoff, or dbt-cloud guidance"
fi

if grep -q "Branches are delivery units; worktrees are concurrency units" /Users/martin/Documents/adrez/agents/AGENTS.md \
  && grep -q "repo-worktree-safety" /Users/martin/Documents/adrez/agents/AGENTS.md \
  && grep -q "git worktree per task branch" /Users/martin/Documents/adrez/agents/skills/repo-pr-handoff/SKILL.md \
  && grep -q "One task = one branch = one git worktree = one agent" /Users/martin/Documents/adrez/agents/skills/repo-worktree-safety/SKILL.md; then
  ok "Concurrent same-repo worktree policy is explicit in shared git guidance"
else
  fail "Concurrent same-repo worktree policy is missing from shared git guidance"
fi

if grep -q "git_task_preflight.sh" /Users/martin/Documents/adrez/agents/skills/repo-worktree-safety/SKILL.md \
  && grep -q "create_task_worktree.sh" /Users/martin/Documents/adrez/agents/skills/repo-worktree-safety/SKILL.md \
  && [ -x /Users/martin/Documents/adrez/agents/scripts/git_task_preflight.sh ] \
  && [ -x /Users/martin/Documents/adrez/agents/scripts/create_task_worktree.sh ] \
  && [ -x /Users/martin/Documents/adrez/agents/scripts/pr_handoff_check.sh ]; then
  ok "Git worktree safety helper scripts are documented and executable"
else
  fail "Git worktree safety helper scripts are missing, undocumented, or not executable"
fi

if grep -q "Never use \`git stash\`, \`git reset\`, \`git checkout --\`, \`git clean\`" /Users/martin/Documents/adrez/agents/AGENTS.md \
  && grep -q "Do not use \`git stash\`, \`git reset\`, \`git checkout --\`, \`git clean\`" /Users/martin/Documents/adrez/agents/skills/repo-pr-handoff/SKILL.md \
  && grep -q "Do not use \`git stash\`, \`git reset\`, \`git checkout --\`, \`git clean\`" /Users/martin/Documents/adrez/agents/skills/repo-worktree-safety/SKILL.md; then
  ok "No implicit stash/reset/checkout/clean rule is explicit"
else
  fail "No implicit stash/reset/checkout/clean rule is missing from git guidance"
fi

if grep -q "GitHub connector \`404\` can mean connector scope" /Users/martin/Documents/adrez/agents/AGENTS.md \
  && grep -q "try \`gh repo view <owner>/<repo>\`" /Users/martin/Documents/adrez/agents/skills/repo-pr-handoff/SKILL.md \
  && grep -q "retry the same narrow \`gh\` command with \`require_escalated\`" /Users/martin/Documents/adrez/agents/skills/repo-pr-handoff/SKILL.md; then
  ok "GitHub connector 404 and sandbox gh fallback guidance is explicit"
else
  fail "GitHub connector 404 and sandbox gh fallback guidance is missing"
fi

if [ -d /Users/martin/Documents/adrez/agents/feedback/inbox ] \
  && [ -d /Users/martin/Documents/adrez/agents/feedback/promoted ] \
  && [ -d /Users/martin/Documents/adrez/agents/feedback/rejected ] \
  && [ -f /Users/martin/Documents/adrez/agents/feedback/TEMPLATE.md ] \
  && grep -q "sensitive_data_checked" /Users/martin/Documents/adrez/agents/feedback/TEMPLATE.md \
  && grep -q "agent-feedback-capture" /Users/martin/Documents/adrez/agents/skills/ai-context-maintenance/SKILL.md \
  && grep -q "feedback/inbox" /Users/martin/Documents/adrez/agents/skills/agent-feedback-capture/SKILL.md; then
  ok "Agent feedback inbox and capture workflow are configured"
else
  fail "Agent feedback inbox or capture workflow is missing"
fi

AVALANCHE_METADATA_SKILL="/Users/martin/Documents/adrez/agents/skills/avalanche-metadata-update/SKILL.md"
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
  /^Current business skills:/ { flag=1; next }
  flag && /^$/ { flag=0 }
  flag && /^- / { sub(/^- /, ""); print }
' "${README_PATH}" | LC_ALL=C sort)"

if [ "${actual_skills}" = "${readme_skills}" ]; then
  ok "agents/README.md skill list matches actual business skills"
else
  fail "agents/README.md skill list is out of sync with skills/ directory"
fi

inventory_skills="$(awk -F'\`' '/^\| `[^`]+` / { print $2 }' /Users/martin/Documents/adrez/agents/ops/skills-inventory.md | LC_ALL=C sort)"

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

while IFS= read -r skill_name; do
  [ -n "${skill_name}" ] || continue
  if [ -f "${CODEX_HOME}/skills/${skill_name}/SKILL.md" ]; then
    :
  else
    fail "Managed skill missing from ~/.codex/skills: ${skill_name}"
  fi

  if [ -f "${CODEX_HOME}/.managed-skills-manifest" ] && grep -Fxq "${skill_name}" "${CODEX_HOME}/.managed-skills-manifest"; then
    :
  else
    fail "Business skill missing from managed skills manifest: ${skill_name}"
  fi

  drift="$(rsync -ani --delete "${SKILLS_DIR}/${skill_name}/" "${CODEX_HOME}/skills/${skill_name}/" 2>/dev/null || true)"
  if [ -z "${drift}" ]; then
    :
  else
    fail "Runtime skill drift detected for ${skill_name}:\n${drift}"
  fi
done <<< "${actual_skills}"

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
