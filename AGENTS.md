# AGENTS.md

## Purpose
Default control hub for Codex in Adrez. Keep this file routing-focused; repo-specific details belong to each repo `AGENTS.md`.

## Communication
- Respond in the user's language unless they explicitly ask otherwise.
- Prefer direct, neutral responses with minimal fluff.

## Execution Order
Apply `/Users/martin/AGENTS.md`, this file, then the closest repo/subfolder
`AGENTS.md`. Nearest repo rules win for repo-specific behavior.

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

## Repo Intent Map
- `dbt-cloud`: dbt models, tests, docs, Snowflake analytics debugging.
- `data-factory`: external-table/load config over already-landed ADLS paths; also the downstream Snowflake half of spreadsheet onboarding.
- `data-platform`: shared Snowflake/Terraform/platform tooling.
- `extractor-spreadsheets`: OneDrive/SharePoint spreadsheet extraction and mapping landing into ADLS; first half of spreadsheet onboarding.
- `metadata-builder`: metadata contract build/export for Avalanche catalog and related eval assets.
- `avalanche-mcp`: active MCP analytics platform; do not touch unless explicitly requested.
- `powerbi`: Power BI / Fabric semantic models, reports, and deployment validation.
- `docs`: VitePress documentation.

## Skill Intent Map
Use these skills when intent clearly matches:
- `snowcli`: query/check Snowflake.
- `asana`: update/comment in Asana tasks.
- `write-commit`: prepare commit message from actual diff.
- `write-docs`: write/update docs.
- `compare-tech`: compare tool options.
- `ai-context-maintenance`: audit AGENTS.md, shared skills, task notes, and durable docs routing.
- `repo-pr-handoff`: prepare clean commits, PR summaries, validation handoffs, and Asana updates.
- `entity-spreadsheet-ingestion`: end-to-end spreadsheet onboarding across extractor-spreadsheets and data-factory.
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
- For implementation tasks, create or switch to a dedicated task branch before editing unless the user explicitly asks to use the current branch.
- Use `repo-pr-handoff` for non-trivial handoffs: model logic, ingestion, Terraform/platform, CI/deploy, or shared AI context.
- Do not force branch/PR workflow for tiny typo/docs-only edits unless the user asks.
- For non-trivial work, unspecified requests like "push", "pushed", "commit and push", or "clean and pushed" mean push a feature branch and open a draft PR.
- Never push directly to `main` for non-trivial work unless the user explicitly says `main`, `directly to main`, or `no PR`.
- A request like "make changes in <repo> and push it" is not permission to work on or push `main`; use a dedicated task branch and draft PR.
- Treat shared AI operating-system changes (`AGENTS.md`, skills, routing, task memory, automation prompts) as non-trivial.
- If non-trivial changes already exist on `main`, create a feature branch before committing; do not direct-push `main` just to clean the worktree.
- Do not push unless explicitly asked.
- Do not amend commits unless explicitly asked.

## GitHub Actions Defaults
- `gh` is the default tool for GitHub Actions inspection across Adrez repos.
- After any user-requested push to a branch with CI, check the latest run with `gh run list --branch <branch> --limit 5`.
- Open the failing run with `gh run view <run-id> --json jobs` and `gh run view <run-id> --log` before guessing at root cause.
- When the user expects CI confirmation, wait for completion with `gh run watch <run-id>` (or poll `gh run view <run-id>`) and report the final result.
- Prefer repo-local workflow files under `.github/workflows/` only as supporting context; use run logs as the source of truth for the actual failure.

## Safety
- Do not run destructive commands unless explicitly asked.
- Ask before network/credentialed commands when required by local repo policy.
- Dry-run mode: if user says "describe only", "don't do it", or equivalent, do not run commands and do not edit files.
