# Agent Feedback

Feedback captures repeatable harness, tooling, routing, prompt, and workflow
lessons before they become durable instructions.

Raw feedback is evidence. Promoted feedback becomes harness behavior.

## Folders
- `inbox/`: raw feedback items waiting for triage.
- `promoted/`: items converted into AGENTS.md, skills, scripts, checks, docs, or Asana backlog.
- `rejected/`: one-off or obsolete items kept for traceability.

## Capture Rule
Create one Markdown file per item:

```text
feedback/inbox/YYYY-MM-DD-short-slug.md
```

Use `feedback/TEMPLATE.md`.

## Promotion Rule
Do not update shared harness surfaces automatically from raw feedback. Promote
only after triage, repeated evidence, explicit user instruction, or clear
P0/P1 safety impact.

Prefer promotion targets in this order:
1. helper script or deterministic check,
2. narrow skill update,
3. repo-local `AGENTS.md`,
4. shared `agents/AGENTS.md`,
5. durable docs or Asana backlog for larger design work.
