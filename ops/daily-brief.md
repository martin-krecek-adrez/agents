# Daily Brief

Latest Chief of Staff output goes here when a brief should persist.

## Latest

2026-05-28 09:14 CEST

- Today: Outlook Calendar má intro Michal Bukáček 10:00-10:30, krátký blok 10:30-10:45 a Lunch 11:30-12:30 Prague. Google Calendar má jen večerní osobní bloky.
- Needs Reply: Outlook ukazuje unread follow-up od Snowflake account managerky Roma Astemberg k rostoucí on-demand spotřebě; odpovědět jen pokud chceš aktivně řešit Snowflake cost/consumption. Gmail bez Adrez akčního reply signálu; většinou osobní/marketing.
- Pipeline / Watch: nové Outlook GitHub notifikace hlásí sérii `adrez-com/powerbi` Fabric sync failures na `dev` 2026-05-27; nepodařilo se ověřit recovery přes GitHub (`gh` bez API spojení, connector 404 bez full SHA). Entra sync alert z 2026-05-27 zůstává neuzavřený v paměti. Teams nelze ověřit kvůli Microsoft Graph 429.
- Open Loops: `mews-users-profile-mapping` je pořád In Progress: vložit CSV do OneDrive workbooku, počkat/spustit extractor, refreshnout externí table a dbt. `reviews-report` má prod build/smoke hotový, ale task note stále říká In Progress a next step lokální build/smoke; `mara-monitoring` je Done a čeká PR/merge. Asana API je stale, Outlook digest ukazuje jen `Dbt Cloud - dbt core OR reduce model numbers` due Jun 1.
- Suggested Priorities: 1) ověřit Power BI Fabric sync recovery/fix na `dev`, 2) dokončit Mews users workbook landing, 3) uzavřít Reviews report stav a rozhodnout `rating_public` vs `rating`, 4) připravit/follow-up Michal intro, 5) zkontrolovat Entra sync errors, pokud ovlivňují M365/Teams/webhooky.

2026-05-27 08:18 CEST

- Today: Outlook Calendar má block 10:45-11:00, AI Vibe Check 11:00-11:30, Lunch 11:30-12:45, busy 15:15-15:30, intro Raffaele Vágner 15:30-16:00 a intro Kristína Gabríková 16:30-17:00 Prague.
- Needs Reply: Outlook/Gmail bez jasného osobního reply-needed vlákna. Pozor na candidate follow-up u Raffaeleho, v poznámce omlouvá přesun původního termínu.
- Pipeline / Watch: Outlook má čerstvý Microsoft Entra Connect Sync alert pro Prague Port tenant, 2 sync errors, last export 2026-05-27 04:32 UTC. Teams Data pipeline notification a Better Stack posty z dneška se načetly bez těla; nelze z nich potvrdit stav. Outlook neukazuje nový dbt/pipeline failure od 2026-05-25; Teams search našel jen Fabric Activator trigger posty z 2026-05-25/26.
- Open Loops: včerejší dbt task `mews-users-profile-mapping` je In Progress; další krok je vložit `mews_user_profiles_by_property.csv` do OneDrive tabulky, počkat/spustit extractor a refreshnout externí table + dbt modely. Asana connector stále ukazuje stale/nekonzistentní My Tasks, ale Outlook Asana digest říká due soon: `Optimize dbt Cloud pipeline runtime` May 31 a `Dbt Cloud - dbt core OR reduce model numbers` Jun 1.
- Suggested Priorities: 1) zkontrolovat Entra sync errors a zda neblokují M365/Teams/webhooky, 2) doplnit Mews users workbook a rozjet landing/dbt refresh, 3) připravit/follow-upnout dnešní dvě candidate intra, 4) rozhodnout dbt Cloud runtime/model-count úspory před May 31/Jun 1.

2026-05-25 08:16 CEST

- Today: Outlook Calendar has Lunch 11:30-12:30 Prague, Data Analyst / Analytics Engineer intro with Anna Horakova 13:00-13:30, private busy 13:30-13:45, and Data Analyst / Analytics Engineer intro with Dominik Stehno 14:00-14:30.
- Needs Reply: no clear reply-needed Outlook/Gmail item found. Outlook unread has Asana due-soon reminder only; Gmail hits are newsletter/social/noise. Teams could not be checked due Microsoft 429.
- Pipeline / Watch: dbt Cloud Production daily run warned on 2026-05-24 with `freshness_per_property_raw_mews_reservation_inc__source_file_modified` WARN 8. Power Automate reported 1 failure for `Send webhook alerts to Data pipeline notification` on 2026-05-22. Power BI paused `Report Usage Metrics Model` scheduled refresh due inactivity. `pipeline-orchestrator` Deploy Worker failures remain parked unless GitHub deploy path matters.
- Open Loops: Mews weekly delete reconciliation now has a read-only data-factory optimization experiment showing `tableWorkers=8` cut sandbox runtime from 26.1s to 7.1s; production change still needs same-window rehearsal. Asana still shows `Snowflake/dbt L1-L2 cleanup backlog` due May 29.
- Suggested Priorities: 1) check/clear dbt reservation freshness warning and Mews `_inc` freshness, 2) prep/follow up today's two candidate intros, 3) decide whether Power Automate alert flow failure needs repair before relying on Teams pipeline notifications, 4) schedule/rehearse Mews weekly table-worker optimization.

