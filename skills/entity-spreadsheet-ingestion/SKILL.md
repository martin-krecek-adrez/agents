---
name: entity-spreadsheet-ingestion
description: Orchestrate end-to-end setup for a SharePoint/OneDrive Excel file, input sheet, mapping file, or manual statement: extractor-spreadsheets landing to ADLS plus data-factory Snowflake external-table exposure. Use when the user says "pridej input sheet", "napoj tenhle Excel", or "dostan tenhle SharePoint/OneDrive soubor do Snowflake" and does not explicitly limit the task to landing only or Snowflake only.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-15
compatibility: Requires /Users/martin/Documents/adrez/extractor-spreadsheets and /Users/martin/Documents/adrez/data-factory with local env setup per each repo README.
---

# entity-spreadsheet-ingestion

Use this skill when the user asks to add or update a spreadsheet, statement file, input sheet, or mapping sheet from OneDrive/SharePoint and does not explicitly limit scope to only extractor landing or only data-factory.

Use `entity-extractor-spreadsheets` for extractor-only work.
Use `entity-data-factory` when the files already land in ADLS and only Snowflake exposure is needed.

## Inputs to confirm
- Entity name.
- Source type: `input sheets` or `mapping`.
- SharePoint item path.
- Target subdir.
- Optional sheet name for Excel.
- Whether Snowflake exposure is needed.

Default assumption: if the user asks to add a new input sheet, connect an Excel, or get a SharePoint/OneDrive file into data/Snowflake and does not narrow the scope, Snowflake exposure is in scope.

## Workflow
1. Open repo instructions:
   - `/Users/martin/Documents/adrez/extractor-spreadsheets/AGENTS.md`
   - `/Users/martin/Documents/adrez/extractor-spreadsheets/README.md`
   - `/Users/martin/Documents/adrez/data-factory/AGENTS.md`
   - `/Users/martin/Documents/adrez/data-factory/README.md`
2. Update `/Users/martin/Documents/adrez/extractor-spreadsheets/ingest_config.yml` using an existing same-type entity as template.
3. Assess extractor config details:
   - folder globs are direct-child only,
   - correction overlays may share the same `target_subdir`,
   - folder queues may require `processed_path` and `processed_date_timezone`,
   - `processed_path` needs write permission,
   - entities may need `parser`, `source_encoding`, or `allow_empty`.
4. Validate landing locally:
```bash
cd /Users/martin/Documents/adrez/extractor-spreadsheets
./run_ingest.sh --only <entity_name>
```
5. Update the downstream external-table config in `/Users/martin/Documents/adrez/data-factory/configs/input_sheets.yaml` or `/Users/martin/Documents/adrez/data-factory/configs/mapping.yaml`, matching the same `target_subdir`.
6. Validate Snowflake exposure locally:
```bash
cd /Users/martin/Documents/adrez/data-factory
./scripts/data-factory-local --config configs/<file>.yaml
```
7. Respect the config's existing mode. `configs/input_sheets.yaml` and
   `configs/mapping.yaml` usually use `mode: full`. If an incremental config
   introduces new formats/stages, run once with full mode:
```bash
./scripts/data-factory-local --config configs/<file>.yaml --mode full
```
8. Check whether production has an explicit `CONFIG_PATHS` override. Normally no change is needed for top-level `configs/*.yaml` because data-factory autodiscovers them.
9. If the user says the files already land in ADLS, skip extractor and use `entity-data-factory` only.
10. If the user says landing only, stop after extractor validation.

## Done checklist
- Extractor config updated and validated.
- Downstream data-factory config updated and validated when in scope.
- Matching folder/subdir names stay aligned across both repos.
- `CONFIG_PATHS` override impact assessed.
