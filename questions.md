# RDD onboarding questions

Ask these **before** writing any project file, and record the answers in
`decisions/answers.md`. Group them into one or two `AskUserQuestion` rounds; use
free text where options don't fit. Questions marked **(auto)** should first be
answered by inspecting the repository and only confirmed with the researcher.

If the researcher wants a default recommendation, offer the **Recommended
defaults profile** below as a single question first; if accepted, ask only the
genuinely project-specific items (domain & goal §A1, commands & compute §C,
data & frozen artifacts §D, evaluation gate & smoke test §E, and any flagged
deviations).

---

## Recommended defaults profile

Offer this first. If accepted, most of §F is set automatically.

```yaml
work_types: [infrastructure, experiment, analysis]   # all three installed
human_gates: card_approval + verdict_confirmation     # both ⛔ required
local_first: true                                     # no external MCP/CLI required
experiment_tracker: complement_existing_or_none       # registry never replaces W&B/MLflow
id_convention: "E<seq>_<slug>"
registry_state: experiments/registry.json             # source of truth
artifacts: html_via_research_css                       # cards/registry/notebook/report styled
hooks_profile: advisory_only_disabled_until_approved
blocking_hooks: available_opt_in                       # launch-approval + frozen-writes
frozen_artifacts_policy: required                      # manifest + check_frozen
smoke_test_required_before_cluster: true
every_run_logged: true                                 # failures + negatives included
compute_gate: ask_before_expensive_or_paid_runs
memory_scope: project_default_global_only_with_explicit_approval
autonomy: disabled_except_documented_readonly_monitoring
language_artifacts: project_language                   # kit files stay English
optional_packs: recommend_per_answers                  # see §F16
```

---

## A. Project identity

1. Research domain and a one-sentence goal of the project.
2. Is there a prior publication/baseline this continues? Where does it live
   (paper sources, reference code, checkpoints)? **(auto: look for `paper/`,
   `baseline/`, checkpoints, citations in README)**
3. Publication target and rough timeline (journal/conference/thesis/internal)?

## B. People and approval

4. Solo or team? Who approves what — supervisor sign-off on gates? co-author
   review of cards? (Sets the `approver` on cards and the verdict gate.)
5. Default language for generated artifacts (kit files stay English)?

## C. Technical stack **(auto where possible)**

6. Languages, frameworks, environments (conda/venv/containers), test runner.
   **(auto: `environment.yml`, `requirements.txt`, `pyproject.toml`, lockfiles)**
7. Where does code run: local only / cluster (which scheduler — SLURM, HTCondor,
   …) / cloud / mixed? Does Claude's machine have a GPU? Who launches long jobs?
8. Experiment tracking already in use (W&B, MLflow, TensorBoard, none)? The kit's
   registry **complements, never replaces**, an existing tracker.

## D. Data

9. Data sources, sizes, licenses/sensitivity (PII? embargoed collaboration data?
   open?). Anything Claude must **never** upload, print, or commit?
10. Which artifacts must be **frozen** (eval sets, benchmark splits, reference
    checkpoints)? These go in `data/frozen-manifest.json`.
11. Data versioning convention (DVC, content hashes, dated filenames, none yet)?

## E. Experiments and evaluation

12. What are the project's evaluation metrics, and what counts as a pass/gate for
    an experiment? *(If unknown, install the question into `PLAN.md` as a TODO
    gate — the reviewer blocks dependent experiments until it's defined.)*
13. Compute budget per experiment (GPU-hours, walltime, queue limits) and per
    month.
14. Smoke-test policy: the smallest run that proves a job won't crash (e.g.
    100-sample overfit on CPU)? *(If unknown, record a TODO; cluster submissions
    are blocked until defined.)*
15. Naming convention for experiments (default `E<seq>_<slug>`; configs and
    launchers carry the same ID).

## F. Harness scope

16. Which optional packs to install (see `skills/optional/README.md`)? Recommend
    defaults based on answers:
    - cluster → `cluster-ops`;
    - paper target → `paper-draft` + `paper-trail` + `literature-watch`;
    - team → `decision-log` (recommended always);
    - data with licenses/sensitivity → `data-provenance`;
    - before-submission → `reproducibility-audit`;
    - plots in the paper → `figure-style`;
    - `experiment-registry` recommended for every project.
17. Hooks: none / advisory only / advisory + blocking (default: advisory only,
    disabled until approved). Confirm the team has bash + `jq` before enabling.
18. Any existing conventions (lab notebook, ADRs, style guides) the kit must
    adopt instead of its own templates? **(auto: look for `docs/`, `notebooks/`,
    `adr/`, an existing `NOTEBOOK`)**

---

## What Claude must NOT assume

- Whether every task uses RDD (vs. the infra/analysis paths).
- The evaluation metric or what counts as a passed gate.
- The smoke-test definition.
- Compute budgets, scheduler commands, partitions, or module loads.
- Which artifacts are frozen, or what data is sensitive.
- Which optional packs to install, or whether hooks are enabled.
- Whether autonomous monitoring beyond read-only is allowed.

If a decision is missing, ask. Unknowns become explicit TODOs, never invented
values.
