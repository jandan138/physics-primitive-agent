# ACCV Version Status

Template provenance: official ACCV 2026 template files downloaded from `https://accv2026.org/wp-content/uploads/2026/04/ACCV_2026_template.zip` on 2026-05-26 and committed under this venue wrapper. The local gate `make -C paper check-template-accv` checks for `accv.sty`, `accvabbrv.sty`, `llncs.cls`, `splncs04.bst`, and `ACCV_TEMPLATE_LICENSE`.

Readiness: submission-readiness candidate for the scoped Phase 0 diagnostic story, pending final human submission actions in OpenReview.

Local section overrides: none. This version inputs shared sections directly.

ACCV 2026 format policy checked on 2026-05-26:

- Main paper page limit: 14 pages including figures and tables, with unlimited reference-only pages.
- Review mode: double blind; omit acknowledgements, institutional identifiers, author-identifying media, and author-identifying links.
- External links: avoid links that expand submission content, compromise anonymity, or bypass page/media/deadline limits.
- Current local build: `make -C paper accv` produces `paper/venues/accv/build/main.pdf` with 13 main-content pages plus three reference-only pages after the Fig. 1 AI-slot visual pass, reference expansion, main-PDF appendix removal, and main-text float compaction.
- Supplement local build: `make -C paper accv-supp` produces `paper/venues/accv/build/supplement.pdf`; `make -C paper accv-all` builds the main ACCV PDF and the supplement together.
- Review style: `preamble.tex` loads `accv` with `review`, `year=2026`, and placeholder `ID=*****`; replace the ID after OpenReview registration.

Known missing checks: no local ACCV template/build/docs checks remain after final verification. Manual submission actions are to replace `ID=*****` after OpenReview registration, upload through the submission system, prepare anonymized supplementary material only if needed, and broaden generated-package robot probes before making whole-robot or benchmark-superiority claims.
