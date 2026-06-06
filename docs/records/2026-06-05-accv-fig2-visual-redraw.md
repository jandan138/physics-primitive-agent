# ACCV Fig. 2 Visual Redraw

Date: 2026-06-05

## Scope

Fig. 2 in the ACCV main paper was redrawn because the previous single-plate mechanism diagnostic was hard to read at paper scale. The revised figure keeps the same evidence boundary and presents the bounded bed/Franka cylinder mechanism as a three-panel diagnostic:

1. isolated target primitive passes,
2. full bed package fails,
3. mechanism audit supports COM/inertia sensitivity.

The 2026-06-05 update replaced the three panel images with realistic simulator-style visual panels so the figure reads closer to manually assembled Newton/RTX diagnostic scenes rather than generic concept art.

## Artifacts

- Composer: `src/primitive_collision_compiler/paper/fig2_mechanism_ai_slot.py`
- Slot manifest: `paper/shared/figures/assets/fig2_mechanism_ai_slots/manifest.yaml`
- Panel assets:
  - `paper/shared/figures/assets/fig2_mechanism_ai_slots/isolated_target_pass_ai.png`
  - `paper/shared/figures/assets/fig2_mechanism_ai_slots/full_package_fail_ai.png`
  - `paper/shared/figures/assets/fig2_mechanism_ai_slots/mechanism_audit_ai.png`
- Final figure:
  - `paper/shared/figures/generated/bed_franka_mechanism_diagnostic.png`
  - `paper/shared/figures/generated/bed_franka_mechanism_diagnostic.pdf`

## Claim Boundary

Pass/fail labels, final speeds, and mechanism wording remain tied to the dated cylinder mechanism records and the paper evidence manifest. The figure is not new experimental evidence, not broad cylinder evidence, not benchmark evidence, not render evidence, and not safety certification.

## Review Notes

- Raw panels were checked for complete visible objects, no pseudo-text, no cropped robot/primitive content, and realistic academic simulator/RTX rendering style.
- The composed figure uses explicit manifest crop boxes, wrapped panel text, and scoped contrast labels to keep the paper-scale view readable.
- Independent visual QA after the replacement pass reported no blocking issues for the three raw panels or the composed Fig. 2.
- ACCV page 6 was rendered from `paper/venues/accv/build/main.pdf` and inspected for paper-scale readability, clipping, caption collision, and page layout.

## Verification Targets

- `python -m pytest tests/test_fig2_mechanism_ai_slot.py tests/test_accv_visuals.py -q`
- `python -m pytest tests/test_fig2_mechanism_ai_slot.py tests/test_accv_visuals.py tests/test_paper_layout.py tests/test_accv_supplement.py -q`
- `make -C paper accv`
- `git diff --check`
