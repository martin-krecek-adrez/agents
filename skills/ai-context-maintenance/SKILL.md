---
name: ai-context-maintenance
description: Audit and maintain the Adrez AI operating system. Use when the user asks to check skills, review what skills exist, clean up skill drift, audit AGENTS.md, verify source/runtime sync, inspect skills inventory, maintain task-memory/docs routing, or turn repeated AI workflow feedback into small proposed changes. Report first; do not edit skills or AGENTS.md unless explicitly approved. Use write-docs for ordinary documentation writing.
scope: business
status: active
owner: martin
last_reviewed: 2026-07-15
compatibility: Requires /Users/martin/Documents/adrez/agents and the Adrez workspace repositories.
---

# ai-context-maintenance

Use this skill when auditing or maintaining the Adrez AI operating system:
`AGENTS.md` files, shared skills, task notes, durable docs routing, and local
Codex setup.

## Boundary
- Use `write-docs` for ordinary durable or repo documentation writing.
- Use `agent-feedback-capture` to record raw feedback; use this skill to triage and promote it.
- Use this skill for skill inventory, source/runtime sync, `AGENTS.md` routing, and context-governance changes.

## Default Behavior
- Report first. Do not rewrite many files automatically unless the user asks.
- Prefer small, reviewable changes.
- Treat `AGENTS.md` as routing and operational guardrails, not durable docs.
- Treat `/Users/martin/Documents/adrez/agents/ops/skills-inventory.md` as the skill review registry.
- Promote reusable workflows to skills only after repetition.
- Promote durable business or operating-state knowledge to
  `/Users/martin/Documents/adrez/docs`, not repo-local task notes.
- Treat `agents/feedback/inbox/` as raw evidence, not durable instructions.
- When reviewing skills interactively, discuss one skill at a time unless the user asks for a batch.

## Skill Review Mode
Use this mode when the user wants to understand, audit, compare, clean up, or improve existing skills.

Report one skill at a time with this compact shape:
- **Skill**: name and source path.
- **What it does**: plain-language purpose.
- **When to use it**: concrete trigger situations.
- **When not to use it**: boundaries and overlaps.
- **Verdict**: keep, tighten, split, merge, archive, or source-fix.
- **Smallest recommended change**: the next reviewable edit, if any.

Rules:
- Do not edit the skill, inventory, automation, or AGENTS.md during review unless the user explicitly says to update it.
- Prefer tightening `description` before expanding the body; the description is the trigger surface.
- Keep `SKILL.md` lean. Move long reference material to `references/`, deterministic repeated logic to `scripts/`, and output templates/assets to `assets/`.
- Use the inventory to track scope, owner, status, source path, runtime sync, review date, and latest verdict.
- If the skill overlaps with another skill, recommend one owner and one boundary instead of duplicating instructions.
- Archive only when the skill is unused, obsolete, or fully replaced; otherwise prefer tightening.

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
   - `/Users/martin/Documents/adrez/agents/ops/skills-inventory.md`
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
5. For skill findings, classify each skill as:
   - **keep**: useful as-is.
   - **tighten**: useful, but trigger description, boundaries, or workflow should be clearer.
   - **split**: one skill covers multiple materially different workflows.
   - **merge**: duplicates another skill and should be folded into it.
   - **archive**: obsolete or no longer worth triggering.
   - **source-fix**: source/runtime/inventory wiring is wrong.
6. If edits are requested, keep scope narrow:
   - update one skill,
   - or one repo `AGENTS.md` hierarchy,
   - or one docs routing improvement,
   - or one automation/check improvement.
7. Process feedback inbox when requested:
   - group items by area and repeated failure mode,
   - decide disposition: promote, create Linear follow-up, keep for more evidence,
     reject as one-off,
   - move processed items to `feedback/promoted/` or `feedback/rejected/` only
     after the decision is reflected in the summary,
   - add `check_ai_setup.sh` guards for promoted critical rules when practical.
8. Summarize exact paths changed and whether `check_ai_setup.sh` passes.

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
- Cross-link Linear, task note, and durable docs when promotion happens.
  Preserve legacy Asana links only as historical provenance.
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
