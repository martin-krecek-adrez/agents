#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path


EXCLUDED_ROOT_REPOSITORIES = frozenset({"commission-tier-monitoring"})
PRUNED_DIRECTORY_NAMES = frozenset({".git", "_worktrees", "adrez-tools", "node_modules", "old"})


def _is_plugin_template(path: Path) -> bool:
    parts = path.parts
    return (
        len(parts) >= 6
        and parts[0] == "tech-plugins"
        and parts[1] == "plugins"
        and parts[3] == "skills"
        and parts[5] == "templates"
    )


def iter_managed_agents(workspace_root: Path) -> list[Path]:
    """Return AGENTS.md files owned by the managed Adrez workspace."""
    root = workspace_root.expanduser().resolve(strict=True)
    found: list[Path] = []
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        relative = current_path.relative_to(root)
        if relative.parts and relative.parts[0] in EXCLUDED_ROOT_REPOSITORIES:
            directories.clear()
            continue
        if _is_plugin_template(relative):
            directories.clear()
            continue

        directories[:] = sorted(
            name
            for name in directories
            if name not in PRUNED_DIRECTORY_NAMES
            and not (
                not relative.parts and name in EXCLUDED_ROOT_REPOSITORIES
            )
            and not _is_plugin_template(relative / name)
        )
        if "AGENTS.md" in filenames:
            found.append(current_path / "AGENTS.md")
    return sorted(found)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_root", type=Path)
    args = parser.parse_args()
    for path in iter_managed_agents(args.workspace_root):
        print(path)


if __name__ == "__main__":
    main()
