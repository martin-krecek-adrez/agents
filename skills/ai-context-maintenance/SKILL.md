---
name: ai-context-maintenance
description: Audit and maintain Adrez AI context surfaces, including AGENTS.md hierarchy, shared skills, repo task notes, durable docs routing, and stale or oversized agent instructions.
scope: business
status: active
owner: martin
last_reviewed: 2026-05-14
compatibility: Requires /Users/martin/Documents/adrez/agents and the Adrez workspace repositories.
---

# ai-context-maintenance

Use this skill when auditing or maintaining the Adrez AI operating system:
`AGENTS.md` files, shared skills, task notes, durable docs routing, and local
Codex setup.

## Default Behavior
- Report first. Do not rewrite many files automatically unless the user asks.
- Prefer small, reviewable changes.
- Treat `AGENTS.md` as routing and operational guardrails, not durable docs.
- Promote reusable workflows to skills only after repetition.
- Promote durable business or operating-state knowledge to
  `/Users/martin/Documents/adrez/docs`, not repo-local task notes.
- Treat `agents/feedback/inbox/` as raw evidence, not durable instructions.

## Workflow
1. Run the setup check:
```bash
/Users/martin/Documents/adrez/agents/scripts/check_ai_setup.sh
```
2. Run the task-note promotion candidate report:
```bash
/Users/martin/Documents/adrez/agents/scripts/report_task_note_promotion_candidates.sh
```
3. Inspect changed or stale context surfaces:
   - `/Users/martin/Documents/adrez/AGENTS.md`
   - `/Users/martin/Documents/adrez/agents/AGENTS.md`
   - repo-local `AGENTS.md` files in active repos
   - `/Users/martin/Documents/adrez/agents/skills/*/SKILL.md`
   - `/Users/martin/Documents/adrez/agents/feedback/inbox/*.md`
   - repo-local `docs/tasks/`
   - `/Users/martin/Documents/adrez/docs/data-platform`
4. Classify findings:
   - **Blocking**: broken setup, missing required files, malformed skill
     metadata, oversized critical `AGENTS.md`.
   - **Maintenance**: stale `last_reviewed`, duplicated routing, weak docs
     routing, long task notes that should be promoted.
   - **Follow-up**: useful improvements that are not needed immediately.
5. If edits are requested, keep scope narrow:
   - update one skill,
   - or one repo `AGENTS.md` hierarchy,
   - or one docs routing improvement,
   - or one automation/check improvement.
6. Process feedback inbox when requested:
   - group items by area and repeated failure mode,
   - decide disposition: promote, create Asana backlog, keep for more evidence,
     reject as one-off,
   - move processed items to `feedback/promoted/` or `feedback/rejected/` only
     after the decision is reflected in the summary,
   - add `check_ai_setup.sh` guards for promoted critical rules when practical.
7. Summarize exact paths changed and whether `check_ai_setup.sh` passes.

## AGENTS.md Heuristics
- Root workspace `AGENTS.md`: routing only.
- Shared `agents/AGENTS.md`: cross-repo operating rules and skill routing.
- Repo root `AGENTS.md`: repo map, validation commands, source-of-truth links.
- Nested `AGENTS.md`: only where local rules materially differ.
- Warning threshold: over 8 KB.
- Failure threshold: over 12 KB.

## Task Notes vs Durable Docs
- Keep task execution, validation SQL, and WIP investigation in repo
  `docs/tasks/`.
- Move current business rules, architecture, source-system behavior, and
  operating-state truth to `/Users/martin/Documents/adrez/docs`.
- Cross-link Asana, task note, and durable docs when promotion happens.
- Treat the promotion report as a candidate list, not proof that every match
  should become durable docs.

## Feedback Inbox
- Raw feedback belongs in `/Users/martin/Documents/adrez/agents/feedback/inbox/`.
- Use `agent-feedback-capture` to create new items.
- Promote only stable, repeated, high-impact, or explicitly requested lessons.
- Prefer scripts/checks over prose when the lesson can be validated
  deterministically.
- Keep incident examples in feedback history; put only the durable rule in
  `AGENTS.md` or skills.

## Done Checklist
- Setup check passes or failures are explained.
- Findings are grouped by severity.
- Suggested edits are small enough for a single review.
- Feedback inbox items were triaged when requested.
- No unrelated worktree changes are reverted.
