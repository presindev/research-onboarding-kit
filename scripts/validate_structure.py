#!/usr/bin/env python3
"""Check that a target project has the expected RDD harness structure.

Run after onboarding (and in Phase 5 of installation). Reports missing expected
files/dirs. Optional pieces (decision logs, optional packs) are only checked when
present. Cross-platform: standard library only.

Usage:
    python scripts/validate_structure.py [--root .]

Exit code 0 if the required structure is present, 1 otherwise. Warnings about
optional pieces do not fail the check.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# (path, is_dir) — required after a standard onboarding.
REQUIRED = [
    ("CLAUDE.md", False),
    ("PLAN.md", False),
    ("experiments", True),
    ("experiments/registry.json", False),
    ("notebook/NOTEBOOK.html", False),
    ("decisions/answers.md", False),
    (".claude/skills/research-workflow/SKILL.md", False),
    (".claude/agents", True),
    (".claude/context/project-map.md", False),
]

# Recommended but not fatal.
RECOMMENDED = [
    ("PLAN.html", False),
    ("experiments/research.css", False),
    ("experiments/research.js", False),
    ("experiments/registry.html", False),
    ("notebook/research.css", False),
    ("scripts/validate_registry.py", False),
    ("scripts/check_frozen.py", False),
    ("scripts/capture_environment.py", False),
    ("scripts/check_placeholders.py", False),
]


def check(root: Path, items) -> list[str]:
    missing = []
    for rel, is_dir in items:
        p = root / rel
        ok = p.is_dir() if is_dir else p.is_file()
        if not ok:
            missing.append(rel + ("/" if is_dir else ""))
    return missing


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    missing_required = check(root, REQUIRED)
    missing_recommended = check(root, RECOMMENDED)

    if missing_recommended:
        print("warnings (recommended, not fatal):")
        for m in missing_recommended:
            print(f"  - missing {m}")

    if missing_required:
        print("structure validation FAILED — missing required:")
        for m in missing_required:
            print(f"  - {m}")
        return 1

    print("structure validation OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
