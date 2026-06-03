# ACCV Supplement Tutorial Atlas Design

## Date

2026-06-03

## Objective

Build a standalone ACCV-style supplementary PDF that helps reviewers understand the scoped
simulation-checked primitive-collider story through tutorial explanations, mathematical
derivations, implementation details, provenance records, and new rendered/diagnostic figures.
The supplement should be at least 20 pages and may be longer if the layout remains readable.

## Hard Constraints

- The main ACCV PDF remains self-contained. The supplement must clarify and deepen the paper, not
  carry claims that are required for the main paper to make sense.
- Supplement figures must not duplicate figures that already appear in the main paper. Reusing the
  same evidence records or assets is allowed only when the rendered view, annotation, composition,
  or teaching purpose is new.
- Supplement tables must not duplicate tables that already appear in the main paper. Tables should
  be glossary, notation, predicate, parameter, provenance, artifact, or claim-boundary tables.
- Avoid pages containing only one figure or one table. Every figure/table page should include
  explanatory prose, equations, glossary entries, or adjacent panels unless the final ACCV template
  layout makes this impossible.
- Preserve ACCV double-blind anonymity. No author names, institutions, usernames, non-anonymous
  URLs, or repository-hosting links appear in the supplement.
- Preserve project claim boundaries. Do not claim broad benchmark superiority, full-simulation
  speedup, whole-robot collision quality, manipulation performance, deployment readiness,
  real-world transfer, safety certification, or formal verification.
- Do not commit raw 3D assets, large logs, run directories, or videos. Commit only small PDF/PNG
  figure outputs, compact manifests, LaTeX sources, records, and tests.

## ACCV Packaging

The supplement is a separate PDF built from `paper/venues/accv/supplement.tex` using the same ACCV
LNCS class, anonymous review package settings, shared math macros, shared venue macros, and shared
bibliography resolution as `paper/venues/accv/main.tex`.

The main paper must not input the supplement. The paper Makefile should expose:

- `make accv` for the main PDF only.
- `make accv-supp` for `paper/venues/accv/build/supplement.pdf`.
- `make accv-all` for both main and supplement.

The supplement may reuse the main bibliography file. It should include a short front-matter block
stating that the main paper is self-contained and that the supplement is tutorial/provenance
material.

## Content Architecture

### S1. Reviewer Guide

Purpose: orient the reader. Explain which sections are tutorial, which are derivations, which are
provenance, and which are extra visual evidence. Restate that supplement figures/tables are new
views or explanatory artifacts, not copies of main-paper figures/tables.

Expected content:

- A compact "how to read this supplement" paragraph.
- A non-claim-expanding roadmap.
- A claim-boundary reminder.

### S2. Notation and Package Model

Purpose: define the mathematical objects hidden behind the main-paper prose.

Expected content:

- Asset, mesh primitive, source USD prim, candidate primitive, package, body, link, diagnostic
  scene, probe, outcome, and fallback notation.
- A non-duplicative notation table.
- Equations for package ownership:
  `p_i = (k_i, F_i, T_i, \theta_i, \ell_i)` and the body attachment map
  `a(p_i) = b_{\ell_i}` when link identity is preserved.

### S3. Diagnostic Predicate Derivations

Purpose: make the named probes easy to audit.

Expected content:

- Drop/settle predicate with final speed, final height, floor breach, and descent terms.
- Stack-or-slide predicate with final contact, horizontal displacement, probe support height, and
  residual speed terms.
- Sphere-rain/contact predicate explanation without overclaiming physical coverage.
- Franka generated-package consumption predicate with missing body links, source-shape
  suppression, and generated self-collision filter accounting.
- Small predicate tables and inline equations, not copied result tables.

### S4. Compound Body-State Mechanism

Purpose: teach why candidate shape plausibility and package-level simulation acceptance can
diverge.

Expected content:

- COM and inertia aggregation derivation for a compound package.
- Explanation of why isolated-primitive success does not imply full-compound success.
- A new teaching figure that contrasts single primitive, full package, and diagnostic gate using
  new panels/annotations rather than the main mechanism figure.

### S5. Link-Aware Robot Package Semantics

Purpose: explain the robot-specific ownership constraint.

