# RDD onboarding instructions for Claude Code

You are configuring the current target repository to use **Research Driven
Development (RDD)** with Claude Code.

Your job is to install a project-specific RDD harness. Do **not** run experiments
or implement research features during onboarding unless the researcher explicitly
asks for a separate task after the harness is installed.

## Mandatory read order

Read these before writing any project file:

1. `reference/rdd-theory.md`
2. `reference/research-integrity-policy.md`
3. `reference/reproducibility-policy.md`
4. `reference/human-in-the-loop-policy.md`
5. `reference/compute-budget-policy.md`
6. `reference/frozen-artifacts-policy.md`
7. `questions.md`
8. `output-project-structure.md`
9. `templates/CLAUDE.md.template`
10. `agents/research-lead.md`, `agents/experiment-designer.md`, `agents/analyst.md`,
    `agents/skeptic.md`, `agents/scribe.md`, `agents/literature-scout.md`
11. `skills/research-workflow/SKILL.md` and `skills/research-workflow/workflow.md`
12. `hooks/hooks-policy.md`
13. `mcps/mcp-criteria.md`

If any file is missing, stop and tell the researcher which one.

## Phase 1 — Inspect the target repository

Identify, without changing anything:

- languages, frameworks, environment manager (conda/venv/container), test runner;
- where code runs (local/cluster/cloud) and any scheduler config (SLURM scripts,
  `*.sub`); whether a GPU is available;
- existing experiment tracker (W&B/MLflow/TensorBoard) — config files, `wandb/`;
- existing data layout, dataset sizes, licenses, anything sensitive/embargoed;
- prior baselines/checkpoints, `paper/`, `baseline/`, citations;
- existing `CLAUDE.md`, `.claude/`, `PLAN`, lab notebook, `docs/adr/`;
- existing git branch and cleanliness.

Do not overwrite existing files without reading them first. Draft auto-answers
for the **(auto)** questions.

## Phase 2 — Ask unresolved decisions

Use `questions.md`. Ask only what you cannot infer confidently; group the
questions. If the researcher wants defaults, offer the **Recommended defaults
profile** first and then ask only the project-specific items. Record everything
in `decisions/answers.md`.

## Phase 3 — Generate the project RDD harness

Create or update, in this order:

1. `CLAUDE.md` (from `templates/CLAUDE.md.template`) — concise, project-specific;
   hard rules rendered from answers; link the project map, don't embed a tree.
2. `.claude/context/project-map.md` (from `templates/project-map.md.template`) —
   shallow tree, commands, protected/frozen areas; unknown commands as
   `TODO: ask the researcher`; never record secrets.
3. `PLAN.md` (from `templates/PLAN.md.template`) — or adopt and link an existing
   plan. Offer to draft it from the interview if none exists. Undefined
   evaluation gates become explicit TODO gates.
4. `experiments/registry.json` (from `templates/registry.json.template`) and
   `experiments/registry.html` (from `templates/registry.html.template`); copy
   `templates/assets/research.css` and `research.js` into `experiments/`.
5. `notebook/NOTEBOOK.html` (from `templates/notebook/NOTEBOOK.html.template`);
   copy `research.css`/`research.js` into `notebook/` too.
6. `decisions/answers.md` (filled), plus the decision logs if the `decision-log`
   pack is selected.
7. The core skill: copy `skills/research-workflow/` to
   `.claude/skills/research-workflow/`. Copy the experiment-card, analysis-report,
   config, and launcher templates the skill references into
   `.claude/skills/research-workflow/templates/` (keep `{{PLACEHOLDER}}` tokens —
   they are instantiated per experiment, not now).
8. Selected optional packs: copy `skills/optional/<name>/` to
   `.claude/skills/<name>/`, adapting placeholders. `cluster-ops` is **generated**
   project-specific (real scheduler commands), not copied verbatim — unknowns are
   TODOs.
9. Agents: copy `agents/*.md` to `.claude/agents/`.
10. Hooks: only if approved — copy chosen scripts to `.claude/hooks/` and add the
    entries from `hooks/settings-snippets.md` to `.claude/settings.json`. Confirm
    bash + `jq` are available first.
11. Scripts: copy `scripts/{validate_structure,validate_registry,capture_environment,check_frozen}.py`
    into the project's `scripts/`. If any artifacts are frozen, create
    `data/frozen-manifest.json` and record checksums with `check_frozen.py --write`.

Adapt every file to the project. Do not leave unresolved placeholders (Markdown,
HTML, YAML, JSON) in final project files — except the per-experiment templates
under `.claude/skills/research-workflow/templates/`, which keep their tokens by
design.

Do **not** copy the kit's `experiments/E001_example-*/` reference example into
the target project — it is a rendered reference for humans/agents, not part of
the installed harness.

## Phase 4 — Validate

1. Run `python scripts/validate_structure.py` if safe.
2. Run `python scripts/validate_registry.py` (empty registry is valid).
3. Verify no unresolved placeholders remain (except the skill templates).
4. Verify `CLAUDE.md` points to `.claude/skills/research-workflow/SKILL.md` and to
   `PLAN.md`, the registry, the notebook, and the project map.
5. Verify the HTML artifacts open in a browser (research.css/js paths resolve).
6. Verify frozen artifacts (if any) are recorded and `check_frozen.py` is green.

## Phase 5 — Summary

Report: files created/modified; hooks enabled or left disabled; MCPs configured
or not; project-specific commands detected; open TODOs (undefined gates, unknown
commands, smoke-test definition); and the first prompt to start work.

## Phase 6 — Propose the first card

Propose the first experiment card — usually a **baseline reproduction** — but do
**not** start it without approval (⛔ gate 1).

## Explicit non-goals during onboarding

Do not: run experiments or launch compute; mutate or regenerate data; refactor
the codebase; invent missing metrics, budgets, or scheduler commands; enable
external integrations without approval; commit unless asked.
