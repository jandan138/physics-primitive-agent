# 2026-05-15 CPD Full Text Import And Translation

## Date

2026-05-15

## Status

Complete

## Changes

- Expanded the CPD companion importer to include the main-paper abstract and all body section files
  referenced by `main.tex`.
- Preserved source-paper figures, algorithms, tables, and equations as gated LaTeX blocks instead
  of publishing copied paper assets before permission evidence is attached.
- Generated full-section MDX pages under `site/src/content/paper/` with 127 translated
  source-paper prose/caption blocks and no empty draft translations.
- Added AI-assisted Simplified Chinese draft translation JSON shards under
  `site/src/data/translations/`.
- Kept every generated `PaperBlock` namespaced as `cpd_paper_source_text` and every reproduction
  state at `not_started`.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_cpd_paper_importer.py tests/test_site_claims.py -q`
  exited 0; 25 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/validate_site_claims.py` exited 0; site claim
  validation passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/validate_docs.py` exited 0; docs validation passed.
- `npm audit --audit-level=moderate` exited 0; found 0 vulnerabilities.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q` exited 0; 237 tests passed.
- `npm run build` exited 0; Astro built 8 static paper pages.
- `git diff --check` exited 0.

## Artifacts

- `site/scripts/import_cpd_paper.py`
- `site/src/components/LatexBlock.astro`
- `site/src/content/paper/`
- `site/src/data/translations/`
- `tests/test_cpd_paper_importer.py`
- `tests/test_site_claims.py`
- `docs/superpowers/plans/2026-05-15-cpd-full-text-import-translation.md`

## Claim Impact

This supports only a permission-record-pending full-text paper companion draft with source-paper
claim namespacing. It does not support public paper asset publication, human-reviewed translation
quality, project-side CPD reproduction, benchmark claims, compiler readiness, or safety validation.

## Next Action

Attach the permission record or redacted permission summary, then enable the public asset/full-text
publication gate and begin section-by-section human translation review.
