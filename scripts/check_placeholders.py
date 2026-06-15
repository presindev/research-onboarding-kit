#!/usr/bin/env python3
r"""Check that no UNRESOLVED placeholder tokens remain in final project files.

Onboarding instantiates templates and must not leave tokens like \{\{TOKEN\}\}
behind in the generated harness. This script finds the ones that matter and stays
quiet about the ones that are kept on purpose, so the end-of-installation check is
clean instead of noisy.

Deliberately ignored (these KEEP their tokens by design):
  * any *.template file (kit templates are not final artifacts);
  * the per-artifact templates copied under .claude/<...>/templates/ — they are
    instantiated per experiment/spec, not during onboarding;
  * VCS / cache / environment dirs (.git, __pycache__, node_modules, venvs).

Cross-platform: standard library only.

Usage:
    python scripts/check_placeholders.py [--root .]

Exit code 0 if no unresolved placeholders remain (warnings are clean), 1 otherwise.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# A placeholder token is two braces, an UPPER_SNAKE name, two braces — the kit
# convention. Built from escaped pieces so this source file is not itself flagged.
TOKEN = re.compile(r"\{\{\s*[A-Z0-9_]+\s*\}\}")

# Only text files worth scanning.
TEXT_SUFFIXES = {
    ".md", ".html", ".htm", ".json", ".yaml", ".yml",
    ".sh", ".py", ".css", ".js", ".txt", ".cfg", ".ini", ".toml",
}

# Directory names skipped wholesale.
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".mypy_cache"}


def is_template_dir(rel: Path) -> bool:
    """True for a per-artifact template dir under .claude (keeps tokens by design)."""
    parts = rel.parts
    return ".claude" in parts and "templates" in parts


def should_skip(rel: Path) -> bool:
    if any(part in SKIP_DIRS for part in rel.parts):
        return True
    if rel.suffix == ".template" or rel.name.endswith(".template"):
        return True
    if is_template_dir(rel):
        return True
    if rel.suffix.lower() not in TEXT_SUFFIXES:
        return True
    return False


def scan(root: Path) -> list[tuple[str, int, str]]:
    offenders: list[tuple[str, int, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if should_skip(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for m in TOKEN.finditer(line):
                offenders.append((rel.as_posix(), lineno, m.group(0)))
    return offenders


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", help="project root (default: cwd)")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    offenders = scan(root)
    if offenders:
        print("placeholder check FAILED -- unresolved tokens in final files:")
        for rel, lineno, tok in offenders:
            print(f"  - {rel}:{lineno}: {tok}")
        print("\nResolve these, or -- if a file is meant to keep its tokens -- move it "
              "under a .claude/.../templates/ directory or give it a .template suffix.")
        return 1

    print("placeholder check OK -- no unresolved tokens in final files "
          "(per-artifact templates intentionally keep theirs).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
