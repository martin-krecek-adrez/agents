#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path

from plugin_runtime import PluginRuntimeError, validate_runtime


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    parser.add_argument("--plugin-source")
    parser.add_argument("--print-root", action="store_true")
    args = parser.parse_args()
    source = Path(args.plugin_source) / "plugins" / "adrez-data-platform" if args.plugin_source else None
    state = validate_runtime(Path(args.codex_home), source_plugin_root=source)
    if args.print_root:
        print(state.root)
    else:
        print(
            f"[OK] adrez-data-platform@adrez-tech {state.version}: "
            f"installed, enabled, {len(state.skills)} cached skills"
        )


if __name__ == "__main__":
    try:
        main()
    except PluginRuntimeError as exc:
        raise SystemExit(f"ERROR: {exc}")
