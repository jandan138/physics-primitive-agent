# 2026-06-04 ACCV Supplement 2D Tutorial Slot Pass

## Date

2026-06-04

## Status

Superseded

## Changes

- Replaced the supplement's unclear or repeated small slot imagery for candidate-lane anatomy,
  compound body-state teaching, Franka link frames, generated-package consumption,
  source-shape suppression, and artifact provenance flow with deterministic academic 2D tutorial
  diagrams.
- Added `deterministic_2d_tutorial_pil` as an explicit supplement slot renderer, with anonymous
  sidecars that record panel counts, style, source records, slot hashes, and claim boundaries.
- Tightened supplement manifest loading so deterministic 2D tutorial sidecars must match the
  figure id, renderer, portable slot path, slot hash, and expected panel count before figure
  provenance is accepted.
- Kept the remaining predicate and failure-storyboard scene slots on Newton `ViewerRTX`, while
  shrinking the Newton RTX supplement slot set so the converted 2D teaching figures cannot be
  accidentally regenerated as repeated Franka RTX triptychs.
- Regenerated the affected slot strips, composed supplement PNG/PDF figures, and the ACCV
  supplement PDF.

## Visual Review

- Local review found an initial polish issue where several long in-panel headers/tags were too
  tight after strip scaling. The 2D slot generator now uses wider header labels and pixel-bounded
  text fitting for tags.
- Independent clean-room visual review inspected:
  `/tmp/ppa_supplement_2d_review/slot_contact_sheet.png`,
  `/tmp/ppa_supplement_2d_review/composed_figure_contact_sheet.png`, and
  `/tmp/ppa_supplement_2d_review/pdf_page_contact_sheet.png`.
- Reviewer verdict: `PASS`. The reviewer reported that Fig.1, Fig.5, and Fig.11 now read as
  information-rich 2D tutorial diagrams; Fig.6, Fig.7, and Fig.8 are visually and semantically
  distinct; and the final PDF pages show no visible caption collision, clipped boundaries, or
  float crowding. The reviewer noted only optional future polish for the smallest in-panel
  microtext.

## Verification

- 2D slot generation:
  `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.supplement_tutorial_2d_slots`;
  result: six slot strips and six sidecars written.
- Supplement figure composition:
  `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.accv_supplement_figures`;
  result: `paper/shared/figures/generated/supplement/manifest.json` regenerated.
- ACCV build:
  `make -C paper accv-all`; result: main and supplement PDFs built, supplement page count remains
  20.
- Targeted tests:
  `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_accv_supplement.py tests/test_supplement_newton_rtx_slots.py tests/test_supplement_tutorial_2d_slots.py tests/test_fig1_franka_rtx_slots.py tests/test_fig1_ai_slot.py tests/test_franka_rtx_task_scene.py tests/test_paper_layout.py -q`;
  result after review-fix tests were added: `55 passed`.
- Repository validation:
  `make validate`; result: docs validation passed, `625 passed, 2 skipped, 1978 deselected`.
- Whitespace check:
  `git diff --check`; result: no output, exit 0.
- Supplement page count:
  `pdfinfo paper/venues/accv/build/supplement.pdf | rg '^Pages:'`; result: `Pages: 20`.
- Supplement log scan:
  `rg -n "Underfull \\vbox|Overfull|LaTeX Warning" paper/venues/accv/build/supplement.log`;
  result: no matches, exit 1.
- Provenance leak scan over the slot manifest, slot sidecars, generated supplement figure
  manifest, and this record found no private absolute path prefix, user-name, repository-host, or
  institution-name matches.
- Fig.6/Fig.7/Fig.8 non-reuse spot check found distinct slot hashes for
  `supplement_franka_link_frames`, `supplement_generated_package_consumption`, and
  `supplement_franka_source_suppression`.

## Artifacts

- `src/primitive_collision_compiler/paper/supplement_tutorial_2d_slots.py`
- `src/primitive_collision_compiler/paper/accv_supplement_figures.py`
- `src/primitive_collision_compiler/paper/supplement_newton_rtx_slots.py`
- `paper/shared/figures/assets/supplement_ai_slots/manifest.yaml`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_candidate_lane_anatomy_slot.png`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_candidate_lane_anatomy_slot.json`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_compound_body_state_teaching_slot.png`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_compound_body_state_teaching_slot.json`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_franka_link_frames_slot.png`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_franka_link_frames_slot.json`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_generated_package_consumption_slot.png`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_generated_package_consumption_slot.json`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_franka_source_suppression_slot.png`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_franka_source_suppression_slot.json`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_provenance_flow_slot.png`
- `paper/shared/figures/assets/supplement_ai_slots/supplement_provenance_flow_slot.json`
- `paper/shared/figures/generated/supplement/manifest.json`
- `paper/shared/figures/generated/supplement/*.png`
- `paper/shared/figures/generated/supplement/*.pdf`
- `paper/venues/accv/build/supplement.pdf`
- `tests/test_supplement_tutorial_2d_slots.py`
- `tests/test_accv_supplement.py`
- `tests/test_supplement_newton_rtx_slots.py`

## Claim Impact

- No experimental, benchmark, deployment, real-world transfer, safety-certification,
  manipulation, or whole-robot collision-quality claims are added.
- The new 2D tutorial slots are explanatory review aids. They do not replace Phase 0 evidence
  records, quantitative result manifests, or Newton diagnostic reports.
- Claim boundaries remain aligned with `docs/reference/claim-boundaries.md`,
  `paper/shared/evidence/claims.yaml`, and the dated Phase 0 records.

## Next Action

- Superseded for the current ACCV supplement by
  `docs/records/2026-06-04-accv-supplement-ai-tutorial-slot-retake.md`, which replaces these
  deterministic program-drawn tutorial slots with AI-generated academic tutorial slots.
