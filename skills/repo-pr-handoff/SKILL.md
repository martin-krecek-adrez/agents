---
name: repo-pr-handoff
description: Prepare non-trivial Adrez repo work for delivery: clean branch scope, final validation, commit, push, draft PR, PR/CI check, merge when explicitly requested, and Linear/Asana/task-note handoff. Use when the user says to commit, push, ship it, make/open a PR, test/check the PR, mark ready for review, merge, or send it to main. Use implementation-review for standalone implementation review before delivery.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-15
compatibility: Requires a git repository in /Users/martin/Documents/adrez and GitHub access when opening PRs.
---

# repo-pr-handoff

Use this skill when preparing non-trivial Adrez work for delivery: validation,
branch scope, commit, push, PR, CI/review follow-up, merge, and task handoff.
This is the delivery workflow. Use `repo-worktree-safety` for standalone
worktree/branch safety questions, `implementation-review` for standalone
review gates, and `write-commit` for commit-message wording.

## Trigger Guidance
- Use for non-trivial changes before validation, commit, push, PR, PR check, or merge.
- Common user phrasing includes "commitni", "pushni", "ship it", "udelat PR",
  "otestuj PR", "ready for review", "mergni", and "posli to do mainu".
- For standalone "udelej review", "zkontroluj implementaci", "spawni subagenty
  na review", or "bud dukladny" requests, use `implementation-review` first.
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
- For long implementation work, validate after each meaningful milestone, not
  only at the end.

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
4. Validate by milestone:
   - use repo-local `AGENTS.md` validation commands,
   - run the narrowest meaningful checks,
   - for multi-step work, test each meaningful milestone before moving on,
   - document any blocker or skipped validation.
5. Review before PR when useful:
   - for standalone review, use `implementation-review`,
   - for delivery-only handoff, ensure review findings are resolved or explicitly
     carried as caveats before pushing,
   - fix material findings before pushing or explain why they are not handled.
6. Commit:
   - stage only the approved file list,
   - use a concise imperative message,
   - include task note/docs updates when they are part of the change.
7. PR handoff for non-trivial work, or when requested:
   - push branch,
   - open draft PR unless the user requests ready-for-review,
   - include summary, validation, risks, rollback notes, and task links.
8. Check PR and CI:
   - resolve the PR and current head SHA,
   - inspect checks/status for that exact head SHA,
   - use CI logs as source of truth for failures,
   - keep PR as draft unless the user asks for ready-for-review.
9. Merge only when explicitly requested:
   - verify required checks, unresolved review threads, mergeability, branch
     scope, base freshness, and current PR head SHA,
   - default to squash merge unless repo-local policy says otherwise,
   - delete short-lived remote branch and prune task worktree when safe.
10. Update Linear/Asana/task notes when a task is known:
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
- For GitHub connector fallback on expected private Adrez repos, try `gh repo view <owner>/<repo>` from the local checkout.
- If sandboxed `gh` reports auth, keyring, DNS, or network-looking errors, retry the same narrow `gh` command with `require_escalated` before concluding auth is broken.
- See `references/delivery-details.md` for GitHub fallback, PR body, and handoff
  details when needed.

## User Intent Parsing
- "push", "push it", "commit and push", "clean and pushed", or "ship this":
  commit current-task changes, push the feature branch, and open a draft PR.
- "test it", "otestuj to", or "otestuj milestone" in a delivery context: run
  the narrowest meaningful validation for the current state and report blockers
  before continuing. For standalone review, use `implementation-review`.
- "no PR" or "jen pushni branch": push branch only and do not open a PR.
- "ready for review": mark the draft PR ready only after validation and PR body
  checks are current.
- "merge", "sluč", or "dej to do main": merge only after PR/CI/review gates
  pass.
- "directly to main" or "push to main": allowed only when explicitly stated;
  still inspect status and confirm scope first.

## Done Checklist
- Current-task files only were staged.
- Milestone/final validation ran or the reason it did not run is explicit.
- Focused reviewer subagents were used for high-risk changes when practical, or skipped intentionally.
- Branch/worktree identity was verified before edits, commit, push, PR, and merge.
- Commit/PR summary matches the actual diff.
- PR CI/check state was reviewed for the current head SHA after push.
- Linear, Asana, or task note is updated when relevant.
