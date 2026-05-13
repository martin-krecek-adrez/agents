---
name: avalanche-metadata-update
description: Rebuild, validate, export, and sync metadata-builder outputs for Avalanche MCP catalog and local metadata files.
scope: business
status: active
owner: martin
last_reviewed: 2026-05-12
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
  --product-key l2_base_output \
  --products-config profiles/products.yml \
  --model gpt-5-mini \
  --api-key-file .secrets/openai_api_key.txt
```
3. Validate contract:
```bash
python scripts/validate_metadata_contract.py \
  --metadata-dir profiles_output_ai/l2_base_output \
  --review-governance-dir contracts/agent
```
4. Export MCP bundle:
```bash
python3 scripts/export_mcp_metadata_json.py \
  --tables-dir profiles_output_ai/l2_base_output \
  --global-dir metadata/global \
  --output-dir mcp_metadata_bundle
```
5. Before syncing local Avalanche files, verify the target repo and review a dry run:
```bash
git -C /Users/martin/Documents/adrez/avalanche-mcp status -sb
test -d /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/metadata
test -f /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/catalog.json

rsync -ani --delete \
  /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/metadata/ \
  /Users/martin/Documents/adrez/avalanche-mcp/metadata/
```
6. Sync local Avalanche files only when the dry run matches the intended scope:
```bash
rsync -a --delete \
  /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/metadata/ \
  /Users/martin/Documents/adrez/avalanche-mcp/metadata/

cp /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/catalog.json \
  /Users/martin/Documents/adrez/avalanche-mcp/docs/catalog.json
```
7. If the task includes local Avalanche seeding, run:
```bash
cd /Users/martin/Documents/adrez/avalanche-mcp
npm run seed-catalog -- local
```

## Done checklist
- `profiles_output_ai/l2_base_output` rebuilt.
- Contract validation passed.
- `mcp_metadata_bundle/catalog.json` regenerated.
- Avalanche sync dry run reviewed before any `rsync --delete`.
- Avalanche local metadata/docs sync completed when in scope.
- Any skipped step is called out explicitly in handoff.
