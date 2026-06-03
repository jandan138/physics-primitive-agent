# 2026-06-03 ACCV Franka RTX Body Figure

## Date

2026-06-03

## Status

Complete

## Changes

- Replaced the ACCV Franka task-smoke body figure with an RTX visual plate at the existing
  `fig:franka-task-scene` location in the Franka articulation smoke subsection.
- Added `paper/shared/figures/generated/franka_link_aware_rtx_task_scene.{png,pdf}` and a
  provenance sidecar at
  `paper/shared/figures/assets/franka_rtx_task_scene/franka_link_aware_rtx_task_scene.json`.
- Added `primitive_collision_compiler.paper.franka_rtx_task_scene` as the deterministic composer.
  The default path composes from the already reviewed Newton `ViewerRTX` Franka diagnostics slot;
  `--worker-render` remains available for a future fresh RTX render when the local RTX session is
  stable.
- The new sidecar records the source RTX slot image plus the source slot sidecar/hash, while source
  report, manifest, and asset paths are written as artifact paths relative to the source artifact
  root.
- Updated `paper/shared/figures/sources.yaml` and the ACCV experiment caption to keep the figure
  tied to generated-package consumption exposition only.

## Verification

- `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_franka_rtx_task_scene.py -q`:
  6 passed.
- `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_franka_rtx_task_scene.py tests/test_fig1_franka_rtx_slots.py tests/test_fig1_ai_slot.py tests/test_paper_layout.py -q`:
  24 passed.
- `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.franka_rtx_task_scene --source-artifact-root /cpfs/user/zhuzihou/dev/physics-primitive-agent`:
  regenerated the PNG, PDF, and sidecar.
- `cd paper && make accv`: generated `paper/venues/accv/build/main.pdf` with 15 pages.
- `git diff --check`: no whitespace errors.
- `make validate`: docs validation passed; 594 passed, 2 skipped, 1978 deselected.
- Rendered final ACCV page 13 for paper-scale inspection with
  `mkdir -p /tmp/ppa_body_rtx_review && pdftoppm -png -r 180 -f 13 -l 13 paper/venues/accv/build/main.pdf /tmp/ppa_body_rtx_review/accv_page`.
- `sha256sum paper/shared/figures/generated/franka_link_aware_rtx_task_scene.png paper/shared/figures/generated/franka_link_aware_rtx_task_scene.pdf /tmp/ppa_body_rtx_review/accv_page-13.png`:
  `afc4082f742cc1fa93211ec96cc98c9db5ec4ac1deb59c49aa6b983b1a1e658c`,
  `b63be713c4ce41eba97a0fb8ad4343f9c9cf136b821dd369cf577f4b62d09c1e`, and
  `982e76f9af4c5ba7e19d447e54cdd5e8f6d0ce99128286759cd0f94ff3be159a`.
- `sha256sum paper/shared/figures/assets/franka_rtx_task_scene/franka_link_aware_rtx_task_scene.json paper/shared/figures/assets/fig1_franka_rtx_slots/newton_diagnostics_franka_rtx.json`:
  `4bcf6f9b7b593cfa4cabcba17748509eb4857bbe95abf6a2a9f4bf92c5acd1d7` and
  `4d37881829a95ee8a7944e21b2508fd451fc071b6a48907db19606672f7e8f50`.

## Visual Review

- Clean-room visual reviewer `019e8e0c-b56b-7761-b702-3174cb673224` returned PASS for the
  standalone figure and final PDF page.
- Reviewer evidence: the Franka-like primitive arm is centered and identifiable, the RTX view and
  status badges are readable, the final page has no clipping, caption collision, float crowding, or
  layout overlap. The only noted residual risk was that the small renderer note is near the lower
  readability limit but still legible.

## Artifacts

- `paper/shared/figures/generated/franka_link_aware_rtx_task_scene.png`
- `paper/shared/figures/generated/franka_link_aware_rtx_task_scene.pdf`
- `paper/shared/figures/assets/fig1_franka_rtx_slots/newton_diagnostics_franka_rtx.json`
- `paper/shared/figures/assets/franka_rtx_task_scene/franka_link_aware_rtx_task_scene.json`
- `paper/venues/accv/build/main.pdf`
- `/tmp/ppa_body_rtx_review/accv_page-13.png`

## Claim Impact

- Does not add benchmark, deployment, safety-certification, manipulation, contact-operation, or
  whole-robot collision-quality claims.
- Supports body-text visual exposition for one recorded Franka generated-package consumption smoke:
  12 detected links, 12 generated box primitives, zero missing body links, and 66 generated
  self-collision filter pairs.
- Quantitative claims remain tied to the 2026-05-26 link-aware package and generated-package task
  probe records.

## Next Action

- Continue ACCV text and figure iteration under the same claim-boundary checks.
