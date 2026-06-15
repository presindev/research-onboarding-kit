# The experiment loop (full procedure)

This is the operational detail behind `SKILL.md`. The ⛔ marks are the two human
gates. Steps 4–8 are the experiment path; infrastructure and analysis tasks
branch at step 1.

## 1. Classify the task

Use `classification-policy.md`.

- **Infrastructure** (pipeline, library, eval code, data loader): take the
  mini-SDD path — write an `infra-spec` (styled HTML,
  `templates/infra-spec.html.template`: contract + acceptance tests) before
  code; tests must pass before `done`. Not the rest of this loop.
- **Analysis / writing**: produce an analysis report whose every number cites a
  card or dataset ID. Not gated on the experiment loop — reading and plotting
  stay friction-free.
- **Experiment**: continue below.

## 2. Draft the experiment card

From `templates/experiment-card.html.template` (see `experiment-card-format.md`).
Fill: hypothesis, **exactly one** change under test, baseline, metrics + gate
criteria, compute budget, artifacts to be produced.

- If `PLAN.md` exists, the card must reference its phase/row (`plan-ref`). A card
  that doesn't fit the plan is a **plan-change proposal**, not a card — raise it
  with the researcher.
- The `experiment-designer` agent refuses a card with more than one change under
  test or with undeclared metrics.
- Create the registry record (`status: draft`) and the experiment folder.

## 3. ⛔ Researcher approves the card

No config, launcher, or run before approval. Approval covers the single change,
the declared gate criteria, and the compute budget. On approval, set
`status: approved` in the card and registry; the metrics/gate are now frozen for
this run (changing them later needs a dated decision —
`reference/research-integrity-policy.md`).

A blocking hook (`block-unapproved-launch.sh`) is available; advisory by default.

## 4. Implement run artifacts

- **Config** (`configs/<ID>.yaml`) — the machine-readable spec; one config = one
  card. Every result-affecting knob lives here.
- **Launcher** (`launchers/<ID>.sh`) — carries the ID, output dir, resume flag,
  and scheduler block.
- **Smoke test** — the smallest run proving the job won't crash. It **must pass
  on the local machine** before anything is queued. Record the command and pass
  date on the card and set `smoke_passed` in the registry.

If the project hasn't defined a smoke test, that's a TODO gate: cluster
submissions are blocked until it's defined (`reference/compute-budget-policy.md`).

## 5. Launch

- If Claude can run it locally within the stated budget, it may
  (`reference/human-in-the-loop-policy.md`).
- If it needs the cluster, money, or the human, Claude hands over the **exact
  submission command** and expected output artifacts (the `cluster-ops` pack
  holds the project recipe), sets `status: launched`, and **waits**. No
  fabricated results; no "expected" numbers written into the card.

## 6. Collect & analyze

When results exist (check `results/<ID>/`):

- Verify outputs against the card's declared metrics, including sanity /
  calibration / seed-variance checks.
- Run the **skeptic** (`skeptic-checklist.md`) — it tries to *refute* the verdict
  before it is proposed: stats validity, calibration, leakage, baseline
  fairness, claim–artifact traceability.
- Fill the card's **Results** section from real outputs. Log failures and
  negative results with the same discipline as wins; set `status: analyzed`.

## 7. ⛔ Verdict confirmed

Claude proposes the verdict against the gate (pass / fail / inconclusive); the
researcher (or named approver) confirms. Only a confirmed verdict updates the
plan gate and may propose a decision-log entry. Claude never declares a gate
passed on its own.

## 8. Scribe updates

- Append a dated `NOTEBOOK.html` entry (what ran, what happened, what's next).
- Update the registry row (status, gate_result, actual_cost).
- A card is not `done` while its artifacts (plots, metrics files) are missing or
  its registry row is stale.
- If the `paper-draft` pack is installed, **append an experiment subsection** to
  `paper/sections/experiments.tex` for the just-confirmed verdict — the single
  change under test and the result, numbers taken only from `results/<ID>/` and
  citing the card. Negative/inconclusive results are written too.

## Paper write-up (if the `paper-draft` pack is installed)

The paper in `paper/` grows with the work, not at the end (see the `paper-draft`
skill). Beyond the per-experiment subsection above: draft the introduction and
related-work after the literature review (with the references the `literature-scout`
found), the methodology once `PLAN.md` fixes the metrics and gates, and aggregate
`results.tex` as confirmed experiments accumulate. Every number cites a confirmed
card (`paper-trail`); the author commits each claim
(`reference/human-in-the-loop-policy.md`).

## Iteration rule

A new experiment varying the same axis gets a **new card**
(`E12_<slug>__v2`, with `supersedes: E12_<slug>`). Editing a completed card's
design section is forbidden; corrections append.

## Hand-over format (cross-session sync)

When handing a job to the human, give: (1) the exact command, (2) the files/dir
the run will produce, (3) what to paste back (job ID, or "done"). The `launched`
status is the synchronization point — on the next session, reconcile against
`results/` (`reference/session-recovery.md`).
