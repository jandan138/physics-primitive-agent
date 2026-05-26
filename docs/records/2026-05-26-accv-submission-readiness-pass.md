# 2026-05-26 ACCV Submission Readiness Pass

## Date

2026-05-26

## Status

Complete for the ACCV local submission-readiness pass.

## Objective

Move the evidence-closed Phase 0 manuscript from a primary draft to an ACCV submission-readiness
candidate without strengthening claims beyond the dated records.

## ACCV Policy Check

Official ACCV 2026 author guidelines checked on 2026-05-26:

- Main paper limit is 14 pages including figures and tables, with unlimited reference-only pages.
- Submissions are double blind and must omit acknowledgements, institutional identifiers, and
  author-identifying links or media.
- External links must not expand the submission, compromise anonymity, or bypass content, page,
  media, or deadline limits.
- Submission deadline is 2026-07-05; supplementary material deadline is 2026-07-08.
- Official template zip:
  `https://accv2026.org/wp-content/uploads/2026/04/ACCV_2026_template.zip`.

## Changes

- Repaired the ACCV LaTeX build failure caused by an unescaped underscore in the Franka path.
- Added related-work citations for CPD, CoACD, V-HACD, animated approximate convex decomposition,
  real-time collision detection, Newton, Warp, and OpenUSD.
- Vendored the official ACCV 2026 text template files into `paper/venues/accv/` and switched the
  ACCV preamble to review mode with line numbering and placeholder paper ID `*****`.
- Expanded the method from a short loop description into candidate generation, acceptance,
  fallback, and evidence-registry stages.
- Reframed V-HACD failures as diagnostic rejections under the scoped Phase 0 configuration, not as
  broad V-HACD inferiority.
- Replaced the visible placeholder pipeline schematic with a submission-facing text schematic.
- Updated the ACCV status file from primary draft to submission-readiness candidate for the scoped
  diagnostic story.

## Current Build Facts

- `make -C paper accv` builds `paper/venues/accv/build/main.pdf`.
- Current ACCV PDF page count is 7 pages, including references and appendix.
- The full multi-venue `template-check` is not the ACCV gate because transfer-candidate venues
  still require their own style packages; the ACCV gate is `check-template-accv`, which checks the
  committed official ACCV template files.

## Claim Impact

Supported:

- Geometry-plausible primitive packages can fail named Newton diagnostics.
- The scoped Phase 0 table can show accepted, failed, and fallback lanes without hiding V-HACD
  failures.
- One Franka generated link-aware package is consumed by a bounded Newton robot task smoke.

Not supported:

- Production compiler readiness.
- Benchmark superiority over CPD, CoACD, V-HACD, or other convex decomposition methods.
- Whole-robot Franka collider quality, manipulation performance, deployment readiness, real-world
  transfer, safety certification, or formal verification.

## Verification

- `make -C paper check-template-accv`: passed; verifies committed official ACCV template files.
- `make -C paper accv`: passed; produced `paper/venues/accv/build/main.pdf`.
- `pdfinfo paper/venues/accv/build/main.pdf`: 7 pages.
- `pdftotext paper/venues/accv/build/main.pdf - | rg ...`: found only expected review
  placeholder paper ID `*****`; no author-identifying local path, username, acknowledgement, or
  institutional template residue.
- `python scripts/validate_docs.py`: passed.
- `make test-fast`: 512 passed, 1978 deselected.
- `git diff --check`: passed.

Reviewer-style preflight:

- Claim/anonymity reviewer reported no Critical or Important blockers after the related-work,
  method, and experiment narrative update.
- Build/reproducibility reviewers flagged the earlier TeX Live-only ACCV template gate and
  misleading all-venue `template-check` wording. This pass addressed those findings by vendoring
  the official ACCV 2026 template files, switching ACCV to review mode, updating the ACCV-specific
  template gate, and clarifying README/status wording.

## Next Action

Replace the review placeholder ID after OpenReview registration, then upload the ACCV PDF and any
needed anonymized supplementary material.
