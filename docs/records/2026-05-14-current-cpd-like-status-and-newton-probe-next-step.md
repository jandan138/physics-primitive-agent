# 2026-05-14 Current CPD-Like Status And Newton Probe Next Step

## Date

2026-05-14

## Status

Complete

## Current State

The repository now has three separate evidence layers that should not be collapsed into one claim:

- environment readiness: the clean external Newton Python environment is recorded as
  `smoke_passed`;
- geometry baseline: the CPD-inspired restricted face-merge path can extract a capped USD mesh,
  fit `box`/`sphere`/`capsule` primitive candidates, merge adjacent face groups, and emit a JSON
  report;
- Newton simulation probes: not implemented yet.

The current executable CPD-like result is a geometry-only primitive proposal smoke path. It is not
full CPD paper reproduction and not Newton collision-quality evidence.

## Recommended Next Step

Implement the first Newton-facing diagnostic probe as a narrow vertical slice:

- consume the existing CPD-like JSON/data path;
- convert the restricted primitive proposal into a Newton-facing diagnostic input;
- run or explicitly report the smallest available Newton probe boundary;
- emit a reproducible JSON report with asset, environment, primitive count, probe status, and
  fallback or dependency-gap reason.

The first probe should prefer a deterministic smoke diagnostic over a broad benchmark. A useful
first target is a simple drop/contact or sphere-rain/contact-stress smoke, but only if Newton's
local Python API supports it cleanly in the current environment. If not, the next slice should
record the exact API gap and stop at Newton-facing package/export diagnostics.

## Claim Impact

Supported wording:

- "geometry-only CPD-like primitive proposal smoke";
- "clean local Newton Python environment readiness smoke";
- "next step is the first Newton diagnostic probe."

Unsupported wording:

- "Newton simulation checker results exist";
- "CPD has been reproduced";
- "collision quality has been evaluated";
- "Do not claim the generated primitive package is deployment-ready."

## Artifacts

- CPD-like config: `configs/experiments/cpd_like_baseline.yaml`
- Smoke asset manifest: `assets/manifests/cpd_like_smoke_assets.yaml`
- Geometry-only CPD-like record:
  `docs/records/2026-05-14-cpd-reproduction-slice.md`
- Clean environment record:
  `docs/records/2026-05-14-clean-newton-environment-readiness.md`

## Next Action

Write the Newton diagnostic probe design and implementation plan, then implement the smallest
TDD-backed probe slice in an isolated worktree.
