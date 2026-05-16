# CPD Paper Package Conversion Mapped-Subset Plan Design

## Context

The current `cpd_paper_offline_report` closes
`paper_package_adapter_unsupported_primitive_policy` as a command-only offline policy table. It
classifies all six paper primitive families and keeps the current 16
`trapezoidal_prism` / `offline_only_unmapped` rows offline with `block_package_conversion`.

The next gate is `paper_package_conversion_mapped_subset_plan`. It must answer a narrower planning
question before any package generation:

```text
Which paper-lane rows would be eligible for a future mapped-subset conversion path, and which
rows stay offline?
```

## Goal

Add `paper_package_conversion_mapped_subset_plan` as an offline-only planning payload inside
`cpd_paper_offline_report`.

The payload must:

- consume `paper_package_adapter_unsupported_primitive_policy`;
- plan a future mapped-subset conversion lane for only explicitly native/mapped paper families;
- keep current `trapezoidal_prism` / `offline_only_unmapped` rows out of the mapped subset;
- record zero current package-conversion candidates;
- keep the top-level report `partial`;
- keep `paper_faithful_offline_supported: false`;
- keep package generation, Newton runtime, real-USD, and benchmark triggers false.

## Non-Goals

This slice must not:

- construct a `CollisionPackage`;
- construct `PrimitiveSpec` rows;
- import or call Newton runtime code;
- perform runtime admissibility checks;
- approximate paper-only primitives;
- silently drop unsupported primitives;
- run bed or Franka USD assets;
- run benchmarks or claim collision-quality improvement.

## Planning Model

The new payload will expose two tables.

### Family Conversion Plan Rows

One row per paper primitive family:

| Paper primitive | Planning result |
| --- | --- |
| `oriented_bounding_box` | future mapped-subset candidate through Newton `box`, but no current-row evidence |
| `sphere` | future mapped-subset candidate through Newton `sphere`, but no current-row evidence |
| `capsule` | future mapped-subset candidate through Newton `capsule`, but no current-row evidence |
| `capped_cylinder` | excluded from direct mapped subset until an explicit policy maps it |
| `frustum` | excluded from direct mapped subset until an explicit policy maps it |
| `trapezoidal_prism` | excluded from direct mapped subset until an explicit policy maps it |

Family-level candidate status is planning metadata, not package support.

### Current Row Conversion Plan Rows

Every current adapter policy row will be reclassified for mapped-subset conversion planning.

For the current 16 rows:

- `paper_primitive`: `trapezoidal_prism`
- `offline_runtime_kind_label`: `offline_only_unmapped`
- `input_unsupported_policy_decision`: `block_package_conversion`
- `conversion_plan_decision`: `exclude_from_mapped_subset`
- `conversion_plan_action`: `keep_offline`
- `package_conversion_candidate`: `false`

No current row becomes eligible for package conversion in this slice.

## Next Gate

After this slice, the top-level next gate should become
`paper_mapped_subset_conversion_candidate_matrix`.

Rationale: after the plan explicitly says the current rows have zero mapped-subset candidates, the
next gate can define the future candidate matrix before any package conversion contract or package
generation. That future matrix must still be offline and must not generate package rows unless a
later contract records stronger evidence.

## Expected Evidence

The report should show:

- `failure_labels == ["paper_mapped_subset_conversion_candidate_matrix_missing"]`;
- `next_required_gate == "paper_mapped_subset_conversion_candidate_matrix"`;
- `paper_faithfulness["implemented_output_contract_scope"]` includes
  `paper_package_conversion_mapped_subset_plan`;
- `paper_faithfulness["missing_before_paper_faithful_offline"]` equals
  `["paper_mapped_subset_conversion_candidate_matrix"]`;
- mapped-subset plan payload has six family rows and 16 current row-plan rows;
- current row-plan summary has zero package-conversion candidates and 16 exclusions.

## Test Strategy

Use TDD:

1. Add failing offline-report tests for the new payload and top-level gate transition.
2. Add failing tests for six family conversion-plan rows.
3. Add failing tests for 16 current row conversion-plan rows and zero candidates.
4. Add a CLI JSON regression check.
5. Implement the minimal offline payload and report wiring.
6. Run focused tests, docs validation, site claim validation, whitespace check, and full pytest.

## Claim Boundary

Allowed wording: command-only offline mapped-subset package-conversion planning.

Forbidden wording: package readiness, package generation, Newton support, runtime admissibility,
approximation support, full CPD reproduction, collision-quality evidence, benchmark evidence,
deployment readiness, or safety certification.
