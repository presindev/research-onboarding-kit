#!/usr/bin/env python3
"""Snapshot the run environment for reproducibility.

Records interpreter version, installed packages, container/GPU info, platform,
and the git SHA + dirty flag. Referenced by each experiment card
(reference/reproducibility-policy.md). Cross-platform: standard library only.

NEVER records secrets: environment variables are intentionally excluded (they
often hold tokens). Capture configuration explicitly in the config, by name.

Usage:
    python scripts/capture_environment.py [--out results/<ID>/env.json]
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone


def run(cmd: list[str]) -> str | None:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if out.returncode == 0:
            return out.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    return None


def packages() -> str | None:
    # Prefer the running interpreter's pip so the snapshot matches this env.
    out = run([sys.executable, "-m", "pip", "freeze"])
    return out


def git_info() -> dict:
    sha = run(["git", "rev-parse", "HEAD"])
    status = run(["git", "status", "--porcelain"])
    dirty = bool(status) if status is not None else None
    return {"sha": sha, "dirty": dirty}


def gpu_info() -> str | None:
    return run(["nvidia-smi",
                "--query-gpu=name,driver_version,memory.total",
                "--format=csv,noheader"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=None, help="write JSON here (default: stdout)")
    args = ap.parse_args()

    snapshot = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "git": git_info(),
        "gpu": gpu_info(),                 # None if no nvidia-smi
        "conda_env": run(["conda", "env", "export"]),   # None if no conda
        "pip_freeze": packages(),
    }

    text = json.dumps(snapshot, indent=2) + "\n"
    if args.out:
        from pathlib import Path
        p = Path(args.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        print(f"environment snapshot written to {args.out}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
