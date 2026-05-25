# Research Roadmap

## Phase 0: Simulation-Checked DeepDive Proof Point (0-4 Weeks)

Goal: show that physics-engine diagnostics can accept, reject, or fall back primitive collider
packages in ways that geometry-only generation would miss.

- Finalize DeepDive claim boundaries and support request.
- Maintain clean Newton environment provenance for every runtime claim.
- Use the materialized Phase 0 GRScenes rigid-asset manifest as the first asset set.
- Include one articulated robot smoke asset if licensing and runtime setup are reproducible.
- Generate primitive candidates from deterministic heuristics, native lanes, or CPD-style outputs.
- Compare against simple baselines: bounding primitive, single convex hull, and CoACD/V-HACD or
  CPD-style candidates when available.
- Build Newton probes: body-state/drop-settle, contact stress, and at least one operation-style
  smoke when feasible.
- For robot assets, enforce link-aware package boundaries and run articulation smoke gates.
- Produce the first accept/reject/fallback evidence report.

## Phase 1: Asset And Robot-Gate Expansion (4-8 Weeks)

Goal: test whether the checker loop generalizes beyond the initial proof point.

- Expand toward about 20-50 assets across rigid props, handles, containers, and robot packages.
- Add multiple robot assets only if the first articulation gate is reproducible.
- Compare runtime, contact behavior, failure labels, primitive count, body-state deltas, and
  fallback ratio against baselines.
- Decide whether simulation-checked primitive packages are useful enough to continue.

## Phase 2: Checker-Guided Repair And Fallback (8-12 Weeks)

Goal: turn diagnostic failures into reliable repair or fallback decisions.

- Add split, merge, expand, shrink, reject, and local fallback operations.
- Add per-region fallback metadata.
- Stabilize failure taxonomy and report quality.
- Validate that fallback decisions are not hiding unsupported geometry or robot-operation failures.

## Phase 3: Optional LLM/VLM Planning After Baseline Value (12-18 Weeks)

Goal: test whether model-based semantic planning or repair critique improves over deterministic
candidate generation and checker-guided repair.

- Introduce LLM/VLM only after Phase 1 evidence supports the need.
- Avoid direct floating-point primitive regression as the main model role.
- Run ablations against the deterministic baseline and repair system.
- Stop model work if it does not provide measurable gain.

## Phase 4: Integration And External Evidence (18-24 Weeks)

Goal: turn evidence into a usable internal tool if earlier phases justify it.

- Integrate with asset import and Newton workflows.
- Add provenance, regression tests, artifact registry, and review gates.
- Conduct broader internal user evaluation.
- Consider a paper, SDK, or demo only after measured evidence exists.

## Strategic Story

The roadmap supports AI model physical-constraint diagnostics by making collision packages
simulation-checked artifacts rather than geometry-only outputs.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, broad benchmark superiority,
full-simulation speedup, primitive-only sufficiency, full CPD reproduction, or complete replacement
of convex decomposition.
