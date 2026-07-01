# Agent Configuration

Configuration for Codex/Codex CLI usage in the Adrez workspace.

## Setup

### [Codex](https://developers.openai.com/codex)

Sync the managed setup:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh
```

Run setup checks:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/check_ai_setup.sh
```

`check_ai_setup.sh` also runs:
- `scripts/validate_business_skills.py` for Adrez skill metadata and UI prompts.
- `scripts/check_repo_hygiene.sh` for tracked junk files such as `.DS_Store`.

See [Skills](https://developers.openai.com/codex/skills) and [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) for details.

## Routing Summary

Main routing is defined in `AGENTS.md`.

- Default workspace scope: `/Users/martin/Documents/adrez`
- Default repo routing:
  - `dbt-cloud` for dbt models/finance/Snowflake analytics work
  - `extractor-documents` for PDF/document parsing into ADLS CSV outputs
  - `extractor-spreadsheets` first for new OneDrive/SharePoint spreadsheets and mapping sheets
  - `data-factory` for already-landed ADLS sources and external-table exposure
  - `data-platform` for shared platform/data tooling
  - `avalanche-mcp` for current MCP analytics / agent work
  - `metadata-builder` for Avalanche metadata/catalog build
  - `powerbi` for Power BI / Fabric work
- Legacy repos:
  - `adrez-data-assistant`
  - `adrez-metadata-sql-agent`
- Skill routing highlights:
  - Thread intake / agent orchestration -> `adrez-agent-orchestration`
  - Snowflake-related requests -> `snowcli`
  - Asana updates/comments -> `asana`
  - Commit message drafting -> `write-commit`
  - Documentation requests -> `write-docs`
  - Reusable harness/process feedback -> `agent-feedback-capture`
  - Tech comparisons -> `compare-tech`
  - Implementation diff/milestone review -> `implementation-review`
  - Parallel repo branches / dirty worktree safety -> `repo-worktree-safety`
  - End-to-end spreadsheet onboarding -> `entity-spreadsheet-ingestion`
  - Add/update spreadsheet entity -> `entity-extractor-spreadsheets`
  - Add/update external-table entity -> `entity-data-factory`
  - Add/update dbt entity/model -> `entity-dbt-cloud`
  - New Power BI report/model scaffold -> `powerbi-report-starter`
  - Rebuild/export Avalanche metadata -> `avalanche-metadata-update`

## Ops Memory

Cross-repo operating state for Codex coordination lives in:
- `/Users/martin/Documents/adrez/agents/ops`

Use it for Chief of Staff briefs, open loops, people follow-ups, pipeline watch
items, and thread handoff prompts. Keep repo implementation notes in repo-local
`docs/tasks/`.

## Skills

Business skills live in:
- `/Users/martin/Documents/adrez/agents/skills`

Personal skills live in:
- `/Users/martin/Documents/live/agent/skills`

Use `scripts/sync_codex_setup.sh` to sync both sets into `~/.codex/skills`.

Current business skills:
- adrez-agent-orchestration
- adrez-linear-workflow
- asana
- agent-feedback-capture
- ai-context-maintenance
- compare-tech
- avalanche-metadata-update
- entity-dbt-cloud
- entity-data-factory
- entity-extractor-spreadsheets
- entity-spreadsheet-ingestion
- grill-me
- implementation-review
- powerbi-report-starter
- repo-pr-handoff
- repo-worktree-safety
- snowcli
- write-commit
- write-docs

## Credits

- michalvavra for the original structure