2026-05-22 08:18 CEST

- Today: Outlook Calendar has Data Catalog - avalanche update 11:00-11:30 Prague, overlapping private Timesheets 11:15-11:30, Lunch 11:30-12:30, and Data Analyst / Analytics Engineer intro with Togi Hanilec 14:00-14:30.
- Needs Reply: no clear reply-needed Outlook/Gmail item found. Unread Outlook is candidate booking/admin plus Asana due-soon; Gmail hits are newsletter/LinkedIn noise. Teams could not be checked due Microsoft 429.
- Pipeline / Watch: 2026-05-22 dbt Cloud Production daily run warned with 5 warnings, not failed. 2026-05-21 dbt fail maps to the Mews soft-delete scope hotfix. `pipeline-orchestrator` has a newer Deploy Worker failure on `main` for `0159de4`; production still understood as covered by local deploy.
- Open Loops: Mews guard is now allowlisted to eight weekly reconciliation entities; keep `_inc` freshness and optional diagnostics audit on watch. Market-stats consolidation landed with legacy compatibility shims for commission-tier-monitoring/pricing.
- Suggested Priorities: 1) check dbt warning details and `_inc` freshness, 2) prep/follow up Togi intro and Monday candidate bookings, 3) unblock/close Asana `Snowflake/dbt L1-L2 cleanup backlog`, 4) park Deploy Worker fix unless GitHub deploy path becomes needed.

## Previous

2026-05-21 08:17 CEST

- Today: Outlook Calendar has Lunch 11:30-12:30 Prague and Data Analyst / Analytics Engineer onsite round with Tatiana Weissova 13:00-14:00, with meeting room block in the same slot.
- Needs Reply: no clear reply-needed Outlook/Teams/Gmail thread found. Unread Outlook has Asana due-soon reminder and a candidate intro notification; Gmail hits are LinkedIn/dbt marketing/social only.
- Pipeline / Watch: Teams Data pipeline notification posted 06:32 CEST but body still fetches empty. No new Outlook GitHub failure beyond known 2026-05-19 items. `powerbi` Fabric sync remains recovered by newer success; `pipeline-orchestrator` Deploy Worker still has only the two known failed runs, production covered by local deploy.
- Open Loops: Mews soft-delete guard task is in progress with compiled weekly/full+inc and daily/inc-only SQL checks; remaining follow-ups are `_inc` freshness monitoring and optional guard diagnostics audit. Extranet base input consolidation landed with follow-up on operational/log-only entities and compatibility-view deprecation.
- Suggested Priorities: 1) finish/ship Mews soft-delete guard and monitoring before next weekly run, 2) handle today's onsite interview prep/follow-up, 3) clear Asana `Snowflake/dbt L1-L2 cleanup backlog` due-today ambiguity, 4) leave GitHub workflow cleanup parked unless it blocks deploys.

2026-05-20 08:17 CEST

- Today: Outlook Calendar has AI Vibe Check 11:00-11:30, Lunch 11:30-12:30, candidate intro 12:30-13:00, short block 13:45-14:00, onsite interview/Karel 14:00-15:00 Prague.
- Needs Reply: no clear reply-needed Outlook/Teams thread found. Outlook unread has Asana due-soon notification only; recent Radana/VN48 Teams thread still ends with Martin's recovery update.
- Pipeline / Watch: `powerbi` Fabric sync failure on 2026-05-19 was followed by a successful newer `dev` run. `pipeline-orchestrator` Deploy Worker failures on `main` (`b788332`, `34de7b3`) are still failed in GitHub, but Martin deployed from local; fix GitHub workflow later. Teams Data Pipeline is fixed; Better Stack is not in this brief's action scope.
- Open Loops: Mews daily/weekly cutover PR notes say daily suppression/weekly reconciliation split is prepared; remaining risk is weekly dbt soft-delete guard, bucket guard, generalized reactivation, audit output, and dbt Cloud job-var verification.
- Suggested Priorities: 1) implement Mews weekly delete reconciliation guard before next Saturday run, 2) verify dbt Cloud Mews daily/weekly vars, 3) decide cash reconciliation business labels with Finance/Martin, 4) park GitHub workflow cleanup for `pipeline-orchestrator` until there is space.

## History

2026-05-19 10:57 CEST

- Today: Outlook Calendar ma jen Lunch 11:30-12:30 Praha.
- Needs Reply: Teams top=1 chat nasel thread Radana/VN48; posledni zprava je od Martina, bez zjevne odpovedi pro Martina. Outlook unread jsou hlavne newslettery/booking intros.
- Pipeline / Watch: VN48 Power BI je podle Teams zpet funkcni; yesterday task note potvrzuje recovery run a weekly report rebuild PASS=29 WARN=0 ERROR=0.
- Open Loops: deploynout dbt soft-delete guard/reactivation logic; vysetrit proc dbt videl incomplete full snapshot; pridat monitoring soft-delete spike; cash recon business bucket draft ceka na Finance/Martin approval.
- Suggested Priorities: 1) dokoncit/deploynout VN48/VN3 guard, 2) rozhodnout cash recon business labels, 3) spravit Asana source mapping pro Adrez projekty.

Keep only short dated summaries here. Move durable decisions to `decisions.md`.
