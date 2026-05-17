# CPD Paper Mapped-Subset Adapter Preflight Contract Design

## Context

The current `cpd_paper_offline_report` closes
`paper_mapped_subset_conversion_candidate_matrix` as a command-only offline candidate matrix. That
matrix records three future native-family review rows (`oriented_bounding_box`, `sphere`,
`capsule`) and keeps all current 16 `trapezoidal_prism` / `offline_only_unmapped` records blocked
and offline. It records zero current package-conversion candidates.

The current next gate is `paper_mapped_subset_adapter_preflight_contract`.

## Goal

Add `paper_mapped_subset_adapter_preflight_contract` as the next command-only offline contract
payload inside `cpd_paper_offline_report`.

The payload must:

- consume `paper_mapped_subset_conversion_candidate_matrix`;
- record the adapter preflight requirements that a later package adapter would need;
- record six family-level preflight rows without treating future native-family rows as current
  package candidates;
- record 16 current-row preflight no-op rows for the current unmapped trapezoidal-prism records;
- keep current preflight pass count and package-candidate count at zero;
- keep the top-level report `partial`;
- keep `paper_faithful_offline_supported: false`;
- keep PrimitiveSpec generation, CollisionPackage generation, package generation, runtime
  admissibility, Newton runtime, real-USD, benchmark, collision-quality, deployment, and
  safety-certification triggers false.

## Non-Goals

This slice must not:

- construct `PrimitiveSpec` rows;
- construct a `CollisionPackage`;
- run a package-generation dry run that creates package artifacts;
- call or import Newton runtime code;
- perform runtime admissibility checks;
- approximate `capped_cylinder`, `frustum`, or `trapezoidal_prism`;
- silently drop unsupported current rows;
- load bed or Franka USD assets;
- run benchmarks;
- claim package readiness, package conversion execution, Newton support, runtime admissibility,
  collision quality, deployment readiness, or safety certification.

## Design Decision

Use `paper_mapped_subset_primitivespec_dry_run_contract` as the next gate after this preflight
contract.

Reason: the current candidate matrix has zero current package-conversion candidates. Advancing
directly to `paper_package_generation_contract` would be technically possible as a named future
boundary, but it risks implying that package generation is now the active work. A PrimitiveSpec
dry-run contract is more precise: it can define report-only schema expectations for a later
adapter path while still blocking actual `PrimitiveSpec` generation, `CollisionPackage`
generation, and Newton runtime work.

## Payload Shape

Top-level payload fields:

```text
gate_id: paper_mapped_subset_adapter_preflight_contract
gate_status: implemented_offline_adapter_preflight_contract_only_partial
closed_gate: paper_mapped_subset_adapter_preflight_contract
input_gate_id: paper_mapped_subset_conversion_candidate_matrix
next_required_gate: paper_mapped_subset_primitivespec_dry_run_contract
decision: remain_partial
decision_reason: adapter_preflight_contract_complete_primitivespec_dry_run_contract_missing
paper_faithful_offline_allowed: false
package_generation_allowed: false
artifact_kind: offline_adapter_preflight_contract_not_primitivespec_not_collision_package
schema_version: 1
source_scope: synthetic_toy_fixtures_only
implementation_boundary: offline_adapter_preflight_no_primitivespec_no_collision_package_no_newton
candidate_count_at_preflight: 0
preflight_action: no_op_keep_offline
```

Required false/zero flags:

```text
primitive_spec_generation_allowed: false
collision_package_generation_allowed: false
runtime_admissibility_supported: false
newton_runtime_allowed: false
approximation_policy_enabled: false
silent_drop_allowed: false
generated_primitive_spec_count: 0
generated_collision_package_count: 0
runtime_admissibility_check_count: 0
primitive_spec_generated: false
collision_package_generated: false
runtime_admissibility_checked: false
newton_support_claimed: false
approximation_policy_applied: false
real_usd_loaded: false
benchmark_run: false
collision_quality_measured: false
deployment_or_certification_claimed: false
package_generation_triggered: false
newton_runtime_triggered: false
real_usd_triggered: false
benchmark_triggered: false
```

## Contract Requirements

