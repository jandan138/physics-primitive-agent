# 2026-05-14 Environment Normalization

## Date

2026-05-14

## Status

Complete

## Changes

- Added a Phase 1 environment-readiness checker for Python, module provenance, Newton source state,
  GPU visibility, output writability, setup-script fingerprinting, and existing repository
  diagnostics.
- Added `scripts/env/readiness_check.py` to emit readiness JSON to stdout and an optional report
  path.
- Added `docs/operations/environment.md` with the local runtime contract and future clean-env
  installation shape.
- Kept `uv` optional until after a clean canonical runtime smoke check.
- Kept setup scripts as a trust boundary: Phase 1 records fingerprints but does not source or
  execute them.

## Verification

- `python -m pytest tests/test_environment_readiness.py -q`: exit 0, 11 passed.
- `python scripts/validate_docs.py`: exit 0.
- `git diff --check`: exit 0.

## Artifacts

- Script: `scripts/env/readiness_check.py`
- Operation doc: `docs/operations/environment.md`
- Generated report target: `reports/generated/environment-readiness/` (ignored).

## Claim Impact

- Supports only environment-readiness diagnostics.
- Does not install the canonical Python environment.
- Does not submit DLC jobs.
- Does not run Newton simulation.
- Does not implement CPD or collision proxy generation.
- Does not support benchmark superiority, deployment readiness, real-world transfer, or safety
  certification claims.

## Next Action

- Create the external clean Python 3.10 environment when ready.
- Install this repository and Newton importers into that environment.
- Run the readiness checker from the clean environment and compare the report against the current
  ambient Isaac/DSW Python evidence.
