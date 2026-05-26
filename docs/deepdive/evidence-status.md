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
- A scoped Phase 0 follow-up run exists for five GRScenes rigid assets plus one Franka USD smoke
  asset. It records bounding-primitive, CPD-style, and CoACD convex-mesh candidate lanes under
  Newton contact, drop/settle, stack-or-slide, and sphere-rain probes; records V-HACD runtime
  evidence for all five selected rigid assets, including V-HACD probe failures on bowl/cup/tray;
  records a Franka link-aware package with 12 link-framed primitives over 12 detected rigid-body
  links, zero cross-link merges, and `/panda/panda_link8` as an explicit meshless placeholder;
  records Franka joint-tree import, short gravity hold, and kinematic trajectory smoke; and
  records a generated-package robot task smoke where all 12 generated package primitives are
  attached to Newton bodies and consumed with source USD shapes suppressed.
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
- Current Franka evidence includes capped-package task smokes, one link-aware package generation
  and boundary-audit record, one USD articulation smoke, and one generated-package robot task
  smoke that consumes the link-aware package. It is not whole-robot collider quality or
  manipulation evidence.

## Current Unsupported Claims

- No production collision compiler is complete.
- No broad benchmark-suite result, full-simulation speedup result, or broad benchmark superiority
  claim exists.
- No complete Phase 0 benchmark coverage exists: CoACD, V-HACD, stack-or-slide, a first Franka
  link-aware package, and a first generated-package Franka task smoke are now present in the scoped
  run, but selected V-HACD lanes still have recorded probe failures and the robot evidence covers
  only one Franka smoke asset.
- No calibrated default primitive selector policy exists.
- No validated COM/inertia repair policy exists.
- No broad cylinder stability result exists.
- No whole-robot Franka joint-performance, manipulation, or articulated-dynamics result exists.
- No full CPD paper reproduction exists.
- No collision-quality validation, deployment readiness, real-world transfer, or safety guarantee
  is supported.

## Current Evidence To Highlight

- [Cylinder goal completion audit after contact closure](../records/2026-05-22-cylinder-goal-completion-audit-after-contact-closure.md)
- [Generated-package robot task probe](../records/2026-05-26-generated-package-robot-task-probe.md)
- [Link-aware robot package generation](../records/2026-05-26-link-aware-robot-package-generation.md)
- [Phase 0 V-HACD runtime follow-up](../records/2026-05-26-phase0-vhacd-runtime-followup.md)
- [Phase 0 GRScenes asset intake](../records/2026-05-25-phase0-grscenes-asset-intake.md)
- [Phase 0 stack/CoACD/articulation follow-up](../records/2026-05-25-phase0-stack-coacd-articulation-followup.md)
- [Phase 0 GRScenes rigid benchmark](../records/2026-05-25-phase0-grscenes-rigid-benchmark.md)
- [Package body-state guard task path](../records/2026-05-22-package-body-state-guard-task-path.md)
- [Bed-aligned box primitive contact-throughput microbenchmark](../records/2026-05-22-bed-aligned-box-primitive-contact-throughput.md)
- [Newton-in-the-loop selector story](../reference/newton-in-the-loop-selector-story.md)
- [Simulation-checked primitive collider direction](../reference/simulation-checked-primitive-collider-direction.md)
- [Claim boundaries](../reference/claim-boundaries.md)

## Next Evidence Needed

The next milestone should produce evidence for simulation-checked acceptance rather than more
paper-lane gate accounting:

- V-HACD probe-failure triage for the bowl, cup, and tray lanes, or an explicit decision to keep
  those failures as recorded diagnostic outcomes;
- broader proof that primitive merges do not cross link/joint boundaries across more robot assets;
- broader generated-package robot task checks beyond the single Franka smoke asset;
- Newton articulation smoke on additional robot assets: joint tree import, gravity hold, simple
  joint trajectory, self-collision sanity, and end-effector pose sanity;
- contact-operation smoke for at least one manipulation-like task when runtime setup is
  reproducible;
- paired comparison against simple baselines and CPD/CoACD/V-HACD-style candidates when available;
- explicit fallback/rejection records for packages that fail body-state, contact, or articulation
  gates.

## Claim Wording Rule

Use "simulation-checked" only when a dated record links a generated package to a named Newton task,
settings, asset, environment, and report. Use "planned", "geometry-only", "contact-only canary",
or "capped task smoke" when those stronger records do not exist.
