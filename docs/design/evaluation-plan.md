# Evaluation Plan

The evaluation plan defines what evidence must exist before the project makes stronger claims. It
supports the DeepDive first milestone: a non-LLM primitive candidate generator plus Newton
diagnostic checker.

Physics engines are treated as executable diagnostics for physical constraints. The metrics below
are scoped observations under named Newton assumptions, tasks, and versions; they are not safety
evidence.

## Phase 0 Baselines

The 0-4 week proof point compares against:

- bounding box or bounding sphere;
- single convex hull;
- CoACD, V-HACD, or CPD-style primitive decomposition when available.

If a baseline is unavailable, record the dependency gap and continue with the required simple
baselines.

## Phase 0 Tasks

Rigid-asset tasks:

- body-state/drop-settle;
- sphere-rain/contact stress;
- stack or slide when setup is reproducible;
- one precision rejection asset if available.

Robot-asset tasks:

- link-boundary audit;
- joint tree import;
- gravity hold;
- simple scripted joint trajectory;
- self-collision sanity;
- end-effector pose sanity;
- one simple contact-operation smoke when runtime setup is reproducible.

## Metrics

| Metric | Operational Definition | Source |
|---|---|---|
| primitive or hull count | number of emitted primitive shapes or baseline hulls per asset | compiler/baseline report |
| fallback ratio | fraction of assets, links, or labeled regions that require non-primitive fallback | compiler report |
| generation failure rate | failed outputs divided by attempted asset-task pairs | compiler report |
| body-state delta | package COM/inertia proxy or recorded Newton body-state difference where available | package/report |
| step time | median simulation step wall time over the recorded probe duration | Newton run log |
| contact throughput | generated contacts per second or microseconds per generated contact in collision-only microbenchmarks | Newton run log |
| contact count | p95 active contact count over the recorded probe duration | Newton run log |
| penetration or jitter | max penetration if available, otherwise rest-state position or velocity jitter | Newton run log |
| final-speed label | pass/fail label for rest-state residual speed under the recorded gate | Newton run log |
| link-boundary status | whether any primitive merge crosses a robot link or joint boundary | compiler report |
| articulation drift | gravity-hold joint drift or base/link pose drift under the recorded gate | Newton run log |
| end-effector pose error | deviation from expected scripted pose after a joint trajectory | Newton run log |

## Phase 0 Implementation Assumptions

- Assets: 5-10 provenance-clear assets selected from simple rigid props, stackable objects,
  handles/contact affordances, containers, one precision negative control if available, and one
  robot smoke asset if reproducible.
- Newton: record exact Newton source/version, Python environment, hardware, solver settings, and
  deviations before reporting results.
- Primitive generator: start with deterministic non-LLM heuristics, native lanes, or imported
  CPD-style outputs.
- Robot policy: forbid cross-link primitive merges; keep joint tree and link frames unchanged.
- Report artifact: one Markdown summary plus JSON/CSV tables linking asset IDs, configs, logs,
  metrics, failure labels, and fallback reasons.

## Reporting

Reports must include:

- paired asset-level comparisons;
- seeds and config snapshots;
- Newton version and environment;
- hardware and solver settings;
- asset hashes and source/license metadata;
- baseline parameters;
- artifact paths;
- failure examples and fallback reasons;
- clear scope labels for capped packages, first-mesh probes, and whole-robot articulation claims.

Single-scene microbenchmarks may be reported as scoped evidence when the metric and boundary are
explicit. Do not report broad benchmark superiority until sample size, task coverage, and
statistical treatment justify it.

## Phase Gates

DeepDive proof point, 0-4 weeks: run a small asset set, named Newton body-state/contact probes, at
least one robot articulation smoke if reproducible, and simple baselines to confirm the project is
measurable and failure modes are reportable.

Phase 1 gate, 4-8 weeks: expand assets and robot tasks, then decide whether simulation-checked
primitive packages provide enough value to continue.

Phase 2 gate, 8-12 weeks: add checker-guided repair and measure whether repair/fallback improves
failures without hiding unsupported regions.

Phase 3/4 gate, 12-24 weeks: add LLM/VLM only after deterministic value is demonstrated.

## No-Go Criteria

Stop, narrow, or pivot if:

- Newton checker labels are unstable or too sensitive to solver settings;
- primitive packages frequently fail without useful fallback reports;
- robot articulation gates fail because the package generator cannot preserve link/joint structure;
- primitive count exceeds baselines without runtime or task benefit;
- precision tasks are incorrectly accepted as primitive-only;
- LLM/VLM shows no measurable gain over deterministic baselines.

## Current Non-Goals

No safety guarantee, real-world transfer, deployment readiness, broad benchmark superiority,
full-simulation speedup, primitive-only sufficiency, full CPD reproduction, or complete replacement
of convex decomposition.
