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
| `daily-brief.md` | Durable morning-brief policy and latest durable corrections; not a daily brief archive. |
| `open-loops.md` | Cross-repo blockers, waiting items, PRs, and Linear follow-ups. |
| `pipeline-watch.md` | Pipeline/status email patterns and watch items. |
| `people-followups.md` | People and threads that likely need a reply. |
| `decisions.md` | Stable operating decisions that affect future brief behavior. |
| `thread-handoff-template.md` | Prompt template for starting a focused new Codex thread. |

## Chief Of Staff Brief Contract

The daily brief should be short enough to fit on one screen.

Daily morning-brief output and raw run notes belong in automation memory, not in
this repository:

- `$CODEX_HOME/automations/adrez-chief-of-staff-morning-brief/memory.md`

`agents/ops` is for durable operating state only. A morning run may update these
files only when the change should affect future ranking, suppression, open-loop
tracking, or people follow-up behavior.

The brief must distinguish:
- confirmed facts from inferred priorities
- actionable items from parked or waiting context
- connector gaps from true absence of signals

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
- Write back only concise durable state that will matter tomorrow; do not
  persist the full daily brief here.
- If a morning run changes tracked files under `agents/ops`, make a focused git
  commit or explicitly say the repo was left dirty because Martin asked.
- Before ranking priorities, apply the latest Martin corrections in
  `daily-brief.md`, `open-loops.md`, `pipeline-watch.md`, and
  `people-followups.md`; never resurface a corrected item unless a newer source
  reopens it.
- Do not turn a `Done`, `Resolved`, `Waiting`, `Parked`, or
  "Martin handles separately" item into a top priority unless there is a fresh
  same-day trigger.
- If a recommendation is inferred from data rather than explicitly requested by
  Martin or another person, label it as an inference.

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
   - Linear for assigned tasks, due-soon work, recently completed work, and
     project/issue status
4. GitHub / CI:
   - only when directly referenced by ops memory, Outlook, Teams, Linear, or a
     recent task note

## Ranking Rules

Rank an item high only when at least one is true:
- it blocks today's scheduled work
- it requires Martin's reply or decision
- it is a fresh production, billing, pipeline, or reporting risk
- Martin corrected it into today's focus
- it has an explicit due date today or tomorrow

Down-rank or omit an item when:
- ops memory marks it `Done`, `Resolved`, `Waiting`, `Parked`, or handled by
  Martin
- the only source is legacy Asana or task-note state contradicted by newer ops
  memory
- it is a recovered pipeline with no new failure
- it is useful background but has no next action today
- it is technically true, but ownership is external or Martin already said he
  will handle it separately

## Connector Handling

- Teams broad chat listing can timeout. Start with small pages (`top=1`) and
  expand only if each call succeeds.
- If Teams returns Microsoft Graph 429, treat it as transient connector
  throttling first: wait briefly, then retry chat-only and channel-only narrow
  listings separately before marking Teams unavailable.
- If a Teams channel or chat fetch returns an empty body, use the thread preview
  and link/title as partial signal; do not reduce the item to "check manually"
  until a narrow retry has been attempted.
- Treat empty Teams notification bodies as unknown status, not success and not
  failure. Escalate only if another source suggests an incident.
- Do not query Asana in routine briefs. It is a historical archive only; use it
  only when Martin explicitly asks for a legacy URL/GID or historical context.
- If Outlook surfaces an old Asana notification with unresolved underlying
  work, find the owning Linear issue before ranking it as active. If none
  exists, surface the migration need and create one only with explicit Martin
  approval.
- "Manually check X" is a last-resort output. Prefer either doing the check via
  a narrower connector call or naming the exact unavailable source/tool.
- When a connector is unavailable, output the exact unavailable source/tool and
  what could not be verified; do not infer "no signal" from connector failure.
