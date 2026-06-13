#!/usr/bin/env bash
set -euo pipefail

# BLOCKING hook (opt-in; PreToolUse on Write/Edit). Refuses to create/edit a
# launcher whose card is not yet `approved` (or later). Enforces ⛔ gate 1: no
# run artifacts before card approval. Fails OPEN when jq is missing (warns).
#
# Exit 2 = block. Exit 0 = allow.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
REGISTRY="$PROJECT_DIR/experiments/registry.json"
INPUT=$(cat)

if ! command -v jq >/dev/null 2>&1; then
  echo "RDD hook warning: jq not found; cannot enforce launch-approval guard." >&2
  exit 0
fi

FILE_PATH=$(jq -r '.tool_input.file_path // empty' <<<"$INPUT" 2>/dev/null | tr -d '\r' || true)

case "$FILE_PATH" in
  */launchers/*) ;;
  *) exit 0 ;;
esac

[ -f "$REGISTRY" ] || {
  echo "Blocked by RDD policy: no registry; cannot confirm the card is approved." >&2
  echo "Draft and approve the card (⛔ gate 1) before building a launcher." >&2
  exit 2
}

base=$(basename "$FILE_PATH")
id="${base%.*}"
status=$(jq -r --arg id "$id" '.experiments[]? | select(.id == $id) | .status' "$REGISTRY" 2>/dev/null | tr -d '\r' || true)

case "$status" in
  approved|launched|analyzed|done) exit 0 ;;
  *)
    echo "Blocked by RDD policy: card '$id' status is '${status:-missing}', not approved." >&2
    echo "No config/launcher/run before the researcher approves the card (⛔ gate 1)." >&2
    exit 2
    ;;
esac
