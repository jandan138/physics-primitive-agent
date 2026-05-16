# CPD Paper Package-Adapter Unsupported Primitive Policy Design

## Context

The current `cpd_paper_offline_report` closes `paper_package_adapter_contract` as a command-only
offline contract. It consumes 16 changed-decomposition primitive records and classifies every
current row as `later_policy_required` because all selected current rows are
`trapezoidal_prism` with `offline_only_unmapped` runtime labels.

The next gate must decide what that means before any package conversion. This is a policy gate,
not a package generator.

## Goal

Add `paper_package_adapter_unsupported_primitive_policy` as an offline-only payload inside
`cpd_paper_offline_report`.

The payload must:

- classify all six CPD paper primitive families by adapter policy;
- classify the current adapter decision rows from `paper_package_adapter_contract`;
- keep current `trapezoidal_prism` / `offline_only_unmapped` rows blocked from package conversion;
- keep the top-level report `partial`;
- keep `paper_faithful_offline_supported: false`;
- keep package generation, Newton runtime, real-USD, and benchmark triggers false.

## Non-Goals

This slice must not:

- construct a `CollisionPackage`;
- construct `PrimitiveSpec` rows;
- import or call Newton runtime code;
- approximate paper-only primitives as native Newton primitives;
- drop unsupported primitives silently;
- run bed or Franka USD assets;
- run benchmarks or claim collision-quality improvement.

## Policy Model

The new payload will expose two policy tables.

### Primitive Family Policy

One row per paper primitive family:

| Paper primitive | Policy |
| --- | --- |
| `oriented_bounding_box` | direct native adapter candidate only after mapped-subset conversion planning |
| `sphere` | direct native adapter candidate only after mapped-subset conversion planning |
| `capsule` | native kind exists in principle, but current rows do not exercise it |
| `capped_cylinder` | offline-only unless a future explicit mapping or approximation policy exists |
| `frustum` | offline-only unless a future explicit mapping or approximation policy exists |
| `trapezoidal_prism` | offline-only unless a future explicit mapping or approximation policy exists |

Family-level policy is not current-row evidence. For example, capsule may have a Newton-native
shape family, but the current changed-decomposition rows do not contain capsule records.

### Current Adapter Decision Policy

Every current adapter decision row will be reclassified by unsupported-primitive policy.

For the current 16 rows:

- `input_adapter_decision`: `later_policy_required`
- `paper_primitive`: `trapezoidal_prism`
- `offline_runtime_kind_label`: `offline_only_unmapped`
- `unsupported_policy_decision`: `block_package_conversion`
- `adapter_action`: `keep_offline`
- `package_candidate_status`: `not_package_candidate_unsupported_policy_block`

No row becomes a package candidate in this slice.

## Next Gate

After this slice, the top-level next gate should become
`paper_package_conversion_mapped_subset_plan`.

Rationale: the current selected rows are all offline-only unmapped paper primitives. Jumping
straight to a package-generation contract would imply more readiness than the evidence supports.
The mapped-subset plan gate should separately decide how only Newton-native, explicitly mapped
paper-lane rows may enter package conversion later.

## Expected Evidence

The report should show:

- `failure_labels == ["paper_package_conversion_mapped_subset_plan_missing"]`;
- `next_required_gate == "paper_package_conversion_mapped_subset_plan"`;
- `paper_faithfulness["implemented_output_contract_scope"]` includes
  `paper_package_adapter_unsupported_primitive_policy`;
- `paper_faithfulness["missing_before_paper_faithful_offline"]` equals
  `["paper_package_conversion_mapped_subset_plan"]`;
- unsupported policy payload has six family rows and 16 current decision rows;
- current decision rows have zero package candidates and zero direct policy eligible rows.

## Test Strategy

Use TDD:

1. Add failing offline-report tests for the new payload and top-level gate transition.
2. Add failing tests for family-policy row classification.
3. Add failing tests for current decision-row policy classification and count partitioning.
4. Add a CLI JSON regression check.
5. Implement the minimal offline payload and report wiring.
6. Run focused tests, docs validation, site claim validation, whitespace check, and full pytest.

## Claim Boundary

Allowed wording: command-only offline unsupported-primitive adapter policy.

Forbidden wording: package readiness, Newton support, runtime admissibility, approximation support,
full CPD reproduction, collision-quality evidence, benchmark evidence, deployment readiness, or
safety certification.
