---
name: implementation-review
description: Review implementation diffs, milestones, branches, or PR-ready work before shipping. Use when the user says "udelej review", "reviewni implementaci", "zkontroluj implementaci", "zkontroluj diff", "reviewni milestone", "spawni subagenty na review", "bud dukladny", "dej si na cas", "najdi bugy", "najdi regrese", or asks for a deep implementation check before more coding, commit, push, PR, or merge.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-16
compatibility: Requires a git repository or a clearly supplied implementation artifact to review.
---

# implementation-review

Use this skill to act as a review gate for implemented work. Default to review
first and do not edit files unless the user explicitly asks to fix findings.

## Boundary
- Use `repo-pr-handoff` for commit, push, PR, CI, ready-for-review, or merge.
- Use this skill before delivery when the user wants defects, regressions,
  missing validation, or scope leaks found.
- Do not use this for broad brainstorming, product strategy, or plan grilling;
  use `grill-me` for plan/design understanding.

## Workflow
1. Establish review scope:
   - current git diff,
   - named files,
   - milestone behavior,
   - branch,
   - PR,
   - or explicit artifact from the user.
2. Inspect repo context:
```bash
git rev-parse --show-toplevel
git branch --show-current
git status -sb
git diff --stat
```
3. Read the closest `AGENTS.md` and relevant nearby code/tests/docs.
4. Review with a bug-finding stance:
   - correctness and edge cases,
   - regressions against existing behavior,
   - missing or weak validation,
   - scope creep or unrelated changes,
   - data/infra/security risk where relevant,
   - stale docs or skill/runtime drift when the change touches AI setup.
5. Use focused reviewer subagents when the change is non-trivial and subagents
   are available. Keep prompts narrow and evidence-based; do not leak expected
   findings. Useful roles:
   - correctness/regression reviewer,
   - tests/validation reviewer,
   - scope/safety reviewer.
6. Run the narrowest meaningful checks when they are safe and local. If a check
   is skipped, say why.
7. Report findings first. Do not bury material issues in a summary.

## Output Shape
Use this structure:
- **Findings**: ordered by severity with file/line, concrete risk, and suggested fix.
- **Validation**: checks run, checks skipped, and why.
- **Verdict**: `fix before ship`, `ship with caveats`, or `ship`.
- **Notes**: only short context that helps the next action.

If there are no findings, say that clearly and call out remaining test gaps or
residual risk.

## Severity Guide
- **P0**: data loss, credential/security exposure, production outage, destructive action.
- **P1**: likely user-facing bug, broken workflow, bad data, failing deploy/CI.
- **P2**: edge-case bug, missing important validation, maintainability risk.
- **P3**: minor cleanup, wording, low-risk style issue.

## Fix Mode
If the user asks to fix findings:
- keep the review findings visible,
- implement only the current-task fixes,
- do not stage unrelated dirty files,
- rerun relevant validation,
- then hand off to `repo-pr-handoff` only if commit/push/PR work is requested.
