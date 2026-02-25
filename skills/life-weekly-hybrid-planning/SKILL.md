---
name: life-weekly-hybrid-planning
description: Hybrid Trello + Google Calendar weekly planning in iterative rounds. Designed for Sunday review and next-week setup.
compatibility: Requires active Trello and Google Calendar web sessions (or API credentials).
scope: life
---

# life-weekly-hybrid-planning

Use this as the orchestration layer above:

- `life-trello-weekly-planning`
- `life-google-calendar-week-planning`

Goal: run weekly planning in small rounds and always report what remains.

## When to Use

- User wants collaborative weekly planning, not one-shot planning.
- User follows flow: close current week card, create next week card, then calendar blocks.
- User expects explicit "what is still missing" after every step.

## Required Round Contract

Every response in this workflow must contain:

- `done_now`
- `remaining`
- `user_action_needed`
- `next_round_focus`

Keep it short and concrete. No long final plan until user asks for it.

## Standard Hybrid Flow

1. `Round A - Trello close`
   - Open current week card (for example `W08`).
   - Read `Planning`, `Sunday Tasks`, and open checklist items.
   - Identify carry-over items.
2. `Round B - Trello seed`
   - Open/create next week card (for example `W09`) from template `2026 WXX`.
   - Seed `Planning` with carry-over + selected new items.
3. `Round C - Calendar skeleton`
   - Open target week in Google Calendar.
   - Protect fixed commitments first (office, commute, existing events).
4. `Round D+ - Capacity fill`
   - Add fitness blocks.
   - Add work focus/admin blocks.
   - Add personal/social blocks.
   - Add Trello execution blocks.
5. `Final round`
   - Confirm unresolved conflicts and intentionally unplanned items.
   - Return compact weekly status, not a giant dump.

## Priority Rules

- Capacity realism over ambition.
- Fixed events are immutable unless user explicitly wants changes.
- Carry-over items are not auto-scheduled; they must pass capacity fit.
- If a round exceeds scope, split it and stop.
- Calendar semantics must stay consistent:
  - `Sport & Zdraví` for gym/sport.
  - `Doprava` for commute only (`HO --> ADRZ`, `ADRZ --> HO`).
  - `Práce` for ADRZ work blocks.
  - `Důležité pro nás` for personal events where one partner acts and the other should be aware.
  - `Společné` for shared events done together.
  - `Martin` includes daily invariant `Večeře & Chill` (`19:30-20:30`) unless explicitly overridden.

## Safety

- Never delete calendar events without explicit approval.
- Never archive Trello cards/lists without explicit approval.
- For edits above 5 event/card changes in one round, summarize first, then execute.
