# 2026-06-04 ACCV Reference Expansion

## Date

2026-06-04

## Status

Complete

## Changes

- Expanded the ACCV main-paper bibliography from 8 cited entries to 35 cited entries.
- Added 27 new cited literature entries to `paper/shared/references.bib` across four scoped
  themes: collision queries and proxy data structures, primitive/convex proxy generation,
  physics-engine and robot-simulator validation, and robot planning collision checks.
- Expanded `paper/shared/sections/related.tex` from three short paragraphs into four dense
  related-work paragraphs that cite the added literature in context.
- Added paper-layout tests that require the ACCV main paper to cite at least 30 paper-like
  references and require the related-work section to retain the four scoped literature themes.
- Kept the additions in related work and did not alter Phase 0 measurements, experiment tables,
  claims, or acceptance labels.

## Search And Screening Strategy

- Inclusion criteria: sources must directly support one of the four related-work themes and must
  be relevant to collider packages, proximity/collision checking, simulation engines, robot
  simulator benchmarks, or robot collision-validity checking.
- Exclusion criteria: general robot learning, generic computer vision, LLM, broad AI-safety, and
  unrelated asset-generation papers were excluded even if they would increase the count.
- GRScenes was not used as a paper citation because only dataset/resource pages were found during
  this pass, not a clear paper artifact.
- Metadata source: DOI content negotiation for DOI-backed entries and arXiv BibTeX for arXiv-only
  entries. A wrong DOI/title match found during screening was excluded rather than repaired by
  guesswork.

## Verification

- ACCV build:
  `make -C paper accv`; result: `paper/venues/accv/build/main.pdf` built successfully.
- ACCV main plus supplement build:
  `make -C paper accv-all`; result: `paper/venues/accv/build/main.pdf` and
  `paper/venues/accv/build/supplement.pdf` targets completed.
- Paper layout and supplement tests:
  `PYTHONPATH=$PWD/src:$PWD python -m pytest tests/test_paper_layout.py tests/test_accv_supplement.py -q`;
  result: `33 passed`.
- Full repository validation:
  `make validate`; result: docs validation passed and pytest reported
  `631 passed, 1978 deselected`.
- Reference count:
  parsed `paper/venues/accv/build/main.bbl`; result: `35` cited bibliography items, `35` unique
  keys, and `30` paper-like cited entries after excluding Newton/Warp/OpenUSD tool entries,
  Ericson's book, and the V-HACD book chapter.
- PDF page count:
  `pdfinfo paper/venues/accv/build/main.pdf | rg '^Pages:'`; result: `Pages: 17`.
- BibTeX/LaTeX integrity scan:
  `rg -n "undefined|Citation .* undefined|Warning--|I couldn't|Repeated|Duplicate|There were undefined" paper/venues/accv/build/main.log paper/venues/accv/build/main.blg`;
  result: no matches, exit 1.
- Layout warning scan:
  final `main.log` and `supplement.log` retain Underfull hbox/vbox diagnostics from figure
  floats, long supplement rows, and bibliography line breaking; no Overfull boxes or final
  `LaTeX Warning` matches were found.
- Double-blind/path leak scan over changed sources:
  scanned for absolute local paths, local user names, repository-host URLs, and center identifiers;
  result: no matches, exit 1.
- Whitespace check:
  `git diff --check`; result: no output, exit 0.

## Artifacts

- `paper/shared/references.bib`
- `paper/shared/sections/related.tex`
- `tests/test_paper_layout.py`
- `paper/venues/accv/build/main.pdf`

## Claim Impact

- No experimental, benchmark, deployment, real-world transfer, safety-certification,
  manipulation, or whole-robot collision-quality claims are added.
- The new citations strengthen literature positioning only. They do not change the evidence
  registry, Phase 0 records, or the scoped diagnostic proof-point claim.
