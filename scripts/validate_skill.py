#!/usr/bin/env python3
"""Validate the distributable Agent Skill without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "comfortable-ones-act-up"
SKILL_DIR = ROOT / SKILL_NAME
SKILL_FILE = SKILL_DIR / "SKILL.md"
OPENAI_FILE = SKILL_DIR / "agents" / "openai.yaml"
README_FILE = ROOT / "README.md"


def local_links(path: Path) -> list[Path]:
    text = path.read_text(encoding="utf-8")
    links: list[Path] = []
    for raw in re.findall(r"\]\(([^)]+)\)", text):
        target = raw.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("#"):
            continue
        links.append((path.parent / target).resolve())
    return links


def main() -> int:
    errors: list[str] = []
    required = [SKILL_FILE, OPENAI_FILE, README_FILE, SKILL_DIR / "references"]
    for path in required:
        if not path.exists():
            errors.append(f"missing required path: {path.relative_to(ROOT)}")

    if not errors:
        skill_text = SKILL_FILE.read_text(encoding="utf-8")
        parts = skill_text.split("---", 2)
        if len(parts) < 3:
            errors.append("SKILL.md is missing YAML frontmatter")
        else:
            frontmatter = parts[1]
            name_match = re.search(r"^name:\s*([^\n]+)$", frontmatter, re.MULTILINE)
            description_match = re.search(
                r"^description:\s*(\S.*)$", frontmatter, re.MULTILINE
            )
            if not name_match:
                errors.append("frontmatter name is missing")
            elif name_match.group(1).strip() != SKILL_NAME:
                errors.append("frontmatter name must match the skill directory")
            if not description_match:
                errors.append("frontmatter description is missing or empty")

        openai_text = OPENAI_FILE.read_text(encoding="utf-8")
        if f"${SKILL_NAME}" not in openai_text:
            errors.append("agents/openai.yaml default prompt must mention the skill")

        linked_refs = {
            path.name
            for path in local_links(SKILL_FILE)
            if path.parent == (SKILL_DIR / "references").resolve()
        }
        actual_refs = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
        for name in sorted(actual_refs - linked_refs):
            errors.append(f"reference is not routed from SKILL.md: {name}")

        for source in [README_FILE, SKILL_FILE]:
            for target in local_links(source):
                if not target.exists():
                    errors.append(
                        f"broken local link in {source.relative_to(ROOT)}: {target}"
                    )

        text_files = list(ROOT.glob("*.md")) + list(SKILL_DIR.rglob("*.md"))
        text_files += list(SKILL_DIR.rglob("*.yaml"))
        for path in text_files:
            text = path.read_text(encoding="utf-8")
            if re.search(r"TODO|FIXME|PLACEHOLDER|\[Add[^]]*\]", text, re.IGNORECASE):
                errors.append(f"unfinished placeholder in {path.relative_to(ROOT)}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    reference_count = len(list((SKILL_DIR / "references").glob("*.md")))
    print(f"Validation passed: {SKILL_NAME} with {reference_count} routed references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
