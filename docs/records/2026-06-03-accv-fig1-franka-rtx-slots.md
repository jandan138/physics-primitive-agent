# 2026-06-03 ACCV Fig.1 Franka RTX Slots

## Date

2026-06-03

## Status

Complete

## Changes

- Replaced the first three ACCV Fig.1 visual slots with Newton `ViewerRTX`
  renders from the recorded `franka_import_smoke` asset/package: asset intake,
  candidate package, and Newton diagnostics.
- Used the shared Newton checkout at `/cpfs/shared/simulation/zhuzihou/dev/newton`
  and installed `ovrtx==0.3.0.312915` plus `pyglet==2.1.14` in the existing
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`
  environment.
- Added deterministic render provenance under
  `paper/shared/figures/assets/fig1_franka_rtx_slots/`, including image JSON
  sidecars and a manifest with source report hashes, asset manifest hash, Newton
  commit, OVRTX version, and claim boundary.
- Added a fixed Franka display pose for Fig.1 readability, sourced from Newton's
  Franka example pose. The sidecars record that this is a display pose, not
  manipulation evidence.
- Updated the Fig.1 slot manifest and figure source registry to point cards
  01--03 at the Franka RTX slots while keeping the AI/report card as exposition.

## Verification

- `sha256sum /cpfs/user/zhuzihou/tmp/ovrtx_wheels/ovrtx-0.3.0.312915-py3-none-manylinux_2_35_x86_64.whl`:
  matched `a6b2b3c357f6487451c8d71e96cc4f83156c08fd9747d10e1b65f3866bed4b8f`.
- `PYTHONPATH=/cpfs/shared/simulation/zhuzihou/dev/newton:$PWD/src:$PWD /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python -c "import newton, ovrtx, pyglet"`:
  imported shared Newton, OVRTX `0.3.0`, and pyglet `2.1.14`.
- `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.fig1_franka_rtx_slots --source-artifact-root /cpfs/user/zhuzihou/dev/physics-primitive-agent`:
  generated three RTX PNGs, sidecars, and manifest.
- `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.fig1_ai_slot`:
  regenerated standalone Fig.1 PDF/PNG.
- `cd paper && make accv`: generated `paper/venues/accv/build/main.pdf`.
- Rendered final ACCV page 2 for paper-scale visual inspection with
  `mkdir -p /tmp/ppa_fig1_review && pdftoppm -png -r 180 -f 2 -l 2 paper/venues/accv/build/main.pdf /tmp/ppa_fig1_review/accv_page`.
  The inspected page render was `/tmp/ppa_fig1_review/accv_page-02.png`.
- `sha256sum paper/venues/accv/build/main.pdf paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf paper/shared/figures/generated/pipeline_schematic_ai_slot.png /tmp/ppa_fig1_review/accv_page-02.png`:
  `00da6e2c279fd8026c1b6018f0166272c9ecc134705380c3cdd92d6d34434b03`,
  `bf74dc763f8980096d59832858ed4c6e76e559b4a3dfed333ab9e10d812ea0e5`,
  `4b3acd70399546762a380927717e41fb2830b18dec00f3003f1ff4942ca0d877`,
  and `f874944903172f6c2537badba582484bf8c5fead7b135b64b280018577c119f8`.
- `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_fig1_franka_rtx_slots.py tests/test_fig1_ai_slot.py tests/test_fig1_newton_slots.py tests/test_paper_layout.py -q`:
  23 passed.
- `git diff --check`: no whitespace errors.
- `make validate`: docs validation passed; 588 passed, 2 skipped, 1978 deselected.
- `make test-paper`: 1978 passed, 590 deselected.

## Visual Review

- Round 1 clean-room reviewer verdict: WARN. Cards A/B/C were complete, but A/B
  were too side-on and the robot silhouette read as a narrow vertical profile.
- Retake 1: applied a fixed Newton Franka display pose and re-rendered the three
  slots. Clean-room reviewer then marked A and B PASS, with C WARN because probe
  markers were small and the green marker was close to the top edge.
- Retake 2: enlarged diagnostic markers, moved the green marker down, and widened
  the diagnostics camera. Local paper-scale review of standalone Fig.1 and final
  ACCV page 2 showed no slot clipping, no caption collision, no stale placeholder
  image, and the card 02 text matched the rendered link-aware box package.

## Artifacts

- `paper/shared/figures/assets/fig1_franka_rtx_slots/asset_intake_franka_rtx.png`
- `paper/shared/figures/assets/fig1_franka_rtx_slots/candidate_package_franka_rtx.png`
- `paper/shared/figures/assets/fig1_franka_rtx_slots/newton_diagnostics_franka_rtx.png`
- `paper/shared/figures/assets/fig1_franka_rtx_slots/*_franka_rtx.json`
- `paper/shared/figures/assets/fig1_franka_rtx_slots/manifest.yaml`
- `paper/shared/figures/assets/fig1_ai_slots/manifest.yaml`
- `paper/shared/figures/generated/pipeline_schematic_ai_slot.png`
- `paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf`
- `paper/venues/accv/build/main.pdf`

## Claim Impact

- Does not add new benchmark, deployment, safety-certification, manipulation, or
  whole-robot collision-quality claims.
- The Franka RTX Fig.1 slots are visual exposition from one recorded smoke asset
  and recorded link-aware primitive package.
- Quantitative claims remain tied to dated records, reports, and paper evidence
  tables.

## Next Action

- Continue ACCV paper iteration with the same claim-boundary checks after any
  additional figure or layout changes.
