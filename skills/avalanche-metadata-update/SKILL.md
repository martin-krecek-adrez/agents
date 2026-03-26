---
name: avalanche-metadata-update
description: Rebuild, validate, export, and sync metadata-builder outputs for Avalanche MCP catalog and local metadata files.
scope: business
status: active
owner: martin
last_reviewed: 2026-03-26
compatibility: Requires /Users/martin/Documents/adrez/metadata-builder and optionally /Users/martin/Documents/adrez/avalanche-mcp.
---

# avalanche-metadata-update

Use this skill when the task is to refresh Avalanche metadata from `metadata-builder`.

## Default scope
- Primary source repo: `/Users/martin/Documents/adrez/metadata-builder`
- Primary consumer repo: `/Users/martin/Documents/adrez/avalanche-mcp`
- Main outputs:
  - `mcp_metadata_bundle/catalog.json`
  - `mcp_metadata_bundle/metadata/*.json`

## Workflow
1. Open:
   - `/Users/martin/Documents/adrez/metadata-builder/AGENTS.md`
   - `/Users/martin/Documents/adrez/metadata-builder/README.md`
2. Build metadata artifact:
```bash
cd /Users/martin/Documents/adrez/metadata-builder
python scripts/build_metadata_artifact.py \
  --database L2_BASE \
  --schema BASE_OUTPUT \
  --schema-docs /Users/martin/Documents/adrez/dbt-cloud/models/l2_base/base_output/base/schema.yml \
  --join-contracts /Users/martin/Documents/adrez/dbt-cloud/metadata/join_contracts.yml \
  --join-graph-mmd /Users/martin/Documents/adrez/dbt-cloud/data/mermaid/l2_base_base_output.mmd \
  --output-dir profiles_output_ai \
  --model gpt-5-mini \
  --api-key-file .secrets/openai_api_key.txt
```
3. Validate contract:
```bash
python scripts/validate_metadata_contract.py --metadata-dir profiles_output_ai
```
4. Export MCP bundle:
```bash
python3 scripts/export_mcp_metadata_json.py \
  --tables-dir profiles_output_ai \
  --global-dir metadata/global \
  --output-dir mcp_metadata_bundle
```
5. Sync local Avalanche files when needed:
```bash
rsync -a --delete \
  /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/metadata/ \
  /Users/martin/Documents/adrez/avalanche-mcp/metadata/

cp /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/catalog.json \
  /Users/martin/Documents/adrez/avalanche-mcp/docs/catalog.json
```
6. If the task includes local Avalanche seeding, run:
```bash
cd /Users/martin/Documents/adrez/avalanche-mcp
npm run seed-catalog -- local
```

## Done checklist
- `profiles_output_ai` rebuilt.
- Contract validation passed.
- `mcp_metadata_bundle/catalog.json` regenerated.
- Avalanche local metadata/docs sync completed when in scope.
- Any skipped step is called out explicitly in handoff.
