#!/usr/bin/env bash
set -euo pipefail

ADREZ_AGENTS_MD="/Users/martin/Documents/adrez/AGENTS.md"
BUSINESS_SKILLS_DIR="/Users/martin/Documents/adrez/agents/skills"
PERSONAL_SKILLS_DIR="/Users/martin/Documents/live/agent/skills"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
TARGET_SKILLS_DIR="${CODEX_HOME}/skills"
MANIFEST_PATH="${CODEX_HOME}/.managed-skills-manifest"

mkdir -p "${TARGET_SKILLS_DIR}"
ln -sfn "${ADREZ_AGENTS_MD}" "${CODEX_HOME}/AGENTS.md"

valid_skill_name() {
  [[ "$1" =~ ^[a-z0-9][a-z0-9._-]*$ ]]
}

contains_skill() {
  local needle="$1"
  shift
  local item
  for item in "$@"; do
    if [ "${item}" = "${needle}" ]; then
      return 0
    fi
  done
  return 1
}

declare -a current_managed=()
declare -a retired_skills=(
  "qmd"
)

copy_skill_dir() {
  local source_root="$1"
  [ -d "${source_root}" ] || return 0

  local skill_dir
  for skill_dir in "${source_root}"/*; do
    [ -d "${skill_dir}" ] || continue
    if [ ! -f "${skill_dir}/SKILL.md" ] && [ ! -f "${skill_dir}/SKILL.MD" ]; then
      continue
    fi

    local skill_name
    skill_name="$(basename "${skill_dir}")"
    if ! valid_skill_name "${skill_name}"; then
      echo "Invalid skill directory name: ${skill_name}" >&2
      exit 1
    fi
    if [ ${#current_managed[@]} -gt 0 ] && contains_skill "${skill_name}" "${current_managed[@]}"; then
      echo "Duplicate managed skill name across source roots: ${skill_name}" >&2
      exit 1
    fi
    current_managed+=("${skill_name}")
    rsync -a --delete "${skill_dir}/" "${TARGET_SKILLS_DIR}/${skill_name}/"
  done
}

copy_skill_dir "${BUSINESS_SKILLS_DIR}"
copy_skill_dir "${PERSONAL_SKILLS_DIR}"

declare -a previous_managed=()
if [ -f "${MANIFEST_PATH}" ]; then
  while IFS= read -r skill_name; do
    previous_managed+=("${skill_name}")
  done < "${MANIFEST_PATH}"
fi

if [ ${#previous_managed[@]} -gt 0 ]; then
  for skill_name in "${previous_managed[@]}"; do
    if ! valid_skill_name "${skill_name}"; then
      echo "Refusing invalid skill name from manifest: ${skill_name}" >&2
      exit 1
    fi
    if ! contains_skill "${skill_name}" "${current_managed[@]}"; then
      delete_path="${TARGET_SKILLS_DIR}/${skill_name}"
      case "${delete_path}" in
        "${TARGET_SKILLS_DIR}"/*) rm -rf "${delete_path}" ;;
        *) echo "Refusing to delete outside managed skills dir: ${delete_path}" >&2; exit 1 ;;
      esac
    fi
  done
fi

for skill_name in "${retired_skills[@]}"; do
  if ! valid_skill_name "${skill_name}"; then
    echo "Invalid retired skill name: ${skill_name}" >&2
    exit 1
  fi
  if ! contains_skill "${skill_name}" "${current_managed[@]}"; then
    rm -rf "${TARGET_SKILLS_DIR}/${skill_name}"
  fi
done

printf "%s\n" "${current_managed[@]}" | LC_ALL=C sort -u > "${MANIFEST_PATH}"

echo "Synced Codex setup:"
echo "- AGENTS.md -> ${CODEX_HOME}/AGENTS.md"
echo "- managed skills -> ${TARGET_SKILLS_DIR}"
