# 2026-06-03 ACCV Fig.1 Newton Render Slots

## Date

2026-06-03

## Status

Complete

## Changes

- Replaced the first three Fig.1 visual slots with Newton `SensorTiledCamera`
  renders: asset intake, candidate package lanes, and diagnostics reconstruction.
- Preserved the fourth AI/report visual slot and the existing ACCV figure output
  path `paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf`.
- Updated Fig.1 manifest, source registry, caption, and composer metadata from
  pure AI-slot composition to hybrid Newton-rendered slots plus AI/report card.
- Added sidecar provenance for the three Newton-rendered slots, including source
  report hashes, asset manifest hash, Newton checkout, renderer recipe, and claim
  boundary.
- Used external source-artifact root
  `/cpfs/user/zhuzihou/dev/physics-primitive-agent` for ignored report/USD inputs;
  those large/raw inputs remain uncommitted and are referenced by path plus hashes
  in the Newton slot sidecars and manifest.

## Verification

- `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.fig1_ai_slot`: PASS.
- `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_fig1_newton_slots.py tests/test_fig1_ai_slot.py tests/test_paper_layout.py -q`: PASS, 15 tests.
- `PYTHONPATH=$PWD/src:$PWD make -C paper accv`: PASS, 15 pages.
- Rendered ACCV page 2 with `pdftoppm` for visual inspection:
  `/tmp/fig1_newton_accv_page2_final-02.png`.
- Independent visual QA first pass: WARN for diagnostics scale/occlusion.
- Diagnostics retake completed; independent visual QA second pass: PASS for the
  composed figure and diagnostics slot.
- Final regenerated standalone Fig.1 visual QA: PASS; optional polish only for
  Card 02 crop tightness and Card 03 marker contrast.

## Artifacts

- `paper/shared/figures/assets/fig1_newton_slots/asset_intake_newton.png`
- `paper/shared/figures/assets/fig1_newton_slots/candidate_package_newton.png`
- `paper/shared/figures/assets/fig1_newton_slots/newton_diagnostics_newton.png`
- `paper/shared/figures/assets/fig1_newton_slots/manifest.yaml`
- `paper/shared/figures/assets/fig1_newton_slots/*_newton.json`
- `paper/shared/figures/assets/fig1_ai_slots/manifest.yaml`
- `paper/shared/figures/generated/pipeline_schematic_ai_slot.png`
- `paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf`
- Paper build: `paper/venues/accv/build/main.pdf`
- PDF page review image: `/tmp/fig1_newton_accv_page2_final-02.png`

## Claim Impact

- Does not add new benchmark, deployment, safety-certification, or whole-robot
  performance claims.
- The Newton-rendered Fig.1 slots are visual exposition derived from recorded
  Phase 0 assets/packages and diagnostics fields; they are not new experimental
  evidence.
- Quantitative claims remain tied to dated records, reports, and experiment
  tables.

## Next Action

- Continue ACCV paper iteration with claim-boundary checks and paper-scale visual
  review after any additional figure or layout changes.
