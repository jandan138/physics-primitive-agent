# 2026-05-14 Newton Contact Smoke

## Date

2026-05-14

## Status

Complete for the first contact-only Newton canary.

## Changes

- Added a common `CollisionPackage` adapter for CPD-like geometry reports.
- Added Newton-independent shape mapping for `box`, `sphere`, and `capsule`.
- Added `newton_contact_smoke`, a contact-only Newton canary that runs one representative
  overlapping probe sphere per emitted primitive type.
- Hardened the contact smoke after review: the CLI preserves JSON-only stdout, Newton runtime
  imports are checked against the configured source checkout, invalid non-finite shape descriptors
  or left-handed axes are rejected before runtime, mapping-gap reports remain JSON-safe, and the
  report records representative-only canary scope metrics.
- Added CLI support:

```bash
npc-compile --config configs/experiments/cpd_like_baseline.yaml --run-newton-contact-smoke
```

## Verification

- `python -m pytest -q`: exit 0, 91 passed.
- `python scripts/validate_docs.py`: exit 0.
- `git diff --check`: exit 0.
- Clean-env contact smoke:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src \
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/cpd_like_baseline.yaml \
  --run-newton-contact-smoke
```

Observed clean-env result:

- stage: `newton_contact_smoke`
- status: `smoke_passed`
- device: `cpu`
- asset ID: `grscenes_bed_0a85b986_smoke`
- package ID: `grscenes_bed_0a85b986_smoke:cpd_like_face_merge`
- Newton source commit: `96713fa965463b69c229a4d30582c733ff3526bb`
- primitive count: `32`
- type counts: `box: 32`
- shape status counts: `mapped: 32`
- representative contact canaries: one `box` canary
- representative box contact count: `1`
- contact canary scope metric: `one_representative_per_mapped_type`
- full package contact coverage metric: `false`
- stdout behavior: one JSON line on stdout; Warp initialization and kernel logs on stderr

## Artifacts

- Config: `configs/experiments/cpd_like_baseline.yaml`
- Smoke asset manifest: `assets/manifests/cpd_like_smoke_assets.yaml`
- Generated report target: `reports/generated/cpd_like_baseline/` (ignored)
- Raw USD assets: not committed.

## Claim Impact

Supported:

- CPD-like primitive proposals can be converted into a common collision package.
- Restricted `box`/`sphere`/`capsule` package primitives can be mapped into Newton-facing shape
  descriptors.
- For the capped bed smoke, the CPD-like output produced 32 Newton-mappable box primitives, and
  one representative box contact canary produced contact output in Newton.

Not supported:

- task-level Newton simulation checker results;
- drop, stack, slide, or sphere-rain probe evidence;
- collision quality, benchmark, or fallback superiority claims;
- full CPD paper reproduction;
- generated collision package deployment readiness;
- safety certification or real-world transfer claims.

## Next Action

Expand from contact-only canary evidence to the first task-level Newton probe, preferably a small
drop/settle probe with explicit solver settings, timestep, seed, and metrics.
