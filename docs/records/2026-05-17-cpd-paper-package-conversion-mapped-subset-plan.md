# 2026-05-17 CPD Paper Package Conversion Mapped-Subset Plan

## Date

2026-05-17

## Status

Complete

## Summary

- Added `paper_package_conversion_mapped_subset_plan` to the command-only partial
  `cpd_paper_offline_report`.
- Closed only the offline mapped-subset package-conversion planning gate and advanced the current
  next gate to `paper_mapped_subset_conversion_candidate_matrix`.
- Kept the new artifact explicitly offline: it is a planning table, not a `CollisionPackage`, not
  package generation, and not Newton runtime support.
- Kept package generation, runtime admissibility, Newton runtime execution, real USD, benchmark,
  collision-quality, deployment, and safety-certification claims blocked.

## What Changed

The new report payload consumes the existing
`paper_package_adapter_unsupported_primitive_policy` payload and records planning metadata over
deterministic synthetic toy fixture evidence:

- six paper primitive family conversion-plan rows;
- future native-mapped family labels for `oriented_bounding_box`, `sphere`, and `capsule`;
- offline-only policy labels for `capped_cylinder`, `frustum`, and `trapezoidal_prism`;
- 16 current row conversion-plan rows, one per current offline primitive record;
- current decision partition: 0 current package-conversion candidates, 16 exclusions that stay
  offline, and 0 dropped records;
- current evidence distribution: 16 `trapezoidal_prism` rows with
  `offline_only_unmapped` runtime labels;
- package/Newton/real-USD/benchmark false triggers at payload and row level.

The top-level report now emits:

```text
next_required_gate: paper_mapped_subset_conversion_candidate_matrix
failure_labels: ["paper_mapped_subset_conversion_candidate_matrix_missing"]
paper_faithful_offline_supported: false
```

## Verification So Far

- RED checks were added before implementation for the new mapped-subset planning gate, family
  conversion-plan rows, current row conversion-plan rows, zero current candidates, and CLI JSON
  surface.
- Targeted RED checks failed first because the report still pointed to
  `paper_package_conversion_mapped_subset_plan_missing` and did not emit the new payload.
- Focused GREEN checks passed:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Result: `151 passed`.

## Claim Boundary

This record supports only this narrow statement:

```text
The partial CPD paper offline report now contains a command-only offline mapped-subset
package-conversion planning table over deterministic synthetic fixture records.
```

It does not support:

- `paper_faithful_offline`;
- full CPD paper reproduction;
- `CollisionPackage` generation;
- package readiness;
- package conversion execution;
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

Proceed to `paper_mapped_subset_conversion_candidate_matrix`. That next slice should turn the
future native-family plan into explicit offline candidate rows before any package generation,
runtime admissibility check, Newton runtime execution, real USD, or benchmark work.
