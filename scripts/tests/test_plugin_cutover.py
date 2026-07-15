#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SYNC = ROOT / "scripts" / "sync_codex_setup.sh"
OWNERSHIP = ROOT / "scripts" / "check_skill_ownership.sh"
sys.path.insert(0, str(ROOT / "scripts"))
import sync_codex_setup  # noqa: E402


def run(command: list[str | Path], env: dict[str, str], check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [str(item) for item in command],
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise AssertionError(f"command failed: {result.stdout}\n{result.stderr}")
    return result


class CutoverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="adrez-cutover-test-")
        self.base = Path(self.temp.name)
        self.home = self.base / "codex"
        self.home.mkdir()
        self.personal = self.base / "personal"
        self.personal.mkdir()
        self.agents = self.base / "AGENTS.md"
        self.agents.write_text("# Test bootstrap\n", encoding="utf-8")
        self.source_repo = self.base / "tech-plugins"
        self.source_plugin = self._make_plugin(self.source_repo)
        self.bin = self.base / "bin"
        self.bin.mkdir()
        self.fake_codex = self.bin / "codex"
        self._write_fake_codex(installed=True, enabled=True)
        self.env = os.environ.copy()
        self.env.update(
            {
                "CODEX_HOME": str(self.home),
                "PERSONAL_SKILLS_DIR": str(self.personal),
                "ADREZ_AGENTS_MD": str(self.agents),
                "ADREZ_TECH_PLUGINS_ROOT": str(self.source_repo),
                "PATH": f"{self.bin}{os.pathsep}{self.env['PATH']}",
            }
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _make_plugin(self, repo: Path, version: str = "0.1.0") -> Path:
        root = repo / "plugins" / "adrez-data-platform"
        (root / ".codex-plugin").mkdir(parents=True)
        (root / ".codex-plugin" / "plugin.json").write_text(
            json.dumps({"name": "adrez-data-platform", "version": version}),
            encoding="utf-8",
        )
        skills = ("plugin-alpha", "plugin-beta")
        (root / "skill-inventory.txt").write_text("\n".join(skills) + "\n", encoding="utf-8")
        for name in skills:
            skill = root / "skills" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: Test skill {name}.\n---\n",
                encoding="utf-8",
            )
        return root

    def _install_cache(self) -> Path:
        cache = (
            self.home
            / "plugins"
            / "cache"
            / "adrez-tech"
            / "adrez-data-platform"
            / "0.1.0"
        )
        shutil.copytree(self.source_plugin, cache)
        return cache

    def _write_fake_codex(self, installed: bool, enabled: bool) -> None:
        entry = {
            "pluginId": "adrez-data-platform@adrez-tech",
            "name": "adrez-data-platform",
            "marketplaceName": "adrez-tech",
            "version": "0.1.0",
            "installed": installed,
            "enabled": enabled,
        }
        payload = {"installed": [entry] if installed else [], "available": []}
        self.fake_codex.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            f"print(json.dumps({payload!r}))\n",
            encoding="utf-8",
        )
        self.fake_codex.chmod(0o755)

    def test_pluginless_sync_fails_without_mutation(self) -> None:
        self._write_fake_codex(installed=False, enabled=False)
        target_agents = self.home / "AGENTS.md"
        target_agents.write_text("original\n", encoding="utf-8")
        result = run(["bash", SYNC], self.env)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target_agents.read_text(), "original\n")
        self.assertFalse((self.home / "skills").exists())

    def test_disabled_plugin_fails_without_mutation(self) -> None:
        self._install_cache()
        self._write_fake_codex(installed=True, enabled=False)
        target_agents = self.home / "AGENTS.md"
        target_agents.write_text("original\n", encoding="utf-8")
        result = run(["bash", SYNC], self.env)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target_agents.read_text(), "original\n")
        self.assertFalse((self.home / "skills").exists())

    def test_valid_sync_removes_legacy_plugin_copy_transactionally(self) -> None:
        self._install_cache()
        legacy = self.home / "skills" / "plugin-alpha"
        legacy.mkdir(parents=True)
        (legacy / "SKILL.md").write_text("legacy\n")
        result = run(["bash", SYNC], self.env, check=True)
        self.assertEqual(result.returncode, 0)
        self.assertFalse(legacy.exists())
        self.assertTrue((self.home / "skills" / "asana" / "SKILL.md").is_file())
        manifest = (self.home / ".managed-skills-manifest").read_text().splitlines()
        self.assertIn("asana", manifest)
        self.assertNotIn("plugin-alpha", manifest)

    def test_incomplete_cache_preserves_legacy_copy(self) -> None:
        cache = self._install_cache()
        shutil.rmtree(cache / "skills" / "plugin-alpha")
        legacy = self.home / "skills" / "plugin-alpha"
        legacy.mkdir(parents=True)
        (legacy / "SKILL.md").write_text("legacy\n")
        target_agents = self.home / "AGENTS.md"
        target_agents.write_text("original\n")
        result = run(["bash", SYNC], self.env)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((legacy / "SKILL.md").is_file())
        self.assertEqual(target_agents.read_text(), "original\n")

    def test_symlink_target_is_rejected_without_external_delete(self) -> None:
        self._install_cache()
        external = self.base / "external"
        external.mkdir()
        unrelated = external / "unrelated.md"
        unrelated.write_text("preserve\n")
        skills = self.home / "skills"
        skills.mkdir()
        (skills / "asana").symlink_to(external, target_is_directory=True)
        result = run(["bash", SYNC], self.env)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(unrelated.is_file())
        self.assertFalse((external / "SKILL.md").exists())

    def test_invalid_manifest_fails_before_changes(self) -> None:
        self._install_cache()
        manifest = self.home / ".managed-skills-manifest"
        manifest.write_text("../escape\n")
        target_agents = self.home / "AGENTS.md"
        target_agents.write_text("original\n")
        result = run(["bash", SYNC], self.env)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target_agents.read_text(), "original\n")
        self.assertFalse((self.home / "skills").exists())

    def test_manifest_symlink_is_rejected_without_external_write(self) -> None:
        self._install_cache()
        external = self.base / "external-manifest"
        external.write_text("preserve\n", encoding="utf-8")
        (self.home / ".managed-skills-manifest").symlink_to(external)
        result = run(["bash", SYNC], self.env)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(external.read_text(), "preserve\n")
        self.assertFalse((self.home / "skills").exists())

    def test_runtime_check_detects_source_cache_drift(self) -> None:
        self._install_cache()
        (self.source_plugin / "skills" / "plugin-alpha" / "SKILL.md").write_text("changed\n")
        result = run(["bash", OWNERSHIP, "--check-runtime", "--require-plugin-source"], self.env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("differs from the checked-out source", result.stderr)

    def test_transaction_failure_restores_all_previous_targets(self) -> None:
        skills_root = self.home / "skills"
        old_skill = skills_root / "direct-skill"
        old_skill.mkdir(parents=True)
        (old_skill / "SKILL.md").write_text("old\n", encoding="utf-8")
        new_skill = self.base / "new-direct-skill"
        new_skill.mkdir()
        (new_skill / "SKILL.md").write_text("new\n", encoding="utf-8")
        agents_target = self.home / "AGENTS.md"
        agents_target.write_text("old agents\n", encoding="utf-8")
        manifest = self.home / ".managed-skills-manifest"
        manifest.write_text("direct-skill\n", encoding="utf-8")

        real_replace = os.replace

        def fail_new_manifest(source: str | Path, target: str | Path) -> None:
            source_path = Path(source)
            target_path = Path(target)
            if (
                target_path == manifest
                and source_path.name == "managed-skills-manifest"
                and source_path.parent.name.startswith(".managed-skills-stage-")
            ):
                raise OSError("simulated manifest install failure")
            real_replace(source, target)

        with mock.patch.object(sync_codex_setup.os, "replace", side_effect=fail_new_manifest):
            with self.assertRaises(OSError):
                sync_codex_setup.transactional_apply(
                    codex_home=self.home,
                    skills_root=skills_root,
                    managed={"direct-skill": new_skill},
                    affected_skills={"direct-skill"},
                    agents_source=self.agents,
                    agents_target=agents_target,
                    manifest_path=manifest,
                )

        self.assertEqual((old_skill / "SKILL.md").read_text(), "old\n")
        self.assertEqual(agents_target.read_text(), "old agents\n")
        self.assertEqual(manifest.read_text(), "direct-skill\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
