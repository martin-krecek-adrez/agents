---
date: 2026-07-01
area: metadata
severity: P2
source: user
status: inbox
related_task:
sensitive_data_checked: yes
promote_to:
  - deterministic-check
  - linear
---

# Avalanche Prague Booking Partnership All Null

## Trigger
User reported that `BOOKING_PARTNERSHIP` in Avalanche is entirely `NULL` for
Prague: 3,708 affected rows.

## Failure Mode
Avalanche exposes or relies on a field that appears populated enough to query,
but for the Prague slice it returns no usable values. This can mislead analysis,
entity discovery, or generated SQL by making the attribute look valid while the
local segment is effectively empty.

## Working Resolution
Verified in Snowflake. `BOOKING_PARTNERSHIP` comes from
`L2_BASE.BASE_OUTPUT.V_SCRAPING_BOOKING_HOTEL`, through
`L2_BASE.BASE.BOOKING_SCRAPE_HOTEL` and
`L2_BASE.BASE_INPUT_SCRAPING_BOOKING.SCRAPING_BOOKING_HOTEL_CORE`.

The source data is present: raw Booking `Property.preferredValue` has enum
values `NONE`, `PREFERRED`, and `PREFERRED_PLUS`. The dbt expression currently
uses `booking_variant_to_boolean(get_path(raw_entity_data, 'preferredValue'))`,
which only handles boolean-ish values and numeric `0`/`1`. It therefore maps all
three enum values to `NULL`.

For the exact Prague slice exposed by `V_SCRAPING_BOOKING_HOTEL`:
- 3,708 hotels total.
- 953 should map to `true` (`PREFERRED` or `PREFERRED_PLUS`).
- 2,755 should map to `false` (`NONE`).
- 0 should remain `NULL`.

## Suggested Harness Change
Add or promote a deterministic metadata/data-quality check for Avalanche-exposed
fields that flags segment-level all-null dimensions for important markets such
as Prague. The check should report the field, source relation, segment filter,
row count, and whether the field should be hidden, documented as sparse, or fixed
upstream.

Model fix candidate: map Booking preferred enum values explicitly. Either keep
`booking_partnership` as boolean with `PREFERRED`/`PREFERRED_PLUS` = true and
`NONE` = false, or add a separate tier field if preserving `PREFERRED_PLUS`
matters analytically.

## Promotion Criteria
Promote to Linear if verification confirms that `BOOKING_PARTNERSHIP` is expected
to be meaningful for Prague, or if another market/field shows the same
all-null-by-segment pattern.

## Notes
No raw row samples or customer data included. Reported aggregate: Prague has
3,708 rows with `BOOKING_PARTNERSHIP` entirely `NULL`.

Snowflake verification also showed the full production view has 409,035 rows and
0 non-null `BOOKING_PARTNERSHIP` values, so this is not Prague-specific.
