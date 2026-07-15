#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path

from plugin_runtime import (
    PluginRuntimeError,
    SKILL_NAME_RE,
    discover_plugin_source,
    validate_runtime,
)


RETIRED_SKILLS = {"qmd"}


class SyncError(RuntimeError):
    pass


def lexists(path: Path) -> bool:
    return os.path.lexists(path)


def validate_regular_or_missing(path: Path, label: str) -> None:
    if not lexists(path):
        return
    if path.is_symlink() or not path.is_file():
        raise SyncError(f"{label} must be a regular file or absent: {path}")


def scan_sources(source_roots: list[Path], plugin_owned: set[str]) -> dict[str, Path]:
    managed: dict[str, Path] = {}
    for source_root in source_roots:
        if not source_root.exists():
            continue
        if source_root.is_symlink() or not source_root.is_dir():
            raise SyncError(f"Skill source root is unsafe: {source_root}")
        for skill_dir in sorted(source_root.iterdir()):
            if skill_dir.is_symlink() or not skill_dir.is_dir():
                continue
            if not (skill_dir / "SKILL.md").is_file() and not (skill_dir / "SKILL.MD").is_file():
                continue
            name = skill_dir.name
            if not SKILL_NAME_RE.fullmatch(name):
                raise SyncError(f"Invalid skill directory name: {name}")
            if name in plugin_owned:
                raise SyncError(
                    f"Plugin-owned skill exists in directly managed source: {skill_dir}"
                )
            if name in managed:
                raise SyncError(f"Duplicate directly managed skill name: {name}")
            for nested in skill_dir.rglob("*"):
                if nested.is_symlink():
                    raise SyncError(f"Direct skill source contains a symlink: {nested}")
            managed[name] = skill_dir
    return managed


def read_previous_manifest(path: Path) -> set[str]:
    validate_regular_or_missing(path, "Managed skills manifest")
    if not path.exists():
        return set()
    names = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(names) != len(set(names)):
        raise SyncError("Managed skills manifest contains duplicate names")
    invalid = [name for name in names if not SKILL_NAME_RE.fullmatch(name)]
    if invalid:
        raise SyncError(f"Managed skills manifest contains invalid names: {invalid}")
    return set(names)


def preflight_targets(
    codex_home: Path,
    skills_root: Path,
    affected_skills: set[str],
    agents_target: Path,
    manifest_path: Path,
) -> None:
    if codex_home.is_symlink() or not codex_home.is_dir():
        raise SyncError(f"CODEX_HOME must be an existing real directory: {codex_home}")
    if lexists(skills_root) and (skills_root.is_symlink() or not skills_root.is_dir()):
        raise SyncError(f"Managed skills root is unsafe: {skills_root}")
    for name in affected_skills:
        target = skills_root / name
        if lexists(target) and (target.is_symlink() or not target.is_dir()):
            raise SyncError(f"Managed skill target is a symlink or non-directory: {target}")
    if lexists(agents_target) and agents_target.is_dir() and not agents_target.is_symlink():
        raise SyncError(f"AGENTS.md target is unexpectedly a directory: {agents_target}")
    validate_regular_or_missing(manifest_path, "Managed skills manifest")


def remove_path(path: Path) -> None:
    if not lexists(path):
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        shutil.rmtree(path)


def transactional_apply(
    codex_home: Path,
    skills_root: Path,
    managed: dict[str, Path],
    affected_skills: set[str],
    agents_source: Path,
    agents_target: Path,
    manifest_path: Path,
) -> None:
    stage = Path(tempfile.mkdtemp(prefix=".managed-skills-stage-", dir=codex_home))
    backup = Path(tempfile.mkdtemp(prefix=".managed-skills-backup-", dir=codex_home))
    processed: list[tuple[Path, Path | None]] = []
    keep_backup = False
    try:
        stage_skills = stage / "skills"
        stage_skills.mkdir()
        for name, source in managed.items():
            shutil.copytree(source, stage_skills / name, symlinks=False, copy_function=shutil.copy2)
        staged_manifest = stage / "managed-skills-manifest"
        staged_manifest.write_text(
            "".join(f"{name}\n" for name in sorted(managed)), encoding="utf-8"
        )
        staged_agents = stage / "AGENTS.md"
        staged_agents.symlink_to(agents_source)

        skills_root.mkdir(parents=True, exist_ok=True)
        if skills_root.is_symlink() or not skills_root.is_dir():
            raise SyncError(f"Managed skills root changed during sync: {skills_root}")

        def replace(target: Path, replacement: Path | None, backup_name: str) -> None:
            backup_path = backup / backup_name
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            had_target = lexists(target)
            if had_target:
                os.replace(target, backup_path)
            processed.append((target, backup_path if had_target else None))
            if replacement is not None:
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(replacement, target)

        for name in sorted(affected_skills):
            replacement = stage_skills / name if name in managed else None
            replace(skills_root / name, replacement, f"skills/{name}")
        replace(agents_target, staged_agents, "AGENTS.md")
        replace(manifest_path, staged_manifest, "managed-skills-manifest")
    except Exception as original:
        try:
            for index, (target, backup_path) in enumerate(reversed(processed)):
                if lexists(target):
                    discard = stage / f"rollback-discard-{index}"
                    os.replace(target, discard)
                if backup_path is not None and lexists(backup_path):
                    target.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(backup_path, target)
        except Exception as rollback_error:
            keep_backup = True
            raise SyncError(
                f"sync failed and rollback was incomplete; backup retained at {backup}: "
                f"{rollback_error}"
            ) from original
        raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        if not keep_backup:
            shutil.rmtree(backup, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    agents_repo = script_dir.parent
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser().absolute()
    skills_root = codex_home / "skills"
    manifest_path = codex_home / ".managed-skills-manifest"
    agents_target = codex_home / "AGENTS.md"
    agents_source = Path(
        os.environ.get("ADREZ_AGENTS_MD", "/Users/martin/Documents/adrez/AGENTS.md")
    ).expanduser().resolve(strict=True)
    if not agents_source.is_file():
        raise SyncError(f"ADREZ_AGENTS_MD must resolve to a file: {agents_source}")
    personal_root = Path(
        os.environ.get("PERSONAL_SKILLS_DIR", "/Users/martin/Documents/live/agent/skills")
    ).expanduser()

    source_plugin = discover_plugin_source(agents_repo)
    runtime = validate_runtime(codex_home, source_plugin_root=source_plugin)
    plugin_owned = set(runtime.skills)
    managed = scan_sources([agents_repo / "skills", personal_root], plugin_owned)
    previous = read_previous_manifest(manifest_path)
    affected = set(managed) | previous | RETIRED_SKILLS | plugin_owned
    preflight_targets(codex_home, skills_root, affected, agents_target, manifest_path)

    if args.preflight_only:
        print(
            f"[OK] sync preflight: {len(managed)} direct skills, "
            f"{len(plugin_owned)} plugin skills, runtime {runtime.version}"
        )
        return

    transactional_apply(
        codex_home,
        skills_root,
        managed,
        affected,
        agents_source,
        agents_target,
        manifest_path,
    )
    print("Synced Codex setup:")
    print(f"- AGENTS.md -> {agents_target}")
    print(f"- directly managed skills -> {skills_root}")
    print(f"- plugin-owned skills -> {runtime.root}")


if __name__ == "__main__":
    try:
        main()
    except (PluginRuntimeError, SyncError, OSError) as exc:
        raise SystemExit(f"ERROR: {exc}")
