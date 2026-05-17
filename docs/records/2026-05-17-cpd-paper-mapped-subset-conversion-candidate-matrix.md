# 2026-05-17 CPD Paper Mapped-Subset Conversion Candidate Matrix

## Date

2026-05-17

## Status

Complete

## Summary

- Added `paper_mapped_subset_conversion_candidate_matrix` to the command-only partial
  `cpd_paper_offline_report`.
- Closed only the offline mapped-subset candidate-matrix gate and advanced the current next gate
  to `paper_mapped_subset_adapter_preflight_contract`.
- Kept the new artifact explicitly offline: it is a review matrix, not a `CollisionPackage`, not
  package generation, not PrimitiveSpec generation, and not Newton runtime support.
- Kept package generation, runtime admissibility, Newton runtime execution, real USD, benchmark,
  collision-quality, deployment, and safety-certification claims blocked.

## What Changed

The new report payload consumes the existing
`paper_package_conversion_mapped_subset_plan` payload and records candidate-matrix metadata over
deterministic synthetic toy fixture evidence:

- six family candidate-matrix rows;
- three native-family review rows for `oriented_bounding_box`, `sphere`, and `capsule`;
- three blocked family rows for `capped_cylinder`, `frustum`, and `trapezoidal_prism`;
- 16 current row candidate-matrix rows, one per current offline primitive record;
- current decision partition: 0 current package-conversion candidates and 16 blocked rows that
  stay offline;
- current evidence distribution: 16 `trapezoidal_prism` rows with
  `offline_only_unmapped` runtime labels;
- PrimitiveSpec/CollisionPackage/runtime-admissibility/Newton/real-USD/benchmark false triggers
  at payload and row level.

The top-level report now emits:

```text
next_required_gate: paper_mapped_subset_adapter_preflight_contract
failure_labels: ["paper_mapped_subset_adapter_preflight_contract_missing"]
paper_faithful_offline_supported: false
```

## Verification So Far

- RED checks were added before implementation for the new candidate-matrix gate, family review
  rows, current row review rows, zero current package-conversion candidates, false runtime/package
  triggers, and CLI JSON surface.
- Targeted RED checks failed first because the report still pointed to
  `paper_mapped_subset_conversion_candidate_matrix_missing` and did not emit the new payload.
- Focused GREEN checks passed:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Result: `155 passed`.

## Claim Boundary

This record supports only this narrow statement:

```text
The partial CPD paper offline report now contains a command-only offline mapped-subset conversion
candidate matrix over deterministic synthetic fixture records.
```

It does not support:

- `paper_faithful_offline`;
- full CPD paper reproduction;
- `PrimitiveSpec` generation;
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

Proceed to `paper_mapped_subset_adapter_preflight_contract`. That next slice should define adapter
preflight requirements and no-op behavior before any PrimitiveSpec generation, CollisionPackage
generation, runtime admissibility check, Newton runtime execution, real USD, or benchmark work.
