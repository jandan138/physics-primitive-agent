# 2026-05-16 CPD Paper Fixture Breadth Expansion Plan

## Date

2026-05-16

## Status

Complete

## Changes

- Added `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`.
- Mapped the nine blocking `paper_faithful_offline_scope_audit` rows to five planned future
  synthetic fixture batches.
- Recommended `paper_fixture_breadth_batch_a` as the next code slice:
  `paper_mixed_face_preprocess_operator`, `paper_degenerate_preprocess_face_drop`, and
  `paper_concave_polygon_rejected`.
- Updated project index, paper gap matrix, offline lane spec, paper-story status, claim
  boundaries, DeepDive evidence status, and records index.
- Kept the slice documentation-only. It does not implement fixtures or change
  `cpd_paper_offline_report`.

## Verification

- Docs validation:
  `python scripts/validate_docs.py`
  - Result: `docs validation passed`.
- Site-claim validation:
  `python scripts/validate_site_claims.py`
  - Result: `site claim validation passed`.
- Whitespace check:
  `git diff --check`
  - Result: passed with no output.
- Full tests:
  `python -m pytest -q`
  - Result: `417 passed in 42.75s`.

## Multi-Agent Review

- Fixture-plan completeness reviewer: found two Important gaps and two Minor gaps. Batch B did
  not explicitly cover sphere or capped cylinder; Batch A operator rows did not require
  eigenvalues/eigenvectors or degeneracy labels; `paper_concave_polygon_rejected` had an
  ambiguous failure label; and fixture rows lacked a per-row claim-boundary column. The plan now
  covers all six paper primitive names, adds `paper_offset_sphere_fit` and
  `paper_flat_capped_cylinder_axis_fit`, requires aggregate/retained-face eigen fields and
  degeneracy labels for Batch A, gives the concave polygon fixture the case-local label
  `source_face_intake_unsupported_concave_polygon`, and adds a per-row claim-boundary column.
  Re-review found no remaining findings.
- Docs/claim reviewer: no Critical or Important findings. One Minor noted that this record still
  had pending verification and review results while marked complete; this section resolves that
  closure issue.
- Reproducibility/navigation reviewer: no Critical findings. One Important matched the pending
  record-results issue above. One Minor found that
  `docs/records/2026-05-15-cpd-paper-permission-assertion.md` existed but was not listed in
  `docs/records/README.md`; the records index now includes it.

## Artifacts

- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/records/README.md`
- `docs/records/2026-05-16-cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/superpowers/specs/2026-05-16-cpd-paper-fixture-breadth-expansion-plan-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-fixture-breadth-expansion-plan.md`

## Claim Impact

- Supports only a documentation-only offline fixture-breadth expansion plan.
- Does not support implemented fixture breadth, `paper_faithful_offline`, full CPD paper
  reproduction, package generation, Newton runtime support, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.

## Next Action

- Implement `paper_fixture_breadth_batch_a` in a future code slice.
