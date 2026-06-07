# 2026-06-07 ACCV Polish Submission Refresh

## Date

2026-06-07

## Status

Complete

## Changes

- Applied a narrow ACCV manuscript polish pass to the main paper and supplement.
- Reworked the main-paper contribution and method prose for clearer reviewer judgment without
  adding new results.
- Replaced visible supplement wording that read like internal tutorial or production scaffolding
  with ordinary explanatory paper language.
- Kept the supplement's explanation-plus-boundary structure while replacing repeated
  template-like figure callouts with compact reading notes.
- Refreshed the ignored local ACCV review package under `paper/submissions/accv2026-review/`.

## Verification

- Checked the ACCV 2026 author-guideline constraints used for this pass: LNCS style, anonymous
  review, 14-page main-paper content limit with reference-only pages allowed, no hidden prompts or
  review-influencing concealed content, and supplement as supporting material rather than a
  replacement for the main paper.
- `make -C paper accv-all` exited 0 after the polish edits.
- `python -m pytest tests/test_fig1_ai_slot.py tests/test_fig2_mechanism_ai_slot.py
  tests/test_accv_visuals.py tests/test_accv_supplement.py
  tests/test_supplement_tutorial_2d_slots.py tests/test_paper_layout.py -q` reported
  `110 passed`.
- `git diff --check` exited 0.
- LaTeX log scan found no overfull boxes, undefined references, undefined citations, or matched
  LaTeX warning patterns after the final build.
- `pdftotext` scans of the built main and supplement PDFs found no reviewer-facing author/path/tool
  leakage terms or removed production-style figure wording.
- `pdfinfo` reported empty title/author/subject/keyword metadata, no JavaScript, no encryption,
  16 main-PDF pages, and 20 supplement-PDF pages.
- Page contact sheets rendered from the built PDFs were visually reviewed for blank pages, severe
  gaps, clipped figures, and broken figure placement.
- `unzip -t paper/submissions/accv2026-review/accv2026-review.zip` reported no compressed-data
  errors.
- A clean local clone of the committed polish state rebuilt the ACCV main paper and supplement,
  reran the focused paper tests with `110 passed`, reported 16 main-PDF text pages and 20
  supplement-PDF text pages, passed the same reviewer-facing text scan, and passed the final LaTeX
  log scan.

## Artifacts

- Main PDF: `paper/venues/accv/build/main.pdf`
- Supplement PDF: `paper/venues/accv/build/supplement.pdf`
- Local review package: `paper/submissions/accv2026-review/accv2026-review.zip`
- Package zip SHA256:
  `8ad13f35bc499e5f6fe4165855fa0744b19f35f313e3184b562fca364111f82a`
- Package PDF SHA256 values:
  - `main.pdf`: `ff8b4dd40b4abdeeee0608c06a539633953183874cbadc1bafda5f4f0135132a`
  - `supplement.pdf`: `6295c6fc1dac53166768b00ebd8ad2279ae1db3e1bb7e0dfc6ade749bcb923f7`

## Claim Impact

- No new experimental, benchmark, robot-operation, deployment, or safety-certification claims are
  introduced.
- The polish weakens visible production-style wording and keeps the existing diagnostic-checker
  evidence boundary intact.
- Submission-portal metadata, author/conflict fields, subject areas, and final upload remain
  manual steps outside the repository record.

## Next Action

- Upload `main.pdf` and `supplement.pdf` from the refreshed local review package through the ACCV
  OpenReview submission portal.
