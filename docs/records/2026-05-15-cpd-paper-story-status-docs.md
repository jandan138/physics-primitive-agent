# 2026-05-15 CPD Paper Story Status Docs

## Date

2026-05-15

## Status

Complete.

## Changes

- Added `docs/reference/cpd-paper-story-status.md` as a plain-language map from the CPD paper
  reproduction story to the repository's current status.
- Updated the documentation index to link the new story-status reference and this record.
- Updated the CPD-like face-merge explainer to point readers to the broader paper-story map.
- Updated evidence status to make the next CPD slice explicit: paper-aligned offline objective
  reporting and inspectable synthetic cases before stronger Newton probes or collision-quality
  claims.
- Updated the README to link both the current baseline explainer and the broader CPD paper-story
  status page.

## Verification

- `python scripts/validate_docs.py`: passed.
- `git diff --check`: passed.

## Artifacts

- `docs/reference/cpd-paper-story-status.md`
- `docs/reference/cpd-like-face-merge-explainer.md`
- `docs/deepdive/evidence-status.md`
- `docs/index.md`
- `docs/records/README.md`
- `README.md`

## Claim Impact

This update adds no new experimental evidence and no stronger supported claim. It clarifies that
the current repository is a CPD reproduction workbench with USD intake, CPD-like proposal
generation, collision-package bridging, Newton smokes, and dated records. It still does not
support full CPD paper reproduction, paper-faithful primitive optimization, benchmark results,
collision-quality validation, or robot collider-quality claims.

## Next Action

Implement a paper-aligned offline objective report for the current CPD-like baseline, then run it
on the bed smoke and small synthetic meshes with dated comparison records.
