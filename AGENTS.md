# AGENTS.md

## Purpose
Default control hub for Codex in Adrez. Keep this file routing-focused; repo-specific details belong to each repo `AGENTS.md`.

## Communication
- Respond in the user's language unless they explicitly ask otherwise.
- Prefer direct, neutral responses with minimal fluff.

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
- `/Users/martin/Documents/adrez/avalanche-mcp`
- `/Users/martin/Documents/adrez/powerbi`
- `/Users/martin/Documents/adrez/docs`

## Legacy Repos
- `/Users/martin/Documents/adrez/adrez-data-assistant`
- `/Users/martin/Documents/adrez/adrez-metadata-sql-agent`

## Repo Intent Map
- `dbt-cloud`: dbt models, tests, docs, Snowflake analytics debugging.
- `data-factory`: external-table/load config over already-landed ADLS paths; also the downstream Snowflake half of spreadsheet onboarding.
- `data-platform`: shared Snowflake/Terraform/platform tooling.
- `extractor-spreadsheets`: OneDrive/SharePoint spreadsheet extraction and mapping landing into ADLS; first half of spreadsheet onboarding.
- `metadata-builder`: metadata contract build/export for Avalanche catalog and related eval assets.
- `avalanche-mcp`: active MCP analytics platform and current agent-facing orchestration surface.
- `powerbi`: Power BI / Fabric semantic models, reports, and deployment validation.
- `docs`: VitePress documentation.

## Legacy Repo Intent Map
- `adrez-data-assistant`: legacy prototype repo; no new feature work unless explicitly requested.
- `adrez-metadata-sql-agent`: legacy SQL-agent repo; no new feature work unless explicitly requested.

## Skill Intent Map
Use these skills when intent clearly matches:
- `snowcli`: connect/query/check Snowflake, run SQL.
- `asana`: update/comment in Asana tasks.
- `write-commit`: prepare commit message from actual diff.
- `write-docs`: write/update docs.
- `qmd`: cross-repo retrieval over docs and notes before analysis or answer generation.
- `compare-tech`: compare tool options.
- `entity-spreadsheet-ingestion`: end-to-end onboarding of a new OneDrive/SharePoint spreadsheet source across extractor-spreadsheets and data-factory.
- `entity-extractor-spreadsheets`: add/update spreadsheet/mapping entities in extractor-spreadsheets.
- `entity-data-factory`: add/update external-table entities/configs in data-factory for already-landed ADLS files or downstream spreadsheet exposure.
- `entity-dbt-cloud`: add/update dbt entities/models (default `l1_raw` first).
- `powerbi-report-starter`: scaffold a new Power BI semantic model + report from scratch with canonical date dimensions.
- `avalanche-metadata-update`: rebuild/export Avalanche metadata bundle and sync catalog artifacts.

## Snowflake Defaults
- For `snowcli` tasks, use locally configured Snow CLI/dbt context by default.
- If required context is missing or ambiguous, ask one short clarifying question.
- Always return executable SQL and prefer fully qualified names (`database.schema.table`).

## Routing Rules
- Decide target repo + skill before editing.
- If the user asks to add a new OneDrive/SharePoint spreadsheet, mapping sheet, or manual statement and does not limit scope, default to end-to-end flow:
  - use `entity-spreadsheet-ingestion`
  - start in `/Users/martin/Documents/adrez/extractor-spreadsheets`
  - continue to `/Users/martin/Documents/adrez/data-factory` unless the user explicitly wants landing only
- If the user asks only for spreadsheet landing, file pickup, or `ingest_config.yml` changes, use `entity-extractor-spreadsheets`.
- If the user says files already exist in ADLS/lake/raw storage, or the source is Mews/Mara/other lake-native ingestion, skip extractor and use `entity-data-factory` in `/Users/martin/Documents/adrez/data-factory`.
- If the user asks to create a new Power BI report or semantic model from scratch, default to `powerbi-report-starter` in `/Users/martin/Documents/adrez/powerbi`.
- If user says "check dbt", default to `/Users/martin/Documents/adrez/dbt-cloud`.
- If user asks about Avalanche MCP, MCP analytics flow, or current agent behavior, default to `/Users/martin/Documents/adrez/avalanche-mcp`.
- If user asks to rebuild metadata/catalog for Avalanche, default to `/Users/martin/Documents/adrez/metadata-builder`.
- If ambiguous whether the file already lands in ADLS, ask one short clarifying question.

## Common Workflow Defaults
- Prefer repo-local `docs/tasks/` only for multi-step, risky, or multi-session work when that repo uses task notes.
- Skip task notes for trivial template-based edits.
- Any temporary filter, scoped workaround, or performance guardrail added to code/config must include a nearby `TODO` with removal condition and, when relevant, a task-note link.

## Task Memory
- Track execution status in Asana.
- Default note split:
  - Repo-local `docs/tasks/`: task execution notes, WIP analysis, temporary investigation context.
  - `/Users/martin/Documents/adrez/docs/`: durable cross-repo documentation.
- Promote notes to `/Users/martin/Documents/adrez/docs/` only when they describe current operational/business state that should be reused across tasks (for example "how we currently operate parking reservations/revenue", city tax policy, reconciliation operating rules).
- Keep modeling-only implementation notes (SQL-level mechanics tied to one repo) in that repo unless they are broadly reusable.
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
