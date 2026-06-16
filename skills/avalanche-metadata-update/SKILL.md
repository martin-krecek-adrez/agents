---
name: avalanche-metadata-update
description: Rebuild, validate, export, and sync metadata-builder outputs for Avalanche MCP catalog and local metadata files. Use when the user says "refreshni Avalanche metadata", "prebuilduj MCP catalog", "syncni metadata do avalanche-mcp", "exportni metadata bundle", "validuj metadata contract", or asks to validate/update both Avalanche catalogs.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-16
compatibility: Requires /Users/martin/Documents/adrez/metadata-builder and optionally /Users/martin/Documents/adrez/avalanche-mcp.
---

# avalanche-metadata-update

Use this skill when the task is to refresh Avalanche metadata from `metadata-builder`.

## Default scope
- Primary source repo: `/Users/martin/Documents/adrez/metadata-builder`
- Primary consumer repo: `/Users/martin/Documents/adrez/avalanche-mcp`
- Main outputs:
  - `mcp_metadata_bundle/catalog.json`
  - `mcp_metadata_bundle_ai/catalog_ai.json`
  - `mcp_metadata_bundle/metadata/*.json`

## Workflow
1. Open:
   - `/Users/martin/Documents/adrez/metadata-builder/AGENTS.md`
   - `/Users/martin/Documents/adrez/metadata-builder/README.md`
   - `/Users/martin/Documents/adrez/avalanche-mcp/AGENTS.md` before touching or validating consumer repo files.
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
5. Build and export the AI catalog too:
```bash
scripts/run_ai_metadata_refresh.sh
```
6. Validate both catalog files against the Avalanche catalog schema:
```bash
cd /Users/martin/Documents/adrez/avalanche-mcp
npm run validate-catalog -- --file /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/catalog.json
npm run validate-catalog -- --file /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle_ai/catalog_ai.json
```
7. Before syncing local Avalanche metadata files, verify the target repo and review a dry run:
```bash
git -C /Users/martin/Documents/adrez/avalanche-mcp status -sb
test -d /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/metadata
test -f /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/catalog.json
test -f /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle_ai/catalog_ai.json

rsync -ani --delete \
  /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/metadata/ \
  /Users/martin/Documents/adrez/avalanche-mcp/metadata/
```
8. Sync local Avalanche metadata files only when the dry run matches the intended scope:
```bash
rsync -a --delete \
  /Users/martin/Documents/adrez/metadata-builder/mcp_metadata_bundle/metadata/ \
  /Users/martin/Documents/adrez/avalanche-mcp/metadata/
```
9. If the task includes publishing or seeding catalogs, update both Avalanche catalog objects (`catalog.json` and `catalog_ai.json`) using current `avalanche-mcp` repo guidance. Do not use stale `docs/catalog.json` or `seed-catalog` paths.

## Done checklist
- `profiles_output_ai/l2_base_output` rebuilt.
- `profiles_output_ai/l2_base_output_ai` rebuilt when AI catalog refresh is in scope.
- Contract validation passed.
- `mcp_metadata_bundle/catalog.json` regenerated.
- `mcp_metadata_bundle_ai/catalog_ai.json` regenerated.
- Both catalogs validated with `npm run validate-catalog -- --file ...`.
- Avalanche sync dry run reviewed before any `rsync --delete`.
- Avalanche local metadata sync completed when in scope.
- Any skipped step is called out explicitly in handoff.
