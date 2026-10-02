---
name: adrez-thread-orchestration
description: Coordinate a non-trivial Adrez project through separate user-owned Codex tasks with one permanent coordinator MAIN, bounded worker lifecycles, compact handoffs, and confirmed worker closure. Use when Martin asks one MAIN task to create, monitor, steer, and close related standalone tasks. Do not use for internal subagents or a small single-outcome task.
metadata:
  scope: business
  status: active
  owner: martin
  last_reviewed: 2026-09-22
  compatibility: Requires Codex app task-management tools.
---

# Adrez Thread Orchestration

Use this skill for project-level coordination through separate Codex tasks in
the sidebar. Tasks are peers. One permanent MAIN provides the project key,
registry, acceptance decisions, and user communication.

## Hard Boundary

- MAIN is a control plane. It may define the charter, maintain the registry,
  create and manage workers, read compact handoffs, inspect targeted evidence,
  make routing and acceptance decisions, and report status.
- MAIN must not edit product files, perform implementation, run normal tests,
  conduct broad repository discovery, or take over unfinished worker work.
- Product integration, conflict resolution, implementation, discovery, and
  verification belong to workers. Use an `INTEGRATE` worker when code or data
  from multiple workers must be combined.
- Use `adrez-agent-orchestration` for local execution, Linear routing,
  branches, worktrees, or internal subagents.
- Do not create or change Linear tracking unless Martin explicitly requests it.

## Guided Start and Mandate

When Martin invokes this skill without a complete project mandate:

1. Ask one short question for the project and desired outcome. Reuse known
   context instead of asking for known facts.
2. Infer the project key, definition of done, scope, constraints, model policy,
   and candidate worker outcomes.
3. Present one compact charter. It requests authority to create, title, monitor,
   steer, and archive workers for the named project.
4. Ask Martin to approve or correct the charter. A plain `ano` approves it.
5. Create workers only after approval. Do not ask again for routine lifecycle
   actions covered by the mandate.

The mandate applies only to the named project. It does not authorize unrelated
external actions, new product scope, or Linear changes. Use the existing Adrez
project specified by the mandate. Resolve its project ID before creation; do not
fall back to a projectless task. Pinning requires a separate explicit request.

There is one permanent MAIN per project. Its task is the user reply destination
and receives every worker result or decision. Do not rotate, replace, or
automatically archive it. A separate user request for a new task is separate
from worker counters and does not alter the current project.

## Naming and Model Policy

Choose a short ASCII project key in uppercase words separated by hyphens.

```text
◆ [PROJECT-KEY] MAIN — project outcome
↳ [PROJECT-KEY/01] DISCOVERY — worker outcome
↳ [PROJECT-KEY/02] IMPLEMENT — worker outcome
↳ [PROJECT-KEY/03] VERIFY — worker outcome
↳ [PROJECT-KEY/04] INTEGRATE — worker outcome
↳ [PROJECT-KEY/05] REVIEW — worker outcome
```

Allowed worker roles are `DISCOVERY`, `IMPLEMENT`, `VERIFY`, `INTEGRATE`,
`REVIEW`, and `DOCS`. Keep titles short and unique. Do not pin tasks unless
Martin explicitly requests it.

- Keep MAIN, implementation, integration, and ambiguous tasks on the configured
  default coding model with medium reasoning.
- A narrow read-only discovery or mechanical verification task may use a faster
  model with low reasoning only when the mandate allows it.
- Do not select `gpt-6-astra` by default. Use it only when Martin explicitly
  authorizes it for a high-consequence or unresolved reasoning problem.

## Worker Eligibility and Isolation

Create a worker only when it has one independent, verifiable outcome, benefits
from isolated context, normally represents 30-60 minutes of work, and has a
non-conflicting write scope. Keep tightly coupled work in one worker.

- Keep at most two workers active at once.
- Use waves. Finish review and closure for the current wave before dispatching
  the next wave.
- Use a separate worktree for every parallel Git writer.
- Assign disjoint write scopes before creating writer tasks. If scopes overlap,
  run them serially or assign one combined outcome.
- Keep discovery, review, and verification read-only unless their prompt grants
  explicit write scope.

## Registry

Keep this compact registry in MAIN:

`No | title | threadId | hostId | project/worktree | write scope | state | fix used | dependency | next action`

Use these worker states:

`PLANNED | STARTING | START_FAILED | START_CANCELLED | ACTIVE | NEEDS_ATTENTION | REVIEW | FIX_REQUESTED | ACCEPTED | SUPERSEDED | ARCHIVE_REQUESTED | ARCHIVED | READY_TO_ARCHIVE`

`STARTING`, `ACTIVE`, `NEEDS_ATTENTION`, `REVIEW`, and `FIX_REQUESTED`
count toward the two-worker limit. They stop consuming capacity only after the
task becomes `ACCEPTED`, `SUPERSEDED`, `ARCHIVE_REQUESTED`, `ARCHIVED`,
`START_FAILED`, `START_CANCELLED`, or is explicitly retained for a reported
blocker. Retention requires evidence that the task cannot run or resume without
coordinator action and an explicit registry reason. Readmit a retained task
within the two-worker limit before it resumes. An unresolved `STARTING` task
stays in capacity.

Keep the registry in task context. Do not create a repository tracking file
unless Martin explicitly requests one. Reconcile it after resume and at the
start of every orchestration turn.

## Worker Prompt Contract

Give every worker:

- one outcome and definition of done;
- project, repository, and path scope;
- read-only status or explicit write ownership;
- constraints, dependencies, and required validation;
- the MAIN thread ID;
- notice that unrelated changes must not be reverted;
- instruction to stop after its outcome and not start the recommended next
  action;
