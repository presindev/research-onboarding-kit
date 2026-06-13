#!/usr/bin/env bash
set -euo pipefail

# ADVISORY hook (PreToolUse on Write/Edit). Warns loudly when the target path is
# under a frozen-manifest entry. Never blocks (see block-frozen-writes.sh for the
# blocking variant). Fails open when jq is missing.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
MANIFEST="$PROJECT_DIR/data/frozen-manifest.json"

INPUT=$(cat)
[ -f "$MANIFEST" ] || exit 0

if ! command -v jq >/dev/null 2>&1; then
  echo "RDD hook note: jq not found; skipping frozen-path check." >&2
  exit 0
fi

FILE_PATH=$(jq -r '.tool_input.file_path // empty' <<<"$INPUT" 2>/dev/null | tr -d '\r' || true)
[ -n "$FILE_PATH" ] || exit 0

# Read non-retired frozen paths and see if FILE_PATH is under any of them.
while IFS= read -r p; do
  [ -n "$p" ] || continue
  case "$FILE_PATH" in
    *"$p"*)
      echo "🔒 RDD WARNING: '$FILE_PATH' is under a FROZEN artifact ($p)." >&2
      echo "   Frozen artifacts never mutate. A replacement gets a NEW name + a decision entry." >&2
      echo "   Verify integrity with: python scripts/check_frozen.py" >&2
      exit 0
      ;;
  esac
done < <(jq -r '.frozen[]? | select(.retired | not) | .path' "$MANIFEST" 2>/dev/null | tr -d '\r')

exit 0
