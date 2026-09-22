---
name: adrez-thread-orchestration
description: Coordinate a non-trivial Adrez project through separate user-owned Codex tasks, with a coordinator-only MAIN, bounded worker lifecycles, compact handoffs, and automatic worker closure. Use when Martin asks one MAIN task to create, monitor, steer, and close related standalone tasks. Do not use for internal subagents or a small single-outcome task.
metadata:
  scope: business
  status: active
  owner: martin
  last_reviewed: 2026-09-22
  compatibility: Requires Codex app task-management tools.
---

# Adrez Thread Orchestration

Use this skill for project-level coordination through separate Codex tasks in
the sidebar. These tasks are peers. MAIN supplies their logical hierarchy,
project key, registry, acceptance decisions, and lifecycle management.

## Hard Boundary

- MAIN is a control plane. It may define the charter, maintain the registry,
  create and manage tasks, read compact handoffs, inspect targeted evidence,
  make routing and acceptance decisions, and report status.
- MAIN must not edit product files, perform implementation, run normal tests,
  conduct broad repository discovery, or take over unfinished worker work.
- Product integration, conflict resolution, implementation, discovery, and
  verification belong to workers. Use an `INTEGRATE` worker when code or data
  from multiple workers must be combined.
- Put tightly coupled implementation steps in one worker. If the work cannot be
  isolated into a worker outcome, do not use this skill for that work.
- Use `adrez-agent-orchestration` for local execution, Linear routing,
  branches, worktrees, or internal subagents.
- Do not create or change Linear tracking unless Martin explicitly requests it.

## Guided Start and Mandate

When Martin invokes this skill without a complete project mandate:

1. Ask one short question for the project and desired outcome. Reuse known
   context instead of asking for known facts.
2. Infer the project key, definition of done, scope, constraints, model policy,
   and candidate worker outcomes.
3. Present one compact charter. It must explicitly request authority to create,
   title, monitor, steer, archive workers, and, when required, rotate
   related tasks for this named project. Pinning requires a separate explicit
   user instruction; general charter approval does not authorize pinning.
4. Ask Martin to approve or correct the charter. A plain `ano` approves that
   project mandate.
5. Create tasks only after approval. Do not ask again for routine lifecycle
   actions covered by the mandate.

The mandate applies only to the named project. It does not authorize unrelated
external actions, new product scope, or Linear changes. If lifecycle authority
is missing, do not archive workers or rotate tasks. Mark workers
`READY_TO_ARCHIVE` and ask once when closure is otherwise ready. Never archive
a MAIN automatically. Archive a MAIN only after its result and successor or
closure state are visible and Martin explicitly asks.

## Worker Eligibility

Create a worker only when all applicable conditions hold:

- It has one independent, verifiable outcome and a clear definition of done.
- It benefits from isolated context or can progress independently.
- It normally represents at least 30-60 minutes of work.
- Its write scope does not conflict with another active task.

Do not create a worker for a lookup or coordination micro-step. Do not move the
micro-step into MAIN when it edits the repository, runs tests, or changes the
deliverable. Keep it in the worker that owns the outcome.

## Naming

Choose a short ASCII project key in uppercase words separated by hyphens. Keep
this root key stable across rotations. Record a monotonic run number, starting
at 1. Run 1 may omit the suffix in titles. Later runs use `-R<N>` consistently
in MAIN and worker titles, the registry, and handoffs. Never append a run suffix
to an already suffixed key. Reserve each successor run number before creation;
never reuse it, including after a confirmed setup failure.

```text
◆ [PROJECT-KEY] MAIN — project outcome
↳ [PROJECT-KEY/01] DISCOVERY — worker outcome
↳ [PROJECT-KEY/02] IMPLEMENT — worker outcome
↳ [PROJECT-KEY/03] VERIFY — worker outcome
↳ [PROJECT-KEY/04] INTEGRATE — worker outcome
↳ [PROJECT-KEY/05] REVIEW — worker outcome
```

Allowed worker roles are `DISCOVERY`, `IMPLEMENT`, `VERIFY`, `INTEGRATE`,
`REVIEW`, and `DOCS`. Keep titles short and unique. Pin a MAIN or worker only
when Martin explicitly requests it. Keep tasks under the existing Adrez project
as specified by the mandate. Resolve its project ID through `list_projects`
before creation; do not create projectless tasks as a fallback.

## Model Policy

- Keep MAIN, implementation, integration, and ambiguous tasks on the configured
  default coding model with medium reasoning.
- A narrow read-only discovery or mechanical verification task may use a faster
  model with low reasoning only when the mandate allows it.
