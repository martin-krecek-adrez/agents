# Delivery Details

Load this reference only when creating/checking a PR, handling GitHub connector
fallback, or writing the final task handoff.

## GitHub Tool Fallback
- Prefer the GitHub connector for PR creation and metadata when it can access
  the repo.
- For private Adrez repos, a connector `404` does not prove the repo is missing.
  Treat it as possible connector installation or scope limitation first.
- If the connector returns `404` for an expected private Adrez repo:
  - verify the local git remote URL,
  - verify repo identity from the local checkout,
  - try `gh repo view <owner>/<repo>`.
- If sandboxed `gh` reports auth, keyring, DNS, or network-looking errors,
  retry the same narrow `gh` command with `require_escalated` before concluding
  auth is broken.
- If escalated `gh auth status` is valid, continue PR creation or CI inspection
  with escalated `gh`.
- Record in the handoff when connector fallback was used.

## PR Body Template
```md
## Summary
-

## Validation
-

## Risk / Rollback
-

## Links
- Linear:
- Asana:
- Task note:
```

## PR Check Notes
- Resolve the PR number and current head SHA after every push.
- Inspect checks/status for that exact SHA, not a stale PR state.
- Use CI logs as source of truth for failures.
- Keep PR as draft unless the user asks for ready-for-review.

## Task Handoff
- Prefer Linear for new Adrez work.
- Use Asana only for explicit legacy Asana tasks or historical context.
- Include changed paths, validation result, PR link, commit hash, merge result
  when applicable, and open follow-ups.
