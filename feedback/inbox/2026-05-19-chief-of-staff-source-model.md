---
date: 2026-05-19
area: prompts
severity: P1
source: user
status: inbox
related_task:
sensitive_data_checked: yes
promote_to:
  - skill
  - shared AGENTS.md
---

# Chief Of Staff Source Model Failed

## Trigger
Morning brief used Gmail and Google Calendar for a work-only Adrez Chief of
Staff workflow, missed Asana and recent repo task notes, and told Martin to
manually check Teams monitoring.

## Failure Mode
The brief treated unavailable or slow connector calls as a reason to punt work
back to the user. It also relied on the wrong personal sources and did not
reconstruct yesterday's actual work from repo `docs/tasks` notes.

## Working Resolution
Use Outlook Calendar, Outlook Email, Teams, Asana, and recent repo task notes as
the default source graph. Teams broad chat listing can timeout, but `top=1`
chat listing and direct fetch worked. Outlook Email plugin needed to be
installed. Asana connector worked, but current search did not find the due-soon
task referenced by the Outlook Asana notification.

## Suggested Harness Change
Create a dedicated Chief of Staff runbook/skill that always:
- Loads local ops memory and automation memory first.
- Loads yesterday/recent `*/docs/tasks/YYYY-MM-DD-*.md` notes.
- Queries Outlook Calendar and Outlook Email.
- Queries Teams incrementally, starting with small pages and retrying narrow
  paths before declaring a gap.
- Queries Asana assigned, due-soon, recently completed, and project status.
- Uses GitHub/CI only when triggered by the above.
- Avoids "check manually" unless the exact failed connector/tool is named.

## Promotion Criteria
Promote immediately if the automation runs again, because this is the core
workflow contract for the brief.

## Notes
Do not include Gmail or Google Calendar in the default work brief.
