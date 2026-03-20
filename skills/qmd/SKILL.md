---
name: qmd
description: Local semantic and hybrid search over docs and notes using tobi/qmd. Use for cross-repo retrieval before analysis or answer generation.
compatibility: Requires qmd CLI installed (bun install -g github:tobi/qmd) and sqlite available.
---

# qmd

Use [tobi/qmd](https://github.com/tobi/qmd) as the default retrieval layer for Adrez docs and notes.

## When to Use

- User asks broad questions that need prior context across repos.
- You need to find existing decisions, definitions, runbooks, or notes fast.
- You need ranked semantic matches, not only exact keyword grep.

Use `rg` for exact string or path matching. Use `qmd` for semantic/hybrid retrieval.

## Workspace Rules

- Workspace root: `/Users/martin/Documents/adrez`
- Never index `/Users/martin/Documents/adrez/old` unless explicitly asked.
- Exclude legacy agent repos from default retrieval:
  - `/Users/martin/Documents/adrez/adrez-data-assistant`
  - `/Users/martin/Documents/adrez/adrez-metadata-sql-agent`
- Prefer indexing:
  - `/Users/martin/Documents/adrez/docs`
  - repo-local `docs/`
  - repo-local `docs/tasks/` when useful for active work

## Standard Flow

1. Query:

```bash
qmd --index adrez query "what is revenue for finance team" --json -n 8
```

2. Open top hits:

```bash
qmd --index adrez get "<docid>" --full
```

3. Build answer from the retrieved documents and cite source paths.

## Collection Setup

```bash
qmd --index adrez collection add /Users/martin/Documents/adrez/docs --name docs --mask "**/*.md"
qmd --index adrez collection add /Users/martin/Documents/adrez/dbt-cloud/docs --name dbt_docs --mask "**/*.md"
qmd --index adrez collection add /Users/martin/Documents/adrez/dbt-cloud/docs/tasks --name dbt_tasks --mask "**/*.md"
qmd --index adrez collection add /Users/martin/Documents/adrez/data-factory/docs --name df_docs --mask "**/*.md"
qmd --index adrez collection add /Users/martin/Documents/adrez/data-platform/docs --name dp_docs --mask "**/*.md"
qmd --index adrez collection add /Users/martin/Documents/adrez/extractor-spreadsheets/docs --name es_docs --mask "**/*.md"
qmd --index adrez collection add /Users/martin/Documents/adrez/metadata-builder/docs --name mb_docs --mask "**/*.md"
```

Optional context labels:

```bash
qmd --index adrez context add qmd://docs "Durable cross-repo operational and business documentation."
qmd --index adrez context add qmd://dbt_tasks "Repo-local dbt investigations and implementation notes."
qmd --index adrez context add qmd://df_docs "Ingestion and orchestration documentation."
```

## Maintenance

```bash
qmd --index adrez update
qmd --index adrez embed
```

- Run `update` after content changes.
- Run `embed` after major changes to improve semantic retrieval quality.

## Notes

- Keep durable operating knowledge in `/Users/martin/Documents/adrez/docs`.
- Keep model or implementation-specific notes in repo-local `docs/tasks/` unless promoted.
- Keep Asana out of QMD runtime retrieval. Asana is for process tracking, not the primary knowledge store.

See [references/setup.md](references/setup.md) for install and quick diagnostics.
