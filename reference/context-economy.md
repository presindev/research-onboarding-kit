# Context economy

Claude Code's context window is a scarce, shared resource. Everything loaded into
a session — project instructions, file contents, tool definitions, conversation
history — competes for the same space. When the window fills up, quality degrades
before capacity runs out: instructions get diluted, earlier decisions fade, and
the model starts re-deriving things it already knew.

This kit treats context management as one explicit policy. (Adapted from the
sdd-onboarding-kit; the practices are identical, the artifacts are the RDD ones.)

## The principle

Load the minimum context needed for the current step, keep durable knowledge in
files instead of chat history, and reset between unrelated tasks.

## Practices

### Keep `CLAUDE.md` concise and linked

`CLAUDE.md` is loaded into every session, so every line has a permanent cost.

- Keep it to stable facts and short rules: commands, the hard rules (frozen
  list, one-change rule, gates), locations, working style.
- Link to deeper files (`reference/`, skills, project map, `PLAN.md`, decision
  logs) instead of copying their content.
- Move any multi-step procedure into the `research-workflow` skill. A skill's
  body loads only when used; `CLAUDE.md` content is always loaded.
- If a section grows past a screen, it belongs in a linked file.

### Inspect usage with `/context`

`/context` visualizes current usage and flags context-heavy tools and memory
bloat. Use it when a session has run long and behavior is degrading, when
deciding whether to compact or start fresh, or to audit whether `CLAUDE.md`,
MCP toolsets, or large result/log files are consuming the window.

### Compact between unrelated tasks with `/compact`

`/compact` frees context by summarizing the conversation so far. Use it between
unrelated experiments, after a noisy analysis or log triage, or when `/context`
shows the window filling.

Prefer **selective compacting**: `/compact` accepts focus instructions. When
compacting mid-experiment, instruct it to preserve:

- the approved card's hypothesis, single change under test, and declared gate;
- current card status (`draft`/`approved`/`launched`/…) and next steps;
- constraints discovered (data quirks, leakage risks, env gotchas);
- unresolved questions.

```text
/compact Preserve: E012's approved gate (ECE down ≥20%, accuracy within 0.5pt),
that it is launched on SLURM job 4417291 awaiting results, the constraint that
val_frozen_v2 must not be reshuffled, and the open question about seed variance.
```

In an RDD project, compaction is safe because durable truth lives in files
(`experiments/registry.json`, the cards, `NOTEBOOK.html`, decision logs), not in
chat. If something matters beyond the session, write it to an artifact before
compacting.

### Use subagents for noisy research

Exploration that reads many files or long outputs — locating code, surveying a
results directory, triaging training logs, scanning a dataset — pollutes the main
context with content only needed to produce a short conclusion. Delegate it to a
subagent and keep only the conclusion. The `literature-scout` and `skeptic`
agents are read-only by design for exactly this reason.

### Use skills for repeatable long procedures

The experiment loop, the reproducibility audit, the cluster hand-over — these are
versioned skills, loaded only when invoked, not pasted into `CLAUDE.md`.

### Avoid loading MCP-heavy toolsets unless needed

Every configured MCP server adds tool definitions to every session. Configure
MCPs per project and only when needed (e.g. a paper-search or experiment-tracker
MCP); prefer scoping heavy toolsets to a dedicated subagent. See
`mcps/mcp-criteria.md`.

## Good vs bad context loading

| Situation | Bad (context-expensive) | Good (context-economical) |
|---|---|---|
| Project orientation | Paste the tree and ten files into chat | Link the project map from `CLAUDE.md` |
| The experiment loop | Copy the full workflow into `CLAUDE.md` | Keep it in the `research-workflow` skill |
| Triaging a long run log | Read the whole log in the main session | Subagent summarizes; returns the failure + line refs |
| Task switch | Continue in the same long session | `/compact` (or `/clear` if truly unrelated) |
| External tools | Enable every MCP globally | Configure per project, scope heavy ones to subagents |
| Past decisions | Rely on chat history | Record in decision logs / cards, link from `CLAUDE.md` |

## Where durable context lives in an RDD project

| Kind of knowledge | Artifact |
|---|---|
| Stable rules and commands | `CLAUDE.md` (short, linked) |
| Plan, phases, gates | `PLAN.md` |
| Experiment state | `experiments/registry.json` |
| Per-experiment hypothesis/design/results | `experiments/E*/card.html` |
| Decisions and rejected options | decision logs (`decisions/`) |
| Running history | `notebook/NOTEBOOK.html` |
| Procedures | `.claude/skills/` |

Command names verified against the Claude Code commands reference (2026-06):
`/context [all]`, `/compact [instructions]`.
