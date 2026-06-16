---
name: write-docs
description: Write AI-scannable technical documentation for Adrez repos and durable docs. Use when the user says "napis dokumentaci", "uprav docs", "zdokumentuj workflow", "vytvor README", "pridej how-to", or "sepis troubleshooting". Use ai-context-maintenance instead for AGENTS.md, shared skill governance, task-memory routing, and Codex setup audits.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-16
---

# Write Documentation

Documentation that is scannable, consistent, and actionable for AI agents.

## Override Rule

- If the current repo or subfolder has a local `AGENTS.md` for documentation, follow that file first.
- Use this skill as the generic fallback only when no repo-local docs rules are more specific.
- Use `ai-context-maintenance` instead when the work is about AGENTS.md hierarchy, skills, task-memory routing, feedback promotion, or local Codex setup.

## Structure

- Max 150 lines per file, one concept per file
- Start with `description:` in YAML frontmatter
- Add TL;DR section at top with most-needed info

## Content

- No duplicates (define once, link elsewhere)
- Use tables for structured data (parameters, config)
- Concrete examples for everything (copy-pasteable)
- Link to real code as templates

## Naming

| Pattern | Use For | Example |
|---------|---------|---------|
| `README.md` | Directory overview | `docs/README.md` |
| `{noun}.md` | Reference | `entities.md` |
| `{verb}-{noun}.md` | How-to | `add-entity.md` |

## Tips

- Use consistent terms (one term per concept)
- Group by task ("How to add X") not system ("X overview")
- Include troubleshooting for common errors
