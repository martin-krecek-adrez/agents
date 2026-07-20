---
name: asana
description: Historical Adrez Asana archive lookup. Use only when Martin explicitly provides a legacy Asana URL/GID, asks for historical context, or requests a final archival comment/update on a named legacy task. Never scan Asana as an active queue; use Linear for all active Adrez work.
scope: business
status: active
owner: martin
last_reviewed: 2026-07-15
---

# Asana Task Skill

## When to use
- User provides an existing Asana task URL/GID.
- User asks to read legacy task context from Asana.
- User asks to recover historical context from Asana.
- User explicitly asks for a final archival comment/update on a named legacy task.
- User asks to connect an existing Asana task with repo task notes.

## Boundary
- Asana is retired as an active Adrez work system.
- Do not create tasks/subtasks, reopen work, scan assigned tasks, or use Asana
  in routine briefs.
- Use this skill only for explicit historical lookup or a user-requested final
  archival update on a named legacy task.
- If historical context reveals active work, first find any owning Linear issue.
  Propose migration when none exists; create or update Linear only when Martin
  authorizes tracking. Never reactivate the Asana task.

## Required inputs
- **Task identifier**: Asana task URL or task GID for read/update/comment actions.
- **Archival completion request**: explicit Martin approval to set an existing
  legacy task to `completed=true`.
- **Comment body**: short archival summary for an existing legacy task, posted
  only when Martin explicitly requests it.

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
3) Complete an existing legacy record only when explicitly requested:
   - `PUT /tasks/{task_gid}` with only `{"completed":true}`.
4) Post an archival note only when explicitly requested:
   - `POST /tasks/{task_gid}/stories` with a concise final summary.
5) For substantial technical work, align with AGENTS task memory:
   - In the relevant repo, create or update `docs/tasks/YYYY-MM-DD-short-task-name.md`.
   - Preserve the Asana task URL in the note as historical provenance.
   - Post the note path back to Asana only when Martin explicitly requested an
     archival update on that task.

## API Examples
### Read task and direct subtasks
```bash
TASK_GID=1234567890
curl -sS -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/tasks/${TASK_GID}?opt_fields=gid,name,parent.gid,parent.name,permalink_url,num_subtasks"

curl -sS -H "Authorization: Bearer $ASANA_TOKEN" \
  "https://app.asana.com/api/1.0/tasks/${TASK_GID}/subtasks?opt_fields=gid,name,completed,assignee.name,due_on,parent.gid,parent.name,permalink_url"
```

### Mark a named legacy task completed
```bash
TASK_GID=1234567890
curl -sS -X PUT \
  -H "Authorization: Bearer $ASANA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data":{"completed":true}}' \
  "https://app.asana.com/api/1.0/tasks/${TASK_GID}"
```

### Post concise archival comment
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
- Never change assignee, title, due/start dates, notes, or set
  `completed=false`; Asana writes are limited to an explicitly requested
  archival comment or `completed=true`.
- Use `opt_fields` to keep responses compact and deterministic.
- Do not assume recursion depth; traverse until no subtasks remain when user asks for full hierarchy.
