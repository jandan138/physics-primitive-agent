# 2026-05-17 CPD Paper Package-Adapter Unsupported Primitive Policy

## Date

2026-05-17

## Status

Complete

## Summary

- Added `paper_package_adapter_unsupported_primitive_policy` to the command-only partial
  `cpd_paper_offline_report`.
- Closed only the offline unsupported-primitive policy gate and advanced the current next gate to
  `paper_package_conversion_mapped_subset_plan`.
- Kept the new artifact explicitly offline: it is an unsupported-primitive policy table, not a
  `CollisionPackage`.
- Kept package generation, Newton runtime execution, real USD, benchmark, collision-quality,
  deployment, and safety-certification claims blocked.

## What Changed

The new report payload consumes the existing `paper_package_adapter_contract` payload and records
policy metadata over deterministic synthetic toy fixture evidence:

- six paper primitive family policy rows;
- direct native adapter candidate labels for `oriented_bounding_box`, `sphere`, and `capsule`,
  without enabling package conversion in this gate;
- offline-only unmapped policy labels for `capped_cylinder`, `frustum`, and
  `trapezoidal_prism`;
- 16 current adapter decision policy rows, one per offline primitive record;
- current decision partition: 0 direct policy eligible records, 16 unsupported-policy blocked
  records, 0 dropped records, and 0 package-candidate records;
- current evidence distribution: 16 `trapezoidal_prism` rows with
  `offline_only_unmapped` runtime labels;
- package/Newton/real-USD/benchmark false triggers at payload and row level.

The top-level report now emits:

```text
next_required_gate: paper_package_conversion_mapped_subset_plan
failure_labels: ["paper_package_conversion_mapped_subset_plan_missing"]
paper_faithful_offline_supported: false
```

## Verification So Far

- RED checks were added before implementation for the new unsupported-primitive policy gate and
  CLI JSON surface.
- Targeted RED checks failed first because the report still pointed to
  `paper_package_adapter_unsupported_primitive_policy_missing` and did not emit the new payload.
- Focused GREEN checks passed:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Result: `147 passed`.

## Claim Boundary

This record supports only this narrow statement:

```text
The partial CPD paper offline report now contains a command-only offline unsupported-primitive
policy table over deterministic synthetic fixture records.
```

It does not support:

- `paper_faithful_offline`;
- full CPD paper reproduction;
- `CollisionPackage` generation;
- package readiness;
- Newton readiness;
- runtime readiness;
- runtime admissibility;
- approximation support;
- Newton runtime execution;
- real USD evidence;
- benchmark evidence;
- collision-quality validation;
- deployment readiness;
- safety certification.

## Next Step

Proceed to `paper_package_conversion_mapped_subset_plan`. That next slice should define how only
explicitly native/mapped paper-lane rows may later enter package conversion while current
paper-only or unmapped rows stay offline unless a separate mapping or approximation policy exists.
