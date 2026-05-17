# CPD Paper Mapped-Subset PrimitiveSpec Dry-Run Contract Design

## Date

2026-05-17

## Context

The current CPD paper offline lane has closed the adapter-preflight gate with
`paper_mapped_subset_adapter_preflight_contract`. That payload is deliberately a command-only
contract: it records six family preflight rows, records 16 current no-op rows, keeps current
package-conversion candidates at zero, and keeps PrimitiveSpec generation, CollisionPackage
generation, runtime admissibility, Newton execution, real-USD loading, and benchmarks disabled.

The next gate is `paper_mapped_subset_primitivespec_dry_run_contract`. Its job is not to generate
`PrimitiveSpec` objects. Its job is to define the report-only dry-run contract that a later
PrimitiveSpec generation gate would have to satisfy.

## Design Choice

Use the conservative offline contract path:

1. Consume only `paper_mapped_subset_adapter_preflight_contract`.
2. Validate that the upstream preflight still has zero current package candidates and zero current
   preflight passes.
3. Record the future native-family PrimitiveSpec shape requirements for the three mapped paper
   families: OBB -> `box`, sphere -> `sphere`, and capsule -> `capsule`.
4. Keep capped cylinder and frustum blocked behind an explicit approximation policy.
5. Keep all current trapezoidal-prism / `offline_only_unmapped` rows as no-op offline rows.
6. Keep generated PrimitiveSpec count at zero.
7. Advance the next gate to `paper_mapped_subset_primitivespec_validation_contract`.

This route is intentionally slower than jumping straight to a CollisionPackage dry-run. The current
lane has no eligible current rows, so a direct package dry-run would risk implying package readiness
from an empty set. A separate validation contract can later check dry-run schema fields, finite
numeric requirements, axis/dimension requirements, source ids, and zero-candidate behavior without
emitting real specs.

## Payload Shape

The new payload will be stored in the top-level CPD paper offline report under
`paper_mapped_subset_primitivespec_dry_run_contract`.

Top-level fields:

- `gate_id`: `paper_mapped_subset_primitivespec_dry_run_contract`
- `gate_status`: `implemented_offline_primitivespec_dry_run_contract_only_partial`
- `closed_gate`: `paper_mapped_subset_primitivespec_dry_run_contract`
- `input_gate_id`: `paper_mapped_subset_adapter_preflight_contract`
- `next_required_gate`: `paper_mapped_subset_primitivespec_validation_contract`
- `decision`: `remain_partial`
- `decision_reason`: `primitivespec_dry_run_contract_complete_primitivespec_validation_contract_missing`
- `artifact_kind`: `offline_primitivespec_dry_run_contract_not_primitivespec_not_collision_package`
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

## Rows

`primitive_spec_dry_run_requirement_rows` has six rows copied from the adapter-preflight family
requirements:

- `oriented_bounding_box`: records future dry-run shape requirements for runtime kind `box`.
- `sphere`: records future dry-run shape requirements for runtime kind `sphere`.
- `capsule`: records future dry-run shape requirements for runtime kind `capsule`.
- `capped_cylinder`: remains blocked because approximation policy is missing.
- `frustum`: remains blocked because approximation policy is missing.
- `trapezoidal_prism`: remains no-op because current rows are unmapped/offline-only.

`current_row_primitivespec_dry_run_rows` has 16 rows copied from the adapter-preflight current rows.
Every current row is:

- `primitive_spec_dry_run_decision`: `skip_unmapped_current_row`
- `primitive_spec_dry_run_action`: `keep_offline`
- `primitive_spec_dry_run_passed`: `False`
- `primitive_spec_candidate`: `False`
- `generated_primitive_spec`: `None`

Each current row preserves source ids from the preflight row so reviewers can trace it back to the
candidate matrix, conversion plan, adapter decision, decomposition output, evidence case, and
offline primitive.

## Validation

The new builder validates its input before emitting the payload:

- input `gate_id` must be `paper_mapped_subset_adapter_preflight_contract`;
- upstream top-level generation/runtime/real-USD/benchmark flags must be false;
- `candidate_count_at_preflight`, `current_package_conversion_candidate_count`,
  `current_preflight_pass_record_count`, and `package_candidate_record_count` must all be zero;
- family and current row ids must be unique;
- family decisions must be known adapter-preflight decisions;
- current rows must have `adapter_preflight_passed == False`;
- current rows must have `current_package_conversion_candidate == False`;
- current rows must require `paper_mapped_subset_primitivespec_dry_run_contract`;
- current rows must preserve the source ids needed for traceability.

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
- `docs/records/2026-05-17-cpd-paper-mapped-subset-primitivespec-dry-run-contract.md`
- `experiments/registry.yaml`

The docs must say this is report-only dry-run contract accounting. They must not say that real
`PrimitiveSpec` objects were generated, that the package path is ready, or that Newton can consume
the result.

## Claim Boundary

Allowed wording:

- command-only offline PrimitiveSpec dry-run contract;
- report-only PrimitiveSpec dry-run requirements;
- zero current PrimitiveSpec candidates;
- current unmapped rows remain offline/no-op;
- next gate is `paper_mapped_subset_primitivespec_validation_contract`.

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

Three review angles were considered before this design:

- claim-boundary review: keep "PrimitiveSpec dry-run" as requirements/accounting, not generation;
- implementation review: mirror the adapter-preflight validation style and keep all candidates zero;
- paper-story review: add a validation-contract gate before any actual PrimitiveSpec or package
  generation gate.

The design follows the conservative paper-story review because the current mapped-subset lane has
zero eligible current rows.
