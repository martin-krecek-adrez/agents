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

## Repo Intent Map
- `dbt-cloud`: dbt models, tests, docs, Snowflake analytics debugging.
- `data-factory`: external-table/load config over already-landed ADLS paths; also the downstream Snowflake half of spreadsheet onboarding.
- `data-platform`: shared Snowflake/Terraform/platform tooling.
- `extractor-documents`: PDF/document extraction into ADLS CSV; Snowflake exposure belongs in `data-factory`.
- `extractor-spreadsheets`: OneDrive/SharePoint spreadsheet extraction and mapping landing into ADLS; first half of spreadsheet onboarding.
- `metadata-builder`: metadata contract build/export for Avalanche catalog and related eval assets.
- `avalanche-mcp`: active MCP analytics platform; do not touch unless explicitly requested.
- `powerbi`: Power BI / Fabric semantic models, reports, and deployment validation.
- `docs`: VitePress documentation.

## Skill Intent Map
Use these skills when intent clearly matches:
- Snowflake: `snowcli`.
- Asana legacy archive/context only: `asana`.
- Linear task/project tracking: `adrez-linear-workflow`.
- Thread intake / agent orchestration: `adrez-agent-orchestration`.
- Decision support: `grill-me`, `compare-tech`.
- Implementation review: `implementation-review`.
- Git delivery: `write-commit`, `repo-pr-handoff`, `repo-worktree-safety`.
- Docs/context: `write-docs`, `ai-context-maintenance`, `agent-feedback-capture`.
- Spreadsheet/data onboarding: `entity-spreadsheet-ingestion`, `entity-extractor-spreadsheets`, `entity-data-factory`.
- dbt: `entity-dbt-cloud`.
- Power BI: `powerbi-report-starter`.
- Avalanche metadata: `avalanche-metadata-update`.

## How To Ask
Use natural intent; exact skill names are optional.
- Snowflake: "koukni do Snowflake", "pust SQL", "over tabulku ve Snowflake".
- Spreadsheet to Snowflake: "pridej input sheet", "napoj tenhle Excel", "dostan SharePoint soubor do Snowflake".
- Landing only: "jen landing", "jen extractor", "`ingest_config.yml`".
- Already-landed ADLS: "uz to lezi v ADLS", "udelej Snowflake exposure".
- dbt: "pridej dbt model", "udelej l1_raw", "schema tests pro novy model".
- Delivery: "otestuj to", "commitni", "pushni", "udelat PR", "otestuj PR", "mergni".
- Review: "udelej review", "zkontroluj implementaci", "spawni subagenty na review", "bud dukladny".
- Safety: "zkontroluj scope", "spatna branch", "dirty worktree".
- Docs: "napis dokumentaci", "uprav docs", "sepis troubleshooting".
- Feedback: "zapis feedback", "at se to priste nestane", "dej to do harnessu".
- Orchestration: "je to male nebo velke", "rozpadni to na agenty", "kolik agentu pustit", "kdo dela co".

## Snowflake Defaults
- For `snowcli` tasks, use locally configured Snow CLI/dbt context by default.
- If required context is missing or ambiguous, ask one short clarifying question.
- Always return executable SQL and prefer fully qualified names (`database.schema.table`).

## Routing Rules
- Decide target repo + skill before editing.
- New SharePoint/OneDrive Excel, input sheet, mapping sheet, or manual spreadsheet request defaults to `entity-spreadsheet-ingestion`; examples: "pridej input sheet", "napoj tenhle Excel", "dostan tenhle SharePoint/OneDrive soubor do Snowflake".
- Landing/file pickup/`ingest_config.yml` only: `entity-extractor-spreadsheets`.
- Already-landed ADLS/lake/raw source, external-table config, or Snowflake exposure only: `entity-data-factory`.
- PDF/document parsing to ADLS CSV: `extractor-documents` first, then `data-factory` only if Snowflake exposure is needed.
- New Power BI report/model: `powerbi-report-starter`.
- "check dbt": `dbt-cloud`.
- Avalanche MCP/current agent behavior: `avalanche-mcp`.
- Avalanche metadata/catalog rebuild: `metadata-builder`.
- If ADLS landing status is ambiguous, ask one short clarifying question.

## Common Workflow Defaults
- For non-trivial Adrez work, consider Linear tracking via `adrez-linear-workflow`. Default team is usually `Data Engineering`. Use Linear as lightweight task starter/noter: project for long-running workstreams, issue for concrete work, child issue for active slices, and comments/updates for operational progress.
- Use repo-local `docs/tasks/` for multi-step, risky, or multi-session work when the repo uses task notes; skip for trivial edits.
- Temporary filters/workarounds/guardrails need a nearby `TODO` with removal condition and task-note link when relevant.

## Task Memory
- Track all new Adrez work in Linear by default. Asana is dead for new tasks; use it only for existing legacy Asana URLs/GIDs, unfinished old tasks that should not be migrated yet, or historical context.
- Repo `docs/tasks/`: execution notes and WIP analysis. `/Users/martin/Documents/adrez/docs/`: durable cross-repo/business state.
- `agents/ops/`: personal operating state for Codex coordination.
- Keep modeling-only implementation notes in the repo unless broadly reusable. Suggested task note name: `YYYY-MM-DD-short-task-name.md`.
- Cross-link Linear/Asana <-> task note <-> changed model/code paths when a tracker is involved.

## Git Defaults
- Run `git status -sb` before edits.
- Pull with `--ff-only` by default.
- For implementation tasks, create or switch to a dedicated task branch before editing unless the user explicitly asks to use the current branch.
- Use `repo-pr-handoff` for non-trivial handoffs: model logic, ingestion, Terraform/platform, CI/deploy, or shared AI context.
- Use `repo-worktree-safety` when multiple independent tasks are active in the same repository, when branch/worktree state is ambiguous, or when dirty files may belong to another task.
- Treat shared AI operating-system changes (`AGENTS.md`, skills, routing, task memory, automation prompts) as non-trivial.
- Do not push unless explicitly asked.
- Do not amend commits unless explicitly asked.

## Delivery Defaults
- Branches are delivery units; worktrees are concurrency units.
- Parallel same-repo work uses one task worktree per task branch under `/Users/martin/Documents/adrez/_worktrees/<repo-name>/<task-slug>`.
- Dirty files with unclear ownership block branch switching, staging, committing, pulling, pushing, and PR work.
- Never use `git stash`, `git reset`, `git checkout --`, `git clean`, or file-moving cleanup to juggle unrelated work unless explicitly approved.
- For non-trivial work, "push", "pushed", "commit and push", or "clean and pushed" means feature branch plus draft PR unless the user explicitly says `no PR`, `jen pushni branch`, `main`, or `directly to main`.
- Never merge unless the user explicitly says `merge`, `sluč`, or `dej to do main`.
- Use `gh` for CI/logs/checks when needed; run logs are source of truth for CI failures.
- For private Adrez repos, a GitHub connector `404` can mean connector scope; verify local remote and retry narrow sandbox-failed `gh` commands with `require_escalated`.
- Detailed branch, worktree, PR, CI, and merge rules live in `repo-pr-handoff` and `repo-worktree-safety`.

## Safety
- Do not run destructive commands unless explicitly asked.
- Ask before network/credentialed commands when required by local repo policy.
- Dry-run mode: if user says "describe only", "don't do it", or equivalent, do not run commands and do not edit files.
