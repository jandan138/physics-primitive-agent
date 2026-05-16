# Paper Site Visual QA

## Date

2026-05-16

## Status

Complete

## Changes

- Ran reader-facing browser QA on the rendered Astro paper companion, not on source files alone.
- Fixed mobile formula overflow by allowing long source-paper tokens to wrap and promoting only
  genuinely over-wide MathML to bounded scrollable math blocks.
- Improved formula readability for narrow-screen fractions by promoting MathML fractions to
  display blocks on mobile.
- Fixed scientific-notation rendering so values such as `9.91e-3` stay compact instead of
  rendering with a spaced binary minus.
- Improved figure presentation by making plot assets span the full figure panel, adding internal
  scroll for very wide plots on narrow screens, and preventing low-resolution plot images from
  being upscaled past their source width.
- Regenerated PDF-derived paper plot assets at a higher rasterization DPI.
- Made preserved source LaTeX blocks wrap inside their panels so they remain readable without
  forcing page-level horizontal scrolling.

## Verification

- `npm --prefix site run build` exited 0 after the rendering changes.
- Browser audit at `/tmp/ppa-site-audit/final-pass-7/audit.json` covered 8 paper routes across
  desktop `1440x1000`, tablet `820x1180`, and mobile `390x844`.
- The final local browser audit reported 0 issues for every route/viewport combination, with no
  page-wide horizontal overflow, broken images, image upscaling, plot undersizing, MathML overflow,
  console errors, request failures, or scientific-notation spacing regressions.
- The final local browser audit also checked visible raw-LaTeX leakage after excluding intentional
  source blocks and hidden MathML annotation nodes, split decimal scientific notation such as
  `6.\text{95e-3}`, and scientific notation after LaTeX commands such as `\leq1e-4`; it reported
  `TOTAL_VISUAL_ISSUES=0`.
- A focused image audit after the final fixes reported `TOTAL_IMAGE_ISSUES=0` across the same
  desktop, tablet, and mobile route matrix.
- First-pass reader agents found formula, image, and source-block readability issues under:
  `/tmp/ppa-site-audit/formula-reader/`,
  `/tmp/ppa-site-audit/image-reader/`, and
  `/tmp/ppa-site-audit/layout-reader/`.
- Second-pass formula reader evidence under `/tmp/ppa-site-audit/postfix-formula-reader/` reported
  0 console errors, 0 page horizontal overflow cases, 0 raw LaTeX leaks outside source blocks, 0
  MathML render errors, and 0 math elements outside the viewport. It found a minor punctuation
  orphan after mobile display fractions; a follow-up TDD fix kept fractions inline with the
  `math-fraction` class and focused browser checks confirmed the punctuation no longer sits on a
  separate line.
- Second-pass layout reader evidence under `/tmp/ppa-site-audit/postfix-layout-reader/` covered 24
  page/viewport checks and reported no remaining reader layout issues, with 0 HTTP failures,
  console/page errors, request failures, page-wide horizontal overflow, uncontained overflow
  elements, unreadable LaTeX/code block findings, math overflow findings, badge overlap findings,
  or broken image findings.
- A second-pass image reader was also dispatched under
  `/tmp/ppa-site-audit/postfix-image-reader/`; it did not return before this record was finalized,
  so the image conclusion relies on the local focused image audit and the first-pass image-reader
  findings that were explicitly fixed.

## Artifacts

- Final local audit JSON: `/tmp/ppa-site-audit/final-pass-7/audit.json`.
- Final local screenshots: `/tmp/ppa-site-audit/final-pass-7/`.
- Focus screenshots include:
  `/tmp/ppa-site-audit/final-pass-3/mobile-method-math.png`,
  `/tmp/ppa-site-audit/final-pass-3/mobile-experiments-science.png`,
  `/tmp/ppa-site-audit/final-pass-3/mobile-additional-fraction.png`,
  `/tmp/ppa-site-audit/final-pass-3/desktop-experiments-plot.png`,
  `/tmp/ppa-site-audit/final-pass-3/desktop-method-primitives.png`, and
  `/tmp/ppa-site-audit/final-pass-3/mobile-method-latex-source.png`.
- Fraction follow-up screenshots:
  `/tmp/ppa-site-audit/final-pass-4/mobile-additional-fraction.png`,
  `/tmp/ppa-site-audit/final-pass-4/mobile-method-p013.png`, and
  `/tmp/ppa-site-audit/final-pass-4/mobile-method-p018.png`.

## Claim Impact

- This record supports only paper companion visual/readability QA for the static site.
- It does not claim CPD reproduction, benchmark validation, compiler functionality, deployment
  readiness, or formal permission completion.
- Source-paper claims remain source-paper namespaced and project reproduction statuses remain
  `not_started` unless separately backed by dated reproduction records.

## Next Action

- Keep this browser-rendered visual QA loop as the required follow-up whenever paper rendering,
  figure handling, generated paper assets, or reader CSS changes.
