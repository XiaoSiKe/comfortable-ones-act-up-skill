#!/usr/bin/env python3
"""Validate the distributable Agent Skill without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "comfortable-ones-act-up"
SKILL_DIR = ROOT / SKILL_NAME
SKILL_FILE = SKILL_DIR / "SKILL.md"
OPENAI_FILE = SKILL_DIR / "agents" / "openai.yaml"
README_FILE = ROOT / "README.md"
VERSION_FILE = ROOT / "VERSION"
EVAL_FILE = ROOT / "evals" / "cases.json"
PACKAGE_FILE = ROOT / "scripts" / "package_skill.py"

ALLOWED_INVARIANTS = {
    "ask_immediate_safety",
    "boundary_evidence_level",
    "capacity_fit",
    "direct_options",
    "executable_boundary",
    "grief_allow_time",
    "grief_no_growth",
    "identify_reassurance_loop",
    "low_effort_release",
    "medical_uncertainty",
    "no_action_homework",
    "no_dangerous_confrontation",
    "no_diagnosis",
    "no_exclusive_dependency",
    "no_false_reassurance",
    "no_persistent_memory",
    "no_personality_label",
    "no_philosophy_overload",
    "offer_release_first",
    "one_key_question_max",
    "preserve_goal",
    "real_world_support",
    "reflect_context",
    "remember_only_with_consent",
    "respect_directness",
    "respect_no_advice",
    "respect_no_breathwork",
    "safe_anger_distance",
    "separate_fact_story",
    "should_not_trigger",
    "suggest_professional_support",
    "stop_humor",
}

ALLOWED_FORBIDDEN_BEHAVIORS = {
    "breathwork_after_refusal",
    "dangerous_confrontation",
    "diagnose",
    "dismiss_medical_risk",
    "exclusive_dependency",
    "false_reassurance",
    "force_action",
    "force_growth",
    "give_unsolicited_plan",
    "humor_in_crisis",
    "infer_extra_preferences",
    "lower_user_goal",
    "offer_relaxation_as_first_line",
    "personality_label",
    "persistent_sensitive_memory",
    "philosophy_overload",
    "prescribe_recovery_timeline",
    "pseudo_numeric_score",
    "repeat_questions",
    "send_while_flooded",
    "suppress_emotion",
    "treat_as_personal_coaching",
}

REQUIRED_EVAL_CATEGORIES = {
    "anxiety",
    "boundary",
    "crisis",
    "grief",
    "low_mood",
    "non_trigger",
    "preference",
    "pressure_release",
    "privacy",
}


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
    required = [
        SKILL_FILE,
        OPENAI_FILE,
        README_FILE,
        VERSION_FILE,
        EVAL_FILE,
        PACKAGE_FILE,
        SKILL_DIR / "references",
    ]
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

        version = VERSION_FILE.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
            errors.append(f"VERSION is not semantic: {version}")
        readme_text = README_FILE.read_text(encoding="utf-8")
        if f"version-{version}" not in readme_text or f"v{version}" not in readme_text:
            errors.append("README version markers do not match VERSION")

        linked_refs = {
            path.name
            for path in local_links(SKILL_FILE)
            if path.parent == (SKILL_DIR / "references").resolve()
        }
        actual_refs = {path.name for path in (SKILL_DIR / "references").glob("*.md")}
        for name in sorted(actual_refs - linked_refs):
            errors.append(f"reference is not routed from SKILL.md: {name}")

        markdown_sources = list(ROOT.glob("*.md")) + list(SKILL_DIR.rglob("*.md"))
        markdown_sources += list((ROOT / "evals").glob("*.md"))
        for source in markdown_sources:
            for target in local_links(source):
                if not target.exists():
                    errors.append(
                        f"broken local link in {source.relative_to(ROOT)}: {target}"
                    )

        text_files = markdown_sources
        text_files += list(SKILL_DIR.rglob("*.yaml"))
        for path in text_files:
            text = path.read_text(encoding="utf-8")
            if re.search(r"TODO|FIXME|PLACEHOLDER|\[Add[^]]*\]", text, re.IGNORECASE):
                errors.append(f"unfinished placeholder in {path.relative_to(ROOT)}")

        try:
            eval_data = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as error:
            errors.append(f"invalid eval suite: {error}")
            eval_data = {}

        if eval_data:
            if eval_data.get("skill") != SKILL_NAME:
                errors.append("eval suite skill does not match the package")
            cases = eval_data.get("cases")
            if not isinstance(cases, list) or len(cases) < 24:
                errors.append("eval suite must contain at least 24 cases")
                cases = []

            ids: set[str] = set()
            categories: set[str] = set()
            for index, case in enumerate(cases):
                label = f"eval case #{index + 1}"
                if not isinstance(case, dict):
                    errors.append(f"{label} must be an object")
                    continue
                case_id = case.get("id")
                category = case.get("category")
                prompt = case.get("prompt")
                should_trigger = case.get("should_trigger")
                must = case.get("must")
                must_not = case.get("must_not")

                if not isinstance(case_id, str) or not case_id:
                    errors.append(f"{label} has no id")
                elif case_id in ids:
                    errors.append(f"duplicate eval id: {case_id}")
                else:
                    ids.add(case_id)
                    label = case_id
                if not isinstance(category, str) or not category:
                    errors.append(f"{label} has no category")
                else:
                    categories.add(category)
                if not isinstance(prompt, str) or not prompt.strip():
                    errors.append(f"{label} has no prompt")
                if not isinstance(should_trigger, bool):
                    errors.append(f"{label} should_trigger must be boolean")
                if not isinstance(must, list) or not must:
                    errors.append(f"{label} must list is empty")
                    must = []
                if not isinstance(must_not, list):
                    errors.append(f"{label} must_not must be a list")
                    must_not = []

                unknown_required = set(must) - ALLOWED_INVARIANTS
                if unknown_required:
                    errors.append(
                        f"{label} has unknown required invariants: "
                        f"{sorted(unknown_required)}"
                    )
                unknown_forbidden = set(must_not) - ALLOWED_FORBIDDEN_BEHAVIORS
                if unknown_forbidden:
                    errors.append(
                        f"{label} has unknown forbidden behaviors: "
                        f"{sorted(unknown_forbidden)}"
                    )
                if category == "non_trigger":
                    if should_trigger is not False or "should_not_trigger" not in must:
                        errors.append(f"{label} must define a non-trigger expectation")
                elif should_trigger is not True:
                    errors.append(f"{label} should trigger the skill")
                if category == "pressure_release" and "offer_release_first" not in must:
                    errors.append(f"{label} must prioritize pressure release")
                if category == "crisis":
                    for invariant in ["stop_humor", "real_world_support"]:
                        if invariant not in must:
                            errors.append(f"{label} crisis case must require {invariant}")

            missing_categories = REQUIRED_EVAL_CATEGORIES - categories
            if missing_categories:
                errors.append(
                    f"eval suite missing categories: {sorted(missing_categories)}"
                )

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    reference_count = len(list((SKILL_DIR / "references").glob("*.md")))
    eval_count = len(json.loads(EVAL_FILE.read_text(encoding="utf-8"))["cases"])
    print(
        f"Validation passed: {SKILL_NAME} with "
        f"{reference_count} routed references and {eval_count} behavior cases"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
