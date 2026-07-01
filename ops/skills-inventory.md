# Skills Inventory

Last reviewed: 2026-07-01

## Model

- Runtime skills are installed in `/Users/martin/.codex/skills`.
- Adrez business source of truth is `/Users/martin/Documents/adrez/agents/skills`.
- Personal/life source of truth is `/Users/martin/Documents/live/agent/skills`.
- Sync is managed by `/Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh`.
- Do not maintain normal working skills only in `~/.codex/skills`; promote them to a source-of-truth folder first.

## Current Decision

- This inventory focuses on Adrez business skills.
- Personal skills are intentionally out of scope for quality review.
- `playwright` is not an Adrez business skill. It overlaps with the Browser Use plugin for local browser work, but it is not the same thing: Browser Use is the in-app browser plugin; `playwright` is a terminal/browser automation skill with bundled CLI workflow. Keep it as personal utility unless it causes trigger noise.

## Business Skills

| Skill | Verdict | Notes | Next Action |
| --- | --- | --- | --- |
| `adrez-agent-orchestration` | keep | New light intake/orchestration layer for deciding tiny/small/tracked/parallel/project thread shape, local vs tracked work, and explicitly authorized subagent roles. Distinct from Linear tracking, implementation review, and repo/domain execution skills. | Forward-test on the next real multi-agent/thread-intake request; tighten trigger if it fires too broadly. |
| `adrez-linear-workflow` | keep | Correctly promoted to business source. Linear is the only default tool for new Adrez task planning/tracking. Long body, but useful because Linear object decisions are fragile. | Consider moving templates to `references/` if it grows. |
| `agent-feedback-capture` | keep | Clear raw-feedback capture skill. Distinct from `ai-context-maintenance`, which triages/promotes. | No immediate change. |
| `ai-context-maintenance` | keep | Correct owner for AGENTS.md, skills, task memory, stale context, setup checks, and inventory-based skill audits. | No immediate change. |
| `asana` | keep | Legacy Asana archive/context workflow only: read historical context, finish/update existing old tasks, or comment on existing Asana URLs/GIDs. No new Asana tasks/subtasks. | No immediate change. |
| `avalanche-metadata-update` | keep | Focused product-scoped metadata workflow for both Avalanche catalogs: `catalog.json` and `catalog_ai.json`. | No immediate change. |
| `compare-tech` | keep | Generic but useful. Low overlap. | No immediate change. |
| `entity-data-factory` | keep | Execution skill for already-landed ADLS/lake/raw sources and Snowflake exposure only. Uses data-factory local wrapper and treats `CONFIG_PATHS` as an override check, not a default edit. | No immediate change. |
| `entity-dbt-cloud` | keep | Focused dbt entity entrypoint skill. | No immediate change. |
| `entity-extractor-spreadsheets` | keep | Execution skill for SharePoint/OneDrive Excel/input sheet/mapping landing only: `ingest_config.yml` and ADLS validation. | No immediate change. |
| `entity-spreadsheet-ingestion` | keep | Orchestrator across extractor + data-factory for unscoped or end-to-end requests such as "pridej input sheet", "napoj tenhle Excel", or "dostan tenhle SharePoint/OneDrive soubor do Snowflake". | No merge. Keep as orchestrator; keep subskills for limited-scope requests. |
| `grill-me` | keep | Business decision-quality skill. Correct source is Adrez and it is wired in `agents/AGENTS.md`. | Keep minimal. Do not expand unless repeated usage shows missing behavior. |
| `implementation-review` | keep | Standalone review gate for implementation diffs, milestones, branches, and PR-ready work. Report-first, no-edit default; can use focused subagents for non-trivial work. | No immediate change. |
| `powerbi-report-starter` | keep | Focused scaffold workflow. | No immediate change. |
| `repo-pr-handoff` | keep | Delivery orchestration skill for commit, push, PR, PR/CI check, merge, and task handoff. Detailed GitHub fallback and PR template live in `references/delivery-details.md`; standalone review belongs to `implementation-review`. | No immediate change. |
| `repo-worktree-safety` | keep | Safety preflight for branch/worktree/scope/dirty-file confusion. Distinct from PR handoff delivery workflow. | No immediate change. |
| `snowcli` | keep | Tool-specific skill. | No immediate change. |
| `write-commit` | keep | Narrow and useful. | No immediate change. |
| `write-docs` | keep | Ordinary Adrez docs writing skill with explicit boundary: use `ai-context-maintenance` for AGENTS.md, skills, task-memory routing, and Codex setup audits. | No immediate change. |

## Consolidation Findings

- Do not merge the spreadsheet skills. The current pattern is correct:
  - `entity-spreadsheet-ingestion` orchestrates end-to-end work.
  - `entity-extractor-spreadsheets` handles OneDrive/SharePoint landing only.
  - `entity-data-factory` handles already-landed ADLS/Snowflake exposure.
- Do not merge `implementation-review`, `repo-pr-handoff`, `repo-worktree-safety`, and `write-commit`.
  - `implementation-review` is a report-first review gate.
  - `repo-worktree-safety` is a safety preflight.
  - `write-commit` is message construction.
  - `repo-pr-handoff` is delivery orchestration.
- Keep `adrez-agent-orchestration` as the thin intake layer above existing execution skills:
  - It classifies thread shape and delegation mode.
  - It hands tracking decisions to `adrez-linear-workflow`.
  - It hands review gates to `implementation-review`.
  - It hands implementation/delivery to repo/domain skills.
- Do not merge `agent-feedback-capture` and `ai-context-maintenance`.
  - Capture stores raw evidence.
  - Maintenance triages/promotes stable lessons.
- Keep `asana` and `adrez-linear-workflow` separate:
  - Asana: dead for new tasks; use only for existing legacy Asana URLs/GIDs, historical context, and comments/updates on old tasks.
  - Linear: all new Adrez planning/tracking, projects/issues/updates.

## Priority Edits

1. Consider trimming `repo-pr-handoff` after current dirty `agents/AGENTS.md` work is settled, because shared git policy and `implementation-review` now carry some adjacent detail.
2. Decide later whether `playwright` should remain a personal utility skill. Do not remove it from runtime until there is evidence that Browser Use fully covers the terminal automation use cases.
3. Forward-test `adrez-agent-orchestration` on the next real orchestration request and tighten its trigger if it fires on ordinary implementation work.

## Health Checks

Current checks to run after source or sync changes:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh
bash /Users/martin/Documents/adrez/agents/scripts/check_ai_setup.sh
bash /Users/martin/Documents/live/agent/scripts/check_personal_setup.sh
```
