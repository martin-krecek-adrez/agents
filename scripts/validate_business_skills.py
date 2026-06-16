#!/usr/bin/env python3
"""Validate Adrez business skill conventions without external dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER = {
    "name",
    "description",
    "scope",
    "status",
    "owner",
    "last_reviewed",
}
ALLOWED_STATUSES = {"active", "legacy", "archived"}
SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TODO_RE = re.compile(r"\[TODO:|TODO:", re.IGNORECASE)


def fail(issues: list[str], path: Path, message: str) -> None:
    issues.append(f"{path}: {message}")


def parse_frontmatter(path: Path, issues: list[str]) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(issues, path, "missing opening YAML frontmatter marker")
        return {}, text

    try:
        end_index = lines[1:].index("---") + 1
    except ValueError:
        fail(issues, path, "missing closing YAML frontmatter marker")
        return {}, text

    frontmatter: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end_index], start=2):
        stripped = line.strip()
        if not stripped:
            continue
        if ":" not in stripped:
            fail(issues, path, f"invalid frontmatter line {line_number}: {line}")
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in frontmatter:
            fail(issues, path, f"duplicate frontmatter key: {key}")
        frontmatter[key] = value

    return frontmatter, text


def parse_simple_yaml_values(path: Path, issues: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in {"display_name", "short_description", "default_prompt"}:
            values[key] = value
        elif stripped.startswith("default_prompt") and not value:
            fail(issues, path, f"empty default_prompt at line {line_number}")

    return values


def validate_skill(skill_dir: Path, issues: list[str], warnings: list[str]) -> None:
    skill_file = skill_dir / "SKILL.md"
    frontmatter, text = parse_frontmatter(skill_file, issues)
    name = frontmatter.get("name", "")

    missing = sorted(REQUIRED_FRONTMATTER - set(frontmatter))
    if missing:
        fail(issues, skill_file, f"missing required frontmatter keys: {', '.join(missing)}")

    if name != skill_dir.name:
        fail(issues, skill_file, f"name '{name}' does not match directory '{skill_dir.name}'")
    if name and not SKILL_NAME_RE.match(name):
        fail(issues, skill_file, f"invalid skill name: {name}")

    if frontmatter.get("scope") != "business":
        fail(issues, skill_file, "scope must be 'business'")
    if frontmatter.get("status") and frontmatter["status"] not in ALLOWED_STATUSES:
        fail(issues, skill_file, f"invalid status: {frontmatter['status']}")
    if frontmatter.get("last_reviewed") and not DATE_RE.match(frontmatter["last_reviewed"]):
        fail(issues, skill_file, f"last_reviewed must be YYYY-MM-DD: {frontmatter['last_reviewed']}")

    description = frontmatter.get("description", "")
    if len(description) < 80:
        warnings.append(f"{skill_file}: short description may under-trigger ({len(description)} chars)")
    if description and "use " not in description.lower():
        warnings.append(f"{skill_file}: description does not include explicit use/trigger guidance")

    if TODO_RE.search(text):
        fail(issues, skill_file, "contains TODO placeholder text")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.exists():
        values = parse_simple_yaml_values(openai_yaml, issues)
        for key in ("display_name", "short_description", "default_prompt"):
            if key not in values:
                fail(issues, openai_yaml, f"missing interface.{key}")
        default_prompt = values.get("default_prompt", "")
        if name and f"${name}" not in default_prompt:
            fail(issues, openai_yaml, f"default_prompt must mention ${name}")


def main() -> int:
    skills_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("skills")
    issues: list[str] = []
    warnings: list[str] = []

    if not skills_root.is_dir():
        print(f"[FAIL] skills root does not exist: {skills_root}", file=sys.stderr)
        return 1

    skill_dirs = sorted(path for path in skills_root.iterdir() if (path / "SKILL.md").is_file())
    for skill_dir in skill_dirs:
        validate_skill(skill_dir, issues, warnings)

    for warning in warnings:
        print(f"[WARN] {warning}", file=sys.stderr)
    if issues:
        for issue in issues:
            print(f"[FAIL] {issue}", file=sys.stderr)
        print(f"Business skill validation failed with {len(issues)} issue(s).", file=sys.stderr)
        return 1

    print(f"[OK] Validated {len(skill_dirs)} business skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
