# CPD-Like Newton Baseline Design

Date: 2026-05-14

## Goal

Define a narrow CPD-like baseline track for Newton diagnostic experiments without changing the
project's claim boundary. The track adapts ideas from *Convex Primitive Decomposition for
Collision Detection* as a measurement baseline, not as this project's algorithmic contribution.

The design converts the current judgment into an implementation-ready boundary:

- CPD-like work is a baseline/reproduction layer.
- Newton probes are an independent measurement layer.
- Reports and records preserve unsupported regions, fallback decisions, and environment settings.
- DeepDive-facing claims remain proposal/bootstrap claims until dated records and reports exist.

## Source Intake

The paper PDF has been downloaded locally under `docs/tmp/papers/`; the source metadata is recorded
in [Temporary paper intake](../../tmp/papers/README.md). This PDF is rough source intake, not
canonical project evidence.

Durable wording must come from:

- [Claim Boundaries](../../reference/claim-boundaries.md)
- [DeepDive Message Map](../../deepdive/message-map.md)
- [Evidence Status](../../deepdive/evidence-status.md)

If this baseline becomes a cited project decision, add a dated record under `docs/records/` and
promote a short literature summary into `docs/reference/`.

## Approved Direction

The accepted direction is:

> Build a Newton-native, CPD-inspired restricted primitive baseline and use it to measure whether
> deterministic primitive collision packages expose useful Newton diagnostic failures.

This is not an attempt to claim full paper reproduction in the first milestone. The paper uses a
broader primitive set, Sketchfab-scale asset evaluation, and its own simulation setup. The first
project milestone should instead produce a small, provenance-clear, paired Newton diagnostic
baseline.

## Alternatives Considered

### Option A: Full CPD Paper Reproduction

This would target the full primitive set, paper-scale assets, geometric distance metrics, and
simulation benchmark parity.

Tradeoff: highest academic fidelity, but too large for the current DeepDive bootstrap and likely
to distract from Newton-specific diagnostic value.

### Option B: CPD-Inspired Newton Subset Baseline

This implements a restricted subset: face/component intake, primitive candidates, bottom-up or
component-level merge logic, Newton export, and paired probes against Newton baselines.

Tradeoff: not a full paper reproduction, but it gives fast evidence about the project-specific
question: whether primitive-first outputs can be checked, rejected, and compared in Newton.

### Option C: Skip CPD-Like Work And Start With Newton Checker Only

This builds probes and reports before any primitive decomposition baseline.

Tradeoff: lower algorithmic scope, but the checker would have too little meaningful candidate
output to evaluate beyond bounding primitives and convex hulls.

Recommended option: Option B.

## Architecture

The baseline should be split into three independent layers.

### 1. Geometry And Baseline Layer

Responsible for reading mesh-level inputs, computing face/component metadata, fitting restricted
primitive candidates, and producing a collision package candidate.

Suggested package boundary:

```text
src/primitive_collision_compiler/
  baselines/
    cpd_like/
      __init__.py
      config.py
      fit.py
      merge.py
      package.py
  geometry/
    mesh.py
    adjacency.py
    primitives.py
```

The baseline layer may use deterministic heuristics and CPD-inspired concepts. It must not call
Newton probes internally. It emits data for later checking.

### 2. Newton Measurement Layer

Responsible for converting a collision package candidate into Newton shapes and running named
diagnostic probes.

Suggested package boundary:

```text
src/primitive_collision_compiler/
  newton/
    export.py
    probes.py
    metrics.py
```

The Newton layer consumes a common collision package spec. It should be equally able to run
CPD-like candidates, bounding primitives, single convex hulls, CoACD/V-HACD outputs, and later
repair/fallback outputs.

### 3. Reporting And Record Layer

Responsible for reproducible evidence, not algorithm execution.

Suggested package and repository boundary:

```text
src/primitive_collision_compiler/
  reports/
    schema.py
    render.py

configs/experiments/
  cpd_like_baseline.yaml

docs/records/
  YYYY-MM-DD-cpd-like-baseline-plan.md
  YYYY-MM-DD-cpd-like-run-001.md

reports/
  cpd_like_baseline/
    README.md
  generated/
    cpd_like_baseline/
```