- Do not select `gpt-6-astra` by default. Use it only when Martin explicitly
  authorizes it for the current task. Reserve it for high-consequence
  architecture, cross-repository decisions, or a hard reasoning blocker that
  the default model could not resolve.
- When Astra resolves a narrow decision, pass a compact decision record to the
  default model for routine implementation and verification.

Subagent defaults do not control standalone sidebar tasks.

## Concurrency and Write Isolation

- Keep at most two worker tasks active at once.
- Use waves. Finish review and closure for the current wave before dispatching
  the next wave.
- Use a separate worktree for every parallel Git writer.
- Assign disjoint write scopes before creating writer tasks.
- If scopes overlap, run the workers serially or give one worker the combined
  outcome.
- Keep discovery, review, and verification read-only unless their prompt grants
  an explicit write scope.

Count waves and created workers per MAIN run. Record each worker's owning run,
including failed/cancelled setup attempts and retries. A confirmed successor
starts at zero waves and zero created workers for its new run. Preserve the
full registry and prior run counters as history, not as its new run budget.
Any carried active workers still consume the shared two-worker capacity.

Stop the current MAIN after three waves or six created workers. If the active
mandate includes rotation, continue through a successor MAIN run without a new
approval. If rotation is missing from the mandate, ask once. Do not extend the
current MAIN.

## Registry

Keep this compact registry in MAIN:

`No | title | threadId | hostId | project/worktree | write scope | state | fix used | dependency | next action`

Also record `origin MAIN threadId` and `current MAIN threadId`. They are the
same at the first run. The origin MAIN is the stable result/status destination
through every rotation. The current MAIN is the instruction and user reply
destination after confirmed rotation. Record the stable root project key,
current run number, and highest reserved run number. Record each return's
project/run, sender ID, stable result ID or monotonic result revision, kind as
separate metadata, and whether delivery is confirmed or uncertain.

Use these worker states:

`PLANNED | STARTING | START_FAILED | START_CANCELLED | ACTIVE | NEEDS_ATTENTION | REVIEW | FIX_REQUESTED | ACCEPTED | SUPERSEDED | ARCHIVE_REQUESTED | ARCHIVED | READY_TO_ARCHIVE`

`STARTING`, `ACTIVE`, `NEEDS_ATTENTION`, `REVIEW`, and `FIX_REQUESTED`
count toward the two-worker limit. They stop consuming capacity only after the
task becomes `ACCEPTED`, `SUPERSEDED`, `ARCHIVE_REQUESTED`, `ARCHIVED`, or is
explicitly retained outside the current wave for a reported blocker. A confirmed
`START_FAILED` or `START_CANCELLED` also releases its slot. Retention outside
the wave requires recorded evidence that the task cannot run or resume without
coordinator action, a blocker report, and an explicit registry retention entry.
An unresolved `STARTING` task stays in capacity because it may still start. A
retained task cannot resume until it is readmitted within the two-worker limit.
Retention does not erase its creation from its owning run's six-worker budget.

Keep the registry in task context. Do not create a repository tracking file
unless Martin explicitly requests one. Reconcile the registry after resume and
at the start of every orchestration turn.

## Worker Prompt Contract

Give every worker:

- one outcome and definition of done;
- project, repository, and path scope;
- read-only status or explicit write ownership;
- constraints and dependencies;
- required validation;
- the compact handoff format below;
- notice that unrelated changes must not be reverted;
- instruction to stop after the stated outcome and not start the recommended
  next action;
- current MAIN thread ID; and
- a direction to report a material scope or priority change to the current MAIN
  and pause affected work.

A worker respects a stop or clarification received in its own task immediately.
It does not treat an approval in another task as authority for a new external
action. A stop takes priority over resuming work. If Martin approves a pending
tool dialog after a stop, the worker does not resume; it first verifies the
action's actual state and does not promise cancellation or rollback.

```text
Status:
Outcome:
Artifacts or changed files:
Validation:
Decisions:
Risks or blockers:
Recommended next action:
```

Keep the handoff to about ten lines when possible. Do not return raw logs,
complete transcripts, full diffs, or browser dumps unless they prove a blocker.

## User Continuity

The current MAIN is the only worker coordinator and normal reply destination.
At creation and after a completed rotation, show Martin the exact title and a
direct link to the current MAIN. Do not assume that the app redirects replies.

When Martin writes in an older MAIN, relay a compact stop, correction, or new
instruction once to the recorded current MAIN, then stop coordination in the
older MAIN. For a stop, do not claim remote work stopped until task state proves
it. The older MAIN does not create workers, reopen work, or become a second
coordinator. A source MAIN respects a stop received in its own task immediately.

