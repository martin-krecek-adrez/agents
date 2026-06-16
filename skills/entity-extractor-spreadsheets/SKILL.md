---
name: entity-extractor-spreadsheets
description: Add or update extractor-spreadsheets config for a SharePoint/OneDrive Excel file, input sheet, mapping file, or manual spreadsheet source and validate ADLS landing only. Use when the user explicitly limits scope to landing/file pickup, ingest_config.yml, ADLS landing, or spreadsheet extractor validation.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-16
compatibility: Requires /Users/martin/Documents/adrez/extractor-spreadsheets and local env setup per README.
---

# entity-extractor-spreadsheets

Use this skill when the task is to add or modify an `input sheets` or `mapping` entity in `extractor-spreadsheets` and the user explicitly limits scope to extractor landing, `ingest_config.yml`, ADLS landing, or validation of the spreadsheet extractor.

Do not use this skill for Mews, Mara, or other sources that already land in ADLS without the spreadsheet extractor.
For unscoped requests such as "pridej input sheet", "napoj tenhle Excel", or "dostan tenhle SharePoint/OneDrive soubor do Snowflake", use `entity-spreadsheet-ingestion` instead.

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
4. Assess config details:
   - folder globs are direct-child only,
   - correction overlays may share the same `target_subdir`,
   - folder queues may require `processed_path` and `processed_date_timezone`,
   - `processed_path` needs write permission,
   - entities may need `parser`, `source_encoding`, or `allow_empty`.
5. Run targeted ingest validation:
```bash
cd /Users/martin/Documents/adrez/extractor-spreadsheets
./run_ingest.sh --only <entity_name>
```
6. This is not a dry run: it uploads to ADLS and may move source files when `processed_path` is configured. For folder queues or processed-path entries, confirm that mutation is intended before running.
7. If Snowflake exposure becomes clearly in scope, switch to `entity-spreadsheet-ingestion` so the end-to-end flow is tracked explicitly.
8. If non-trivial, create/update `docs/tasks/YYYY-MM-DD-<task>.md`.

## Done checklist
- Config updated and syntax valid.
- Targeted local ingest command ran.
- Any downstream dependency was either updated or explicitly called out.
