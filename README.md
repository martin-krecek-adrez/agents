# Agent Configuration

Configuration for Codex/Codex CLI usage in the Adrez workspace.

## Setup

### [Codex](https://developers.openai.com/codex)

Sync the managed setup:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh
```

Refresh the managed QMD index:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/qmd_refresh.sh
```

Run setup checks:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/check_ai_setup.sh
```

See [Skills](https://developers.openai.com/codex/skills) and [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) for details.

## Routing Summary

Main routing is defined in `AGENTS.md`.

- Default workspace scope: `/Users/martin/Documents/adrez`
- Default repo routing:
  - `dbt-cloud` for dbt models/finance/Snowflake analytics work
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
  - Snowflake-related requests -> `snowcli`
  - Asana updates/comments -> `asana`
  - Commit message drafting -> `write-commit`
  - Documentation requests -> `write-docs`
  - Tech comparisons -> `compare-tech`
  - End-to-end spreadsheet onboarding -> `entity-spreadsheet-ingestion`
  - Add/update spreadsheet entity -> `entity-extractor-spreadsheets`
  - Add/update external-table entity -> `entity-data-factory`
  - Add/update dbt entity/model -> `entity-dbt-cloud`
  - New Power BI report/model scaffold -> `powerbi-report-starter`
  - Rebuild/export Avalanche metadata -> `avalanche-metadata-update`

## Skills

Business skills live in:
- `/Users/martin/Documents/adrez/agents/skills`

Personal skills live in:
- `/Users/martin/Documents/live/agent/skills`

Use `scripts/sync_codex_setup.sh` to sync both sets into `~/.codex/skills`.

Current business skills:
- asana
- compare-tech
- qmd
- avalanche-metadata-update
- entity-dbt-cloud
- entity-data-factory
- entity-extractor-spreadsheets
- entity-spreadsheet-ingestion
- powerbi-report-starter
- snowcli
- write-commit
- write-docs

## Credits

- michalvavra for the original structure
