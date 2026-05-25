# DeepDive Review Q&A

Canonical message source: [message-map.md](message-map.md).

## Taste

**Question: Why is this more than asset tooling?**

Collision packages decide what a simulator believes can touch, move, pass, or support weight. For
physical intelligence, that makes them part of the executable diagnostic path, not just an export
format. The project makes those packages measurable, rejectable, and fallback-aware.

**Question: Why primitive colliders?**

Primitives are editable, interpretable, and often cheap in physics engines. The claim is not
primitive-only. The claim is candidate primitives plus Newton diagnostics and fallback.

**Question: Do you have early performance evidence?**

Yes, with a narrow boundary. In one bed-aligned collision-only pressure test, Newton-native box
primitives achieved 2.21x higher generated-contact throughput than same-count 64-vertex
convex-mesh proxies: 19.8k versus 9.0k generated contacts per second. The end-to-end
collision-only wall time improved by about 5.3%, so this should be presented as contact-throughput
evidence, not full simulation speedup.

**Question: How is this different from CPD 2026?**

CPD-style work generates compact primitive collider packages and evaluates geometry/simulation
performance. This project treats those packages as candidates and adds acceptance gates after they
enter Newton: body-state checks, contact behavior, articulation integrity, and task operation.

**Question: Why not start with LLM/VLM?**

The first milestone should establish a deterministic checker loop. Without that baseline, LLM/VLM
results would be hard to interpret. Future model roles should be semantic planning, task-aware
budgeting, or repair critique, not direct untrusted floating-point geometry output.

## Benchmark

**Question: What will you compare against?**

Phase 0 should compare simple bounding primitives, single convex hulls, and CoACD/V-HACD or
CPD-style candidates when available. Later comparisons can add authored colliders, VisACD, SDF,
hydroelastic, triangle mesh where valid, and Newton-native approximation modes.

**Question: What metrics matter?**

Rigid assets need primitive/hull count, fallback ratio, generation failure rate, step time,
contact count, penetration or jitter, and final-speed/body-state labels. Robot assets also need
link-boundary preservation, joint tree import status, gravity-hold drift, trajectory completion,
self-collision sanity, and end-effector pose error.

**Question: How do you avoid benchmark overclaiming?**

Use paired asset-level comparisons, fixed configs, recorded seeds, Newton version, hardware, solver
settings, asset hashes, baseline parameters, and artifact paths. The current 2.21x bed-aligned
result is a preliminary single-scene contact-throughput hook; do not claim broad benchmark
superiority before sample size and task coverage justify it.

## Robot Operation

**Question: Will primitive merging affect Franka joints?**

It can if done incorrectly. Primitive merging must be constrained by the robot link/joint graph.
Merging within one rigid link can be acceptable if body state and contact behavior pass diagnostics.
Merging across joint boundaries is invalid for articulated simulation because it collapses bodies
that must move relative to each other.

**Question: Does current Franka evidence prove whole-robot behavior?**

No. Current Franka evidence is capped-package and task-smoke evidence. It does not prove full
articulated Franka joint performance. The first link-aware package record is generation and
boundary accounting only; generated-package robot task probes are still required.

**Question: What would make the robot claim credible?**

A dated record should show generated link-aware packages exercised under named Newton robot task
settings: no cross-link merges, preserved joint tree, gravity hold, scripted joint trajectory,
self-collision sanity, end-effector pose sanity, and task/contact behavior.

## Value Delivering

**Question: What value can be delivered in four weeks?**

The proof point can deliver a deterministic compiler/checker loop, a small asset set, one
articulation smoke if reproducible, and clear accept/reject/fallback reports. That is enough to
decide whether the direction deserves broader support.

**Question: What if primitives do not beat convex decomposition?**

That is still useful if the checker reliably identifies when primitives are inappropriate and
routes to fallback. The project value is not only runtime speed; it is traceability, editability,
and failure visibility.

## Likely Hard Questions

**Is this a safety project?**

It is safety-relevant infrastructure; do not claim a safety guarantee. It can expose candidate
collision-proxy failures under specified simulator assumptions, but it does not certify real-world
safety.

**Are you replacing convex decomposition?**

No. Convex decomposition remains a baseline and fallback.

**Why Newton specifically?**

Newton is the target execution layer for the first checker. The project uses named Newton tasks,
metrics, solver settings, and source/environment provenance so collider behavior is observable.

**What would make you stop?**

Stop or narrow if the checker cannot produce stable failure labels, primitive packages frequently
fail without useful fallback reports, robot articulation gates are too brittle to interpret, or
LLM/VLM adds no measurable value after deterministic baselines.

## Non-Goals

No safety guarantee, real-world transfer, deployment readiness, broad benchmark superiority,
full-simulation speedup, full CPD reproduction, complete replacement of convex decomposition, or
whole-robot robot-operation claim before generated link-aware packages are exercised under robot
task probes and broader articulation records exist.
