#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path


EXCLUDED_ROOT_REPOSITORIES = frozenset(
    {"commission-tier-monitoring", "market-overview-analysis"}
)
PRUNED_DIRECTORY_NAMES = frozenset(
    {".git", "_handoffs", "_worktrees", ".worktrees", ".sdlc-state", "_local-state",
     "adrez-tools", "node_modules", "old"}
)


# Instruction-source scope only. Do not reuse these exclusions for runtime data.
EXCLUDED_INSTRUCTION_SUBTREES = (
    ("docs", ".vitepress", "dist"),
    ("extractor-documents",),
    ("adrez-data-assistant",),
    ("adrez-metadata-sql-agent",),
    ("booking-data", "Competition_Data", "archive"),
)


def _is_excluded_instruction_subtree(path: Path) -> bool:
    return any(path.parts[:len(prefix)] == prefix
               for prefix in EXCLUDED_INSTRUCTION_SUBTREES)


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
    """Return current managed AGENTS.md sources, excluding frozen snapshots."""
    root = workspace_root.expanduser().resolve(strict=True)
    found: list[Path] = []
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        relative = current_path.relative_to(root)
        if relative.parts and relative.parts[0] in EXCLUDED_ROOT_REPOSITORIES:
            directories.clear()
            continue
        if _is_plugin_template(relative) or _is_excluded_instruction_subtree(relative):
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
            and not _is_excluded_instruction_subtree(relative / name)
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
