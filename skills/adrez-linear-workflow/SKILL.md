---
name: adrez-linear-workflow
description: Track actual Adrez work in Linear automatically. Use at the start, material progress, and handoff of implementation, investigation, or deliverable work; reuse or create the owning issue and maintain its assignee and state. Also use for explicit Linear requests. Skip pure questions and respect explicit read-only or no-Linear instructions.
scope: business
status: active
owner: martin
last_reviewed: 2026-10-02
---

# Adrez Linear Workflow

## Purpose
Use Linear as a lightweight task starter and task noter for Adrez work. Keep it useful for humans and agents without turning it into heavy project management.

Default team is `Data Engineering` for almost all Adrez data, analytics, reporting, dbt, ingestion, platform-adjacent, and agent/data-product work. Use another team only when the user explicitly asks or the work is clearly outside this flow.

For Data Engineering work, read
[`references/data-engineering-portfolio.md`](references/data-engineering-portfolio.md)
before selecting or changing a project or initiative. Route by the primary
business outcome or platform capability, not by repository name.

## Boundary
- Linear is the only active tool for Adrez task planning and tracking.
- Asana is retired. Do not create tasks/subtasks, reopen work, or scan it as an
  active queue.
- Use `asana` only when Martin explicitly provides a legacy URL/GID or asks
  for historical context.
- If legacy Asana context reveals active work, first find any existing Linear
  tracking. Propose migration when none exists; create or update Linear only
  when Martin has authorized tracking, and keep the Asana item archival.

## When To Use
- User asks to create, update, organize, or inspect Linear projects/issues.
- User asks to migrate, summarize, or link Asana/task context into Linear.
- User starts non-trivial Adrez work that likely needs tracking across threads.
- User gives a loose spoken/written requirement and wants help turning it into an actionable task.
- Work produces a PR, dbt model, report, ingestion config, infrastructure change, analysis deliverable, or multi-step handoff.

Skip Linear for pure questions, explanations, and one-off lookups that produce
no work deliverable. Small implementation edits still use the owning issue.
An explicit read-only or no-Linear instruction overrides automatic tracking.

## Thread Intake
Martin has authorized automatic tracking for actual Adrez work. Do not ask
whether to create an issue or post a routine work update.

1. Resolve the owning issue in this order: an issue ID/URL from the user or
   current thread; an issue linked to the exact branch/worktree or PR; a search
   by repository and the concrete outcome. Inspect matches before creating.
2. Reuse the matching issue. Create one only when no matching issue exists.
   If ownership remains ambiguous, continue independent local work and ask one
   focused ownership question. Do not create a competing issue by default.
3. Use `Data Engineering` and the existing project that owns the outcome.
   Assign new or unassigned work to Martin. Preserve another existing assignee
   unless the user explicitly asks to transfer ownership.
4. Move work to `In Progress` when execution starts. Keep the issue URL in the
   task handoff. The main agent owns tracking for internal subagents.
5. Post one concise update for material progress: completed validation,
   a blocker, a scope or ownership change, or a delivery link. Do not post on
   every tool call and do not repeat an unchanged update.
6. Use `In Review` while user review or the agreed delivery is pending. Use
   `Done` only when the issue acceptance criteria and agreed delivery are met.
   Never present a local patch as pushed, merged, or deployed. Preserve the
   terminal state of historical issues; use a linked follow-up for new work.

After an ambiguous create/update result, read Linear to reconcile the outcome
before retrying. Never retry creation blindly. If Linear is unavailable,
continue safe local work and report the tracking gap; do not claim it was saved.
Automatic tracking does not authorize new scope, production mutations, or
messages outside the owning Linear issue. Explicit read-only and no-Linear
instructions always take precedence.

## Project Vs Issue Vs Child Issue
Create a **project** when:
- It is a long-running area of work.
- It will likely contain more than three issues.
- Multiple future threads/agents will need the same context.
- Historical links, status, milestones, or project updates should live in one place.

Create an **issue** when:
- There is a concrete task or slice with a clear outcome.
- A human or agent can work it independently.
- It belongs under an existing project or is a standalone operational task.

Create a **child issue** when:
- A parent issue already exists.
- The child is a concrete implementation slice.
- The parent would become too broad or noisy.
- The work is actually starting soon, not just theoretically possible.

