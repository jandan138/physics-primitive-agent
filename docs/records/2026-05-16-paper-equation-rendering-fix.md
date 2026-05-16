# Paper Equation Rendering Fix

## Date

2026-05-16

## Status

Complete

## Changes

- Fixed reader-visible display-math blocks that were rendered as preserved LaTeX source blocks on
  the paper companion pages.
- Added an `EquationBlock` component that renders source-paper `equation` and `align` environments
  through KaTeX MathML while leaving non-math LaTeX environments, such as algorithms, in the
  preserved-source path.
- Updated the CPD paper importer so regenerated MDX emits `EquationBlock` for display math.
- Regenerated the paper MDX so `background-l001`, `method-l005`, `method-l006`, `method-l007`,
  and `method-l008` are rendered formulas instead of fenced LaTeX blocks.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_cpd_paper_importer.py tests/test_site_claims.py`
  exited 0 with 45 passed.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/validate_site_claims.py` exited 0.
- `PYTHONDONTWRITEBYTECODE=1 python scripts/validate_docs.py` exited 0.
- `git diff --check` exited 0.
- `npm --prefix site run build` exited 0 and built 8 pages.
- Browser audit at `/tmp/ppa-site-audit/fig-fix/audit.json` checked the affected background and
  method equation blocks on desktop `1125x647` and mobile `390x844`, with no console errors,
  page errors, failed requests, page-wide overflow, raw `\begin{equation}` or `\begin{align}`
  leakage, or `pre` blocks inside display-math components.

## Artifacts

- Audit JSON: `/tmp/ppa-site-audit/fig-fix/audit.json`.
- Focus screenshots:
  `/tmp/ppa-site-audit/fig-fix/desktop-background-l001.png`,
  `/tmp/ppa-site-audit/fig-fix/desktop-method-l008.png`,
  `/tmp/ppa-site-audit/fig-fix/mobile-background-l001.png`, and
  `/tmp/ppa-site-audit/fig-fix/mobile-method-l008.png`.
- User-provided issue screenshots remain under `docs/tmp/fig/`.

## Claim Impact

- This record supports only the reader-facing paper companion equation-rendering fix.
- It does not claim CPD reproduction, compiler functionality, benchmark validation, deployment
  readiness, or paper-asset permission completion.

## Next Action

- Keep `equation` and `align` environments on the rendered-math path during future paper imports.
