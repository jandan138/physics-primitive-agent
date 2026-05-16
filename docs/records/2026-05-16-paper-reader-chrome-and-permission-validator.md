# 2026-05-16 Paper Reader Chrome And Permission Validator

## Date

2026-05-16

## Status

Complete

## Changes

- Removed reader-visible internal review chrome from `PaperBlock` output while keeping status
  fields as machine-readable `data-*` attributes.
- Removed stale badge/status CSS and the unused `StatusBadge` component after the reader no longer
  renders those badges.
- Split `FigurePanel` images into visual, inset, and plot groups so long plots no longer force the
  main thumbnail grid to behave like one wide strip.
- Extended site claim validation so paper assets are not allowed by filename-only placeholder
  permission records. The validator now requires explicit user-asserted or formal permission
  evidence markers inside the dated record.

## Verification

- `python -m pytest tests/test_site_claims.py -q` exited 0; 26 tests passed.
- `python -m pytest -q` exited 0; 412 tests passed.
- `python scripts/validate_site_claims.py` exited 0; site claim validation passed.
- `python scripts/validate_docs.py` exited 0; docs validation passed.
- `git diff --check` exited 0.
- `npm --prefix site run build` exited 0; Astro built 8 static paper pages.
- Multi-agent review found no Critical or Important issues after tightening permission-evidence
  validation and removing stale reader chrome CSS/API.

## Artifacts

- `scripts/validate_site_claims.py`
- `tests/test_site_claims.py`
- `site/src/components/FigurePanel.astro`
- `site/src/components/PaperBlock.astro`
- `site/src/layouts/PaperLayout.astro`
- `site/src/styles/paper.css`
- `site/README.md`

## Claim Impact

- Preserves source-paper and project-claim separation in the CPD paper companion site.
- Does not support formal permission completion, human-reviewed translation quality, project-side
  CPD reproduction, benchmark evidence, collision-quality validation, deployment readiness, or
  safety certification.

## Next Action

- Attach the formal permission artifact or redacted permission summary when supplied by the user.
