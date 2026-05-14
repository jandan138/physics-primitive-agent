# Newton Drop/Settle Design

Date: 2026-05-14

Status: Approved by current agent recommendation flow. This design follows the user's instruction
to proceed without stopping for extra approval.

## Goal

Add the first task-level Newton diagnostic after the contact-only canary.

The diagnostic is `newton_drop_settle`: it consumes a `CollisionPackage`, maps every primitive that
must participate in the task to Newton shapes, attaches those primitives to one dynamic rigid body,
drops that body under gravity onto a static ground plane, and reports bounded smoke metrics.

This is the next executable chain:

```text
USD -> CPD-like proposals -> CollisionPackage -> Newton drop/settle probe
```

The probe is still a smoke diagnostic. It is not a collision quality result, benchmark, safety
claim, or CPD paper reproduction.

## Current Inputs

Existing executable input:

- `npc-compile --config configs/experiments/cpd_like_baseline.yaml --run-cpd-like`
- a geometry-only CPD-like report over the capped bed smoke asset;
- `CollisionPackage` adaptation from that report;
- clean Newton Python environment:
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`;
- Newton source checkout:
  `/cpfs/user/zhuzihou/dev/newton`, commit
  `96713fa965463b69c229a4d30582c733ff3526bb`.

A one-off API probe in the clean environment confirmed that Newton CPU XPBD can drop a sphere from
`z=1.0` onto `add_ground_plane()`, ending at `z=0.10000000149` with final contact count `1` and
vertical velocity `0.0`.

## Scope

In scope:

- add a named `newton_drop_settle` runner that takes only `CollisionPackage` as its geometry input;
- require full Newton mapping coverage for task-level smoke success;
- build one dynamic compound body from mapped `box`, `sphere`, and `capsule` primitives;
- use a static Newton ground plane at `z=0`;
- use CPU by default, XPBD by default, deterministic step counts, and explicit solver settings;
- emit JSON with stage, status, asset, package, environment, mapping coverage, task scope, solver
  settings, initial conditions, per-run summaries, summary metrics, failure labels, and claim
  boundary;
- add a dedicated CLI flag for the integrated path;
- add a dedicated config file for the first bed drop/settle smoke.

Out of scope:

- full CPD algorithm reproduction;
- full collision quality validation;
- CoACD, V-HACD, or manual primitive comparison;
- penetration-depth quality scoring if Newton does not expose it in the minimal runner;
- raw trace, USD, video, or generated asset commits;
- deployment, policy-training, real-robot, certification, or safety claims.

## Architecture

Keep dependencies one-way:

- `baselines/cpd_like/package.py` adapts CPD-like geometry reports to `CollisionPackage`;
- `contracts.py` owns Newton-independent package contracts;
- `newton/shapes.py` maps package primitives to Newton-facing descriptors without importing Newton;
- `newton/drop_settle.py` owns the task-level probe and lazily reuses the Newton runtime import
  boundary from `newton/diagnostics.py`;
- `cli.py` is the only layer that calls both CPD-like decomposition and Newton diagnostics.

The CPD-like baseline must not import Newton. The Newton layer must not import CPD-like modules.

## Diagnostic Behavior

For each run:

1. Map the package with `map_package_shapes()`.
2. If any primitive is not mapped, return `mapping_gap` and do not claim task-level execution.
3. Import Newton and Warp from the configured `newton.source_dir`.
4. Estimate an asset-frame support AABB for mapped primitives.
5. Attach all mapped primitives to one dynamic body with local transforms relative to the estimated
   package bottom-center anchor.
6. Place the body so the package bottom starts `height_m` above the static plane.
7. Simulate fixed `frames * substeps` with `SolverXPBD`.
8. Record finite-state status, initial/final body height, final linear velocity and speed,
   estimated support height, maximum contact count, final contact count, contact-observed flag,
   descent flag, and failure labels.

Default smoke settings:

- `device: cpu`
- `solver: xpbd`
- `iterations: 2`
- `frames: 360`
- `frame_dt_seconds: 0.016666666666666666`
- `substeps: 8`
- `height_m: 0.25`
- `gravity_mps2: -9.81`
- `ground_height_m: 0.0`
- `max_floor_breach_m: 0.05`
- `max_settle_linear_speed_mps: 0.05`

## Status Semantics

- `smoke_passed`: all primitives mapped, Newton runtime imported from the configured source, the
  fixed simulation completed, the state stayed finite, the package body descended, at least one
  contact was observed, final contact is still present, final linear speed is under the recorded
  settle threshold, and support height stays within the recorded floor-breach tolerance.
- `mapping_gap`: one or more package primitives could not be mapped into supported Newton primitive
  shapes.
- `dependency_gap`: source or Python dependency readiness prevents the Newton runtime import.
- `runtime_failure`: Newton imports but the probe crashes, produces non-finite state, does not
  descend, observes no contacts, ends with no final contact, ends above the recorded settle speed,
  or breaches the recorded support-height floor tolerance.

The status name `smoke_passed` means the diagnostic executed and returned basic expected signals. It
does not mean the collision proxy is high quality, stable for downstream tasks, safe, or benchmarked.

## Claim Boundary

Default claim boundary:

```text
drop_settle_task_smoke_not_collision_quality_or_safety
```

Supported wording after this slice, if clean-env verification passes:

- "The named `newton_drop_settle` diagnostic completed under the recorded config and environment."
- "The run reports task-level smoke metrics and failure labels for the named asset and package."

Unsupported wording:

- "Collision quality is validated."
- "The package is safe, certified, ready for deployment, or physically verified."
- "The CPD paper has been reproduced."
- "The method beats CoACD, V-HACD, CPD, or manual primitive colliders."

## Verification

Required repository verification:

- `python -m pytest -q`
- `python scripts/validate_docs.py`
- `git diff --check`

Required clean-env smoke:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src \
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/newton_drop_settle.yaml \
  --run-newton-drop-settle
```

The clean-env smoke should return JSON with `stage: newton_drop_settle`. A passing report is evidence
only for this named smoke diagnostic.
