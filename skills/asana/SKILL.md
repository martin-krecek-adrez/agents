---
name: asana
description: Legacy Adrez Asana archive/context workflow. Use only for existing Asana URLs/GIDs, unfinished old Asana tasks that should not be migrated yet, historical context lookup, or concise comments/updates on existing legacy tasks. Do not create new Asana tasks or subtasks; use Linear for all new Adrez task planning/tracking.
scope: business
status: active
owner: martin
last_reviewed: 2026-06-15
---

# Asana Task Skill

## When to use
- User provides an existing Asana task URL/GID.
- User asks to read legacy task context from Asana.
- User asks to recover historical context from Asana.
- User asks to comment on or update an existing legacy Asana task from this Codex thread.
- User asks to connect an existing Asana task with repo task notes.

## Boundary
- Asana is dead for new Adrez tasks.
- Do not create new Asana tasks or subtasks.
- Use this skill only for existing legacy Asana work that should not be migrated yet, unfinished old Asana tasks, comments/updates on existing Asana tasks, or historical Asana context lookup.
- Use `adrez-linear-workflow` for all new Adrez projects/issues/tasks.

## Required inputs
- **Task identifier**: Asana task URL or task GID for read/update/comment actions.
- **Update payload**: fields to update on an existing legacy task (for example notes, assignee, due date, completed).
- **Comment body**: short summary of work completed in this Codex thread for an existing legacy task.

## Auth
- Use a personal access token in env var `ASANA_TOKEN`.
- Do not paste tokens into chat. If missing, ask the user to provide it via env var.

## Workflow
1) Resolve task reference:
   - Parse task GID from URL, or use given GID directly.
2) Read hierarchy as needed:
   - Parent task details: `GET /tasks/{task_gid}`.
   - Direct subtasks: `GET /tasks/{task_gid}/subtasks`.
   - Parent from subtask: inspect `parent` in `GET /tasks/{subtask_gid}`.
   - If user asks for nested tree, recurse through `/subtasks` until leaf nodes.
3) Update existing records as needed:
   - `PUT /tasks/{task_gid}` for fields (`name`, `notes`, `assignee`, `due_on`, `start_on`, `completed`).
4) Post execution notes:
   - `POST /tasks/{task_gid}/stories` with concise bullet summary.
5) For substantial technical work, align with AGENTS task memory:
   - In the relevant repo, create or update `docs/tasks/YYYY-MM-DD-short-task-name.md`.
   - Cross-link Asana task URL in the note, and post the note path back to Asana.

## API Examples
### Read task and direct subtasks
```bash
TASK_GID=1234567890
curl -sS -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/tasks/${TASK_GID}?opt_fields=gid,name,parent.gid,parent.name,permalink_url,num_subtasks"

curl -sS -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/tasks/${TASK_GID}/subtasks?opt_fields=gid,name,completed,assignee.name,due_on,parent.gid,parent.name,permalink_url"
```

### Update task description (notes)
```bash
TASK_GID=1234567890
curl -sS -X PUT \
  -H "Authorization: Bearer $ASANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data":{"notes":"Updated context from Codex thread."}}' \
  "https://app.asana.com/api/1.0/tasks/${TASK_GID}"
```

### Post concise progress comment
```bash
TASK_GID=1234567890
curl -sS -X POST \
  -H "Authorization: Bearer $ASANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data":{"text":"- Summary line 1\n- Summary line 2"}}' \
  "https://app.asana.com/api/1.0/tasks/${TASK_GID}/stories"
```

## Guardrails
- Keep comments short and actionable (4-8 lines).
- Do not include secrets.
- Do not create new Asana tasks or subtasks. Use Linear for new Adrez work.
- Use `opt_fields` to keep responses compact and deterministic.
- If user asks to attach files, ask how to access the file and use Asana attachments API.
- Do not assume recursion depth; traverse until no subtasks remain when user asks for full hierarchy.
