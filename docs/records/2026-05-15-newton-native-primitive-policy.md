# 2026-05-15 Newton-Native Primitive Policy

## Date

2026-05-15

## Status

Complete as a policy update. Implementation has not started.

## Changes

- Recorded the decision to make runtime primitive work Newton-native first.
- Classified the capped-cylinder proxy as an offline paper-alignment diagnostic, not the runtime
  primitive roadmap.
- Defined the next native analytic runtime bundle as `cylinder`, `cone`, and `ellipsoid` added
  together on top of the already mapped `box`, `sphere`, and `capsule`.
- Explicitly kept `frustum` and `trapezoidal_prism` out of the next runtime path.

## Verification

- Documentation-only update.
- `python scripts/validate_docs.py`: run after the update.
- `git diff --check`: run after the update.

## Artifacts

- Design:
  `docs/superpowers/specs/2026-05-15-newton-native-primitive-policy-design.md`
- Claim boundary:
  `docs/reference/claim-boundaries.md`
- CPD story map:
  `docs/reference/cpd-paper-story-status.md`
- Objective-report alignment:
  `docs/reference/cpd-objective-report-alignment.md`

## Claim Impact

No new runtime primitive support is claimed. This record supports only the planning decision that
future runtime primitive expansion should prioritize Newton-native analytic primitives over
paper-vocabulary completeness.

## Next Action

Write and execute a focused implementation plan for the native analytic primitive bundle:
`cylinder`, `cone`, and `ellipsoid`.
