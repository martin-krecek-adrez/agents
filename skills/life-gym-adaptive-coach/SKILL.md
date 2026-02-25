---
name: life-gym-adaptive-coach
description: Life-only coaching workflow over Trello Gym board. Builds weekly training plan, evaluates 4-8 week trends, and proposes template updates.
compatibility: Requires Trello API access (TRELLO_API_KEY, TRELLO_API_TOKEN) and a Gym board with recurring template workouts.
scope: life
---

# life-gym-adaptive-coach

Personal coaching skill for Trello-based gym tracking.

## Goal

Turn training logs into weekly decisions:

- what to train this week,
- whether performance is going up/flat/down,
- and which template weights or volume should change.

## Board Assumptions

- Board has lists similar to: `To Do`, `Trainings`, `Finished`, `TEMPLATES`.
- Template cards exist for rotating sessions (for example heavy/light chest/back/legs variants).
- Session execution notes are stored in card `desc`.
- Due date is used as session date when available.

## Modes

Use exactly one mode per run:

1. `plan-week`
2. `review-trend`
3. `propose-template-updates`

If mode is missing, ask one short question.

## Mode: plan-week

Use on Sunday planning.

### Inputs

- week window (Monday-Sunday),
- available gym days,
- preferred split (`2+1` or `3+1`),
- constraints (travel, injury, sleep, recovery).

### Flow

1. Read recent completed sessions (last 14-21 days).
2. Select next session sequence from template rotation.
3. Respect constraints and recovery spacing.
4. Create/update planned cards for the week in `To Do`.
5. Return concise plan summary with dates and sessions.

### Output

- `week_range`
- `planned_sessions`
- `split_selected`
- `notes`

## Mode: review-trend

Compare similar sessions for last 4-8 weeks.

### Exercise Matching Rules

- Prefer exact exercise name match.
- If names differ but pattern is equivalent, map to same family (for example bench variants).
- If ambiguity is high, ask once for mapping confirmation and cache decision in the current run.

### Metrics

For each main lift/family, estimate:

- top-set load trend,
- total work estimate (sets x reps x load),
- intensity proxy from logged RPE,
- completion adherence (planned vs completed).

### Classification

- `up`: clear positive direction in load/work at similar RPE.
- `flat`: no meaningful change.
- `down`: repeated regression or missed targets.

Use practical thresholds:

- load change around +/-2.5% as minimal signal,
- require at least 2 comparable sessions before strong conclusion.

### Output

- `trend_summary` by session type (chest/back/legs),
- `exercise_highlights`,
- `confidence` (`high|medium|low`),
- `data_gaps`.

## Mode: propose-template-updates

Suggest next-template changes based on trend review.

### Decision Rules

- If `up` and RPE controlled: increase working load by ~2.5%.
- If `flat`: keep load, adjust one variable (small volume or rep target change).
- If `down` with high fatigue: reduce load 2.5-5% or deload volume.
- Never apply aggressive jumps in one step.

### Knee Injury Guardrails

- Treat legs trend separately with recovery-aware logic.
- Do not penalize long gap after injury as negative trend.
- Prefer conservative progression and optional pain-free variant swaps.

### Output

- `template_changes_proposed`
- `rationale`
- `risk_flags`
- `confirmation_needed`

Never modify template cards unless user confirms.

## Parsing Notes

- Read weights/sets/reps/RPE from free text in `desc`.
- When parsing is uncertain, include ambiguity in `data_gaps`.
- Prefer transparent assumptions over silent guessing.

## Communication Style

- Coach tone: direct, concrete, short.
- Show the decision and why.
- Keep each recommendation actionable for next session.

## Safety

- Not medical advice.
- Stop and ask user when pain/injury notes suggest escalation.
- Never delete cards or history.
