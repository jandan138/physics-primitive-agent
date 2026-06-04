# 2026-06-04 ACCV Main Float Layout Gap Fix

## Date

2026-06-04

## Status

Complete

## Changes

- Reworked ACCV experiment float placement to remove large reader-visible gaps after Fig. 3 and
  Fig. 6 in the main paper.
- Added bounded `\FloatBarrier` points around experiment float groups, kept large tables as
  flexible floats, anchored the outcome matrix with its explanatory text, and reduced the
  collision-probe figure width slightly.
- Enabled `\raggedbottom` and top-aligned float pages in the ACCV main wrapper so unavoidable
  white space is left at page bottoms rather than stretched between figures, captions, and text.
- Added shared preamble dependency coverage for `placeins`, `listings`, and `array` across the
  transfer-candidate venues because shared sections and macros now rely on those packages.

## Verification

- `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_paper_layout.py tests/test_accv_supplement.py -q`
  passed: 39 passed.
- `make -C paper accv-all` passed and rebuilt `venues/accv/build/main.pdf` and
  `venues/accv/build/supplement.pdf`.
- `make -C paper arxiv` passed as part of the `make -C paper all` attempt after preamble
  dependency fixes.
- `make -C paper neurips` passed.
- `make validate` passed: docs validation passed; 635 tests passed, 2 skipped, 1978 deselected.
- `git diff --check` passed.
- ACCV main log scan found no undefined citations/references, LaTeX warnings, overfull boxes, or
  underfull vbox entries after the final ACCV build.
- `make -C paper all` is still not a complete gate in this environment because ECCV stops at the
  template check: `venues/eccv/eccv.sty` is not installed or committed.

## Artifacts

- Main ACCV PDF: `paper/venues/accv/build/main.pdf`.
- Final visual review screenshots: `/tmp/accv_layout_fix_final3/main_page-08.png` through
  `/tmp/accv_layout_fix_final3/main_page-12.png`.

## Claim Impact

- No experiment result, benchmark, safety, deployment, or robot-performance claim was added.
- The change is layout/build-readiness only and preserves the existing simulation-checked claim
  boundaries.

## Next Action

- Install or vendor the ECCV author-kit style before using `make -C paper all` as a full
  multi-venue release gate.
