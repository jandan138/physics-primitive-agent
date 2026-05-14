# Newton Contact Smoke Design

Date: 2026-05-14

Status: Approved by current agent recommendation flow. This design follows the user's instruction
to proceed without stopping for extra approval.

## Goal

Add the first Newton-facing diagnostic after the geometry-only CPD-like smoke path.

The diagnostic is `newton_contact_smoke`: a contact-only canary that consumes the existing
CPD-like primitive proposal output, maps supported `box`/`sphere`/`capsule` primitives into
Newton-facing shape descriptors, builds a tiny Newton contact scene for one representative
primitive per emitted type, and reports whether Newton's contact pipeline produced contact output.

This is intentionally narrower than a full drop, stack, or sphere-rain probe.

## Current Inputs

Existing executable input:

- `npc-compile --config configs/experiments/cpd_like_baseline.yaml --run-cpd-like`
- geometry-only CPD-like report with restricted `box`/`sphere`/`capsule` primitive proposals;
- clean Newton Python environment:
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`;
- Newton source checkout:
  `/cpfs/user/zhuzihou/dev/newton`, commit
  `96713fa965463b69c229a4d30582c733ff3526bb`.

The current CPD-like report is not yet a reusable collision package. The CLI currently decorates
the report at the edge. The next slice should add a common package adapter before adding the
Newton diagnostic.

## Scope

In scope:

- convert `CPDLikeDecompositionReport` into a Newton-independent `CollisionPackage`;
- preserve primitive IDs, kind, center, axes, dimensions, source faces, containment flag, and
  volume fields;
- map `box`, `sphere`, and `capsule` packages into Newton-facing shape descriptors;
- report structured mapping gaps for malformed or unsupported primitives;
- run one contact-only Newton canary per emitted primitive type when Newton imports cleanly;
- emit JSON with stage, status, asset, package summary, environment status, type counts, mapping
  gaps, contact canaries, device, Newton source commit, and claim boundary;
- add a CLI flag for the integrated smoke path.

Out of scope:

- full CPD paper reproduction;
- full-asset drop, stack, slide, or sphere-rain probes;
- collision quality or benchmark metrics;
- CoACD/V-HACD comparison;
- generated USD or Newton artifact export;
- deployment, policy-training, real-robot, or safety claims.

## Architecture

Keep dependencies one-way:

- `baselines/cpd_like/package.py` adapts CPD-like geometry reports to `CollisionPackage`;
- `contracts.py` owns common, Newton-independent collision package contracts;
- `newton/shapes.py` maps common package primitives into Newton-facing descriptors without
  importing CPD code;
- `newton/diagnostics.py` imports Newton lazily and runs the contact canary only when available;
- `cli.py` orchestrates config, CPD-like decomposition, package adaptation, and diagnostics.

The CPD-like baseline must not import Newton. The Newton layer must not import CPD-like modules.
Only CLI orchestration may call both sides.

## Diagnostic Behavior

For each representative primitive type:

1. Build a tiny Newton model on the requested device, defaulting to CPU.
2. Add the candidate primitive as a static Newton shape.
3. Add an overlapping probe sphere at the same center.
4. Run `CollisionPipeline(model).collide(state, contacts)`.
5. Record `rigid_contact_count`.

The diagnostic status is:

- `smoke_passed` when Newton imports cleanly, all selected shape mappings pass, and every canary
  produces at least one contact;
- `dependency_gap` when Newton or Warp cannot import;
- `mapping_gap` when no supported Newton-mappable primitive is available;
- `runtime_failure` when Newton imports but the canary crashes or produces no contact.

## Claim Boundary

Supported wording after this slice, if clean-env verification passes:

- "CPD-like primitive proposals can be ingested by Newton for a contact-only canary."
- "Newton contact smoke exists for named primitive types, asset, device, and environment."

Unsupported wording:

- "Newton simulation checker quality results exist."
- "The generated collision package is simulation-checked for a task."
- "The CPD paper has been reproduced."
- "Collision quality, benchmark superiority, deployment readiness, or safety have been shown."

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
  --config configs/experiments/cpd_like_baseline.yaml \
  --run-newton-contact-smoke
```

The clean-env smoke should return JSON with `stage: newton_contact_smoke`. A passing report is
evidence only for the contact canary, not for collision package quality.
