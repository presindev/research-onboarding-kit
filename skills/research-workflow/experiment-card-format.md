# Experiment card format

How to fill `templates/experiment-card.html.template`. The card is the central
artifact: heavier than a chat message, lighter than an SDD spec. Resist adding
traceability matrices — card + registry + notebook are enough for a research
cadence.

## Placeholders and what goes in them

| Placeholder | Fill with |
|---|---|
| `{{ID}}` | `E<seq>_<slug>`, matching config/launcher/results/registry |
| `{{TITLE}}` | short human title |
| `{{PLAN_REF}}` | `PLAN.md §<phase>` this card serves |
| `{{SUPERSEDES_OR_NONE}}` | ID this replaces, or `none` |
| `{{APPROVER}}` | who confirms the card and the verdict (from `decisions/answers.md`) |
| `{{HYPOTHESIS}}` | the question/claim being tested |
| `{{SINGLE_CHANGE}}` | **exactly one** change vs. baseline; if you need two, split the card |
| `{{BASELINE_…}}` | a card ID or named reference result |
| Setup fields | config path, launcher path, git SHA, dataset IDs+checksums, frozen IDs, env-capture ref, seeds, budget, smoke command + pass date |
| `{{METRIC_ID}}` / `{{GATE_CRITERION}}` | declared **before** launch; frozen at approval |
| Results | filled **only** from real outputs; link `results/<ID>/` artifacts |
| Skeptic / frozen notes | see `skeptic-checklist.md` |
| Verdict | proposed by Claude, confirmed by the approver |

## Hard rules the format encodes

1. **One change under test.** The `experiment-designer` refuses cards that
   violate this.
2. **Metrics and gate declared before launch.** They live in the card at
   `approved` and are frozen for the run; later changes require a dated decision.
3. **Results from real outputs only.** Never pre-fill "expected" numbers; never
   fill Results before the run returns.
4. **Append, don't overwrite.** After approval, the design sections are
   append-only; corrections append; a new axis is a new card.

## Keeping the card and registry in sync

When a status changes, update **both** the card's status badge and the
`experiments/registry.json` record (status, gate_result, smoke_passed,
actual_cost). `registry.json` is authoritative; `validate_registry.py` checks
the two agree and that `results/<ID>/` matches the claimed status.

## Assets

The card links `../research.css` and `../research.js` (one shared copy per
`experiments/` tree). Keep that relative path correct for the installed layout.
