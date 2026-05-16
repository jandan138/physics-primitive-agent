# 2026-05-16 CPD Pipeline Step-By-Step Explainer

## Date

2026-05-16

## Status

Complete

## Changes

- Added `docs/reference/cpd-pipeline-step-by-step-explainer.md`.
- The new explainer separates the CPD algorithm steps, Newton workbench steps, and benchmark
  evaluation step in plain language.
- It clarifies where the latest four-block slice report fits: a command-only evidence map for one
  recorded synthetic slice, not a new algorithm or new Newton result.

## Verification

- `python scripts/validate_docs.py`: `docs validation passed`.
- `python scripts/validate_site_claims.py`: `site claim validation passed`.
- `git diff --check`: passed with no output.

## Claim Impact

- No new experiment evidence is added.
- No full CPD paper reproduction, benchmark, collision-quality, real-asset improvement,
  deployment, certification, or safety claim is added.

## Next Action

- Use the explainer as the first reference when explaining how the CPD algorithm, Newton
  workbench, and benchmark/evaluation layers differ.
