# Pipeline Watch

Signals Chief of Staff should look for in email, Teams, CI, and status surfaces.

## Watch Patterns

| Signal | Where | Treat As Important When |
| --- | --- | --- |
| Pipeline failed | Outlook Email / Teams / GitHub Actions | Any Adrez ingestion, extractor, dbt, deploy, or scheduler failure. |
| Pipeline warning | Outlook Email / Teams / GitHub Actions | The same warning repeats, mentions missing data, or blocks reporting. |
| Pipeline success | Outlook Email / Teams | Only surface when a previously failing or explicitly watched pipeline recovers. |
| Missing expected status | Outlook Email / Teams | A regular success/failure email is absent and the pipeline is important today. |

## Active Watches

| Item | Source | Expected Signal | Notes | Updated |
| --- | --- | --- | --- | --- |
| VN48 / VN3 Mews order item recovery | Teams / Outlook / dbt task notes | Power BI / weekly report remains recovered; no new mass soft-delete spike | 2026-05-21 hotfix limited soft-delete reconciliation to eight validated weekly entities; today's dbt Cloud production run warned instead of failing. Remaining follow-up is monitoring `_inc` freshness and optional diagnostics audit. | 2026-05-22 |
| Power BI Fabric sync | Outlook / GitHub | Resolved unless new failure appears | Latest checked `dev` runs still show successful newer run `c53d07a` after failed `920e2b9`; no new failure surfaced in Outlook. | 2026-05-21 |
| Pipeline orchestrator deploy worker | Outlook / GitHub | GitHub workflow fixed later; production covered by local deploy | Latest checked Deploy Worker runs on `main` now include a 2026-05-21 failure for `0159de4` plus the two 2026-05-19 failures. Treat as parked unless it blocks deploys. | 2026-05-22 |
| dbt reservation freshness warning | Outlook / dbt Cloud / Snowflake | Warning cleared or understood | 2026-05-25 Snowflake check shows 7 property reservation increment files still last modified on 2026-05-24 04:51-05:42 UTC while the other 10 properties have 2026-05-25 files. Stale: `czprg_palac_u_kocku`, `czprg_river_dance`, `czprg_vn17_rooftop`, `czprg_theatre_9`, `czprg_prague_residences`, `czprg_vn48_suites`, `czprg_vn3_terraces`. Likely ingestion/source landing gap, not dbt-only. | 2026-05-25 |
| Power Automate Teams pipeline alert flow | Outlook / Teams | Flow healthy before Teams pipeline notifications are trusted | 2026-05-22 Power Automate reported 1 failure for `Send webhook alerts to Data pipeline notification`; Teams connector was 429 on 2026-05-25 so channel verification was unavailable. | 2026-05-25 |
| Mews weekly delete reconciliation runtime | data-factory task note | Production rehearsal before enabling parallel workers | Read-only sandbox benchmark showed `tableWorkers=8` reducing runtime from 26.1s to 7.1s with schemas matching; row/hash compare needs same snapshot window before production enablement. | 2026-05-25 |
| Power BI Fabric sync dev failures | Outlook / GitHub | Confirm whether a newer successful run recovered `dev` | 2026-05-27 Outlook reported multiple `adrez-com/powerbi` Fabric sync failures on `dev` (`d17a27a`, `1d8ef7c`, `711ce3f`, `a86981d`, `899eda6`). GitHub could not be verified from the morning automation because `gh` had no API connectivity and connector lookup without full SHA returned 404. | 2026-05-28 |
