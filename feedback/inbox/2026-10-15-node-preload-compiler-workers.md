---
date: 2026-10-15
area: tooling
severity: P3
source: failed-run
status: inbox
related_task: DTE-81
sensitive_data_checked: yes
promote_to:
  - local profiling helper
---

# Limit a profiling preload to the intended Node process

## Trigger
A local Cube timing preload opened a fixed output file with exclusive creation.
Cube compiler workers inherited NODE_OPTIONS and ran the preload again.
Compilation failed because the output file already existed.

## Failure Mode
Syntax and wrapper unit checks did not exercise the worker startup lifecycle.
Automatic container removal also discarded the first startup log.

## Working Resolution
Instrument only the primary container process and the main Node thread.
The local helper checks process.pid === 1 and worker_threads.isMainThread.
Keep a failed owned container long enough to read its logs, then remove it.
The corrected runtime reached READY and recorded all three intended stages.

## Suggested Harness Change
For container entry-point profiling, guard inherited preload execution before
opening output files or importing the instrumented framework. Use a process
identity appropriate for the actual launcher. Verify one real application startup.
Do not use a PID 1 condition for host processes or other launch arrangements.

## Promotion Criteria
Add the guard to a reusable profiling helper if this local approach is adopted.
No shared skill or AGENTS.md change is required for this first occurrence.

## Notes
Both failed local containers were removed. No production workflow failed.
The timing wrapper measures parent-side wall time, including worker waits.
It does not measure worker CPU separately.
