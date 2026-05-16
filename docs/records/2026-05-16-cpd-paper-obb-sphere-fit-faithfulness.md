# 2026-05-16 CPD Paper OBB Sphere Fit Faithfulness

## Date

2026-05-16

## Status

Complete

## Changes

- Replaced the `cpd_paper_offline_report` OBB and sphere candidate rows with offline
  paper-shaped fit-audit rows for named deterministic toy fixtures.
- Kept the shared CPD-like primitive fitter unchanged so existing package, Newton, real-USD, and
  diagnostic paths do not inherit this paper-lane clamp change.
- Recorded paper OBB projected lower/upper bounds, local center, world-space center, half-extents,
  `1e-3` primitive clamp, volume formula, and containment status.
- Recorded paper sphere center source as the OBB center, unclamped max-distance radius, clamped
  radius, volume formula, and containment status.
- Added `paper_tiny_sphere_clamp` to exercise the sphere radius clamp path below `1e-3`.
- Added candidate uniqueness checks so OBB/sphere rows replace the earlier report-local surrogate
  rows instead of duplicating paper primitive names.
- Recorded matrix-layout metadata so operator eigenvectors are labeled as column vectors and
  primitive axes are labeled as row vectors.
- Advanced the next paper-lane gate to `paper_duplicate_vertex_preprocessing_audit`.
- Kept the command in the offline paper lane: no package generation, no Newton runtime invocation,
  no real USD, no benchmark, and no collision-quality claim.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_duplicate_vertex_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_duplicate_vertex_audit tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed in the RED step for the old OBB/sphere failure label, old next gate, missing implemented
  scope entry, and old OBB/sphere surrogate metadata.
- The same focused command passed with 4 tests after implementation.
- After review fixes, `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed with 2 tests and exercised `paper_tiny_sphere_clamp`.
- Pre-review `python -m pytest -q` passed with 417 tests.
- Final post-review `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  passed with 9 tests.
- Final post-review CLI smoke emitted `partial`, `paper_duplicate_vertex_preprocessing_audit`,
  `["paper_duplicate_vertex_preprocessing_missing"]`, the 11 expected cases, and
  `paper_tiny_sphere_clamp` sphere radius `0.001` from unclamped radius
  `7.071067811865475e-05`.
- Final post-review `python -m pytest -q` passed with 417 tests.
- Final post-review `python scripts/validate_docs.py` passed.
- Final post-review `python scripts/validate_site_claims.py` passed.
- Final post-review `git diff --check` passed.

## Multi-Agent Review

- Spec review found no Critical issues.
- Paper-alignment review required explicit sphere radius clamping, explicit OBB world-center
  accounting, clarification that the point set means vertices of subsumed faces, and an axis-order
  policy field.
- Claim-boundary review required explaining why `next_required_gate` advances past the record gate,
  replacing proof-style wording with recorded diagnostic wording, and keeping fit-failure semantics
  available for future degenerate fixtures.
- Implementation review required avoiding duplicate OBB/sphere candidate rows, keeping the
  paper-specific clamp local to the paper report, checking a non-axis-aligned fixture, asserting
  candidate uniqueness, and preserving merge-cost/queue-trace regression visibility.
- Implementation review found that the sphere clamp path was not exercised, the CLI JSON assertions
  were too shallow, and safe docs omitted the new OBB/sphere wording. The follow-up fixes added
  `paper_tiny_sphere_clamp`, asserted sphere axes and CLI OBB/sphere metadata, added the record to
  the docs index, and updated safe wording.
- A formula review Minor noted that operator eigenvectors and primitive axes use different matrix
  layouts in the report. The report now labels those layouts explicitly.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/index.md`
- `docs/records/README.md`
- `docs/records/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/superpowers/specs/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-obb-sphere-fit-faithfulness.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only OBB/sphere fit-faithfulness audit.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, Newton runtime support,
  package generation, real-USD evidence, benchmark evidence, collision-quality validation,
  deployment readiness, or safety certification.
- The report remains `status: partial` with `paper_faithful_offline_supported: false`.

## Next Action

- Add `paper_duplicate_vertex_preprocessing_audit` for overlapped or duplicate vertices and
  source-face remap behavior.
