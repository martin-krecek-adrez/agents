#!/usr/bin/env python3
"""Read-only size checks with reviewed exceptions for exact AGENTS.md paths."""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path

from list_managed_agents import iter_managed_agents

WARN_BYTES = 8000
FAIL_BYTES = 12000


def check_sizes(workspace: Path, budgets: dict, today: date | None = None) -> list[tuple[str, str]]:
    today = today or date.today()
    findings: list[tuple[str, str]] = []
    valid_budgets: dict[str, int] = {}
    for name, entry in budgets.items():
        path = Path(name)
        try:
            if not isinstance(entry, dict):
                raise ValueError("budget must be an object")
            if path.is_absolute() or ".." in path.parts or path.name != "AGENTS.md":
                raise ValueError("must name an exact workspace-relative AGENTS.md")
            cap = entry["max_bytes"]
            if type(cap) is not int or not FAIL_BYTES < cap <= 32000:
                raise ValueError("max_bytes must be an integer between 12001 and 32000")
            if not entry.get("owner") or not entry.get("reason"):
                raise ValueError("owner and reason are required")
            reviewed = date.fromisoformat(entry["reviewed_on"])
            if reviewed > today:
                raise ValueError("review date is in the future")
            if not (workspace / path).is_file():
                raise ValueError("target file is missing")
            valid_budgets[name] = cap
            if (today - reviewed).days > 90:
                findings.append(("WARN", f"Review AGENTS size budget: {name} ({reviewed})"))
        except (KeyError, TypeError, ValueError) as exc:
            findings.append(("FAIL", f"Invalid size budget {name}: {exc}"))
    for path in iter_managed_agents(workspace):
        relative = path.relative_to(workspace.resolve()).as_posix()
        size = path.stat().st_size
        cap = valid_budgets.get(relative, FAIL_BYTES)
        if size > cap:
            findings.append(("FAIL", f"AGENTS.md exceeds {cap} bytes ({size}): {path}"))
        elif size > WARN_BYTES:
            suffix = f"; reviewed cap {cap}" if relative in valid_budgets else ""
            findings.append(("WARN", f"AGENTS.md exceeds {WARN_BYTES} bytes ({size}{suffix}): {path}"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--budgets", type=Path, default=Path(__file__).resolve().parents[1] / "ops/agents-size-budgets.json")
    args = parser.parse_args()
    try:
        budgets = json.loads(args.budgets.read_text())
        if not isinstance(budgets, dict):
            raise ValueError("size budgets must be an object")
        findings = check_sizes(args.workspace, budgets)
    except (OSError, ValueError) as exc:
        print(f"[FAIL] AGENTS size check: {exc}")
        return 1
    for level, message in findings:
        print(f"[{level}] {message}")
    return int(any(level == "FAIL" for level, _ in findings))


if __name__ == "__main__":
    raise SystemExit(main())
