# 2026-05-26 Phase 0 Paper Evidence Closure

## Date

2026-05-26

## Status

Complete for the current Phase 0 paper-evidence closure pass.

## Objective

Freeze the current paper-facing evidence packet for the scoped Phase 0 story. This closure does
not add new experiments. It aligns the existing records, paper evidence manifests, and experiments
section so the manuscript can cite the evidence without upgrading claim strength.

## Evidence Packet

| Evidence block | Primary record | Paper use |
|---|---|---|
| Capped bed/Franka cylinder mechanism | `docs/records/2026-05-22-cylinder-goal-completion-audit-after-contact-closure.md` | Shows geometry-plausible primitives can fail only in full package context. |
| Package body-state guard task path | `docs/records/2026-05-22-package-body-state-guard-task-path.md` | Shows fallback can be package-local and diagnostic rather than hidden. |
| Bed-aligned contact-throughput hook | `docs/records/2026-05-22-bed-aligned-box-primitive-contact-throughput.md` | Provides one collision-only performance hook for accepted native boxes. |
| Phase 0 rigid/V-HACD diagnostic outcomes | `docs/records/2026-05-26-phase0-vhacd-runtime-followup.md` | Shows candidate packages are accepted, rejected, or routed to fallback by named Newton probes. |
| Franka link-aware generated-package robot smoke | `docs/records/2026-05-26-generated-package-robot-task-probe.md` | Shows one generated link-aware Franka package is consumed by a Newton robot task smoke. |

The authoritative generated report remains ignored by git:

- `reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json`

## Current Report Facts

- Report status: `completed_with_recorded_failures`.
- Outcome counts: `accept=99`, `failure=11`, `fallback=30`, `not_applicable=70`,
  `dependency_gap=0`.
- V-HACD generated packages for all five selected rigid assets with hull counts
  `[1, 16, 16, 16, 16]`.
- V-HACD diagnostic failures are recorded on:
  - bowl/container: drop/settle labels `no_descent`, `not_settled`, `floor_breach`; stack/slide
    labels `excess_horizontal_slide`, `probe_below_support`;
  - cup/contact-affordance: drop/settle label `not_settled`;
  - tray/stackable: drop/settle label `not_settled`.
- Franka generated-package task smoke records `smoke_passed` and `accept`, with 12 generated
  collision shapes, 12 consumed package primitives, zero missing body links, zero source USD
  collision shapes remaining, and 66 generated self-collision filter pairs.

## Paper Claims That Are Supported

- Simulation-checked acceptance is needed because geometry-only candidate generation can produce
  packages that fail Newton body-state, contact, support, or robot-task diagnostics.
- The capped bed/Franka mechanism supports a full-compound body-state sensitivity story for the
  recorded package scope.
- The opt-in package body-state guard supports a diagnostic fallback path, not a calibrated default
  selector.
- The contact-throughput result is a single-scene collision-only performance hook for accepted
  native boxes.
- The Phase 0 diagnostic table can report accept, failure, fallback, and dependency-gap counts
  across the selected assets and candidate lanes.
- The generated-package Franka task smoke can be cited as one recorded generated-package
  consumption smoke, not as robot manipulation or whole-robot collision-quality evidence.

## Required Limitations

- Do not claim broad benchmark superiority over V-HACD, CoACD, CPD-style methods, or convex
  decomposition.
- Do not claim all V-HACD lanes pass. The recorded bowl/cup/tray failures are intentionally
  preserved as diagnostic outcomes.
- Do not claim full-simulation speedup from the collision-only throughput hook.
- Do not claim broad cylinder stability, calibrated COM/inertia repair, or calibrated selector
  thresholds.
- Do not claim whole-robot Franka performance, manipulation validity, deployment readiness,
  real-world transfer, safety certification, or formal verification.

## Frozen Paper-Facing Artifacts

- `paper/shared/evidence/claims.yaml`
- `paper/shared/evidence/results_manifest.yaml`
- `paper/shared/sections/experiments.tex`
- `paper/shared/sections/discussion.tex`
- `docs/deepdive/evidence-status.md`
- `docs/reference/claim-boundaries.md`

Future evidence can extend this packet, but stronger claims require new dated records and updated
claim boundaries.
