# Agent Configuration

Configuration for Codex/Codex CLI usage in the Adrez workspace.

## Setup

### [Codex](https://developers.openai.com/codex)

Install and verify the team plugin before the first managed sync:

```bash
codex plugin marketplace add git@github.com:adrez-com/tech-plugins.git
codex plugin add adrez-data-platform@adrez-tech
codex plugin list --json
```

Then preflight and sync the directly managed setup:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh --preflight-only
bash /Users/martin/Documents/adrez/agents/scripts/sync_codex_setup.sh
```

This sync installs only directly managed operating, context, and out-of-plugin
skills. Team data-platform skills are installed separately from the
`Adrez Data Platform` plugin in `adrez-com/tech-plugins`; they must not be
copied into `~/.codex/skills`. The sync intentionally fails without one
complete, enabled plugin runtime so it cannot delete legacy copies prematurely.

Run setup checks:

```bash
bash /Users/martin/Documents/adrez/agents/scripts/check_ai_setup.sh
```

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
  - Asana updates/comments -> `asana`
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

### Data Platform plugin cutover

Apply ownership changes in this order:

1. Merge, tag, and publish `adrez-data-platform` in `adrez-com/tech-plugins`.
2. Add the marketplace and install the plugin:

   ```bash
   codex plugin marketplace add git@github.com:adrez-com/tech-plugins.git
   codex plugin add adrez-data-platform@adrez-tech
   ```

3. Merge the `agents` ownership cutover.
4. Run a no-write preflight, the transactional sync, and the health check:

   ```bash
   export ADREZ_TECH_PLUGINS_ROOT=<resolved-tech-plugins-checkout>
   bash scripts/sync_codex_setup.sh --preflight-only
   bash scripts/sync_codex_setup.sh
   bash scripts/check_ai_setup.sh
   ```

   Resolve the placeholder to the main checkout or task worktree being released;
   do not paste it literally.

5. Start a new Codex task so the installed plugin skills are loaded.

The sync verifies `installed` and `enabled` state, exact version, bundled
inventory, every cached `SKILL.md`, and source/cache payload equality when a
source checkout is available. It stages all direct skills before replacing any
runtime path and refuses symlink targets.

### Upgrade and rollback

For an upgrade, publish a release with matching Codex and Claude manifest
versions, refresh the marketplace, reinstall, run the preflight and health
check, and start a new task:

```bash
codex plugin marketplace upgrade adrez-tech
codex plugin add adrez-data-platform@adrez-tech
bash scripts/sync_codex_setup.sh --preflight-only
bash scripts/check_ai_setup.sh
```

Prefer a forward revert with a new patch release. Do not uninstall or disable a
working plugin before its replacement passes the runtime check. If the agents
cutover itself must be rolled back, first revert the agents commit so the direct
skill sources and previous sync implementation are restored, run that sync,
verify a new task loads the direct skills, and only then disable the plugin.

Current directly managed Adrez skills:
- adrez-agent-orchestration
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
