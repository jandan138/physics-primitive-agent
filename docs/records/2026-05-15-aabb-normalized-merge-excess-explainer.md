# 2026-05-15 AABB-Normalized Merge-Excess Explainer

## Date

2026-05-15

## Status

Complete.

## Changes

- Added a plain-language explanation of AABB-normalized merge-excess to
  `docs/reference/cpd-objective-report-alignment.md`.
- Added a shorter "empty wrapper space" explanation to
  `docs/reference/cpd-like-face-merge-explainer.md`.
- Added the cost definition and current toy-fixture numbers to
  `docs/reference/cpd-paper-story-status.md`.
- Linked this record from the documentation index and records index.

## Verification

- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.
- `python -m pytest -q`: passed.

## Artifacts

- `docs/reference/cpd-objective-report-alignment.md`
- `docs/reference/cpd-like-face-merge-explainer.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/index.md`
- `docs/records/README.md`

## Claim Impact

This is a documentation clarification only. It does not add experiment evidence or strengthen the
cost-guided smoke claim. AABB-normalized merge-excess remains a geometry-only surrogate for
diagnostic accounting and one restricted toy merge decision, not a collision-quality metric,
benchmark result, paper-faithful objective, or CPD optimizer.

## Next Action

Use this definition when comparing future synthetic fixtures or primitive-fitting improvements.
