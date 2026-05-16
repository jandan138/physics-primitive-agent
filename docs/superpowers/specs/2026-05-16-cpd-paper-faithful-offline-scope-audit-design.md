# CPD Paper Faithful Offline Scope Audit Design

## Context

The current `cpd_paper_offline_report` has advanced through the exact-coordinate
duplicate-vertex preprocessing fixture. Its next required gate is now
`paper_faithful_offline_scope_audit`.

That gate must not silently upgrade the lane to `paper_faithful_offline`. Its job is to compare
the current named-fixture report against the gap matrix and offline-lane spec, then make a
reviewable decision about whether the current evidence is still partial.

## Chosen Approach

Add one top-level `paper_faithful_offline_scope_audit` object to the command-only
`cpd_paper_offline_report`.

The audit is offline-only. It does not generate packages, call Newton, load real USD assets, run
benchmarks, or change primitive selection. It is a report gate that answers:

```text
Can the current fixture-scoped offline paper lane be called paper_faithful_offline?
```

For this slice, the answer must be `false`. The report should remain `status: partial` and
`paper_faithful_offline_supported: false`.

## Scope-Audit Payload

The top-level payload should contain:

```text
paper_faithful_offline_scope_audit
```

with these required fields:

- `audit_scope: fixture_scoped_offline_paper_lane`;
- `audit_version: 1`;
- `decision: remain_partial`;
- `paper_faithful_offline_allowed: false`;
- `decision_reason: fixture_scope_still_partial`;
- `criteria`;
- `blocking_criteria_ids`;
- `package_generation_triggered: false`;
- `newton_runtime_triggered: false`;
- `real_usd_triggered: false`;
- `benchmark_triggered: false`.

Each `criteria` row must include:

- `criterion_id`;
- `paper_requirement`;
- `current_evidence`;
- `status`;
- `surrogate_or_paper_faithful`;
- `blocking_for_paper_faithful_offline`;
- `claim_boundary`;
- `next_action`.

Allowed `status` values for this audit are:

- `implemented_fixture_scope`;
- `partial_fixture_scope`;
- `not_started`;
- `blocked_until_later_gate`.

Allowed `surrogate_or_paper_faithful` values are:

- `fixture_scoped_paper_shaped`;
- `paper_aligned_boundary`;
- `not_paper_faithful`;
- `out_of_offline_scope`.

No row may use `paper_faithful_offline` in the `status` field or the
`surrogate_or_paper_faithful` field in this slice.

## Required Criteria Rows

The first scope audit should use these exact criterion ids, in order:

1. `source_mesh_and_preprocessing_policy`;
2. `source_face_intake_policy`;
3. `operator_q_audit`;
4. `primitive_vocabulary_and_fit`;
5. `paper_collapse_cost_and_weighting`;
6. `greedy_priority_queue_trace`;
7. `target_count_and_threshold_stop`;
8. `component_pair_edge_handling`;
9. `enclosed_primitive_postprocess`;
10. `report_schema_tests_and_records`;
11. `package_generation_boundary`;
12. `newton_runtime_boundary`;
13. `real_usd_boundary`;
14. `benchmark_evaluation_boundary`.

The blocking rows should be:

```text
source_mesh_and_preprocessing_policy
source_face_intake_policy
operator_q_audit
primitive_vocabulary_and_fit
paper_collapse_cost_and_weighting
greedy_priority_queue_trace
target_count_and_threshold_stop
component_pair_edge_handling
enclosed_primitive_postprocess
```

The package-generation, Newton, real-USD, and benchmark rows are boundary rows. They are
non-blocking for `paper_faithful_offline` because that status is offline and fixture-scoped. They
remain blockers for runtime, real-asset, benchmark, collision-quality, deployment, and safety
claims.

## Canonical Criteria Table

The implementation should use these exact row meanings. String wording can be wrapped for source
formatting, but it should not change substance without updating tests and records.

