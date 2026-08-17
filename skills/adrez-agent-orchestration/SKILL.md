---
name: adrez-agent-orchestration
description: Triage and orchestrate non-trivial Adrez Codex threads into local work, Linear tracking, task branches/worktrees, or explicitly authorized subagent work. Use when the user asks to size or split work, coordinate repositories or phases, create an agent-ready plan, assign ownership, recover from long-session drift, or move an agreed non-trivial task from discussion into implementation with prompts such as "implementuj", "udělej to", or "pokračuj realizací".
scope: business
status: active
owner: martin
last_reviewed: 2026-08-17
---

# Adrez Agent Orchestration

Use this skill as a light intake layer above normal Adrez repo and delivery
skills. It decides the shape of the work before implementation starts.

## Boundary
- Use `adrez-linear-workflow` when the main decision is Linear project/issue
  structure or task updates.
- Use `implementation-review` when the task is reviewing an existing diff,
  branch, PR, milestone, or implementation artifact.
- Use repo/domain skills for execution once the path is clear:
  `entity-spreadsheet-ingestion`, `entity-data-factory`,
  `entity-dbt-cloud`, `powerbi-report-starter`, `repo-pr-handoff`,
  `repo-worktree-safety`, and similar focused skills.
- Do not use this skill for small one-off questions, simple lookups, or
  obvious single-file edits unless the user explicitly asks for orchestration.

## Intake Workflow
1. Restate the target outcome in one sentence.
2. Classify the thread with the triage levels below.
3. Pick the execution mode:
   - local only,
   - local plus Linear tracking,
   - task branch/worktree,
   - planned subagent delegation,
   - or follow-up project/issue planning.
4. Declare the delivery target: local implementation, pushed branch and PR,
   merged `main`, or deployment. Do not infer a later stage from `udělej`.
5. Name the owner of each slice: main agent, human, Linear issue, or subagent
   role.
6. Define the immediate next local action. Keep blocking work local instead of
   delegating it away.

## Triage Levels
- **1 tiny**: explanation, lookup, command output, or small text edit. No
  Linear, no branch, no subagent.
- **2 small**: one repo, clear scope, low risk, likely one short patch or check.
  Work locally; create a branch only if repo policy requires it.
- **3 tracked**: multi-step, user-facing, data/infra/reporting impact, or likely
  useful across threads. Use `adrez-linear-workflow` unless the user opts out.
- **4 parallelizable**: independent slices exist, write scopes can be disjoint,
  or read-only exploration can run beside local work. Propose or use subagents
  only when the user explicitly asks for agents, delegation, or parallel work.
- **5 project**: long-running area, more than three likely issues, cross-repo
  coordination, or uncertain business scope. Use `adrez-linear-workflow` to
  draft a project/parent issue and avoid starting broad implementation first.

## Delegation Rules
- Spawn subagents only when the user explicitly authorizes subagents,
  delegation, or parallel agent work in this thread.
- Start with at most two subagents in each wave. Keep one concurrency slot
  free for follow-up work and coordination.
- Review the first wave before spawning another wave. Spawn more agents only
  when unresolved work is still independent and the expected value is clear.
- Stop or interrupt redundant, stalled, or looping agents. Do not use more
  agents to repeat evidence that is already sufficient for a decision.
- Delegate sidecar work that can run independently while the main agent handles
  the critical path.
- Do not delegate the next blocking step if the main agent needs its result
  immediately.
- Give every delegated task:
  - concrete output,
  - repo/path scope,
  - read-only or write ownership,
  - validation expectation,
  - and a handoff format.
- For write tasks, split by disjoint files or modules. Tell workers they are not
  alone in the codebase and must not revert unrelated edits.
- Prefer read-only explorer roles for broad discovery and worker roles for
  bounded patches.

## Task-Lifetime Wave Ledger

When subagents are used, keep one ledger for the full parent task:

`Wave | subagents started | scope | status | evidence reviewed | decision`

- Carry the ledger across context compaction, resumed work, and follow-up
  turns. Count replacement agents and child-spawned agents in the same totals.
- Before each later wave, reconcile all prior agents, results, and unresolved
  scopes. Prefer a follow-up to an existing agent over spawning a replacement.
- Start another wave only for a distinct unresolved scope with a clear
  advantage over local work. Do not use another wave to repeat sufficient
  evidence.
- Stop after three waves or six total spawned agents. Summarize the evidence
  and remaining scopes. Continue delegation only after Martin renews
  authorization in the current thread.
- After Martin corrects or narrows scope, update the ledger before more tool
  calls or delegation. Stop and restate the current in-scope and out-of-scope
  work when repeated corrections show session drift.

## Standard Role Set
- **main agent**: owns the critical path, integration, final judgment, and user
  communication.
- **explorer**: answers one scoped codebase/data/process question without edits.
- **worker**: implements one bounded slice with explicit write ownership.
- **reviewer**: checks correctness, regressions, validation, and scope leaks.
- **verifier**: runs or inspects validation that can happen in parallel.

## Delivery checkpoint

- Before implementation, name the target remote/base and required final state.
- For same-repo concurrency, route execution through `repo-worktree-safety`.
- Before delivery, route through `repo-pr-handoff` and require exact SHA proof
  for every requested stage.
- Before handoff, run proportionate validation and inspect the current-task
  diff.
- At final handoff, state local, remote branch, PR, `main`, deployment, and
  cleanup separately. If a stage was not requested or reached, say so.

## Output Shape
For a normal orchestration response, keep it short:

```md
Triage: level N - reason.
Mode: local / tracked / branch / parallel / project.
Delivery target: local / PR / main / deployment.
Slices:
- Main agent: ...
- Optional subagent role: ...
Immediate next action: ...
Tracking: none / Linear issue / existing issue.
Required proof: base SHA / remote SHA / PR head / main SHA / deployment ID.
Wave ledger: none / current wave and cumulative agent count.
```

For large ambiguous work, ask at most one clarification question. If a safe
assumption exists, state it and proceed.
