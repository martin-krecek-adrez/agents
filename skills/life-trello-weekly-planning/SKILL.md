---
name: life-trello-weekly-planning
description: Life-only Trello workflow for weekly planning: review previous week, close completed tasks, and prepare a new weekly board/card structure.
compatibility: Requires Trello access (web login or API key/token) and an existing weekly template card/list structure.
scope: life
---

# life-trello-weekly-planning

Life skill for personal weekly planning in Trello.

## When to Use

- User asks to run or assist personal weekly planning in Trello.
- User wants to review last week and prepare a new week plan card.
- User wants repetitive weekly Trello updates reduced to a standard flow.

## Inputs to Confirm

- Board name (or URL).
- Source template card/list used for a new week.
- Week label convention (for example `2026-W08`).
- Definition of done for moving/checking off items.

## Standard Flow

1. Open target board and find the previous week card(s).
2. Review checklist items and card states:
   - Mark completed items done.
   - Move unfinished items to carry-over section/list.
3. Create the new week card from template or duplicate last week structure.
4. Rename card using agreed week naming convention.
5. Seed the new card with:
   - Top priorities for the week.
   - Carry-over items from previous week.
   - Optional quick wins / backlog picks.
6. Return a short summary:
   - Done count.
   - Carry-over count.
   - New week card URL.

## Iterative Mode (Required)

Run in short rounds. Do not do everything at once.

For each round, return exactly:

- `done_now`: what was completed in this round.
- `remaining_in_trello`: concrete checklist items/cards still open.
- `user_action_needed`: only actions the user must do manually.
- `next_round_focus`: one narrow next step.

Use this style especially for Sunday flow:

1. Close current week card (`W08`) and identify incomplete items.
2. Create/open next week card (`W09`) from template.
3. Seed `Planning` with carry-over and candidate items.
4. Stop and report what is still missing before calendar blocking.

## Execution Options

Use one of these approaches:

- Trello API approach (preferred for deterministic automation).
- Browser automation approach via Playwright when API setup is not ready.

## Output Format

Return:

- `previous_week_card`
- `new_week_card`
- `completed_items_count`
- `carry_over_items_count`
- `notes`
- `remaining_in_trello`
- `user_action_needed`
- `next_round_focus`

## Safety

- Never archive or delete cards/lists without explicit confirmation.
- Never move cards across boards unless the user asked for it.
- Ask before bulk edits affecting more than one weekly card.