| Criterion id | Paper requirement | Current evidence | Status | Surrogate/paper field | Blocking? | Claim boundary | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `source_mesh_and_preprocessing_policy` | Mesh vertices/faces plus duplicate or overlapped vertex preprocessing and source-face remap. | Triangle toy fixtures, fan-triangulated source-face fixtures, and one exact-coordinate duplicate-vertex fixture; broader unclean-mesh policy is absent. | `partial_fixture_scope` | `fixture_scoped_paper_shaped` | true | Exact-overlap toy preprocessing only; no robust arbitrary mesh cleanup. | Expand preprocessing/source-mesh fixture breadth before stronger wording. |
| `source_face_intake_policy` | Preserve face ownership across triangle, quad, and polygon source faces. | One quad and one five-vertex polygon fan-triangulation fixture with source-face remap and operator ownership accounting. | `partial_fixture_scope` | `fixture_scoped_paper_shaped` | true | Source-face intake is toy-scoped, not a general polygon mesh implementation. | Add broader source-face cases only after a fixture-breadth plan. |
| `operator_q_audit` | Per-face and merged-group `Q` operators with eigen decomposition. | Per-face and merged-group operator rows exist for named toy fixtures, including source-face aggregate rows. | `partial_fixture_scope` | `fixture_scoped_paper_shaped` | true | Operator evidence is named-fixture audit data, not full paper decomposition. | Expand operator degeneracy and fixture coverage. |
| `primitive_vocabulary_and_fit` | Audit the six paper primitive candidates, containment, formulas, axis policies, and primitive weights. | All six paper primitive names have fixture-scoped audit rows, but capped cylinder, frustum, and trapezoidal prism remain offline-only and fitting breadth is limited. | `partial_fixture_scope` | `fixture_scoped_paper_shaped` | true | Primitive rows are audit rows, not Newton runtime support or collision-quality evidence. | Expand fitting fixtures and paper-specific invariants. |
| `paper_collapse_cost_and_weighting` | Use paper base collapse cost, separate weighted priority cost, and no intersection-volume primary cost. | One two-face cost fixture plus priority-queue event fields record base and weighted costs. | `partial_fixture_scope` | `fixture_scoped_paper_shaped` | true | Cost rows are toy accounting, not optimizer or benchmark evidence. | Broaden merge-cost fixtures and threshold cases. |
| `greedy_priority_queue_trace` | Initialize adjacent face-pair candidates, pop minimum priority cost, handle stale entries, and merge greedily. | Topology, deduplicated-topology, and component-pair toy traces exist with deterministic queue keys. | `partial_fixture_scope` | `fixture_scoped_paper_shaped` | true | Search traces are toy-scoped and do not prove merge-policy superiority. | Expand priority-queue fixtures before stronger wording. |
| `target_count_and_threshold_stop` | Stop at target primitive count or when valid threshold policy blocks remaining candidates. | Target-count traces and one zero finite-threshold component-pair block exist. | `partial_fixture_scope` | `fixture_scoped_paper_shaped` | true | Threshold evidence is narrow toy accounting. | Add fixture-breadth plan for target/threshold combinations. |
| `component_pair_edge_handling` | Insert pairwise component candidates when disconnected topology cannot reach the target. | One accepted threshold-disabled component-pair trace and one finite-threshold blocked trace exist. | `partial_fixture_scope` | `fixture_scoped_paper_shaped` | true | Component merging evidence is diagnostic accounting, not broad asset evidence. | Decide whether capped skipped-pair fixtures are needed. |
| `enclosed_primitive_postprocess` | Remove primitives enclosed by other primitives. | One explicit identity-axis nested OBB cull fixture exists; generated-search postprocess breadth is absent. | `partial_fixture_scope` | `fixture_scoped_paper_shaped` | true | Postprocess cull evidence is one offline canary, not a general containment library. | Expand postprocess fixtures if required by scope audit follow-up. |
| `report_schema_tests_and_records` | Keep report schema, tests, registry, and dated records reproducible. | This slice adds RED/GREEN tests, final verification, registry entry, and a dated record. | `implemented_fixture_scope` | `paper_aligned_boundary` | false | Reproducibility evidence supports the audit record only, not stronger algorithm claims. | Keep records updated for every future gate. |
| `package_generation_boundary` | Keep offline paper mechanics separate from package conversion. | The report records package-generation false triggers and no `CollisionPackage` conversion. | `blocked_until_later_gate` | `out_of_offline_scope` | false | Package generation is a later explicit adapter gate. | Add package conversion only after a changed offline package boundary exists. |
| `newton_runtime_boundary` | Keep offline paper mechanics separate from Newton runtime diagnostics. | The report records Newton false triggers and no runtime execution. | `blocked_until_later_gate` | `out_of_offline_scope` | false | Newton support requires separate mapping and diagnostic records. | Run Newton only after package conversion and runtime admissibility are recorded. |
| `real_usd_boundary` | Keep toy fixture audit separate from real asset evidence. | The report records real-USD false triggers and uses synthetic toy fixtures only. | `blocked_until_later_gate` | `out_of_offline_scope` | false | Real-USD evidence requires separate asset manifests and records. | Defer bed/Franka or other real assets until a package-changing gate exists. |
| `benchmark_evaluation_boundary` | Keep paper benchmark evaluation separate from offline paper-mechanics audit. | The report records benchmark false triggers and no timing, surface-distance, byte-cost, or baseline comparison metrics. | `blocked_until_later_gate` | `out_of_offline_scope` | false | Benchmark evidence is not required for bounded offline status and is not claimed here. | Defer benchmarks until offline decomposition and runtime package gates are ready. |

