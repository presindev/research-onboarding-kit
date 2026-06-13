#!/usr/bin/env bash
set -euo pipefail

# ADVISORY hook (PostToolUse on Write/Edit). When a file is written under
# results/<ID>/, remind to fill the card's Results section and update the
# registry row. Never blocks. Does not write anything.

INPUT=$(cat)

if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

FILE_PATH=$(jq -r '.tool_input.file_path // empty' <<<"$INPUT" 2>/dev/null | tr -d '\r' || true)
[ -n "$FILE_PATH" ] || exit 0

case "$FILE_PATH" in
  */results/*)
    # Extract the experiment ID: the path component right after results/.
    after="${FILE_PATH#*/results/}"
    id="${after%%/*}"
    echo "RDD reminder: results landed under results/$id/." >&2
    echo "  - Fill the Results section of experiments/$id/card.html from the REAL outputs (failures and negatives count too)." >&2
    echo "  - Update the registry record ($id): status -> analyzed, gate_result, actual_cost." >&2
    echo "  - Run the skeptic before proposing a verdict; then ⛔ the researcher confirms it." >&2
    ;;
esac

exit 0
