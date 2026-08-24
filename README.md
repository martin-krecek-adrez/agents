# Agent Configuration

Configuration for Codex/Codex CLI usage in the Adrez workspace.

## Audience and ownership

This repository is Martin's local control hub. Its sync manages Martin-only
operating, tracking, context, and life skills. Team members must not run this
repository's sync; their portable onboarding lives in
`adrez-com/tech-plugins/README.md` and uses the `Adrez Tech` marketplace.

The absolute `/Users/martin/...` paths below are intentional local defaults for
this managed setup, not copyable instructions for another machine. Team plugin
content must remain machine-portable and must not use these paths.

## Setup

### [Codex](https://developers.openai.com/codex)

Install and verify the team plugin before the first managed sync:

```bash
python3 /Users/martin/Documents/adrez/tech-plugins/plugins/adrez-data-platform/scripts/check_local_skill_conflicts.py
codex plugin marketplace add git@github.com:adrez-com/tech-plugins.git
codex plugin add adrez-data-platform@adrez-tech
codex plugin list --json
```

Then preflight and sync the directly managed setup:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh --preflight-only
bash /Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh
python3 /Users/martin/Documents/adrez/tech-plugins/plugins/adrez-data-platform/scripts/check_local_skill_conflicts.py --installed
```

This sync installs only directly managed operating, context, and out-of-plugin
skills. Team data-platform skills are installed separately from the
`Adrez Data Platform` plugin in `adrez-com/tech-plugins`; they must not be
copied into `~/.codex/skills`. The sync intentionally fails without one
complete, enabled plugin runtime so it cannot delete legacy copies prematurely.

The portable preflight is the default for every plugin user. It reports direct
name conflicts without mutation, can archive unmanaged copies only when invoked
with `--archive-conflicts`, and refuses to archive entries owned by another
managed sync. This repository's transactional sync is the source-aware migration
for Martin's managed copies; do not use the generic archive option for those.

Run setup checks:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/check_ai_setup.sh
```

The weekly report-only audit also runs a network-dependent freshness check:

```bash
python3 /Users/martin/Documents/adrez/agents/scripts/check_adrez_data_platform_update.py
```

This check compares the installed cache and local marketplace snapshot with
remote `main` without changing an existing checkout or plugin installation.
Network unavailability is reported as a warning, never as proof that no update
exists.

`check_ai_setup.sh` also runs:
- `scripts/validate_business_skills.py` for Adrez skill metadata and UI prompts.
- `scripts/check_repo_hygiene.sh` for tracked junk files such as `.DS_Store`.

