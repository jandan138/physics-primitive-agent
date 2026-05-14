# 2026-05-14 CPD-Like Face-Merge Explainer

## Date

2026-05-14

## Status

Complete for the current documentation clarification.

## Changes

- Added `docs/reference/cpd-like-face-merge-explainer.md`.
- Documented the plain-language meaning of the current geometry-only CPD-like face-merge baseline.
- Clarified where the repository currently sits in the CPD paper story:
  mesh intake is partially in place, the current primitive proposal path is a simple baseline, the
  Newton path is contact-only, and paper-scope evaluation has not started.
- Repeated safe and unsafe wording so reviewer-facing documents do not accidentally upgrade the
  current smoke path into a CPD reproduction claim.

## Verification

- `python scripts/validate_docs.py`: exit 0.
- `git diff --check`: exit 0.

## Artifacts

- Explainer: `docs/reference/cpd-like-face-merge-explainer.md`
- Related geometry smoke record: `docs/records/2026-05-14-cpd-like-geometry-smoke-slice.md`
- Related Newton contact smoke record: `docs/records/2026-05-14-newton-contact-smoke.md`

## Claim Impact

Supported:

- clearer explanation of "geometry-only CPD-like face-merge primitive proposal smoke";
- clearer separation between a primitive proposal baseline and a full CPD paper reproduction;
- clearer explanation of why a temporary baseline exists before paper-scope implementation.

Not supported:

- any new algorithmic result;
- full CPD paper reproduction;
- collision quality;
- benchmark superiority;
- task-level Newton simulation evidence;
- safety, deployment, or real-world transfer claims.

## Next Action

Use the explainer as the human-readable reference when discussing the current baseline. Continue
technical progress with the first task-level Newton diagnostic probe before strengthening any CPD or
collision-quality claims.
