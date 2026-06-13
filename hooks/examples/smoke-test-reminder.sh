#!/usr/bin/env bash
set -euo pipefail

# ADVISORY hook (PreToolUse/PostToolUse on Write to launchers/). When a launcher
# is created whose card has no recorded smoke-test pass, remind that the smoke
# test must pass locally before any cluster submission. Never blocks. Fails open.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
REGISTRY="$PROJECT_DIR/experiments/registry.json"
INPUT=$(cat)

if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

FILE_PATH=$(jq -r '.tool_input.file_path // empty' <<<"$INPUT" 2>/dev/null | tr -d '\r' || true)

case "$FILE_PATH" in
  */launchers/*) ;;
  *) exit 0 ;;
esac

base=$(basename "$FILE_PATH")
id="${base%.*}"

[ -f "$REGISTRY" ] || { echo "RDD reminder: smoke test must pass locally before queuing '$id'." >&2; exit 0; }

smoke=$(jq -r --arg id "$id" '.experiments[]? | select(.id == $id) | .smoke_passed // empty' "$REGISTRY" 2>/dev/null | tr -d '\r' || true)

if [ -z "$smoke" ] || [ "$smoke" = "null" ]; then
  echo "RDD reminder: card '$id' has no recorded smoke-test pass." >&2
  echo "  Run the smallest sanity job locally first; record smoke_passed before any cluster submission (compute-budget-policy)." >&2
fi

exit 0
