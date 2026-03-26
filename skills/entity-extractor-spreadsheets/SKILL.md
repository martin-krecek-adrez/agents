---
name: entity-extractor-spreadsheets
description: Add or update a OneDrive/SharePoint spreadsheet or mapping source in extractor-spreadsheets and validate ADLS landing. Use for the first half of spreadsheet ingestion.
scope: business
status: active
owner: martin
last_reviewed: 2026-03-26
compatibility: Requires /Users/martin/Documents/adrez/extractor-spreadsheets and local env setup per README.
---

# entity-extractor-spreadsheets

Use this skill when the task is to add or modify an `input sheets` or `mapping` entity in `extractor-spreadsheets`, or when the user says a new spreadsheet comes from OneDrive/SharePoint.

Do not use this skill for Mews, Mara, or other sources that already land in ADLS without the spreadsheet extractor.

## Inputs to confirm
- Entity name (`name` in config).
- Source type (`input sheets` or `mapping`).
- SharePoint item path.
- Target subdir.
- Optional sheet name (for Excel).
- Whether downstream Snowflake external-table setup is also in scope.

## Workflow
1. Open `/Users/martin/Documents/adrez/extractor-spreadsheets/AGENTS.md` and `README.md`.
2. Edit `ingest_config.yml` using an existing same-type entity as template.
3. Keep naming/path conventions consistent with nearby entities.
4. Run local validation:
```bash
cd /Users/martin/Documents/adrez/extractor-spreadsheets
./run_ingest.sh --only <entity_name>
```
5. If the task is end-to-end spreadsheet onboarding, or Snowflake exposure is clearly implied, continue with `/Users/martin/Documents/adrez/agents/skills/entity-data-factory/SKILL.md` using the same `target_subdir`.
6. For downstream Snowflake exposure, the usual targets are `data-factory/configs/input_sheets.yaml` or `data-factory/configs/mapping.yaml`.
7. If non-trivial, create/update `docs/tasks/YYYY-MM-DD-<task>.md`.

## Done checklist
- Config updated and syntax valid.
- Targeted local ingest command ran.
- Any downstream dependency was either updated or explicitly called out.
