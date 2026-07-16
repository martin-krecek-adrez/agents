#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from list_managed_agents import iter_managed_agents  # noqa: E402


class ManagedAgentsScopeTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
