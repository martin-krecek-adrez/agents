# Skills Inventory

Last reviewed: 2026-08-24

## Ownership model

- `agents/skills` is the source of truth for Martin's Adrez operating,
  tracking, and AI-context skills.
- `adrez-com/tech-plugins/plugins/adrez-data-platform/skills` is the only source
  of truth for team data-platform and repository-delivery skills.
- The personal agent repository remains the source of truth for life skills.
- `scripts/sync_codex_setup.sh` copies only directly managed skills into
  `~/.codex/skills`.
- Codex installs and caches plugin skills separately. Never copy plugin skills
  manually into `~/.codex/skills`.
- The plugin's bundled `skill-inventory.txt` is the machine-readable ownership
  contract used from source and installed cache.

## Change routing

- Portable team data-platform or repository-delivery workflow: add or update
  the owning plugin in `tech-plugins`.
- Portable workflow for another team domain: use that domain's plugin rather
  than expanding `adrez-data-platform` without a clear fit.
- Martin-only Adrez operating, tracking, or context workflow: add or update
  `agents/skills`.
- Life-only workflow: add or update the personal agent repository.
- Runtime paths (`~/.codex/skills` and plugin caches) are outputs only.
- Promotion from a direct source to a plugin must use the source-aware cutover
  in `README.md`; never leave the same skill name in both sources.

## Directly managed skills

| Skill | Verdict | Notes | Next Action |
| --- | --- | --- | --- |
| `adrez-agent-orchestration` | keep | Personal intake layer above tracking and execution skills. It routes separate user-owned sidebar tasks to `adrez-thread-orchestration` and keeps internal subagent work distinct. | Forward-test the three-wave or six-agent stop and exact final-state reporting. |
| `adrez-thread-orchestration` | keep | Coordinates a bounded set of user-owned sidebar tasks under one MAIN task, with a compact registry and explicit lifecycle mandate. | Keep its sidebar-task boundary distinct from internal subagent orchestration. |
| `adrez-linear-workflow` | keep | Default Adrez Linear planning and updates, with a reviewed Data Engineering portfolio routing reference. | Keep the reference aligned with approved portfolio changes. |
| `agent-feedback-capture` | keep | Captures raw reusable harness feedback. | No change. |
| `ai-context-maintenance` | keep | Owns AGENTS, inventory, sync, and context governance. | Enforce plugin boundary. |
| `asana` | keep | Historical archive lookup only for explicit legacy URLs/GIDs. Never use it as an active queue or routine brief source. | Keep the trigger narrow and archive-only. |
| `avalanche-metadata-update` | keep | Product-specific metadata refresh remains outside plugin V1. | Reassess for plugin V1.1. |
| `compare-tech` | keep | Generic decision support. | No change. |
| `grill-me` | keep | Personal plan/design interview workflow. | No change. |
| `powerbi-report-starter` | keep | Product-specific scaffold remains outside plugin V1. | Reassess for plugin V1.1. |
| `write-commit` | keep | Generic commit-message wording. | No change. |

## Plugin-owned skills

The canonical names are defined only by
`plugins/adrez-data-platform/skill-inventory.txt` in `tech-plugins` and are
shipped in the installed cache. Do not copy that list into this repository.
The plugin owns each skill's `SKILL.md`, UI metadata, references, and bundled
helper scripts. Changes must be made in `tech-plugins`, validated there, and
released through the `Adrez Tech` marketplace.

## Stable boundaries

- Keep spreadsheet orchestration separate from extractor-only and
  data-factory-only execution.
- Keep implementation review, repository safety, and PR delivery as separate
  skills.
- Keep `adrez-agent-orchestration` in `agents`; it may route to plugin-provided
  skills by name but does not own their implementations.
- Keep `adrez-thread-orchestration` in `agents`; it owns Martin-specific Codex
  sidebar task lifecycle and must not move into the data-platform plugin.
- Keep `asana` and `adrez-linear-workflow` separate. Asana is an explicit
  historical archive lookup only; Linear owns all active planning and tracking.
- Keep Avalanche metadata and Power BI outside plugin V1 until explicitly
  promoted.

## Health checks

```bash
bash scripts/check_skill_ownership.sh --require-plugin-source
bash scripts/sync_codex_setup.sh --preflight-only
bash scripts/sync_codex_setup.sh
bash scripts/check_ai_setup.sh
```
