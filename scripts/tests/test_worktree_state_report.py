#!/usr/bin/env python3
from __future__ import annotations

import datetime
import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "scripts" / "report_worktree_state.py"


def run(*args: str | Path, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [str(arg) for arg in args],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result


class WorktreeStateReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="adrez-worktree-report-")
        self.workspace = Path(self.temp.name)
        self.origin = self.workspace / "origin.git"
        self.repo = self.workspace / "sample"
        run("git", "init", "--bare", self.origin)
        run("git", "clone", self.origin, self.repo)
        old = str(int(time.time()) - 10 * 86400)
        env = os.environ.copy()
        env.update({"GIT_AUTHOR_DATE": old, "GIT_COMMITTER_DATE": old})
        run(
            "git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
            "commit", "--allow-empty", "-m", "initial", cwd=self.repo, env=env,
        )
        run("git", "branch", "-M", "main", cwd=self.repo)
        run("git", "push", "-u", "origin", "main", cwd=self.repo)
        self.task = self.workspace / "_worktrees" / "sample" / "old-task"
        self.task.parent.mkdir(parents=True)
        run("git", "worktree", "add", self.task, "-b", "feature/old-task", "origin/main", cwd=self.repo)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def report(self) -> list[dict[str, object]]:
        output = run("python3", REPORT, self.workspace, "--json").stdout
        return json.loads(output)["worktrees"]

    def test_old_clean_merged_worktree_requires_cleanup_review(self) -> None:
        rows = self.report()
        task = next(row for row in rows if Path(str(row["path"])).resolve() == self.task.resolve())
        self.assertEqual(task["state"], "cleanup-review")
        self.assertGreaterEqual(task["age_days"], 9)
        self.assertEqual(task["remote_refs"], "local-cache-only")

    def test_dirty_worktree_is_never_cleanup_candidate(self) -> None:
        (self.task / "uncommitted.txt").write_text("keep me\n", encoding="utf-8")
        rows = self.report()
        task = next(row for row in rows if Path(str(row["path"])).resolve() == self.task.resolve())
        self.assertEqual(task["state"], "active-or-uncommitted")
        self.assertEqual(task["dirty_paths"], 1)
        self.assertTrue((self.task / "uncommitted.txt").is_file())

    def test_external_repositories_are_excluded(self) -> None:
        external = self.workspace / "commission-tier-monitoring"
        run("git", "init", external)
        repositories = {row["repository"] for row in self.report()}
        self.assertEqual(repositories, {"sample"})

    def test_summary_is_compact_and_read_only(self) -> None:
        before = run("git", "status", "--porcelain=v1", cwd=self.task).stdout
        output = run(
            "python3", REPORT, self.workspace, "--summary-only"
        ).stdout
        after = run("git", "status", "--porcelain=v1", cwd=self.task).stdout
        self.assertIn("sample\tcanonical\t1", output)
        self.assertIn("sample\tcleanup-review\t1", output)
        self.assertEqual(before, after)

    def test_top_level_linked_checkout_does_not_duplicate_repository(self) -> None:
        sibling = self.workspace / "sample-sibling"
        run(
            "git", "worktree", "add", sibling, "-b", "feature/sibling", "origin/main",
            cwd=self.repo,
        )
        rows = self.report()
        self.assertEqual({row["repository"] for row in rows}, {"sample"})
        self.assertEqual(len(rows), 3)

    def test_local_git_metadata_supplies_owner_without_dirtying_worktree(self) -> None:
        git_dir = Path(
            run("git", "rev-parse", "--absolute-git-dir", cwd=self.task).stdout.strip()
        )
        (git_dir / "codex-worktree.json").write_text(
            json.dumps(
                {
                    "owner": "codex-task:test-thread",
                    "task_ref": "DTE-999",
                    "created_at": "2026-08-12T00:00:00+00:00",
                }
            ),
            encoding="utf-8",
        )
        task = next(
            row
            for row in self.report()
            if Path(str(row["path"])).resolve() == self.task.resolve()
        )
        self.assertEqual(task["owner"], "codex-task:test-thread")
        self.assertEqual(task["task_ref"], "DTE-999")
        self.assertEqual(run("git", "status", "--porcelain=v1", cwd=self.task).stdout, "")

    def test_metadata_creation_time_overrides_old_head_commit_age(self) -> None:
        git_dir = Path(
            run("git", "rev-parse", "--absolute-git-dir", cwd=self.task).stdout.strip()
        )
        created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        (git_dir / "codex-worktree.json").write_text(
            json.dumps({"created_at": created_at}),
            encoding="utf-8",
        )
        task = next(
            row
            for row in self.report()
            if Path(str(row["path"])).resolve() == self.task.resolve()
        )
        self.assertEqual(task["age_days"], 0)
        self.assertEqual(task["age_source"], "created_at")


if __name__ == "__main__":
    unittest.main(verbosity=2)
