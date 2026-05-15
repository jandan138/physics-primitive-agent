# 2026-05-15 Real USD Native Probe Story Explainer Docs

## Date

2026-05-15

## Status

Complete

## Changes

- Added a dedicated plain-language reference page for the latest real-USD bed/Franka native probe
  slice in the CPD paper story.
- Linked the new page from the CPD paper story status page and the bed/Franka native probe
  comparison page.
- Updated the documentation index and record index with the new explanatory record.

## Verification

- `python scripts/validate_docs.py` exited `0`.
- `git diff --check` exited `0`.

## Artifacts

- `docs/reference/real-usd-native-probe-paper-story-explainer.md`
- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/bed-franka-native-probe-comparison.md`
- `docs/index.md`
- `docs/records/README.md`

## Claim Impact

- Clarifies that the latest bed/Franka real-USD native probe is downstream diagnostic-path
  evidence.
- Does not add benchmark, collision-quality, native primitive improvement, whole-robot Franka, or
  full CPD reproduction claims.

## Next Action

- Improve primitive fitting or merge search using inspectable synthetic comparisons before
  re-running bed/Franka for native primitive value evidence.
