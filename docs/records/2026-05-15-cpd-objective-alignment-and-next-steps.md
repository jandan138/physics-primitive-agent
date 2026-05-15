# 2026-05-15 CPD Objective Alignment And Next Steps

## Date

2026-05-15

## Status

Complete.

## Changes

- Added `docs/reference/cpd-objective-report-alignment.md` to explain that the current objective
  report is design-aligned with the CPD paper story, but not mathematically paper-faithful.
- Updated the CPD paper story status to answer whether the current objective report is
  paper-consistent.
- Updated the face-merge explainer, evidence status, claim boundaries, documentation index, and
  README to link the alignment boundary.
- Clarified the next algorithmic sequence: turn one objective-report term into a decision-making
  cost, compare on synthetic fixtures, then re-run bed and Franka smokes before changing Newton
  probes.

## Verification

- `python scripts/validate_docs.py`: passed.
- `python -m pytest -q`: 153 passed.
- `git diff --check`: passed.

## Artifacts

- `docs/reference/cpd-objective-report-alignment.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/cpd-like-face-merge-explainer.md`
- `docs/reference/claim-boundaries.md`
- `docs/deepdive/evidence-status.md`
- `docs/index.md`
- `README.md`

## Claim Impact

No new experimental claim is added. This record clarifies that "paper-aligned surrogate objective
report" means diagnostic accounting aligned with the paper story's categories, not a paper-faithful
objective implementation, not collision-quality evidence, and not full CPD reproduction.

## Next Action

Implement the first cost-guided algorithm slice against the synthetic comparison harness. The
preferred slice is one focused merge-search or primitive-fitting improvement that reuses the
existing objective report for before/after comparison.
