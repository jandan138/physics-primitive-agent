# 2026-06-06 ACCV Submission Package Readiness

## Date

2026-06-06

## Status

Complete

## Changes

- Built the ACCV main manuscript and matching supplement from the tracked LaTeX sources.
- Created an ignored local review package under `paper/submissions/accv2026-review/` containing
  `main.pdf`, `supplement.pdf`, `SHA256SUMS`, and `README.txt`.
- Checked the ACCV 2026 author-guideline constraints used for this pass: LNCS style, anonymous
  review, main-paper length counted through figures and tables with references excluded, and
  supplementary material used as supporting material rather than a page-limit bypass.
- Kept the package artifacts out of git under the existing `paper/.gitignore` submission-artifact
  policy.

## Verification

- `make -C paper accv-all` exited 0.
- `pdfinfo paper/venues/accv/build/main.pdf` reported 16 PDF pages; text extraction placed the
  first References page at page 13, so non-reference main-paper content remains within the
  14-page ACCV review limit.
- `pdfinfo paper/venues/accv/build/supplement.pdf` reported 20 PDF pages; text extraction placed
  the supplement References page at page 20.
- `pdftotext` plus case-insensitive scans found no reviewer-facing author/path/tool leakage terms
  in the built main or supplement PDFs.
- The LaTeX logs had no matched overfull-box, undefined-reference, or undefined-citation warnings
  under the project log scan used for this pass.
- `python -m pytest tests/test_fig1_ai_slot.py tests/test_fig2_mechanism_ai_slot.py
  tests/test_accv_visuals.py tests/test_accv_supplement.py
  tests/test_supplement_tutorial_2d_slots.py tests/test_paper_layout.py -q` reported
  `110 passed`.
- `git diff --check` exited 0.
- Page contact sheets rendered from the built PDFs were visually reviewed for obvious blank pages,
  severe gaps, clipped figures, and broken figure placement.
- `zip -q accv2026-review.zip main.pdf supplement.pdf SHA256SUMS README.txt` produced the local
  review package, and `unzip -l accv2026-review.zip` listed the four expected files.
- After commit `1bb8f53`, a clean local clone rebuilt the ACCV main paper and supplement, reran
  the focused paper tests with `110 passed`, reported 16 main-PDF pages and 20 supplement-PDF
  pages, passed the same reviewer-facing text scan, and passed the final LaTeX log scan.

## Artifacts

- Main PDF: `paper/venues/accv/build/main.pdf`
- Supplement PDF: `paper/venues/accv/build/supplement.pdf`
- Local review package directory: `paper/submissions/accv2026-review/`
- Package zip SHA256:
  `a6a07b4b862513a6a145a42a0d5db164e59da5726ffc477af8419af9635afea8`
- Package PDF SHA256 values:
  - `main.pdf`: `b70059da88043f502ee211b90368bb141aec97dd2106c1f1bd2c627d0409a4b1`
  - `supplement.pdf`: `e426fbbd33ffd8d56cb13c97ceb1eee1c7c00d5c7d7deb2cac9d964466340a85`

## Claim Impact

- No new experimental or deployment claims are introduced.
- The pass preserves the existing claim boundaries for simulation-checked diagnostic evidence,
  candidate collision packages, and scoped Franka/link-aware exposition.
- Human portal metadata, author/conflict fields, and final upload actions remain outside the git
  evidence record.

## Next Action

- Fill the submission portal metadata, author/conflict fields, and upload fields manually from the
  local review package.
