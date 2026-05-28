# Operating Decisions

Stable decisions for Adrez Chief of Staff and Codex coordination.

## Current

- Use long-running threads for coordination, not as the only source of truth.
- Use focused new threads for implementation work with a clear handoff prompt.
- Keep central operating state in `agents/ops/`.
- Keep repo implementation details in repo-local `docs/tasks/`.
- Keep durable cross-repo/business documentation in `/Users/martin/Documents/adrez/docs`.
- Daily briefs should be short, ranked, and action-oriented.
- Adrez Chief of Staff morning brief is work-only: use Outlook Calendar,
  Outlook Email, Teams, and triggered GitHub/CI; do not use Gmail or Google
  Calendar as default sources.
- Every morning brief should load recent repo `docs/tasks` notes to reconstruct
  what changed yesterday; Asana alone is not enough source of truth for agent
  work.
- Use Asana in every work brief, but treat missing/stale Asana results as a
  source-quality finding, not as proof that no work exists.
- For Teams, use narrow incremental listing/fetch retries before declaring a
  source gap. Broad chat listing may timeout.