See [Skills](https://developers.openai.com/codex/skills) and [AGENTS.md](https://developers.openai.com/codex/guides/agents-md) for details.

## Routing Summary

Main routing is defined in `AGENTS.md`.

- Default workspace scope: `/Users/martin/Documents/adrez`
- Default repo routing:
  - `dbt-cloud` for dbt models/finance/Snowflake analytics work
  - `extractor-spreadsheets` first for new OneDrive/SharePoint spreadsheets and mapping sheets
  - `data-factory` for already-landed ADLS sources and external-table exposure
  - `data-platform` for shared platform/data tooling
  - `avalanche-mcp` for current MCP analytics / agent work
  - `metadata-builder` for Avalanche metadata/catalog build
  - `powerbi` for Power BI / Fabric work
- Archived repos (historical reference only):
  - `adrez-data-assistant`
  - `adrez-metadata-sql-agent`
  - `extractor-documents`
- Expedia payout/remittance PDF extraction is owned by `extranet-scraper`.
- New document extraction is routed to the owning active source/ingestion repo.
- Skill routing highlights:
  - Thread intake / agent orchestration -> `adrez-agent-orchestration`
  - Snowflake-related requests -> `snowcli`
  - Explicit legacy Asana lookup -> `asana`
  - Commit message drafting -> `write-commit`
  - Documentation requests -> `write-docs`
  - Reusable harness/process feedback -> `agent-feedback-capture`
  - Tech comparisons -> `compare-tech`
  - Implementation diff/milestone review -> `implementation-review`
  - Parallel repo branches / dirty worktree safety -> `repo-worktree-safety`
  - End-to-end spreadsheet onboarding -> `entity-spreadsheet-ingestion`
  - Add/update spreadsheet entity -> `entity-extractor-spreadsheets`
  - Add/update external-table entity -> `entity-data-factory`
  - Add/update dbt entity/model -> `entity-dbt-cloud`
  - New Power BI report/model scaffold -> `powerbi-report-starter`
  - Rebuild/export Avalanche metadata -> `avalanche-metadata-update`

## Ops Memory

Cross-repo operating state for Codex coordination lives in:
- `/Users/martin/Documents/adrez/agents/ops`

Use it for Chief of Staff briefs, open loops, people follow-ups, pipeline watch
items, and thread handoff prompts. Keep repo implementation notes in repo-local
`docs/tasks/`.

## Skills

Directly managed Adrez operating, context, and out-of-plugin skills live in:
- `/Users/martin/Documents/adrez/agents/skills`

Personal skills live in:
- `/Users/martin/Documents/live/agent/skills`

Use `scripts/sync_codex_setup.sh` to sync those two source roots into
`~/.codex/skills`.

Team data-platform and repository-delivery skills live only in:
- `adrez-com/tech-plugins/plugins/adrez-data-platform/skills`

Install them through the `Adrez Tech` plugin marketplace. Ownership is enforced
by the plugin's bundled `skill-inventory.txt`; the sync fails if an inventory
name appears in either directly managed source root or direct runtime.

### Adding or changing a skill

- Reusable team data-platform or repository-delivery workflow: change the
  `adrez-data-platform` plugin in `tech-plugins`.
- Reusable workflow for another team domain: use the matching plugin in
  `tech-plugins`; do not put every team workflow into `adrez-data-platform`.
- Martin-only Adrez operating, tracking, or context workflow: change
  `agents/skills` and update this README plus `ops/skills-inventory.md`.
- Life-only workflow: change the personal agent repository.
- Never edit `~/.codex/skills` or the plugin cache as a source.

For a direct skill change, run `scripts/sync_codex_setup.sh --preflight-only`,
the actual sync, and `scripts/check_ai_setup.sh`, then start a new Codex task so
the refreshed skill registry is loaded. For a plugin change, follow the
contribution and release checklist in `tech-plugins/README.md`. Promoting a
direct skill into a plugin uses the source-aware cutover below so no name is
owned by both sources.

### Data Platform plugin cutover

Apply ownership changes in this order:

1. Merge, tag, and publish `adrez-data-platform` in `adrez-com/tech-plugins`.
2. Run the portable conflict preflight. Existing managed copies are expected
   during this one-time cutover; do not archive them generically:

   ```bash
   python3 /Users/martin/Documents/adrez/tech-plugins/plugins/adrez-data-platform/scripts/check_local_skill_conflicts.py
   ```

3. Add the marketplace and install the plugin, but do not start a new task:

   ```bash
   codex plugin marketplace add git@github.com:adrez-com/tech-plugins.git --ref main
   codex plugin add adrez-data-platform@adrez-tech
   ```

4. Merge the `agents` ownership cutover so the managed source no longer owns
   the plugin skill names.
5. Run a no-write preflight, the transactional sync, the generic conflict check,
   and the health check:

   ```bash
   export ADREZ_TECH_PLUGINS_ROOT=<resolved-tech-plugins-checkout>
   bash scripts/sync_codex_setup.sh --preflight-only
   bash scripts/sync_codex_setup.sh
   python3 "${ADREZ_TECH_PLUGINS_ROOT}/plugins/adrez-data-platform/scripts/check_local_skill_conflicts.py" --installed
   bash scripts/check_ai_setup.sh
   ```

   Resolve the placeholder to the main checkout or task worktree being released;
   do not paste it literally.

6. Start a new Codex task so the installed plugin skills are loaded.

The sync verifies `installed` and `enabled` state, exact version, bundled
inventory, every cached `SKILL.md`, and source/cache payload equality when a
source checkout is available. It stages all direct skills before replacing any
runtime path and refuses symlink targets.

### Upgrade and rollback

For a version-only upgrade whose inventory does not claim another directly
managed name, publish matching Codex and Claude manifest versions, refresh the
marketplace, reinstall, run the installed-inventory preflight and health check,
and start a new task:

```bash
codex plugin marketplace upgrade adrez-tech
codex plugin add adrez-data-platform@adrez-tech
python3 "${ADREZ_TECH_PLUGINS_ROOT}/plugins/adrez-data-platform/scripts/check_local_skill_conflicts.py" --installed
bash scripts/sync_codex_setup.sh --preflight-only
bash scripts/check_ai_setup.sh
```

If an upgrade adds a skill name currently owned by `agents`, treat it as another
ownership cutover: publish and install the plugin without starting a new task;
merge removal of that name from the directly managed source; then run the actual
transactional sync before the generic check and health check:

```bash
bash scripts/sync_codex_setup.sh --preflight-only
bash scripts/sync_codex_setup.sh
python3 "${ADREZ_TECH_PLUGINS_ROOT}/plugins/adrez-data-platform/scripts/check_local_skill_conflicts.py" --installed
bash scripts/check_ai_setup.sh
```

Only after all four commands pass should a new task be started. The first
pre-install conflict report is expected to show a managed copy; never archive
that copy with the generic helper.

Prefer a forward revert with a new patch release. Do not uninstall or disable a
working plugin before its replacement passes the runtime check. If the agents
cutover itself must be rolled back, first revert the agents commit so the direct
skill sources and previous sync implementation are restored, run that sync, and
verify the direct runtime files. Then remove the plugin, start a new task, and
verify that task loads only the restored direct skills.

Current directly managed Adrez skills:
- adrez-agent-orchestration
- adrez-thread-orchestration
- adrez-linear-workflow
- asana
- agent-feedback-capture
- ai-context-maintenance
- compare-tech
- avalanche-metadata-update
- grill-me
- powerbi-report-starter
- write-commit

## Credits

- michalvavra for the original structure
