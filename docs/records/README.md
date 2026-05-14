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

## Current Record Index

- [2026-05-14 Project Bootstrap](2026-05-14-project-bootstrap.md): DeepDive-first repository
  bootstrap.
- [2026-05-14 CPD-Like Newton Source And Assets](2026-05-14-cpd-like-newton-source-and-assets.md):
  Newton source and initial asset choices.
- [2026-05-14 CPD-Like Newton Slice](2026-05-14-cpd-like-newton-slice.md): CPD-like
  planning slice.
- [2026-05-14 Newton USD Smoke](2026-05-14-newton-usd-smoke.md): USD asset-open smoke
  diagnostics.
- [2026-05-14 Environment Normalization](2026-05-14-environment-normalization.md): Phase 1
  environment-readiness checker, docs, and tests.
- [2026-05-14 Environment Readiness Master Verification](2026-05-14-environment-readiness-master-verification.md):
  post-merge `master` readiness status and verification evidence.
- [2026-05-14 Clean Newton Environment Readiness](2026-05-14-clean-newton-environment-readiness.md):
  clean external conda environment creation and `smoke_passed` readiness evidence.
- [2026-05-14 CPD-Like Geometry Smoke Slice](2026-05-14-cpd-like-geometry-smoke-slice.md): geometry-only
  CPD-like face-merge primitive proposal smoke evidence.
- [2026-05-14 CPD-Like Face-Merge Explainer](2026-05-14-cpd-like-face-merge-explainer.md):
  plain-language clarification of the current baseline and its CPD paper-story boundary.
- [2026-05-14 Current CPD-Like Status And Newton Probe Next Step](2026-05-14-current-cpd-like-status-and-newton-probe-next-step.md):
  separates clean environment readiness, geometry-only CPD-like evidence, and the unimplemented
  Newton simulation probe layer.
- [2026-05-14 Newton Contact Smoke](2026-05-14-newton-contact-smoke.md): first contact-only
  Newton canary consuming CPD-like primitive proposals.
