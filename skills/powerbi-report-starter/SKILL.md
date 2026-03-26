---
name: powerbi-report-starter
description: Create a new Power BI semantic model and report scaffold from scratch using the repo script, with canonical DIM_DATE and optional role-playing date tables.
scope: business
status: active
owner: martin
last_reviewed: 2026-03-26
compatibility: Requires /Users/martin/Documents/adrez/powerbi and local Python environment per repo README.
---

# powerbi-report-starter

Use this skill when the task is to create a new Power BI report or semantic model from scratch in the `powerbi` repo.

This skill is for scaffolding and first-pass setup.
For incremental edits to an existing report or semantic model, follow repo-local guidance in `/Users/martin/Documents/adrez/powerbi/AGENTS.md`.

## Inputs to confirm
- Base solution name.
- Optional semantic model name override.
- Optional report name override.
- Date roles to scaffold (for example `created`, `cancelled`, `consumed`, `snapshot`).
- Whether to run only `--dry-run` or write files.
- Whether static validation is in scope after scaffolding.

## Workflow
1. Open `/Users/martin/Documents/adrez/powerbi/AGENTS.md` and `README.md`.
2. Prefer the built-in scaffold script:
```bash
cd /Users/martin/Documents/adrez/powerbi
python3 scripts/create_blank_report.py --name "<name>" --roles <role1> <role2> --dry-run --pretty
```
3. Review the dry-run output before writing files.
4. Write the scaffold only after the target names and roles are confirmed:
```bash
python3 scripts/create_blank_report.py --name "<name>" --roles <role1> <role2> --force --pretty
```
5. Validate locally with the umbrella validator when in scope:
```bash
python3 scripts/validate.py --mode static
```
6. Runtime validation, DEV sync, or PROD sync are separate follow-up steps. Do not push or trigger release-style sync unless the user explicitly asks.

## Done checklist
- Report and semantic model scaffold created in `workspace/`.
- Canonical `DIM_DATE` and requested role-playing date tables are present.
- Static validation ran or the reason it did not run was stated.
