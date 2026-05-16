# CPD Paper Source Policy Generalization Design

## Context

The `cpd_paper_offline_report` currently has named synthetic fixture breadth for the paper-lane
source mesh, preprocessing, source-face intake, and operator `Q` criteria. The latest planning gate
closed `paper_faithful_offline_generalization_plan` and named
`paper_generalization_batch_a_source_policy` as the first implementation slice.

This slice should close only `paper_generalization_batch_a_source_policy`. It must not claim
`paper_faithful_offline`, full CPD reproduction, robust mesh cleanup, package generation, Newton
runtime support, real-USD evidence, benchmark evidence, or collision-quality validation.

## Chosen Approach

Add one top-level offline report payload:

```text
paper_generalization_batch_a_source_policy
```

The payload should summarize source-policy evidence already present in the named fixture cases:

- `paper_mixed_face_preprocess_operator`;
- `paper_degenerate_preprocess_face_drop`;
- `paper_concave_polygon_rejected`.

This is a report-only policy matrix. It does not add new geometry, a mesh preprocessor, a package
adapter, a Newton path, a real-asset runner, or benchmark logic.

## Payload Boundary

The payload should record:

- `gate_id: paper_generalization_batch_a_source_policy`;
- `gate_status: implemented_offline_report_only_partial`;
- `closed_gate: paper_generalization_batch_a_source_policy`;
- `next_required_gate: paper_generalization_batch_b_primitive_fit_engine`;
- `decision: remain_partial`;
- `paper_faithful_offline_allowed: false`;
- `source_scope: synthetic_in_memory_source_mesh_policy_matrix`;
- `implementation_boundary: offline_report_only_no_package_or_newton`;
- false triggers for package generation, Newton runtime, real USD, and benchmark work.

It should define four policy sections:

1. `source_mesh_contract`: variable-arity source faces can be represented in the report, and source
   face ids remain distinct from generated triangle ids.
2. `preprocessing_policy`: exact-coordinate, first-occurrence deduplication only, with
   `distance_tolerance: 0.0`; degenerate faces after deduplication are dropped from executable rows.
3. `source_face_intake_policy`: planar, convex, non-degenerate, consistently wound source faces use
   fan triangulation from the first vertex; concave source polygons stay explicitly unsupported.
4. `operator_policy`: compute `Q` on executable triangles, then aggregate source-face `Q` rows by
   summing generated triangle rows.

It should include a `policy_matrix` with three rows:

| Row | Evidence case | Meaning |
| --- | --- | --- |
| `accepted_mixed_triangle_quad_polygon_exact_dedup` | `paper_mixed_face_preprocess_operator` | Accepted mixed triangle/quad/convex polygon source mesh with exact duplicate coordinates. |
| `accepted_degenerate_after_exact_dedup_drop` | `paper_degenerate_preprocess_face_drop` | Accepted preprocessing path where one source face becomes degenerate and is dropped. |
| `rejected_concave_polygon` | `paper_concave_polygon_rejected` | Unsupported concave polygon intake path with no executable primitive/operator rows. |

## Gate Semantics

After this slice:

- top-level `failure_labels` should remove
  `paper_generalization_batch_a_source_policy_missing`;
- top-level `next_required_gate` should become
  `paper_generalization_batch_b_primitive_fit_engine`;
- `paper_faithfulness.missing_before_paper_faithful_offline` should list only B-E gates;
- `paper_faithfulness.implemented_generalization_scope` should include
  `paper_generalization_batch_a_source_policy`;
- `paper_faithfulness.implemented_planning_scope` should still include
  `paper_faithful_offline_generalization_plan`;
- `paper_faithful_offline_supported` should remain `false`;
- `status` should remain `partial`.

The nested `paper_fixture_breadth_completion_review` can remain historically pointed at
`paper_faithful_offline_generalization_plan`, because that review closed a previous gate. The
current top-level and current generalization-plan metadata must point at Batch B after this slice.

## Test Requirements

Add RED tests before implementation:

- one report-level test that asserts Batch A is closed, B-E remain missing, the source-policy
  payload exists, and all runtime/package/asset/benchmark triggers remain false;
- one consistency test that the policy-matrix rows match the referenced fixture case payloads for
  source mesh, preprocessing, source-face intake, operator rows, primitive-fit source ids, and the
  unsupported concave boundary;
- update existing report and CLI expectations from A-E missing to B-E missing;
- update current top-level next-gate expectations from Batch A to Batch B while keeping historical
  nested fixture-breadth review expectations unchanged.

## Documentation Requirements

Update:

- `README.md`;
- `docs/index.md`;
- `docs/deepdive/evidence-status.md`;
- `docs/reference/claim-boundaries.md`;
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`;
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`;
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/records/README.md`;
- `experiments/registry.yaml`;
- a new dated record under `docs/records/`.

## Claim Boundaries

Allowed wording:

- "offline source-policy generalization report";
- "source-policy matrix for deterministic synthetic meshes";
- "closes only `paper_generalization_batch_a_source_policy`";
- "next required gate is `paper_generalization_batch_b_primitive_fit_engine`";
- "report remains partial."

Disallowed wording:

- `paper_faithful_offline` support;
- full CPD paper reproduction;
- robust arbitrary mesh cleanup;
- general polygon mesh intake;
- primitive-fit/search/postprocess/package generalization;
- Newton runtime support;
- real-USD evidence;
- benchmark or collision-quality evidence;
- deployment readiness or safety certification.

## Verification

Required verification:

```bash
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_source_policy_generalization_gate -q
python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_source_policy_generalization_rows_match_case_payloads -q
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
python -m pytest -q
python scripts/validate_docs.py
python scripts/validate_site_claims.py
git diff --check
```
