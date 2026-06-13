# Research Onboarding Kit for Claude Code

This kit installs a **Research Driven Development (RDD)** harness in any repository
you work on with Claude Code. It is the research-focused sibling of the
`sdd-onboarding-kit`: same philosophy and mechanics, but built for research
projects (ML research, computational science, data analysis, paper-producing
work) instead of product software.

It is not a global user configuration. It is a reusable template that produces a
project-specific configuration: `CLAUDE.md`, `PLAN.md`, `.claude/agents/`,
`.claude/skills/`, `.claude/settings.json`, `experiments/` (cards + registry),
`notebook/NOTEBOOK.html`, `decisions/`, and validation scripts.

## Documentation

Full operational documentation lives in **[`DOCUMENTATION.html`](DOCUMENTATION.html)**
(open it in a browser). The documentation is layered:

- `README.md` — quick start, purpose, safety model (this file);
- `DOCUMENTATION.html` — full operational documentation;
- `reference/` — deeper theory and policy material;
- `skills/` — reusable procedural instructions (installed as `.claude/skills/`);
- `agents/` — role-specific agents (installed as `.claude/agents/`).

**English is canonical for all reusable kit files.** Generated project-specific
artifacts (cards, notebook, decisions) may use the project's preferred language.

The kit protects Claude Code's context window: generated `CLAUDE.md` files stay
short and link out, long procedures live in skills, and durable knowledge lives in
versioned artifacts instead of chat history (see
[`reference/context-economy.md`](reference/context-economy.md)).

## What RDD does

The SDD kit's central object is the **feature spec**. Research has a different
central object and different failure modes, so RDD replaces the spec loop with the
**experiment loop**, built around the **experiment card**:

1. **Classify** the task — infrastructure (mini-SDD), experiment (the card loop),
   or analysis/writing (cited report).
2. **Draft the experiment card** — exactly one change under test, a baseline, and
   metrics + gate criteria declared *before* launch.
3. ⛔ **The researcher approves the card** — no config, launcher, or run before this.
4. **Build run artifacts** — config (the machine-readable spec), launcher, and a
   **smoke test** that must pass locally first.
5. **Launch** — cheap local runs Claude may do; expensive/cluster runs are handed
   to the human, the card goes `launched`, and Claude waits (no fabricated results).
6. **Collect & analyze** — verify real results against the gate; the skeptic tries
   to refute the verdict; every run is logged, including failures and negatives.
7. ⛔ **The researcher confirms the verdict** — Claude proposes; it never declares a
   gate passed.
8. **Scribe** updates the notebook and registry.

The two ⛔ gates sit where research goes expensively or dishonestly wrong:
**launching compute** and **making claims**. Everything else — reading, analyzing,
plotting, drafting, coding infrastructure — stays friction-free.

## Why these mechanisms

The kit was distilled from a real case: a project that lost ~6 months to
simultaneous untested changes, a silently corrupted validation set, and checkpoint
selection keyed to it. Each mechanism targets a classic research failure:

| Failure mode | Countermeasure |
|---|---|
| Many simultaneous changes; results unattributable | One change per experiment, enforced by the card |
| Evaluation data silently mutated / leaks | Frozen-artifact policy + manifest + `check_frozen.py` |
| No baseline; can't tell if anything improved | Baseline & reproduction gate before new experiments |
| Silent retries and cherry-picking (p-hacking) | Every run logged, including failures/negatives |
| Results not reproducible months later | Config-as-spec, seeds, env capture, data versioning |
| Compute wasted on undebugged jobs | Smoke test before cluster submission |
| Knowledge trapped in one head/chat | Decision logs, lab notebook, recorded answers |
| Paper claims not traceable to artifacts | Claim → card → artifact traceability at write-up |

## How to use this kit

Copy or add this folder to the project where you want to install RDD:

```text
my-research-project/
└── research-onboarding-kit/
```

Then open Claude Code in `my-research-project/` and run:

```text
Read `research-onboarding-kit/instructions.md` and configure this repository to
use Research Driven Development. Ask me all necessary questions before making
project-specific decisions.
```

