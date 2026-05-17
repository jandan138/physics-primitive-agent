# CPD Paper Mapped-Subset PrimitiveSpec Validation Contract Design

## Date

2026-05-17

## Context

Before this slice, the CPD paper offline lane closed only
`paper_mapped_subset_primitivespec_dry_run_contract`. That gate recorded the shape of a future
PrimitiveSpec handoff, but deliberately kept current PrimitiveSpec candidates at zero because all
current rows remain `trapezoidal_prism` / `offline_only_unmapped`.

This slice implements `paper_mapped_subset_primitivespec_validation_contract`. Its job is not to
create real `PrimitiveSpec` objects. Its job is to validate that the dry-run contract is
claim-bounded before a later generation gate: row ids are unique, required schema fields are
present, allowed future mapping-candidate labels are limited to the planned mapped subset, current
no-op rows preserve source traceability, and all generation/runtime triggers remain false. After
this slice, the current next gate is
`paper_mapped_subset_primitivespec_generation_preflight_contract`.

## Design Choice

Use a conservative command-only validation contract:

1. Consume only `paper_mapped_subset_primitivespec_dry_run_contract`.
2. Validate that the upstream dry-run gate has zero current candidates, zero generated
   PrimitiveSpecs, zero generated CollisionPackages, and zero runtime-admissibility checks.
3. Validate the declared PrimitiveSpec field list against the required dry-run field set.
4. Validate the declared future mapping-candidate labels against the mapped subset:
   `box`, `sphere`, and `capsule`.
5. Validate six family requirement rows: three future native shape rows, two blocked approximation
   rows, and one no-op unmapped current-family row.
6. Validate 16 current no-op rows: no pass, no candidate, no generated spec, source ids preserved,
   and no silent drop.
7. Emit validation-result rows and coverage accounting, still with zero real PrimitiveSpec
   generation.
8. Advance the next gate to `paper_mapped_subset_primitivespec_generation_preflight_contract`.

This next gate name is intentionally cautious. It says the lane has validated a dry-run contract,
not that generation is ready or that a nonzero package exists.

## Payload Shape

The new payload will be stored in the top-level CPD paper offline report under
`paper_mapped_subset_primitivespec_validation_contract`.

Top-level fields:

- `gate_id`: `paper_mapped_subset_primitivespec_validation_contract`
- `gate_status`: `implemented_offline_primitivespec_validation_contract_only_partial`
- `closed_gate`: `paper_mapped_subset_primitivespec_validation_contract`
- `input_gate_id`: `paper_mapped_subset_primitivespec_dry_run_contract`
- `next_required_gate`: `paper_mapped_subset_primitivespec_generation_preflight_contract`
- `decision`: `remain_partial`
- `decision_reason`: `primitivespec_validation_contract_complete_primitivespec_generation_preflight_contract_missing`
- `artifact_kind`: `offline_primitivespec_validation_contract_not_primitivespec_not_collision_package`
- `validated_primitive_spec_candidate_count`: `0`
- `generated_primitive_spec_count`: `0`
- `generated_collision_package_count`: `0`
- `runtime_admissibility_check_count`: `0`

The payload keeps all generation/runtime booleans false:

- `primitive_spec_generated`
- `collision_package_generated`
- `runtime_admissibility_checked`
- `newton_support_claimed`
- `approximation_policy_applied`
- `package_generation_triggered`
- `newton_runtime_triggered`
- `real_usd_triggered`
- `benchmark_triggered`
- `collision_quality_measured`
- `deployment_or_certification_claimed`

## Validation Rows

`primitive_spec_validation_requirement_rows` has six rows copied from
`primitive_spec_dry_run_requirement_rows`.

Expected decisions:

- `oriented_bounding_box`: `future_native_family_primitivespec_shape_requirement_validated`
- `sphere`: `future_native_family_primitivespec_shape_requirement_validated`
- `capsule`: `future_native_family_primitivespec_shape_requirement_validated`
- `capped_cylinder`: `blocked_approximation_policy_validation_recorded`
- `frustum`: `blocked_approximation_policy_validation_recorded`
- `trapezoidal_prism`: `noop_unmapped_family_validation_recorded`

