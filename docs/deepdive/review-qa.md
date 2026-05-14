# DeepDive Review Q&A

Canonical message source: [message-map.md](message-map.md).

## Taste

**Question: Why is this a good problem rather than just asset tooling?**

Collision proxies are a low-level physical contract. For physical intelligence, model outputs must be checked against physical constraints, and a physics engine is the executable diagnostic layer. If the collision proxy is wrong, the diagnostic layer can produce misleading task results. The project is infrastructure for making that contract editable, measurable, and fallback-aware.

**Question: Why primitive-first?**

Primitives are editable, interpretable, cheap to simulate in many cases, and often sufficient for non-precision tasks. The tasteful claim is not primitive-only. It is primitive-first with explicit fallback when primitives are the wrong representation.

**Question: Why not start with LLM/VLM?**

The first milestone should establish a non-LLM baseline. Without that baseline, LLM/VLM results would be hard to interpret. LLM/VLM may later help with semantic part planning, budget selection, or repair critique, but not direct untrusted floating-point geometry output.

## Benchmark

**Question: What will you compare against?**

For the first 0-4 weeks, compare against 2-3 baselines: bounding box or sphere, single convex hull, and CoACD or V-HACD when available. The later candidate matrix includes CPD-like primitive decomposition when available, manual primitive colliders where available, SDF/hydroelastic reference comparison where task-valid, original triangle mesh where valid, VisACD when available, and Newton-native `approximate_meshes()` modes.

**Question: What metrics matter?**

The required 0-4 week metrics are primitive or hull count, fallback ratio, generation failure rate, step time, contact count, and one penetration or jitter signal. Later metrics can add narrowphase time, broadphase pair count, contact normal error, task success, fallback surface ratio, and human edit time when instrumentation exists.

**Question: How do you avoid benchmark overclaiming?**

Report paired asset-level comparisons, confidence intervals or effect sizes where enough samples exist, seeds/config snapshots, Newton version, hardware, solver settings, asset hashes, baseline parameters, and artifact paths. Avoid benchmark superiority claims until enough evidence exists.

## User Experience

**Question: Who is the user?**

Initial users are internal robotics simulation, asset import, RL, and digital-twin workflows that need collision assets that are faster to inspect, edit, and reject than opaque hull soups.

**Question: What should the output look like?**

The output should be a collision package plus report: primitives, task labels, source regions, confidence, fallback regions, failure reasons, metrics, config hashes, and provenance.

**Question: What is the experience when the compiler fails?**

Failure should be explicit. The system should say which task failed, which region fell back, why fallback was chosen, and which representation is recommended. Silent primitive-only output is not acceptable.

## Value Delivering

**Question: What value can be delivered in four weeks?**

The 0-4 week milestone can deliver evidence: a non-LLM primitive baseline, a Newton diagnostic checker harness, baseline comparisons on a small asset set, and clear failure/fallback reports. That is enough to decide whether the project deserves broader support.

**Question: What is the strategic value if it works?**

It gives Physical Intelligence Center a reusable diagnostic component for AI-generated or imported physical assets. The value is not only runtime speed; it is traceability, editability, failure visibility, and safer interpretation of simulation checks.

**Question: What if primitives do not beat convex decomposition?**

That is still useful if the checker and fallback report reveal when primitives are inappropriate. If the non-LLM baseline shows no measurable benefit and fallback dominates, the project should narrow or stop before LLM/VLM work.

## Likely Hard Questions

**Is this a safety project?**

It is safety-relevant infrastructure, not a safety guarantee. It can help expose candidate collision-proxy failures under specified simulator assumptions, but it does not certify real-world safety.

**Are you replacing convex decomposition?**

No. The nuanced claim is primitive-first and fallback-aware. Convex decomposition remains an important fallback and baseline.

**Why Newton specifically?**

Newton is the target execution layer for the first diagnostic checker. The project uses Newton tasks, metrics, solver settings, and native approximation modes to make collision proxy quality observable.

**Is the Newton environment ready now?**

Not yet. The repository now has an environment-readiness checker that records Python provenance,
Newton source state, module imports, GPU visibility, and output writability. The current local
status is `dependency_gap`, which is useful setup evidence but not Newton simulation evidence.

**What would make you stop?**

Stop or narrow if primitive count exceeds CoACD hull count without runtime/task benefit, fallback dominates, the Newton checker is unstable, precision tasks are incorrectly accepted as primitive-only, or LLM/VLM adds no measurable value after the baseline.

## Strategic Story, Milestone, And Non-Goals

Strategic story: physics engines are executable diagnostic layers for AI model physical safety constraints, and collision proxies are one of their critical inputs.

Narrow first milestone: clean Newton environment readiness, non-LLM primitive baseline, and Newton
diagnostic checker.

Current non-goals: safety guarantee, real-world transfer, deployment readiness, benchmark superiority, complete replacement of convex decomposition, and LLM/VLM claims before baseline evidence.
