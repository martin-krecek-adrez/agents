# AGENTS.md

## Purpose
This repository manages Martin's personal operating setup and routing.
Team working rules are owned by `tech-plugins/docs/adrez-working-rules.md`
and distributed in repository `AGENTS.md` files. Team members do not run this sync.
Keep repo-specific details in the owning repository.

## Communication
- Respond in the user's language unless they explicitly ask otherwise.
- Prefer direct, neutral responses with minimal fluff.

## Execution Order
Apply `/Users/martin/AGENTS.md`, `/Users/martin/Documents/adrez/AGENTS.md`,
this file, then the closest repo/subfolder `AGENTS.md`. Nearest repo rules win for repo-specific behavior.

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
- `reporting`: report apps, generators, decks, and HTML artefacts. Transformations
  stay in dbt-cloud; Power BI and Fabric stay in powerbi.
- `tech-plugins`: shared team rules and skills.

## Archived Repo Boundary
- `adrez-data-assistant`: replaced by `avalanche-mcp`.
- `adrez-metadata-sql-agent`: metadata ownership moved to `metadata-builder`; active agent runtime work moved to `avalanche-mcp`.
- `extractor-documents`: its Expedia payout/remittance PDF flow moved to `extranet-scraper`.
- Do not route new work to archived repos. Use them only for an explicitly approved restore, migration, or historical investigation.

## Skill Intent Map
`adrez-com/tech-plugins` owns team data-platform and delivery skills through
`adrez-data-platform`. This repo owns personal operating and context skills.
Never copy plugin skills into `agents/skills` or `~/.codex/skills`.
Team members install the plugin; they must not run Martin's local sync.

Use these skills when intent clearly matches:
- Snowflake: `snowcli`.
- Linear task/project tracking: `adrez-linear-workflow`.
- Thread intake / agent orchestration: `adrez-agent-orchestration`.
- Standalone sidebar task lifecycle under one MAIN task: `adrez-thread-orchestration`.
- Decision review: `grill-me`.
- Implementation review: `implementation-review`.
- Git delivery: `write-commit`, `repo-pr-handoff`, `repo-worktree-safety`.
- Docs/context: `write-docs`, `ai-context-maintenance`, `agent-feedback-capture`.
- Spreadsheet/data onboarding: `entity-spreadsheet-ingestion`, `entity-extractor-spreadsheets`, `entity-data-factory`.
- dbt: `entity-dbt-cloud`.
- Avalanche metadata: `avalanche-metadata-update`.

The installed plugin's `skill-inventory.txt` defines ownership. Local sync must
validate it and reject duplicate direct source or runtime skills.

## Routing Rules
- Decide target repo + skill before editing.
- New SharePoint/OneDrive Excel, input sheet, mapping sheet, or manual spreadsheet request defaults to `entity-spreadsheet-ingestion`; examples: "pridej input sheet", "napoj tenhle Excel", "dostan tenhle SharePoint/OneDrive soubor do Snowflake".
- Landing/file pickup/`ingest_config.yml` only: `entity-extractor-spreadsheets`.
- Already-landed ADLS/lake/raw source, external-table config, or Snowflake exposure only: `entity-data-factory`.
- Expedia payout/remittance PDF extraction: `extranet-scraper`.
- New document extraction: route to the owning active source/ingestion repo; do not revive `extractor-documents` without an explicit migration decision.
- "check dbt": `dbt-cloud`.
- Airflow status, DAG runs, task instances, logs, and approved control actions:
  route to `airflow-orchestrator` and use SSH to the VPS with the local key
  `~/.ssh/adrez_vps_hostinger`. Follow the repo-local
  `.codex/rules/airflow-readonly-api.md` rule. Do not use the 1Password-backed
  Airflow REST API unless the user explicitly requests that access path.
- `test on local Airflow`, `otestuj na airflow local`, and equivalent requests:
  route to `<workspace>/airflow-orchestrator/docs/test-airflow-locally.md`. Use
  its exact production-parity runtime procedure and the standard read-only
  1Password service account. Do not replace it with unit tests or a different
  local Airflow installation.
- Avalanche MCP/current agent behavior: `avalanche-mcp`.
- Avalanche metadata/catalog rebuild: `metadata-builder`.
- If ADLS landing status is ambiguous, ask one short clarifying question.

## Common Workflow Defaults
- Use the workspace definition of routine work.
- Validate changed behavior and affected contracts. Reuse checks only when
  relevant code, configuration, inputs, and environment assumptions are unchanged.
