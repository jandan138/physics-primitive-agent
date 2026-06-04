# 2026-06-04 ACCV Supplement AI Tutorial Slot Retake

## Date

2026-06-04

## Status

Complete

## Changes

- Replaced the program-drawn supplement tutorial slots for Fig.1, Fig.5, Fig.6, Fig.7, Fig.8,
  and Fig.11 with AI-generated academic tutorial slot strips.
- Kept critical paper text outside the generated slot images: figure titles, panel labels,
  callout text, captions, and claim-boundary text remain deterministic in the paper composer or
  LaTeX.
- Updated the tutorial slot sidecars to record the built-in image-generation source id, slot
  hash, panel count, AI tutorial style, and per-slot normalized segment boundaries.
- Changed the supplement figure composer to use sidecar segment boundaries before contain-scaling
  each panel, instead of assuming that AI-generated wide strips are evenly divided.
- Regenerated the six affected slot images, six sidecars, composed supplement PNG/PDF figures,
  generated supplement manifest, and ACCV supplement PDF.

## Visual Review

- Local review inspected raw slot, composed figure, final PDF page, and dense page crop contact
  sheets under the temporary review directory.
- Local result: the AI-generated slots are visually more polished than the replaced program-drawn
  diagrams; Fig.6, Fig.7, and Fig.8 are semantically distinct; Fig.8 no longer has edge-cut
  markers after sidecar-guided segmenting; and final PDF pages show no obvious text overlap,
  caption collision, or slot clipping.
- Independent clean-room visual review inspected only the supplied review images. Reviewer
  verdict: `WARN` only because the first dense QA crops cut into the figure titles; raw AI slots,
  composed figures, and final PDF pages were all reported as `PASS`, with no commit-blocking
  figure issue.
- The QA-only Fig.8 and Fig.11 dense crops were re-exported with extra top padding after the
  review warning; the paper figure assets and PDF were unchanged by that crop-only correction.
- Independent code review found no blocking issue. Its low-risk finding was that sidecar claim
  boundary validation accepted the weak phrase `not experimental evidence` alone; the loader and
  tests now require all tutorial claim-boundary exclusion phrases, including benchmark,
  deployment, manipulation, whole-robot collision-quality, and safety-certification exclusions.

## Verification

- AI tutorial sidecar regeneration:
  `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.supplement_tutorial_2d_slots`;
  result: six sidecars written.
- Supplement figure composition:
  `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.accv_supplement_figures`;
  result: `paper/shared/figures/generated/supplement/manifest.json` regenerated.
- ACCV build:
  `make -C paper accv-all`; result: main and supplement PDFs built, supplement page count remains
  20.
- Targeted sidecar and segment-bound tests:
  `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_supplement_tutorial_2d_slots.py tests/test_accv_supplement.py::test_supplement_slot_manifest_accepts_2d_tutorial_slots tests/test_accv_supplement.py::test_supplement_slot_manifest_rejects_mismatched_2d_tutorial_sidecar tests/test_accv_supplement.py::test_supplement_slot_manifest_rejects_stale_2d_tutorial_sidecar_hash tests/test_accv_supplement.py::test_supplement_slot_manifest_rejects_stale_2d_tutorial_panel_count tests/test_accv_supplement.py::test_supplement_slot_manifest_rejects_bad_2d_tutorial_segment_bounds tests/test_accv_supplement.py::test_supplement_slot_manifest_rejects_weak_2d_tutorial_claim_boundary tests/test_accv_supplement.py::test_supplement_figure_composer_preserves_slot_segments_without_center_crop -q`;
  result: `11 passed`.
- Paper figure and layout tests:
  `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_accv_supplement.py tests/test_supplement_newton_rtx_slots.py tests/test_supplement_tutorial_2d_slots.py tests/test_fig1_franka_rtx_slots.py tests/test_fig1_ai_slot.py tests/test_franka_rtx_task_scene.py tests/test_paper_layout.py -q`;
  result: `57 passed`.
- Repository validation:
  `make validate`; result: docs validation passed and `627 passed, 2 skipped, 1978 deselected`.
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

## Artifacts

- `src/primitive_collision_compiler/paper/supplement_tutorial_2d_slots.py`
- `src/primitive_collision_compiler/paper/accv_supplement_figures.py`
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

## Claim Impact

- No experimental, benchmark, deployment, real-world transfer, safety-certification,
  manipulation, or whole-robot collision-quality claims are added.
- The AI-generated tutorial slots are explanatory review aids only. They do not replace Phase 0
  evidence records, quantitative result manifests, or Newton diagnostic reports.
- Claim boundaries remain aligned with `docs/reference/claim-boundaries.md`,
  `paper/shared/evidence/claims.yaml`, and dated Phase 0 records.

## Next Action

- Use sidecar-guided segment boundaries for any future AI-generated strip slots so non-even AI
  panel spacing cannot cut objects or markers at card boundaries.
