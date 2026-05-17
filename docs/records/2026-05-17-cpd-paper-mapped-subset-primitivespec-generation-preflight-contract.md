# CPD Paper Mapped-Subset PrimitiveSpec Generation Preflight Contract

## Date

2026-05-17

## Status

Complete for an offline/report-only generation-preflight contract. Not complete for real
PrimitiveSpec generation, CollisionPackage generation, package readiness, Newton runtime, real-USD
evidence, benchmarks, collision-quality measurement, deployment readiness, or safety certification.

## Decision

Implement `paper_mapped_subset_primitivespec_generation_preflight_contract` as a command-only
offline report gate after `paper_mapped_subset_primitivespec_validation_contract`.

## What Changed

- The CPD paper offline report now records PrimitiveSpec generation-preflight requirement rows for
  six paper primitive families.
- OBB/box, sphere, and capsule are recorded as future native-family generation requirements.
- Capped cylinder and frustum remain blocked behind approximation policy.
- Trapezoidal prism remains no-op/unmapped.
- The report now records 16 current no-op generation-preflight rows for unmapped
  trapezoidal-prism rows.
- Generation-preflight candidate count is zero.
- Generated PrimitiveSpec count is zero.
- Generated CollisionPackage count is zero.
- Runtime-admissibility check count is zero.
- The top-level next gate is now `paper_mapped_subset_primitivespec_generation_contract`.

## Boundary

This is not real PrimitiveSpec generation, CollisionPackage generation, package readiness, runtime
admissibility, Newton support, real-USD evidence, benchmark evidence, collision-quality evidence,
deployment readiness, or safety certification. Current unmapped rows remain offline/no-op.

## Verification

- `python -m pytest tests/test_cpd_paper_offline.py -k 'primitivespec_generation_preflight or primitivespec_validation or offline_report_covers_first_toy_slice' -q`
  - Result: `57 passed, 70 deselected`
- `python -m pytest tests/test_cli.py -k cpd_paper_offline -q`
  - Result after CLI assertion expansion: `2 passed, 109 deselected in 1.05s`
- Reviewer-run focused verification:
  `python -m pytest -q tests/test_cpd_paper_offline.py tests/test_cli.py`
  - Result: `238 passed`

## Next Action

Implement `paper_mapped_subset_primitivespec_generation_contract` as the next offline gate without
claiming package readiness, Newton runtime support, real-USD evidence, benchmarks, collision
quality, deployment readiness, or safety certification.
