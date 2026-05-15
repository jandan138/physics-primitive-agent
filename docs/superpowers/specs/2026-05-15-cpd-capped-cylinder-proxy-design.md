# CPD Capped-Cylinder Proxy Design

## Context

The expected-failure workbench made the next CPD paper-story target explicit:
`restricted_primitive_vocabulary_gap` points to `primitive_fit_extension`. The current CPD-like
baseline supports `box`, `sphere`, and `capsule` in
`src/primitive_collision_compiler/baselines/cpd_like/primitives.py`, while
`capped_cylinder`, `frustum`, and `trapezoidal_prism` remain reported as unsupported paper
primitive types.

This slice adds the first primitive-vocabulary extension without claiming full CPD primitive
fitting. It should reduce the paper primitive gap in a named offline opt-in report, not change
existing Newton task claims.

## Goal

Add an opt-in offline `capped_cylinder` geometry proposal proxy to the CPD-like primitive fitter,
then record that a named offline report can reduce the unsupported paper primitive gap from 3 to 2.

## Non-Goals

- Do not implement paper-faithful capped-cylinder fitting.
- Do not add Newton mapping for `capped_cylinder`.
- Do not alter completed experiment configs or dated records.
- Do not claim collision-quality improvement, benchmark evidence, asset/task improvement, or full
  CPD paper reproduction.
- Do not make existing Newton drop/settle or sphere-rain configs emit `capped_cylinder` shapes.

## Recommended Approach

Use a narrow opt-in implementation:

1. Add `capped_cylinder` to the CPD-like fitter as a supported geometry proposal proxy.
2. Keep existing default/configured Newton-facing primitive subsets unchanged.
3. Add a new offline objective-report config for the capped-cylinder proxy.
4. Keep Newton shape support unchanged so `PrimitiveSpec(kind="capped_cylinder")` still maps to a
   Newton `mapping_gap`.

This makes the primitive vocabulary accounting more paper-aligned while preserving the current
runtime boundary.

## Primitive Fit Semantics

The proxy uses the same local-axis machinery as existing primitive fits:

- choose the axis with the largest local span;
- compute axial projection min/max and half height;
- compute a center on that axis using the projection midpoint and perpendicular centroid;
- set radius to the maximum radial distance from the axis;
- use positive floors from `MIN_DIMENSION`;
- report containment using the same capsule-style distance check;
- report volume as a capped cylinder with hemispherical caps:

```text
pi * radius^2 * (2 * half_height) + (4/3) * pi * radius^3
```

The output dimensions must include explicit proxy markers:

```python
{
    "radius": radius,
    "half_height": half_height,
    "axis_index": axis_index,
    "cap_model": "hemisphere_caps",
    "proxy_fit": "axis_span_radial_proxy",
}
```

Those markers are required so reviewers do not confuse this with paper-faithful primitive fitting.

## Unsupported Primitive Accounting

Unsupported paper primitive accounting should be based on requested and supported vocabulary, not
only on the winning fit. If a run requests `("box", "capped_cylinder")`, then `capped_cylinder`
should be removed from the unsupported paper list even if `box` wins a particular face group.

Expected behavior:

- `primitive_subset=("box",)` keeps unsupported primitives as
  `("capped_cylinder", "frustum", "trapezoidal_prism")`;
- `primitive_subset=("capped_cylinder",)` reports unsupported primitives as
  `("frustum", "trapezoidal_prism")`;
- `primitive_subset=("box", "capped_cylinder")` also reports unsupported primitives as
  `("frustum", "trapezoidal_prism")`.

## Tie-Breaking

Because the capped-cylinder proxy is intentionally close to the current capsule geometry, this
slice must avoid silently changing existing Newton-facing outputs. The simplest rule is:

- when multiple candidate primitives have equal weighted volume, preserve the order in
  `primitive_subset`.

Existing configs list `sphere`, `capsule`, and `box` before unsupported paper primitives, so this
rule avoids making `capped_cylinder` win accidentally when it is appended to historical metadata.
New opt-in tests and the new offline config should request `("capped_cylinder",)` when they need
the proxy to appear.

## Offline Config

Add a new config:

```text
configs/experiments/cpd_like_capped_cylinder_proxy.yaml
```

It should mirror the existing objective-report smoke but remain offline-only:

- `compile.verify` contains only `cpd_like_objective_report`;
- `cpd_like.primitive_subset` contains only `capped_cylinder`;
- `cpd_like.unsupported_primitives` lists only `frustum` and `trapezoidal_prism`;
- `cpd_like_objective.primitive_type_weights` includes `capped_cylinder: 1.0`;
- no Newton diagnostic stage is requested.

## Tests

Add failing tests first:

- `fit_best_primitive(..., ("capped_cylinder",))` returns `capped_cylinder`, positive dimensions,
  proxy markers, containment true, and only `frustum`/`trapezoidal_prism` unsupported.
- Existing `("box",)` behavior still reports all three unsupported paper primitives.
- Mixed `("box", "capped_cylinder")` objective accounting removes only `capped_cylinder` from
  `paper_primitive_gap`.
- Newton `map_package_shapes` still returns `mapping_gap` for `capped_cylinder`.
- CLI objective-report smoke with the new offline config emits strict JSON and records unsupported
  paper primitive count 2 without invoking Newton.

## Documentation

Update:

- `README.md`;
- `docs/index.md`;
- `docs/reference/claim-boundaries.md`;
- `docs/deepdive/evidence-status.md`;
- `docs/reference/cpd-like-face-merge-explainer.md`;
- `docs/reference/cpd-paper-story-status.md`;
- `docs/reference/cpd-objective-report-alignment.md`;
- `docs/records/README.md`;
- `experiments/registry.yaml`;
- add `docs/records/2026-05-15-cpd-capped-cylinder-proxy.md`.

Use:

- "opt-in offline `capped_cylinder` geometry proposal proxy";
- "primitive-vocabulary accounting for a restricted proposal baseline";
- "unsupported paper primitive gap decreases from 3 to 2 in the named opt-in report";
- "no Newton mapping or task-level improvement is claimed for `capped_cylinder`."

Avoid:

- "CPD primitive fitting implemented";
- "paper-faithful capped cylinder support";
- "Newton supports capped cylinders";
- "collision quality improved";
- "benchmark result";
- "safe collider";
- "validated collider."

## Verification

Before merge, run:

```bash
python scripts/validate_docs.py
git diff --check
python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_objective.py tests/test_newton_shapes.py tests/test_cli.py -q -k "capped_cylinder or primitive_subset or objective_report"
python -m pytest -q
```

If `ruff` is not installed in the active Python environment, record that explicitly instead of
claiming lint coverage.

## Claim Boundary

This slice may support only this new claim:

```text
The current code can run an opt-in offline capped-cylinder geometry proposal proxy and report that
the named objective smoke reduces unsupported paper primitive vocabulary from three types to two.
```

It does not support paper-faithful CPD primitive fitting, Newton support for capped cylinders,
collision-quality validation, benchmark evidence, or full CPD paper reproduction.
