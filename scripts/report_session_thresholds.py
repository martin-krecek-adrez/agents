#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import datetime
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


TOOL_CALL_TYPES = {"custom_tool_call", "function_call", "local_shell_call"}


@dataclass
class SessionStats:
    session_id: str
    path: Path
    tool_calls: int = 0
    compactions: int = 0
    max_same_tool_run: int = 0
    max_same_tool_name: str = ""
    malformed_lines: int = 0
    file_count: int = 1
    tool_counts: collections.Counter[str] = field(default_factory=collections.Counter)


def parse_since(value: str) -> float:
    try:
        parsed = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid ISO timestamp: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed.timestamp()


def nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be zero or greater")
    return parsed


def inspect_session(path: Path) -> SessionStats:
    stats = SessionStats(session_id=path.stem, path=path)
    current_tool = ""
    current_run = 0

    with path.open(encoding="utf-8") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                stats.malformed_lines += 1
                continue
            if not isinstance(event, dict):
                continue
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            if event.get("type") == "session_meta":
                identifier = payload.get("session_id") or payload.get("id")
                if isinstance(identifier, str) and identifier:
                    stats.session_id = identifier
                continue
            if event.get("type") != "response_item":
                continue

            payload_type = payload.get("type")
            if payload_type == "compaction":
                stats.compactions += 1
                continue
            if payload_type not in TOOL_CALL_TYPES:
                continue

            name = payload.get("name")
            tool_name = name if isinstance(name, str) and name else str(payload_type)
            stats.tool_calls += 1
            stats.tool_counts[tool_name] += 1
            if tool_name == current_tool:
                current_run += 1
            else:
                current_tool = tool_name
                current_run = 1
            if current_run > stats.max_same_tool_run:
                stats.max_same_tool_run = current_run
                stats.max_same_tool_name = tool_name

    return stats


def discover_sessions(root: Path, since_timestamp: float) -> list[Path]:
    if not root.is_dir():
        raise FileNotFoundError(f"session root does not exist: {root}")
    return sorted(
        path
        for path in root.rglob("*.jsonl")
        if path.is_file() and path.stat().st_mtime >= since_timestamp
    )


def make_report(
    sessions: list[SessionStats],
    *,
    root: Path,
    since_timestamp: float,
    tool_call_threshold: int,
    compaction_threshold: int,
    same_tool_run_threshold: int,
) -> dict[str, Any]:
    grouped: dict[str, SessionStats] = {}
    for session in sessions:
        aggregate = grouped.get(session.session_id)
        if aggregate is None:
            aggregate = SessionStats(session_id=session.session_id, path=session.path)
            aggregate.file_count = 0
            grouped[session.session_id] = aggregate
        aggregate.tool_calls += session.tool_calls
        aggregate.compactions += session.compactions
        aggregate.malformed_lines += session.malformed_lines
        aggregate.file_count += session.file_count
        aggregate.tool_counts.update(session.tool_counts)
        if session.max_same_tool_run > aggregate.max_same_tool_run:
            aggregate.max_same_tool_run = session.max_same_tool_run
            aggregate.max_same_tool_name = session.max_same_tool_name

    breaches = []
    all_tools: collections.Counter[str] = collections.Counter()
    for session in grouped.values():
        all_tools.update(session.tool_counts)
        reasons = []
        if session.tool_calls >= tool_call_threshold:
            reasons.append("tool-calls")
        if session.compactions >= compaction_threshold:
            reasons.append("compactions")
        if session.max_same_tool_run >= same_tool_run_threshold:
            reasons.append("same-tool-run")
        if reasons:
            breaches.append(
                {
                    "session_id": session.session_id,
                    "file_count": session.file_count,
                    "tool_calls": session.tool_calls,
                    "compactions": session.compactions,
                    "max_same_tool_run": session.max_same_tool_run,
                    "max_same_tool_name": session.max_same_tool_name,
                    "reasons": reasons,
                }
            )

    breaches.sort(
        key=lambda item: (
            item["tool_calls"],
            item["compactions"],
            item["max_same_tool_run"],
        ),
        reverse=True,
    )
    return {
        "privacy": "event counts and tool names only; no prompt content or tool inputs",
        "sessions_root": str(root),
        "since": datetime.datetime.fromtimestamp(
            since_timestamp, tz=datetime.timezone.utc
        ).isoformat(),
        "thresholds": {
            "tool_calls": tool_call_threshold,
            "compactions": compaction_threshold,
            "same_tool_run": same_tool_run_threshold,
        },
        "summary": {
            "session_files": len(sessions),
            "sessions": len(grouped),
            "tool_calls": sum(session.tool_calls for session in grouped.values()),
            "compactions": sum(session.compactions for session in grouped.values()),
            "malformed_lines": sum(
                session.malformed_lines for session in grouped.values()
            ),
            "sessions_over_any_threshold": len(breaches),
        },
        "top_tools": [
            {"name": name, "count": count} for name, count in all_tools.most_common(10)
        ],
        "breaches": breaches,
    }


