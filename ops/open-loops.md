# Open Loops

Cross-repo and personal operating loops that should survive between Codex
threads.

## Status Semantics

- `Open`: actionable and can be considered for today's priorities.
- `Waiting`: real context, but do not rank as a priority unless a fresh source
  asks Martin to act.
- `Done`: do not surface except as brief closure context for one day, then leave
  out unless reopened.
- `Parked`: real but intentionally not for today's brief unless explicitly
  triggered.

## Active

| Status | Item | Source | Next Step | Updated |
| --- | --- | --- | --- | --- |
| Open | Adrez Chief of Staff pilot | Codex thread | Harden source order and signal ranking. | 2026-05-19 |
| Open | Teams connector chat pagination | Morning brief feedback | Use `top=1` chat listing and incremental retries; avoid broad chat list calls. | 2026-05-19 |
| Open | Asana source quality | Morning brief feedback | Identify correct Adrez project/task surfaces; current search misses due-soon task from Outlook Asana email. | 2026-05-19 |
| Open | Yesterday work synthesis | Morning brief feedback | Load recent `docs/tasks` notes before priorities. | 2026-05-19 |
| Open | Mews weekly delete reconciliation guard | Local task brief / repo notes | Finish guard rollout; add `_inc` freshness monitoring and consider diagnostics audit after weekly pattern settles. | 2026-05-21 |
| Open | Pipeline orchestrator GitHub deploy workflow | Outlook / gh / Martin correction | Latest Deploy Worker run on `main` also failed on 2026-05-21 for `0159de4`; production is still understood as covered by local deploy, so fix when capacity allows unless deploys start depending on GitHub. | 2026-05-22 |
| Done | Mews ingestor coverage proposal | Martin correction | Proposal/update sent to Michal and data is available; do not keep surfacing as today's priority. | 2026-06-01 |
| Waiting | Reviews report handoff | Martin correction / dbt task note | Martin will continue, but is waiting for feedback before next push; keep `rating_public` vs `rating` decision visible only if feedback touches scoring. | 2026-06-04 |
| Done | Tools invoices for billing | Martin correction | Invoices are done; future improvement is an automation because the current manual process is repetitive. | 2026-06-12 |
| Open | CFO dynamic report demo | Martin correction | Prepare/show CFO demo of the dynamic report. | 2026-06-01 |
| Waiting | Avalanche rollout prep | Martin correction | Shown to everyone on 2026-06-03; wait for feedback, no active push unless someone responds. | 2026-06-04 |
| Open | Finance Reconciliation Program 2026 | Outlook / Teams / Martin correction | This is Martin's main work today; Cash recon is his active focus on 2026-07-01. | 2026-07-01 |
| Waiting | Rev Management booking-window heatmap prod deploy | Outlook GitHub notification / Martin correction | Code is in `main`; only a trivial prod deploy remains, so do not rank as development blocker. | 2026-06-12 |
| Done | Booking room layout Avalanche metadata | Martin correction | Done as of 2026-06-03; do not keep surfacing as approval blocker. | 2026-06-03 |
| Open | HR windows | Martin correction | One HR window already happened and another is still coming; keep candidate follow-up light but visible. | 2026-06-01 |
| Done | CH9 01 Mews data export | Outlook / Pavla Šípová / Martin correction | Martin confirmed done on 2026-06-09; do not surface unless Pavla reopens it. | 2026-06-09 |
| Done | Snowflake Trust Center scanner charges | Outlook / Snowflake Support | Support approved an 8-credit goodwill adjustment and closed the case; only scanner on/off policy remains if charges should not recur. | 2026-06-11 |
| Open | PPR occupancy/report repair | dbt task notes / Martin correction | Martin is handling this separately; report broke, so do not treat as a simple rollout recommendation. | 2026-06-12 |
| Open | Mews Adyen migration / payout reconciliation | Outlook / Martin correction | Martin asked Mews whether Adyen payout amounts can be reconstructed from API settlement data; he is watching responses. 2026-06-20 account-verification deadline is Mews KYB/compliance from original migration email. | 2026-06-16 |
| Open | Bank statements Snowflake automation | Teams / Jiří Dufek / Martin correction | Martin told Jiří he will automate bank statements into Snowflake/storage and analyze completeness/linkability; this is Martin's main work today. | 2026-06-16 |
| Open | Benchmark answer packet ingestion changes | Linear SWE-252 / Hapl | Hapl will test after Martin implements the ingestion changes. | 2026-06-18 |
| Open | Expedia payout/remittance Snowflake exposure | Linear DTE-55 / Hapl | Three new `expedia_*` payout/remittance tables now land in ADLS; register entities in `data-factory`, add dbt views/tests, and preserve `payment_reference_number` as the cash-recon join key. | 2026-06-29 |
| Open | Booking Search Results Score catalog coverage | Linear DTE-82 / Hapl / Martin correction | SRS cleanup task note is done; Martin will handle remaining extranet/catalog follow-up today. | 2026-07-01 |

## Parking Lot

Items that are real but not actionable today.
