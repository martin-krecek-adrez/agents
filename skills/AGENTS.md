# AGENTS.md

## Purpose
Registry and maintenance rules for shared Adrez Codex skills.

## Scope Split
- Directly managed Adrez operating, tracking, context-maintenance, and
  out-of-plugin product skills live here.
- Team data-platform and repository-delivery skills live only in
  `adrez-com/tech-plugins/plugins/adrez-data-platform/skills`.
- Personal/life skills live outside Adrez in the personal agent repository.

Keep this folder free of names listed by the installed Adrez Data Platform
plugin's `skill-inventory.txt`.

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
- That sync owns only skills stored in this repository and the personal agent
  repository. It requires a verified plugin runtime but does not install plugin
  skills.
- Install plugin skills through the `Adrez Tech` marketplace. Never copy them
  manually into `~/.codex/skills`.

## Promotion Rule
- Keep repo-specific procedures in repo-local `AGENTS.md` until the workflow is stable and reused.
- Promote to a shared skill only when the procedure is repeated across tasks and benefits from reuse.
- For repeated multi-repo flows, prefer one orchestration skill plus smaller repo-specific skills for single-hop work.
