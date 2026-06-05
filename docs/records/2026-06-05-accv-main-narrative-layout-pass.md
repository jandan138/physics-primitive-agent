# ACCV Main Narrative And Layout Pass

Date: 2026-06-05

## Summary

- Reframed the ACCV main paper around simulation-checked acceptance as an explicit gate between
  candidate primitive packages and executable Newton task artifacts.
- Revised the abstract, introduction, method, experiments, discussion, and conclusion to reduce
  repeated claim-boundary bookkeeping while preserving the recorded evidence scope.
- Compacted the main-paper failure-label table float so the failure-label and Franka sections no
  longer leave a large mid-paper blank region.
- Updated the ACCV status note and layout regression tests for the current 13 main-content pages
  plus three reference-only pages.

## Evidence Boundary

This pass changes wording and float placement only. It does not add experiments, change figure
assets, change reported numbers, or broaden claims beyond the existing `claims.yaml` registry and
`docs/reference/claim-boundaries.md`.

## Verification

- `make -C paper accv-all`: passed; `paper/venues/accv/build/main.pdf` has 16 total pages and
  `paper/venues/accv/build/supplement.pdf` has 20 total pages.
- `python -m pytest tests/test_paper_layout.py tests/test_accv_visuals.py tests/test_accv_supplement.py -q`:
  99 passed.
- `git diff --check`: passed.
- Visual audit artifact: `/tmp/accv-main-layout-audit-after/contact_p01_p14.png` showed the
  previous large page-11 blank region removed after the failure-label table float compaction.
