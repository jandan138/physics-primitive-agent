# CPD Paper Mapped-Subset PrimitiveSpec Generation Preflight Contract Design

## Date

2026-05-17

## Context

The CPD paper offline lane currently closes
`paper_mapped_subset_primitivespec_validation_contract`. That gate validates the dry-run contract
shape for future PrimitiveSpec handoff, but it deliberately keeps all current PrimitiveSpec
candidates and generated PrimitiveSpec rows at zero because the current executable rows still
remain `trapezoidal_prism` / `offline_only_unmapped`.

The next gate is `paper_mapped_subset_primitivespec_generation_preflight_contract`. Its job is not
to generate real `PrimitiveSpec` objects. Its job is to perform one final command-only preflight
before any future generation gate: confirm the validation payload is the expected input, confirm
future family requirements remain limited to OBB/box, sphere, and capsule, confirm blocked and
no-op families still cannot generate, confirm current rows remain zero-candidate/no-op, and keep
all package/runtime/evaluation triggers false.

After this slice, the current next gate should be
`paper_mapped_subset_primitivespec_generation_contract`. That later gate may decide whether actual
PrimitiveSpec dictionaries can be emitted for a mapped subset. This slice must not emit them.
This is a new mapped-subset PrimitiveSpec gate and must not reuse the older
`paper_package_generation_contract` package-level gate.

## Design Choice

Use a conservative command-only generation-preflight contract:

1. Consume only `paper_mapped_subset_primitivespec_validation_contract`.
2. Validate that the upstream validation gate generated zero PrimitiveSpecs, zero CollisionPackages,
   and zero runtime-admissibility checks.
3. Validate the generation-preflight contract still has zero current generation candidates because
   current rows are unmapped/no-op.
4. Validate six family requirement rows:
   - OBB/box, sphere/sphere, and capsule/capsule are future mapped-family generation requirements.
   - capped cylinder and frustum remain blocked behind approximation policy.
   - trapezoidal prism remains no-op/unmapped for current rows.
5. Validate 16 current rows:
   - no validation pass;
   - no PrimitiveSpec candidate;
   - no generated PrimitiveSpec;
   - source ids preserved;
   - no silent drop;
   - required later gate points to this generation-preflight gate.
6. Emit generation-preflight result rows and coverage accounting, still with zero real
   PrimitiveSpec generation.
7. Advance the next gate to `paper_mapped_subset_primitivespec_generation_contract`.

This naming is intentionally cautious. "Generation preflight" means the lane has checked whether
generation prerequisites are structurally present. It does not mean generation, package conversion,
Newton compatibility, or runtime admissibility is supported.

## Payload Shape

The new payload will be stored in the top-level CPD paper offline report under
`paper_mapped_subset_primitivespec_generation_preflight_contract`.

Top-level fields:

- `gate_id`: `paper_mapped_subset_primitivespec_generation_preflight_contract`
- `gate_status`: `implemented_offline_primitivespec_generation_preflight_contract_only_partial`
- `closed_gate`: `paper_mapped_subset_primitivespec_generation_preflight_contract`
- `input_gate_id`: `paper_mapped_subset_primitivespec_validation_contract`
- `next_required_gate`: `paper_mapped_subset_primitivespec_generation_contract`
- `decision`: `remain_partial`
- `decision_reason`: `primitivespec_generation_preflight_contract_complete_primitivespec_generation_contract_missing`
- `artifact_kind`: `offline_primitivespec_generation_preflight_contract_not_primitivespec_not_collision_package`
- `generation_preflight_candidate_count`: `0`
- `generated_primitive_spec_count`: `0`
- `generated_collision_package_count`: `0`
- `runtime_admissibility_check_count`: `0`
- `real_usd_loaded`: `False`
- `benchmark_run`: `False`

The top-level report must also move forward:

- `next_required_gate`: `paper_mapped_subset_primitivespec_generation_contract`
- `failure_labels`: `["paper_mapped_subset_primitivespec_generation_contract_missing"]`
- `paper_faithfulness.missing_before_paper_faithful_offline`:
  `["paper_mapped_subset_primitivespec_generation_contract"]`
- `paper_faithfulness.implemented_output_contract_scope` includes
  `paper_mapped_subset_primitivespec_generation_preflight_contract`

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

## Generation-Preflight Rows

`primitive_spec_generation_preflight_requirement_rows` has six rows copied from validation rows
with explicit generation-preflight decisions.

Every family row must include:

- `primitive_spec_generation_preflight_row_id`
- `source_primitivespec_validation_row_id`
- `source_primitivespec_dry_run_row_id`
- `source_adapter_preflight_row_id`
- `source_candidate_matrix_row_id`
- `source_conversion_plan_row_id`
- `paper_primitive`
- `candidate_mapping_label`
- `validated_future_primitive_spec_kind`
- `input_primitivespec_validation_decision`
- `primitive_spec_generation_preflight_decision`
- `generation_preflight_candidate`
- `required_later_gate`

Expected decisions:

- `oriented_bounding_box`: `future_native_family_generation_requirement_preflighted`
- `sphere`: `future_native_family_generation_requirement_preflighted`
- `capsule`: `future_native_family_generation_requirement_preflighted`
- `capped_cylinder`: `blocked_approximation_policy_generation_preflight_recorded`
- `frustum`: `blocked_approximation_policy_generation_preflight_recorded`
- `trapezoidal_prism`: `noop_unmapped_family_generation_preflight_recorded`