Claude inspects the repository, asks the configuration questions from
`questions.md`, and generates a complete project-specific RDD harness.

## What gets installed

**Installed by default** (every onboarding):

- A short, project-specific `CLAUDE.md` and a `PLAN.md` (objectives, phases, gates).
- `.claude/agents/`: research-lead, experiment-designer, analyst, skeptic, scribe,
  literature-scout.
- `.claude/skills/research-workflow/`: the core experiment loop, state machine,
  classification policy, skeptic checklist, and the artifact templates.
- `experiments/` (registry.json + registry.html + the shared `research.css`/`research.js`),
  `notebook/NOTEBOOK.html`, `decisions/answers.md`, and the project map.
- Cross-platform validation scripts (`validate_registry.py`, `check_frozen.py`,
  `capture_environment.py`, `validate_structure.py`).

**Optional — only with your explicit selection:**

- Any of the ten skill packs (`questions.md` §16): `experiment-registry`,
  `reproducibility-audit`, `cluster-ops`, `literature-watch`, `paper-trail`,
  `data-provenance`, `decision-log`, `failure-learning`, `git-discipline`,
  `figure-style`.
- Hooks — shipped as examples, never enabled without approval.
- MCPs — none configured by default (paper-search/tracker MCPs only on opt-in).

Nothing in the kit phones home, stores credentials, or enables external access by
itself — the default install is fully local.

## Artifacts: styled HTML + machine state

Mirroring the SDD kit's two-tier model:

- **Styled, self-contained HTML** for durable human-facing artifacts — the
  experiment cards, the registry dashboard, the lab notebook, analysis reports —
  sharing one design system (`research.css` + `research.js`). Open any in a browser.
- **Machine state** in `experiments/registry.json` — the validation source of
  truth, kept separate from the HTML so `validate_registry.py` stays robust.
- **Markdown** for Claude-facing operational files (`CLAUDE.md`, skills, agents,
  policies, project map, decisions); **text** for configs and launchers.

A fully rendered reference example lives under `experiments/E001_example-baseline/`
(open `card.html`) — it is a reference for humans and agents, not installed into
target projects.

## Safety model

- **Two human gates** (card approval, verdict confirmation) that Claude never
  crosses on its own.
- **No expensive/long compute without approval**; smoke test before any cluster job.
- **Frozen artifacts never mutate**; replacements get new names + a decision.
- **Every run logged**, failures and negatives included; no metric shopping.
- **Memory discipline**: no global memory write without explicit approval of the
  exact text; no secrets or sensitive/embargoed data in any layer.
- **Hooks** are advisory or blocking, never mutating/dangerous, and disabled by
  default. **Autonomy** is read-only monitoring at most; it never crosses a gate.

See the `reference/` policies and `DOCUMENTATION.html` for detail.

## Key files

| File | Purpose |
|---|---|
| `instructions.md` | Step-by-step onboarding procedure Claude follows |
| `questions.md` | Project-specific decisions Claude asks before writing files |
| `agents/` | Subagent templates (research-lead, experiment-designer, analyst, skeptic, scribe, literature-scout) |
| `skills/research-workflow/` | The core experiment loop (copied to `.claude/skills/`) |
| `skills/optional/` | Optional skill packs, installed only when selected |
| `templates/` | `{{PLACEHOLDER}}` files Claude adapts (cards, registry, notebook, configs, …) |
| `templates/assets/` | The `research.css` / `research.js` design system |
| `reference/` | RDD theory and the integrity/reproducibility/compute/frozen/memory/autonomy policies |
| `hooks/` | Hook policy, settings snippets, and example scripts |
| `mcps/mcp-criteria.md` | When an external MCP is justified |
| `scripts/` | Cross-platform validation scripts |
| `output-project-structure.md` | Expected target-project structure after onboarding |
| `usage-prompts.md` | Ready-to-use prompts for daily research use |
| `DOCUMENTATION.html` | Full operational documentation (open in a browser) |

## Central principle

The onboarding produces a project-specific configuration. It does not copy generic
rules without adapting them. If a decision is missing, Claude asks. Unknowns become
explicit TODOs, never invented values.

## License

MIT — see [LICENSE](LICENSE).
