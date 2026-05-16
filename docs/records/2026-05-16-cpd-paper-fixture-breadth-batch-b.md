# 2026-05-16 CPD Paper Fixture Breadth Batch B

## Date

2026-05-16

## Status

Complete

## Changes

- Added six Batch B primitive-fit breadth fixtures to the partial offline
  `cpd_paper_offline_report`: `paper_rotated_box_fit`, `paper_offset_sphere_fit`,
  `paper_off_axis_capsule_fit`, `paper_flat_capped_cylinder_axis_fit`,
  `paper_tapered_frustum_fit`, and `paper_asymmetric_trapezoid_fit`.
- Added generic sphere audit metadata for the distance between the paper OBB center and the
  assigned-point centroid.
- Updated the scope-audit `primitive_vocabulary_and_fit` evidence text to mention Batch B while
  keeping the report partial.
- Advanced `next_required_gate` to `paper_fixture_breadth_batch_c`.
- Kept the command offline-only: no package generation, Newton runtime execution, real USD, or
  benchmark work.

## Verification

- RED command:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_b tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_b tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result before implementation: failed because the six Batch B cases were absent and the next
    gate was still `paper_fixture_breadth_batch_b`.
- GREEN command:
  `python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_fixture_breadth_batch_b tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_next_gate_is_fixture_breadth_batch_c tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json -q`
  - Result after implementation: `3 passed`.
- Focused verification:
  `python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py::test_cli_run_cpd_paper_offline_report_emits_json tests/test_cli.py::test_cli_run_cpd_paper_offline_report_rejects_nonfinite_json -q`
  - Result: `11 passed`.
- CLI smoke and inspected JSON facts:
  `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report | python -c 'import json,sys; p=json.load(sys.stdin); cases={c["case_id"]:c for c in p["cases"]}; print(p["next_required_gate"]); print(p["paper_faithfulness"]["implemented_fixture_scope"][-3:]); print([cid for cid in cases if cid.startswith("paper_")][-6:]); print(cases["paper_offset_sphere_fit"]["primitive_fit_audit"]["candidates"][1]["dimensions"]["center_centroid_distance"]); print(cases["paper_tapered_frustum_fit"]["primitive_fit_audit"]["candidates"][4]["dimensions"]["top_radius"], cases["paper_tapered_frustum_fit"]["primitive_fit_audit"]["candidates"][4]["dimensions"]["bottom_radius"])'`
  - Result: printed `paper_fixture_breadth_batch_c`; printed implemented fixture scope ending in
    `paper_fixture_breadth_batch_b_primitive_fit`; printed all six Batch B case ids; printed
    offset sphere center/centroid distance `0.041350653479840654`; printed frustum top/bottom
    radii `1.1926860441876566 0.260768096208107`.
- Full tests:
  `python -m pytest -q`
  - Result: `419 passed in 83.81s`.
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

- Initial plan review found critical offset-sphere fixture symmetry, brittle frustum radius
  assertions, incomplete CLI/scope-audit test update instructions, and incomplete record/registry
  sequencing. The Batch B implementation plan was updated and re-reviewed with no remaining
  Critical or Important findings.
- RED test review found no Critical or Important findings in the Batch B test surface.
- Implementation precheck highlighted the same minimal implementation path used in this slice:
  deterministic synthetic mesh builders, Batch B case rows, Batch C next gate, and no runtime
  support changes.
- Final implementation review: no Critical, Important, or Minor findings. The reviewer found Batch
  B fixture rows and false runtime/package/asset/benchmark triggers correctly preserved.
- Final docs/claim review: no Critical findings. It found stale Batch A current-gate wording and
  pending record status while docs presented Batch B as implemented. The stale wording was made
  intermediate/historical, and this record now includes concrete verification with `Status:
  Complete`.
- Final reproducibility review: no Critical findings. It found the same pending record closure gap
  and a missing registry entry. This record now includes concrete command results, and
  `experiments/registry.yaml` has the Batch B entry.

## Fixture Scope

- Synthetic toy fixtures only.
- Primitive-fit audit rows only.
- No package generation, Newton runtime, real USD, benchmark, deployment, or safety-certification
  evidence.

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
- `docs/records/2026-05-16-cpd-paper-fixture-breadth-batch-b.md`
- `experiments/registry.yaml`

## Claim Impact

- Supports only partial, fixture-scoped, command-only Batch B primitive-fit breadth accounting.
- Does not support `paper_faithful_offline`, full CPD reproduction, package generation, Newton
  runtime support, real-USD evidence, benchmark evidence, collision-quality validation, deployment
  readiness, or safety certification.

## Next Action

- Proceed to `paper_fixture_breadth_batch_c`.
