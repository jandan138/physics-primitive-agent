# 2026-06-04 ACCV Supplement Newton RTX Layout Pass

## Date

2026-06-04

## Status

Complete

## Changes

- Replaced the nine scene-explanation supplement slot images with Newton `ViewerRTX` renders:
  predicate drop/settle, stack-or-slide, sphere-rain, generated-package consumption,
  compound-body state, Franka link frames, Franka source suppression, bowl failure storyboard,
  and cup/tray failure storyboard.
- Kept the remaining non-scene teaching plates as AI-slot assets, and taught the supplement
  manifest to distinguish `newton_viewer_rtx_ovrtx` scene slots from `built_in_imagegen`
  explanatory slots.
- Added RTX sidecars for every Newton-rendered scene slot, with repository-relative provenance
  and no private source paths.
- Added a deterministic Newton RTX supplement renderer. The renderer uses one worker process per
  figure because long single-process OVRTX sessions produced blank background-only renders after
  the first few plates during local diagnosis.
- Re-exported the Newton RTX slot strips with taller `620x760` slot tiles while keeping the source
  RTX panels at `620x620`; sidecars now record the slot composition size so future reviews can
  distinguish complete source panels from paper-slot strip packaging.
- Changed supplement floats from forced `[H]` placement to flexible `[tbp]`/`[t]` placement,
  enabled `\raggedbottom`, and tightened float separation lengths so text pages do not stretch
  paragraphs into large blank gaps.
- Added `placeins` barriers and guarded large robot/storyboard figures after review found that
  two failure storyboards could otherwise collect onto a figure-only page. The storyboards now use
  local `[!ht]` placement, and section tables/large robot scene figures are bounded to their
  explanatory text.
- Added a short reviewer-audit walkthrough in the limitations section so the supplement remains
  above the 20-page target without creating artificial whitespace.

## Verification

- RTX environment import smoke: `newton`, `ovrtx`, `pyglet`, and `warp` import from the selected
  Newton-capable environment.
- Newton scene slot generation:
  `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.supplement_newton_rtx_slots --source-artifact-root <artifact-root> --panel-dir /tmp/ppa_supplement_newton_rtx_panels`.
- Supplement figure composition:
  `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.accv_supplement_figures`.
- Targeted tests:
  `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_accv_supplement.py tests/test_supplement_newton_rtx_slots.py tests/test_fig1_franka_rtx_slots.py tests/test_fig1_ai_slot.py tests/test_franka_rtx_task_scene.py tests/test_paper_layout.py -q`;
  result: `47 passed`.
- Repository validation:
  `make validate`; result: docs validation passed, `617 passed, 2 skipped, 1978 deselected`.
- ACCV build:
  `make -C paper accv-all`; result: main and supplement PDFs built.
- Supplement page count after the layout pass: `pdfinfo paper/venues/accv/build/supplement.pdf`
  reports `Pages: 20`.
- Supplement log scan for page-stretch and hard layout problems found no `Underfull \vbox`,
  `Overfull`, or `LaTeX Warning` matches in `paper/venues/accv/build/supplement.log`.
- Provenance leak scan over the AI/RTX slot manifest, RTX sidecars, and generated supplement
  figure manifest found no private path or repository-host matches.
- PDF page raster review used the rebuilt `paper/venues/accv/build/supplement.pdf` and
  `pdftoppm -r 120`. Final page contact sheet:
  `/tmp/ppa_supp_final_pages_rtx_tall.png`.
- Slot contact-sheet review used `/tmp/ppa_supp_final_slots_rtx_tall.png`. The first independent
  pass warned that raw slot strips looked vertically tight; after taller slot recomposition, the
  second independent reviewer returned `PASS` for both final pages and final slots with no retake
  or layout recommendation.

## Artifacts

- `src/primitive_collision_compiler/paper/supplement_newton_rtx_slots.py`
- `src/primitive_collision_compiler/paper/accv_supplement_figures.py`
- `paper/shared/figures/assets/supplement_ai_slots/manifest.yaml`
- `paper/shared/figures/assets/supplement_ai_slots/*_slot.json`
- `paper/shared/figures/assets/supplement_ai_slots/*_slot.png`
- `paper/shared/figures/generated/supplement/manifest.json`
- `paper/shared/figures/generated/supplement/*.png`
- `paper/shared/figures/generated/supplement/*.pdf`
- `paper/venues/accv/supplement.tex`
- `paper/shared/supplemental/*.tex`
- `tests/test_accv_supplement.py`
- `tests/test_supplement_newton_rtx_slots.py`
- `paper/venues/accv/build/supplement.pdf`

## Claim Impact

- No new experimental, benchmark, deployment, real-world transfer, safety-certification,
  manipulation, or whole-robot collision-quality claims are added.
- The Newton RTX supplement slots are reviewer-facing exposition for recorded diagnostic concepts
  and artifact-consumption paths. They do not replace the evidence registries or dated Phase 0
  diagnostic records.
- Claim boundaries remain aligned with `docs/reference/claim-boundaries.md`,
  `paper/shared/evidence/claims.yaml`, and the dated Phase 0 records.

## Next Action

- Merge the supplement layout/RTX pass after final validation and keep future supplement visuals
  on the same sidecar-plus-visual-review path.
