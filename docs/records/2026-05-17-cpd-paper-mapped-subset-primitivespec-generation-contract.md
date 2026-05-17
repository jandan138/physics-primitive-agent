# CPD Paper Mapped-Subset PrimitiveSpec Generation Contract

## Date

2026-05-17

## Status

Complete for a command-only offline/report-only PrimitiveSpec generation contract. Not complete for
runtime `PrimitiveSpec` generation, `CollisionPackage` generation, package readiness, runtime
admissibility, Newton runtime, real-USD evidence, benchmarks, collision-quality measurement,
deployment readiness, or safety certification.

## Decision

Implement `paper_mapped_subset_primitivespec_generation_contract` after
`paper_mapped_subset_primitivespec_generation_preflight_contract`.

The gate stays offline. It emits template and accounting rows only, then advances the paper-lane
blocker to `paper_mapped_subset_primitivespec_candidate_source_contract`.

## What Changed

- The CPD paper offline report now records three native-family PrimitiveSpec template rows for
  future box, sphere, and capsule generation.
- Those template rows are not runtime `PrimitiveSpec` objects.
- Capped cylinder and frustum remain blocked behind a later explicit approximation policy.
- Trapezoidal prism remains no-op/unmapped.
- The report records 16 current no-generation rows for the current unmapped trapezoidal-prism
  records.
- PrimitiveSpec generation candidate count remains zero.
- Generated runtime PrimitiveSpec count remains zero.
- Generated CollisionPackage count remains zero.
- Runtime-admissibility check count remains zero.
- The top-level next gate is now `paper_mapped_subset_primitivespec_candidate_source_contract`.
- Input validation now rejects duplicate generation-preflight row ids before emitting generation
  rows.

## Boundary

This is not real PrimitiveSpec generation, CollisionPackage generation, package readiness, runtime
admissibility, Newton support, real-USD evidence, benchmark evidence, collision-quality evidence,
deployment readiness, or safety certification. Current unmapped rows remain offline/no-op until a
separate mapped current-candidate source contract or approximation-policy gate exists.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py -k 'duplicate_input_preflight_row_ids or duplicate_emitted_row_ids' -q`
  - Result: `3 passed, 159 deselected`
- `python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_generation or primitivespec_generation_preflight or offline_report_covers_first_toy_slice' -q`
  - Result: `61 passed, 101 deselected`
- `python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py`
  - Result: `272 passed`

## Review Notes

Two independent reviewers checked the implementation. One stale exact-scope test expectation was
fixed by adding `paper_mapped_subset_primitivespec_generation_contract` to the expected implemented
scope. A second review found that duplicate input generation-preflight row ids were not rechecked by
the generation-contract validator; a RED test was added, verified failing, and then fixed.

## Next Action

Implement `paper_mapped_subset_primitivespec_candidate_source_contract` as the next offline gate.
Do not claim runtime PrimitiveSpec generation, package conversion, Newton runtime support,
real-USD evidence, benchmarks, collision-quality evidence, deployment readiness, or safety
certification from this slice.
