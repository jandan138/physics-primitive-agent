# 2026-05-15 CPD Expected-Failure Master Verification

## Date

2026-05-15

## Status

Complete

## Changes

- Fast-forward merged `cpd-synthetic-failure-workbench-20260515` into `master`.
- Verified the expected-failure workbench slice from `master` at commit `f7b53b5`.

## Verification

- `python scripts/validate_docs.py`: exit 0, `docs validation passed`.
- `git diff --check`: exit 0, no whitespace errors.
- `python -m pytest tests/test_cpd_like_synthetic.py tests/test_cli.py -q -k "expected_failure or synthetic_comparison"`:
  exit 0, `14 passed, 38 deselected`.
- `python -m pytest -q`: exit 0, `173 passed`.

## Artifacts

- Implementation record:
  [CPD Synthetic Expected-Failure Workbench](2026-05-15-cpd-synthetic-expected-failure-workbench.md)
- Branch: `cpd-synthetic-failure-workbench-20260515`
- Master commit: `f7b53b5`

## Claim Impact

No stronger claim is added. This record only confirms that the expected-failure workbench slice was
merged and verified on `master`.

## Next Action

Use the expected-failure fixtures to select one focused primitive-fitting or merge-search
improvement before re-running bed or Franka smokes.