Add a **comment/update** instead of creating a new issue when:
- The issue already exists and the current thread changed its state.
- Work found a blocker, produced a PR, changed scope, or left a useful handoff.
- The update is operational progress rather than a new unit of work.

Before creating a new project or issue, search existing Linear projects/issues with likely names to avoid duplicates.

For Data Engineering issues:
- Assign an existing project whenever the work has a clear durable owner.
- Leave an issue without a project only when it is a small standalone operation
  or its ownership is genuinely unresolved.
- When work crosses projects, assign it to the project that owns the primary
  outcome. Use related or blocking links for the other dependencies.
- Do not force every project into an initiative. Initiatives are the selected
  executive-reporting layer, not a required folder for every project.

## Project Template
Use this shape for long-running projects. Keep it shorter when the project is simple.

```md
## Goal
Long-term outcome of the project.

## Scope
Types of issues that belong here.

## Current state
What already exists.

## Legacy links
Asana, docs, old tasks, source folders, or previous decisions.

## Operating rules
When to create child issues, milestones, or updates.

## Open questions
Decisions still needed.
```

## Issue Templates
For small tasks:

```md
## Goal
Do X.

## Acceptance criteria
- X works / is verified.
```

For larger or agent-ready tasks:

```md
## Goal
What should be true when this is done.

## Context
Why this exists, business reason, historical notes, and links.

## Scope
What is included.

## Out of scope
What should not be solved now.

## Inputs
Repos, tables, files, reports, APIs, source systems.

## Acceptance criteria
How to know it is done.

## Agent notes
Relevant repos/files, validation commands, risks, expected handoff.

## Next step
First concrete action.
```

For loose user requirements, draft the issue first and wait for approval when the task is broad, ambiguous, or creates a new project:

```md
Navrzeny Linear issue:

Title:

Project:

Description:

Acceptance criteria:

Open questions:
```

For small clear tasks, creating directly is fine.

## Comments And Updates
Add a Linear comment or project update when the thread produces meaningful operational state.

Use this compact update template:

```md
- Done:
- Found:
- Blocked / risks:
- Next:
```

For small updates, one sentence is enough.

Good triggers:
- Implementation step finished.
- PR/branch/report/model/config was created.
- Validation passed or failed.
- Blocker discovered.
- Scope changed.
- Work remains unfinished and another agent/thread needs the latest state.

Do not paste long logs. Link PRs, docs, paths, or task notes when available.

## Labels
Prefer a small stable label set.

Recommended labels:
- `Agent Ready`: enough context exists for an agent to start.
- `Needs Scope`: user/business clarification is needed.
- `Investigation`: discovery/debugging/analysis task.
- `Data Modeling`: dbt/Snowflake modeling work.
- `Ingestion`: extraction, landing, external tables, source setup.
- `Reporting`: Power BI, report UI, dashboard, analytics deliverable.
- Existing labels: `Bug`, `Feature`, `Improvement`, `External Dependency`.

Create missing labels only when they will be reused. Do not create one-off labels.

## Statuses
Use the Data Engineering statuses consistently:
- `Backlog`: captured, not ready or not planned.
- `Todo`: ready to work.
- `In Progress`: actively being worked.
- `In Review`: waiting for validation/review.
- `Done`: completed.
- `Canceled`: no longer relevant.

## Milestones And Project Updates
Use milestones only for larger projects where phases help. Suggested milestone names:
- `Discovery / Scope`
- `Data ingestion`
- `Modeling`
- `Report / UI`
- `Validation / Rollout`

Use project updates sparingly: when the project status materially changes, or roughly weekly for an active long-running project. Prefer concise updates over daily noise.

## Asana Migration
When converting Asana context:
- Link the original Asana task in Linear.
- Preserve useful historical notes, but summarize instead of copying everything verbatim.
- If an Asana parent has many subtasks, create one Linear parent-style issue first unless the user asks for child issues.
- Put possible future child issues in the description as a list, then split only when work actually starts.
- Put legacy Asana links at project level when the project may need historical lookup later.

## Do Not Over-PM
- Do not create a project for every small task.
- Do not create child issues just because a future breakdown is possible.
- Do not write long descriptions for tasks that only need "do X".
- Do not use Linear as durable technical documentation. Use repo docs/task notes for detailed implementation history and link them from Linear.
- Linear should hold: what, why, state, links, next step.
