# Records

Records are durable dated notes for decisions, verification, failures, and evidence changes.
Every record should be short enough to read during review and concrete enough to reproduce the
state it describes.

## Record Template

```md
# YYYY-MM-DD Short Title

## Date

YYYY-MM-DD

## Status

Proposed | In progress | Complete | Failed | Superseded

## Changes

- What changed.

## Verification

- Commands run and exit status.

## Artifacts

- Paths to configs, reports, logs, or asset manifests.

## Claim Impact

- Claims now supported, unchanged, or explicitly not supported.

## Next Action

- The next concrete step.
```

## Rules

- Link claims to records before using them in DeepDive updates.
- Record failures and fallback decisions; do not only record successful runs.
- Keep large logs and generated artifacts outside git and link their manifest path instead.
