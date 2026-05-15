# 2026-05-15 CPD Capped-Cylinder Proxy

## Date

2026-05-15

## Status

Complete

## Changes

- Added an opt-in offline `capped_cylinder` geometry proposal proxy to the CPD-like primitive
  fitter.
- Added `configs/experiments/cpd_like_capped_cylinder_proxy.yaml`, an offline-only objective-report
  smoke config.
- Kept Newton shape mapping unchanged: `capped_cylinder` remains a mapping gap.
- Added tests for primitive fitting, unsupported paper primitive accounting, objective reporting,
  config ownership, CLI behavior, and Newton mapping boundary.

## Result

Command:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli \
  --config configs/experiments/cpd_like_capped_cylinder_proxy.yaml \
  --run-cpd-like-objective-report
```

Result:

- exit code: 0;
- stage: `cpd_like_offline_objective`;
- status: `smoke_passed`;
- asset id: `grscenes_bed_0a85b986_capped_cylinder_proxy`;
- decomposition stage: `cpd_like_component_merge_gate`;
- primitive count: 32;
- target primitive count: 32;
- contained primitive count: 32;
- unsupported paper primitive count: 2;
- remaining unsupported paper primitives: `frustum`, `trapezoidal_prism`;
- evidence level: `offline_cpd_like_capped_cylinder_proxy_smoke`.

## Verification

- `python -m pytest tests/test_cpd_like_decompose.py -q -k "capped_cylinder or unsupported_gap or equal_proxy"`:
  exit 0, `3 passed, 16 deselected`.
- `python -m pytest tests/test_cpd_like_decompose.py tests/test_cpd_like_objective.py tests/test_newton_shapes.py tests/test_cli.py tests/test_cpd_like_config.py -q -k "capped_cylinder or unsupported_gap or equal_proxy"`:
  exit 0, `7 passed, 88 deselected`.
- Real offline config command above: exit 0, `smoke_passed`.
- `python scripts/validate_docs.py`: exit 0, `docs validation passed`.
- `git diff --check`: exit 0, no whitespace errors.
- `python -m pytest -q`: exit 0, `180 passed`.
- `python -m ruff check .`: not run to completion because the current `/usr/bin/python`
  environment does not have `ruff` installed.

## Artifacts

- Config: `configs/experiments/cpd_like_capped_cylinder_proxy.yaml`
- Source: `src/primitive_collision_compiler/baselines/cpd_like/primitives.py`
- Tests:
  - `tests/test_cpd_like_decompose.py`
  - `tests/test_cpd_like_objective.py`
  - `tests/test_newton_shapes.py`
  - `tests/test_cli.py`
  - `tests/test_cpd_like_config.py`
- No raw or generated 3D assets, large logs, videos, or run directories were added.

## Claim Impact

This supports only a narrow claim: the current code can run an opt-in offline
`capped_cylinder` geometry proposal proxy and report that a named objective smoke reduces the
unsupported paper primitive vocabulary gap from three types to two.

This does not support paper-faithful CPD primitive fitting, Newton support for capped cylinders,
collision-quality validation, benchmark evidence, broad asset/task evidence, or full CPD paper
reproduction.

## Next Action

Use this primitive-vocabulary accounting to select the next restricted primitive-fit quality or
merge-search target. Do not broaden Newton task claims until a separate mapping implementation and
diagnostic record exist.
