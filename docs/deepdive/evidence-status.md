# Evidence Status

This file separates current evidence from future claims. See [message-map.md](message-map.md) for
canonical DeepDive wording.

## Current Supported Claims

- The repository is a DeepDive-first bootstrap for a Newton Primitive Collision Compiler proposal.
- The current research direction is simulation-checked primitive collider generation, not a claim
  that automatic primitive collider generation itself is novel.
- CPD-style decomposition, CoACD, V-HACD, authored colliders, SDF, hydroelastic, convex meshes, and
  triangle meshes where valid are candidate generators, baselines, or fallbacks.
- The current executable surface includes config dry-runs, USD asset-open diagnostics, ignored
  repo-local USD mirror materialization for the current bed/Franka assets and Phase 0 GRScenes
  rigid-asset intake, Newton source and environment-readiness diagnostics, CPD-like geometry smoke
  paths, Newton contact canaries, and named Newton task smokes.
- Phase 0 now has five selected GRScenes rigid assets materialized into ignored repo-local mirrors
  with tracked source paths, source/local hashes, and concrete localized USD/MDL/texture dependency
  filenames.
- A scoped Phase 0 rigid diagnostic run exists for those five GRScenes assets. It records
  bounding-primitive and CPD-style first-mesh candidate lanes under Newton contact, drop/settle,
  and sphere-rain probes, including two CPD-style drop/settle `not_settled` failures and explicit
  fallback/dependency-gap labels for convex hull, CoACD/V-HACD, stack-or-slide, and precision
  review.
- The repository has dated records for capped bed/Franka native probe paths and opt-in selected
  cylinder packages.
- The capped bed/Franka cylinder mechanism question is complete for the recorded scope: the bed
  `not_settled` label is a full-compound package effect involving a large flat cylinder and
  COM/inertia body-state sensitivity; the recorded Franka cylinder packages are much smaller and
  pass under their capped package context.
- An explicitly opt-in package body-state guard task path has been recorded: it falls back only the
  flagged capped bed package while keeping the unflagged capped Franka cylinder package in the
  recorded Newton task smoke.
- A preliminary bed-aligned, collision-only contact-throughput microbenchmark has been recorded:
  native Newton boxes achieved 2.21x generated-contact throughput versus same-count convex64 mesh
  proxies in one pressure scene, with about 5.3% collision-only wall-time reduction.
- Current Franka evidence is capped-package and task-smoke evidence. It is not whole-robot
  articulated-dynamics evidence.

## Current Unsupported Claims

- No production collision compiler is complete.
- No broad benchmark-suite result, full-simulation speedup result, or broad benchmark superiority
  claim exists.
- No complete Phase 0 benchmark coverage exists: CoACD/V-HACD executable baselines, dedicated
  stack-or-slide execution, and articulated robot smoke remain open.
- No calibrated default primitive selector policy exists.
- No validated COM/inertia repair policy exists.
- No broad cylinder stability result exists.
- No whole-robot Franka joint-performance, manipulation, or articulated-dynamics result exists.
- No full CPD paper reproduction exists.
- No collision-quality validation, deployment readiness, real-world transfer, or safety guarantee
  is supported.

## Current Evidence To Highlight

- [Cylinder goal completion audit after contact closure](../records/2026-05-22-cylinder-goal-completion-audit-after-contact-closure.md)
- [Phase 0 GRScenes asset intake](../records/2026-05-25-phase0-grscenes-asset-intake.md)
- [Phase 0 GRScenes rigid benchmark](../records/2026-05-25-phase0-grscenes-rigid-benchmark.md)
- [Package body-state guard task path](../records/2026-05-22-package-body-state-guard-task-path.md)
- [Bed-aligned box primitive contact-throughput microbenchmark](../records/2026-05-22-bed-aligned-box-primitive-contact-throughput.md)
- [Newton-in-the-loop selector story](../reference/newton-in-the-loop-selector-story.md)
- [Simulation-checked primitive collider direction](../reference/simulation-checked-primitive-collider-direction.md)
- [Claim boundaries](../reference/claim-boundaries.md)

## Next Evidence Needed

The next milestone should produce evidence for simulation-checked acceptance rather than more
paper-lane gate accounting:

- link-aware primitive package generation for an articulated robot asset;
- Phase 0 follow-up runs with dedicated stack-or-slide execution and CoACD/V-HACD baselines;
- proof that primitive merges do not cross link/joint boundaries;
- Newton articulation smoke: joint tree import, gravity hold, simple joint trajectory,
  self-collision sanity, and end-effector pose sanity;
- contact-operation smoke for at least one manipulation-like task when runtime setup is
  reproducible;
- paired comparison against simple baselines and CPD/CoACD/V-HACD-style candidates when available;
- explicit fallback/rejection records for packages that fail body-state, contact, or articulation
  gates.

## Claim Wording Rule

Use "simulation-checked" only when a dated record links a generated package to a named Newton task,
settings, asset, environment, and report. Use "planned", "geometry-only", "contact-only canary",
or "capped task smoke" when those stronger records do not exist.
