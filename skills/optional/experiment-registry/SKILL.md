---
name: experiment-registry
description: Maintain experiments/registry.json and registry.html, the ID/superseding conventions, and the validate_registry wiring. Use when registering, updating, or auditing experiments.
---

# Experiment registry

## Purpose

Keep `experiments/registry.json` (the machine-readable source of truth) and
`experiments/registry.html` (the human dashboard) accurate and consistent with
the cards and `results/` directories.

## When to use

- Registering a new experiment (a card moves to `draft`).
- Updating a record on any status change (approved/launched/analyzed/done/failed).
- Auditing consistency, or reconciling after time away.

## When not to use

- As a substitute for an existing experiment tracker (W&B/MLflow) — the registry
  *complements* it; it does not replace run-level logging.

## ID & superseding conventions

- IDs follow `E<seq>_<slug>` (or the project convention in `decisions/answers.md`);
  the same ID is used on the card, config, launcher, `results/`, and the record.
- A re-run varying the same axis gets a **new** record (`E12_<slug>__v2`) with
  `supersedes` set to the original. Completed cards are not edited.

## Procedure

1. On a status change, update **both** the card's status badge and the
   `registry.json` record (status, gate_result, smoke_passed, actual_cost,
   code_version), and reflect it in `registry.html`.
2. Run `python scripts/validate_registry.py`; fix or flag every reported
   inconsistency.
3. Reconcile `launched` records against `results/<ID>/` — artifacts win
   (`reference/session-recovery.md`).
4. Keep the schema in `templates/experiments/README.md`; don't add fields ad hoc.

## Output artifact

An updated `registry.json` + `registry.html`, validated green.

## Safety constraints

- Never fabricate a record for a run that didn't happen.
- Never mark `done` while results are missing or the gate is `pending`.
- The registry records state; it never confirms a verdict (that's the human gate).
