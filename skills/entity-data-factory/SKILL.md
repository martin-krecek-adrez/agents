---
name: entity-data-factory
description: Add or update a data-factory external-table config for an already-landed ADLS source, or for the downstream Snowflake half of a spreadsheet ingestion flow.
scope: business
status: active
owner: martin
last_reviewed: 2026-03-26
compatibility: Requires /Users/martin/Documents/adrez/data-factory and local Snowflake credentials/key setup per README.
---

# entity-data-factory

Use this skill when the task is to add or modify entity configs in `data-factory` (`configs/*.yaml`) for files that already exist in ADLS, including the downstream Snowflake half of a spreadsheet ingestion flow.

Do not use this skill for the initial OneDrive/SharePoint landing step when the spreadsheet is not yet configured in `extractor-spreadsheets`.

## Inputs to confirm
- Config file path (`configs/<name>.yaml`).
- Entity identifier and source folder/path.
- Whether upstream landing already exists in ADLS.
- Whether this is incremental-only or needs first full run.
- Whether function app `CONFIG_PATHS` must be updated.

## Workflow
1. Open `/Users/martin/Documents/adrez/data-factory/AGENTS.md` and `README.md`.
2. If the source is a new OneDrive/SharePoint spreadsheet and landing is not already configured, first use `/Users/martin/Documents/adrez/agents/skills/entity-extractor-spreadsheets/SKILL.md`.
3. Edit `configs/*.yaml` using same-type entity template.
4. Keep naming/path conventions and schema behavior aligned.
5. Spreadsheet downstream defaults usually live in `configs/input_sheets.yaml` or `configs/mapping.yaml`.
6. Validate locally:
```bash
cd /Users/martin/Documents/adrez/data-factory
python3 main.py --config configs/<file>.yaml
```
7. If incremental config introduces new formats/stages, run once with full mode:
```bash
python3 main.py --config configs/<file>.yaml --mode full
```
8. Note whether Azure Function `CONFIG_PATHS` must include the config.
9. If non-trivial, create/update `docs/tasks/YYYY-MM-DD-<task>.md`.

## Done checklist
- Config updated and validated locally.
- Full-mode bootstrap considered where needed.
- Upstream ADLS landing was either already present or handled explicitly.
- `CONFIG_PATHS` impact assessed.