## Gate Advancement

After this slice:

- top-level `failure_labels` should become
  `["paper_fixture_breadth_expansion_missing"]`;
- top-level `next_required_gate` should become `paper_fixture_breadth_expansion_plan`;
- `paper_faithfulness.implemented_fixture_scope` should include
  `paper_faithful_offline_scope_audit`;
- `paper_faithfulness.missing_before_paper_faithful_offline` should become
  `["paper_fixture_breadth_expansion"]`;
- `status` must remain `partial`;
- `paper_faithful_offline_supported` must remain `false`.

This means the scope audit is complete, but it rejects stronger paper-faithfulness wording until
the next offline fixture-breadth plan is explicit.

## Tests

Add RED/GREEN tests that verify:

- top-level failure label and next gate advance to fixture-breadth expansion;
- `paper_faithfulness.missing_before_paper_faithful_offline` advances to
  `["paper_fixture_breadth_expansion"]`;
- `paper_faithful_offline_scope_audit` exists;
- the scope audit decision is `remain_partial`;
- `paper_faithful_offline_allowed` is `false`;
- all fourteen criteria rows match the canonical table in exact order;
- every criterion row has the required schema fields;
- no criterion row uses `paper_faithful_offline` as `status` or
  `surrogate_or_paper_faithful`;
- the expected blocking criteria ids are present in exact order;
- report schema/tests/records is non-blocking;
- package, Newton, real-USD, and benchmark boundary rows are blocked until later gates but
  non-blocking for the offline scope decision;
- package/Newton/real-USD/benchmark triggers stay false;
- `paper_faithfulness.implemented_fixture_scope` includes
  `paper_faithful_offline_scope_audit`;
- `status` remains `partial`;
- `paper_faithful_offline_supported` remains `false`;
- CLI JSON includes the new audit and gate fields.

## Documentation And Records

Update:

- `docs/index.md`;
- `docs/deepdive/evidence-status.md`;
- `docs/reference/claim-boundaries.md`;
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`;
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/records/README.md`;
- `experiments/registry.yaml`;
- a new dated record under `docs/records/`.

The wording must say this is a scope audit that keeps the lane partial. It must not claim
`paper_faithful_offline`, full CPD reproduction, package generation, Newton runtime support,
real-USD evidence, benchmark evidence, collision-quality validation, deployment readiness, or
safety certification.

## Verification

Required verification:

- focused RED/GREEN pytest for scope audit assertions and CLI JSON;
- `python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report`;
- `python -m pytest -q`;
- `python scripts/validate_docs.py`;
- `python scripts/validate_site_claims.py`;
- `git diff --check`.