The preflight contract should record the requirements for any later adapter:

- input candidate matrix is present;
- input gate id equals `paper_mapped_subset_conversion_candidate_matrix`;
- input candidate matrix has six family rows;
- input candidate matrix has 16 current rows;
- current package-conversion candidate count is zero;
- current rows have stable source output ids and offline primitive ids;
- current rows preserve source evidence case ids;
- no current row is silently dropped;
- unsupported or unmapped rows stay offline until a separate mapping or approximation policy
  exists;
- all generation/runtime/real-USD/benchmark triggers from the input matrix remain false.

## Family Preflight Rows

Emit one row per paper primitive family.

| Paper primitive | Adapter preflight decision | Meaning |
| --- | --- | --- |
| `oriented_bounding_box` | `future_native_family_preflight_recorded_only` | Native-family metadata is recorded for a later contract, but no current row is package-ready. |
| `sphere` | `future_native_family_preflight_recorded_only` | Native-family metadata is recorded for a later contract, but no current row is package-ready. |
| `capsule` | `future_native_family_preflight_recorded_only` | Native-family metadata is recorded for a later contract, but no current row is package-ready. |
| `capped_cylinder` | `blocked_approximation_policy_missing` | No direct Newton primitive mapping is allowed by this gate. |
| `frustum` | `blocked_approximation_policy_missing` | No direct Newton primitive mapping is allowed by this gate. |
| `trapezoidal_prism` | `noop_current_unmapped_rows_keep_offline` | Current rows exist, but all remain offline and unmapped. |

Expected counts:

```text
family_preflight_requirement_row_count: 6
future_native_family_preflight_record_count: 3
blocked_family_preflight_record_count: 3
```

## Current Row Preflight Rows

Emit one row per current candidate-matrix row.

For the current 16 rows:

- `paper_primitive`: `trapezoidal_prism`
- `offline_runtime_kind_label`: `offline_only_unmapped`
- `input_candidate_matrix_decision`: `blocked_unmapped_current_rows`
- `adapter_preflight_decision`: `noop_keep_offline_unmapped_current_row`
- `current_package_conversion_candidate`: `false`
- `adapter_preflight_passed`: `false`
- `package_generation_enabled_by_this_gate`: `false`

Expected counts:

```text
current_row_adapter_preflight_row_count: 16
current_preflight_pass_record_count: 0
current_preflight_noop_record_count: 16
current_package_conversion_candidate_count: 0
package_candidate_record_count: 0
current_paper_primitive_distribution: {"trapezoidal_prism": 16}
current_runtime_kind_distribution: {"offline_only_unmapped": 16}
```

## Expected Evidence

After this slice, the report should show:

- `failure_labels == ["paper_mapped_subset_primitivespec_dry_run_contract_missing"]`;
- `next_required_gate == "paper_mapped_subset_primitivespec_dry_run_contract"`;
- `paper_faithfulness["implemented_output_contract_scope"]` includes
  `paper_mapped_subset_adapter_preflight_contract`;
- `paper_faithfulness["missing_before_paper_faithful_offline"]` equals
  `["paper_mapped_subset_primitivespec_dry_run_contract"]`;
- the preflight payload has six family preflight rows and 16 current row preflight rows;
- current preflight pass count is zero;
- package candidate record count remains zero.

## Test Strategy

Use TDD:

1. Add failing offline-report tests for the new payload and top-level gate transition.
2. Add failing tests for family preflight rows and counts.
3. Add failing tests for current-row no-op rows and zero current preflight passes.
4. Add failing tests that all generation/runtime/admissibility triggers remain false.
5. Add a CLI JSON regression check.
6. Implement the minimal offline payload and report wiring.
7. Run focused tests, docs validation, site claim validation, whitespace check, smoke, and full
   pytest.

## Claim Boundary

Allowed wording: command-only offline mapped-subset adapter preflight contract and no-op
accounting.

Forbidden wording: package readiness, package conversion execution, PrimitiveSpec generation,
CollisionPackage generation, Newton support, runtime admissibility support, approximation support,
full CPD reproduction, collision-quality evidence, benchmark evidence, deployment readiness, or
safety certification.
