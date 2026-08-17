# Data Engineering Linear portfolio

Use this reference when creating, updating, or reorganizing Data Engineering
projects and issues. Verify the live Linear structure before a bulk change.

## Initiatives and projects

| Initiative | Projects |
|---|---|
| `Finance` | `Cash Reconciliation`, `Executive Reporting` |
| `Revenue` | `Revenue Analytics (Market)`, `Revenue Management Reporting` |
| `Expansion` | `Expansion Analytics` |
| `Avalanche` | `Avalanche` |
| `Data Platform` | `Platform Infrastructure & Operations`, `Data Orchestration`, `Data Ingestion`, `Snowflake & dbt`, `Analytics Delivery Platform`, `Adrez Intelligence Hub`, `Business Metrics & Definitions` |

Keep these projects without an initiative until the business portfolio changes:

- `Support Analytics App`
- `Customers Analytics`
- `Reviews Report`
- `Guest Experience Journey`

Do not route new work to the removed `Call Recordings Transcription Pipeline`
project. Route new IPEX acquisition to `Data Ingestion`. Route governed
journey modeling to `Guest Experience Journey`.

## Project routing

### Finance

- `Cash Reconciliation`: bank, CSOB, payment-provider statements, payment
  matching, reconciliation rules, finance controls, and the Cash Recon app.
- `Executive Reporting`: CEO/CFO/top-line reporting, leadership KPI views,
  executive exports, stakeholder validation, and adoption.

### Revenue

- `Revenue Analytics (Market)`: competitor and market data, Lighthouse
  replacement, rates, parity, comp sets, external demand, pricing signals, and
  the `revenue.adrez.com` market product.
- `Revenue Management Reporting`: internal property performance, pickup,
  forecast, channel mix, stay-date strategy, and revenue-management reporting.

### Expansion

- `Expansion Analytics`: city, location, competitor, cohort, investment, and
  expansion decision analytics.

### Avalanche

- `Avalanche`: Avalanche MCP behavior, business-facing AI analytics, governed
  catalog coverage, metadata delivery for Avalanche, and entity rollout.
- Do not place `Adrez Intelligence Hub` or company metric governance here.

### Data Platform

- `Platform Infrastructure & Operations`: VPS/Azure hosting, deployment,
  platform access, secrets, monitoring, alerting, backup, recovery, and runtime
  operations.
- `Data Orchestration`: Airflow, dbt execution runtime, DAG dependencies,
  scheduling, orchestration releases, lifecycle, recovery, and retirement of
  legacy orchestrators.
- `Data Ingestion`: source acquisition, ingestors and extractors, ADLS/lake
  landing, data-factory exposure, cursors, overlap, replay, deduplication,
  reconciliation, and source-level freshness.
- `Snowflake & dbt`: shared Snowflake access and lifecycle, reusable dbt
  patterns, incremental processing, SCD2/history, shared schemas, and
  cross-domain model contracts.
- `Analytics Delivery Platform`: shared analytics-app contract, UI conventions,
  serving/export architecture, Cloudflare deployment and access, refresh,
  CI/CD, and application migrations.
- `Adrez Intelligence Hub`: the business-facing landing page, application
  catalog, access-aware discovery, business guidance, backoffice entry, and
  adoption. Keep it in Data Platform for now.
- `Business Metrics & Definitions`: shared company definitions for revenue,
  occupancy, ADR, RevPAR, entity identifiers, and cross-report metric
  contracts. Keep it in Data Platform for now.

### Projects without an initiative

- `Support Analytics App`: Support Analytics product work and the future
  Data-team ownership of `email-analytics`. Put mailbox, Runnr, and IPEX source
  acquisition in `Data Ingestion`.
- `Customers Analytics`: customer, guest, and stay analytics specific to the
  Customers product.
- `Reviews Report`: review score, channel/property performance, taxonomy,
  clustering, and review-report product work.
- `Guest Experience Journey`: governed stay journey, communication evidence,
  review attribution, service recovery, and active-stay experience workflows.

## Boundary rules

1. Route by the primary outcome, not by the repository changed.
2. Keep business-specific models in the business project. Put only reusable or
   cross-domain Snowflake/dbt capabilities in `Snowflake & dbt`.
3. Put source acquisition in `Data Ingestion`, even when the downstream product
   is Support, Revenue, Finance, or Expansion.
4. Put pipeline scheduling and execution behavior in `Data Orchestration`.
5. Put shared app delivery mechanisms in `Analytics Delivery Platform`; keep
   application-specific content in its product project.
6. Use issue relations for cross-project dependencies. Do not create a generic
   catch-all project.
7. Search before creating a project. Create a new project only for a durable
   workstream with repeated future work and a distinct owner or roadmap.
