---
name: snowflake-analysis-playbook
description: In-progress analytical workflow for broad/ad-hoc Snowflake investigations with mandatory scope clarification before querying.
compatibility: Requires Snowflake access (prefer via `snowcli`) and should be used with fully qualified object names.
status: in_progress
---

# snowflake-analysis-playbook

This is an in-progress skill. Use it to avoid vague analysis and force a structured approach.

## Core rule
If user request is broad or ambiguous, ask clarifying questions before analysis.

## Mandatory clarification (ask first when needed)
1. Scope:
   - Which database/schema/table(s)?
2. Time window:
   - Exact date range?
3. Grain:
   - row-level, reservation-level, payment-level, daily, monthly?
4. Filters:
   - property/entity/channel/OTA subset?
5. Output expectation:
   - count, sum, delta, mapping rate, anomaly list?

## Modes
### 1) quick-check
- Single table/schema sanity and KPI.
- Output:
  - one primary query
  - one validation query
  - one short interpretation

### 2) deep-dive
- Cross-table root-cause analysis.
- Output:
  - baseline query (coverage/null/date range)
  - main join query
  - exception query
  - interpretation + caveats

### 3) recon
- Reconciliation/control style analysis.
- Output:
  - expected vs observed query
  - unmatched bucket query
  - confidence/limitations

## Query/output contract
Always return:
1. Executable SQL (fully qualified names).
2. Numerical result summary.
3. Interpretation.
4. Confidence/limitations.
5. Next best drill-down query (optional).

## Default starting points (Adrez)
- Finance analysis: `L3_PRODUCT.FINANCE.FINANCE_FLAT_V2`
- Reconciliation: `L3_PRODUCT.FINANCE.*recon*` models
- Raw/base checks: `L1_RAW.*`, `L2_BASE.*`

## Evolution log (update from real cases)
- 2026-02-11: skill scaffold created; enforce pre-query scope clarification for broad asks.
- TODO: add reusable query snippets from 5-10 real finance cases.

## Maintenance behavior
- At end of substantial analyses, ask:
  - "Should I append this case to the skill evolution log/template snippets?"
- Do not auto-edit the skill unless user confirms.
