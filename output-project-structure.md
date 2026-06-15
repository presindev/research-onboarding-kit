# Expected target-project structure after onboarding

This is what a repository looks like once the RDD harness is installed. Optional
pieces (decision logs, optional packs, hooks) appear only when selected.

```text
target-project/
├── CLAUDE.md                         # concise, project-specific; links out
├── PLAN.md                           # objectives, phases, gates, experiment matrix (canonical, Claude-facing)
├── PLAN.html                         # human-facing twin of PLAN.md (styled; links experiments/research.css)
├── decisions/
│   ├── answers.md                    # recorded onboarding answers
│   ├── architecture-decisions.md     # (if decision-log pack selected)
│   └── rejected-options.md           # (if decision-log pack selected)
├── experiments/
│   ├── research.css  research.js     # shared design system (copied from the kit)
│   ├── registry.json                 # MACHINE STATE — validation source of truth
│   ├── registry.html                 # human-facing dashboard
│   └── E001_<slug>/
│       ├── card.html                 # the experiment card
│       └── analysis-report.html      # (optional, analysis tasks)
├── specs/                            # (only when infra/spec tasks occur)
│   ├── research.css  research.js     # copied so the HTML specs render
│   └── <module>/
│       └── infra-spec.html           # mini-SDD contract + acceptance tests (styled HTML)
├── notebook/
│   ├── research.css  research.js
│   └── NOTEBOOK.html                 # reverse-chronological lab notebook
├── configs/    E001_<slug>.yaml      # one config = one card
├── launchers/  E001_<slug>.sh        # carries ID, output dir, resume, scheduler block
├── results/    E001_<slug>/          # real run outputs (cards reconcile against these)
├── data/
│   └── frozen-manifest.json          # (if any artifacts are frozen)
├── scripts/
│   ├── validate_structure.py
│   ├── validate_registry.py
│   ├── capture_environment.py
│   └── check_frozen.py
└── .claude/
    ├── agents/
    │   ├── research-lead.md  experiment-designer.md  analyst.md
    │   ├── skeptic.md  scribe.md  literature-scout.md
    ├── skills/
    │   ├── research-workflow/        # core skill + supporting docs + templates/
    │   └── <optional packs>/         # only those selected
    ├── context/
    │   └── project-map.md
    ├── hooks/                        # only if hooks approved
    └── settings.json                 # only if hooks/MCPs configured
```

## Format conventions (mirrors the SDD kit's two-tier model)

- **Styled HTML** (shared `research.css`/`research.js`): the experiment cards,
  `registry.html`, `NOTEBOOK.html`, analysis reports, infra-specs, and any other
  human-facing spec/design/proposal doc (generic `doc.html` template). **Every
  document a human is meant to read is styled HTML**, never plain Markdown — copy
  `research.css`/`research.js` next to a new artifact so its link resolves. Open
  them in a browser.
- **Machine state**: `experiments/registry.json` is authoritative for status;
  `validate_registry.py` checks it against the cards and `results/`.
- **Markdown** (Claude-facing operational files only): `CLAUDE.md`, `PLAN.md`,
  skills, agents, decisions, project map. `PLAN.md` is canonical (Claude edits it)
  but also ships a human-facing styled twin, `PLAN.html` — keep the two in sync,
  exactly like the `README.md`/`README.html` pair.
- **Text**: `configs/*.yaml`, `launchers/*.sh`.

## Not installed into the target project

- The kit's rendered reference example (`experiments/E001_example-*/`).
- `templates/`, `reference/`, `hooks/examples/`, `agents/` from the kit root —
  only their adapted copies under `.claude/` and the project tree are installed.
