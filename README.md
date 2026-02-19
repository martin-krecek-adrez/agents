# Agent Configuration

Configuration for Codex CLI usage.

## Setup

### [Codex](https://developers.openai.com/codex)

Copy skills (Codex [ignores symlinked directories](https://developers.openai.com/codex/skills/create-skill#skill-doesnt-appear))

```bash
ln -sf {baseDir}/AGENTS.md ~/.codex/AGENTS.md
cp -r {baseDir}/skills/ ~/.codex/skills/
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
- Skill routing highlights:
  - Snowflake-related requests -> `snowcli`
  - Asana updates/comments -> `asana`
  - Commit message drafting -> `write-commit`
  - Documentation requests -> `write-docs`
  - Tech comparisons -> `compare-tech`
  - Multi-session memory workflows -> `beads`
  - Add/update spreadsheet entity -> `entity-extractor-spreadsheets`
  - Add/update external-table entity -> `entity-data-factory`
  - Add/update dbt entity/model -> `entity-dbt-cloud`
  - Broad Snowflake investigations -> `snowflake-analysis-playbook` (in progress)

## Skills

This repo keeps a focused set of skills.

Current skills:
- asana
- beads
- compare-tech
- qmd
- entity-dbt-cloud
- entity-data-factory
- entity-extractor-spreadsheets
- rohlik-grocery
- snowflake-analysis-playbook
- snowcli
- write-commit
- write-docs

## Credits

- michalvavra for the original structure