- a direction to report a material scope or priority change to MAIN and pause
  affected work; and
- a direction to send its final result, blocker, stop instruction with verified
  state, or material user clarification to MAIN through
  `send_message_to_thread` when available, with sender ID and result revision.

A worker respects a stop or clarification received in its own task immediately.
It does not treat approval in another task as authority for a new external
action. A stop takes priority over resuming work. If Martin approves a pending
tool dialog after a stop, the worker does not resume; it first verifies the
action's actual state and does not promise cancellation or rollback.

Record whether a worker-to-MAIN delivery is confirmed or uncertain. Before a
retry, check the MAIN task history for the same sender and result revision. MAIN
uses worker messages first; its wait or targeted read is the fallback to surface
an undelivered result. Do not display or process a duplicate result.

A corrected report uses a higher result revision. MAIN re-evaluates the affected
acceptance and holds archival while a decision or follow-up remains unresolved.
A report-only correction needs no new worker. Further work after completion is a
bounded successor outcome with a linked registry entry; do not reopen the
completed worker. Do not unarchive history only to record a correction.

Require this compact final handoff:

```text
Status:
Outcome:
Artifacts or changed files:
Validation:
Decisions:
Risks or blockers:
Recommended next action:
```

Keep the handoff to about ten lines. Do not return raw logs, full diffs, or
browser dumps unless they prove a blocker.

## Enforceable Lifecycle

Use this cycle continuously until the project is done:

```text
RECONCILE -> DISPATCH -> WAIT -> REVIEW -> ARCHIVE WORKERS -> NEXT WAVE | CLOSE
```

### 1. Reconcile

At the start of every orchestration turn:

1. List tasks and match the exact project-key prefix.
2. Reconcile their real state with the registry.
3. Process completed or attention-needed workers before creating workers.
4. Retry an `ARCHIVE_REQUESTED` entry only after reconciliation shows it
   remains unarchived.

Treat archival as confirmed only when the archive action reports completion or
the exact `threadId` appears in the archived-task listing. Absence from the
normal task listing is not proof.

### 2. Dispatch

Create only workers that pass eligibility and the two-worker limit. Creation is
asynchronous. If it returns only a client ID, record `STARTING`. Do not pass a
client ID to tools that require a real `threadId`.

On reconciliation, match a `STARTING` worker from its unique exact title and
project key, then record its real `threadId` and `hostId`. If setup is
explicitly reported failed or cancelled by the create result or matching task
state, record `START_FAILED` or `START_CANCELLED`, with the evidence and
next action. If uncertain, keep it `STARTING`; elapsed time or absence from a
listing is not failure proof. Do not create a speculative replacement or busy
poll.

### 3. Wait

Use one bounded event-driven wait for active workers. Do not busy poll. After a
timeout, report compact status or perform other control-plane work. Do not
replace waiting with repository implementation in MAIN. Do not promise an
unattended future return when no coordinator is active. Use a targeted task read
only when the wait or a worker message does not surface a needed result here.

### 4. Review and Remediation

Review the final handoff and stated validation. Read targeted evidence only when
the handoff is insufficient for acceptance.

A worker may receive at most one targeted remediation follow-up for the same
acceptance criteria. Set `fix used = yes`. Create a successor worker when a
second remediation would be required, criteria change materially, context is
insufficient, or the remaining work is a new deliverable. Record the partial
validation and successor link, then set the original worker to `SUPERSEDED`
when the successor has a real `threadId`.

Do not reuse an accepted or completed worker for a new outcome.

### 5. Archive Workers

When lifecycle authority is active, request archival in the same orchestration
turn for an accepted worker when it submitted its final handoff, is no longer
running, has clear required validation, has no pending approval, user input, or
follow-up, and Martin did not ask to keep it open.

Set `ARCHIVE_REQUESTED` after the archive call. Confirm `ARCHIVED` only from
the archive result or archived-task listing. Also archive an eligible
`SUPERSEDED` worker once its partial handoff, failed validation, and successor
link are recorded. Never archive a running worker, a worker with a pending
approval or question, or MAIN. Never delete a task.

### 6. Handle Blockers and Close

For `NEEDS_ATTENTION`, record the exact blocker and required decision. If the
mandate determines the answer, steer the worker once. Otherwise report the
decision to Martin and leave the worker open. Do not retry unchanged work or
create another worker to reproduce it.

Create the next wave only after every worker in the current wave is accepted,
superseded, archive-requested, archived, start-failed, start-cancelled, or
explicitly retained for a reported blocker.

When the definition of done is met, reconcile all workers, prepare the final
registry and user-facing summary, and request archival for every eligible
worker. Confirm each archival or report unresolved cleanup in the summary. MAIN
remains open for Martin's replies and future status questions.

## Token Discipline

- Pass the smallest context that lets a worker act correctly.
- Perform shared discovery once and pass a concise brief to dependent workers.
- Prefer compact snapshots and final handoffs over full histories.
- Search narrowly and do not create workers to repeat sufficient evidence.

## Stop Conditions

Stop dispatch and return to Martin when the outcome or definition of done is
missing, authority exceeds the mandate, write ownership cannot be isolated, a
worker needs material scope expansion, a blocker needs Martin's decision, or
the next work cannot be expressed as a bounded worker outcome.

## MAIN Status Output

```text
Project: [PROJECT-KEY] — outcome
Mandate: active / missing
Workers: active N/2
Accepted and closing: ...
Active: ...
Needs attention: ...
Decision or next action: ...
```
