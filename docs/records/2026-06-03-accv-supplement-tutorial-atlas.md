# 2026-06-03 ACCV Supplement Tutorial Atlas

## Date

2026-06-03

## Status

Complete

## Changes

- Added a separate ACCV supplement entrypoint that uses the ACCV/LNCS preamble and shared
  bibliography while keeping the main paper self-contained.
- Added supplement-only tutorial sections for reviewer guidance, notation, diagnostic predicate
  derivations, compound body-state accounting, link-aware robot package semantics, visual reading
  rules, reproducibility, and claim boundaries.
- Added deterministic supplement-only teaching figures and a committed supplement figure manifest.
  The figures are new supplement assets, not copies of main-paper figures.
- Added supplement-only tables for notation, predicate parameters, robot audit semantics,
  visual-reading rules, provenance, and claim-boundary checklists. The tables are new supplement
  assets, not copies of main-paper result tables.
- Iterated figure and table layout after visual review so dense pages contain explanatory text and
  the updated Franka, cup/tray, and provenance figure panels do not clip or spill into gutters.
- Resolved merge-review provenance issues by making the committed manifest path portable, fixing
  deterministic PDF metadata, and replacing a missing source-record reference.

## Verification

- `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_accv_supplement.py -q` exited 0
  (`9 passed`).
- `make -C paper accv-supplement` exited 0 and produced a 21-page supplement PDF.
- `rg -n "Overfull|undefined references|undefined citations|Citation .* undefined|Reference .* undefined|Label\\(s\\) may have changed" paper/venues/accv/build/supplement.log || true`
  returned no matches after the final build.
- `pdftotext -layout paper/venues/accv/build/supplement.pdf -` page audit found text on every
  rendered page and no page reduced to only a figure or only a table.
- Page PNG review focused on pages 12, 16, 17, 18, 19, and 20 after rebuilding the supplement.
- Independent clean-room visual review of pages 12, 16, 17, 18, 19, and 20 plus the standalone
  Franka link, cup/tray storyboard, and provenance-flow figures returned PASS with high
  confidence. The review found no required retake or relayout.
- Added regression coverage for manifest double-blind scanning, portable manifest paths,
  source-record existence, and stable regenerated figure hashes.

## Artifacts

- `paper/venues/accv/supplement.tex`
- `paper/shared/supplemental/`
- `src/primitive_collision_compiler/paper/accv_supplement_figures.py`
- `paper/shared/figures/generated/supplement/manifest.json`
- `paper/shared/figures/generated/supplement/supplement_*.pdf`
- `paper/shared/figures/generated/supplement/supplement_*.png`

## Claim Impact

- Supports a clearer ACCV supplement presentation of the existing scoped diagnostic-checker story.
- Does not add benchmark superiority, deployment readiness, whole-robot collision quality,
  manipulation evidence, safety certification, or formal verification claims.
- Keeps generated primitive packages framed as safety-affecting candidate artifacts that require
  simulation-checked diagnostics and review.

## Next Action

- Preserve the supplement source, manifest, and generated small figure assets under version
  control; keep raw assets, run directories, logs, and videos out of git.
