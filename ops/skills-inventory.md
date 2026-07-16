# Skills Inventory

Last reviewed: 2026-07-15

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

## Directly managed skills

| Skill | Verdict | Notes | Next Action |
| --- | --- | --- | --- |
| `adrez-agent-orchestration` | keep | Personal intake layer above tracking and execution skills. | Keep plugin skill references by name. |
| `adrez-linear-workflow` | keep | Default Adrez Linear planning and updates. | No change. |
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
