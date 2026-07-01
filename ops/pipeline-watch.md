# Pipeline Watch

Signals Chief of Staff should look for in email, Teams, CI, and status surfaces.

## Watch Patterns

| Signal | Where | Treat As Important When |
| --- | --- | --- |
| Pipeline failed | Outlook Email / Teams / GitHub Actions | Any Adrez ingestion, extractor, dbt, deploy, or scheduler failure. |
| Pipeline warning | Outlook Email / Teams / GitHub Actions | The same warning repeats, mentions missing data, or blocks reporting. |
| Pipeline success | Outlook Email / Teams | Only surface when a previously failing or explicitly watched pipeline recovers. |
| Missing expected status | Outlook Email / Teams | A regular success/failure email is absent and the pipeline is important today. |

## Surfacing Rules

- Surface failures and repeated warnings.
- Surface recoveries only when they close a previously surfaced failure.
- Do not keep surfacing recovered CI/deploy items unless a new failure appears.
- Do not infer pipeline health from empty Teams bodies; use Outlook, GitHub,
  dbt, Better Stack, or task notes when a real incident is suspected.
- Keep low-urgency platform notices as watch/backlog items unless they have a
  near-term deadline or concrete operational risk today.

## Active Watches

| Item | Source | Expected Signal | Notes | Updated |
| --- | --- | --- | --- | --- |
| VN48 / VN3 Mews order item recovery | Teams / Outlook / dbt task notes | Power BI / weekly report remains recovered; no new mass soft-delete spike | 2026-05-21 hotfix limited soft-delete reconciliation to eight validated weekly entities; today's dbt Cloud production run warned instead of failing. Remaining follow-up is monitoring `_inc` freshness and optional diagnostics audit. | 2026-05-22 |
| Power BI Fabric sync | Outlook / GitHub | Resolved unless new failure appears | Latest checked `dev` runs still show successful newer run `c53d07a` after failed `920e2b9`; no new failure surfaced in Outlook. | 2026-05-21 |
| Pipeline orchestrator deploy worker | Outlook / GitHub | Recovered unless new deploy failure appears | 2026-06-30 `gh run list` shows newer successful `Deploy Worker` runs on `main` after the 2026-06-26 failures, latest `Add GitHub API user agent` at 2026-06-29 18:58 UTC. | 2026-06-30 |
| dbt reservation freshness warning | Outlook / dbt Cloud / Snowflake | Warning cleared or understood | 2026-05-25 Snowflake check shows 7 property reservation increment files still last modified on 2026-05-24 04:51-05:42 UTC while the other 10 properties have 2026-05-25 files. Stale: `czprg_palac_u_kocku`, `czprg_river_dance`, `czprg_vn17_rooftop`, `czprg_theatre_9`, `czprg_prague_residences`, `czprg_vn48_suites`, `czprg_vn3_terraces`. Likely ingestion/source landing gap, not dbt-only. | 2026-05-25 |
| Power Automate Teams pipeline alert flow | Outlook / Teams | Flow healthy before Teams pipeline notifications are trusted | 2026-05-22 Power Automate reported 1 failure for `Send webhook alerts to Data pipeline notification`; Teams connector was 429 on 2026-05-25 so channel verification was unavailable. | 2026-05-25 |
| Mews weekly delete reconciliation runtime | data-factory task note | Production rehearsal before enabling parallel workers | Read-only sandbox benchmark showed `tableWorkers=8` reducing runtime from 26.1s to 7.1s with schemas matching; row/hash compare needs same snapshot window before production enablement. | 2026-05-25 |
| Power BI Fabric sync dev failures | Outlook / GitHub | Recovered unless new failure appears | 2026-05-29 `gh run list` showed multiple newer successful `adrez-com/powerbi` Fabric sync runs on `dev`; latest checked run `26586118726` succeeded at 2026-05-28 15:57 UTC. | 2026-05-29 |
| Mews source property names | dbt task notes / Martin correction | Resolved; do not keep surfacing unless new `CZPRG` pollution appears | L1 data patch is done and temporary hotfix removal is already in `origin/main` as `c9981a6 Remove Mews CZPRG cleanup hooks (#51)`. | 2026-06-02 |
| Mews ingestor landing coverage | Martin correction / local task note | Data available; do not rank as blocker unless new failure appears | Martin sent the update to Michal and says data is available. Historical findings remain useful context only: `address` increment gap, sparse `resource_block`, and 2026-05-25 16/17 files. | 2026-06-01 |
| Pipeline orchestrator re-enable | Martin correction | Check tomorrow whether it ran and model count is lower | Orchestrator was disabled due dbt model limit. New month plus fewer dbt models/views removed should allow re-enabling; tomorrow verify 1) it ran, 2) fewer models ran. | 2026-06-01 |
| dbt reservation freshness warning | Martin correction | Resolved unless warning returns | Martin says data was filled on 2026-06-09 and there is no error today; do not surface as active. | 2026-06-09 |
| Azure budget spike | Outlook/Gmail Azure budget alerts | Review cost source before it burns the monthly budget | Budget alert moved from 25.24 USD on 2026-06-04 to 50.29 USD on 2026-06-06, then to 76.09 USD at 2026-06-08 16:04 UTC against 100 USD monthly budget. | 2026-06-09 |
| Teams pipeline notification body visibility | Teams | Do not infer success/failure from empty connector posts | 2026-06-08 Data pipeline notification and 2026-06-07 Better Stack posts still fetch as empty bodies. Use external status checks if incident suspicion appears. | 2026-06-08 |
| Power BI Fabric sync/dev deploy | Outlook / GitHub | Recovered unless report/refresh smoke fails | 2026-06-08 `Fabric sync on push` failed for `96cb35f` (`Add Rev Management report`) and 2026-06-09 had two failed `Fabric CICD deploy` dispatches, but `gh run list` on 2026-06-10 showed newer successful `dev` deploy runs, latest `Set cash recon defaults to May` at 2026-06-09 14:06 UTC. | 2026-06-10 |
| PPR room inventory / OOO availability | dbt task notes / Martin correction | Martin is handling separately | Report broke; do not frame this as a simple Power BI denominator rollout until Martin confirms the repair path. | 2026-06-12 |
| Azure GPv1 storage retirement | Outlook Azure service notice / Linear | Tracked in Linear for late July check | Repo references `stadrezdevweu`, `stbookingdatahubweu`, and Terraform backend `stadreztfstateshared`; if any are legacy GPv1 / `Kind=Storage`, migrate to GPv2 before 2026-10-13. Linear `DTE-48` due 2026-07-31 captures the check/migration task. | 2026-06-15 |
| dbt Mews rate-pricing freshness | Outlook dbt Cloud / Martin correction | OK unless a fresh warning/failure appears | 2026-06-14 Production daily run warned on 4 per-property freshness tests for Mews rate-pricing sources: `rate_pricing`, `rate_pricing_category_amountprices`, `rate_pricing_category_adjustment`, and `rate_pricing_age_category_adjustment`, each WARN 17. Martin confirmed on 2026-06-23 that dbt is OK; do not surface as active unless a new warning/failure appears. | 2026-06-23 |
| Azure billing/payment method | Outlook Azure / Martin correction | Monitor only unless Azure repeats or blocks service/payment | 2026-06-22 Outlook showed Azure payment-method issue notices. Martin clarified on 2026-06-23 that Azure billing was some error; monitor, but do not treat as active escalation unless it repeats or becomes blocking. | 2026-06-23 |
| Booking Data Scraper telemetry | Teams Better Stack / Martin correction | Not Martin-owned; surface only if explicitly escalated to Data/Adrez ops | 2026-06-14 Teams search found repeated Better Stack `Booking Data Scraper Telemetry` failure-event incidents with auto-resolves. Martin clarified this is a software engineering problem and not for him to handle. | 2026-06-15 |
| Power BI Fabric sync main | Outlook / GitHub | Recovered unless new main/dev deploy failure appears | Outlook showed 2026-06-12 `Fabric sync on push - main` failure for `d03c57e`; `gh run list` showed multiple successful Fabric CICD runs afterward on 2026-06-12, including main and dev. Martin confirmed treat as OK. | 2026-06-15 |
| Teams pipeline notification bodies | Teams | Do not infer success/failure from empty connector posts | 2026-06-16 Data pipeline notification 06:34 CEST and Better Stack 23:51 CEST fetched with empty bodies again; Outlook found no matching fresh pipeline failure. | 2026-06-16 |
| dbt Production daily run / Pipeline default | Martin correction / Outlook dbt Cloud / Teams Data pipeline | Resolved unless a fresh failure appears | 2026-07-01 morning Outlook dbt said `Production daily run` failed after `dbt build` errored in 27m09s; Teams Data pipeline later showed started/completed at 09:14/09:57 CEST. Martin confirmed dbt was resolved separately and Power BI/reports were refreshed, so do not surface as open. | 2026-07-01 |
| Reporting Top Line Worker deploy | Outlook / GitHub / Teams | Recovered unless new deploy failure appears | 2026-06-26 Outlook/Teams showed failed `Deploy Top Line Worker` runs, but `gh run list` later showed three successful newer `Deploy Top Line Worker` runs on `main`, latest `Add Top Line internal refresh endpoint (#16)` at 2026-06-26 14:10 UTC. | 2026-06-29 |
| Reporting Rev Management refresh | Outlook / GitHub / Martin correction | Recovered unless next scheduled refresh fails | 2026-06-29 manual test refresh failed, but newer rerun, UUID-triggered run, and 2026-06-30 scheduled-default refresh all succeeded. Martin confirmed on 2026-07-01 that Power BI and reports were refreshed. | 2026-07-01 |
| dbt Cloud successful-model usage | Outlook dbt Cloud | Monthly usage resets 2026-07-01; monitor only unless overage recurs next month | 2026-06-30 dbt email says account exceeded 90% of included 15,000 successful models built; this is a billing/usage watch, not a failed run. | 2026-06-30 |
| Snowflake Trust Center network policy violation | Outlook Snowflake Trust Center | Check whether this is accepted posture or needs scoped remediation | 2026-07-01 unread Snowflake Trust Center email reports 1 critical CIS violation: users not covered by network policy to restrict access to trusted IPs. This is separate from the resolved scanner-charge case. | 2026-07-01 |
