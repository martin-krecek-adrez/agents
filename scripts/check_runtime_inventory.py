#!/usr/bin/env python3
"""Validate the local operating map. This never calls or changes live services."""
from __future__ import annotations

import argparse
import ast
from datetime import date
import json
from pathlib import Path
import re

from list_managed_agents import EXCLUDED_ROOT_REPOSITORIES, PRUNED_DIRECTORY_NAMES

FIELDS = ("id", "repository", "runtime", "trigger", "outputs", "health_check", "owner", "reviewed_on")


def has_scheduled_workflow(text: str, dag_id: str, workflow_name: str) -> bool:
    """Check a direct Workflow operator inside the named scheduled DAG block."""
    tree = ast.parse(text)
    constants = {node.targets[0].id: node.value.value for node in tree.body
                 if isinstance(node, ast.Assign) and len(node.targets) == 1
                 and isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Constant)}

    def name(node: ast.AST) -> str | None:
        return node.id if isinstance(node, ast.Name) else None

    def literal(node: ast.AST | None):
        if isinstance(node, ast.Constant):
            return node.value
        return constants.get(node.id) if isinstance(node, ast.Name) else None

    for block in ast.walk(tree):
        if not isinstance(block, ast.With):
            continue
        for item in block.items:
            call = item.context_expr
            if not isinstance(call, ast.Call) or name(call.func) != "DAG":
                continue
            keywords = {entry.arg: entry.value for entry in call.keywords}
            schedule = keywords.get("schedule")
            if literal(keywords.get("dag_id")) != dag_id or not isinstance(schedule, ast.Call) or name(schedule.func) != "CronTriggerTimetable":
                continue
            for statement in block.body:
                operator = getattr(statement, "value", None)
                if isinstance(operator, ast.Call) and name(operator.func) == "CloudflareWorkflowOperator":
                    args = {entry.arg: entry.value for entry in operator.keywords}
                    if literal(args.get("workflow_name")) == workflow_name:
                        return True
    return False


def source_path(workspace: Path, name: str) -> Path:
    path = Path(name)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError("source must be workspace-relative without parent traversal")
    if path.parts[0] in EXCLUDED_ROOT_REPOSITORIES or set(path.parts) & PRUNED_DIRECTORY_NAMES:
        raise ValueError("source is outside managed scope")
    candidate = workspace / path
    if any(parent.is_symlink() for parent in (candidate, *candidate.parents) if parent != workspace.parent):
        raise ValueError("source must not traverse symlinks")
    if not candidate.is_file():
        raise ValueError("source file is missing")
    return candidate


def validate_inventory(workspace: Path, payload: dict, today: date | None = None) -> list[tuple[str, str]]:
    today = today or date.today()
    findings: list[tuple[str, str]] = []
    if payload.get("version") != 1 or not isinstance(payload.get("components"), list) or not payload["components"]:
        return [("FAIL", "Runtime inventory requires version 1 and a nonempty components list")]
    seen: set[str] = set()
    for item in payload["components"]:
        if not isinstance(item, dict):
            findings.append(("FAIL", "Runtime component must be an object"))
            continue
        identity = item.get("id", "<missing>")
        missing = [field for field in FIELDS if not isinstance(item.get(field), str) or not item[field].strip()]
        if missing:
            findings.append(("FAIL", f"{identity}: missing fields {missing}"))
            continue
        if identity in seen:
            findings.append(("FAIL", f"Duplicate runtime component: {identity}"))
        seen.add(identity)
        try:
            reviewed = date.fromisoformat(item["reviewed_on"])
            if reviewed > today:
                raise ValueError("review date is in the future")
            if (today - reviewed).days > 90:
                findings.append(("WARN", f"{identity}: review operating map (last reviewed {reviewed})"))
        except ValueError as exc:
            findings.append(("FAIL", f"{identity}: {exc}"))
        refs = item.get("source_refs")
        if not isinstance(refs, list) or not refs:
            findings.append(("FAIL", f"{identity}: source_refs must be nonempty"))
            continue
        for reference in refs:
            try:
                path = source_path(workspace, reference["path"])
                patterns = reference.get("required_patterns", [])
                if not isinstance(patterns, list) or not patterns or not all(isinstance(p, str) and p for p in patterns):
                    raise ValueError("each source needs nonempty required_patterns")
                text = path.read_text(encoding="utf-8")
                for pattern in patterns:
                    if not re.search(pattern, text, re.MULTILINE):
                        findings.append(("FAIL", f"{identity}: source contract changed: {reference['path']} / {pattern}"))
                contract = reference.get("airflow_workflow")
                if contract is not None and not has_scheduled_workflow(text, contract["dag_id"], contract["workflow_name"]):
                    findings.append(("FAIL", f"{identity}: scheduled DAG no longer directly owns the Workflow: {reference['path']}"))
            except (OSError, KeyError, TypeError, ValueError, SyntaxError, re.error) as exc:
                findings.append(("FAIL", f"{identity}: invalid source reference {reference!r}: {exc}"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--inventory", type=Path, default=Path(__file__).resolve().parents[1] / "ops/runtime-inventory.json")
    parser.add_argument("--overview", action="store_true", help="Print the operating map as Markdown")
    args = parser.parse_args()
    try:
        payload = json.loads(args.inventory.read_text())
        if not isinstance(payload, dict):
            raise ValueError("inventory must be an object")
        findings = validate_inventory(args.workspace.resolve(), payload)
    except (OSError, ValueError) as exc:
        print(f"[FAIL] Runtime inventory: {exc}")
        return 1
    for level, message in findings:
        print(f"[{level}] {message}")
    if any(level == "FAIL" for level, _ in findings):
        return 1
    print(f"[OK] {len(payload['components'])} operating-map entries have valid source files and declared anchors; live health and deployed configuration are not checked.")
    if args.overview:
        print("\n| Component | Runs on | Trigger | Output | Read-only health check |\n|---|---|---|---|---|")
        for item in payload["components"]:
            print("| " + " | ".join(item[k].replace("|", "/").replace("\n", " ") for k in ("id", "runtime", "trigger", "outputs", "health_check")) + " |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
