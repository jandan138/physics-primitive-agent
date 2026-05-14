# 2026-05-14 Newton Drop/Settle

## Date

2026-05-14

## Status

Complete for the first named task-level Newton smoke diagnostic.

## Changes

- Added `newton_drop_settle`, a task-level Newton diagnostic that consumes a `CollisionPackage`,
  maps all included primitives to supported Newton shapes, attaches them to one dynamic compound
  rigid body, drops that body onto a static plane, and records bounded smoke metrics.
- Added `--run-newton-drop-settle` and `configs/experiments/newton_drop_settle.yaml` for the
  integrated CPD-like bed smoke path.
- Added drop/settle report schema fields for task scope, solver settings, initial conditions, and
  per-run summaries.
- Added support-height tracking so floor-breach decisions are based on the estimated bottom of the
  compound package, not only the rigid-body origin.

## Verification

- `python -m pytest tests/test_cli.py::test_cli_run_newton_drop_settle_keeps_stdout_json_only tests/test_cpd_like_config.py::test_newton_drop_settle_config_owns_probe_parameters -q`:
  exit 0, 2 passed.
- `python -m pytest tests/test_newton_drop_settle.py tests/test_reports_schema.py -q`: exit 0,
  10 passed.
- `python -m pytest -q`: exit 0, 101 passed.
- `python scripts/validate_docs.py`: exit 0.
- `git diff --check`: exit 0.
- Clean-env drop/settle smoke:

```bash
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
PYTHONPATH=src \
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m primitive_collision_compiler.cli \
  --config configs/experiments/newton_drop_settle.yaml \
  --run-newton-drop-settle
```

Observed clean-env result:

- stage: `newton_drop_settle`
- status: `smoke_passed`
- device: `cpu`
- asset ID: `grscenes_bed_0a85b986_drop_settle`
- package ID: `grscenes_bed_0a85b986_drop_settle:cpd_like_face_merge`
- Newton source commit: `96713fa965463b69c229a4d30582c733ff3526bb`
- primitive count: `32`
- shape status counts: `mapped: 32`
- completed steps: `960`
- solver: `xpbd`, `frames: 120`, `substeps: 8`, `iterations: 2`
- initial body height: `0.25`
- final body height: `-0.248321533203125`
- minimum body height: `-1.2665519714355469`
- final support height: `-0.00000394387747348901`
- minimum support height: `-0.0010166456339897323`
- maximum contact count: `8`
- final contact count: `3`
- failure labels: none

The body-origin height is not treated as the floor-breach metric. The estimated support height is
the bounded smoke metric for ground-plane breach, with `max_floor_breach_m: 0.05` recorded in the
config.

## Artifacts

- Config: `configs/experiments/newton_drop_settle.yaml`
- Smoke asset manifest: `assets/manifests/cpd_like_smoke_assets.yaml`
- Generated report target: `reports/generated/newton_drop_settle/` (ignored)
- Implementation commit before this record: `521f5ca`
- Raw USD assets: not committed.

## Claim Impact

Supported:

- The named `newton_drop_settle` diagnostic completed under the recorded config and environment.
- The capped bed CPD-like collision package mapped all 32 restricted primitives into Newton-facing
  shape descriptors for this diagnostic.
- The diagnostic reports bounded task-level smoke metrics and failure labels for this named asset,
  package, config, Newton source checkout, and Python environment.

Not supported:

- collision quality validation;
- benchmark superiority or comparison against CoACD, V-HACD, CPD, or manual primitive colliders;
- full CPD paper reproduction;
- safety certification, real-world transfer, or deployment readiness;
- general behavior across arbitrary assets or robot tasks.

## Next Action

Add a second task probe or asset class only after this record is reviewed. The likely next narrow
step is a sphere-rain or stack/slide stress probe that can expose overhang, missing support, or
jitter failure labels without broadening claims.
