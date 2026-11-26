---
name: avalanche-metadata-update
description: Rebuild, validate, export, and sync metadata-builder outputs for Avalanche MCP catalog and local metadata files. Use when the user says "refreshni Avalanche metadata", "prebuilduj MCP catalog", "syncni metadata do avalanche-mcp", "exportni metadata bundle", "validuj metadata contract", or asks to validate/update both Avalanche catalogs.
scope: business
status: active
owner: martin
last_reviewed: 2026-09-28
compatibility: Requires /Users/martin/Documents/adrez/metadata-builder and optionally /Users/martin/Documents/adrez/avalanche-mcp.
---

# avalanche-metadata-update

Use this skill when the task is to refresh Avalanche metadata from `metadata-builder`.

## Catalogs

| Profile | Builder product | Local catalog | R2 object |
| --- | --- | --- | --- |
| Technical Avalanche | `l2_base_output` | `mcp_metadata_bundle/catalog.json` | `catalog.json` |
| Avalanche 2.0 | `l3_avalanche` | `mcp_metadata_bundle_avalanche/catalog_avalanche.json` | `catalog_avalanche_v2.json` |

## Workflow

1. Read the owning repositories' `AGENTS.md` and identify the environment and profile.
2. For technical metadata, use the [Metadata Builder README](https://github.com/adrez-com/metadata-builder/blob/main/README.md). Run `scripts/build_metadata_artifact.py --product-key l2_base_output` with the maintained product configuration and the approved profiling scope. Validate the profiles with `scripts/validate_metadata_contract.py` before export.
3. For Avalanche 2.0, use [the catalog guide](https://github.com/adrez-com/metadata-builder/blob/main/docs/avalanche-pilot.md). Run `scripts/run_avalanche_metadata_refresh.py` with `l3_avalanche` and the dbt manifest for the same environment and revision.
4. Validate each generated catalog from the Avalanche MCP repo with `npm run validate-catalog -- --file <catalog-path>`. Record the catalog path, entity count and dbt revision.
5. For scheduled builds and R2 publication, use the [Airflow runbook](https://github.com/adrez-com/metadata-builder/blob/main/docs/airflow-metadata-refresh.md) and verify the intended object key after the approved write.

## Optional local sync

Check the target repository and run a dry run before syncing technical metadata to a local consumer.

```bash
git -C "$AVALANCHE_MCP_REPO" status -sb
rsync -ani --delete \
  "$METADATA_BUILDER_REPO/mcp_metadata_bundle/metadata/" \
  "$AVALANCHE_MCP_REPO/metadata/"
```

Apply the sync only when its scope matches the requested changes.
