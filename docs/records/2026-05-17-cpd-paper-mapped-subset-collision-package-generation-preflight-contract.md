# 2026-05-17 CPD Paper Mapped-Subset CollisionPackage Generation Preflight Contract

## Date

2026-05-17

## Status

Complete.

## Context

The previous gate,
`paper_mapped_subset_primitivespec_runtime_construction_contract`, constructed exactly one
runtime `PrimitiveSpec` object for the deterministic synthetic `paper_single_box` OBB/box row and
stored only `PrimitiveSpec.to_dict()` in the report.

That previous gate deliberately created zero CollisionPackages, zero runtime-admissibility
checks, no Newton evidence, no real-USD evidence, no benchmark evidence, and no collision-quality
evidence. It pointed next to:

`paper_mapped_subset_collision_package_generation_preflight_contract`

This record covers only that next single-fixture offline preflight gate.

## What Changed

The partial `cpd_paper_offline_report` now includes
`paper_mapped_subset_collision_package_generation_preflight_contract`.

The new payload:

- consumes `paper_mapped_subset_primitivespec_runtime_construction_contract`;
- validates the input gate, expected next gate, one runtime-construction row, fixture id,
  primitive kind, explicit false boundary flags, and carried-forward runtime PrimitiveSpec counts;
- requires the source row to have `runtime_instance_generated: true` and
  `runtime_primitivespec_construction_triggered: true`;
- requires the carried `generated_primitive_spec` dict to equal the carried
  `constructed_primitivespec_dict`;
- records exactly one later package-generation candidate row for the synthetic `paper_single_box`
  OBB/box runtime `PrimitiveSpec.to_dict()` payload;
- records `package_generation_allowed_in_current_gate: false`;
- records `generated_collision_package_count: 0`;
- records `runtime_admissibility_check_count: 0`;
- advances the next gate to `paper_mapped_subset_collision_package_generation_contract`.

The preflight row is intentionally a candidate record only. It is not a CollisionPackage, is not
fed to Newton, and is not evidence for runtime admissibility, real-USD behavior, benchmark
behavior, collision quality, or full CPD paper reproduction.

## Verification

Commands run during this branch:

```bash
PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_preflight and (lockstep or missing_source_row_lineage)' -q
# exit 0; 3 passed, 445 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_collision_package_generation_preflight_rejects_coherent_canonical_payload_drift -q
# initial exit 1; coherent drift across loaded payload, canonical JSON, generated dict, and constructed dict was accepted

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_collision_package_generation_preflight_rejects_coherent_canonical_payload_drift -q
# exit 0; 1 passed

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_collision_package_generation_preflight_rejects_drifted_source_row_lineage_value -q
# initial exit 1; drifted source lineage ids were accepted

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py::test_cpd_paper_collision_package_generation_preflight_rejects_drifted_source_row_lineage_value -q
# exit 0; 1 passed

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_preflight and (lockstep or missing_source_row_lineage or drifted_source_row_lineage or coherent_canonical)' -q
# exit 0; 5 passed, 445 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -k 'collision_package_generation_preflight or runtime_construction' -q
# exit 0; 144 passed, 306 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_offline.py -q
# exit 0; 450 passed

PYTHONPATH=src python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q
# exit 0; 3 passed, 109 deselected

PYTHONPATH=src python -m pytest tests/test_cpd_paper_importer.py::test_imported_experiment_translation_ids_stay_semantically_aligned -q
# initial exit 1; the isolated worktree was missing ignored paper source intake

PYTHONPATH=src python -m pytest tests/test_cpd_paper_importer.py::test_imported_experiment_translation_ids_stay_semantically_aligned -q
# exit 0 after syncing ignored source intake into this worktree; 1 passed

PYTHONPATH=src python -m pytest tests/test_cpd_paper_importer.py -q
# exit 0; 37 passed

PYTHONPATH=src python -m pytest -q
# exit 0; 861 passed

PYTHONPATH=src python scripts/validate_docs.py
# exit 0; docs validation passed

PYTHONPATH=src python scripts/validate_site_claims.py
# exit 0; site claim validation passed

git diff --check
# exit 0
```

The importer failure was environmental rather than a tracked code regression: the complete
`docs/tmp/papers/arXiv-2602.07369v1/` LaTeX source intake is ignored by git and was absent from
the isolated worktree. It was copied from the main workspace into this worktree for verification
only. The copied source remains ignored and is not a commit artifact.

Review-driven fixes added explicit schema checks for missing source-row lineage fields,
independent validation of the carried `PrimitiveSpec.to_dict()` payload, and an anchored source-row
check against the deterministic runtime-construction row. Lockstep drift between
`generated_primitive_spec` and `constructed_primitivespec_dict` cannot pass by equality alone, and
coherent drift across the loaded payload, canonical JSON, generated dict, and constructed dict is
rejected before a package-generation candidate row is recorded. The anchored check also compares
the lineage/source ids copied into the package-generation candidate, so drifted provenance ids are
rejected instead of being emitted.

The docs, site-claim, and whitespace checks above were rerun after this record update.

## Artifacts

- Report key: `paper_mapped_subset_collision_package_generation_preflight_contract`
- Next report gate: `paper_mapped_subset_collision_package_generation_contract`
- Implementation plan:
  `docs/superpowers/plans/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-preflight-contract.md`
- Design spec:
  `docs/superpowers/specs/2026-05-17-cpd-paper-mapped-subset-collision-package-generation-preflight-contract-design.md`

## Claim Boundary

Supported:

- partial single-fixture offline package-generation preflight accounting for one deterministic
  synthetic fixture;
- one later package-generation candidate row from a report-scoped `PrimitiveSpec.to_dict()`
  payload;
- explicit accounting that generated CollisionPackages, runtime-admissibility checks, Newton
  runtime, real-USD loading, benchmark runs, collision-quality measurement, deployment, and
  certification triggers remain zero or false.

Not supported:

- package readiness;
- actual CollisionPackage generation;
- runtime admissibility;
- Newton support or Newton execution;
- real-USD evidence;
- benchmark evidence;
- collision-quality evidence;
- `paper_faithful_offline` support;
- full CPD reproduction;
- deployment readiness or safety certification.

## Claim Impact

This record supports only a partial, single-fixture offline package-generation preflight claim for
one deterministic synthetic `paper_single_box` OBB/box fixture. It does not add package
readiness, Newton runtime evidence, real-USD evidence, benchmark evidence, collision-quality
evidence, `paper_faithful_offline` support, or full CPD reproduction.

## Next Gate

`paper_mapped_subset_collision_package_generation_contract`

That next gate must decide how the preflight candidate becomes a bounded package artifact before
any runtime-admissibility or Newton-related checks are claimed.

## Next Action

- Implement `paper_mapped_subset_collision_package_generation_contract` under a separate dated
  record before claiming package readiness, runtime admissibility, or Newton runtime support.
