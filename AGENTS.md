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
- Asana: `asana`.
- Git delivery: `write-commit`, `repo-pr-handoff`, `repo-worktree-safety`.
- Docs/context: `write-docs`, `ai-context-maintenance`, `agent-feedback-capture`, `compare-tech`.
- Spreadsheet/data onboarding: `entity-spreadsheet-ingestion`, `entity-extractor-spreadsheets`, `entity-data-factory`.
- dbt: `entity-dbt-cloud`.
- Power BI: `powerbi-report-starter`.
- Avalanche metadata: `avalanche-metadata-update`.

## Snowflake Defaults
- For `snowcli` tasks, use locally configured Snow CLI/dbt context by default.
- If required context is missing or ambiguous, ask one short clarifying question.
- Always return executable SQL and prefer fully qualified names (`database.schema.table`).

## Routing Rules
- Decide target repo + skill before editing.
- New OneDrive/SharePoint spreadsheet, mapping sheet, or manual statement defaults to `entity-spreadsheet-ingestion`: `extractor-spreadsheets` first, then `data-factory` unless landing-only is requested.
- Spreadsheet landing/file pickup/`ingest_config.yml` only: `entity-extractor-spreadsheets`.
- PDF/document parsing to ADLS CSV: `extractor-documents` first, then `data-factory` only if Snowflake exposure is needed.
- Already-landed ADLS/lake/raw or lake-native source: `entity-data-factory`.
- New Power BI report/model: `powerbi-report-starter`.
- "check dbt": `dbt-cloud`.
- Avalanche MCP/current agent behavior: `avalanche-mcp`.
- Avalanche metadata/catalog rebuild: `metadata-builder`.
- If ADLS landing status is ambiguous, ask one short clarifying question.

## Common Workflow Defaults
- Use repo-local `docs/tasks/` for multi-step, risky, or multi-session work when the repo uses task notes; skip for trivial edits.
- Temporary filters/workarounds/guardrails need a nearby `TODO` with removal condition and task-note link when relevant.

## Task Memory
- Track execution status in Asana.
- Repo `docs/tasks/`: execution notes and WIP analysis. `/Users/martin/Documents/adrez/docs/`: durable cross-repo/business state.
- `agents/ops/`: personal operating state for Codex coordination, including Chief of Staff briefs, open loops, people follow-ups, pipeline watch items, and thread handoff prompts.
- Keep modeling-only implementation notes in the repo unless broadly reusable. Suggested task note name: `YYYY-MM-DD-short-task-name.md`.
- Cross-link Asana <-> task note <-> changed model/code paths.

## Git Defaults
- Run `git status -sb` before edits.
- Pull with `--ff-only` by default.
- For implementation tasks, create or switch to a dedicated task branch before editing unless the user explicitly asks to use the current branch.
- Use `repo-pr-handoff` for non-trivial handoffs: model logic, ingestion, Terraform/platform, CI/deploy, or shared AI context.
- Use `repo-worktree-safety` when multiple independent tasks are active in the same repository, when branch/worktree state is ambiguous, or when dirty files may belong to another task.
- Do not force branch/PR workflow for tiny typo/docs-only edits unless asked.
- For non-trivial work, "push", "pushed", "commit and push", or "clean and pushed" means push a feature branch and open a draft PR.
- Never push directly to `main` for non-trivial work unless the user explicitly says `main` or `directly to main`.
- "make changes in <repo> and push it" is not permission to push `main`; use a task branch and draft PR.
- Pushing a branch without PR requires explicit `no PR` or `jen pushni branch`.
- Treat shared AI operating-system changes (`AGENTS.md`, skills, routing, task memory, automation prompts) as non-trivial.
- If non-trivial changes already exist on `main`, create a feature branch before committing.
- Do not push unless explicitly asked.
- Do not amend commits unless explicitly asked.

## Concurrent Git Work
- Branches are delivery units; worktrees are concurrency units.
- For parallel same-repo tasks, use one `git worktree` per task branch. Do not switch one shared checkout between unrelated task branches.
- Default task worktree location: `/Users/martin/Documents/adrez/_worktrees/<repo-name>/<task-slug>`.
- Before editing, committing, pushing, PR, or merge, verify `pwd`, repo root, current branch, `git status -sb`, and intended task.
- If branch does not match the task, stop and switch to the correct worktree or ask.
- If dirty file ownership is unclear, stop and ask. Never use `git stash`, `git reset`, `git checkout --`, `git clean`, or file-moving cleanup to juggle unrelated work unless explicitly approved.
- Multi-repo work uses one branch and PR per repo. Multi-task same-repo work uses one worktree, branch, and PR per task.

## PR And Merge Defaults
- Non-trivial work default: dedicated branch -> focused commit(s) -> push branch -> draft PR -> CI check -> Asana handoff.
- After a user-requested push, open a draft PR unless the user explicitly says `no PR`, `jen pushni branch`, or asks for ready-for-review.
- Use GitHub connector for PR creation/metadata when cleanly resolvable; use `gh` for CI/logs/checks/review threads/merge.
- For private Adrez repos, a GitHub connector `404` can mean connector scope; verify local remote and retry narrow sandbox-failed `gh` commands with `require_escalated` before concluding auth/repo is broken.
- After pushing, resolve PR and head SHA, then check PR status for that exact head SHA.
- Never merge unless the user explicitly says `merge`, `sluč`, or `dej to do main`.
- Before merge, verify checks, review threads, mergeability, scope, base freshness, and current PR head SHA.
- Default merge method is squash merge unless repo-local policy says otherwise.
- After merge, delete safe short-lived remote branch, prune task worktree, sync `main`, and update Asana.

## GitHub Actions Defaults
- `gh` is the default tool for GitHub Actions inspection across Adrez repos.
- After user-requested push to a branch with CI, check current PR/head-SHA status and inspect failures with `gh`.
- When the user expects CI confirmation, wait for completion with `gh run watch <run-id>` (or poll `gh run view <run-id>`) and report the final result.
- Use run logs as source of truth for CI failures.

## Safety
- Do not run destructive commands unless explicitly asked.
- Ask before network/credentialed commands when required by local repo policy.
- Dry-run mode: if user says "describe only", "don't do it", or equivalent, do not run commands and do not edit files.
