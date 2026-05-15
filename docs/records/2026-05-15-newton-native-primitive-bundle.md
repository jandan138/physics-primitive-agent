# 2026-05-15 Newton Native Primitive Bundle

## Decision

Runtime primitive expansion stays Newton-native first. This slice adds package mapping and Newton
diagnostic construction for `cylinder`, `cone`, and `ellipsoid`, on top of the already supported
`box`, `sphere`, and `capsule` path.

`capped_cylinder`, `frustum`, and `trapezoidal_prism` remain in the offline paper-alignment lane.
They are not Newton runtime primitives in this repository.

## Implementation

- Added `cylinder`, `cone`, and `ellipsoid` to the Newton shape mapping contract.
- Added dimension validation:
  - `cylinder`: positive finite `radius`, non-negative finite `half_height`, optional
    `axis_index` in `{0, 1, 2}`;
  - `cone`: positive finite `radius`, non-negative finite `half_height`, optional `axis_index`
    in `{0, 1, 2}`;
  - `ellipsoid`: three positive finite `radii`.
- Added Newton builder dispatch for the new native kinds in:
  - contact canary static shapes;
  - drop/settle dynamic compound shapes;
  - sphere-rain static package shapes.
- Added conservative package bounds and support-height estimates for drop/settle and sphere-rain
  setup.
- Hardened validation so `axis_index` and positive integer solver/count options reject booleans
  and non-integral floats instead of silently casting them.
- Kept `capped_cylinder` as a mapping gap.

## Clean-Env Runtime Smoke

Local clean environment:

- Python: `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python`
- Newton source: `/cpfs/user/zhuzihou/dev/newton`
- Device: `cpu`
- Import path: command was run from this branch worktree with `PYTHONPATH=src`, so the external
  Python imported the reviewed worktree package instead of an installed checkout from another
  path.
- Package: synthetic six-primitive native bundle containing `box`, `sphere`, `capsule`,
  `cylinder`, `cone`, and `ellipsoid`

Observed result:

- `newton_contact_smoke`: `smoke_passed`
  - representative canaries passed for all six kinds;
  - contact count was `1` for each representative kind.
- `newton_drop_settle`: `smoke_passed`
  - options: `frames=120`, `substeps=4`;
  - completed steps: `480`;
  - max contact count: `10`;
  - final contact count: `7`;
  - final linear speed stayed below `0.01 m/s` in review reruns;
  - final support height was about `-0.006m` to `-0.008m`, within the configured `0.05m`
    floor-breach tolerance;
  - failure labels: none.
- `newton_sphere_rain`: `smoke_passed`
  - options: `sphere_count_x=2`, `sphere_count_y=2`, `frames=120`, `substeps=4`;
  - completed steps: `480`;
  - max contact count: `4`;
  - max contacted probe count: `4`;
  - contact density proxy: `1.0`;
  - failure labels: none.

## Verification

- `python -m pytest tests/test_newton_shapes.py -q`: `7 passed`
- `python -m pytest tests/test_newton_diagnostics.py -q`: `7 passed`
- `python -m pytest tests/test_newton_drop_settle.py -q`: `10 passed`
- `python -m pytest tests/test_newton_sphere_rain.py -q`: `12 passed`

Final full-suite verification is recorded in the branch completion notes after review and merge.

## Boundaries

This record supports a narrow claim: this repository can map and construct Newton diagnostic
shapes for a synthetic package containing the six Newton-native analytic kinds `box`, `sphere`,
`capsule`, `cylinder`, `cone`, and `ellipsoid`.

This is not full CPD paper reproduction, benchmark evidence, collision-quality validation,
deployment readiness, whole-robot collider-quality evidence, or proof that the CPD-like generator
should emit these new native kinds by default.
