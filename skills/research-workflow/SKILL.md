---
name: research-workflow
description: Run the Research Driven Development (RDD) experiment loop for Claude Code. Use when starting, designing, launching, or analyzing an experiment, or when the project CLAUDE.md says a task follows RDD.
argument-hint: "[experiment-id-or-task-description]"
---

# RDD Workflow Skill

Use this skill when the researcher asks to work through an experiment, or when the
project `CLAUDE.md` says a task follows RDD. The central artifact is the
**experiment card**; the loop has two human gates (⛔).

## Required supporting files

Read the relevant file before acting:

- `workflow.md` — the full experiment loop, step by step.
- `classification-policy.md` — decide infrastructure / experiment / analysis.
- `experiment-state-machine.md` — card statuses and transitions.
- `experiment-card-format.md` — when drafting or editing a card.
- `skeptic-checklist.md` — when verifying results before proposing a verdict.
- `examples.md` — when an output example is needed.

## Core rules

1. **Classify first.** Infrastructure → mini-SDD path (`infra-spec` + tests).
   Experiment → this loop. Analysis/writing → cited report.
2. **No config, launcher, or run before the card is approved (⛔ gate 1).**
3. **Smoke test must pass locally before any expensive/cluster launch.**
4. **Results are filled only from real outputs.** No fabricated or "expected"
   numbers. Every run logged, including failures and negatives.
5. **Claude proposes the verdict; the researcher confirms it (⛔ gate 2).** Claude
   never declares a plan gate passed.

## Standard execution

1. Identify the task / experiment (`$ARGUMENTS`).
2. Classify it (`classification-policy.md`).
3. For an experiment: draft the card from the template (`experiment-card-format.md`).
4. ⛔ Stop for card approval.
5. After approval: build config + launcher + smoke test; run the smoke test.
6. Launch (cheap-local within budget) or hand over to the human (cluster/paid);
   set status `launched`; wait — do not fabricate results.
7. When results return: verify against the declared gate; run the skeptic
   (`skeptic-checklist.md`); fill Results; propose a verdict.
8. ⛔ Stop for verdict confirmation.
9. Scribe updates the notebook and registry; mark `done` only when artifacts
   exist and the registry row is current.

## Argument

Use `$ARGUMENTS` as the experiment ID, card slug, or task description. If empty,
select the next eligible card from `experiments/registry.json` (e.g. an
`approved` card awaiting launch, or a `launched` card whose `results/` now has
outputs).

## State lives in artifacts

`experiments/registry.json` is the source of truth for status; the card carries
the detail; `notebook/NOTEBOOK.html` carries the narrative. After any
resume/compaction, reconcile the registry and cards against `results/` before
continuing — artifacts win (`reference/session-recovery.md`).
