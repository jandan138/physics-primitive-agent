# DeepDive Message Map

This is the canonical source for DeepDive-facing wording. Other files should preserve these claims and boundaries.

## Leadership Narrative

Physical Intelligence Center needs AI systems that respect physical safety constraints, not only systems that generate plausible assets, actions, or robot plans. A physics engine is the executable diagnostic layer for those constraints: under named simulator assumptions, tasks, metrics, and versions, it can expose candidate penetrations, unstable contacts, unsafe force-transfer patterns, false clearance assumptions, and task-level physical failures.

Collision geometry is one of the hidden contracts behind that diagnostic layer. A render mesh can look correct while its collision proxy is physically misleading. Under-conservative proxies can let a model appear to pass through objects; over-conservative proxies can reject feasible grasps, navigation paths, or stacking behaviors. A collision compiler that produces editable proxies, checks them in Newton, and falls back when primitives are not enough is a concrete piece of physical-intelligence infrastructure.

## Technical Thesis

Build a primitive-first, Newton-diagnostic-checked, fallback-aware collision asset compiler for Newton. The compiler should prefer editable primitive compounds when they are sufficient for the task, use Newton checks to catch behavioral failures, and fall back locally to CoACD, SDF, hydroelastic, convex mesh, or manual review when primitive proxies are not adequate.

The thesis is not that primitives replace convex decomposition. The thesis is that primitives should be attempted first when the task and asset permit it, while the system preserves a measured fallback path.

## Safe One-Liner

Newton Primitive Collision Compiler is a proposal for primitive-first, Newton-diagnostic-checked, fallback-aware collision asset compilation: generate editable primitive proxies, check task behavior in Newton, and fall back when primitives are not enough.

## Unsafe Claims

Do not claim:

- Do not claim a physical safety guarantee;
- Do not claim a real-world transfer guarantee;
- deployment readiness;
- benchmark superiority;
- complete replacement of convex decomposition;
- primitive-only sufficiency for all assets or precision tasks;
- LLM/VLM benefit before the non-LLM baseline is measured;
- task-level Newton checker results before the checker exists and has run;
- simulator checks as proof of collision correctness outside named assumptions.
- CPD paper-lane offline gates as real PrimitiveSpec generation, CollisionPackage generation,
  Newton runtime support, benchmark evidence, collision-quality evidence, deployment readiness, or
  safety certification.
- CPD PrimitiveSpec candidate-source audits as evidence that current native PrimitiveSpec
  candidates exist; the current candidate-source audit records zero eligible current candidates
  until a separate native current-fixture gate is implemented.

## First 4-Week Proof Point

The 0-4 week proof point is deliberately narrow:

- implement a non-LLM primitive baseline for 5-10 simple, provenance-clear assets;
- build 2-3 Newton probes first: drop, stack or slide, and sphere-rain/contact stress;
- compare against 2-3 baselines first: bounding box or sphere, single convex hull, and CoACD or V-HACD when available;
- report a minimal metric set: primitive count, fallback ratio, step time, contact count, penetration or jitter, and generation failure rate;
- produce failure examples and fallback reasons instead of hiding them.

The full benchmark matrix belongs to later phases after this proof point shows the path is measurable.

LLM/VLM planning, repair, or semantic decomposition is deferred until the non-LLM baseline demonstrates value.

## Ask And Support Request

Requested DeepDive support:

- technical review from Newton, robotics simulation, geometry processing, and physical-intelligence safety reviewers;
- access to representative internal assets with clear license/provenance boundaries;
- guidance on Newton checker scenarios, solver settings, and metric thresholds;
- a small compute and engineering allocation for the 0-4 week proof point;
- help identifying downstream users in robotics, asset import, RL, and digital-twin workflows.

The ask is for milestone-based exploration. If the non-LLM baseline cannot show measurable value, the project should stop or narrow before adding LLM/VLM complexity.

## Strategic Story, Milestone, And Non-Goals

Strategic story: physics engines are executable diagnostic layers for AI model physical safety constraints, and collision proxies are a low-level contract that must be checked.

Narrow first milestone: non-LLM primitive baseline plus Newton diagnostic checker in 0-4 weeks.

Current non-goals: safety guarantee, real-world transfer, deployment readiness, benchmark superiority, and complete replacement of convex decomposition.
