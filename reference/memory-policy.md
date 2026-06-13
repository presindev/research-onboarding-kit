# Memory policy

Claude Code has several places where knowledge can persist across sessions. They
differ in scope, visibility, and risk. This policy defines which layer to use for
what, and one non-negotiable rule:

**Claude never writes global memory silently. Every memory write — global or
project — requires explicit researcher approval of the specific entry text.**

(Adapted from the sdd-onboarding-kit; the RDD artifacts replace the SDD ones.)

## Memory layers

| Layer | Location | Scope | Versioned with the repo | Who sees it |
|---|---|---|---|---|
| Global (user) memory | `~/.claude/CLAUDE.md` | All projects of this user | No | Only this user |
| Auto memory | `~/.claude/projects/<project>/memory/` (`MEMORY.md` index + topic files) | One project, one user | No | Only this user |
| Project memory — instructions | `./CLAUDE.md` (team) and `./CLAUDE.local.md` (personal, gitignored) | One project | `CLAUDE.md` yes; `.local` no | Team / only this user |
| Project memory — decision logs | `decisions/` (e.g. `answers.md`, failure-learning entries) | One project | Yes | Team |
| Lab notebook | `notebook/NOTEBOOK.html` | One project | Yes | Team |
| Experiment card | `experiments/E*/card.html` | One experiment | Yes | Team |

Notes:

- **Global memory** is loaded into every session in every project — the most
  expensive and most dangerous layer. A project-specific rule written there
  contaminates unrelated projects. Project-specific rules go to global memory
  only when the researcher explicitly approves exactly that.
- **Auto memory** is project-scoped but lives outside the repo and is not
  reviewed by the team. Under this policy, lessons and decisions that matter go
  to **versioned project artifacts** (decision logs, cards, notebook), not auto
  memory — artifacts survive machine changes, are reviewable, and are shared.
- **Project memory** is the preferred destination. Load-bearing rules belong in
  `CLAUDE.md` (short — see `reference/context-economy.md`); decisions and lessons
  belong in `decisions/`; what-happened narrative in `NOTEBOOK.html`; per-run
  detail in the card.

## What may be stored where

| Kind of knowledge | Correct layer |
|---|---|
| Personal, project-independent preference | Global memory — with approval |
| Reusable project lesson (leaked split, unseeded run, wrong prior) | `decisions/` entry; promote to a `CLAUDE.md` hard rule if load-bearing |
| Methodological/architectural decision | Decision log / ADR |
| One-off finding tied to one experiment | The card / `NOTEBOOK.html` |
| Secrets, credentials, tokens, private endpoints | Nowhere. Never. |
| Sensitive/embargoed data, PII | Nowhere in memory. Reference by ID/hash only. |
| Speculative conclusions not yet confirmed | Nowhere until confirmed |

## Mandatory confirmation before any memory write

Before writing any memory entry (global or project), Claude shows the exact
proposed text and asks:

```text
I found a reusable lesson from this:

<proposed memory entry>

Do you want me to record this?
1. Yes, global memory.
2. Yes, project memory only (decision log).
3. No, keep it only in the card / notebook.
4. Revise the wording first.
```

1. **Global** → append to `~/.claude/CLAUDE.md`; only after this explicit choice,
   and only if genuinely project-independent with no project internals.
2. **Project** (default) → append to a decision log using the failure-learning
   entry format; propose a `CLAUDE.md` hard rule additionally only if load-bearing.
3. **Card/notebook only** → no memory write.
4. **Revise** → rewrite and ask again.

If the researcher does not answer, nothing is written.

## Entry format

Memory entries use `templates/memory/failure-learning-entry.md` (installed by the
`failure-learning` pack): title, date, scope, trigger, what went wrong, root
cause, rule to remember, where to apply, where not to apply, source
card/experiment.

## Security and privacy

- Never store secrets, credentials, tokens, or connection strings in any layer.
- Never store sensitive, embargoed, or personal data — reference datasets by ID
  and hash, never by pasted content (`reference/frozen-artifacts-policy.md`, and
  the data-sensitivity answers in `decisions/answers.md`).
- Never put project-specific rules in global memory unless explicitly approved.
- Anything in `decisions/`, `NOTEBOOK.html`, the cards, or `CLAUDE.md` is visible
  to everyone with repo access — write accordingly.

## Relationship to the failure-learning skill

The optional `failure-learning` pack implements this policy for research mistakes
(wrong prior, leaked split, unseeded run, metric shopping): it drafts the entry,
shows the confirmation prompt, and writes only where the researcher chose. The
advisory hooks may *suggest* running it; they never write memory themselves.

---

Memory locations and commands verified against the Claude Code docs (2026-06):
user memory `~/.claude/CLAUDE.md`; project `CLAUDE.md` / `CLAUDE.local.md`; auto
memory `~/.claude/projects/<project>/memory/` with `MEMORY.md` index; `/memory`
lists and edits memory files; `@path` imports supported.
