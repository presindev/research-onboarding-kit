#!/usr/bin/env python3
"""Verify that frozen artifacts have not changed.

Recomputes the checksum of every entry in the frozen manifest and compares it to
the stored value. A mismatch means a frozen eval set / split / reference
checkpoint was mutated — a stop-and-investigate event
(reference/frozen-artifacts-policy.md). Cross-platform: standard library only.

Manifest format (default data/frozen-manifest.json):
    {"frozen": [{"id": "...", "path": "...", "checksum": "sha256:...", ...}, ...]}

Usage:
    python scripts/check_frozen.py [--root .] [--manifest data/frozen-manifest.json]
    python scripts/check_frozen.py --write   # fill in missing checksums (first freeze)

Exit code 0 if all frozen artifacts match, 1 on any mismatch/missing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def hash_path(path: Path) -> str:
    """sha256 of a file, or of a directory's sorted (relpath, contents)."""
    h = hashlib.sha256()
    if path.is_file():
        _feed_file(h, path)
    elif path.is_dir():
        for f in sorted(p for p in path.rglob("*") if p.is_file()):
            # Include the relative path so renames/moves are detected.
            h.update(str(f.relative_to(path)).replace("\\", "/").encode("utf-8"))
            _feed_file(h, f)
    else:
        raise FileNotFoundError(path)
    return "sha256:" + h.hexdigest()


def _feed_file(h: "hashlib._Hash", path: Path) -> None:
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--manifest", default="data/frozen-manifest.json")
    ap.add_argument("--write", action="store_true",
                    help="record checksums for entries that have none yet (initial freeze)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    manifest_path = root / args.manifest
    if not manifest_path.exists():
        print(f"no frozen manifest at {args.manifest} — nothing to check.")
        return 0

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = data.get("frozen", [])
    problems: list[str] = []
    wrote = False

    for rec in entries:
        if rec.get("retired"):
            continue
        rid = rec.get("id", "<no id>")
        rel = rec.get("path")
        if not rel:
            problems.append(f"{rid}: manifest entry has no 'path'")
            continue
        target = root / rel
        try:
            actual = hash_path(target)
        except FileNotFoundError:
            problems.append(f"{rid}: frozen path missing on disk: {rel}")
            continue

        stored = rec.get("checksum")
        if not stored:
            if args.write:
                rec["checksum"] = actual
                wrote = True
                print(f"{rid}: recorded checksum {actual}")
            else:
                problems.append(f"{rid}: no checksum recorded (run with --write to freeze)")
        elif stored != actual:
            problems.append(f"{rid}: CHECKSUM MISMATCH -- frozen artifact changed!\n"
                            f"      stored: {stored}\n      actual: {actual}")

    if wrote:
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    if problems:
        print("frozen-artifact check FAILED:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"frozen-artifact check OK ({len(entries)} entries).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
