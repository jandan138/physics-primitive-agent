# 2026-05-21 Newton-In-The-Loop Selector Story Docs

## Date

2026-05-21

## Status

Complete.

## Changes

- Added `docs/reference/newton-in-the-loop-selector-story.md` as a plain-language summary of the
  current real-USD Newton-in-the-loop selector cycle.
- Linked the summary from the project index, bed/Franka comparison guide, real-USD paper-story
  guide, native-bundle explainer, evidence status, and claim boundaries.
- Kept the page explanatory only; it adds no new experiment result and does not broaden claims.

## Verification

- `python scripts/validate_docs.py`: exit `0`, `docs validation passed`.
- `python scripts/validate_site_claims.py`: exit `0`, `site claim validation passed`.
- `git diff --check`: exit `0`.

## Artifacts

- `docs/reference/newton-in-the-loop-selector-story.md`

## Claim Impact

- Clarifies that the 2026-05-21 guarded selector slice is one controlled opt-in diagnostic cycle:
  historical bed opt-in failed drop/settle, the guarded bed package passed the recorded task
  smokes, and guarded Franka retained its recorded smaller cylinders.
- Does not support full CPD paper reproduction, benchmark evidence, collision-quality validation,
  calibrated selector thresholds, default policy changes, deployment readiness, safety
  certification, or real-world transfer.

## Next Action

- Use this story page as the short reviewer-facing map before choosing the next controlled
  selector or fitting slice.
