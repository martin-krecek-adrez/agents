# Adrez Ops Memory

Lightweight operating memory for Codex coordination across Adrez workstreams.

Use this folder for personal operating state that does not belong to one repo:
daily priorities, open loops, people follow-ups, pipeline watch items, and
thread handoffs.

Do not use this folder for implementation details that belong in repo
`docs/tasks/`, durable business documentation that belongs in
`/Users/martin/Documents/adrez/docs`, or raw feedback that belongs in
`agents/feedback/inbox/`.

## Files

| File | Purpose |
| --- | --- |
| `daily-brief.md` | Latest Chief of Staff brief and short history. |
| `open-loops.md` | Cross-repo blockers, waiting items, PRs, Asana follow-ups. |
| `pipeline-watch.md` | Pipeline/status email patterns and watch items. |
| `people-followups.md` | People and threads that likely need a reply. |
| `decisions.md` | Stable operating decisions that affect future brief behavior. |
| `thread-handoff-template.md` | Prompt template for starting a focused new Codex thread. |

## Chief Of Staff Brief Contract

The daily brief should be short enough to fit on one screen.

Default sections:
- `Today`
- `Needs Reply`
- `Pipeline / Watch`
- `Open Loops`
- `Suggested Priorities`

Rules:
- Prefer ranked bullets over explanation.
- Draft replies only when useful; never send them without confirmation.
- Do not delete, archive, send, schedule, or mutate external systems without
  explicit user approval.
- Write back only concise state that will matter tomorrow.

## Morning Source Order

This is a work Chief of Staff brief. Do not use Gmail or Google Calendar by
default.

1. Local ops memory:
   - `agents/ops/*.md`
   - automation memory
2. Yesterday / recent execution context:
   - repo task notes under `*/docs/tasks/YYYY-MM-DD-*.md`
   - especially files dated yesterday or modified since yesterday
3. Work systems:
   - Outlook Calendar for today's schedule
   - Outlook Email for reply-needed and pipeline/status signals
   - Teams channels and chats for people, pipeline, incident, and status signals
   - Asana for assigned tasks, due-soon work, recently completed work, and
     project/task status
4. GitHub / CI:
   - only when directly referenced by ops memory, Outlook, Teams, Asana, or a
     recent task note

## Connector Handling

- Teams broad chat listing can timeout. Start with small pages (`top=1`) and
  expand only if each call succeeds.
- If Teams returns Microsoft Graph 429, treat it as transient connector
  throttling first: wait briefly, then retry chat-only and channel-only narrow
  listings separately before marking Teams unavailable.
- If a Teams channel or chat fetch returns an empty body, use the thread preview
  and link/title as partial signal; do not reduce the item to "check manually"
  until a narrow retry has been attempted.
- Asana can be incomplete or stale. Cross-check Asana against Outlook Asana
  notifications and local repo task notes before ranking priorities.
- "Manually check X" is a last-resort output. Prefer either doing the check via
  a narrower connector call or naming the exact unavailable source/tool.