`current_row_primitivespec_generation_preflight_rows` has 16 rows copied from validation rows.

Every current row remains:

- `primitive_spec_generation_preflight_decision`: `skip_unmapped_current_row_preflighted`
- `primitive_spec_generation_preflight_action`: `keep_offline`
- `primitive_spec_generation_preflight_passed`: `False`
- `primitive_spec_generation_candidate`: `False`
- `generated_primitive_spec`: `None`
- `silent_drop_detected`: `False`
- `required_later_gate`: `paper_mapped_subset_primitivespec_generation_contract`

Each current row must preserve these source ids:

- `primitive_spec_generation_preflight_row_id`
- `source_primitivespec_validation_row_id`
- `source_primitivespec_dry_run_row_id`
- `source_adapter_preflight_row_id`
- `source_candidate_matrix_row_id`
- `source_conversion_plan_row_id`
- `source_policy_decision_id`
- `source_adapter_decision_id`
- `source_output_id`
- `evidence_case_id`
- `offline_primitive_id`

## Validation Rules

The new builder validates its input before emitting the payload:

- input `gate_id` must be `paper_mapped_subset_primitivespec_validation_contract`;
- top-level generation/runtime/real-USD/benchmark/collision-quality/deployment flags must be false;
- `generated_primitive_spec_count`, `generated_collision_package_count`, and
  `runtime_admissibility_check_count` must be zero;
- `validated_primitive_spec_candidate_count` must be zero;
- `coverage_summary.validated_primitive_spec_candidate_record_count`,
  `coverage_summary.generated_primitive_spec_record_count`, and
  `coverage_summary.current_primitivespec_validation_pass_record_count` must be zero;
- family and current validation row ids must be unique and non-empty;
- family rows must match the expected ordered six-family contract:
  OBB/box, sphere/sphere, capsule/capsule, blocked capped cylinder, blocked frustum, and no-op
  trapezoidal prism;
- future-native family rows must have mapped future PrimitiveSpec kinds in the allowed set;
- blocked or no-op family rows must not claim a future PrimitiveSpec kind;
- current rows must have `primitive_spec_validation_passed == False`;
- current rows must have `primitive_spec_candidate == False`;
- current rows must have `generated_primitive_spec is None`;
- current rows must require `paper_mapped_subset_primitivespec_generation_preflight_contract`;
- family and current rows must preserve non-empty source ids needed for traceability;
- row-level generation/runtime/real-USD/benchmark/collision-quality/deployment flags must be false.
- emitted generation-preflight row ids must be unique and non-empty.

The emitted `coverage_summary` must contain:

- `primitive_spec_generation_preflight_requirement_row_count`: `6`
- `future_native_primitivespec_generation_preflight_count`: `3`
- `blocked_primitivespec_generation_preflight_requirement_count`: `2`
- `noop_primitivespec_generation_preflight_requirement_count`: `1`
- `current_row_primitivespec_generation_preflight_row_count`: `16`
- `current_primitivespec_generation_preflight_pass_record_count`: `0`
- `current_primitivespec_generation_preflight_noop_record_count`: `16`
- `generation_preflight_candidate_record_count`: `0`
- `generated_primitive_spec_record_count`: `0`

Validation failures raise `ValueError` with specific labels so tests can lock claim boundaries.

Required failure labels include:

- `primitivespec_generation_preflight_input_gate_id_mismatch`
- `generation_preflight_input_trigger_flag_true:<flag>`
- `generation_preflight_input_candidate_count_nonzero`
- `generation_preflight_input_generated_spec_nonzero`
- `generation_preflight_input_generated_collision_package_nonzero`
- `generation_preflight_coverage_count_mismatch:<field>`
- `generation_preflight_family_primitive_sequence_mismatch`
- `generation_preflight_future_mapping_label_mismatch:<paper_primitive>`
- `generation_preflight_family_contract_mismatch:<paper_primitive>`
- `generation_preflight_missing_validation_row_id:<field>`
- `generation_preflight_missing_current_row_source_id:<field>`
- `duplicate_primitivespec_validation_row_id`
- `duplicate_primitivespec_generation_preflight_row_id`
- `unknown_primitivespec_validation_family_decision:<decision>`
- `unknown_primitivespec_validation_current_decision:<decision>`
- `generation_preflight_current_row_required_later_gate_mismatch`

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
- `experiments/registry.yaml`
- `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-generation-preflight-contract.md`

Docs must state that generation preflight is implemented as report-only/offline, not real
PrimitiveSpec generation, not CollisionPackage generation, not package readiness, not Newton
runtime support, not real-USD evidence, not benchmark evidence, not collision-quality evidence,
not deployment readiness, and not safety certification.

## Non-Goals

- No real `PrimitiveSpec` dataclass instantiation.
- No `CollisionPackage` generation.
- No package adapter execution.
- No runtime admissibility checks.
- No Newton support claim or Newton execution.
- No real-USD loading.
- No benchmark or collision-quality measurement.
- No approximation policy for capped cylinder, frustum, or trapezoidal prism.
- No change to paper-faithful status; the report remains partial.

## Self-Review

- The design is one offline report gate, not a broad package-generation project.
- It keeps all current generation counts at zero.
- It names the next gate as a future generation contract but does not implement generation.
- It preserves the mapped-subset boundary: OBB/box, sphere, and capsule are future requirements;
  capped cylinder, frustum, and trapezoidal prism do not enter runtime or package generation here.
