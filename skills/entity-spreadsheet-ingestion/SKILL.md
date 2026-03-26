---
name: entity-spreadsheet-ingestion
description: End-to-end onboarding of a OneDrive/SharePoint spreadsheet or mapping source across extractor-spreadsheets and data-factory, including ADLS landing and Snowflake external-table setup.
scope: business
status: active
owner: martin
last_reviewed: 2026-03-26
compatibility: Requires /Users/martin/Documents/adrez/extractor-spreadsheets and /Users/martin/Documents/adrez/data-factory with local env setup per each repo README.
---

# entity-spreadsheet-ingestion

Use this skill when the user asks to add or update a spreadsheet, statement file, or mapping sheet from OneDrive/SharePoint and does not explicitly limit scope to only extractor landing or only data-factory.

Use `entity-extractor-spreadsheets` for extractor-only work.
Use `entity-data-factory` when the files already land in ADLS and only Snowflake exposure is needed.

## Inputs to confirm
- Entity name.
- Source type: `input sheets` or `mapping`.
- SharePoint item path.
- Target subdir.
- Optional sheet name for Excel.
- Whether Snowflake exposure is needed.

Default assumption: if the user says "add a new spreadsheet" and does not narrow the scope, Snowflake exposure is in scope.

## Workflow
1. Open `/Users/martin/Documents/adrez/extractor-spreadsheets/AGENTS.md` and `/Users/martin/Documents/adrez/data-factory/AGENTS.md`.
2. Update `/Users/martin/Documents/adrez/extractor-spreadsheets/ingest_config.yml` using an existing same-type entity as template.
3. Validate landing locally:
```bash
cd /Users/martin/Documents/adrez/extractor-spreadsheets
./run_ingest.sh --only <entity_name>
```
4. Update the downstream external-table config in `/Users/martin/Documents/adrez/data-factory/configs/input_sheets.yaml` or `/Users/martin/Documents/adrez/data-factory/configs/mapping.yaml`, matching the same `target_subdir`.
5. Validate Snowflake exposure locally:
```bash
cd /Users/martin/Documents/adrez/data-factory
python3 main.py --config configs/<file>.yaml
```
6. If the config is incremental and introduces new formats/stages, run once with full mode:
```bash
python3 main.py --config configs/<file>.yaml --mode full
```
7. Assess whether Azure Function `CONFIG_PATHS` needs an update.
8. If the user says the files already land in ADLS, skip extractor and use `entity-data-factory` only.
9. If the user says landing only, stop after extractor validation.

## Done checklist
- Extractor config updated and validated.
- Downstream data-factory config updated and validated when in scope.
- Matching folder/subdir names stay aligned across both repos.
- `CONFIG_PATHS` impact assessed.
