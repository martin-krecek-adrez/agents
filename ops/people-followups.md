# People Follow-Ups

People or threads that likely need a reply, decision, or gentle nudge.

## Surfacing Rules

A person/thread belongs in `Needs Reply` only when Martin likely needs to reply,
decide, or nudge today. If Martin is handling it separately, or the latest
message is from Martin without a clear ask, keep it as context but do not rank
it.

## Active

| Person / Thread | Channel | Why It Matters | Suggested Next Step | Updated |
| --- | --- | --- | --- | --- |
| Dominik Filip / Snowflake read credentials | Teams chat | Martin už se zeptal, co/kam/na co přesně potřebuje; risk je bezpečnost i zbytečně široký přístup. | Počkat na upřesnění a nabídnout scoped role/user nebo sdílený read-only view. | 2026-06-08 |
| Jiří Dufek / XML bank statements | Teams / Outlook / Martin correction | XML výpisy budou prospektivně, historicky prý banka neumí; ČSOB emailová distribuce výpisů je stále nejistá. | Martin to testuje sám bokem; nesurfacingovat jako follow-up pro Codex, pokud se znovu neotevře. | 2026-06-12 |
| Martin Hapl / candidate email wording | Teams chat | Upozornil, že dovolenou raději nepsat kandidátům emailem; je to spíš procesní připomínka pro další intra. | U dnešních candidate follow-upů držet email stručný a citlivé HR detaily řešit ústně. | 2026-06-05 |
| Mews / Adyen migration | Outlook / Martin correction | Hapl přidal Martina jako ownera změny; Martin poslal technické otázky k settlement identifierům, payout rekonstrukci a bank-statement identifikaci. | Martin hlídá Mews odpovědi; nesurfacingovat jako Codex reply-needed, jen jako watch. | 2026-06-16 |
| Martin Hapl / SWE-252 benchmark answer packet | Linear / Outlook notification | Hapl čeká na Martinovy ingestion changes, než otestuje benchmark ask-packet answers. | Posunout ingestion změny nebo mu napsat krátký ETA/status. | 2026-06-18 |

## Resolved

- 2026-06-11: Snowflake Support / Threat Intelligence scanner charges: support approved 8-credit goodwill adjustment and closed case; only internal decision remains whether to disable Threat Intelligence scanner.
- 2026-06-19: Michal Bukáček / Snowflake URL: Martin poslal Snowflake URL v Teams 2026-06-18 14:28 CEST; do not surface as reply-needed unless Michal reopens access trouble.
- 2026-06-12: Michal Bukáček / nabídka spolupráce: kandidát nabídku přijal a Martin informoval Tech team; bez dalšího reply-needed signálu v briefu.
- 2026-06-09: Daniel Tomschi / bank movements currency: Martin likely answered; Dan's latest Teams reply was only "Dík", so do not surface as waiting for Martin unless reopened.
- 2026-06-09: Pavla Šípová / CH9 01 Mews data export confirmed done by Martin; do not surface unless reopened.
- 2026-06-03: Martin Hapl Teams `Takhle?` is being handled in person; Martin will send Michal an offer.
- 2026-06-05: Martin Hapl room-source data follow-up handled; Martin answered with `V_SCRAPING_BOOKING_ROOM_LAYOUT`, then refactored Booking layout grain and dbt prod build passed.

## Reply Rules

- Draft concise replies when there is enough context.
- Ask before sending.
- Prefer "what changed / current state / next step" over long explanations.
