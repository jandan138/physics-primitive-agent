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
- CPD paper-lane offline gates as package-ready or general real PrimitiveSpec generation,
  CollisionPackage generation, Newton runtime support, benchmark evidence, collision-quality
  evidence, deployment readiness, or safety certification. The only current runtime PrimitiveSpec
  exception is the single synthetic `paper_single_box` runtime-construction contract, which stores
  only `PrimitiveSpec.to_dict()` in the report and remains outside package/Newton/evaluation
  claims.
- CPD PrimitiveSpec candidate-source audits as evidence that current native PrimitiveSpec
  candidates exist; the candidate-source audit records zero eligible current candidates, and the
  native-current fixture contract records only one synthetic `paper_single_box` OBB/box source row
  for a later report-only generation gate. The native-fixture generation contract emits one
  serialized offline PrimitiveSpec-like dict for review, not a runtime `PrimitiveSpec` object,
  package, Newton run, benchmark, or collision-quality result. The native-fixture serialization
  contract validates strict canonical JSON and round-trip equality for that one report-only dict;
  it still creates no runtime `PrimitiveSpec`, no `CollisionPackage`, and no Newton evidence. The
  runtime-boundary preflight contract records one later runtime-construction candidate for that row,
  but still allows no runtime construction in the current gate and creates no runtime
  `PrimitiveSpec`, no `CollisionPackage`, and no Newton evidence. The runtime-construction
  contract now constructs exactly one runtime `PrimitiveSpec` object from the canonical synthetic
  `paper_single_box` OBB/box preflight JSON after checking the runtime-boundary preflight row's
  canonical JSON SHA-256 fingerprint and stores only `PrimitiveSpec.to_dict()` in the report; it
  still creates no `CollisionPackage`, no Newton evidence, no real-USD evidence, no benchmark
  evidence, and no collision-quality evidence. The collision-package generation preflight
  contract records one later package-generation candidate from that dict, but keeps actual
  package generation disallowed in the current gate and still creates no `CollisionPackage`, no
  runtime-admissibility evidence, no Newton evidence, no real-USD evidence, no benchmark evidence,
  and no collision-quality evidence. The collision-package generation contract then constructs
  exactly one synthetic, report-scoped `CollisionPackage.to_dict()` artifact for the
  `paper_single_box` OBB/box row and records `generated_collision_package_count: 1`, but still
  creates no runtime-admissibility evidence, no Newton evidence, no real-USD evidence, no
  benchmark evidence, no collision-quality evidence, and no paper primitive vocabulary coverage.
  The runtime-admissibility preflight contract then consumes that one synthetic package artifact,
  records exactly one later runtime-admissibility candidate row without copying the full package
  dict, and still runs no runtime-admissibility check and no Newton code. It is not package
  readiness, not executable runtime-admissibility, not Newton support or execution, not real-USD
  evidence, not benchmark or collision-quality evidence, not full CPD reproduction, not
  `paper_faithful_offline`, and not deployment, safety, or certification evidence. The
  runtime-admissibility contract then records one offline/static finite-geometry and box-schema
  check for that same synthetic package. That check is report-only and does not run Newton shape
  mapping, Newton runtime, real USD, benchmark, or collision-quality tasks. The Newton
  shape-mapping preflight contract then records one offline/static mapper-handoff row for the same
  synthetic box dict, with zero mapping attempts, zero Newton mapping records, and zero Newton
  runtime executions. The Newton shape-mapping contract then records exactly one offline/static
  report-scoped descriptor dict for target kind `box`, still with zero mapping attempts, zero
  Newton mapping records, zero Newton shape objects, and zero Newton runtime executions. The
  Newton shape runtime-boundary preflight contract then records exactly one later
  runtime-construction candidate for that descriptor row while still constructing zero Newton
  shape objects and running zero Newton code. The Newton shape runtime-construction contract then
  records exactly one repo-local `NewtonShapeMapping.to_dict()` mapping record for that descriptor
  row while still creating zero Newton engine shape objects, making zero builder shape calls, and
  running zero Newton code. The Newton shape runtime builder-preflight contract then records
  exactly one JSON-safe future box builder call plan while still making zero builder calls,
  creating zero Newton engine shape objects, and running zero Newton code. The Newton shape
  runtime builder-construction contract then calls only the repo-local static shape dispatch
  helper with a recording builder and fake Warp-like module and records one JSON-safe fake
  `add_shape_box` call artifact while still importing no real Newton runtime, instantiating no
  `newton.ModelBuilder`, creating zero Newton engine shape objects, making zero real Newton
  builder shape calls, and running zero Newton code. It is still not package readiness, not
  Newton readiness, not Newton support or execution, not full CPD reproduction, and not safety
  evidence. The Newton shape runtime engine-builder boundary preflight contract then records one
  offline/static checklist row for the future real `newton.ModelBuilder` / `add_shape_box`
  boundary while still importing no real Newton runtime, instantiating no `newton.ModelBuilder`,
  making zero real Newton builder shape calls, finalizing no model, creating no collision
  pipeline, and running zero Newton code. The bounded environment-probe contract then records
  configured-source-dir status and JSON-safe Newton/Warp `find_spec` provenance shape while the
  default report remains no-config and imports no real Newton or Warp runtime. The bounded
  API-surface contract then records default no-config source-AST API-surface status for the same
  future builder boundary while still importing no Newton/Warp runtime, instantiating no
  `newton.ModelBuilder`, making no real builder shape call, finalizing no model, creating no
  collision pipeline, and running no Newton code. The engine-builder entry contract then records
  a report-only default no-runtime-entry decision for that same synthetic box lineage, with zero
  real Newton/Warp imports, zero `newton.ModelBuilder` instantiations, zero real builder calls,
  zero model finalization, zero collision pipeline calls, and zero Newton runtime executions.
  The report-only engine-builder smoke gate now records
  `smoke_decision: skip_real_runtime_smoke` for the default no-runtime-entry path. The
  report-only engine-builder runtime-execution gate now records
  `runtime_execution_decision: skip_real_runtime_execution` for the default no-runtime-smoke path.
  The report-only runtime-lane review gate now records
  `runtime_lane_review_decision: keep_real_runtime_execution_blocked`, preserves the skipped-runtime
  claim boundary, and keeps runtime compatibility unvalidated. The report-only configured-runtime
  design gate now records the required runtime input design for the same synthetic lineage while
  keeping runtime config validation false and all real runtime counters zero. The report-only
  configured-runtime preflight gate now consumes that design row and records the bounded preflight
  decision while still reading no config, resolving no runtime source/device, importing no
  Newton/Warp runtime, and running no Newton code. The report-only configured-runtime validation
  gate now consumes the preflight row, records the default missing-config validation result while
  reading no config file or environment, resolves no runtime source/device, imports no
  Newton/Warp runtime, and runs no Newton code. The report-only configured-runtime
  source-resolution gate now consumes that validation row, records that `newton.source_dir` is not
  configured, attempts no filesystem probe, resolves no runtime source/device, imports no
  Newton/Warp runtime, and runs no Newton code. The report-only configured-runtime device-resolution
  gate now consumes that source-resolution row, records that `newton_diagnostic.device` is not
  configured, creates no runtime device object, imports no Newton/Warp runtime, and runs no Newton
  code. The report-only configured-runtime entry-decision gate now consumes that device-resolution
  row, records the default no-runtime-entry decision, attempts no runtime entry, imports no
  Newton/Warp runtime, and runs no Newton code. The report-only configured-runtime smoke gate now
  consumes that entry-decision row, records
  `skip_real_runtime_smoke_missing_configured_runtime_entry`, attempts no runtime smoke, imports no
  Newton/Warp runtime, and runs no Newton code. The next runtime-lane gate is
  `paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract`.

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
