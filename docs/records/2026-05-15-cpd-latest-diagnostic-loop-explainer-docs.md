# 2026-05-15 CPD Latest Diagnostic Loop Explainer Docs

## Date

2026-05-15

## Status

Complete

## Changes

- Added a plain-language reference page explaining the latest candidate-loss and controlled
  cylinder-axis slice as a diagnostic loop in the CPD paper reproduction story.
- Linked the new page from the documentation index, CPD paper story status page, real-USD story
  explainer, and records index.
- Kept the claim boundary unchanged: the slice supports diagnostic accounting and Newton smoke
  gating, not collision-quality validation or full CPD reproduction.

## Verification

- `python scripts/validate_docs.py` exited 0 with docs validation passed.
- `python scripts/validate_site_claims.py` exited 0 with site claim validation passed.
- `git diff --check` exited 0.

## Artifacts

- `docs/reference/cpd-latest-diagnostic-loop-explainer.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/real-usd-native-probe-paper-story-explainer.md`
- `docs/index.md`
- `docs/records/README.md`

## Claim Impact

No new executable evidence is added. The documentation makes the latest evidence easier to read
while preserving the existing claim boundaries.

## Next Action

Use the candidate-loss diagnosis to pick one concrete primitive-fitting or merge-search target,
then reproduce that target in a synthetic fixture before rerunning bed/Franka.
