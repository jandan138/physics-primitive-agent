# CPD Paper Mapped-Subset Conversion Candidate Matrix Design

## Context

The current `cpd_paper_offline_report` closes
`paper_package_conversion_mapped_subset_plan` as a command-only offline planning table. That
payload identifies `oriented_bounding_box`, `sphere`, and `capsule` as future native-family review
rows, keeps `capped_cylinder`, `frustum`, and `trapezoidal_prism` behind explicit mapping or
approximation policy, and records all current 16 `trapezoidal_prism` / `offline_only_unmapped`
rows as kept offline.

The current next gate is `paper_mapped_subset_conversion_candidate_matrix`.

## Goal

Add `paper_mapped_subset_conversion_candidate_matrix` as an offline-only review payload inside
`cpd_paper_offline_report`.

The payload must:

- consume `paper_package_conversion_mapped_subset_plan`;
- convert the plan into explicit family and current-record review rows;
- keep current package-conversion candidate count at zero;
- keep all 16 current `trapezoidal_prism` / `offline_only_unmapped` rows visible as blocked and
  offline;
- keep the top-level report `partial`;
- keep `paper_faithful_offline_supported: false`;
- keep package generation, PrimitiveSpec generation, CollisionPackage generation, runtime
  admissibility, Newton runtime, real-USD, benchmark, collision-quality, deployment, and
  safety-certification triggers false.

## Non-Goals

This slice must not:

- construct `PrimitiveSpec` rows;
- construct a `CollisionPackage`;
- call or import Newton runtime code;
- perform runtime admissibility checks;
- approximate `capped_cylinder`, `frustum`, or `trapezoidal_prism`;
- silently drop unsupported current rows;
- load bed or Franka USD assets;
- run benchmarks;
- claim package readiness, Newton support, runtime support, collision quality, deployment, or
  safety certification.

## Candidate Matrix Model

The word "candidate" in this gate means review candidate, not package-ready candidate. To avoid
claim drift, the payload must distinguish:

- `future_family_review_candidate`: a paper primitive family may be reviewed in a later native
  mapping contract, but has no current package-conversion row;
- `current_package_conversion_candidate`: a concrete current row can enter a later package
  conversion contract.

For the current report:

```text
future_family_review_candidate_count: 3
current_package_conversion_candidate_count: 0
```

## Payload Shape

Top-level payload fields:

```text
gate_id: paper_mapped_subset_conversion_candidate_matrix
gate_status: implemented_offline_candidate_matrix_only_partial
closed_gate: paper_mapped_subset_conversion_candidate_matrix
input_gate_id: paper_package_conversion_mapped_subset_plan
next_required_gate: paper_mapped_subset_adapter_preflight_contract
decision: remain_partial
decision_reason: candidate_matrix_complete_adapter_preflight_contract_missing
paper_faithful_offline_allowed: false
package_generation_allowed: false
artifact_kind: offline_mapped_subset_candidate_matrix_not_collision_package
schema_version: 1
source_scope: synthetic_toy_fixtures_only
implementation_boundary: offline_candidate_matrix_no_primitivespec_no_collision_package_no_newton
```

The next gate is intentionally `paper_mapped_subset_adapter_preflight_contract`, not
`paper_package_generation_contract`. The current report has zero current package-conversion
candidates, so a preflight contract is the safer next boundary. It can define adapter field
requirements and no-op behavior before any later package-generation contract.

## Tables

### Future Family Candidate Matrix Rows

Emit one row for each paper primitive family.

Native-family review rows:

| Paper primitive | Candidate matrix decision | Runtime kind | Current rows |
| --- | --- | --- | --- |
| `oriented_bounding_box` | `native_family_review_only` | `box` | 0 |
| `sphere` | `native_family_review_only` | `sphere` | 0 |
| `capsule` | `native_family_review_only` | `capsule` | 0 |

Excluded family rows:

| Paper primitive | Candidate matrix decision | Runtime kind | Current rows |
| --- | --- | --- | --- |
| `capped_cylinder` | `blocked_approximation_policy_missing` | `offline_only_unmapped` | 0 |
| `frustum` | `blocked_approximation_policy_missing` | `offline_only_unmapped` | 0 |
| `trapezoidal_prism` | `blocked_unmapped_current_rows` | `offline_only_unmapped` | 16 |

Every family row must record:

- source conversion-plan row id;
- input conversion-plan decision;
- candidate matrix decision;
- `future_family_review_candidate`;
- `current_package_conversion_candidate_count`;
- `package_conversion_enabled_by_this_gate: false`;
- `primitive_spec_generation_triggered: false`;
- `collision_package_generation_triggered: false`;
- `runtime_admissibility_triggered: false`;
- `newton_runtime_triggered: false`;
- `real_usd_triggered: false`;
- `benchmark_triggered: false`;
- claim boundary text.

### Current Row Candidate Matrix Rows

Emit one row for each current row from `current_row_conversion_plan_rows`.

For the current 16 rows:

- `paper_primitive`: `trapezoidal_prism`
- `offline_runtime_kind_label`: `offline_only_unmapped`
- `input_conversion_plan_decision`: `exclude_requires_explicit_mapping_or_approximation_policy`
- `candidate_matrix_decision`: `blocked_unmapped_current_rows`
- `candidate_matrix_action`: `keep_offline`
- `current_package_conversion_candidate`: `false`
- `package_candidate_status`: `not_current_candidate_unsupported_policy_block`
- `required_future_policy`: `explicit_mapping_or_approximation_policy_before_package_generation`

No current row becomes a package-conversion candidate in this slice.

## Expected Evidence

The report should show:

- `failure_labels == ["paper_mapped_subset_adapter_preflight_contract_missing"]`;
- `next_required_gate == "paper_mapped_subset_adapter_preflight_contract"`;
- `paper_faithfulness["implemented_output_contract_scope"]` includes
  `paper_mapped_subset_conversion_candidate_matrix`;
- `paper_faithfulness["missing_before_paper_faithful_offline"]` equals
  `["paper_mapped_subset_adapter_preflight_contract"]`;
- candidate matrix payload has six family review rows and 16 current row review rows;
- family summary has three future-family review candidates and zero current package candidates;
- current-row summary has 16 blocked rows and zero package candidates.

## Test Strategy

Use TDD:

1. Add failing offline-report tests for the new payload and top-level gate transition.
2. Add failing tests for six family candidate matrix rows.
3. Add failing tests for 16 current row candidate matrix rows and zero current candidates.
4. Add failing tests that all generation/runtime/admissibility triggers remain false.
5. Add a CLI JSON regression check.
6. Implement the minimal offline payload and report wiring.
7. Run focused tests, docs validation, site claim validation, whitespace check, smoke, and full
   pytest.

## Claim Boundary

Allowed wording: command-only offline mapped-subset conversion candidate matrix.

Forbidden wording: package readiness, package conversion execution, PrimitiveSpec generation,
CollisionPackage generation, Newton support, runtime admissibility, approximation support, full
CPD reproduction, collision-quality evidence, benchmark evidence, deployment readiness, or safety
certification.
