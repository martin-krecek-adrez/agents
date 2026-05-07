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
- For implementation tasks, create or switch to a dedicated task branch before
  editing unless the user explicitly asks to use the current branch.
- A request like "make changes in <repo> and push it" is not permission to work
  on or push `main`; use a dedicated task branch and draft PR.
- If the user asks for non-trivial work to be "pushed", "clean and pushed", or
  "commit and push" without naming `main`, interpret that as feature branch plus
  draft PR handoff.
- Direct commits or pushes to `main` require explicit wording such as "push
  directly to main" or "commit directly to main".
- Pushing a branch without opening a PR requires explicit wording such as
  "no PR" or "jen pushni branch".
- Treat shared AI operating-system changes as non-trivial by default, including
  `AGENTS.md`, skills, routing, task-memory rules, agent docs, and automation
  prompts.

## Workflow
1. Inspect worktree:
```bash
git status -sb
git diff --stat
```
2. Choose branch:
   - if current branch is `main`, create a short dedicated task branch before
     editing,
   - if already on a task branch that matches the work, continue there,
   - if current branch is unrelated or ambiguous, ask before reusing it.
3. Split scope:
   - identify files that belong to the current task,
   - identify unrelated dirty files,
   - never stage unrelated changes.
4. Validate:
   - use repo-local `AGENTS.md` validation commands,
   - run the narrowest meaningful checks,
   - document any blocker or skipped validation.
5. Commit:
   - stage only the approved file list,
   - use a concise imperative message,
   - include task note/docs updates when they are part of the change.
6. PR handoff for non-trivial work, or when requested:
   - push branch,
   - open draft PR unless the user requests ready-for-review,
   - include summary, validation, risks, rollback notes, Asana/task-note links.
7. Update Asana when a task is known:
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
