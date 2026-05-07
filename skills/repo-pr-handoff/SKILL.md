---
name: repo-pr-handoff
description: Prepare a clean branch, commit, validation summary, pull request body, and Asana handoff for non-trivial Adrez repo changes.
scope: business
status: active
owner: martin
last_reviewed: 2026-05-07
compatibility: Requires a git repository in /Users/martin/Documents/adrez and GitHub access when opening PRs.
---

# repo-pr-handoff

Use this skill when preparing non-trivial Adrez work for branch/PR handoff,
especially model logic, ingestion, Terraform/platform, CI/deploy, or shared AI
context changes.

## Trigger Guidance
- Use for non-trivial changes before commit/push/PR.
- Do not force PR ceremony for tiny typo/docs-only edits unless the user asks.
- If the user explicitly says to commit directly, keep the same hygiene but skip
  PR creation.

## Workflow
1. Inspect worktree:
```bash
git status -sb
git diff --stat
```
2. Split scope:
   - identify files that belong to the current task,
   - identify unrelated dirty files,
   - never stage unrelated changes.
3. Validate:
   - use repo-local `AGENTS.md` validation commands,
   - run the narrowest meaningful checks,
   - document any blocker or skipped validation.
4. Commit:
   - stage only the approved file list,
   - use a concise imperative message,
   - include task note/docs updates when they are part of the change.
5. PR handoff when requested:
   - push branch,
   - open draft PR unless the user requests ready-for-review,
   - include summary, validation, risks, rollback notes, Asana/task-note links.
6. Update Asana when a task is known:
   - changed paths,
   - validation result,
   - PR link or commit hash,
   - open follow-ups.

## PR Body Template
```md
## Summary
- 

## Validation
- 

## Risk / Rollback
- 

## Links
- Asana:
- Task note:
```

## Done Checklist
- Current-task files only were staged.
- Validation ran or the reason it did not run is explicit.
- Commit/PR summary matches the actual diff.
- Asana or task note is updated when relevant.
