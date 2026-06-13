#!/usr/bin/env bash
set -euo pipefail

# BLOCKING hook (opt-in; PreToolUse on Write/Edit). Refuses any write to a path
# under a non-retired frozen-manifest entry. Enforces the frozen-artifacts policy.
# Fails OPEN when jq is missing (warns). Exit 2 = block.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
MANIFEST="$PROJECT_DIR/data/frozen-manifest.json"
INPUT=$(cat)

[ -f "$MANIFEST" ] || exit 0

if ! command -v jq >/dev/null 2>&1; then
  echo "RDD hook warning: jq not found; cannot enforce frozen-write guard." >&2
  exit 0
fi

FILE_PATH=$(jq -r '.tool_input.file_path // empty' <<<"$INPUT" 2>/dev/null | tr -d '\r' || true)
[ -n "$FILE_PATH" ] || exit 0

while IFS= read -r p; do
  [ -n "$p" ] || continue
  case "$FILE_PATH" in
    *"$p"*)
      echo "Blocked by RDD policy: '$FILE_PATH' is under a FROZEN artifact ($p)." >&2
      echo "Frozen artifacts never mutate. Create a replacement with a NEW name and record a decision." >&2
      exit 2
      ;;
  esac
done < <(jq -r '.frozen[]? | select(.retired | not) | .path' "$MANIFEST" 2>/dev/null | tr -d '\r')

exit 0