def print_text(report: dict[str, Any]) -> None:
    summary = report["summary"]
    thresholds = report["thresholds"]
    print("Codex session threshold report")
    print(f"Sessions root: {report['sessions_root']}")
    print(f"Since: {report['since']}")
    print(f"Privacy: {report['privacy']}")
    print(
        "Thresholds: "
        f"tool calls >= {thresholds['tool_calls']}, "
        f"compactions >= {thresholds['compactions']}, "
        f"same-tool run >= {thresholds['same_tool_run']}"
    )
    print(
        "Summary: "
        f"{summary['session_files']} session files, "
        f"{summary['sessions']} logical sessions, "
        f"{summary['tool_calls']} tool calls, "
        f"{summary['compactions']} compactions, "
        f"{summary['malformed_lines']} malformed lines, "
        f"{summary['sessions_over_any_threshold']} sessions over a threshold"
    )
    print("Top tools:")
    if report["top_tools"]:
        for item in report["top_tools"]:
            print(f"- {item['name']}: {item['count']}")
    else:
        print("- none")
    print("Threshold breaches:")
    if report["breaches"]:
        for item in report["breaches"]:
            reasons = ",".join(item["reasons"])
            print(
                f"- {item['session_id']}: tool_calls={item['tool_calls']} "
                f"compactions={item['compactions']} "
                f"max_same_tool_run={item['max_same_tool_run']} "
                f"tool={item['max_same_tool_name'] or '-'} "
                f"files={item['file_count']} reasons={reasons}"
            )
    else:
        print("- none")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Report aggregate Codex session thresholds without reporting prompt content "
            "or tool inputs. Session selection uses file modification time."
        )
    )
    parser.add_argument(
        "--sessions-root",
        type=Path,
        default=Path.home() / ".codex" / "sessions",
    )
    window = parser.add_mutually_exclusive_group()
    window.add_argument("--since", type=parse_since, help="ISO timestamp")
    window.add_argument("--days", type=nonnegative_int, default=7)
    parser.add_argument("--tool-call-threshold", type=nonnegative_int, default=500)
    parser.add_argument("--compaction-threshold", type=nonnegative_int, default=10)
    parser.add_argument("--same-tool-run-threshold", type=nonnegative_int, default=25)
    parser.add_argument("--json", action="store_true", help="print JSON")
    args = parser.parse_args()

    since_timestamp = (
        args.since if args.since is not None else time.time() - args.days * 86400
    )
    try:
        paths = discover_sessions(args.sessions_root, since_timestamp)
    except FileNotFoundError as exc:
        parser.error(str(exc))
    sessions = [inspect_session(path) for path in paths]
    report = make_report(
        sessions,
        root=args.sessions_root,
        since_timestamp=since_timestamp,
        tool_call_threshold=args.tool_call_threshold,
        compaction_threshold=args.compaction_threshold,
        same_tool_run_threshold=args.same_tool_run_threshold,
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