- Broaden for an affected contract, required repo check, or observed failure.
  State the reason in an existing update; do not add a form.
- Stop when required checks pass and blockers are resolved. Record unavailable
  checks under repo handoff rules; do not substitute an unrelated broad build.
- Delivery-only work reuses valid checks. CI, human review, production approval,
  and delivery proof still apply.
- Create new Linear issues automatically only for substantial independent work:
  multiple sessions, coordination, or significant business/production impact.
  Minor work reuses an applicable issue. A commit or PR alone does not qualify.
  Use `adrez-linear-workflow`; explicit creation requests and read-only/no-Linear
  take precedence. Assign new/unassigned work to Martin. Record material state.
  Tracking authorizes no production action or outside message.
- Use existing repo `docs/tasks/` for multi-step, risky, or multi-session work;
  skip trivial edits. Temporary workarounds need a nearby removal-condition
  `TODO` and a task-note link when relevant.

## Task Memory
- Linear is the active tracker for substantial work. Asana is retired and must not be
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
- Before a task branch/worktree, use `repo-worktree-safety` and fetch its remote
  base. Do not use unverified local `main`.
- Reuse the current worktree. Create another only for an explicit parallel task
  with a distinct owner and delivery branch. Pull only `--ff-only` when clean.
- Use a dedicated task branch before implementation unless the user explicitly
  chooses the current branch.
- Use `repo-pr-handoff` for non-trivial delivery and `implementation-review`
  before each non-trivial commit, push, PR, or merge. Reuse review only for the
  same implementation fingerprint and assumptions. Check current delivery state
  and refresh remote-base proof before delivery.
- Use `repo-worktree-safety` for concurrent work, ambiguous state, or dirty files.
- Shared AI behavior changes are non-trivial: instruction policy, skills,
  routing, task-memory rules, and automation prompts. Evidence-only notes,
  review records, or runtime-gap updates remain routine when behavior is unchanged.
- Do not push or amend commits unless explicitly asked.

## Delivery Defaults
- Branches are delivery units; worktrees are concurrency units.
  At intake, declare the delivery target. Default to local unless later stages
  are authorized.
- Parallel tasks use `/Users/martin/Documents/adrez/_worktrees/<repo>/<task-slug>`.
- Unclear-owner dirty files block switching, staging, commit, pull, push, and PR
  work. Never use `git stash`, `git reset`, `git checkout --`, `git clean`,
  or move unrelated work without approval.
- For non-trivial work, push/commit-and-push/ship means a feature branch and draft
  PR unless the user requests no PR, branch-only push, or direct `main`.
  Never merge without an explicit merge instruction.
- Before handoff, fetch and prove current-base ancestry. After push, prove that
  local HEAD, the remote task branch, and the PR head use the same SHA.
  After merge, verify the fetched remote base against GitHub's merge SHA.
- Report local, branch, PR, `main`, deployment, and cleanup separately. Do not
  call local or branch-only work merged or deployed.
- Never delete a worktree because of age alone. Inventory with
  `scripts/report_worktree_state.py --summary-only`. Remove only owned, clean,
  remotely recoverable worktrees with confirmed completion or abandonment.
  Cleanup otherwise remains a separate explicit action.
- Keep canonical checkouts clean and synced. Dirty, detached, ahead, behind, or
  diverged state is an audit finding, never reset permission.
- After a PR merge, close a helper-created task lifecycle: prove delivery on
  the actual remote base, fetch/prune, remove its owned clean worktree and local
  branch, and verify remote deletion. Run `repo-pr-handoff` finish check first;
  require direct ancestry or an exact merged-head-to-merge mapping.
- Report a Codex-app-managed worktree without helper metadata ready for archival.
  Do not fabricate ownership or force cleanup. Follow
  `/Users/martin/Documents/adrez/docs/data-platform/repository-hygiene.md`.
  Remote deletion needs approval when auto-delete did not handle it.
- Use `gh` for CI checks and logs. Logs are the CI-failure source of truth.
  GitHub connector `404` can mean connector scope; verify the remote and retry narrow
  sandbox-failed `gh` commands with `require_escalated`.

## Safety
- Do not run destructive commands unless explicitly asked.
- Ask before network/credentialed commands when required by local repo policy.
- Dry-run mode: if user says "describe only", "don't do it", or equivalent, do not run commands and do not edit files.
- For local read-only access to Adrez 1Password secrets, follow
  `ops/1password-agent-access.md`. The service account is limited to the
  `Data Platform` and `API Users` vaults. Never print, log, or commit its token.

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
