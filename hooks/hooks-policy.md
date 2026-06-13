# Hooks policy for the RDD harness

Hooks are optional but useful for enforcing the experiment loop's constraints
deterministically — regardless of whether Claude remembers them. The RDD gates
protect two things: **launches** and **claims**. The hooks reinforce the launch
side (card approval, smoke test, frozen artifacts); the claim side stays a human
gate by design.

**Do not enable hooks without explicit researcher approval.**

## Recommended rollout

1. Start with no hooks enabled.
2. Install hook scripts as examples.
3. Ask which hooks to enable.
4. Enable advisory (warn-only) mode first.
5. Move to blocking mode after the team trusts the workflow.

## Environment requirements

The example hooks are bash and rely on `jq` for reading the hook JSON, the
registry, and the frozen manifest. On Windows that means Git Bash (or WSL) plus
`jq` on `PATH`. The examples **fail open** — warn and allow — when `jq` is
missing; switch any to fail closed only if the team explicitly accepts that hooks
will block work on machines without `jq`.

## Safety classification

Every hook is classified by its highest-risk behavior:

- **Advisory** — observes and suggests; never blocks, never writes project files
  or memory (a temp counter at most). Safe to enable first.
- **Blocking** — can stop a tool call (exit 2 / deny). Writes nothing. Enable
  once the rule is trusted.
- **Mutating** — changes files/state. **The kit ships none.** Adding one requires
  explicit opt-in and a README documenting every side effect.
- **Dangerous** — touches external systems, credentials, git history,
  deployments, or production/sensitive data. **The kit ships none and recommends
  against them.**

## Classification of the kit's example hooks

All are **examples, disabled by default**. None is enabled by installing the kit.

| Hook | Class | Notes |
|---|---|---|
| `suggest-card.sh` | Advisory | On edits to `configs/` or `launchers/` with no matching `approved` card: reminds. Never blocks. |
| `frozen-path-warning.sh` | Advisory | On Write/Edit to a frozen-manifest path: warns loudly. Never blocks. |
| `post-results-reminder.sh` | Advisory | When files appear under `results/<ID>/`: reminds to fill the card's Results and the registry row. |
| `smoke-test-reminder.sh` | Advisory | On creating a launcher whose card has no recorded smoke-test pass: reminds. |
| `block-unapproved-launch.sh` | Blocking (opt-in) | Refuses edits to a launcher whose card is not `approved` (or later). |
| `block-frozen-writes.sh` | Blocking (opt-in) | Refuses writes to frozen paths outright. |

No mutating or dangerous hooks are shipped (kit invariant, same as the SDD kit).

## What the hooks deliberately do NOT do

- They never confirm a verdict or declare a gate passed — that is a human gate
  with no hook substitute (`reference/human-in-the-loop-policy.md`).
- They never launch, delete, upload, or mutate anything.
- They never write the card, registry, notebook, or memory.

## Project-specific requirement

Before enabling a hook, Claude must know: the event, the matcher, the command,
whether it blocks, what files it reads, and what false positives are acceptable.
See `settings-snippets.md` for the `.claude/settings.json` wiring.
