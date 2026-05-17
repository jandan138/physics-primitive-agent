# 2026-05-17 CPD Paper Mapped-Subset Adapter Preflight Contract

## Date

2026-05-17

## Status

Complete

## Summary

- Added `paper_mapped_subset_adapter_preflight_contract` to the command-only partial
  `cpd_paper_offline_report`.
- Closed only the offline mapped-subset adapter-preflight gate and advanced the current next gate
  to `paper_mapped_subset_primitivespec_dry_run_contract`.
- Kept the new artifact explicitly offline: it is an adapter-preflight contract, not
  `PrimitiveSpec` generation, not a `CollisionPackage`, not package generation, and not Newton
  runtime support.
- Kept package generation, runtime admissibility, Newton runtime execution, real USD, benchmark,
  collision-quality, deployment, and safety-certification claims blocked.

## What Changed

The new report payload consumes the existing
`paper_mapped_subset_conversion_candidate_matrix` payload and records adapter-preflight metadata
over deterministic synthetic toy fixture evidence:

- six adapter preflight requirement rows, one per paper primitive family;
- three future native-family preflight records for `oriented_bounding_box`, `sphere`, and
  `capsule`;
- three blocked or no-op family rows for `capped_cylinder`, `frustum`, and
  `trapezoidal_prism`;
- 16 current row adapter-preflight rows, one per current offline primitive record;
- current decision partition: 0 current preflight pass records, 0 current package-conversion
  candidates, and 16 no-op rows that stay offline;
- current evidence distribution: 16 `trapezoidal_prism` rows with
  `offline_only_unmapped` runtime labels;
- PrimitiveSpec/CollisionPackage/runtime-admissibility/Newton/real-USD/benchmark false triggers
  at payload and row level.

The top-level report now emits:

```text
next_required_gate: paper_mapped_subset_primitivespec_dry_run_contract
failure_labels: ["paper_mapped_subset_primitivespec_dry_run_contract_missing"]
paper_faithful_offline_supported: false
```

## Verification So Far

- RED checks were added before implementation for the new preflight gate, family preflight rows,
  current row no-op rows, zero current preflight passes, zero current package-conversion
  candidates, false runtime/package triggers, and CLI JSON surface.
- Targeted RED checks failed first because the report still pointed to
  `paper_mapped_subset_adapter_preflight_contract_missing` and did not emit the new preflight
  payload.
- Focused GREEN checks passed:

```bash
python -m pytest tests/test_cpd_paper_offline.py tests/test_cli.py -q
```

Result: `159 passed`.

## Claim Boundary

This record supports only this narrow statement:

```text
The partial CPD paper offline report now contains a command-only offline mapped-subset adapter
preflight contract over deterministic synthetic fixture records.
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

Proceed to `paper_mapped_subset_primitivespec_dry_run_contract`. That next slice should define a
report-only PrimitiveSpec dry-run contract and zero-candidate behavior before any real
`PrimitiveSpec` generation, CollisionPackage generation, runtime admissibility check, Newton
runtime execution, real USD, or benchmark work.
