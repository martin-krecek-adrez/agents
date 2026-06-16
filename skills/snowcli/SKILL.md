---
name: snowcli
description: CLI for Snowflake. Query data, inspect warehouses/databases/schemas/tables/stages, describe objects, and validate Snowflake state. Use when the user says "koukni do Snowflake", "podivej se do Snowflake", "pust SQL", "over tabulku ve Snowflake", "ukaz schema", "najdi columns", "zkontroluj data ve Snowflake", or "over external table".
scope: business
status: active
owner: martin
last_reviewed: 2026-06-16
compatibility: Requires snow CLI (docs.snowflake.com/en/developer-guide/snowflake-cli). Needs ~/.snowflake/config.toml with connection config.
---

# snowcli

CLI for Snowflake via [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli).

## Quick Reference

```bash
# Run SQL query (use --format json for pipeable output)
snow sql -q "SELECT * FROM table LIMIT 10" --format json

# Show objects
snow sql -q "SHOW WAREHOUSES" --format json
snow sql -q "SHOW DATABASES" --format json
snow sql -q "SHOW SCHEMAS" --format json
snow sql -q "SHOW TABLES" --format json
snow sql -q "SHOW TABLES IN database.schema" --format json

# Describe table structure
snow sql -q "DESCRIBE TABLE database.schema.table" --format json

# Object commands
snow object list warehouse --format json
snow object list database --format json
snow object list schema --format json
snow object list table --format json

# Connection test
snow connection test
```

## Output Formats

Always use `--format json` for agent workflows (pipeable to jq):

```bash
snow sql -q "SHOW TABLES" --format json | jq '.[].name'
snow sql -q "SELECT * FROM t" --format json | jq 'length'
```

Available formats: `json`, `csv`, `tsv`, `plain`, `table` (default).

## Safety

- Default to read-only SQL and metadata inspection.
- Do not run DDL, DML, `TRUNCATE`, warehouse changes, stage uploads/removals, or other mutating Snowflake commands unless the user explicitly asks for that action.

## Specifying Connection

```bash
snow sql -q "SHOW TABLES" -c connection_name
```

---

See [references/setup.md](references/setup.md) for configuration and authentication.
See [references/examples.md](references/examples.md) for query patterns and workflows.
