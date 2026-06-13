#!/usr/bin/env bash
set -euo pipefail

# ADVISORY hook (PreToolUse on Write/Edit). When a config or launcher is edited,
# remind if there is no matching `approved` card in experiments/registry.json.
# Never blocks. Fails open when jq is missing.
#
# The experiment ID is the basename of the config/launcher without extension,
# e.g. configs/E012_frozen-encoder.yaml -> E012_frozen-encoder.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
REGISTRY="$PROJECT_DIR/experiments/registry.json"

INPUT=$(cat)

if ! command -v jq >/dev/null 2>&1; then
  echo "RDD hook note: jq not found; skipping card-approval reminder." >&2
  exit 0
fi

FILE_PATH=$(jq -r '.tool_input.file_path // empty' <<<"$INPUT" 2>/dev/null | tr -d '\r' || true)

case "$FILE_PATH" in
  */configs/*|*/launchers/*) ;;
  *) exit 0 ;;
esac

[ -f "$REGISTRY" ] || { echo "RDD hook note: no registry yet; remember to register this experiment." >&2; exit 0; }

base=$(basename "$FILE_PATH")
id="${base%.*}"

status=$(jq -r --arg id "$id" '.experiments[]? | select(.id == $id) | .status' "$REGISTRY" 2>/dev/null | tr -d '\r' || true)

if [ -z "$status" ]; then
  echo "RDD reminder: no card registered for '$id'. Draft and get the card approved before building run artifacts (⛔ gate 1)." >&2
elif [ "$status" = "draft" ]; then
  echo "RDD reminder: card '$id' is still 'draft'. No config/launcher should be built before researcher approval (⛔ gate 1)." >&2
fi

exit 0
