# Evaluation Plan

The evaluation plan defines what evidence must exist before the project makes stronger claims. It supports the DeepDive first milestone: non-LLM primitive baseline plus Newton checker/verifier.

Physics engines are treated here as executable diagnostics for AI model physical safety constraints. The metrics below are not safety guarantees; they are scoped observations of candidate collision-proxy failures under named Newton assumptions, tasks, and versions.

## Baseline

Compare against:

- bounding box;
- bounding sphere;
- single convex hull;
- V-HACD;
- CoACD;
- CPD-like primitive decomposition when available;
- VisACD when available;
- manual primitive colliders when available;
- SDF or hydroelastic oracle where appropriate;
- original triangle mesh where valid for the simulator/task;
- Newton-native `approximate_meshes()` modes.

Baselines must record parameters, versions, asset hashes, and artifact paths.

## Task

Task templates:

- drop;
- stack;
- slide;
- sphere rain;
- roll;
- grasp proxy;
- container;
- hole traversal;
- explicit precision-task rejection.

Precision insertion, thin walls, threads, gears, and similar assets must not be accepted as primitive-only unless metrics justify that decision under the named task.

## Metric

Report:

- step time;
- narrowphase time;
- broadphase pair count;
- contact count p95;
- penetration;
- jitter;
- contact normal error;
- task success;
- primitive or hull count;
- fallback surface ratio;
- generation failure rate;
- human edit time.

Metrics should be paired at asset level so differences are attributable to the collision representation rather than asset mix.

## Reporting

Reports must include:

- paired asset-level comparisons;
- confidence intervals or effect sizes where enough samples exist;
- seeds and config snapshots;
- Newton version;
- hardware;
- solver settings;
- asset hashes;
- source/license metadata;
- baseline parameters;
- artifact paths;
- failure examples and fallback reasons.

Do not report benchmark superiority until the sample size, task coverage, and statistical treatment justify it.

## Phase Gate

DeepDive proof point, 0-4 weeks: run 5-10 provenance-clear assets, 2-3 Newton probes, and 2-3 baselines to confirm the project is measurable and failure modes are reportable.

Phase 1 gate, 4-8 weeks: expand toward about 20-50 assets and the broader baseline matrix, including VisACD when available, manual primitives when available, and Newton-native approximation modes.

Phase 2 gate, 8-12 weeks: add checker-guided repair and measure whether repair/fallback improves failures without hiding unsupported regions.

Phase 3/4 gate, 12-24 weeks: add LLM/VLM only after non-LLM value is demonstrated; require ablation evidence that model semantics improve planning, budget selection, or repair, then decide whether productization or paper work is justified.

## No-Go Criteria

Stop, narrow, or pivot if:

- LLM/VLM shows no measurable gain over the non-LLM baseline;
- primitive count exceeds CoACD hull count without runtime or task benefit;
- fallback dominates the output;
- Newton checker is unstable or too sensitive to solver settings for the intended decision;
- precision tasks are incorrectly accepted as primitive-only;
- reports cannot preserve asset provenance, settings, and failure reasons.

## Strategic Story

This evaluation plan supports a physical-intelligence diagnostic layer. It checks collision proxies in simulation under named assumptions; it does not guarantee physical safety or real-world transfer.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, benchmark superiority, primitive-only sufficiency, or complete replacement of convex decomposition.
