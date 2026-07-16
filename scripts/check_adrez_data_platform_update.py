#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from plugin_runtime import PluginRuntimeError, validate_plugin_root, validate_runtime


MARKETPLACE = "adrez-tech"
PLUGIN = "adrez-data-platform"
REMOTE = "git@github.com:adrez-com/tech-plugins.git"
REF = "refs/heads/main"
NETWORK_TIMEOUT_SECONDS = 30
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$"
)


def _run(
    command: list[str],
    *,
    check: bool = True,
    timeout: Optional[int] = None,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    environment["GIT_SSH_COMMAND"] = (
        "ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10"
    )
    return subprocess.run(
        command,
        text=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
        timeout=timeout,
        env=environment,
    )


def _failure_reason(result: subprocess.CompletedProcess[str]) -> str:
    lines = [line.strip() for line in result.stderr.splitlines() if line.strip()]
    return lines[0] if lines else "unknown error"


def _run_remote(
    command: list[str], label: str
) -> Tuple[Optional[subprocess.CompletedProcess[str]], Optional[str]]:
    try:
        result = _run(
            command,
            check=False,
            timeout=NETWORK_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return None, f"[WARN] {label} timed out after {NETWORK_TIMEOUT_SECONDS}s"
    if result.returncode != 0:
        return None, f"[WARN] {label} unavailable: {_failure_reason(result)}"
    return result, None


def _semver_precedence(version: str) -> tuple:
    match = SEMVER_RE.fullmatch(version)
    if not match:
        raise PluginRuntimeError(f"invalid semantic version: {version!r}")
    major, minor, patch = (int(match.group(index)) for index in range(1, 4))
    prerelease = match.group(4)
    if prerelease is None:
        return major, minor, patch, 1, ()
    identifiers = tuple(
        (0, int(item)) if item.isdigit() else (1, item)
        for item in prerelease.split(".")
    )
    return major, minor, patch, 0, identifiers


def parse_marketplace(payload: object) -> Path:
    if not isinstance(payload, dict) or not isinstance(payload.get("marketplaces"), list):
        raise PluginRuntimeError("codex marketplace list returned an invalid payload")
    matches = [
        item
        for item in payload["marketplaces"]
        if isinstance(item, dict) and item.get("name") == MARKETPLACE
    ]
    if len(matches) != 1:
        raise PluginRuntimeError(f"{MARKETPLACE} marketplace is not configured exactly once")
    item = matches[0]
    source = item.get("marketplaceSource")
    if not isinstance(source, dict) or source.get("sourceType") != "git":
        raise PluginRuntimeError(f"{MARKETPLACE} is not a Git marketplace")
    if source.get("source") != REMOTE:
        raise PluginRuntimeError(
            f"unexpected {MARKETPLACE} remote: {source.get('source')!r}"
        )
    root = item.get("root")
    if not isinstance(root, str) or not root:
        raise PluginRuntimeError(f"{MARKETPLACE} marketplace root is missing")
    return Path(root).expanduser()


def classify_payload(
    installed_version: str,
    installed_digest: str,
    remote_version: str,
    remote_digest: str,
    remote_sha: str,
) -> str:
    if remote_version != installed_version:
        remote_precedence = _semver_precedence(remote_version)
        installed_precedence = _semver_precedence(installed_version)
        if remote_precedence > installed_precedence:
            return (
                f"[UPDATE] installed={installed_version} remote={remote_version} "
                f"sha={remote_sha}"
            )
        return (
            f"[WARN] remote version is not newer: installed={installed_version} "
            f"remote={remote_version} sha={remote_sha}"
        )
    if remote_digest != installed_digest:
        return (
            f"[WARN] remote payload changed without version bump: "
            f"version={remote_version} sha={remote_sha}"
        )
    return f"[OK] installed plugin payload is current: version={installed_version}"


def main() -> None:
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()
    listing = _run(["codex", "plugin", "marketplace", "list", "--json"])
    try:
        marketplace_root = parse_marketplace(json.loads(listing.stdout))
    except json.JSONDecodeError as exc:
        raise PluginRuntimeError(f"codex marketplace list returned invalid JSON: {exc}") from exc

    snapshot_plugin = marketplace_root / "plugins" / PLUGIN
    installed = validate_runtime(codex_home, source_plugin_root=snapshot_plugin)
    snapshot_sha = _run(
        ["git", "-C", str(marketplace_root), "rev-parse", "HEAD"]
    ).stdout.strip()

    remote_result, warning = _run_remote(
        ["git", "ls-remote", REMOTE, REF],
        "remote marketplace freshness",
    )
    if warning:
        print(warning)
        return
    assert remote_result is not None
    fields = remote_result.stdout.split()
    if len(fields) != 2 or fields[1] != REF:
        raise PluginRuntimeError("git ls-remote returned an unexpected main ref")
    remote_sha = fields[0]
    if remote_sha == snapshot_sha:
        print(
            f"[OK] marketplace snapshot is current: version={installed.version} "
            f"sha={remote_sha}"
        )
        return

    with tempfile.TemporaryDirectory(prefix="adrez-plugin-update-check-") as temp:
        checkout = Path(temp) / "tech-plugins"
        clone, warning = _run_remote(
            [
                "git",
                "clone",
                "--quiet",
                "--depth",
                "1",
                "--branch",
                "main",
                REMOTE,
                str(checkout),
            ],
            "remote marketplace payload",
        )
        if warning:
            print(warning)
            return
        assert clone is not None
        cloned_sha = _run(["git", "-C", str(checkout), "rev-parse", "HEAD"]).stdout.strip()
        if cloned_sha != remote_sha:
            print(
                "[WARN] remote main moved during update check: "
                f"observed={remote_sha} cloned={cloned_sha}"
            )
            return
        remote = validate_plugin_root(checkout / "plugins" / PLUGIN)

    print(
        classify_payload(
            installed.version,
            installed.digest,
            remote.version,
            remote.digest,
            remote_sha,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (PluginRuntimeError, OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"[FAIL] {exc}")
