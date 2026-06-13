---
name: figure-style
description: Apply the project's plotting conventions so every figure is consistent and regenerable. Use when producing or revising figures for analysis reports or the paper.
---

# Figure style

## Purpose

Make figures consistent (style, palette, sizing for the target venue) and
**regenerable** — every published figure is produced by a named script from named
inputs, never hand-edited (`reference/reproducibility-policy.md`).

## When to use

- Producing a figure for an analysis report or the paper.
- Standardizing existing figures before submission.

## When not to use

- Throwaway exploratory plots in a session (though even these benefit from the
  style file).

## Project conventions (fill at onboarding)

```text
Style/theme:   {{STYLE_FILE}}     # e.g. matplotlib stylesheet / seaborn theme / TODO
Palette:       {{PALETTE}}        # colorblind-safe by default
Figure sizes:  {{SIZES}}          # single/double-column for {{VENUE}}
Fonts/sizes:   {{FONTS}}
Output format: {{FORMAT}}         # e.g. PDF (vector) + PNG; DPI for raster
Save location: {{FIGURES_DIR}}
```

## Procedure

1. Generate the figure with a **script** that takes its inputs (card IDs / result
   files) and writes to `{{FIGURES_DIR}}`. No manual post-editing.
2. Apply the style file/palette/sizes above so it matches the venue.
3. Record figure provenance: the figure names its generating script and inputs
   (feeds `paper-trail`).
4. Confirm re-running the script reproduces the figure byte-for-byte (or
   visually, for stochastic content).

## Output artifact

A regenerable figure plus its provenance (script + inputs), styled to the venue.

## Safety constraints

- Never hand-edit a published figure into existence — it must regenerate.
- Figures must not embed sensitive/embargoed raw data.
- Cite the source artifacts; a figure's numbers trace like any other claim.
