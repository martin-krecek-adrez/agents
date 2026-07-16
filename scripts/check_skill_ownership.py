#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path

from plugin_runtime import (
    PluginRuntimeError,
    discover_plugin_source,
    validate_plugin_root,
    validate_runtime,
)


def lexists(path: Path) -> bool:
    return os.path.lexists(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-plugin-source", action="store_true")
    parser.add_argument("--check-runtime", action="store_true")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    agents_repo = script_dir.parent
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()
    personal_root = Path(
        os.environ.get("PERSONAL_SKILLS_DIR", "/Users/martin/Documents/live/agent/skills")
    ).expanduser()

    source_root = discover_plugin_source(agents_repo)
    if args.require_plugin_source and source_root is None:
        raise PluginRuntimeError("plugin source not found; set ADREZ_TECH_PLUGINS_ROOT")
    source = validate_plugin_root(source_root) if source_root is not None else None
    runtime = (
        validate_runtime(codex_home, source_plugin_root=source_root)
        if args.check_runtime
        else None
    )
    state = source or runtime
    if state is None:
        raise PluginRuntimeError(
            "plugin inventory is unavailable; install the plugin or provide its source checkout"
        )

    failures: list[str] = []
    for name in state.skills:
        for source_dir in (agents_repo / "skills", personal_root):
            skill = source_dir / name
            if (skill / "SKILL.md").is_file() or (skill / "SKILL.MD").is_file():
                failures.append(f"plugin-owned skill duplicated in direct source: {skill}")
        if args.check_runtime and lexists(codex_home / "skills" / name):
            failures.append(f"plugin-owned skill exists in directly managed runtime: {name}")
    if failures:
        raise PluginRuntimeError("; ".join(failures))

    print(f"[OK] {len(state.skills)} plugin-owned skill names have one source of truth.")
    if source is not None:
        print(f"[OK] Plugin source: {source.root}")
    if runtime is not None:
        print(f"[OK] Plugin runtime: {runtime.root}")


if __name__ == "__main__":
    try:
        main()
    except PluginRuntimeError as exc:
        raise SystemExit(f"ERROR: {exc}")
