# 2026-05-17 CPD Paper Mapped-Subset PrimitiveSpec Runtime-Construction Contract

## Date

2026-05-17

## Status

Complete.

## Context

The previous gate,
`paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`, validated exactly one
runtime-construction candidate for the deterministic synthetic `paper_single_box` OBB/box row.
That previous gate deliberately created zero runtime objects and pointed next to:

`paper_mapped_subset_primitivespec_runtime_construction_contract`

This record covers only that next single-fixture offline runtime-construction gate.

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_primitivespec_runtime_construction_contract`.

The new payload:

- consumes `paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract`;
- verifies the input gate, expected next gate, row count, fixture id, primitive kind, explicit
  false boundary flags, canonical JSON schema, canonical JSON stability, the preflight row's
  canonical JSON SHA-256 fingerprint, serialized payload values, nested geometry shape, and box
  volume consistency;
- loads the runtime-construction source from `canonical_primitivespec_json`;
- constructs exactly one runtime `PrimitiveSpec` object from the canonical `paper_single_box`
  OBB/box preflight JSON;
- stores only the resulting `PrimitiveSpec.to_dict()` payload in the JSON report;
- records `constructed_runtime_primitivespec_count: 1`;
- records `generated_runtime_primitive_spec_count: 1`;
- records `generated_primitive_spec_count: 1`;
- records `generated_collision_package_count: 0`;
- records `runtime_admissibility_check_count: 0`;
- advances the next gate to
  `paper_mapped_subset_collision_package_generation_preflight_contract`.

The constructed object is intentionally report-scoped. It is not a collision package, is not fed to
Newton, and is not evidence for real-USD behavior, benchmark behavior, collision quality, or full
CPD paper reproduction.

## Verification

Commands:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'runtime_construction or runtime_boundary_preflight' -q
# exit 0; 105 passed, 275 deselected

PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# exit 0; 3 passed, 109 deselected

PYTHONPATH=src python -m primitive_collision_compiler.cli --run-cpd-paper-offline-report >/tmp/cpd_paper_runtime_construction_report.json
# exit 0

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
# exit 0; 375 passed

PYTHONPATH=src python -m pytest -q
# exit 0; 786 passed

PYTHONPATH=src python scripts/validate_docs.py
# exit 0; docs validation passed

PYTHONPATH=src python scripts/validate_site_claims.py
# exit 0; site claim validation passed

git diff --check
# exit 0
```

Multi-agent review found and the implementation now rejects missing runtime-construction false
flags, malformed nested canonical-payload drift, and valid-but-wrong canonical payload drift that
would otherwise silently change `center`, `axes`, `dimensions`, `source_faces`, `pose`, `volume`,
or `weighted_volume`. Runtime construction now compares the canonical JSON against the SHA-256
fingerprint recorded by the runtime-boundary preflight row before constructing the report-scoped
`PrimitiveSpec`. The static guard now scans the full runtime-construction helper block from
`_RUNTIME_CONSTRUCTION_BOUNDARY_FALSE_FLAGS` through the next section and blocks direct
Newton/USD/package/benchmark/collision-quality tokens.

The fingerprint is a report-row consistency check, not a tamper-proof custody mechanism. It rejects
stale or drifted `canonical_primitivespec_json` when the paired preflight fingerprint does not
match. It does not prove immutability if both the JSON and fingerprint are rewritten together before
runtime construction.

## Artifacts

- Report key: `paper_mapped_subset_primitivespec_runtime_construction_contract`
- Next report gate:
  `paper_mapped_subset_collision_package_generation_preflight_contract`
- Implementation plan:
  `docs/superpowers/plans/2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-construction-contract.md`
- Design spec:
  `docs/superpowers/specs/2026-05-17-cpd-paper-mapped-subset-primitivespec-runtime-construction-contract-design.md`

## Claim Boundary

Supported:

- partial single-fixture offline runtime-construction accounting for one deterministic synthetic
  fixture;
- construction of exactly one runtime `PrimitiveSpec` object from canonical preflight JSON;
- rejection of canonical preflight JSON drift through a report-scoped SHA-256 fingerprint check;
- report-row consistency checking only, not cryptographic custody or tamper-proof provenance;
- JSON-report storage of only `PrimitiveSpec.to_dict()` output;
- explicit accounting that CollisionPackages, runtime-admissibility checks, Newton runtime,
  real-USD loading, benchmark runs, collision-quality measurement, deployment, and certification
  triggers remain zero or false.

Not supported:

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

This record supports only a partial, single-fixture offline runtime-construction claim for one
deterministic synthetic `paper_single_box` OBB/box fixture. It does not add package readiness,
Newton runtime evidence, real-USD evidence, benchmark evidence, collision-quality evidence,
`paper_faithful_offline` support, or full CPD reproduction.

## Next Gate

`paper_mapped_subset_collision_package_generation_preflight_contract`

That next gate must decide the preconditions for package generation before any constructed
`PrimitiveSpec` is converted into a package artifact or exposed to Newton-related checks.

## Next Action

- Implement `paper_mapped_subset_collision_package_generation_preflight_contract` under a separate
  dated record before claiming package generation, package readiness, runtime admissibility, or
  Newton runtime support.
