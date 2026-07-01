# Daily Brief

This file is not the daily brief archive.

Daily morning-brief output and raw run notes belong outside this repository in
the automation memory file:

- `$CODEX_HOME/automations/adrez-chief-of-staff-morning-brief/memory.md`

Use this file only for durable Chief of Staff brief policy that future runs must
follow.

## Writeback Rules

- Do not persist the full daily brief in this repo.
- Do not write raw source digests, calendar dumps, email summaries, or transient
  daily priorities into `agents/ops`.
- Promote only durable state that should influence future runs:
  - stable Martin corrections
  - open loops that remain actionable beyond the current day
  - suppression rules for items that should not resurface
  - pipeline watch decisions that change future ranking
  - people follow-up state that is still relevant tomorrow
- Write durable state to the specific file that owns it:
  - `open-loops.md` for cross-workstream loops
  - `pipeline-watch.md` for recurring status or incident interpretation
  - `people-followups.md` for reply/relationship state
  - `decisions.md` for stable operating rules
- If a morning run changes tracked files under `agents/ops`, make those changes
  a focused git commit or explicitly leave the repo dirty only when Martin asks.

## Latest Durable Corrections

- 2026-07-01: dbt incident from the morning brief was resolved separately;
  Power BI and reports were refreshed. Do not keep surfacing it as an open
  incident unless a fresh failure appears. Martin is working on Cash recon
  today and will handle extranet items today.
- 2026-06-26: `Cash recon- Danovy kontroly + Martinuv update` was a meeting
  invite/context for next Wednesday finance meet/sync, not a reply-needed email.
  Martin will handle CSOB match-key work, and reporting/app focus remains a
  today's focus.
- 2026-06-26: Do not rank small Michal/reporting PRs as morning priorities only
  because GitHub requested Martin's review. Martin and Michal agreed not to use
  PR review friction for small non-production/non-important-pipeline changes.
  Surface them only when they touch PROD, an important pipeline, or a real
  release/risk decision.
- 2026-06-16: Mews Adyen account verification deadline is a Mews KYB/compliance
  request from the original migration email, not a Codex-created technical
  deadline.
- 2026-06-16: Avalanche follow-up is handled in the scheduled meeting; Adyen
  responses are watched by Martin; bank statements Snowflake automation is
  Martin's main work today; Michal Bukacek is coming in the afternoon.
- 2026-06-15: Do not surface dbt Mews rate-pricing warning, Power BI Fabric
  failure, or Booking Data Scraper/Better Stack incidents without a fresh
  trigger.