Committed summaries live under `reports/cpd_like_baseline/`. Large generated tables, logs, and run
artifacts live under `reports/generated/cpd_like_baseline/` and are not committed.

## Data Contracts

The current `PrimitiveSpec` and `CollisionPackage` dataclasses are sufficient for bootstrap dry
runs, but CPD-like evidence needs richer records. The implementation plan should extend contracts
conservatively rather than replacing them wholesale.

Required fields for baseline evidence:

- asset ID, source path, source hash, unit scale, and normalization notes;
- primitive type, pose, dimensions, and source face/component IDs;
- implemented primitive types and requested primitive types;
- unsupported primitive types, such as frustum or trapezoidal prism in the restricted subset;
- containment status for the points or faces assigned to each primitive;
- excess volume or fitting cost where available;
- fallback target and fallback reason;
- generation status and failure label.

This makes fallback a first-class outcome instead of a hidden failure.

## Phase 0 Scope

The first implementation should be a vertical slice, not a full benchmark.

Minimum useful slice:

- 2-3 provenance-clear assets;
- restricted primitive set: box, sphere, capsule, cylinder;
- explicit unsupported list: frustum and trapezoidal prism;
- one Newton probe first, preferably drop or sphere-rain/contact stress;
- one paired report comparing CPD-like, bounding box or sphere, and single convex hull;
- dependency-gap reporting for CoACD/V-HACD if unavailable.

Expanded Phase 0:

- 5-10 provenance-clear assets;
- drop, stack or slide, and sphere-rain/contact stress probes;
- paired comparison against bounding primitive, single convex hull, and CoACD/V-HACD when
  available;
- failure taxonomy, fallback ratio, generation failure rate, primitive/hull count, step time,
  contact count p95, displacement, and penetration or rest jitter.

## Fairness Rules

Every paired comparison must use:

- the same asset version, hash, scale, origin, and mass/inertia assumptions;
- the same Newton version, solver settings, device, fixed timestep, seed, and probe duration;
- the same inclusion of failed, unsupported, and fallback cases;
- recorded dependency gaps for optional baselines;
- asset-level tables before aggregate summaries.

The report must not compare a cleaned mesh for one method against a raw mesh for another method
unless the cleaning step is recorded and applied to every method.

## Claim Boundaries

Allowed wording:

- "CPD-like primitive decomposition baseline adapted for Newton diagnostic probes."
- "Newton-native restricted primitive subset baseline."
- "Simulation-checked under named Newton probes, settings, assets, and records."
- "Dependency gap recorded for unavailable optional baselines."

Avoid:

- Do not say "we reproduced CPD".
- Do not say "our CPD method".
- Do not say "state-of-the-art primitive decomposition".
- Do not say "benchmark superiority".
- Do not say "deployment-ready compiler".
- Do not say "safety guarantee".
- Do not say "simulation-verified collision correctness".

The current design supports a future implementation plan. It does not itself support any result
claim.

## Non-Conflicts With Later Work

This baseline should make later work cleaner if dependencies stay one-way:

- CPD-like baseline emits candidate packages and generation metadata.
- Newton probes consume packages and emit task metrics and failure labels.
- Repair/fallback consumes probe failures and package metadata.
- Task-aware or LLM/VLM components may later propose budgets, priorities, or repairs, but only
  after deterministic baseline evidence exists.

The baseline must not become the only path through the system. Future methods should be compared
through the same package and probe interface.

## Acceptance Criteria For The Spec

This design is ready for implementation planning when the next plan can point to:

- a standalone CPD-like baseline config;
- a common collision package schema;
- a Newton harness that accepts multiple candidate sources;
- a paired report schema with unsupported and fallback fields;
- tests that validate config parsing, report serialization, and claim-safe dry-run behavior.

## Next Step

Write an implementation plan for the minimal vertical slice. The plan should start with contracts,
config loading, and report schema tests before any Newton execution code.
