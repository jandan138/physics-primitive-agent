# 2026-06-04 ACCV Supplement Labeled AI Tutorial Slot Retake

## Date

2026-06-04

## Status

Complete

## Changes

- Retook the six supplement tutorial slot strips for Fig.1, Fig.5, Fig.6, Fig.7, Fig.8, and
  Fig.11 using AI-generated academic tutorial imagery with visible in-image labels.
- Replaced the earlier text-free AI slot strips so the small images now carry short local labels
  such as generator/package/check, COM/gate, link/body-attachment/merge-risk, source/generated
  counts, suppression audit, and config/record/manifest/PDF provenance flow.
- Preserved deterministic paper-owned text for figure titles, outer panel headers, callout boxes,
  captions, and claim-boundary footer text.
- Updated tutorial slot sidecars with the new built-in image-generation source ids, slot hashes,
  labeled-panel recipe, panel roles, prompt summaries, and reviewed segment boundaries.
- Regenerated the six affected supplement PNG/PDF figures and the ACCV supplement PDF.

## Visual Review

- Local raw-slot review inspected
  `/tmp/ppa_labeled_slots_review/raw_labeled_slots_sheet.png`.
- Local composed-figure review inspected
  `/tmp/ppa_labeled_slots_review/composed_labeled_figures_sheet.png`.
- Local paper-scale review inspected the rendered supplement PDF page sheet
  `/tmp/ppa_labeled_slots_review/pdf_labeled_pages_sheet.png`.
- Local dense-region review inspected
  `/tmp/ppa_labeled_slots_review/pdf_labeled_figure_crops_sheet_v3.png`.
- A first composed review found the Fig.5 strip segmentation too tight for the generated
  `BODY`/`GATE` regions; the compound-body slot bounds were reset to thirds and the figure was
  regenerated before PDF review.
- Independent clean-room visual review inspected only the supplied images. Reviewer verdict:
  `PASS`. The reviewer found all six groups visible and identifiable, the main in-image labels
  useful, no obvious clipping or caption collision, and no retake requirement. The only residual
  risk was that a few micro-labels in dense provenance/accounting panels are near the lower
  readability limit.

## Verification

- AI tutorial sidecar regeneration:
  `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.supplement_tutorial_2d_slots`;
  result: six sidecars written.
- Supplement figure composition:
  `PYTHONPATH=$PWD/src:$PWD python -m primitive_collision_compiler.paper.accv_supplement_figures`;
  result: generated supplement figure manifest and six affected figure PNG/PDF files regenerated.
- ACCV build:
  `make -C paper accv-all`; result: `main.pdf` and `supplement.pdf` built.
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
  manifest, this record, the superseded AI tutorial record, and the record index found no private
  absolute path prefix, user-name, repository-host, or institution-name matches.

## Artifacts

- `src/primitive_collision_compiler/paper/supplement_tutorial_2d_slots.py`
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
- `paper/shared/figures/generated/supplement/supplement_candidate_lane_anatomy.png`
- `paper/shared/figures/generated/supplement/supplement_candidate_lane_anatomy.pdf`
- `paper/shared/figures/generated/supplement/supplement_compound_body_state_teaching.png`
- `paper/shared/figures/generated/supplement/supplement_compound_body_state_teaching.pdf`
- `paper/shared/figures/generated/supplement/supplement_franka_link_frames.png`
- `paper/shared/figures/generated/supplement/supplement_franka_link_frames.pdf`
- `paper/shared/figures/generated/supplement/supplement_generated_package_consumption.png`
- `paper/shared/figures/generated/supplement/supplement_generated_package_consumption.pdf`
- `paper/shared/figures/generated/supplement/supplement_franka_source_suppression.png`
- `paper/shared/figures/generated/supplement/supplement_franka_source_suppression.pdf`
- `paper/shared/figures/generated/supplement/supplement_provenance_flow.png`
- `paper/shared/figures/generated/supplement/supplement_provenance_flow.pdf`
- `paper/venues/accv/build/supplement.pdf`

## Claim Impact

- No experimental, benchmark, deployment, real-world transfer, safety-certification,
  manipulation, or whole-robot collision-quality claims are added.
- The labeled AI tutorial slots are explanatory review aids only. They do not replace Phase 0
  evidence records, quantitative result manifests, or Newton diagnostic reports.
- Claim boundaries remain aligned with `docs/reference/claim-boundaries.md`,
  `paper/shared/evidence/claims.yaml`, and dated Phase 0 records.

## Next Action

- Continue using labeled AI tutorial slots as the current ACCV supplement state; retake only if a
  later paper-scale visual review flags a concrete readability or clipping issue.
