---
name: asana
description: Manage Asana tasks from Codex (read hierarchy, create/update tasks and subtasks, and post concise status comments).
scope: business
status: active
owner: martin
last_reviewed: 2026-03-26
---

# Asana Task Skill

## When to use
- User asks to read task context from Asana.
- User asks to comment on a task from this Codex thread.
- User asks to create or update a task/subtask.
- User asks to connect Asana execution tracking with repo task notes.

## Required inputs
- **Task identifier**: Asana task URL or task GID for read/update/comment actions.
- **Create payload** (for new task/subtask): at minimum title + parent/project destination.
- **Update payload**: fields to update (for example notes, assignee, due date, completed).
- **Comment body**: short summary of work completed in this Codex thread.

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
3) Create records as needed:
   - New task: `POST /tasks` with workspace/project.
   - New subtask under parent task: `POST /tasks/{parent_gid}/subtasks`.
4) Update records as needed:
   - `PUT /tasks/{task_gid}` for fields (`name`, `notes`, `assignee`, `due_on`, `start_on`, `completed`).
5) Post execution notes:
   - `POST /tasks/{task_gid}/stories` with concise bullet summary.
6) For substantial technical work, align with AGENTS task memory:
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

### Create subtask under a parent task
```bash
PARENT_GID=1234567890
curl -sS -X POST \
  -H "Authorization: Bearer $ASANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data":{"name":"POS merchant statements","notes":"Scope and validation details go here."}}' \
  "https://app.asana.com/api/1.0/tasks/${PARENT_GID}/subtasks"
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
- Confirm destination before creating new top-level tasks (workspace/project/section).
- Use `opt_fields` to keep responses compact and deterministic.
- If user asks to attach files, ask how to access the file and use Asana attachments API.
- Do not assume recursion depth; traverse until no subtasks remain when user asks for full hierarchy.
