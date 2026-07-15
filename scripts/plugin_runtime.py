#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


PLUGIN_NAME = "adrez-data-platform"
MARKETPLACE_NAME = "adrez-tech"
PLUGIN_ID = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"
INVENTORY_NAME = "skill-inventory.txt"
SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
VERSION_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)


class PluginRuntimeError(RuntimeError):
    pass


@dataclass(frozen=True)
class PluginState:
    root: Path
    version: str
    skills: tuple[str, ...]
    digest: str


def _regular_file(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise PluginRuntimeError(f"{label} must be a regular file: {path}")


def read_inventory(plugin_root: Path) -> tuple[str, ...]:
    inventory_path = plugin_root / INVENTORY_NAME
    _regular_file(inventory_path, "Plugin skill inventory")
    names = tuple(
        line.strip()
        for line in inventory_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    if not names:
        raise PluginRuntimeError(f"Plugin skill inventory is empty: {inventory_path}")
    if names != tuple(sorted(set(names))):
        raise PluginRuntimeError("Plugin skill inventory must be sorted and unique")
    invalid = [name for name in names if not SKILL_NAME_RE.fullmatch(name)]
    if invalid:
        raise PluginRuntimeError(f"Invalid plugin-owned skill names: {invalid}")
    return names


def _payload_digest(plugin_root: Path, skills: tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    paths = [
        plugin_root / INVENTORY_NAME,
        plugin_root / ".codex-plugin" / "plugin.json",
    ]
    for skill in skills:
        paths.extend(
            path
            for path in sorted((plugin_root / "skills" / skill).rglob("*"))
            if path.is_file() or path.is_symlink()
        )
    for path in paths:
        if path.is_symlink() or not path.is_file():
            raise PluginRuntimeError(f"Plugin payload contains a symlink or missing file: {path}")
        relative = path.relative_to(plugin_root).as_posix().encode()
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
        digest.update(b"x" if os.access(path, os.X_OK) else b"-")
    return digest.hexdigest()


def validate_plugin_root(plugin_root: Path, expected_version: str | None = None) -> PluginState:
    plugin_root = plugin_root.expanduser().absolute()
    if plugin_root.is_symlink() or not plugin_root.is_dir():
        raise PluginRuntimeError(f"Plugin root is missing or unsafe: {plugin_root}")
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    _regular_file(manifest_path, "Codex plugin manifest")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PluginRuntimeError(f"Invalid plugin manifest JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise PluginRuntimeError(f"Plugin manifest must be a JSON object: {manifest_path}")
    if manifest.get("name") != PLUGIN_NAME:
        raise PluginRuntimeError(f"Unexpected plugin name in {manifest_path}")
    version = manifest.get("version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise PluginRuntimeError(f"Invalid plugin version in {manifest_path}: {version!r}")
    if expected_version is not None and version != expected_version:
        raise PluginRuntimeError(
            f"Plugin cache version mismatch: CLI={expected_version}, manifest={version}"
        )

    skills = read_inventory(plugin_root)
    skills_root = plugin_root / "skills"
    if skills_root.is_symlink() or not skills_root.is_dir():
        raise PluginRuntimeError(f"Plugin skills root is missing or unsafe: {skills_root}")
    actual = tuple(
        sorted(
            path.name
            for path in skills_root.iterdir()
            if path.is_dir() and not path.is_symlink() and (path / "SKILL.md").is_file()
        )
    )
    if actual != skills:
        raise PluginRuntimeError(
            f"Plugin cache inventory mismatch: expected={skills}, actual={actual}"
        )
    for name in skills:
        _regular_file(skills_root / name / "SKILL.md", f"Skill {name}")
    return PluginState(
        root=plugin_root,
        version=version,
        skills=skills,
        digest=_payload_digest(plugin_root, skills),
    )


def validate_runtime(codex_home: Path, source_plugin_root: Path | None = None) -> PluginState:
    codex_home = codex_home.expanduser().absolute()
    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home)
    try:
        result = subprocess.run(
            ["codex", "plugin", "list", "--json"],
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except FileNotFoundError as exc:
        raise PluginRuntimeError("codex is not available on PATH") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise PluginRuntimeError(f"codex plugin list failed: {detail}") from exc
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise PluginRuntimeError(f"codex plugin list returned invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise PluginRuntimeError("codex plugin list must return a JSON object")

    matches = [
        item
        for item in data.get("installed", [])
        if isinstance(item, dict) and item.get("pluginId") == PLUGIN_ID
    ]
    if len(matches) != 1:
        raise PluginRuntimeError(f"{PLUGIN_ID} is not installed exactly once")
    entry = matches[0]
    if entry.get("installed") is not True or entry.get("enabled") is not True:
        raise PluginRuntimeError(f"{PLUGIN_ID} is not installed and enabled")
    version = entry.get("version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise PluginRuntimeError(f"{PLUGIN_ID} has an invalid installed version: {version!r}")

    cache_root = (
        codex_home
        / "plugins"
        / "cache"
        / MARKETPLACE_NAME
        / PLUGIN_NAME
        / version
    )
    runtime = validate_plugin_root(cache_root, expected_version=version)
    if source_plugin_root is not None:
        source = validate_plugin_root(source_plugin_root)
        if source.version != runtime.version:
            raise PluginRuntimeError(
                f"Installed plugin version {runtime.version} differs from source {source.version}"
            )
        if source.skills != runtime.skills or source.digest != runtime.digest:
            raise PluginRuntimeError("Installed plugin cache differs from the checked-out source")
    return runtime


def _git_worktrees(repo: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "worktree", "list", "--porcelain"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError:
        return []
    return [
        Path(line.removeprefix("worktree "))
        for line in result.stdout.splitlines()
        if line.startswith("worktree ")
    ]


def discover_plugin_source(agents_repo: Path) -> Path | None:
    explicit = os.environ.get("ADREZ_TECH_PLUGINS_ROOT")
    if explicit:
        repo = Path(explicit).expanduser().absolute()
        root = repo / "plugins" / PLUGIN_NAME
        if not (root / INVENTORY_NAME).is_file():
            raise PluginRuntimeError(f"Explicit plugin source is invalid: {repo}")
        return root

    workspaces: list[Path] = []
    for worktree in _git_worktrees(agents_repo) or [agents_repo]:
        parts = worktree.parts
        if "_worktrees" in parts:
            index = parts.index("_worktrees")
            workspace = Path(*parts[:index])
        else:
            workspace = worktree.parent
        if workspace not in workspaces:
            workspaces.append(workspace)

    candidates: list[Path] = []
    for workspace in workspaces:
        tech_main = workspace / "tech-plugins"
        candidates.append(tech_main)
        for worktree in _git_worktrees(tech_main):
            candidates.append(worktree)
        candidates.append(workspace / "_worktrees" / "tech-plugins" / PLUGIN_NAME)

    for repo in candidates:
        root = repo / "plugins" / PLUGIN_NAME
        if (root / INVENTORY_NAME).is_file():
            return root
    return None
