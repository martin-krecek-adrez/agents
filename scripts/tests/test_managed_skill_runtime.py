#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from check_managed_skill_runtime import (  # noqa: E402
    ManagedSkillError,
    validate_managed_runtime,
)


class ManagedSkillRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="managed-skill-runtime-")
        self.root = Path(self.temp.name)
        self.business = self.root / "business"
        self.personal = self.root / "personal"
        self.codex = self.root / "codex"
        self.business.mkdir()
        self.personal.mkdir()
        (self.codex / "skills").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def add_skill(self, source: Path, name: str, text: str = "# skill\n") -> None:
        skill = source / name
        skill.mkdir()
        (skill / "SKILL.md").write_text(text, encoding="utf-8")
        shutil.copytree(skill, self.codex / "skills" / name)

    def write_manifest(self, *names: str) -> None:
        (self.codex / ".managed-skills-manifest").write_text(
            "".join(f"{name}\n" for name in names), encoding="utf-8"
        )

    def test_all_source_roots_match_runtime(self) -> None:
        self.add_skill(self.business, "business-skill")
        self.add_skill(self.personal, "life-skill")
        self.write_manifest("business-skill", "life-skill")
        self.assertEqual(
            validate_managed_runtime((self.business, self.personal), self.codex),
            ("business-skill", "life-skill"),
        )

    def test_personal_runtime_drift_is_detected(self) -> None:
        self.add_skill(self.personal, "life-skill")
        self.write_manifest("life-skill")
        (self.codex / "skills" / "life-skill" / "SKILL.md").write_text(
            "changed\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(ManagedSkillError, "life-skill"):
            validate_managed_runtime((self.business, self.personal), self.codex)

    def test_multiple_runtime_drifts_are_reported_together(self) -> None:
        self.add_skill(self.business, "business-skill")
        self.add_skill(self.personal, "life-skill")
        self.write_manifest("business-skill", "life-skill")
        for name in ("business-skill", "life-skill"):
            (self.codex / "skills" / name / "SKILL.md").write_text(
                "changed\n", encoding="utf-8"
            )

        with self.assertRaises(ManagedSkillError) as raised:
            validate_managed_runtime((self.business, self.personal), self.codex)
        message = str(raised.exception)
        self.assertIn("runtime skill drift detected for business-skill", message)
        self.assertIn("runtime skill drift detected for life-skill", message)

    def test_manifest_mismatch_and_runtime_drift_are_reported_together(self) -> None:
        self.add_skill(self.business, "business-skill")
        self.write_manifest("stale-skill")
        (self.codex / "skills" / "business-skill" / "SKILL.md").write_text(
            "changed\n", encoding="utf-8"
        )

        with self.assertRaises(ManagedSkillError) as raised:
            validate_managed_runtime((self.business, self.personal), self.codex)
        message = str(raised.exception)
        self.assertIn("managed skills manifest differs from sources", message)
        self.assertIn("runtime skill drift detected for business-skill", message)

    def test_unmanaged_adrez_runtime_skill_is_detected(self) -> None:
        self.write_manifest()
        unmanaged = self.codex / "skills" / "adrez-thread-orchestration"
        unmanaged.mkdir()
        (unmanaged / "SKILL.md").write_text("# unmanaged\n", encoding="utf-8")

        with self.assertRaisesRegex(
            ManagedSkillError, "unmanaged Adrez runtime skill detected"
        ):
            validate_managed_runtime((self.business, self.personal), self.codex)

    def test_unmanaged_non_adrez_runtime_skill_is_ignored(self) -> None:
        self.write_manifest()
        unmanaged = self.codex / "skills" / "unrelated-skill"
        unmanaged.mkdir()
        (unmanaged / "SKILL.md").write_text("# unmanaged\n", encoding="utf-8")

        self.assertEqual(
            validate_managed_runtime((self.business, self.personal), self.codex), ()
        )

    def test_unmanaged_adrez_runtime_symlink_is_rejected(self) -> None:
        self.write_manifest()
        target = self.root / "external-skill"
        target.mkdir()
        (target / "SKILL.md").write_text("# external\n", encoding="utf-8")
        (self.codex / "skills" / "adrez-external").symlink_to(target)

        with self.assertRaisesRegex(
            ManagedSkillError, "unmanaged Adrez runtime skill is a symlink"
        ):
            validate_managed_runtime((self.business, self.personal), self.codex)

    def test_unmanaged_adrez_runtime_file_is_rejected(self) -> None:
        self.write_manifest()
        (self.codex / "skills" / "adrez-broken").write_text(
            "not a directory\n", encoding="utf-8"
        )

        with self.assertRaisesRegex(
            ManagedSkillError, "unmanaged Adrez runtime entry is not a directory"
        ):
            validate_managed_runtime((self.business, self.personal), self.codex)

    def test_managed_adrez_runtime_skill_passes(self) -> None:
        self.add_skill(self.business, "adrez-thread-orchestration")
        self.write_manifest("adrez-thread-orchestration")

        self.assertEqual(
            validate_managed_runtime((self.business, self.personal), self.codex),
            ("adrez-thread-orchestration",),
        )

    def test_duplicate_source_name_is_detected(self) -> None:
        self.add_skill(self.business, "duplicate")
        duplicate = self.personal / "duplicate"
        duplicate.mkdir()
        (duplicate / "SKILL.md").write_text("# duplicate\n", encoding="utf-8")
        self.write_manifest("duplicate")
        with self.assertRaisesRegex(ManagedSkillError, "duplicate directly managed"):
            validate_managed_runtime((self.business, self.personal), self.codex)

    def test_stale_manifest_name_is_detected(self) -> None:
        self.add_skill(self.business, "business-skill")
        self.write_manifest("business-skill", "removed-skill")
        with self.assertRaisesRegex(ManagedSkillError, r"stale=\['removed-skill'\]"):
            validate_managed_runtime((self.business, self.personal), self.codex)

    def test_invalid_source_name_is_detected(self) -> None:
        self.add_skill(self.business, "invalid skill")
        self.write_manifest("invalid skill")
        with self.assertRaisesRegex(ManagedSkillError, "invalid managed skill source name"):
            validate_managed_runtime((self.business, self.personal), self.codex)

    def test_invalid_manifest_name_is_detected(self) -> None:
        self.write_manifest("invalid skill")
        with self.assertRaisesRegex(ManagedSkillError, "manifest contains invalid names"):
            validate_managed_runtime((self.business, self.personal), self.codex)


if __name__ == "__main__":
    unittest.main(verbosity=2)
