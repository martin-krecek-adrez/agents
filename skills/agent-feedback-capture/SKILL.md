---
name: agent-feedback-capture
description: Capture reusable Adrez harness feedback as structured inbox items for later triage and promotion. Use when the user says "zapis feedback", "zachyt feedback", "at se to priste nestane", "priste to delej jinak", "dej to do harnessu", "tohle je reusable lesson", or when agent/tool/connector behavior reveals a reusable workflow lesson.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-15
compatibility: Requires /Users/martin/Documents/adrez/agents/feedback.
---

# agent-feedback-capture

Use this skill when a Codex run reveals a reusable lesson about the Adrez
agent harness, tooling, routing, prompts, git workflow, or connector behavior.

## Trigger Guidance
Capture feedback when:
- a tool or connector fails but a workaround succeeds,
- sandbox behavior differs from the real environment,
- connector and CLI results conflict,
- an agent misroutes work, uses the wrong repo/branch, or misunderstands user
  intent,
- a workflow needs a new fallback, guardrail, script, or setup check,
- a skill, `AGENTS.md`, or durable context surface is stale,
- the user says "zapis feedback", "zachyt feedback", "priste to delej jinak",
  "pridej to do harnessu", "at se to priste nestane", or equivalent.

Do not use this skill for normal product-code bugs unless the reusable lesson is
about agent/harness behavior.

## Default Output
Create one Markdown item in:

```text
/Users/martin/Documents/adrez/agents/feedback/inbox/YYYY-MM-DD-short-slug.md
```

Use:

```text
/Users/martin/Documents/adrez/agents/feedback/TEMPLATE.md
```

## Required Fields
- `date`
- `area`
- `severity`
- `source`
- `status: inbox`
- `sensitive_data_checked`
- `promote_to`

## Sensitive Data Rules
- Do not include secrets, tokens, private keys, customer data, personal
  identifiers, raw SQL result samples, or full sensitive URLs.
- Summarize logs instead of pasting them when they may contain private data.
- If sensitivity was not checked, set `sensitive_data_checked: no`; such items
  cannot be promoted until reviewed.

## Local Note vs Linear
Create a local feedback item for reusable lessons, unclear future triage, or
small harness improvements.

Create a Linear issue as well when:
- the change needs design discussion,
- it affects multiple repos or production workflows,
- it requires ownership or prioritization,
- it is security, privacy, reliability, or architecture relevant,
- it cannot be safely implemented in the current thread.

## Promotion Policy
- First occurrence: capture feedback.
- Second similar occurrence: propose durable rule or skill/script/check change.
- Clear P0/P1 safety issue: propose immediate harness update or Linear issue.
- Prefer promotion targets in this order:
  1. helper script or deterministic check,
  2. narrow skill update,
  3. repo-local `AGENTS.md`,
  4. shared `agents/AGENTS.md`,
  5. durable docs or Linear issue.

## Done Checklist
- Feedback item exists in `feedback/inbox/`.
- The item is sanitized or marks `sensitive_data_checked: no`.
- Suggested promotion target is explicit.
- Larger design work has a Linear issue when needed.
