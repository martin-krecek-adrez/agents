---
name: entity-data-factory
description: Add or update an entity config in data-factory external-table sync flow and validate with local run.
compatibility: Requires /Users/martin/Documents/adrez/data-factory and local Snowflake credentials/key setup per README.
---

# entity-data-factory

Use this skill when the task is to add or modify entity configs in `data-factory` (`configs/*.yaml`), including external table ingestion setup.

## Inputs to confirm
- Config file path (`configs/<name>.yaml`).
- Entity identifier and source folder/path.
- Whether this is incremental-only or needs first full run.
- Whether function app `CONFIG_PATHS` must be updated.

## Workflow
1. Open `/Users/martin/Documents/adrez/data-factory/AGENTS.md` and `README.md`.
2. Edit `configs/*.yaml` using same-type entity template.
3. Keep naming/path conventions and schema behavior aligned.
4. Validate locally:
```bash
cd /Users/martin/Documents/adrez/data-factory
python3 main.py --config configs/<file>.yaml
```
5. If incremental config introduces new formats/stages, run once with full mode:
```bash
python3 main.py --config configs/<file>.yaml --mode full
```
6. Note whether Azure Function `CONFIG_PATHS` must include the config.
7. If non-trivial, create/update `docs/tasks/YYYY-MM-DD-<task>.md`.

## Done checklist
- Config updated and validated locally.
- Full-mode bootstrap considered where needed.
- `CONFIG_PATHS` impact assessed.

