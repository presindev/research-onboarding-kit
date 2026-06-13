# Frozen-artifacts policy

Some artifacts must not change once created, because results are compared
*against* them across many experiments: evaluation sets, benchmark splits,
reference checkpoints, held-out test data. If one of these silently mutates —
a split reshuffled, a few labels "cleaned", a test file regenerated — every
result that used it becomes incomparable, and the corruption is usually
discovered long after the experiments that depended on it. Freezing turns these
artifacts into fixed reference points whose integrity is checkable.

This policy defines what freezing means, how the manifest works, and what the
tooling and hooks do with it.

## What "frozen" means

A frozen artifact is **generated once, checksummed, and never mutated**.

- It is created deliberately (a held-out split is drawn with a recorded seed; a
  reference checkpoint is saved), its checksum is recorded in the manifest, and
  from then on it is read-only in spirit and verified in practice.
- It is **never** edited, reshuffled, re-cleaned, appended to, or regenerated in
  place. "Just fixing a few labels" in a frozen eval set is the exact failure
  this policy prevents.
- A replacement is a **new artifact with a new name and a new manifest entry**,
  accompanied by a dated decision (`decisions/`) explaining why the old one was
  retired and what changed. Old results remain attributed to the old artifact;
  they are not silently re-pointed at the new one.

## The manifest

Frozen artifacts are listed in a manifest file (default
`data/frozen-manifest.json`, location confirmed during onboarding). It is the
single source of truth consumed by `scripts/check_frozen.py` and by the frozen
hooks. Each entry records identity and integrity:

```json
{
  "frozen": [
    {
      "id": "val_frozen_v2",
      "path": "data/eval/val_frozen_v2/",
      "kind": "eval-split",
      "checksum": "sha256:…",
      "created": "2026-05-30",
      "created_by": "E007_make-eval-split",
      "seed": 1337,
      "note": "Held-out validation split; never reshuffle. Supersedes val_frozen_v1 (label noise, see decisions/)."
    }
  ]
}
```

- `checksum` is a content hash (directory checksums hash the sorted file
  contents, not timestamps). `check_frozen.py` recomputes and compares.
- `kind` is free-form but conventional: `eval-split`, `test-set`,
  `reference-checkpoint`, `benchmark`, `fixed-config`.
- A retired artifact stays in the manifest with a `retired` date rather than
  being deleted from it, so its checksum history is preserved.

## Tooling and hooks

- **`scripts/check_frozen.py`** — recomputes checksums for every manifest entry
  and reports any mismatch (corruption or accidental mutation) or any missing
  file. Run it before trusting an evaluation, and in the
  `reproducibility-audit`. A mismatch is a stop-and-investigate event.
- **`frozen-path-warning.sh`** (advisory, default) — warns loudly when a
  Write/Edit targets a path under the manifest.
- **`block-frozen-writes.sh`** (blocking, opt-in) — refuses writes to frozen
  paths outright.

Hooks are advisory by default and disabled until configured; the policy holds
whether or not a hook is enforcing it (see `hooks/hooks-policy.md`).

## In the experiment loop

- A card lists the frozen artifacts it consumed by `id`; the verdict is only
  trustworthy if `check_frozen.py` was green for those IDs at run time.
- Creating a frozen artifact is itself an experiment-or-infrastructure task with
  its own card/spec (it has a seed, a config, and outputs) — so the split's
  provenance is reproducible (`reference/reproducibility-policy.md`).
- Evaluation never trains on, tunes against, or peeks at a frozen test set;
  doing so is leakage, caught by the skeptic and the integrity policy.

## Boundaries

- Freezing protects *reference* artifacts, not working data — training inputs,
  scratch outputs, and intermediate caches are not frozen and change freely.
- The manifest stores checksums and paths, never the data itself and never
  secrets.
- Deleting or regenerating any frozen artifact is human-gated and requires a
  recorded decision — it is on the "must ask" list in
  `reference/human-in-the-loop-policy.md`.
