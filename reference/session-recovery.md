# Session recovery

Sessions get interrupted, go stale, or go wrong: days pass between working
sessions, compaction summarizes away details, a run launched last week finally
returns, or Claude heads in a wrong direction for several turns. Claude Code
ships features for all of these — and one rule keeps them safe in an RDD project:

> **Durable artifacts are the source of truth, never chat history.**
> `experiments/registry.json` holds experiment state, the cards hold
> hypotheses/designs/results, the decision logs hold settled decisions,
> `NOTEBOOK.html` holds what happened, and the `results/` directories hold what
> actually came back from runs. A summary, restored checkpoint, or resumed
> conversation is a convenience for reorienting — anything it claims is verified
> against the artifacts before acting on it.

(Adapted from the sdd-onboarding-kit; the RDD addition is the
reconcile-against-`results/` rule, because runs complete outside the session.)

## Feature landscape

(Names verified against the official docs on 2026-06-12 — re-verify before
relying on syntax.)

- **Recap** — `/recap` summarizes the session; an automatic recap appears after
  time away. Orientation only.
- **Rewind / checkpoints** — `/rewind` restores conversation, code, or both.
  **It tracks only Claude's direct file edits** — not bash side effects, not
  manual edits, and crucially **not external run state**: a job you launched is
  still running (or done) regardless of any rewind. Local undo, not version
  control.
- **Resume** — `claude --continue` / `--resume` reopen sessions; per machine and
  per directory, they do not sync across machines.
- **Branching** — `/branch` copies the conversation to try an alternative.
- **Compaction** — `/compact [focus]` replaces history with a summary;
  `CLAUDE.md` and memory reload from disk and survive.
- **Stopping** — Esc stops the current turn; work so far is kept.
- **Transcripts** — full logs under `~/.claude/projects/` (default 30-day);
  `/export` saves a session.

## The four practices

### 1. Reorient with recap — then verify against artifacts

After days away: read the recap, then open the durable artifacts before doing
anything: `registry.json` for every experiment's actual status, the active card
for what was approved and what the declared gate is, `NOTEBOOK.html` for what was
done, the decision logs for what was settled. The recap says where to look; the
artifacts say what is true. On disagreement, the artifacts win.

### 2. Reconcile against `results/` — the RDD-specific step

Because runs complete **outside the session**, the conversation can be hours or
days behind reality. After any resume or compaction, before continuing:

- For every card marked `launched`, check whether its `results/<ID>/` directory
  now has outputs. If results arrived, the card is really ready for analysis even
  if the chat still says "waiting".
- A run may have **failed** while you were away — check logs/exit status, don't
  assume success.
- `validate_registry.py` flags cards whose status disagrees with their
  `results/` directory. **Artifacts win**: update the card and registry to match
  what the filesystem shows, then continue.

### 3. Rewind when Claude went the wrong way

When several turns went down a wrong path, rewinding beats arguing the session
back on course. But check what rewind cannot restore: bash side effects, manual
edits, and **external run state** — a launched job, a deleted file, a mutated
dataset — survive the rewind. `git status` and a look at `results/` after
rewinding tell you what actually changed.

### 4. Rely on durable artifacts as truth

- **Reading:** after any resume/rewind/compaction, state is read from
  `registry.json`, the cards, reviews-by-skeptic notes, decision logs,
  `NOTEBOOK.html`, and `results/` — not assumed from a stale conversation.
- **Writing:** verdicts, status changes, gate decisions, and constraints are
  written to those artifacts *when they happen*, so losing a session loses
  nothing that matters.

## Resume checklist

1. `registry.json` — status of the experiment you think you are on, and any card
   marked `launched` or `analyzed`.
2. For each `launched` card — does `results/<ID>/` have outputs now? Did it fail?
3. The active card — hypothesis, single change, and **declared gate** as
   approved, not as remembered.
4. `git status` and the current diff — what is actually changed but uncommitted.
5. Decision logs / `NOTEBOOK.html` — decisions and events since the context you
   remember.

If conversation memory and any of these disagree, trust the artifact and say so
explicitly before continuing.

## RDD constraints

- Rewind and resume never change experiment state by themselves: a card that was
  `launched` before a rewind is still `launched`, and its real outcome is
  whatever `results/` and the registry show.
- Restored context does not revive an expired approval: if a card's design
  changed after the restored checkpoint, the card on disk is authoritative, and
  approval status is whatever the registry says.
- A run that completed during the gap is not "undone" by a rewind — recover its
  outcome from `results/` and git, not from the conversation.
- Recovery features are session conveniences, not audit trails — the durable
  artifacts and git history remain the record (see also
  `reference/autonomy-policy.md` for runs nobody watches).
