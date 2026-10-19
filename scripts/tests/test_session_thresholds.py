#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from report_session_thresholds import discover_sessions, inspect_session, make_report  # noqa: E402


class SessionThresholdReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="session-threshold-test-")
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_session(self, name: str, events: list[dict], *, mtime: float) -> Path:
        path = self.root / f"{name}.jsonl"
        path.write_text(
            "".join(json.dumps(event) + "\n" for event in events),
            encoding="utf-8",
        )
        os.utime(path, (mtime, mtime))
        return path

    def test_report_counts_only_metadata_and_thresholds(self) -> None:
        now = time.time()
        events = [
            {
                "type": "session_meta",
                "payload": {
                    "id": "rollout-safe",
                    "session_id": "session-safe",
                    "base_instructions": "secret prompt",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call",
                    "name": "exec",
                    "input": "secret tool input",
                },
            },
            {
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call",
                    "name": "exec",
                    "input": "another secret",
                },
            },
            {"type": "response_item", "payload": {"type": "compaction"}},
        ]
        path = self.write_session("current", events, mtime=now)
        stats = inspect_session(path)
        report = make_report(
            [stats],
            root=self.root,
            since_timestamp=now - 60,
            tool_call_threshold=2,
            compaction_threshold=1,
            same_tool_run_threshold=2,
        )

        self.assertEqual(stats.session_id, "session-safe")
        self.assertEqual(stats.tool_calls, 2)
        self.assertEqual(stats.compactions, 1)
        self.assertEqual(stats.max_same_tool_run, 2)
        self.assertEqual(report["breaches"][0]["reasons"], [
            "tool-calls",
            "compactions",
            "same-tool-run",
        ])
        rendered = json.dumps(report)
        self.assertNotIn("secret prompt", rendered)
        self.assertNotIn("secret tool input", rendered)

    def test_report_aggregates_rollout_files_by_session_id(self) -> None:
        now = time.time()
        paths = []
        for name in ("rollout-one", "rollout-two"):
            paths.append(
                self.write_session(
                    name,
                    [
                        {
                            "type": "session_meta",
                            "payload": {"id": name, "session_id": "shared-session"},
                        },
                        {
                            "type": "response_item",
                            "payload": {"type": "compaction"},
                        },
                    ],
                    mtime=now,
                )
            )
        report = make_report(
            [inspect_session(path) for path in paths],
            root=self.root,
            since_timestamp=now - 60,
            tool_call_threshold=99,
            compaction_threshold=2,
            same_tool_run_threshold=99,
        )

        self.assertEqual(report["summary"]["session_files"], 2)
        self.assertEqual(report["summary"]["sessions"], 1)
        self.assertEqual(report["breaches"][0]["session_id"], "shared-session")
        self.assertEqual(report["breaches"][0]["file_count"], 2)

    def test_discovery_uses_modification_time(self) -> None:
        now = time.time()
        current = self.write_session("current", [], mtime=now)
        self.write_session("old", [], mtime=now - 10_000)

        self.assertEqual(discover_sessions(self.root, now - 60), [current])

    def test_malformed_lines_are_reported_without_failure(self) -> None:
        path = self.root / "broken.jsonl"
        path.write_text(
            "not-json\n"
            + json.dumps(
                {
                    "type": "response_item",
                    "payload": {"type": "function_call", "name": "lookup"},
                }
            )
            + "\n",
            encoding="utf-8",
        )

        stats = inspect_session(path)

        self.assertEqual(stats.malformed_lines, 1)
        self.assertEqual(stats.tool_calls, 1)


if __name__ == "__main__":
    unittest.main()
