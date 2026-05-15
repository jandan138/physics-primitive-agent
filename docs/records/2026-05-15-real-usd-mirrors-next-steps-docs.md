# 2026-05-15 Real USD Mirrors Next Steps Docs

## Date

2026-05-15

## Status

Complete

## Changes

- Expanded the asset mirror materialization reference with the repo-local mirror norm, runtime
  resolution rule, bed and Franka closure details, git artifact boundaries, and mirror check
  workflow.
- Added a plain-language next-steps reference for CPD-like work after the real-USD mirrors.
- Updated the CPD paper story status and documentation index to point to the next algorithmic
  sequence.

## Verification

- `python scripts/validate_docs.py` exited 0; docs validation passed.
- `git diff --check` exited 0.

## Artifacts

- `docs/reference/asset-mirror-materialization.md`
- `docs/reference/cpd-next-steps-after-real-usd-mirrors.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/index.md`
- `docs/records/README.md`

## Claim Impact

This is a documentation clarification only. It does not add benchmark evidence, collision-quality
evidence, native primitive improvement evidence, whole-robot Franka collider-quality evidence, or
full CPD paper reproduction evidence.

## Next Action

Implement the candidate-loss diagnosis report so the current real-USD box selections can be
explained before changing primitive fitting or merge search.
