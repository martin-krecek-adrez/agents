#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path

from plugin_runtime import SKILL_NAME_RE


class ManagedSkillError(RuntimeError):
    pass


def _skill_directories(root: Path) -> dict[str, Path]:
    if not root.exists():
        return {}
    if root.is_symlink() or not root.is_dir():
        raise ManagedSkillError(f"managed skill source must be a real directory: {root}")

    skills: dict[str, Path] = {}
    for path in sorted(root.iterdir()):
        if path.is_symlink() or not path.is_dir():
            continue
        if not (path / "SKILL.md").is_file() and not (path / "SKILL.MD").is_file():
            continue
        if not SKILL_NAME_RE.fullmatch(path.name):
            raise ManagedSkillError(f"invalid managed skill source name: {path.name}")
        skills[path.name] = path
    return skills


def _tree_digest(root: Path) -> str:
    if root.is_symlink() or not root.is_dir():
        raise ManagedSkillError(f"managed skill runtime must be a real directory: {root}")

    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ManagedSkillError(f"managed skill tree contains a symlink: {path}")
        relative = path.relative_to(root).as_posix().encode()
        if path.is_dir():
            digest.update(b"D\0" + relative + b"\0")
            continue
        if not path.is_file():
            raise ManagedSkillError(f"managed skill tree contains an unsupported entry: {path}")
        mode = stat.S_IMODE(path.stat().st_mode)
        digest.update(b"F\0" + relative + b"\0" + str(mode).encode() + b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _read_manifest(path: Path) -> set[str]:
    if path.is_symlink() or not path.is_file():
        raise ManagedSkillError(f"managed skills manifest must be a regular file: {path}")
    names = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(names) != len(set(names)):
        raise ManagedSkillError("managed skills manifest contains duplicate names")
    invalid = sorted(name for name in names if not SKILL_NAME_RE.fullmatch(name))
    if invalid:
        raise ManagedSkillError(f"managed skills manifest contains invalid names: {invalid}")
    return set(names)


def _unmanaged_adrez_runtime_issues(
    skills_root: Path, managed_names: set[str]
) -> list[str]:
    if not skills_root.exists():
        return []
    if skills_root.is_symlink() or not skills_root.is_dir():
        return [f"runtime skills root must be a real directory: {skills_root}"]

    issues: list[str] = []
    for path in sorted(skills_root.iterdir()):
        name = path.name
        if not name.startswith("adrez-") or name in managed_names:
            continue
        if path.is_symlink():
            issues.append(f"unmanaged Adrez runtime skill is a symlink: {path}")
            continue
        if not path.is_dir():
            issues.append(f"unmanaged Adrez runtime entry is not a directory: {path}")
            continue
        if (path / "SKILL.md").is_file() or (path / "SKILL.MD").is_file():
            issues.append(
                f"unmanaged Adrez runtime skill detected for {name}: runtime={path}"
            )
            continue
        issues.append(
            f"unmanaged Adrez runtime directory has no SKILL.md: {path}"
        )
    return issues


def validate_managed_runtime(
    source_roots: tuple[Path, ...], codex_home: Path
) -> tuple[str, ...]:
    sources: dict[str, Path] = {}
    for root in source_roots:
        for name, path in _skill_directories(root).items():
            if name in sources:
                raise ManagedSkillError(
                    f"duplicate directly managed skill source: {sources[name]} and {path}"
                )
            sources[name] = path

    manifest = _read_manifest(codex_home / ".managed-skills-manifest")
    source_names = set(sources)
    issues: list[str] = []
    if manifest != source_names:
        missing = sorted(source_names - manifest)
        stale = sorted(manifest - source_names)
        issues.append(
            f"managed skills manifest differs from sources: missing={missing}, stale={stale}"
        )

    for name, source in sorted(sources.items()):
        runtime = codex_home / "skills" / name
        try:
            source_digest = _tree_digest(source)
            runtime_digest = _tree_digest(runtime)
        except (ManagedSkillError, OSError) as exc:
            issues.append(str(exc))
            continue
        if source_digest != runtime_digest:
            issues.append(
                f"runtime skill drift detected for {name}: source={source}, runtime={runtime}"
            )

    issues.extend(
        _unmanaged_adrez_runtime_issues(codex_home / "skills", source_names)
    )
    if issues:
        details = "\n".join(f"- {issue}" for issue in issues)
        raise ManagedSkillError(f"managed skill runtime validation failed:\n{details}")
    return tuple(sorted(sources))


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    agents_repo = script_dir.parent
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()
    personal_root = Path(
        os.environ.get("PERSONAL_SKILLS_DIR", "/Users/martin/Documents/live/agent/skills")
    ).expanduser()
    skills = validate_managed_runtime((agents_repo / "skills", personal_root), codex_home)
    print(
        f"[OK] {len(skills)} directly managed skill(s) match source, manifest, and runtime."
    )


if __name__ == "__main__":
    try:
        main()
    except (ManagedSkillError, OSError) as exc:
        raise SystemExit(f"ERROR: {exc}")
