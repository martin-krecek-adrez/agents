# Operating Decisions

Stable decisions for Adrez Chief of Staff and Codex coordination.

## Current

- Use long-running threads for coordination, not as the only source of truth.
- Use focused new threads for implementation work with a clear handoff prompt.
- Keep central operating state in `agents/ops/`.
- Keep repo implementation details in repo-local `docs/tasks/`.
- Keep durable cross-repo/business documentation in `/Users/martin/Documents/adrez/docs`.
- Daily briefs should be short, ranked, and action-oriented.
- Daily morning-brief output and raw run notes live in automation memory, not in
  tracked `agents/ops` files.
- `agents/ops` is durable operating state only; if a run changes it, commit the
  focused ops update or explicitly report that the repo was intentionally left
  dirty.
- Adrez Chief of Staff morning brief is work-only: use Outlook Calendar,
  Outlook Email, Teams, and triggered GitHub/CI; do not use Gmail or Google
  Calendar as default sources.
- Every morning brief should load recent repo `docs/tasks` notes to reconstruct
  what changed yesterday; task notes complement current Linear state.
- Linear is the only active Adrez task tracker. Asana is retired and must not be
  queried in routine work briefs; use it only for an explicit legacy URL/GID or
  historical-context request.
- For Teams, use narrow incremental listing/fetch retries before declaring a
  source gap. Broad chat listing may timeout.
- Avoid parallel Microsoft 365 connector fan-out in morning briefs. Run Outlook
  and Teams checks sequentially with small result sets to reduce Microsoft Graph
  429 throttling; if Martin provides direct context in chat, use that as a
  higher-confidence correction.
- Martin corrections are higher priority than older task notes, legacy Asana state,
  pipeline memory, or previous brief text.
- A brief should not recommend rollout, deploy, closure, or business
  communication from technical validation alone; label such items as inferred
  and ask for a decision when the business path is unclear.
- Recovered or merged work should not remain a Suggested Priority unless the
  remaining step is concrete, current, and user-facing.
- Treat `Done`, `Waiting`, `Parked`, and "Martin handles separately" as
  suppression signals for `Suggested Priorities` unless a newer source
  explicitly reopens the item.
