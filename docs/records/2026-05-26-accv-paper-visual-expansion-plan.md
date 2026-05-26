# 2026-05-26 ACCV Paper Visual Expansion Plan

## Date

2026-05-26

## Status

Proposed

## Objective

Expand the ACCV submission candidate from the current 7-page skeleton into an evidence-rich
13--14 page main paper without adding unsupported claims. The expansion should use real Phase 0
experiment evidence, deterministic diagnostic visualizations, and collision-scene render figures
rather than filler text.

ACCV 2026 limits the main paper to 14 pages including figures and tables, with additional
reference-only pages allowed. The target working length is about 13.5 main-paper pages, leaving a
small formatting margin before the hard limit.

## Current Baseline

- Current ACCV PDF: `paper/venues/accv/build/main.pdf`.
- Current page count: 7 pages.
- Current Phase 0 report: `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`.
- Current report status: `completed_with_recorded_failures`.
- Current report outcome counts: `accept=99`, `failure=11`, `fallback=30`,
  `not_applicable=70`, `dependency_gap=0`.
- Current rigid scope: five selected GRScenes assets.
- Current robot scope: one Franka smoke asset with link-aware package generation and one
  generated-package task smoke.

## Planned Main-Paper Figure Blocks

| Planned figure block | Evidence source | Purpose | Expected page gain |
|---|---|---|---|
| Phase 0 asset suite and primitive-package overlays | Phase 0 USD mirrors and generated package fields in the Phase 0 report | Show the input asset shape and the candidate collider packages side by side. | 1.5--2 pages |
| Collision-probe scene render panels | Recorded drop/settle, stack-or-slide, contact, and task-smoke scenes | Show what the diagnostics test in physical context, especially bowl/cup/tray failures. | 1--1.5 pages |
| Phase 0 outcome matrix | Phase 0 report outcome labels | Summarize accept, failure, fallback, and not-applicable outcomes without hiding failed lanes. | 1 page |
| Capped bed/Franka mechanism diagnostic figure | 2026-05-22 cylinder mechanism records | Explain why geometry-plausible primitives can fail only in full package context. | 1 page |
| Franka link-aware package and task scene figure | Link-aware generation and generated-package robot task records | Show generated package consumption by Newton bodies while preserving robot claim boundaries. | 1--1.5 pages |

The planned visual expansion should add roughly 6--7 main-paper pages when paired with expanded
method, protocol, and limitations text.

## Collision-Scene Render Scope

The collision-scene render panels should prioritize evidence value over visual polish:

- bowl/container: show a generated package that maps into Newton but is rejected by
  drop/settle and stack-or-slide diagnostics;
- cup/contact-affordance: show drop/settle rejection while contact/sphere probes can still pass;
- tray/stackable: show the V-HACD drop/settle rejection alongside lanes that pass;
- Franka generated-package task smoke: show the link-aware generated package attached to Newton
  bodies with source USD shapes suppressed.

These figures should be described as diagnostic visualizations or collision-probe scene renders,
not as photorealistic rendering evidence.

## Generation Policy

- Generate figures deterministically from repo-local ignored asset mirrors, recorded Phase 0
  package data, and dated report artifacts.
- Do not commit raw USD assets, generated 3D assets, videos, large logs, or run directories.
- Commit only small publication figures, figure manifests, and scripts when needed.
- Record figure provenance in `paper/shared/figures/sources.yaml`.
- If USD Hydra/Blender rendering is unavailable in the verified environment, use reproducible
  mesh/package overlays generated from `pxr`, `matplotlib`, or another available deterministic
  renderer.
- Do not reuse figures from source papers under `docs/tmp/papers/`.

## Claim Boundaries

This expansion does not support broad benchmark superiority, full-simulation speedup,
whole-robot manipulation performance, deployment readiness, real-world transfer, safety
certification, or formal verification claims.

The V-HACD bowl/cup/tray failures should remain visible as favorable evidence for the paper
story: V-HACD can generate packages for the selected assets, but simulation diagnostics still
reject selected lanes. That supports simulation-checked acceptance, not a blanket claim that
V-HACD is inferior.

GRScenes media and asset-license status must be checked before public submission. Until that is
resolved, the safest paper visuals are non-identifying mesh silhouettes, wireframes, primitive
overlays, and diagnostic scene views with explicit provenance rather than texture-heavy marketing
renders.

## Verification

Recorded during this planning pass:

- `git status --short --branch` showed a clean branch before edits.
- `pdfinfo paper/venues/accv/build/main.pdf` reported 7 pages.
- The Phase 0 report was parsed locally for status and outcome counts.

## Next Action

Implement the ACCV visual expansion pass:

1. add deterministic figure-generation scripts and source manifests;
2. generate compact publication figures for the planned figure blocks;
3. expand the ACCV shared method, experiment, and limitation text around those figures;
4. rebuild the ACCV PDF and keep the main-paper length between 13 and 14 pages;
5. rerun documentation and paper checks before committing the implementation.
