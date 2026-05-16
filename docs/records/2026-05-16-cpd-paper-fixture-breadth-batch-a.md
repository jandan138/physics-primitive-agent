# 2026-05-16 CPD Paper Fixture Breadth Batch A

## Date

2026-05-16

## Status

Complete

## Changes

- Added Batch A source/preprocess/intake/operator fixture breadth to the partial
  `cpd_paper_offline_report`.
- Added `paper_mixed_face_preprocess_operator`, a mixed triangle/quad/polygon source-face fixture
  with exact-coordinate preprocessing and source-face aggregate `Q` eigen fields.
- Added `paper_degenerate_preprocess_face_drop`, an exact-coordinate preprocessing fixture that
  drops one source face after deduplication makes it degenerate.
- Added `paper_concave_polygon_rejected`, a case-local unsupported source-face intake fixture with
  failure label `source_face_intake_unsupported_concave_polygon`.
- Advanced `next_required_gate` to `paper_fixture_breadth_batch_b`.
- Kept the command offline-only: no package generation, Newton runtime execution, real USD, or
  benchmark work.

## Verification

- RED command:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_a tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result before implementation: failed because the three Batch A cases were absent.
- GREEN command:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_b tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_a tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_covers_first_toy_slice tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result after implementation: `4 passed`.
- Review-fix regression command:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_a tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result after fixing retained source-face ownership in primitive-fit audit rows: `2 passed`.
- Focused verification:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  - Result: `10 passed`.
- CLI smoke:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report | python -c 'import json,sys; p=json.load(sys.stdin); print(p["next_required_gate"]); print(p["paper_faithfulness"]["implemented_fixture_scope"][-2:]); print([c["case_id"] for c in p["cases"][-3:]]); print(p["cases"][-2]["primitive_fit_audit"]["source_faces"])'`
  - Result: printed `paper_fixture_breadth_batch_b`, the final fixture-scope entries ending in
    `paper_fixture_breadth_batch_a_source_preprocess_intake_operator`, the three Batch A case IDs,
    and retained primitive-fit source faces `[1]` for `paper_degenerate_preprocess_face_drop`.
- Full tests:
  `python -m pytest -q`
  - Result: `418 passed in 44.63s`.
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

- Implementation review found that `paper_degenerate_preprocess_face_drop` retained source face `1`
  in the operator audit but still reported primitive-fit `source_faces: [0]`. Fixed by passing
  `executable_source_face_ids` into primitive-fit audit payloads and adding regression assertions.
- Documentation/claim review found stale present-tense wording that could read
  `paper_fixture_breadth_expansion_plan` as the current gate. Fixed by framing that as the prior
  scope-audit gate and keeping Batch A as the current `paper_fixture_breadth_batch_b` transition.
- Reproducibility/registry review found that this record was marked complete while verification and
  review entries were still pending. Fixed by recording concrete commands and results above.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/records/README.md`
- `docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-a.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only partial, fixture-scoped, command-only Batch A source/preprocess/intake/operator
  fixture-breadth accounting.
- Does not support broad mesh cleanup, general polygon intake, `paper_faithful_offline`, full CPD
  paper reproduction, package generation, Newton runtime support, real-USD evidence, benchmark
  evidence, collision-quality validation, deployment readiness, or safety certification.

## Next Action

- Proceed to `paper_fixture_breadth_batch_b`.
