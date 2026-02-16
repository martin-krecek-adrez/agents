# AGENTS.md

## Purpose
Default control hub for Codex in Adrez. Keep this file routing-focused; repo-specific details belong to each repo `AGENTS.md`.

## Execution Order
Apply instructions in this order:
1. `/Users/martin/AGENTS.md`
2. `/Users/martin/Documents/adrez/agents/AGENTS.md`
3. Closest repo/subfolder `AGENTS.md`
If rules conflict, nearest repo `AGENTS.md` wins for repo-specific behavior.

## Workspace Scope
- Root: `/Users/martin/Documents/adrez`
- Do not inspect `/Users/martin/Documents/adrez/old` unless explicitly asked.

## Primary Repos
- `/Users/martin/Documents/adrez/dbt-cloud`
- `/Users/martin/Documents/adrez/data-factory`
- `/Users/martin/Documents/adrez/data-platform`
- `/Users/martin/Documents/adrez/extractor-spreadsheets`
- `/Users/martin/Documents/adrez/metadata-builder`
- `/Users/martin/Documents/adrez/adrez-data-assistant`
- `/Users/martin/Documents/adrez/docs`

## Repo Intent Map
- `dbt-cloud`: dbt models, tests, docs, Snowflake analytics debugging.
- `data-factory`: ingestion/orchestration and external-table/load config.
- `data-platform`: shared Snowflake/Terraform/platform tooling.
- `extractor-spreadsheets`: OneDrive spreadsheet extraction/mapping ingestion.
- `metadata-builder`: metadata profiling and YAML generation tools.
- `adrez-data-assistant`: business QA assistant app over Snowflake metadata.
- `docs`: VitePress documentation.

## Skill Intent Map
Use these skills when intent clearly matches:
- `snowcli`: connect/query/check Snowflake, run SQL.
- `asana`: update/comment in Asana tasks.
- `write-commit`: prepare commit message from actual diff.
- `write-docs`: write/update docs.
- `compare-tech`: compare tool options.
- `beads`: persistent multi-session task memory.
- `entity-extractor-spreadsheets`: add/update spreadsheet/mapping entities in extractor-spreadsheets.
- `entity-data-factory`: add/update external-table entities/configs in data-factory.
- `entity-dbt-cloud`: add/update dbt entities/models (default `l1_raw` first).
- `snowflake-analysis-playbook` (in progress): structured mode-based Snowflake analysis with mandatory scope clarification for broad asks.

## Snowflake Defaults
- For `snowcli` tasks, use locally configured Snow CLI/dbt context by default.
- If required context is missing or ambiguous, ask one short clarifying question.
- Always return executable SQL and prefer fully qualified names (`database.schema.table`).

## Routing Rules
- Decide target repo + skill before editing.
- If user says "check dbt", default to `/Users/martin/Documents/adrez/dbt-cloud`.
- If ambiguous across repos, ask one short clarifying question.

## Task Memory
- Track execution status in Asana.
- Keep durable technical context in repo task notes (for example `docs/tasks/` where available).
- Suggested task note naming: `YYYY-MM-DD-short-task-name.md`.
- Cross-link Asana <-> task note <-> changed model/code paths.

## Git Defaults
- Run `git status -sb` before edits.
- Pull with `--ff-only` by default.
- Do not push unless explicitly asked.
- Do not amend commits unless explicitly asked.

## Safety
- Do not run destructive commands unless explicitly asked.
- Ask before network/credentialed commands when required by local repo policy.
- Dry-run mode: if user says "describe only", "don't do it", or equivalent, do not run commands and do not edit files.
