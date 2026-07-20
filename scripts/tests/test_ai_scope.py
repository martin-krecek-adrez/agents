#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from list_managed_agents import iter_managed_agents  # noqa: E402


class ManagedAgentsScopeTests(unittest.TestCase):
    def test_active_ops_do_not_route_external_repository(self) -> None:
        for path in sorted((ROOT / "ops").glob("*.md")):
            self.assertNotIn(
                "commission-tier-monitoring",
                path.read_text(encoding="utf-8"),
                str(path),
            )

    def test_external_and_generated_repositories_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory(prefix="adrez-agents-scope-") as temp:
            workspace = Path(temp).resolve()
            included = [workspace / "AGENTS.md", workspace / "owned-repo" / "AGENTS.md"]
            excluded = [
                workspace / "commission-tier-monitoring" / "AGENTS.md",
                workspace / "old" / "AGENTS.md",
                workspace / "_worktrees" / "repo" / "task" / "AGENTS.md",
                workspace
                / "tech-plugins"
                / "plugins"
                / "sample"
                / "skills"
                / "sample"
                / "templates"
                / "AGENTS.md",
            ]
            for path in included + excluded:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# test\n", encoding="utf-8")

            self.assertEqual(iter_managed_agents(workspace), sorted(included))

    def test_task_note_report_prunes_external_repository(self) -> None:
        with tempfile.TemporaryDirectory(prefix="adrez-task-note-scope-") as temp:
            workspace = Path(temp).resolve()
            included = workspace / "owned-repo" / "docs" / "tasks" / "included.md"
            excluded = (
                workspace
                / "commission-tier-monitoring"
                / "docs"
                / "tasks"
                / "excluded.md"
            )
            sibling_checkout = (
                workspace
                / "dbt-cloud-mews-l1-append"
                / "docs"
                / "tasks"
                / "duplicate.md"
            )
            for path in (included, excluded, sibling_checkout):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("canonical workflow\n", encoding="utf-8")
                old = time.time() - 40 * 24 * 60 * 60
                os.utime(path, (old, old))

            result = subprocess.run(
                [
                    str(ROOT / "scripts" / "report_task_note_promotion_candidates.sh"),
                    str(workspace),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(included), result.stdout)
            self.assertNotIn("commission-tier-monitoring", result.stdout)
            self.assertNotIn(str(excluded), result.stdout)
            self.assertNotIn(str(sibling_checkout), result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
