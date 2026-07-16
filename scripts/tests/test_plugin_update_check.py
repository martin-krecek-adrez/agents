#!/usr/bin/env python3
from __future__ import annotations

import sys
import subprocess
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from check_adrez_data_platform_update import (  # noqa: E402
    PluginRuntimeError,
    _run,
    _run_remote,
    classify_payload,
    parse_marketplace,
)


class PluginUpdateCheckTests(unittest.TestCase):
    def marketplace(self, source: str = "git@github.com:adrez-com/tech-plugins.git") -> dict:
        return {
            "marketplaces": [
                {
                    "name": "adrez-tech",
                    "root": "/tmp/adrez-tech",
                    "marketplaceSource": {
                        "sourceType": "git",
                        "source": source,
                    },
                }
            ]
        }

    def test_canonical_marketplace_is_accepted(self) -> None:
        self.assertEqual(parse_marketplace(self.marketplace()), Path("/tmp/adrez-tech"))

    def test_unexpected_remote_is_rejected(self) -> None:
        with self.assertRaisesRegex(PluginRuntimeError, "unexpected adrez-tech remote"):
            parse_marketplace(self.marketplace("https://example.invalid/plugins.git"))

    def test_new_version_is_reported_as_update(self) -> None:
        result = classify_payload("0.1.0", "old", "0.2.0", "new", "abc123")
        self.assertTrue(result.startswith("[UPDATE]"))

    def test_changed_payload_without_version_bump_is_warning(self) -> None:
        result = classify_payload("0.1.0", "old", "0.1.0", "new", "abc123")
        self.assertTrue(result.startswith("[WARN]"))

    def test_equal_payload_is_current(self) -> None:
        result = classify_payload("0.1.0", "same", "0.1.0", "same", "abc123")
        self.assertTrue(result.startswith("[OK]"))

    def test_older_remote_version_is_warning(self) -> None:
        result = classify_payload("0.2.0", "new", "0.1.0", "old", "abc123")
        self.assertTrue(result.startswith("[WARN]"))

    def test_build_metadata_only_version_change_is_warning(self) -> None:
        result = classify_payload(
            "0.1.0+installed",
            "old",
            "0.1.0+remote",
            "new",
            "abc123",
        )
        self.assertTrue(result.startswith("[WARN]"))

    @mock.patch("check_adrez_data_platform_update.subprocess.run")
    def test_run_is_noninteractive(self, run_mock: mock.Mock) -> None:
        run_mock.return_value = subprocess.CompletedProcess(["git"], 0, "", "")
        _run(["git", "status"])
        kwargs = run_mock.call_args.kwargs
        self.assertIs(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(kwargs["env"]["GIT_TERMINAL_PROMPT"], "0")
        self.assertIn("BatchMode=yes", kwargs["env"]["GIT_SSH_COMMAND"])
        self.assertIn("StrictHostKeyChecking=yes", kwargs["env"]["GIT_SSH_COMMAND"])

    @mock.patch("check_adrez_data_platform_update._run")
    def test_remote_timeout_is_warning(self, run_mock: mock.Mock) -> None:
        run_mock.side_effect = subprocess.TimeoutExpired(["git", "ls-remote"], 30)
        result, warning = _run_remote(["git", "ls-remote"], "remote check")
        self.assertIsNone(result)
        self.assertTrue(warning.startswith("[WARN] remote check timed out"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
