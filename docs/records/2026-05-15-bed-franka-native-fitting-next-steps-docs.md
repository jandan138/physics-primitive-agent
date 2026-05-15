# 2026-05-15 Bed Franka Native Fitting Next Steps Docs

## Date

2026-05-15

## Status

Complete

## Changes

- Added `docs/reference/bed-franka-native-fitting-next-steps.md`.
- Linked the new next-steps guide from the documentation index.
- Linked the new guide from `docs/reference/newton-native-fitting-comparison.md`.
- Added this dated documentation record.

## Verification

- `python scripts/validate_docs.py`
- `git diff --check`

## Artifacts

- `docs/reference/bed-franka-native-fitting-next-steps.md`
- `docs/reference/newton-native-fitting-comparison.md`
- `docs/index.md`
- `docs/records/README.md`

## Claim Impact

No new experiment evidence is added. This update clarifies the next executable slice:

```text
synthetic native fitting comparison
-> real-USD old/new offline objective reports for bed and Franka
-> Newton contact canary only if mapping is clean
-> drop/settle or sphere-rain only after contact canary
```

The document keeps bed and Franka as next-scope assets, not completed old/new native-fitting
evidence.

## Next Action

Implement a config-driven real-USD old/new native fitting report runner for `bed_dev_smoke` and
`franka_import_smoke`.
