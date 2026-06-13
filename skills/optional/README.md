# Optional skill packs

Source templates for optional, per-project skills. The core RDD behavior lives in
`skills/research-workflow/` and is always installed; the packs here are installed
**only when the researcher selects them** during onboarding (`questions.md` §16)
or asks for them later.

## Installation rule

For each selected pack, copy `skills/optional/<name>/` to `.claude/skills/<name>/`
and adapt placeholders and project-specific details. Record installed and
declined packs in `decisions/answers.md`. Do not install unselected packs "just
in case", and do not paste skill bodies into `CLAUDE.md` — list installed skills
there by name with a one-line purpose at most. Skill bodies load only when
invoked, which keeps them cheap (`reference/context-economy.md`).

`cluster-ops` is **generated** project-specific (real scheduler commands), not
copied verbatim — unknown values become TODOs, never invented.

## Available packs

| Skill | Purpose | Recommended when |
|---|---|---|
| `experiment-registry` | Registry maintenance, ID/superseding conventions, `validate_registry` wiring | Every project |
| `reproducibility-audit` | Verify a finished card can be rerun before a paper goes out | Paper target |
| `cluster-ops` | The project's real scheduler recipe + hand-over format | Cluster compute |
| `literature-watch` | Periodic novelty / related-work sweep procedure | Paper target |
| `paper-trail` | Claim→card→artifact table, figure provenance, reproducibility statement | Write-up phase |
| `data-provenance` | Dataset cards (origin, license, hashes, sensitivity); update procedure | Licensed/sensitive data |
| `decision-log` | Record durable methodological/workflow decisions | Team (always) |
| `failure-learning` | Turn real mistakes into reusable lessons (proposed, never auto-written) | Recommended |
| `git-discipline` | Clean branches/commits/PRs without risky git actions | Any git project |
| `figure-style` | Consistent, regenerable plotting conventions for the target venue | Paper figures |

Every pack documents: purpose, when to use, when not to use, required inputs,
output artifact, and safety constraints. All packs are advisory or
permission-gated: none mutates external systems, compute, or memory without
explicit researcher approval, and none crosses an RDD gate.
