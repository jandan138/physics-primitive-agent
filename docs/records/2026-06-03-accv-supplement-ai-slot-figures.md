# ACCV Supplement AI-Slot Figure Redraw

Date: 2026-06-03

## Decision

All generated supplement tutorial plates now use AI visual slots for their main scene content.
The deterministic composer still owns titles, panel labels, callouts, captions through LaTeX,
claim-boundary notes, file names, hashes, and the output manifest.

This keeps the supplement figures visually richer than the earlier program-drawn scene plates
without turning AI imagery into experimental evidence.

## Artifacts

- AI slot assets and manifest:
  `paper/shared/figures/assets/supplement_ai_slots/`
- Deterministic composer:
  `src/primitive_collision_compiler/paper/accv_supplement_figures.py`
- Generated figure manifest:
  `paper/shared/figures/generated/supplement/manifest.json`
- ACCV supplement PDF:
  `paper/venues/accv/build/supplement.pdf`

## Boundary

The AI slot visuals are tutorial exposition only. They are not benchmark evidence, not
deployment readiness, not whole-robot collision quality, not manipulation evidence, and not
safety certification. Claims remain bounded by the supplement text, dated records, and the
generated figure manifest.

## Verification

- `PYTHONPATH=$PWD/src $NPC_PYTHON -m pytest tests/test_accv_supplement.py -q`
  - Result: `14 passed`.
- `make -C paper accv-all`
  - Result: built `venues/accv/build/main.pdf` and `venues/accv/build/supplement.pdf`.
- Final log scan:
  - No `Overfull`, `undefined`, `Undefined`, `LaTeX Error`, package error, fatal, or emergency
    matches in `paper/venues/accv/build/main.log` or `paper/venues/accv/build/supplement.log`.
- PDF page count after rebuild:
  - Main: 15 pages.
  - Supplement: 21 pages.
