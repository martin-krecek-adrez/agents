---
name: adrez-thread-orchestration
description: Coordinate a non-trivial Adrez project through separate user-owned Codex tasks visible in the sidebar. Use when Martin asks one MAIN task to create, name, monitor, steer, and close related standalone tasks. Do not use for internal subagents or small single-outcome work.
scope: business
status: active
owner: martin
last_reviewed: 2026-08-24
compatibility: Requires Codex app task-management tools.
---

# Adrez Thread Orchestration

Use this skill for project-level coordination through separate Codex tasks.
These tasks are peers in the app. The MAIN task provides their logical
hierarchy, shared project key, registry, and integration.

## Boundary

- Use `adrez-agent-orchestration` for intake, local execution, Linear routing,
  branches, worktrees, or internal subagents.
- Use this skill only when Martin explicitly wants standalone tasks in the
  sidebar or authorizes a MAIN task to create them for one named project.
- Do not create a standalone task for a lookup, micro-step, or tightly coupled
  work that should remain in one task.
- Do not create or change Linear tracking unless Martin explicitly requests it.

## Guided Start

When Martin invokes this skill with little project detail, guide the setup:

1. Ask one short question for the project and desired outcome. Use known
   workspace context instead of asking for information that is already known.
2. Infer a project key, definition of done, likely scope, and candidate worker
   outcomes. Ask one follow-up only when a missing fact changes the plan.
3. Present one compact charter with:
   - project name and key;
   - outcome and definition of done;
   - scope and important constraints;
   - the mandate to create, title, pin, monitor, steer, and archive tasks;
   - the proposed model policy;
   - the proposed initial task split.
4. Ask Martin to approve or correct the charter. A plain `ano` is sufficient
   approval for that project mandate.
5. Create tasks only after approval. Do not request the same authorization for
   each worker covered by the mandate.

If Martin already supplied enough information and an explicit mandate, proceed
without repeating intake. If the outcome is clear but the mandate is missing,
propose the charter and ask only for approval.

## Project Mandate

Obtain an explicit mandate for the current project before creating any task.
The mandate can authorize the MAIN task to create, title, pin, monitor, steer,
and archive related tasks. It does not carry to another project or authorize
unrelated external actions.

If the mandate is missing or unclear, propose task names without creating them.
Archive a worker only after its handoff is accepted, validation is reviewed,
and no follow-up remains. Never delete a task.

## Eligibility Gate

Create a worker task only when all applicable conditions hold:

- It has one independent, verifiable outcome and a clear definition of done.
- It benefits from isolated context or can progress independently.
- It normally represents at least 30-60 minutes of work.
- Its write scope does not conflict with another active task.

Keep dependent micro-steps and tightly coupled work in MAIN or in one existing
worker. Reuse a worker for follow-up on the same outcome.

## Naming Convention

Choose a short, stable ASCII project key. Use uppercase words separated by
hyphens. Add a run suffix such as `-R2` for a later independent run.

Use these titles:

```text
◆ [PROJECT-KEY] MAIN — project outcome
↳ [PROJECT-KEY/01] DISCOVERY — worker outcome
↳ [PROJECT-KEY/02] IMPLEMENT — worker outcome
↳ [PROJECT-KEY/03] VERIFY — worker outcome
↳ [PROJECT-KEY/04] REVIEW — worker outcome
```

Allowed worker roles are `DISCOVERY`, `IMPLEMENT`, `VERIFY`, `REVIEW`, and
`DOCS`. Keep titles short and unique. The ASCII project segment is the primary
identifier. If the app mishandles the symbols, omit only the symbols.

Pin MAIN. Do not pin workers unless Martin requests it.

## Model Policy

- Keep MAIN, implementation, integration, and ambiguous tasks on the default
  frontier coding model with medium reasoning.
- A narrow read-only discovery or mechanical verification task may use a
  faster model with low reasoning only when the project mandate allows it.
- Do not infer a cheaper model for work that edits files or makes consequential
  decisions.

Subagent defaults do not control standalone sidebar tasks.

## Concurrency and Worktrees

- Keep at most two worker tasks active at once.
- Use waves. Review the current wave before creating another one.
- Use a separate worktree for every parallel Git writer.
- Assign disjoint write scopes before creating writer tasks.
- If scopes overlap, run tasks serially or combine them.
- Keep review and discovery read-only unless their prompt assigns write scope.

Stop after three waves or six created worker tasks. Continue only after Martin
renews the mandate for the current project.

## MAIN Registry

Keep a compact registry in MAIN:

`No | title | threadId | hostId | project/worktree | write scope | status | dependency | next step`

Do not create a repository tracking file unless Martin explicitly requests a
durable artifact. Carry the registry through compaction and resumed turns.
After resume, reconcile it with the current task list by project-key prefix.

## Worker Prompt Contract

Give every worker:

- one outcome and definition of done;
- project, repository, and path scope;
- read-only or explicit write ownership;
- constraints and dependencies;
- required validation;
- the handoff format below;
- notice that unrelated changes must not be reverted.

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

Keep the handoff to about ten lines when possible. Do not return raw logs,
complete transcripts, full diffs, or browser dumps unless they prove a blocker.

## Lifecycle

1. Define the outcome, constraints, verification, and project mandate.
2. Select the project and stable project key.
3. Split only independent outcomes that pass the eligibility gate.
4. Inspect Git state and isolate parallel writers with worktrees.
5. Create no more than two workers in the current wave and record their IDs.
6. Use event-driven task waiting with one bounded wait for the active set.
7. Review each compact handoff and read more only when evidence is insufficient.
8. Send follow-up to the same worker when the same outcome needs more work.
9. Update the registry and decide whether another wave is justified.
10. Integrate or hand off the result. Archive eligible workers and MAIN last
    when the mandate includes lifecycle management.

The MAIN task is not a permanent daemon. After a bounded wait times out, avoid
busy polling. Continue useful local coordination or return a compact status.

## Token Discipline

- Pass the smallest context that lets a worker act correctly.
- Perform shared discovery once and pass a concise brief to dependent workers.
- Prefer compact status snapshots and final handoffs over full histories.
- Do not create workers only to repeat evidence that is already sufficient.

## Stop Conditions

Stop task creation and return to Martin when:

- the project outcome or definition of done is missing;
- required authority exceeds the project mandate;
- write ownership conflicts cannot be isolated;
- a worker needs a material scope expansion;
- three waves or six workers have been reached;
- the next work is dependent rather than independently executable.

## MAIN Status Output

Use this shape:

```text
Project: [PROJECT-KEY] — outcome
Mandate: active / missing / renewal required
Wave: N; active workers: N/2; total workers: N/6
Completed: ...
Active: ...
Blocked: ...
Decision or next action: ...
```
