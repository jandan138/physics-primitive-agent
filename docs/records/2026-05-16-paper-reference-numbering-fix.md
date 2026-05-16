# Paper Reference Numbering Fix

## Date

2026-05-16

## Status

Complete

## Changes

- Updated the CPD paper importer to collect LaTeX labels from sections, paragraphs, figures,
  tables, algorithms, and display equations.
- Added deterministic paper-number assignment for imported figure, table, algorithm, equation, and
  section references.
- Regenerated the paper MDX so reader-facing text uses labels such as `Fig. 4`, `Alg. 3`,
  `Eq. (1)`, and `Sec. 3.3` instead of internal source labels such as `fig:primitives` or
  `method / figure / method-l004`.
- Counted unlabeled numbered equations and captioned floats, omitted labels for unnumbered display
  equations, and used `Inset` for uncaptioned figure-like image blocks.
- Extended site claim validation to reject reader-visible internal paper block labels, generic
  figure/equation labels, placeholder figure captions, and unresolved paper reference tokens in
  generated paper pages.

## Review

- Multi-agent site/importer review found that the initial generated MDX still exposed
  `Alg. isotrap` in `additional-results.mdx`; the root cause was stale generated paper content
  rather than an uncovered importer code path. Regenerating with the current importer resolved the
  issue.
- Focused validation then exposed stale generated generic labels and placeholder captions; a second
  regeneration with asset output resolved those generated-content issues without leaving tracked
  paper assets deleted.
- Multi-agent docs/claim review found stale next-gate text in the CPD paper gap matrix and offline
  lane spec. The docs now point to `paper_capsule_axis_policy_audit`.
- Post-fix multi-agent review found no remaining Critical or Important issues after `validate_docs`,
  `validate_site_claims`, `git diff --check`, full pytest, and site build passed.

## Verification

- Passed: `python -m pytest -q` (`406 passed in 43.94s`).
- Passed: `PYTHONDONTWRITEBYTECODE=1 python site/scripts/import_cpd_paper.py --source docs/tmp/papers/arXiv-2602.07369v1 --output site/src/content/paper --translations site/src/data/translations --asset-output site/public/paper-assets`
  (exit `0`; regenerated paper MDX and paper web assets with current importer).
- Passed:
  `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_cpd_paper_importer.py tests/test_site_claims.py tests/test_cpd_paper_offline.py`
  (`61 passed in 0.65s`).
- Passed: `python scripts/validate_site_claims.py` (`site claim validation passed`).
- Passed: `python scripts/validate_docs.py` (`docs validation passed`).
- Passed: `git diff --check` (no output).
- Passed: `npm --prefix site run build` (8 pages built in 7.70s).

## Artifacts

- `site/scripts/import_cpd_paper.py`
- `site/src/content/paper/*.mdx`
- `site/src/components/EquationBlock.astro`
- `site/src/components/FigurePanel.astro`
- `scripts/validate_site_claims.py`
- `tests/test_cpd_paper_importer.py`
- `tests/test_site_claims.py`

## Claim Impact

- Supports only a reader-facing paper companion import/formatting improvement.
- Does not claim CPD reproduction, compiler functionality, benchmark validation, deployment
  readiness, source-asset permission completion, or collision-quality evidence.

## Next Action

- Keep imported paper references resolved to reader-facing numbers during future companion-site
  regeneration.
