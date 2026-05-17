# 2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Runtime-Boundary Preflight Contract

## Date

2026-05-17

## Status

Complete.

## Context

The previous gate,
`paper_mapped_subset_primitivespec_native_fixture_serialization_contract`, validated strict
canonical JSON and round-trip equality for exactly one report-only PrimitiveSpec-like dict from
the deterministic synthetic `paper_single_box` OBB/box native-fixture row.

This record closes only the next command-only offline gate:

`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`.

The new payload:

- consumes `paper_mapped_subset_primitivespec_native_fixture_serialization_contract`;
- verifies the input gate, expected next gate, row count, fixture id, primitive kind, schema keys,
  canonical JSON stability, JSON round-trip equality, and schema-validation status;
- records exactly one runtime-boundary preflight row for the same `paper_single_box` OBB/box
  source;
- records one later runtime `PrimitiveSpec` construction candidate;
- keeps runtime construction disallowed in the current gate;
- records `generated_runtime_primitive_spec_count: 0`;
- records `generated_primitive_spec_count: 0`;
- records `generated_collision_package_count: 0`;
- records `runtime_admissibility_check_count: 0`;
- advances the next gate to
  `paper_mapped_subset_primitivespec_runtime_construction_contract`.

The row is boundary metadata only. It is not a runtime `PrimitiveSpec` object and is not part of a
`CollisionPackage`. Review follow-up tightened the boundary input check so a row whose top-level
kind remains `box` but whose serialized payload drifts to another kind is rejected instead of
being allowed into the next runtime-construction gate.

## Verification

Commands:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report >/tmp/cpd_paper_runtime_boundary_preflight_report.json
# exit 0

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_boundary_preflight or native_fixture_serialization' -q
# exit 0; 48 passed, 258 deselected

PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# exit 0; 3 passed, 109 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_boundary_preflight_rejects_json_schema_drift or changed_decomposition_output_contract_gate or package_adapter_contract_gate' -q
# exit 0; 7 passed, 300 deselected

PYTHONPATH=src python -m pytest -q
# exit 0; 718 passed

PYTHONPATH=src python scripts/validate_docs.py
# exit 0

PYTHONPATH=src python scripts/validate_site_claims.py
# exit 0

git diff --check
# exit 0
```

The relevant report fields are:

- `next_required_gate: paper_mapped_subset_primitivespec_runtime_construction_contract`
- `failure_labels: [paper_mapped_subset_primitivespec_runtime_construction_contract_missing]`
- `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract.runtime_boundary_preflight_row_count: 1`
- `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract.later_runtime_primitivespec_construction_candidate_count: 1`
- `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract.runtime_construction_allowed_in_current_gate: false`
- `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract.generated_runtime_primitive_spec_count: 0`
- `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract.generated_collision_package_count: 0`
- `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract.runtime_admissibility_check_count: 0`

Malformed input checks now reject stale or drifted input with explicit failure labels for gate
identity, next-gate identity, row count, fixture id, primitive kind, serialized payload presence,
schema keys, serialized payload value drift, canonical JSON stability, runtime-object leakage, and
counter drift.

## Artifacts

- Report key: `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`
- Registry entry:
  `experiments.registry.cpd-paper-mapped-subset-primitivespec-runtime-boundary-preflight-contract`
- Implementation plan:
  `docs/superpowers/plans/2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-boundary-preflight-contract.md`
- Design spec:
  `docs/superpowers/specs/2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-boundary-preflight-contract-design.md`

## Claim Boundary

Supported:

- partial command-only offline runtime-boundary preflight for one deterministic synthetic fixture;
- source traceability from the boundary row back to the native-fixture serialization row;
- explicit accounting that runtime construction is not allowed in the current gate;
- explicit accounting that runtime PrimitiveSpecs, CollisionPackages, runtime-admissibility checks,
  Newton runtime, real-USD loading, benchmark runs, collision-quality measurement, deployment, and
  certification triggers remain zero or false.

Not supported:

- runtime `PrimitiveSpec` object creation;
- package readiness or `CollisionPackage` generation;
- runtime admissibility;
- Newton support or Newton execution;
- real-USD evidence;
- benchmark evidence;
- collision-quality evidence;
- `paper_faithful_offline` support;
- full CPD reproduction;
- deployment readiness or safety certification.

## Claim Impact

This record supports only a partial, command-only offline boundary-preflight claim for one
deterministic synthetic fixture. It does not add runtime `PrimitiveSpec` readiness, package
readiness, Newton runtime evidence, real-USD evidence, benchmark evidence, collision-quality
evidence, `paper_faithful_offline` support, or full CPD reproduction.

## Next Gate

`paper_mapped_subset_primitivespec_runtime_construction_contract`

That next gate must decide whether any runtime `PrimitiveSpec` object can be represented without
silently crossing into package generation, Newton execution, real-USD evidence, benchmark evidence,
or collision-quality claims.

## Next Action

- Implement or explicitly reject `paper_mapped_subset_primitivespec_runtime_construction_contract`
  under a separate dated record before claiming any runtime `PrimitiveSpec` object exists.
