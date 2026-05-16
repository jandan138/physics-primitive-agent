# 2026-05-16 CPD Paper Duplicate Vertex Preprocessing

## Date

2026-05-16

## Status

Complete

## Changes

- Added the planned `paper_duplicate_vertex_preprocessing` slice to the partial
  `cpd_paper_offline_report`.
- The fixture uses two input triangles with six vertex ids and exactly overlapping coordinates on
  one edge.
- The report records exact-coordinate deduplication with first-occurrence vertex ordering:
  `[0, 1, 2, 0, 1, 3]`.
- The report records duplicate clusters `[[0, 3], [1, 4]]`, before/after component counts,
  source-face remap rows, retained/dropped source-face ids, and false package/Newton/real-USD/
  benchmark triggers.
- The executable geometry used by the operator, primitive-fit, and topology trace rows is the
  deduplicated mesh. The new topology trace records one initial topology edge and one accepted
  merge from source faces `[0]` and `[1]`.
- The top-level report remains `status: partial` and
  `paper_faithful_offline_supported: false`; the next gate advances to
  `paper_faithful_offline_scope_audit`.

## Verification

- RED command:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_duplicate_vertex_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_duplicate_vertex_audit tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result before implementation: failed on old `paper_duplicate_vertex_preprocessing_missing`
    label and old `paper_duplicate_vertex_preprocessing_audit` gate.
- GREEN command:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_failure_labels_point_to_duplicate_vertex_gap tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_duplicate_vertex_audit tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result after implementation: `4 passed`.
- Focused verification:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  - Result: `9 passed`.
- CLI smoke:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`
  - Result: exited `0` and emitted strict JSON with
    `failure_labels: ["paper_faithful_offline_scope_missing"]`,
    `next_required_gate: "paper_faithful_offline_scope_audit"`, and the
    `paper_duplicate_vertex_preprocessing` case.
- Full tests:
  `python -m pytest -q`
  - Result: `417 passed`.
- Docs validation:
  `python scripts/validate_docs.py`
  - Result: `docs validation passed`.
- Site-claim validation:
  `python scripts/validate_site_claims.py`
  - Result: `site claim validation passed`.
- Whitespace check:
  `git diff --check`
  - Result: passed with no output.

## Multi-Agent Review

- Dedup/topology reviewer: no Critical, Important, or Minor findings. Confirmed exact-overlap
  vertices, first-occurrence remap, component counts, target count, initial topology edge, and
  accepted merge.
- Test/schema reviewer: no Critical or Important findings. One Minor noted that two historical
  RED test names still reference the previous gate wording while their assertions check the new
  scope gate. Kept as-is because the RED command in this record used those names.
- Docs/claim reviewer: no Critical, Important, or Minor findings. Confirmed exact-coordinate
  fixture scope, `status: partial`, `paper_faithful_offline_supported: false`, next gate
  `paper_faithful_offline_scope_audit`, and no Newton/package/real-USD/benchmark/collision-quality
  claims.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/index.md`
- `docs/records/README.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/claim-boundaries.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only a fixture-scoped exact-coordinate duplicate-vertex preprocessing audit inside the
  partial offline paper lane.
- Does not support nonzero-distance deduplication, approximate spatial hashing, broad mesh
  cleanup, `paper_faithful_offline`, full CPD paper reproduction, package generation, Newton
  runtime support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
  readiness, or safety certification.

## Next Action

- Proceed to `paper_faithful_offline_scope_audit` after this slice is committed.
