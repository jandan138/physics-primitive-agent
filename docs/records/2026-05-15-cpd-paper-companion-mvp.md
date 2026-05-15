# 2026-05-15 CPD Paper Companion MVP

## Date

2026-05-15

## Status

Complete

## Changes

- Recorded user-asserted private permission status for future full paper text, draft translation,
  paragraph annotations, figures, and GitHub Pages publication, with permission evidence still
  pending as a private record or redacted summary.
- Added an Astro + MDX CPD paper companion site scaffold.
- Added LaTeX import tooling, stricter site claim validation, and draft bilingual sample content.
- Kept explanations and reproduction notes claim-bounded as empty or not-started states until dated
  reproduction records exist.
- Withheld copied paper figure assets from the public scaffold until permission evidence is attached.

## Verification

- `npm install --ignore-scripts --loglevel warn` exited 0; dependency tree updated to
  `astro` 6.3.3 and `@astrojs/mdx` 5.0.6.
- `npm run build` exited 0; Astro built 8 static pages under `site/dist/`.
- `npm run preview -- --host 0.0.0.0 --port 4321` launched local preview; HTTP smoke checks
  against `http://localhost:4321/physics-primitive-agent/paper/` and
  `http://localhost:4321/physics-primitive-agent/paper/introduction/` returned 200 and expected
  page markers.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/test_cpd_paper_importer.py tests/test_site_claims.py -q`
  exited 0; 14 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/validate_site_claims.py` exited 0; site claim
  validation passed.
- `npm audit --audit-level=moderate` exited 0; found 0 vulnerabilities.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q` exited 0; 223 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/validate_docs.py` exited 0; docs validation passed.
- `git diff --check` exited 0.

## Artifacts

- `site/`
- `site/package-lock.json`
- `scripts/validate_site_claims.py`
- `tests/test_cpd_paper_importer.py`
- `tests/test_site_claims.py`
- `docs/superpowers/specs/2026-05-15-cpd-paper-companion-design.md`
- `docs/superpowers/plans/2026-05-15-cpd-paper-companion.md`

## Claim Impact

This supports only the existence of a permission-record-pending bilingual paper companion scaffold
with AI draft translation and source-paper claim namespacing. It does not support public full-text
release before permission evidence is attached, full CPD reproduction, benchmark claims,
collision-quality validation, production compiler readiness, or human-reviewed translation quality.

## Next Action

Review the generated bilingual pages, then incrementally add full-paper import coverage, human
translation review, and section-level reproduction notes tied to dated records.
