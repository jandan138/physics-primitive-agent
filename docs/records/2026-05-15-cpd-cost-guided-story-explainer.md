# 2026-05-15 CPD Cost-Guided Story Explainer

## Date

2026-05-15

## Status

Complete.

## Changes

- Expanded `docs/reference/cpd-paper-story-status.md` with a plain-language explanation of the
  cost-guided merge smoke in the full CPD paper story.
- Clarified that the new change moves from "measure a merge cost" toward "use one merge cost for
  one opt-in toy merge decision."
- Added a short explanation to `docs/reference/cpd-like-face-merge-explainer.md`.
- Added a dashboard/steering analogy to `docs/reference/cpd-objective-report-alignment.md` for the
  relationship between the objective report and the new decision hook.
- Fixed cost-guided smoke wording in record indexes from plural synthetic fixtures to one
  deterministic synthetic fixture.

## Verification

- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.
- `python -m pytest -q`: passed.

## Artifacts

- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/cpd-like-face-merge-explainer.md`
- `docs/reference/cpd-objective-report-alignment.md`
- `docs/index.md`
- `docs/records/README.md`

## Claim Impact

This is a documentation clarification only. It adds no new experiment evidence and no stronger
claim. The cost-guided merge smoke remains a restricted CPD-like toy-fixture decision hook, not a
paper-faithful optimizer, collision-quality validation, benchmark result, or full CPD paper
reproduction.

## Next Action

Use this explanation when deciding the next algorithmic slice: add a specific expected-failure
synthetic fixture or one primitive-fitting improvement before broadening Newton task probes.
