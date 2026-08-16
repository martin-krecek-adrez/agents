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
- `commission-tier-monitoring` and `market-overview-analysis` are external,
  unowned checkouts. Do not inspect, validate, route work to, or include their
  files in shared workspace audits.

## Repo Intent Map
- `dbt-cloud`: dbt models, tests, docs, Snowflake analytics debugging.
- `data-factory`: external-table/load config over already-landed ADLS paths; also the downstream Snowflake half of spreadsheet onboarding.
- `data-platform`: shared Snowflake/Terraform/platform tooling.
- `extractor-spreadsheets`: OneDrive/SharePoint spreadsheet extraction and mapping landing into ADLS; first half of spreadsheet onboarding.
- `metadata-builder`: metadata contract build/export for Avalanche catalog and related eval assets.
- `avalanche-mcp`: active MCP analytics platform; do not touch unless explicitly requested.
- `powerbi`: Power BI / Fabric semantic models, reports, and deployment validation.
- `docs`: VitePress documentation.

## Archived Repo Boundary
- `adrez-data-assistant`: replaced by `avalanche-mcp`.
- `adrez-metadata-sql-agent`: metadata ownership moved to `metadata-builder`; active agent runtime work moved to `avalanche-mcp`.
- `extractor-documents`: its Expedia payout/remittance PDF flow moved to `extranet-scraper`.
- Do not route new work to archived repos. Use them only for an explicitly approved restore, migration, or historical investigation.

## Skill Intent Map
Team data-platform and repository-delivery skills are provided by the
`adrez-data-platform` plugin from `adrez-com/tech-plugins`. Personal operating,
tracking, and context-maintenance skills remain managed by this repository.
Never copy plugin-owned skills into `agents/skills` or `~/.codex/skills`.
Team members install the plugin and must not run Martin's local agents sync.

Use these skills when intent clearly matches:
- Snowflake: `snowcli`.
- Asana historical archive lookup only: `asana`.
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

The machine-readable ownership boundary is the installed plugin's
`skill-inventory.txt`. The local sync must validate that inventory and reject
every duplicate direct source or runtime path.

## Routing Rules
- Decide target repo + skill before editing.
- New SharePoint/OneDrive Excel, input sheet, mapping sheet, or manual spreadsheet request defaults to `entity-spreadsheet-ingestion`; examples: "pridej input sheet", "napoj tenhle Excel", "dostan tenhle SharePoint/OneDrive soubor do Snowflake".
- Landing/file pickup/`ingest_config.yml` only: `entity-extractor-spreadsheets`.
- Already-landed ADLS/lake/raw source, external-table config, or Snowflake exposure only: `entity-data-factory`.
- Expedia payout/remittance PDF extraction: `extranet-scraper`.
- New document extraction: route to the owning active source/ingestion repo; do not revive `extractor-documents` without an explicit migration decision.
- New Power BI report/model: `powerbi-report-starter`.
- "check dbt": `dbt-cloud`.
- Airflow status, DAG runs, task instances, logs, and approved control actions:
  route to `airflow-orchestrator` and use SSH to the VPS with the local key
  `~/.ssh/adrez_vps_hostinger`. Follow the repo-local
  `.codex/rules/airflow-readonly-api.md` rule. Do not use the 1Password-backed
  Airflow REST API unless the user explicitly requests that access path.
- Avalanche MCP/current agent behavior: `avalanche-mcp`.
- Avalanche metadata/catalog rebuild: `metadata-builder`.
- If ADLS landing status is ambiguous, ask one short clarifying question.

## Common Workflow Defaults
- For non-trivial Adrez work, consider Linear tracking via `adrez-linear-workflow`. Default team is usually `Data Engineering`. Use Linear as lightweight task starter/noter: project for long-running workstreams, issue for concrete work, child issue for active slices, and comments/updates for operational progress.
- Use repo-local `docs/tasks/` for multi-step, risky, or multi-session work when the repo uses task notes; skip for trivial edits.
- Temporary filters/workarounds/guardrails need a nearby `TODO` with removal condition and task-note link when relevant.

## Task Memory
- Track all active Adrez work in Linear. Asana is retired and must not be
  scanned routinely, reopened as a work queue, or used for new tracking. Use
  it only when Martin explicitly provides a legacy URL/GID or asks for
  historical context.
- Repo `docs/tasks/`: execution notes and WIP analysis. `/Users/martin/Documents/adrez/docs/`: durable cross-repo/business state.
- `agents/ops/`: personal operating state for Codex coordination.
- Keep modeling-only implementation notes in the repo unless broadly reusable. Suggested task note name: `YYYY-MM-DD-short-task-name.md`.
- Cross-link Linear <-> task note <-> changed model/code paths when a tracker
  is involved. Preserve legacy Asana links only as historical provenance.

