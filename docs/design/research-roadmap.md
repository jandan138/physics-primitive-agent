# Research Roadmap

## Phase 0: Bootstrap And DeepDive Proof Point (0-4 Weeks)

Goal: make the project measurable before claiming research progress.

- Finalize DeepDive claim boundaries and support request.
- Normalize the Newton runtime environment and record readiness from the selected Python
  executable.
- Prepare 5-10 provenance-clear assets.
- Reproduce 2-3 simple baselines: bounding box or sphere, single convex hull, and CoACD or V-HACD when available.
- Build 2-3 Newton probes: drop, stack or slide, and sphere-rain/contact stress.
- Produce the first evidence report format.

## Phase 1: Non-LLM Primitive Baseline Expansion (4-8 Weeks)

Goal: test whether primitive-first compilation has value without LLM/VLM.

- Generate primitive proposals using geometry and task heuristics.
- Expand toward about 20-50 assets across task templates.
- Compare runtime, contact behavior, failure rate, primitive count, and fallback ratio against baselines.
- Decide whether primitive-first behavior is useful enough to continue.

## Phase 2: Checker-Guided Repair And Fallback (8-12 Weeks)

Goal: convert raw baseline failures into actionable repair and fallback decisions.

- Add split, merge, expand, shrink, and reject operations.
- Add local fallback region metadata.
- Improve failure taxonomy and report quality.
- Validate that fallback decisions are stable and not hiding failures.

## Phase 3: LLM/VLM Planning Only After Baseline Value (12-18 Weeks)

Goal: test whether model-based semantic planning, budget selection, or repair critique improves over the non-LLM baseline.

- Introduce LLM/VLM only after Phase 1 evidence supports the need.
- Avoid direct floating-point primitive regression as the main model role.
- Run ablations against the non-LLM baseline and repair system.
- Stop model work if it does not provide measurable gain.

## Phase 4: Integration, Productization, And External Evidence (18-24 Weeks)

Goal: turn evidence into a usable internal tool if earlier phases justify it.

- Integrate with asset import and Newton workflows.
- Add provenance, regression tests, and artifact registry.
- Conduct broader internal user evaluation.
- Consider paper, SDK, or demo only after measured evidence exists.

## Strategic Story

The roadmap supports AI model physical safety constraints by improving one executable diagnostic input: collision geometry for physics-engine checks.

## Narrow First Milestone

The immediate milestone is Phase 0 into Phase 1: clean Newton environment readiness, non-LLM
primitive baseline, and Newton diagnostic checker.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, benchmark superiority, primitive-only sufficiency, or complete replacement of convex decomposition.
