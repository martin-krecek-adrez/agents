---
name: entity-data-factory
description: Add or update data-factory external-table configs for files that already land in ADLS, or complete the Snowflake exposure step for a spreadsheet flow after ADLS landing exists. Use when the user says the file/source already lands, asks for external tables, config sync, CONFIG_PATHS, "dostan ADLS folder do Snowflake", or Snowflake exposure only.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-16
compatibility: Requires /Users/martin/Documents/adrez/data-factory and local Snowflake credentials/key setup per README.
---

# entity-data-factory

Use this skill when the task is to add or modify entity configs in `data-factory` (`configs/*.yaml`) for files that already exist in ADLS, including the downstream Snowflake half of a spreadsheet ingestion flow.

Do not use this skill for the initial OneDrive/SharePoint landing step when the spreadsheet is not yet configured in `extractor-spreadsheets`.

## Inputs to confirm
- Config file path (`configs/<name>.yaml`).
- Entity identifier and source folder/path.
- Target external table name for targeted validation when known.
- Whether upstream landing already exists in ADLS.
- Whether this is incremental-only or needs first full run.
- Whether function app `CONFIG_PATHS` must be updated.

## Workflow
1. Open `/Users/martin/Documents/adrez/data-factory/AGENTS.md` and `README.md`.
2. If the source is a new OneDrive/SharePoint spreadsheet and landing is not already configured, use `/Users/martin/Documents/adrez/agents/skills/entity-spreadsheet-ingestion/SKILL.md` unless the user explicitly asked for landing-only work.
3. Edit `configs/*.yaml` using same-type entity template.
4. Keep naming/path conventions and schema behavior aligned.
5. Spreadsheet downstream defaults usually live in `configs/input_sheets.yaml` or `configs/mapping.yaml`.
6. Prefer targeted validation for changed/new tables:
```bash
cd /Users/martin/Documents/adrez/data-factory
./scripts/data-factory-local --config configs/<file>.yaml --only-table <table_name>
```
7. Run the whole config only when a broad config-level validation is intended.
8. Respect the config's existing mode. `configs/input_sheets.yaml` and
   `configs/mapping.yaml` usually use `mode: full`. If an incremental config
   introduces new formats/stages, run once with full mode:
```bash
./scripts/data-factory-local --config configs/<file>.yaml --mode full
```
9. Check whether production has an explicit `CONFIG_PATHS` override. Normally no change is needed for top-level `configs/*.yaml` because data-factory autodiscovers them.
10. If non-trivial, create/update `docs/tasks/YYYY-MM-DD-<task>.md`.

## Done checklist
- Config updated and validated locally, preferably with `--only-table` for new/changed tables.
- Full-mode bootstrap considered where needed.
- Upstream ADLS landing was either already present or handled explicitly.
- `CONFIG_PATHS` override impact assessed.