While a successor is `STARTING`, the older MAIN holds new user instructions and
does not dispatch. After the successor has a real ID and accepted handoff, it
passes only that instruction delta. It does not invent a successor link. A
concrete user instruction may be relayed without asking Martin to repeat it;
an approval required by a tool remains local to that tool.

An origin MAIN may answer "what is done" from a fresh read-only task snapshot
with a link to the current MAIN. It does not rotate, reopen work, or coordinate.

## Enforceable Lifecycle

Use this state cycle:

```text
RECONCILE -> DISPATCH -> WAIT -> REVIEW -> ARCHIVE WORKERS -> NEXT WAVE | ROTATE | CLOSE
```

### 1. Reconcile

At the start of every orchestration turn:

1. List tasks and match the project-key prefix. Resolve any `STARTING` worker
   from its unique exact title, stable project key, and reserved run number.
2. Reconcile their real state with the registry.
3. Process completed or attention-needed workers before creating new workers.
4. Retry an earlier `ARCHIVE_REQUESTED` state only after reconciliation shows
   that the task remains unarchived.

Treat archival as confirmed only when the archive action reports completion or
the exact `threadId` appears in the archived-task listing. Absence from the
normal task listing is not proof. Page the archived listing when necessary. Do
not claim that a background archive request completed until positive evidence
confirms it.

### 2. Dispatch

Create only workers that pass the eligibility gate and current concurrency
limit. Task creation is asynchronous. If creation returns only a client task
identifier, record the worker as `STARTING`. Do not pass that identifier to
wait, read, message, or archive tools that require a real `threadId`. On a later
reconciliation, use the task listing to match the unique exact title and project
key and run number and record the real `threadId` and `hostId`. If setup is
explicitly reported failed or cancelled by the create result or a matching task
status, record `START_FAILED` or `START_CANCELLED`. Preserve the client ID,
exact title, run number, and observed evidence. Report the blocker and required
next action. These terminal setup entries are retained outside wave capacity
and do not block wave closure. A new attempt needs a distinct registry entry
and title, consumes its owning run's worker creation budget, and must address
the cause within the mandate; do not retry an unchanged blocker. If failure or cancellation
is uncertain, leave it `STARTING`, keep its capacity reservation, and report
unresolved setup. Absence from a listing or elapsed time is not failure proof.
Do not create a speculative replacement or busy poll. Apply the same setup
rules to a successor MAIN; a confirmed failed attempt does not transfer the
coordinator role. Keep user instruction deltas with the predecessor until a
successor accepts the handoff.

### 3. Wait

Use one bounded event-driven wait for the active worker set. Do not busy poll.
After a timeout, report compact status or perform other control-plane work. Do
not replace waiting with repository implementation in MAIN.

### 4. Review and Remediation

Review the final handoff and its stated validation. Read additional task output
or targeted repository evidence only when the handoff is insufficient for an
acceptance decision.

A worker may receive at most one targeted remediation follow-up for the same
acceptance criteria. Set `fix used = yes`. Create a successor worker with a
compact handoff when:

- a second remediation would be required;
- the outcome or acceptance criteria change materially;
- the worker reports insufficient context; or
- the remaining work is a new deliverable.

When a successor is required because the original worker did not meet the
acceptance criteria, capture the failed or partial validation and the successor
link. Wait until the successor has a real `threadId`, then set the original
worker to `SUPERSEDED`. Do not leave the original worker open for more fixes.

Do not reuse an accepted or completed worker for a new outcome.

### 5. Archive Workers

When lifecycle authority is active, request worker archival in the same
orchestration turn when all conditions hold:

- the worker submitted its final handoff and is no longer running;
- required validation is clear and accepted;
- the outcome and decisions are captured in the registry;
- no approval, user input, or follow-up is pending; and
- Martin did not ask to keep the task open.

Set the state to `ARCHIVE_REQUESTED` after the archive call. Confirm `ARCHIVED`
only from the archive result or archived-task listing.

Also archive a `SUPERSEDED` worker in the same turn when its final or partial
handoff, failed validation, and successor link are recorded; the successor has
a real `threadId`; the original worker is no longer running; and no approval or
Martin decision is pending. Never archive a running worker or a worker that
needs Martin's decision.

### 6. Handle Blockers

For `NEEDS_ATTENTION`, record the exact blocker and required decision. If the
mandate already determines the answer, steer the worker once. Otherwise report
the decision to Martin and leave the worker open. Do not retry unchanged work
or create another worker to reproduce the same blocker.

### 7. Next Wave or Close

