# Hook settings snippets

Wiring for `.claude/settings.json`. **Nothing here is active until the researcher
approves it and it is written into settings.json.** Copy the chosen hook scripts
into the project (e.g. `.claude/hooks/`) and reference them by path. Adapt event
names/matchers to the installed Claude Code version before relying on exact
syntax.

## Advisory tier (recommended to enable first)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "bash .claude/hooks/suggest-card.sh" },
          { "type": "command", "command": "bash .claude/hooks/frozen-path-warning.sh" },
          { "type": "command", "command": "bash .claude/hooks/smoke-test-reminder.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "bash .claude/hooks/post-results-reminder.sh" }
        ]
      }
    ]
  }
}
```

## Blocking tier (opt-in, after the workflow is trusted)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "bash .claude/hooks/block-unapproved-launch.sh" },
          { "type": "command", "command": "bash .claude/hooks/block-frozen-writes.sh" }
        ]
      }
    ]
  }
}
```

## Notes

- Advisory hooks print to stderr and exit 0 (never block). Blocking hooks exit 2
  to deny a tool call.
- All hooks **fail open** when `jq` is missing (warn and allow). Switch to
  fail-closed only with explicit, recorded approval
  (`decisions/architecture-decisions.md`).
- The blocking pair enforces the launch side of ⛔ gate 1 and the frozen-artifacts
  policy. The claim side (verdict confirmation, ⛔ gate 2) has **no hook
  substitute** — it stays a human decision by design.
- Keep matchers narrow; an over-broad blocking hook stops legitimate work.
