#!/usr/bin/env python3
from __future__ import annotations

import argparse
import collections
import datetime
import json
import subprocess
import time
from pathlib import Path
from typing import Any


EXCLUDED_REPOSITORIES = {
    "_worktrees",
    "commission-tier-monitoring",
    "market-overview-analysis",
    "old",
}


def git(path: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip() if result.returncode == 0 else ""


def discover_repositories(workspace: Path, names: set[str] | None) -> list[Path]:
    repositories: list[Path] = []
    seen_common_dirs: set[Path] = set()
    for child in sorted(workspace.iterdir()):
        if not child.is_dir() or child.name in EXCLUDED_REPOSITORIES:
            continue
        if names is not None and child.name not in names:
            continue
        top_level = git(child, "rev-parse", "--show-toplevel", check=False)
        if top_level and Path(top_level).resolve() == child.resolve():
            common_dir_text = git(child, "rev-parse", "--git-common-dir", check=False)
            common_dir = Path(common_dir_text)
            if not common_dir.is_absolute():
                common_dir = child / common_dir
            common_dir = common_dir.resolve()
            if common_dir in seen_common_dirs:
                continue
            seen_common_dirs.add(common_dir)
            repositories.append(child)
    return repositories


def parse_worktrees(repo: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    record: dict[str, str] = {}
    for line in git(repo, "worktree", "list", "--porcelain").splitlines() + [""]:
        if not line:
            if record:
                records.append(record)
                record = {}
            continue
        key, _, value = line.partition(" ")
        record[key] = value
    return records


def divergence(path: Path, left: str, right: str = "HEAD") -> tuple[int, int] | None:
    output = git(path, "rev-list", "--left-right", "--count", f"{left}...{right}", check=False)
    if not output:
        return None
    left_only, right_only = output.split()
    return int(left_only), int(right_only)


def is_ancestor(path: Path, ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(path), "merge-base", "--is-ancestor", ancestor, descendant],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def worktree_metadata(path: Path) -> dict[str, Any]:
    git_dir_text = git(path, "rev-parse", "--absolute-git-dir", check=False)
    if not git_dir_text:
        return {}
    metadata_path = Path(git_dir_text) / "codex-worktree.json"
    try:
        value = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def metadata_created_timestamp(metadata: dict[str, Any]) -> int | None:
    value = metadata.get("created_at")
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return int(parsed.timestamp())


def classify(
    *,
    canonical: bool,
    dirty_count: int,
    detached: bool,
    upstream: str,
    local_only: int | None,
    base_only: int | None,
    task_only: int | None,
    merged_to_cached_main: bool,
    age_days: int,
    stale_days: int,
    prunable: bool,
) -> str:
    if canonical:
        return "canonical"
    if prunable:
        return "prunable-review"
    if dirty_count:
        return "active-or-uncommitted"
    if local_only and local_only > 0:
        return "unmerged-or-unpushed"
    if task_only and task_only > 0 and not merged_to_cached_main:
        return "unmerged-or-unpushed"
    if detached:
        return "detached-review"
    if not upstream:
        return "owner-and-upstream-review"
    if age_days >= stale_days and merged_to_cached_main:
        return "cleanup-review"
    if base_only and base_only > 0:
        return "stale-base-review"
    if age_days >= stale_days:
        return "stale-review"
    return "recent"


def canonical_health(
    *,
    canonical: bool,
    dirty_count: int,
    detached: bool,
    upstream: str,
    upstream_divergence: tuple[int, int] | None,
) -> str:
    if not canonical:
        return ""
    if dirty_count:
        return "dirty"
    if detached:
        return "detached"
    if not upstream:
        return "no-upstream"
    if upstream_divergence:
        upstream_only, local_only = upstream_divergence
        if upstream_only and local_only:
            return "diverged"
        if upstream_only:
            return "behind"
        if local_only:
            return "ahead"
    return "clean"


def inspect_repository(repo: Path, stale_days: int, now: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    records = parse_worktrees(repo)
    canonical_path = Path(records[0]["worktree"]).resolve() if records else repo.resolve()
    cached_main = "refs/remotes/origin/main"
    cached_main_exists = bool(git(repo, "rev-parse", "--verify", cached_main, check=False))

    for record in records:
        path = Path(record["worktree"])
        canonical = path.resolve() == canonical_path
        detached = "detached" in record
        branch_ref = record.get("branch", "")
        branch = branch_ref.removeprefix("refs/heads/") if branch_ref else "DETACHED"
        prunable = "prunable" in record
        metadata = worktree_metadata(path)
        dirty_lines = git(path, "status", "--porcelain=v1", check=False).splitlines()
        dirty_count = len(dirty_lines)
        upstream = git(
            path,
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{u}",
            check=False,
        )
        upstream_divergence = divergence(path, upstream) if upstream else None
        local_only = upstream_divergence[1] if upstream_divergence else None
        base_divergence = divergence(path, cached_main) if cached_main_exists else None
        base_only = base_divergence[0] if base_divergence else None
        task_only = base_divergence[1] if base_divergence else None
        merged_to_cached_main = (
            cached_main_exists and is_ancestor(path, "HEAD", cached_main)
        )
        commit_timestamp_text = git(path, "show", "-s", "--format=%ct", "HEAD", check=False)
        commit_timestamp = int(commit_timestamp_text) if commit_timestamp_text else now
        created_timestamp = metadata_created_timestamp(metadata)
        age_timestamp = created_timestamp if created_timestamp is not None else commit_timestamp
        age_days = max(0, (now - age_timestamp) // 86400)
        state = classify(
            canonical=canonical,
            dirty_count=dirty_count,
            detached=detached,
            upstream=upstream,
            local_only=local_only,
            base_only=base_only,
            task_only=task_only,
            merged_to_cached_main=merged_to_cached_main,
            age_days=age_days,
            stale_days=stale_days,
            prunable=prunable,
        )
        canonical_state = canonical_health(
            canonical=canonical,
            dirty_count=dirty_count,
            detached=detached,
            upstream=upstream,
            upstream_divergence=upstream_divergence,
        )
        rows.append(
            {
                "repository": repo.name,
                "path": str(path),
                "branch": branch,
                "owner": metadata.get("owner", "unknown" if not canonical else "canonical"),
                "task_ref": metadata.get("task_ref", ""),
                "created_at": metadata.get("created_at", ""),
                "age_source": "created_at" if created_timestamp is not None else "head_commit",
                "state": state,
                "canonical_health": canonical_state,
                "age_days": age_days,
                "dirty_paths": dirty_count,
                "upstream": upstream,
                "upstream_only": upstream_divergence[0] if upstream_divergence else None,
                "local_only": local_only,
                "cached_main_only": base_only,
                "task_only_vs_cached_main": task_only,
                "merged_to_cached_main": merged_to_cached_main,
                "remote_refs": "local-cache-only",
            }
        )
    return rows


def tsv_text(rows: list[dict[str, Any]]) -> str:
    columns = (
        "repository",
        "state",
        "canonical_health",
        "age_days",
        "dirty_paths",
        "branch",
        "owner",
        "task_ref",
        "upstream",
        "cached_main_only",
        "task_only_vs_cached_main",
        "path",
    )
    lines = ["\t".join(columns)]
    for row in rows:
        lines.append(
            "\t".join(
                "" if row[column] is None else str(row[column]) for column in columns
            )
        )
    return "\n".join(lines) + "\n"


def count_metrics(rows: list[dict[str, Any]]) -> dict[str, int]:
    canonical_rows = [row for row in rows if row["state"] == "canonical"]
    metrics = {
        "total_worktrees": len(rows),
        "canonical_worktrees": len(canonical_rows),
        "non_canonical_worktrees": len(rows) - len(canonical_rows),
    }
    for health, count in collections.Counter(
        row["canonical_health"] for row in canonical_rows
    ).items():
        metrics[f"canonical_health.{health}"] = count
    for state, count in collections.Counter(row["state"] for row in rows).items():
        metrics[f"state.{state}"] = count
    return metrics


def report_scope(
    workspace: Path, repositories: set[str] | None, stale_days: int
) -> dict[str, Any]:
    return {
        "workspace": str(workspace),
        "repositories": sorted(repositories) if repositories is not None else None,
        "stale_days": stale_days,
    }


def load_baseline(
    path: Path, expected_scope: dict[str, Any]
) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise SystemExit(f"cannot read baseline JSON: {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise SystemExit(f"invalid baseline JSON: {path}: {error}") from error
    if not isinstance(payload, dict):
        raise SystemExit(f"baseline JSON must contain an object: {path}")
    actual_scope = payload.get("scope")
    if actual_scope != expected_scope:
        raise SystemExit(
            f"baseline JSON scope does not match the current report: {path}"
        )
    rows = payload.get("worktrees")
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise SystemExit(f"baseline JSON must contain a worktrees list: {path}")
    return rows


def metric_deltas(
    current_rows: list[dict[str, Any]], baseline_rows: list[dict[str, Any]]
) -> dict[str, int]:
    current = count_metrics(current_rows)
    baseline = count_metrics(baseline_rows)
    return {
        metric: current.get(metric, 0) - baseline.get(metric, 0)
        for metric in sorted(current.keys() | baseline.keys())
    }


def render_summary(
    rows: list[dict[str, Any]], deltas: dict[str, int] | None = None
) -> None:
    canonical_rows = [row for row in rows if row["state"] == "canonical"]
    print("metric\tcount")
    print(f"total_worktrees\t{len(rows)}")
    print(f"canonical_worktrees\t{len(canonical_rows)}")
    print(f"non_canonical_worktrees\t{len(rows) - len(canonical_rows)}")
    print()
    health_counts = collections.Counter(row["canonical_health"] for row in canonical_rows)
    print("canonical_health\tcount")
    for health, count in sorted(health_counts.items()):
        print(f"{health}\t{count}")
    print()
    counts = collections.Counter((row["repository"], row["state"]) for row in rows)
    print("repository\tstate\tcount")
    for (repository, state), count in sorted(counts.items()):
        print(f"{repository}\t{state}\t{count}")
    if deltas is not None:
        print()
        print("metric_delta\tcount")
        for metric, count in deltas.items():
            print(f"{metric}\t{count}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report Adrez worktree evidence without fetching or changing repositories."
    )
    parser.add_argument("workspace", nargs="?", default="/Users/martin/Documents/adrez")
    parser.add_argument("--repo", action="append", dest="repositories")
    parser.add_argument("--stale-days", type=int, default=7)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    parser.add_argument("--baseline-json", type=Path)
    parser.add_argument("--max-noncanonical-growth", type=int)
    parser.add_argument("--tsv-output", type=Path)
    parser.add_argument("--overwrite-tsv-output", action="store_true")
    args = parser.parse_args()
    if args.stale_days < 0:
        raise SystemExit("--stale-days must be zero or greater")
    if args.max_noncanonical_growth is not None:
        if args.max_noncanonical_growth < 0:
            raise SystemExit("--max-noncanonical-growth must be zero or greater")
        if args.baseline_json is None:
            raise SystemExit("--max-noncanonical-growth requires --baseline-json")
    if args.json and args.summary_only:
        raise SystemExit("--json and --summary-only cannot be combined")
    if args.overwrite_tsv_output and args.tsv_output is None:
        raise SystemExit("--overwrite-tsv-output requires --tsv-output")

    workspace = Path(args.workspace).resolve()
    names = set(args.repositories) if args.repositories else None
    scope = report_scope(workspace, names, args.stale_days)
    rows: list[dict[str, Any]] = []
    now = int(time.time())
    for repo in discover_repositories(workspace, names):
        rows.extend(inspect_repository(repo, args.stale_days, now))

    baseline_rows = (
        load_baseline(args.baseline_json, scope) if args.baseline_json else None
    )
    deltas = metric_deltas(rows, baseline_rows) if baseline_rows is not None else None

    if args.tsv_output:
        mode = "w" if args.overwrite_tsv_output else "x"
        try:
            with args.tsv_output.open(mode, encoding="utf-8") as output:
                output.write(tsv_text(rows))
        except FileExistsError as error:
            raise SystemExit(
                f"TSV output already exists; use --overwrite-tsv-output to replace it: "
                f"{args.tsv_output}"
            ) from error

    if args.json:
        payload: dict[str, Any] = {
            "workspace": str(workspace),
            "scope": scope,
            "worktrees": rows,
        }
        if deltas is not None:
            payload["deltas"] = deltas
        print(json.dumps(payload, indent=2))
    elif args.summary_only:
        render_summary(rows, deltas)
    else:
        print(tsv_text(rows), end="")

    if args.max_noncanonical_growth is not None and deltas is not None:
        growth = deltas["non_canonical_worktrees"]
        if growth > args.max_noncanonical_growth:
            raise SystemExit(2)


if __name__ == "__main__":
    main()
