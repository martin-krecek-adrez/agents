# Agent Configuration

Configuration for Codex CLI usage.

## Setup

### [Codex](https://developers.openai.com/codex)

Sync the managed setup:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh
```

See [Skills](https://developers.openai.com/codex/skills) and [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) for details.

## Routing Summary

Main routing is defined in `AGENTS.md`.

- Default workspace scope: `/Users/martin/Documents/adrez`
- Default repo routing:
  - `dbt-cloud` for dbt models/finance/Snowflake analytics work
  - `data-factory` for ingestion/orchestration pipelines
  - `data-platform` for shared platform/data tooling
  - `extractor-spreadsheets` for spreadsheet extractors/mappings
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
  - Add/update spreadsheet entity -> `entity-extractor-spreadsheets`
  - Add/update external-table entity -> `entity-data-factory`
  - Add/update dbt entity/model -> `entity-dbt-cloud`
  - Rebuild/export Avalanche metadata -> `avalanche-metadata-update`
  - Broad Snowflake investigations -> `snowflake-analysis-playbook` (in progress)

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
- snowflake-analysis-playbook
- snowcli
- write-commit
- write-docs

## Credits

- michalvavra for the original structure
