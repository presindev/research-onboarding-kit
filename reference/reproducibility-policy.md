# Reproducibility policy

A result that cannot be reproduced is a rumor with a number attached. Months
after a run, the question is always the same: *exactly what produced this
figure?* This policy makes that question answerable by construction — every
experiment carries enough provenance to be rerun by someone who was not there.

The standard the kit aims at: **a colleague (or you, in six months) can take a
finished experiment card and reproduce its headline number from the artifacts
alone**, without asking the original author anything. The optional
`reproducibility-audit` pack verifies a card against this standard before a
paper goes out.

## The five provenance requirements

Every experiment records all five. The card template has a slot for each, so a
complete card is a reproducible card.

### 1. Config as spec
One config file fully specifies one experiment (`one config = one card`). Every
knob that affects the result lives in the config, not in ad-hoc command-line
edits or notebook cells. The config is versioned and its path is on the card.
Re-running the experiment means re-running that config — nothing is "obvious" or
"left at the default in my shell".

### 2. Seeds recorded
Every source of randomness is seeded and the seeds are written on the card
(data shuffling, init, augmentation, dropout, sampling). Multi-seed experiments
record all seeds. "Set the seed" includes the framework-specific incantations
(e.g. Python/NumPy/torch/CUDA determinism flags) — record what you actually set,
and note known nondeterminism that no seed removes (e.g. some GPU kernels).

### 3. Environment captured per run
Each run snapshots its environment with `scripts/capture_environment.py`:
interpreter version, package versions (pip freeze / conda export / lockfile),
container image digest if used, GPU/driver/CUDA versions, and the **git SHA** of
the code that ran. The snapshot is an artifact referenced by the card, not a
sentence in the notebook. A dirty working tree at launch is recorded as such.

### 4. Data referenced by hash or version
Datasets are identified by content hash or an explicit version (DVC, dated
release, manifest), never by a bare path that might point at different bytes
next month. The card lists the dataset IDs and checksums it consumed. See
`reference/frozen-artifacts-policy.md` for the artifacts that must never change
once frozen, and the `data-provenance` pack for dataset cards.

### 5. Figures regenerable by a named script
Every published figure names the script that generated it and the inputs
(card IDs / result files) it consumed. No figure is hand-edited into existence;
re-running its script on the same inputs reproduces it. The `figure-style` and
`paper-trail` packs formalize this for write-up.

## Resumability (the compute-side of reproducibility)

Long jobs are **designed to resume**: they checkpoint and accept a `--resume`
flag, so a preempted or crashed run continues rather than restarting. This is
both a compute-budget rule (`reference/compute-budget-policy.md`) and a
reproducibility rule — a run that can resume from a checkpoint can also be
*restarted from* that checkpoint to verify a later stage. The launcher template
carries the checkpoint/output-dir/resume convention.

## Checklist (used by `reproducibility-audit`)

A card passes the reproducibility bar when:

- [ ] One config file fully specifies the run; its path is on the card.
- [ ] All seeds are recorded; determinism flags noted; residual nondeterminism stated.
- [ ] An environment snapshot exists for the run and is referenced (incl. git SHA).
- [ ] Every dataset is referenced by hash/version; frozen inputs verified with `check_frozen.py`.
- [ ] Every figure names its generating script and inputs, and regenerates from them.
- [ ] The run is resumable from its last checkpoint (or the card states why not).

## Boundaries

- Reproducibility ≠ determinism. Some experiments are inherently stochastic; the
  requirement is that the *distribution* is reproducible (seeds + N runs +
  reported variance), not that one bit-identical number returns.
- Capturing the environment never captures secrets: tokens, credentials, and
  private endpoints are excluded from snapshots; environment variables are
  recorded by name, never value (see `reference/memory-policy.md`).
- The policy records provenance; it does not by itself rerun anything expensive
  — reruns spend compute and are human-gated like any launch.
