# CPD Paper Mapped-Subset PrimitiveSpec Candidate-Source Contract

## Date

2026-05-17

## Status

Complete for a command-only offline/report-only PrimitiveSpec candidate-source audit. Not complete
for runtime `PrimitiveSpec` generation, `CollisionPackage` generation, package readiness, runtime
admissibility, Newton runtime, real-USD evidence, benchmarks, collision-quality measurement,
deployment readiness, or safety certification.

## Decision

Implement `paper_mapped_subset_primitivespec_candidate_source_contract` after
`paper_mapped_subset_primitivespec_generation_contract`.

The gate stays offline. It audits whether the generation-contract payload contains any eligible
current source row that a later PrimitiveSpec generator could instantiate. The current answer is
deliberately zero because the current decomposition rows remain `trapezoidal_prism` /
`offline_only_unmapped`.

## What Changed

- The CPD paper offline report now records
  `paper_mapped_subset_primitivespec_candidate_source_contract`.
- The payload classifies three native-family template rows as future-only source templates for
  box, sphere, and capsule.
- The payload classifies capped cylinder and frustum as blocked behind later approximation policy.
- The payload classifies trapezoidal prism as no-op/unmapped for this gate.
- The payload records 16 current source rows copied from the generation contract and classifies
  each as traceable but ineligible because each row is still `trapezoidal_prism` /
  `offline_only_unmapped`.
- Eligible current PrimitiveSpec candidate source count remains zero.
- PrimitiveSpec generation candidate count remains zero.
- Generated runtime PrimitiveSpec count remains zero.
- Generated CollisionPackage count remains zero.
- Runtime-admissibility check count remains zero.
- The top-level next gate is now `paper_mapped_subset_native_current_fixture_contract`.
- Input validation now rejects malformed generation-contract payloads before emitting
  candidate-source audit rows.
- Earlier gate tests were updated to expect the new top-level native-current-fixture gate and the
  expanded implemented output-contract scope after the candidate-source contract closes.

## Boundary

This is not real PrimitiveSpec generation, CollisionPackage generation, package readiness, runtime
admissibility, Newton support, approximation support, real-USD evidence, benchmark evidence,
collision-quality evidence, deployment readiness, or safety certification. Future native templates
are not current candidates. Current unmapped rows remain offline/no-op until a separate native
current-fixture or explicit mapping-policy gate exists.

## Verification

- `python -m py_compile src/primitive_collision_compiler/baselines/cpd_paper/offline.py tests/test_cpd_paper_offline.py`
  - Result: passed.
- `git diff --check`
  - Result: passed.
- `python -m pytest tests/test_cpd_paper_offline.py -k 'candidate_source or primitivespec_generation_contract_gate' -q`
  - RED result before implementation: `23 failed, 1 passed, 159 deselected`.
  - GREEN result after implementation and docs update: `24 passed, 159 deselected`.
- `python -m pytest tests/test_cli.py -k cpd_paper_offline_report -q`
  - Result: `2 passed, 109 deselected`.
- `python -m pytest tests/test_cpd_paper_offline.py -k 'changed_decomposition_output_contract_gate or package_adapter_contract_gate or package_conversion_mapped_subset_plan_gate or mapped_subset_conversion_candidate_matrix_gate' -q`
  - Result after fixing stale top-level expectations: `4 passed, 179 deselected`.
- `python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py`
  - Result: `294 passed`.
- `python -m pytest -q`
  - Result: `593 passed`.
- `python scripts/validate_docs.py`
  - Result: `docs validation passed`.
- `python scripts/validate_site_claims.py`
  - Result: `site claim validation passed`.

## Artifacts

- `src/primitive_collision_compiler/baselines/cpd_paper/offline.py`
- `tests/test_cpd_paper_offline.py`
- `tests/test_cli.py`
- `docs/superpowers/specs/2026-05-17-cpd-paper-mapped-subset-primitivespec-candidate-source-contract-design.md`
- `docs/superpowers/plans/2026-05-17-cpd-paper-mapped-subset-primitivespec-candidate-source-contract.md`
- `experiments/registry.yaml`

## Claim Impact

Supported only:

- command-only offline PrimitiveSpec candidate-source audit for deterministic synthetic fixture
  records;
- explicit future-template versus current-row separation;
- zero eligible current PrimitiveSpec candidate sources;
- next gate moved to `paper_mapped_subset_native_current_fixture_contract`.

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

Implement `paper_mapped_subset_native_current_fixture_contract` as the next offline gate. Do not
claim runtime PrimitiveSpec generation, package conversion, Newton runtime support, real-USD
evidence, benchmarks, collision-quality evidence, deployment readiness, or safety certification
from this slice.