`current_row_primitivespec_validation_rows` has 16 rows copied from
`current_row_primitivespec_dry_run_rows`.

Every current row remains:

- `primitive_spec_validation_decision`: `skip_unmapped_current_row_validated`
- `primitive_spec_validation_action`: `keep_offline`
- `primitive_spec_validation_passed`: `False`
- `primitive_spec_candidate`: `False`
- `generated_primitive_spec`: `None`
- `silent_drop_detected`: `False`

Each current row must preserve source ids from the dry-run row:

- `source_candidate_matrix_row_id`
- `source_conversion_plan_row_id`
- `source_policy_decision_id`
- `source_adapter_decision_id`
- `source_output_id`
- `evidence_case_id`
- `offline_primitive_id`

## Validation Rules

The new builder validates its input before emitting the payload:

- input `gate_id` must be `paper_mapped_subset_primitivespec_dry_run_contract`;
- top-level generation/runtime/real-USD/benchmark/collision-quality/deployment flags must be false;
- `candidate_count_at_dry_run`, `generated_primitive_spec_count`,
  `generated_collision_package_count`, and `runtime_admissibility_check_count` must be zero;
- `coverage_summary.primitive_spec_candidate_record_count`,
  `coverage_summary.generated_primitive_spec_record_count`, and
  `coverage_summary.current_primitivespec_dry_run_pass_record_count` must be zero;
- `primitive_spec_dry_run_contract.required_primitive_spec_fields` must exactly match the
  repository's required field list;
- `primitive_spec_dry_run_contract.allowed_future_runtime_kinds` must be treated as future
  mapping-candidate labels `box`, `sphere`, and `capsule`;
- family and current dry-run row ids must be unique;
- family rows must match the expected ordered six-family contract:
  OBB/box, sphere/sphere, capsule/capsule, blocked capped cylinder, blocked frustum, and no-op
  trapezoidal prism;
- future-native family rows must have a mapped future PrimitiveSpec kind in the allowed set;
- future-native family rows must keep their mapping-candidate labels aligned with the future kind;
- blocked or no-op family rows must not claim a future PrimitiveSpec kind;
- family and current rows must preserve non-empty source ids needed for traceability;
- current rows must have `primitive_spec_dry_run_passed == False`;
- current rows must have `primitive_spec_candidate == False`;
- current rows must have `generated_primitive_spec is None`;
- current rows must require `paper_mapped_subset_primitivespec_validation_contract`;

Validation failures raise `ValueError` with specific labels so tests can lock claim boundaries.

## Documentation Updates

Update these docs and records:

- `README.md`
- `docs/index.md`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/reference/cpd-paper-fixture-breadth-expansion-plan.md`
- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/records/README.md`
- `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-validation-contract.md`
- `experiments/registry.yaml`

The docs must say this is report-only validation of a dry-run contract. They must not say that real
`PrimitiveSpec` objects were generated, that the package path is ready, or that Newton can consume
the result.

## Claim Boundary

Allowed wording:

- command-only offline PrimitiveSpec validation contract;
- validation of PrimitiveSpec dry-run requirements;
- zero validated current PrimitiveSpec candidates;
- current unmapped rows remain offline/no-op;
- next gate is `paper_mapped_subset_primitivespec_generation_preflight_contract`.

Disallowed wording:

- PrimitiveSpec generation;
- PrimitiveSpec readiness;
- CollisionPackage generation;
- package readiness;
- package conversion execution;
- runtime admissibility;
- Newton support or Newton execution;
- approximation support for capped cylinder or frustum;
- real-USD evidence;
- benchmark evidence;
- collision-quality evidence;
- deployment readiness or safety certification.

## Review Notes

The validation gate is deliberately one step before any real generation gate. In the CPD paper
story, this narrows the gap between a paper-shaped offline report and a later package path, but it
does not close the package path. The output should be treated as audit evidence that the dry-run
contract has no hidden candidate, source-traceability, or claim-boundary leak.
