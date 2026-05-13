---
name: repo-pr-handoff
description: Prepare a clean branch, commit, validation summary, pull request body, and Asana handoff for non-trivial Adrez repo changes.
scope: business
status: active
owner: martin
last_reviewed: 2026-05-12
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
- If multiple independent tasks are active in the same repo, use a dedicated
  git worktree per task branch instead of switching branches in one checkout.
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
pwd
git rev-parse --show-toplevel
git branch --show-current
git status -sb
git diff --stat
```
2. Choose branch and worktree:
   - if current branch is `main`, create a short dedicated task branch before
     editing,
   - if already on a task branch that matches the work, continue there,
   - if current branch is unrelated or ambiguous, ask before reusing it.
   - if another independent task is active in the same repo, create or use a
     task-specific worktree under
     `/Users/martin/Documents/adrez/_worktrees/<repo>/<task-slug>`,
   - if the worktree has dirty files whose owner is unclear, stop before branch
     switching, staging, committing, pulling, or pushing.
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
7. Check PR and CI:
   - resolve the PR and current head SHA,
   - inspect checks/status for that exact head SHA,
   - use CI logs as source of truth for failures,
   - keep PR as draft unless the user asks for ready-for-review.
8. Merge only when explicitly requested:
   - verify required checks, unresolved review threads, mergeability, branch
     scope, base freshness, and current PR head SHA,
   - default to squash merge unless repo-local policy says otherwise,
   - delete short-lived remote branch and prune task worktree when safe.
9. Update Asana when a task is known:
   - changed paths,
   - validation result,
   - PR link, commit hash, merge result when applicable,
   - open follow-ups.

## Branch / Worktree Safety
- Branches are delivery units; worktrees are concurrency units.
- Single task in a clean repo checkout can use a dedicated branch in the normal
  repo path.
- Parallel same-repo work must use one git worktree per task branch.
- Before editing, committing, pushing, opening a PR, or merging, confirm:
  - expected repo equals actual repo,
  - expected branch equals actual branch,
  - dirty files are either absent or belong to the current task.
- Unknown dirty files block branch switching, staging, committing, pulling, and
  pushing until ownership is clarified.
- Do not use `git stash`, `git reset`, `git checkout --`, `git clean`, or file
  moving to juggle unrelated work unless the user explicitly approves the exact
  action.

## User Intent Parsing
- "push", "push it", "commit and push", "clean and pushed", or "ship this":
  commit current-task changes, push the feature branch, and open a draft PR.
- "no PR" or "jen pushni branch": push branch only and do not open a PR.
- "ready for review": mark the draft PR ready only after validation and PR body
  checks are current.
- "merge", "sluč", or "dej to do main": merge only after PR/CI/review gates
  pass.
- "directly to main" or "push to main": allowed only when explicitly stated;
  still inspect status and confirm scope first.

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
- Branch/worktree identity was verified before edits, commit, push, PR, and merge.
- Commit/PR summary matches the actual diff.
- PR CI/check state was reviewed for the current head SHA after push.
- Asana or task note is updated when relevant.
