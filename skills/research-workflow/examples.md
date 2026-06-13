# Examples

Short worked examples of the loop. Illustrative — adapt to the project.

## Example 1 — a clean experiment

> Researcher: "Try freezing the encoder and see if calibration improves."

1. **Classify** → experiment (one change, a metric, a baseline).
2. **Draft card** `E012_frozen-encoder`: hypothesis (freezing improves OOD
   calibration without hurting accuracy); change = `encoder.requires_grad=False`,
   all else as `E011`; baseline = `E011`; metrics M-ACC, M-ECE; gate = "ECE down
   ≥20% relative AND accuracy within 0.5pt". Registry record `status: draft`.
3. ⛔ Researcher approves → `status: approved`, gate frozen.
4. Build `configs/E012_frozen-encoder.yaml`, `launchers/E012_frozen-encoder.sh`,
   smoke test (100-sample CPU overfit) → passes → record `smoke_passed`.
5. Cluster job → hand over `sbatch launchers/E012_frozen-encoder.sh`; researcher
   pastes back job ID; `status: launched`; **wait**.
6. Results return in `results/E012_frozen-encoder/`. Verify vs gate. Skeptic:
   "only 1 seed — variance unverified" → **blocking** → run 3 seeds. Re-verify.
   Fill Results; `status: analyzed`.
7. ⛔ Propose verdict: "PASS on calibration, accuracy held; robustness regressed —
   inconclusive overall, recommend follow-up." Researcher confirms.
8. Scribe: notebook entry + registry row (gate_result, actual_cost). `status: done`.

## Example 2 — classification catches plumbing

> Researcher: "Make a clean held-out validation split."

→ **Infrastructure**, not an experiment: write an `infra-spec` (contract: input
data → split with recorded seed; acceptance tests: sizes, no overlap,
determinism), implement, tests pass. Then register the split in the frozen
manifest with its checksum (`reference/frozen-artifacts-policy.md`). No card.

## Example 3 — a negative result is still a result

> A run underperforms the baseline.

The card records the real numbers and a `fail`/negative verdict; it is **not**
deleted or silently re-run until a seed "works". The notebook logs it; if it
settles something ("approach X doesn't help here"), propose a
`rejected-options.md` entry. This is the anti-p-hacking rule in action.

## Example 4 — the human runs the job, days pass

After resuming a session: a card is `launched`. Check `results/E012/` — outputs
are there now (the run finished while away). Reconcile: the card is really ready
for analysis even though the chat said "waiting". `validate_registry.py` would
flag the mismatch. Artifacts win — proceed to step 6
(`reference/session-recovery.md`).