Create the next wave only after every worker in the current wave is accepted,
superseded, archive-requested, archived, confirmed setup-failed/cancelled, or
explicitly retained for a reported blocker under the Registry conditions.

When the project definition of done is met:

1. Reconcile all workers.
2. Prepare the final registry and user-facing summary.
3. Request archive for every eligible worker not already closed.
4. Return the prepared final summary. Never delete a task or automatically
   archive a MAIN.

## MAIN Rotation

The task API does not expose reliable per-task context or token usage and cannot
invoke `/compact`. Do not invent a context percentage or claim automatic
compaction.

Rotate based on observable events. A successor MAIN is required when work must
continue after three waves or six workers. If the active mandate includes
rotation, create the successor without another approval. Ask Martin only when
rotation authority is missing or the product scope changes materially. Then:

1. Prepare a compact charter, registry, decisions, active blockers, next action,
   origin/current MAIN IDs, stable root project key, and run counters.
2. Reserve `N = highest reserved run number + 1`. Create `[PROJECT-KEY-R<N>]
   MAIN` under the same Adrez project with that full handoff in its creation prompt.
   For example, two successful rotations use root `PROJECT-KEY`, runs 1 -> 2 -> 3,
   and MAIN titles `[PROJECT-KEY]`, `[PROJECT-KEY-R2]`, `[PROJECT-KEY-R3]`.
   The registry and each handoff carry those same run numbers.
   Do not resend the same handoff after creation.
3. Confirm a real successor thread ID and a task snapshot showing that the
   successor received the handoff and accepts the coordinator role. A title
   match or handoff marker alone is not proof.
4. Record it as current MAIN, show Martin a direct link and reply destination,
   and retain the predecessor as a source MAIN. Do not automatically archive it.

After that confirmation, if the predecessor is the origin MAIN, update its
registry and user notice without self-sending. Otherwise, the predecessor sends
the origin MAIN one informational current-MAIN update with project/run,
predecessor ID, successor ID, and link. It records a failed or timed-out
delivery as uncertain, not sent. Before a retry, check destination task history.
Do not echo duplicates.

Carry origin MAIN ID and current MAIN ID through every later rotation. When a
current MAIN other than the origin has a completed result or needs Martin's
decision, it sends one informational return message to the origin MAIN after
checking prior delivery history. The return includes project/run, sender ID,
a stable result ID or monotonic result revision, kind as separate metadata,
result, validation, decision needed if any, and a link
to the current MAIN. Record success only when delivery is confirmed; a timeout
is uncertain. Before a retry, check destination task history. This is best-effort
duplicate prevention, not exactly-once delivery.

Accept a return only from a known successor in the registry; a textual marker
alone is not authority. If a later successor was not announced, verify the
chain from the last known MAIN through its task handoff before accepting the
return. Do not block Martin while that targeted check runs. Compare an accepted
return's stored project/run, sender ID, and stable result ID or result revision
before display. A retry of the same result must reuse this identity. A corrected
result must use a new result ID or a higher revision, even when its kind is still
`completed`. Never deduplicate on kind alone. Ignore a later duplicate with the
same identity; do not display or process it again. If the same identity carries
a changed payload, report the conflict and request a new identity rather than
silently discarding the correction. When current equals origin, do not self-send
a return.

The origin MAIN shows the return briefly. It does not echo it, create workers,
reopen work, or resume coordination. The current MAIN remains the reply
destination. Do not renew the same MAIN indefinitely.

## Token Discipline

- Pass the smallest context that lets a worker act correctly.
- Perform shared discovery once and pass a concise brief to dependent workers.
- Prefer compact task snapshots and final handoffs over full histories.
- Search narrowly. Read only the files and line ranges required for the current
  decision.
- Keep tool output bounded. Use filtered excerpts or summaries instead of full
  logs, schemas, documents, repository listings, or diffs.
- Do not create workers to repeat evidence that is already sufficient.

## Stop Conditions

Stop dispatch and return to Martin when:

- the project outcome or definition of done is missing;
- required authority exceeds the mandate;
- write ownership conflicts cannot be isolated;
- a worker needs material scope expansion;
- a blocker requires Martin's decision;
- three waves or six workers have been reached and rotation authority is
  missing; or
- the next work cannot be expressed as a bounded worker outcome.

## MAIN Status Output

```text
Project: [PROJECT-KEY] — outcome
Mandate: active / missing / renewal required
Current MAIN: title + thread link
Run: R<N>; run waves: N/3; active workers across runs: N/2; run created workers: N/6
Accepted and closing: ...
Active: ...
Needs attention: ...
Decision or next action: ...
```
