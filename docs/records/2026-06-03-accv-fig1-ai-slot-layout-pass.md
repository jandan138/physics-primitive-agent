# 2026-06-03 ACCV Fig. 1 AI-Slot Layout Pass

## Date

2026-06-03

## Status

Complete for the Fig. 1 and light ACCV layout pass.

## Objective

Replace the placeholder text-only ACCV Fig. 1 with an AI-slot protocol schematic while preserving
the claim boundary that generated visuals are exposition only, not experimental evidence. Apply
light ACCV layout fixes without changing the evidence packet or making stronger claims.

## Changes

- Added AI-generated visual slots for asset intake, candidate packages, Newton diagnostics, and
  decision reporting under `paper/shared/figures/assets/fig1_ai_slots/`.
- Added a slot manifest and deterministic PIL composer for
  `paper/shared/figures/generated/pipeline_schematic_ai_slot.pdf`.
- Updated Fig. 1 LaTeX integration and `paper/shared/figures/sources.yaml` provenance.
- Removed the ACCV appendix include from the main PDF wrapper so reference-only pages are not mixed
  with appendix material.
- Fixed the Phase 0 failure-label table placement to avoid late float spillover after references.
- Updated ACCV status and paper README wording from the older 7-page skeleton state.

## Claim Impact

No new experiment was added. The Fig. 1 AI-slot assets are protocol exposition only and can be
replaced by real renders later. Quantitative claims remain tied to the existing dated records,
paper evidence registry, and Phase 0 report.

## Claim Boundaries

- Do not describe Fig. 1 as runtime evidence.
- Do not claim broad benchmark superiority, full-simulation speedup, whole-robot manipulation,
  deployment readiness, real-world transfer, safety certification, or formal verification.
- Keep "simulation-checked" tied to dated Newton diagnostic records.

## Verification Scope

This pass was verified by rebuilding Fig. 1, rebuilding the ACCV PDF, visually reviewing the
standalone figure and rendered PDF page, and running the paper/layout tests plus the normal
validation lane. The ACCV page-limit boundary was checked against the ACCV 2026 author guidelines:
<https://accv2026.org/submissions/author-guidelines/>.

Final local verification:

- `python -m primitive_collision_compiler.paper.fig1_ai_slot`: PASS.
- `make -C paper check-template-accv`: PASS.
- `make -C paper accv`: PASS; `venues/accv/build/main.pdf` has 15 total pages, with main content
  on pages 1--14 and References starting on page 15.
- `make validate`: PASS; docs validation passed and `577 passed, 1978 deselected`.
- `make test-paper`: PASS; `1978 passed, 577 deselected`.
- `git diff --check`: PASS.

## Visual Review

Local render visual review completed in this session. A follow-up review found that the original
slot placement used a fill-and-crop strategy, so the wide AI slot images lost side content inside
the taller card boxes. The composer was updated to preserve the full slot image by trimming only
light outer borders and then using contain-style placement.

Follow-up iteration notes:

- Round 0: FAIL for slot completeness. Temporary edge-marker slots lost the left/right boundaries,
  reproducing the visible crop issue.
- Round 1: PASS for completeness after contain-style placement, with a WARN for excess vertical
  whitespace in each slot frame.
- Round 2: PASS after light border trimming; all four slot subjects remained complete and more
  legible.
- Round 3: PASS after reducing the slot frame height and moving badge/status rows upward; no
  badge, status, footer, or feedback-loop overlap was visible.
- Round 4: PASS after embedding at `0.98\textwidth` in the ACCV PDF; the rendered page preserved
  complete slot content, caption separation, and the 14-page main-content boundary.

Temporary inspection renders used during the pass included:

- Standalone figure: `paper/shared/figures/generated/pipeline_schematic_ai_slot.png`.
- Dense crops: `/tmp/ppa_pdf_pages/fig1_headers.png`,
  `/tmp/ppa_pdf_pages/fig1_badges_loop_footer.png`, and
  `/tmp/ppa_pdf_pages/fig1_decision_panel.png`.
- Rendered ACCV page: `/tmp/ppa_pdf_pages/accv_fig1_page_final.png`.
- Rendered references page: `/tmp/ppa_pdf_pages/accv_refs_page_final.png`.
- Follow-up rendered page: `/tmp/ppa_fig1_review_round4/accv_page-02.png`.

Verdict: PASS for the Fig. 1 and ACCV page integration. Fig. 1 has no panel-title clipping,
slot-image cropping, footer overlap, caption collision, or stale text-box placeholder. The
generated slot content is visually readable as exposition; paper-critical labels and claim-boundary
text are deterministic. The final PDF keeps main content on pages 1--14 and starts References on
page 15. Small in-panel badges are intentionally secondary to the deterministic panel headers and
caption.
