# 2026-05-18 CPD Paper Mapped-Subset Runtime-Admissibility Contract

## Date

2026-05-18

## Status

Complete.

## Context

The previous gate, `paper_mapped_subset_runtime_admissibility_preflight_contract`, consumed the
single synthetic, report-scoped `CollisionPackage.to_dict()` artifact for `paper_single_box` and
recorded exactly one later runtime-admissibility candidate row without copying the full package
dict. It deliberately kept `runtime_admissibility_check_count: 0` and did not run Newton.

That previous gate pointed next to:

`paper_mapped_subset_runtime_admissibility_contract`

This record covers only that next single-fixture offline/static contract. It does not cover Newton
shape mapping, Newton runtime execution, real-USD evaluation, benchmark work, or collision-quality
measurement.

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_runtime_admissibility_contract`.

The new payload:

- consumes `paper_mapped_subset_runtime_admissibility_preflight_contract`;
- validates the input gate id, expected next gate, row counts, false boundary flags, and one
  preflight row;
- validates source identity fields for the one deterministic `paper_single_box` OBB/box package
  handoff;
- rejects copied source package dicts so the contract stays a row-level handoff instead of
  becoming a duplicate package store;
- validates the candidate `PrimitiveSpec.to_dict()` shape for the mapped box subset;
- rejects preflight top-level metadata drift for `input_gate_id`, `closed_gate`, and
  `runtime_admissibility_preflight_contract`;
- rejects valid-but-different primitive geometry drift by requiring the center, axes, dimensions,
  and self-consistent volume fields to match the canonical `paper_single_box` preflight primitive;
- checks finite center coordinates;
- checks finite, unit-length, mutually orthogonal, right-handed axes;
- checks positive `half_extents` under the target box dimension schema;
- checks source-face coverage for the twelve generated box faces;
- checks the recorded containment flag and positive volume accounting;
- records exactly one `runtime_admissibility_rows` entry for
  `runtime_admissibility__paper_single_box__box`;
- records `offline_static_runtime_admissibility_check_count: 1`;
- records `runtime_admissibility_check_count: 1` only as report-side static accounting;
- keeps runtime execution, Newton shape mapping, Newton runtime execution, real-USD loading,
  benchmark runs, collision-quality measurement, deployment, and certification triggers zero or
  false;
- keeps `paper_faithful_offline` blockers separate from runtime-lane gates;
- advances the next gate to `paper_mapped_subset_newton_shape_mapping_preflight_contract`.

The row is intentionally a narrow static report check for one synthetic package-shaped artifact.
It says the row is admissible for a later Newton shape-mapping preflight; it does not say Newton
has mapped or executed it.

## Verification

Commands run during this branch after implementation:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_runtime_admissibility_contract_gate -q
# first focused RED before implementation: exit 1; KeyError: 'paper_mapped_subset_runtime_admissibility_contract'

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_records_mapped_subset_runtime_admissibility_contract_gate -q
# exit 0; 1 passed

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_contract' -q
# exit 0; 70 passed, 615 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_preflight or runtime_admissibility_contract or collision_package_generation_contract' -q
# exit 0; 168 passed, 450 deselected

PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# exit 0; 3 passed, 109 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_contract_rejects_input_drift or runtime_admissibility_contract_rejects_primitivespec_drift' -q
# first focused RED after review: exit 1; 5 failed, 16 passed, 669 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_contract_rejects_input_drift or runtime_admissibility_contract_rejects_primitivespec_drift' -q
# exit 0; 21 passed, 669 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_admissibility_contract' -q
# exit 0; 75 passed, 615 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate tests/test_cpd_paper_offline.py::test_cpd_paper_offline_report_records_package_adapter_contract_gate -q
# exit 0; 2 passed

PYTHONPATH=src python -m pytest -q
# exit 0; 1099 passed, 2 skipped

PYTHONPATH=src python scripts/validate_docs.py
# exit 0; docs validation passed

PYTHONPATH=src python scripts/validate_site_claims.py
# exit 0; site claim validation passed

git diff --check
# exit 0
```

Independent review:

- Code/tests reviewer: no findings. The reviewer confirmed the exact-list scope fix is legitimate
  because the runtime-admissibility contract is appended after the preflight contract, exposed in
  the report payload, and advances to the Newton shape-mapping preflight gate.
- Docs/claim-boundary reviewer: no findings. The reviewer confirmed the docs keep this slice
  bounded to offline/static accounting and do not claim Newton runtime execution, compiler
  readiness, benchmark evidence, real-USD evidence, deployment readiness, or safety certification.

## Artifacts

- Report key: `paper_mapped_subset_runtime_admissibility_contract`
- Previous report gate: `paper_mapped_subset_runtime_admissibility_preflight_contract`
- Next report gate: `paper_mapped_subset_newton_shape_mapping_preflight_contract`
- Static row id: `runtime_admissibility__paper_single_box__box`
- Source preflight row id: `runtime_admissibility_preflight__paper_single_box__box`
- Source package id:
  `paper_single_box:paper_mapped_subset_collision_package_generation_contract`
- Implementation plan:
  `docs/superpowers/plans/2026-05-18-cpd-paper-mapped-subset-runtime-admissibility-contract.md`
- Design spec:
  `docs/superpowers/specs/2026-05-18-cpd-paper-mapped-subset-runtime-admissibility-contract-design.md`

## Claim Boundary

Supported:

- partial single-fixture offline/static runtime-admissibility accounting for one deterministic
  synthetic fixture;
- validation that the candidate row still describes the expected `paper_single_box` box package;
- validation that the candidate box row has finite center coordinates, right-handed orthonormal
  axes, positive half extents, expected source faces, containment flag, and positive volume fields;
- exactly one report-side static runtime-admissibility row;
- explicit accounting that Newton shape mapping, Newton runtime execution, real-USD loading,
  benchmark runs, collision-quality measurement, deployment, and certification triggers remain
  zero or false.

Not supported:

- general package readiness;
- Newton readiness;
- Newton shape mapping;
- Newton support or Newton execution;
- real-USD evidence;
- benchmark evidence;
- collision-quality evidence;
- paper primitive vocabulary coverage;
- approximation support;
- `paper_faithful_offline` support;
- full CPD reproduction;
- deployment readiness or safety certification.

## Claim Impact

This record supports only a partial, single-fixture offline/static runtime-admissibility claim for
one deterministic synthetic `paper_single_box` OBB/box fixture. It moves the CPD paper runtime lane
from "one bounded package dict has a handoff row" to "that handoff row has one bounded static
finite-geometry and box-schema check".

It does not add Newton shape mapping and does not add Newton execution evidence.

## Next Gate

`paper_mapped_subset_newton_shape_mapping_preflight_contract`

That next gate must decide what the one report-scoped package artifact must record before any
Newton shape mapping can be attempted or claimed.

## Next Action

- Implement `paper_mapped_subset_newton_shape_mapping_preflight_contract` under a separate dated
  record before claiming Newton shape mapping, Newton runtime support, or broader package
  readiness.
