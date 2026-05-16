# 2026-05-16 CPD Paper Gap Matrix And Offline Lane Spec

## Date

2026-05-16

## Status

Complete

## Changes

- Added `docs/reference/cpd-paper-reproduction-gap-matrix.md` to separate paper requirements,
  current repository artifacts, surrogate status, offline-first work, Newton runtime admissibility,
  and claim boundaries.
- Added `docs/reference/cpd-paper-faithful-offline-lane-spec.md` to define a planned
  fixture-scoped offline paper-faithful lane before any benchmark, bed/Franka, or Newton runtime
  expansion.
- Linked the new reference pages from the project index, paper-story status page, and records
  index.
- Incorporated parallel read-only review feedback on paper mechanics, Newton primitive mapping
  boundaries, and documentation claim boundaries.

## Verification

- Passed: `python scripts/validate_docs.py`
- Passed: `python scripts/validate_site_claims.py`
- Passed: `git diff --check`
- Passed: `python -m pytest -q` (`389 passed in 41.57s`)

## Artifacts

- `docs/reference/cpd-paper-reproduction-gap-matrix.md`
- `docs/reference/cpd-paper-faithful-offline-lane-spec.md`
- `docs/records/2026-05-16-cpd-paper-gap-matrix-and-offline-lane-spec.md`
- `docs/index.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/cpd-pipeline-step-by-step-explainer.md`
- `docs/reference/claim-boundaries.md`
- `docs/records/README.md`

## Claim Impact

- No new experiment, benchmark, Newton runtime, real-USD, collision-quality, deployment, or safety
  claim is supported.
- The documentation narrows the next CPD step to an offline paper-lane specification and keeps
  current CPD-like workbench artifacts labeled as surrogates unless dated paper-faithful evidence
  exists.

## Next Action

- Implement the first offline-only toy fixture slice for paper operator, primitive-fit, and
  collapse-cost audit fields before moving to real assets or Newton package probes.