Expected content:

- Link graph and body attachment definitions.
- Cross-link merge violation predicate.
- Meshless sentinel explanation for `/panda/panda_link8` without implying whole-robot quality.
- New RTX or deterministic-render figures showing multiple Franka views, link ownership, source
  shape suppression, and package attachment. These figures must not duplicate the main Fig. 7
  plate.

### S6. Visual Evidence Atlas

Purpose: add reviewer-friendly qualitative evidence without duplicating main figures.

Expected content:

- New rendered/diagnostic plates for rigid assets and Franka.
- Multi-panel storyboards for failure labels: initial state, final state, measured symptom, emitted
  label.
- Side-by-side candidate-lane anatomy where the annotation scheme differs from the main overlays.
- Every plate should have text on the same page explaining what to look for and what not to infer.

### S7. Implementation and Reproducibility Notes

Purpose: explain how records, configs, manifests, and sidecars fit together.

Expected content:

- Config/report path glossary with anonymous artifact names.
- Sidecar schema snippets and hashes.
- Exact local build/generation commands.
- Explanation of why ignored raw assets and large logs are not committed.

### S8. Claim Boundary and Limitations

Purpose: prevent overreading.

Expected content:

- Supported vs unsupported statement table.
- Additional evidence required for broader benchmark, robot, deployment, or safety claims.
- Reminder that generated collision packages are safety-affecting artifacts requiring review.

## Figure Policy

Supplement figures should be generated from deterministic code under `src/primitive_collision_compiler/paper/`
or short scripts under `scripts/paper/`. Preferred figure families:

- `supplement_franka_multiview`: new Franka package views, using the already reviewed RTX source
  render where appropriate or deterministic 2D compositions when a fresh RTX session is unstable.
- `supplement_predicate_diagrams`: explanatory diagrams for drop/settle, stack-or-slide,
  sphere-rain, and generated-package consumption predicates.
- `supplement_failure_storyboards`: new storyboards from Phase 0 recorded labels and metrics.
- `supplement_provenance_map`: record/config/report/figure sidecar flow.

Each generated figure needs a compact sidecar/manifest recording source reports, source figures if
composited, hashes, renderer/composer, and claim boundary.

## Table Policy

Supplement tables should be compact and explanatory:

- notation table;
- predicate glossary;
- diagnostic parameter table;
- artifact/provenance table;
- claim-boundary table.

Do not copy `tab:phase0-grscenes-rigid` or `tab:phase0-failure-labels` from the main paper.

## Layout Policy

- Use the ACCV/LNCS format and the same visual tone as the main paper.
- Prefer `figure` placements with text before and after; avoid global `[H]` for large floats in
  the supplement unless it prevents worse float-only pages.
- Use `minipage` or compact composite plates to keep prose and visual evidence together.
- Use `\paragraph{...}` teaching callouts for "What this shows" and "What this does not show."
- Run visual review on rendered supplement pages after each major figure batch.

## Tests and Verification

Add tests that assert:

- ACCV supplement entrypoint exists and main paper does not input it.
- `paper/Makefile` includes `accv-supp` and `accv-all` targets.
- Supplement source includes the hard-constraint phrases and avoids forbidden positive claims.
- Supplement source does not include main figure output filenames or main table labels.
- Supplement figure manifests exist and record source hashes.

Build and visual verification:

- `cd paper && make accv-supp`.
- `cd paper && make accv-all`.
- `pdfinfo paper/venues/accv/build/supplement.pdf` should report at least 20 pages.
- Render selected pages with `pdftoppm` and inspect for clipping, unreadable text, duplicate main
  figures/tables, or float-only pages.
- Run `git diff --check`, `python scripts/validate_docs.py`, and the focused paper tests before
  commit.

## Review Gates

- Clean-room structure review after the scaffold and outline are written.
- Visual review after the first generated figure batch.
- Code/paper-source review before merge.

## Non-Goals

- Do not add new experimental claims unless a dated record and evidence registry update supports
  them.
- Do not make the supplement a camera-ready appendix for a different venue.
- Do not introduce raw USD/video/log artifacts into git.
- Do not turn the supplement into a marketing deck; it should remain reviewer-facing technical
  evidence and teaching material.
