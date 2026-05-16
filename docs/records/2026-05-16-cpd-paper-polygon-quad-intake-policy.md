# 2026-05-16 CPD Paper Polygon Quad Intake Policy

## Date

2026-05-16

## Status

Complete

## Changes

- Added `paper_quad_face_intake`, a deterministic one-quad source-face fixture fan-triangulated
  into two executable triangle faces.
- Added `paper_polygon_face_intake`, a deterministic one-five-vertex source-face fixture
  fan-triangulated into three executable triangle faces.
- Recorded source vertex ids, generated triangle face ids, generated triangle vertex triples,
  executable triangle faces, source-face remap, fixture preconditions, and source-face aggregate
  operator matrices.
- Recorded generated triangle face ids and original source face ids separately so reviewers do not
  read generated triangle ids as source polygon ids.
- Removed `polygon_and_quad_face_policy_missing` from the partial paper-lane failure labels.
- Advanced the next paper-lane gate to `paper_obb_sphere_fit_faithfulness_audit`.
- Kept the command in the offline paper lane: no package generation, no Newton runtime invocation,
  no real USD, no benchmark, and no collision-quality claim.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_obb_sphere_fit_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_obb_sphere_fit_audit tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_polygon_quad_intake_policy tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  failed in the RED step for the old failure label, old next gate, missing quad/polygon fixtures,
  and old CLI case list.
- `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_obb_sphere_fit_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_obb_sphere_fit_audit tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_polygon_quad_intake_policy tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  passed with 4 tests after implementation.
- `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  passed with 9 tests.
- `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report` emitted JSON with
  `status: partial`, `failure_labels: ["paper_obb_sphere_fit_faithfulness_missing"]`,
  `next_required_gate: paper_obb_sphere_fit_faithfulness_audit`, `paper_quad_face_intake`,
  `paper_polygon_face_intake`, source-face remap rows, `source_faces: [0]`,
  generated triangle face ids, executable triangle faces, and false
  package/Newton/real-USD/benchmark triggers.
- After implementation review fixes, `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  passed with 9 tests.
- After implementation review fixes, the CLI smoke emitted `partial`,
  `paper_obb_sphere_fit_faithfulness_audit`, `["paper_obb_sphere_fit_faithfulness_missing"]`,
  quad `source_faces: [0]` with generated triangle ids `[0, 1]`, and polygon `source_faces: [0]`
  with generated triangle ids `[0, 1, 2]`.
- `python scripts/validate_docs.py` and `python -m pytest -q` initially failed because
  `experiments/registry.yaml` marked this slice complete before this record status was updated from
  `In progress` to `Complete`. The record status was updated to `Complete`; final post-review
  verification is recorded below before commit.
- Final post-review `python -m pytest -q` passed with 417 tests.
- Final post-review `python scripts/validate_docs.py` passed.
- Final post-review `python scripts/validate_site_claims.py` passed.
- Final post-review `git diff --check` passed.

## Multi-Agent Review

- Initial design review found one Critical issue: the remap schema recorded only generated triangle
  ids and could not prove the fan triangulation matched `TriangleMesh`. The spec and plan were
  updated to require source vertex ids and generated triangle vertex triples.
- Review also required typed immutable remap dataclasses, source-face aggregate operator rows,
  fixture preconditions, canonical `paper_polygon_quad_intake_policy_audit` scope naming,
  independently observable RED tests, and explicit registry entry shape.
- Re-review found no remaining Critical, Important, or Minor issues before implementation.
- Implementation review found that `source_faces` still carried generated triangle ids in the
  polygon/quad rows. The report now keeps `source_faces` as original source face ids and records
  generated triangle ids only under `generated_triangle_face_ids`.
- Implementation review also required tests to prove `generated_triangle_vertex_ids` match the
  executable `TriangleMesh` triangles. The report now emits `executable_triangle_faces`, and the
  intake fixture test checks the remap against those executable faces.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/index.md`
- `docs/records/README.md`
- `docs/records/2026-05-16-cpd-paper-polygon-quad-intake-policy.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/superpowers/specs/2026-05-16-cpd-paper-polygon-quad-intake-policy-design.md`
- `docs/superpowers/plans/2026-05-16-cpd-paper-polygon-quad-intake-policy.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a partial, fixture-scoped, command-only quad/polygon source-face intake policy
  audit.
- Does not support `paper_faithful_offline`, full CPD paper reproduction, general polygon mesh
  handling, Newton runtime support, package generation, real-USD evidence, benchmark evidence,
  collision-quality validation, deployment readiness, or safety certification.
- The report remains `status: partial` with `paper_faithful_offline_supported: false`.

## Next Action

- Add `paper_obb_sphere_fit_faithfulness_audit` for the current OBB and sphere rows.
