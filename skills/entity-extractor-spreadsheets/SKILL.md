---
name: entity-extractor-spreadsheets
description: Add or update a spreadsheet/mapping entity in extractor-spreadsheets and validate ingestion locally.
compatibility: Requires /Users/martin/Documents/adrez/extractor-spreadsheets and local env setup per README.
---

# entity-extractor-spreadsheets

Use this skill when the task is to add or modify an `input sheets` or `mapping` entity in `extractor-spreadsheets`.

## Inputs to confirm
- Entity name (`name` in config).
- Source type (`input sheets` or `mapping`).
- SharePoint item path.
- Target subdir.
- Optional sheet name (for Excel).

## Workflow
1. Open `/Users/martin/Documents/adrez/extractor-spreadsheets/AGENTS.md` and `README.md`.
2. Edit `ingest_config.yml` using an existing same-type entity as template.
3. Keep naming/path conventions consistent with nearby entities.
4. Run local validation:
```bash
cd /Users/martin/Documents/adrez/extractor-spreadsheets
./run_ingest.sh --only <entity_name>
```
5. Capture downstream impact note if config/path affects `data-factory` or dbt sources.
6. If non-trivial, create/update `docs/tasks/YYYY-MM-DD-<task>.md`.

## Done checklist
- Config updated and syntax valid.
- Targeted local ingest command ran.
- Any downstream dependency called out.

