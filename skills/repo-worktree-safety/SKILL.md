---
name: repo-worktree-safety
description: Isolate parallel same-repo work with git worktrees and recover safely from branch, scope, or dirty-worktree confusion. Use when the user says "mam bordel v branchich", "zkontroluj worktree", "jsem ve spatne branchi", "zkontroluj scope", "nez commitnes zkontroluj scope", "dirty worktree", or asks to create/use a task worktree.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-16
compatibility: Requires a git repository in /Users/martin/Documents/adrez.
---

# repo-worktree-safety

Use this skill when multiple independent tasks may be active in the same repo,
when a branch does not clearly match the task, or when dirty files may belong to
another user, agent, or task.

## Core Rule
One task = one branch = one git worktree = one agent.

Branches are delivery units. Worktrees are concurrency units.

## Default Layout
- Main checkout: `/Users/martin/Documents/adrez/<repo>`
- Task worktree: `/Users/martin/Documents/adrez/_worktrees/<repo>/<task-slug>`

Keep the main checkout clean when parallel task work exists.

## Required Preflight
Before editing, committing, pushing, opening a PR, or merging:
```bash
/Users/martin/Documents/adrez/agents/scripts/git_task_preflight.sh \
  /Users/martin/Documents/adrez/<repo-or-worktree> \
  <expected-branch>
```

If the expected branch is not known yet, run:
```bash
/Users/martin/Documents/adrez/agents/scripts/git_task_preflight.sh \
  /Users/martin/Documents/adrez/<repo-or-worktree>
```

Stop if the actual repo, branch, or dirty file ownership is unclear.

## Create A Task Worktree
```bash
/Users/martin/Documents/adrez/agents/scripts/create_task_worktree.sh \
  /Users/martin/Documents/adrez/<repo> \
  <task-slug> \
  <task-branch>
```

Then work only inside the printed worktree path.

## Dirty Worktree Rules
- Current-task dirty files may be continued.
- Unrelated tracked or untracked files must not be staged.
- Unknown dirty files block branch switching, pulling, committing, pushing, PRs,
  and merges until ownership is clarified.
- Do not use `git stash`, `git reset`, `git checkout --`, `git clean`, or file
  moving to juggle unrelated work unless the user explicitly approves the exact
  action.

## Recovery From Git Confusion
If branch/worktree state looks inconsistent:
1. Stop editing immediately.
2. Do not run destructive cleanup commands.
3. Capture state:
```bash
pwd
git rev-parse --show-toplevel
git branch --show-current
git status -sb
git worktree list
git diff --stat
git diff --name-only
```
4. Identify which dirty files belong to the current task, another task, the user,
   generated output, or unknown ownership.
5. Preserve unknown work only after explicit user approval.
6. Resume only after the correct worktree and branch are confirmed.

## Done Checklist
- Correct repo path and branch were verified.
- Parallel same-repo work used a task-specific worktree.
- Dirty files were classified before any branch switch, commit, push, or PR.
- No implicit stash/reset/checkout/clean was used.
- Handoff includes the worktree path when a task worktree was used.
