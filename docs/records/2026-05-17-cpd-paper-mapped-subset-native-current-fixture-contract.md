# CPD Paper Mapped-Subset Native-Current Fixture Contract

## Date

2026-05-17

## Status

Complete for a command-only offline/report-only native-current fixture source-row contract. Not
complete for runtime `PrimitiveSpec` generation, `CollisionPackage` generation, package readiness,
runtime admissibility, Newton runtime, real-USD evidence, benchmarks, collision-quality
measurement, deployment readiness, or safety certification.

## Decision

Implement `paper_mapped_subset_native_current_fixture_contract` after
`paper_mapped_subset_primitivespec_candidate_source_contract`.

The gate stays offline. It consumes the candidate-source audit, then adds one deterministic
synthetic current source row from `paper_single_box` so the next gate can test report-only
PrimitiveSpec row generation for the Newton-native mapped subset. It does not construct a runtime
`PrimitiveSpec`, does not construct a `CollisionPackage`, and does not call Newton.

## What Changed

- The CPD paper offline report now records
  `paper_mapped_subset_native_current_fixture_contract`.
- The payload selects exactly one deterministic synthetic current fixture source:
  `paper_single_box`.
- The selected paper primitive is `oriented_bounding_box`.
- The mapped Newton/runtime primitive kind is `box`.
- The source row is traced to `candidate_source_template__oriented_bounding_box`.
- The source row records `fixture_source_faces: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]`.
- The payload records one eligible current candidate source.
- The payload records one report-only PrimitiveSpec generation candidate.
- Generated runtime PrimitiveSpec count remains zero.
- Generated CollisionPackage count remains zero.
- Runtime-admissibility check count remains zero.
- Newton runtime, real-USD loading, benchmark, collision-quality, deployment, and certification
  triggers remain false.
- The top-level next gate is now
  `paper_mapped_subset_primitivespec_native_fixture_generation_contract`.
- Input validation now rejects malformed candidate-source payloads before emitting the
  native-current fixture row.
- Review fix: input validation now iterates all 16 candidate-source current rows and rejects
  current-row leaks of eligible candidate flags, PrimitiveSpec generation-candidate flags,
  generated PrimitiveSpec payloads, and runtime/package/Newton/evaluation trigger flags.
- Selected-fit validation now rejects missing `paper_single_box`, duplicate `paper_single_box`,
  missing primitive-fit audits, empty source faces, wrong paper primitive, wrong Newton kind,
  wrong fit model, wrong axis policy, containment drift, clamp drift, and nonfinite geometry.
- Review fix: selected-fit validation now also rejects valid-but-wrong OBB geometry by comparing
  selected center, axes, half-extents, volume, and weighted volume against the OBB candidate row in
  the same `paper_single_box` primitive-fit audit.

## Boundary

This is not runtime PrimitiveSpec generation, CollisionPackage generation, package readiness,
runtime admissibility, Newton support, approximation support, real-USD evidence, benchmark
evidence, collision-quality evidence, deployment readiness, or safety certification. It only
records a traceable synthetic OBB/box source row for a later report-only PrimitiveSpec generation
gate.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py -k 'native_current_fixture' -q`
  - RED result before implementation: `37 failed, 189 deselected`.
  - GREEN result after implementation: `37 passed, 189 deselected`.
- `python -m pytest tests/test_cpd_paper_offline.py -k 'candidate_source or native_current_fixture' -q`
  - Result: `66 passed, 160 deselected`.
- `python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q`
  - Result: `2 passed, 109 deselected`.
- `python -m py_compile src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py tests/test_cli.py`
  - Result: passed.
- `python scripts/validate_docs.py`
  - Result: `docs validation passed`.
- `python scripts/validate_site_claims.py`
  - Result: `site claim validation passed`.
- `git diff --check`
  - Result: passed.
- `python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py`
  - Result after documentation and registry updates: `337 passed`.
- `python -m pytest tests/test_cpd_paper_offline.py -k 'current_row_runtime_leaks or valid_selected_geometry_drift' -q`
  - RED result before review fix: `9 failed, 226 deselected`.
  - GREEN result after review fix: `9 passed, 226 deselected`.
- `python -m pytest tests/test_cpd_paper_offline.py -k 'candidate_source or native_current_fixture' -q`
  - Result after review fix: `75 passed, 160 deselected`.
- `python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py`
  - Result after review fix and documentation updates: `346 passed`.
- Implementation review follow-up after the review fix:
  - Result: previous High and Medium findings confirmed fixed; no new blocker found.
- `python -m pytest -q`
  - Result after review fix: `645 passed`.
- `python scripts/validate_docs.py && python scripts/validate_site_claims.py && git diff --check`
  - Result after review fix: docs validation passed; site claim validation passed; diff check
    passed.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-17-cpd-paper-mapped-subset-native-current-fixture-contract-design.md`
- `docs/superpowers/plans/2026-05-17-cpd-paper-mapped-subset-native-current-fixture-contract.md`
- `experiments/registry.yaml`

## Claim Impact

Supported only:

- command-only offline native-current fixture source-row accounting for deterministic synthetic
  fixture records;
- one traceable `paper_single_box` OBB/box source row;
- one eligible current candidate source;
- one report-only PrimitiveSpec generation candidate;
- next gate moved to `paper_mapped_subset_primitivespec_native_fixture_generation_contract`.

Still unsupported:

- runtime `PrimitiveSpec` generation;
- `CollisionPackage` generation;
- runtime admissibility;
- Newton runtime support;
- approximation support for paper-only primitives;
- real-USD evidence;
- benchmark evidence;
- collision-quality validation;
- deployment readiness;
- safety certification;
- full CPD paper reproduction or `paper_faithful_offline` support.

## Next Action

Implement `paper_mapped_subset_primitivespec_native_fixture_generation_contract` as the next
offline gate. Do not claim runtime PrimitiveSpec generation, package conversion, Newton runtime
support, real-USD evidence, benchmarks, collision-quality evidence, deployment readiness, or
safety certification from this slice.
