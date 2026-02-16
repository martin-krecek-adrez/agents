---
name: entity-dbt-cloud
description: Add a new dbt entity/model entry point in dbt-cloud (usually l1_raw first), docs/tests, and selector-based validation.
compatibility: Requires /Users/martin/Documents/adrez/dbt-cloud and dbt environment access.
---

# entity-dbt-cloud

Use this skill when adding a new entity/table model in `dbt-cloud`.

## Default scope rule
- Unless explicitly requested otherwise, stop at the first model entry point (`l1_raw`), plus schema docs/tests.
- Do not auto-build full `l2/l3` chain in the same task unless requested.

## Inputs to confirm
- Entity name and expected source.
- Target folder/layer (`l1_raw` by default).
- Required columns and primary keys.
- Whether downstream (`l2/l3`) is in scope.

## Workflow
1. Open `/Users/martin/Documents/adrez/dbt-cloud/AGENTS.md` and relevant nearby schema/model files.
2. Create model SQL (typically `models/l1_raw/.../raw_<entity>.sql`).
3. Update corresponding `schema.yml`/`schema.yaml` with descriptions/tests.
4. If requested, wire to downstream layers (`l2/l3`) explicitly.
5. Validate with selector-based run:
```bash
cd /Users/martin/Documents/adrez/dbt-cloud
dbt build --select <model_name>
```
6. If environment blocks validation, document exact reason in task note/handoff.
7. If non-trivial, create/update `docs/tasks/YYYY-MM-DD-<task>.md`.

## Done checklist
- Model added in correct layer/path.
- Schema docs/tests updated.
- Selector validation run or documented blocker.

