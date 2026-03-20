# AGENTS.md

## Purpose
Registry and maintenance rules for shared Adrez Codex skills.

## Scope Split
- Business skills live here: `/Users/martin/Documents/adrez/agents/skills`
- Personal skills live outside Adrez: `/Users/martin/Documents/live/agent/skills`

Keep this folder business-only.

## Skill Structure
- One skill per folder.
- Each skill must include `SKILL.md`.
- Optional folders: `references/`, `scripts/`, `assets/`.
- Keep `SKILL.md` concise; move detail into `references/` when needed.

## Naming
- Folder names: lowercase + hyphen.
- Skill names should describe the action or workflow clearly.

## Sync
- Managed sync into `~/.codex/skills` runs through:
  - `/Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh`
- Do not rely on manual `cp -r` as the default workflow.

## Promotion Rule
- Keep repo-specific procedures in repo-local `AGENTS.md` until the workflow is stable and reused.
- Promote to a shared skill only when the procedure is repeated across tasks and benefits from reuse.
