# Workflow simplification, 28 October 2026

Martin approved implementation after the read-only audit and two rounds of
independent review. The initial delivery target was local changes. Martin then
authorized commits, pushes, and review PRs. Merge remains conditional on the
review and checks. No plugin publication or production execution is needed.

## Changes

- Remove repeated Git lifecycle procedures from dbt-cloud, data-factory, and
  reporting. Retain local contracts and conditional links to installed skills
  or their team source. Routine edits need focused checks and diff review.
- Shorten the personal Git policy and restrict the task-branch default to
  non-trivial implementation. Preserve authorization and owned-work safeguards.
- Bind production approval to the task's exact operation instead of a required
  phrase or message order. Require fresh checks. Retry without new approval only
  with proof that no production mutation occurred. Stop after uncertain effects.
- Restore the shared policy from the real historical commit
  `a3b7a5e865065fc9588c77bcd66ac585853e1194`. Its content matches the existing
  dbt-cloud, data-factory, and extractor-spreadsheets copies. Delivery now pins
  those copies to the repaired source commit
  `4a95d3cb1533bd1bfbd1b12c4842de1e5a0fe182`.
- Replace duplicated procedural phrase checks with source, routing, and shared
  block consistency checks. Remove the Airflow validator's release-step name
  requirement. Keep command, version, capacity, and no-data-run checks.

## Locations

All branches are `task/simplify-delivery-20261028`.

| Repository | Working directory | Starting revision |
| --- | --- | --- |
| agents | `_worktrees/agents/simplify-delivery-20261028` | `df14aa17d4c30325c1d4f1c70435a3b5ed862aaf` |
| tech-plugins | `tech-plugins` | `0ecab68` |
| dbt-cloud | `_worktrees/dbt-cloud/simplify-delivery-20261028` | `dc1756ceaf287f71b01fc53aefa0fe672a189ad5` |
| data-factory | `_worktrees/data-factory/simplify-delivery-20261028` | `8c84188cfc98d20949db5906bbd48dbf4f6ccbca` |
| reporting | `_worktrees/reporting/simplify-delivery-20261028` | `83171b967f38e2611c7efaba320717e0ebbfb90e` |
| extractor-spreadsheets | `_worktrees/extractor-spreadsheets/simplify-delivery-20261028` | `d8f9607462048c8af4be20dc3e3a74ce946701e8` |
| airflow-orchestrator | `_worktrees/airflow-orchestrator/simplify-delivery-20261028` | `eb1cc66da024f6fe2ac15a88d9048b6015637332` |

Paths are relative to `/Users/martin/Documents/adrez`. Other tasks' checkouts,
dirty files, handoffs, and installed plugin caches were not edited.
The branch copies are not active shared policy until integrated. Merge the
source repair before its distributed revision pins. Integrate the agents setup
check with the three shortened repository routes. PR checks and review results
belong in the linked GitHub PRs; PRs are attached to this Codex chat.

## Validation and review

- Setup check passed before changes and with the task's repository overrides.
  Logs: `/tmp/adrez-simplify-setup-before.log` and
  `/tmp/adrez-simplify-setup-after.log`.
- `python3 -m unittest discover -s scripts/tests -p test_ai_scope.py -v`: 4 pass.
- Shared-block checker: accepts equal content; rejects changed, missing, and
  duplicated policy blocks. The check runs only during setup maintenance.
- Airflow focused modules `test_airflow_deploy_workflow.py` and
  `test_airflow_control_plane_manifest.py`: 62 pass. Changed Python paths pass
  Ruff check/format. The required repository docstring AST check passes.
- Shell syntax and diff whitespace checks pass. No broad build or runtime test.
- Independent policy review found no blocker. Main-agent Airflow review found
  and resolved a stale prior-approval prohibition and repeated-summary wording.
  Policy scenarios cover prepared delivery, one dbt model, one external config,
  reporting UI, one DAG, and shared runtime changes. This is not live proof.
- Existing size gap: current reporting/main AGENTS.md was 14,856 bytes, above
  the default 12,000-byte limit. This change reduces it to 14,163 bytes. The
  setup size scan reads the older canonical checkout, so its pass does not
  clear this existing gap. No size-budget exception was added.
- Live workflow inspection before push: agents and tech-plugins PR validation
  is active. dbt and Airflow validation is disabled manually. Reporting has
  manual-only validation; data-factory and extractor-spreadsheets exclude
  AGENTS.md from runtime CI paths. Missing checks are not reported as green.

## Agent ledger

1. Two original audit agents covered Airflow/reporting and dbt/data-factory.
2. Two adjudication agents challenged policy and delivery proposals in two
   focused rounds. Main agent selected the final changes.
3. After implementation approval, reused those agents for the Airflow patch
   and independent policy review. No new agents or sidebar tasks were created.