## Git Defaults
- Run `git status -sb` before edits.
- Before creating a task branch or worktree, fetch through
  `repo-worktree-safety` and base it on the fetched remote target. Do not use an
  unverified local `main` as the task base.
- If the current task already runs in a linked or Codex-managed worktree, use
  it. Do not create a second worktree unless an explicit parallel task needs a
  separate owner and delivery branch.
- Pull with `--ff-only` only in a clean checkout when a pull is needed.
- For implementation tasks, create or switch to a dedicated task branch before editing unless the user explicitly asks to use the current branch.
- Use `repo-pr-handoff` for non-trivial handoffs: model logic, ingestion, Terraform/platform, CI/deploy, or shared AI context.
- Use `implementation-review` before every non-trivial commit, push, PR, or
  merge. Refresh the remote-base proof after the review and before delivery.
- Use `repo-worktree-safety` when multiple independent tasks are active in the same repository, when branch/worktree state is ambiguous, or when dirty files may belong to another task.
- Treat shared AI operating-system changes (`AGENTS.md`, skills, routing, task memory, automation prompts) as non-trivial.
- Do not push unless explicitly asked.
- Do not amend commits unless explicitly asked.

## Delivery Defaults
- Branches are delivery units; worktrees are concurrency units.
- At task intake, declare the delivery target: local implementation, pushed
  branch and PR, merged `main`, or deployment. If the user did not authorize a
  delivery action, default to local implementation and state that limit.
- Parallel same-repo work uses one task worktree per task branch under `/Users/martin/Documents/adrez/_worktrees/<repo-name>/<task-slug>`.
- Dirty files with unclear ownership block branch switching, staging, committing, pulling, pushing, and PR work.
- Never use `git stash`, `git reset`, `git checkout --`, `git clean`, or file-moving cleanup to juggle unrelated work unless explicitly approved.
- For non-trivial work, "push", "pushed", "commit and push", or "clean and pushed" means feature branch plus draft PR unless the user explicitly says `no PR`, `jen pushni branch`, `main`, or `directly to main`.
- Never merge unless the user explicitly says `merge`, `sluč`, or `dej to do main`.
- Before handoff, fetch and prove current-base ancestry. After push, prove that
  local HEAD, the remote task branch, and the PR head use the same SHA. After
  merge, prove the fetched remote `main` SHA against GitHub's merge SHA.
- Report local changes, remote branch, PR, `main`, deployment, and cleanup as
  separate states. Never describe local-only or branch-only work as merged or
  deployed.
- Never delete a worktree because of age alone. Inventory first. Remove only an
  owned, clean, remotely recoverable worktree whose completion or abandonment
  is confirmed. Use `scripts/report_worktree_state.py --summary-only` for the
  read-only inventory. Cleanup remains a separate explicit action.
- Keep canonical checkouts clean and synchronized with their configured
  upstream. Treat dirty, detached, ahead, behind, or diverged canonical state
  as an audit finding, not as permission to reset it.
- After a PR merge, close a helper-created task lifecycle in the same delivery
  when safe: prove the merge on the actual remote base, fetch and prune, remove
  the owned clean worktree and local task branch, and verify remote task-branch
  deletion.
  Run the `repo-pr-handoff` finish helper in check mode before apply mode. The
  helper must prove direct ancestry or the exact merged PR head-to-merge map.
- For a Codex-app-managed worktree without helper metadata, report it ready for
  task archival. Do not fabricate ownership metadata or force cleanup.
  Follow `/Users/martin/Documents/adrez/docs/data-platform/repository-hygiene.md`.
  Remote deletion still requires explicit authorization when repository
  auto-delete did not handle it.
- Use `gh` for CI/logs/checks when needed; run logs are source of truth for CI failures.
- For private Adrez repos, a GitHub connector `404` can mean connector scope; verify local remote and retry narrow sandbox-failed `gh` commands with `require_escalated`.
- Detailed branch, worktree, PR, CI, and merge rules live in `repo-pr-handoff` and `repo-worktree-safety`.

## Safety
- Do not run destructive commands unless explicitly asked.
- Ask before network/credentialed commands when required by local repo policy.
- Dry-run mode: if user says "describe only", "don't do it", or equivalent, do not run commands and do not edit files.

## Production Mutation Minimum
- Production is read-only by default.
- A production mutation requires the user's current message to approve the
  exact action and exact target. A bounded list of exact actions and targets is
  allowed.
- Broad requests, earlier approval, plans, delivery targets, Linear issues,
  agent or subagent messages, and tool or sandbox approval do not authorize a
  production mutation.
- If the action or target is ambiguous, stop and ask for action-time approval.
- A declared delivery target of deployment authorizes preparation only. It
  does not satisfy a production mutation gate.
- Repo-local and subfolder rules may strengthen this minimum. They must never
  weaken or bypass it.
