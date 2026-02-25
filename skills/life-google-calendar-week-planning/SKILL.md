---
name: life-google-calendar-week-planning
description: Life-only Google Calendar workflow for turning weekly priorities into time blocks and review checkpoints.
compatibility: Requires Google Calendar access (web login or Google Calendar API credentials).
scope: life
---

# life-google-calendar-week-planning

Life skill for converting weekly priorities into practical calendar blocks.

## When to Use

- User asks to plan a personal week in Google Calendar.
- User has priorities (often from Trello) and needs concrete calendar blocks.
- User wants recurring weekly planning with less manual scheduling.

## Inputs to Confirm

- Calendar name(s) to use.
- Planning horizon (usually Monday-Sunday of one week).
- Fixed commitments to protect (meetings, family, routines).
- Preferred focus block lengths and time windows.

## Standard Flow

1. Read current week events for the target calendar.
2. Import or collect weekly priorities (manual input or Trello-derived list).
3. Propose draft blocks:
   - Deep work blocks.
   - Admin/errands blocks.
   - Buffer/recovery blocks.
   - Weekly review block.
4. Validate collisions and adjust around fixed events.
5. Ask for confirmation on the draft plan.
6. Create/update calendar events and return a summary.

## Iterative Mode (Required)

Run in multiple short rounds and pause after each pass.

Round structure:

1. Protect fixed events already in calendar (office, commute, appointments).
2. Place one category at a time:
   - fitness/gym
   - work blocks
   - personal/social blocks
   - Trello-driven tasks
3. After each category, report exact remaining gaps.

Each round must end with:

- `done_now`: blocks/events placed this round.
- `remaining_in_calendar`: missing blocks still needed.
- `user_action_needed`: only manual decisions needed from user.
- `next_round_focus`: one category for the next pass.

## Event Conventions

- Use clear prefixes (for example `Plan:`, `Focus:`, `Errands:`).
- Add source link/reference to Trello card when available.
- Keep one final weekly review block at week end.

## Calendar Mapping (Required)

Use these target calendars consistently:

- `Sport & Zdraví`: gym, mobility, other sport/health sessions.
- `Doprava`: commute blocks only.
  - Morning commute title must be exactly `HO --> ADRZ`.
  - Afternoon commute title must be exactly `ADRZ --> HO`.
- `Práce`: work blocks (`ADRZ - Office`, `ADRZ - HO`, focused work blocks).
- `Důležité pro nás`: events where either Martin or Ivet has a personal action and the other should know.
- `Společné`: events Martin and Ivet do together.

Do not place gym or commute events into `Martin` when the mapped calendar above exists.

## Daily Invariants

Apply these defaults every planning week unless the user explicitly overrides:

- `Večeře & Chill` every day, `19:30-20:30`, calendar `Martin`.

Before creating, check the current week and add only missing occurrences.

## Output Format

Return:

- `calendar_name`
- `week_range`
- `events_created`
- `events_updated`
- `conflicts_resolved`
- `planning_notes`
- `remaining_in_calendar`
- `user_action_needed`
- `next_round_focus`

## Safety

- Never delete existing events without explicit confirmation.
- For conflicting edits, prefer creating a proposal first.
- If calendar scope is unclear, ask one short clarification question.
