# 2026-05-14 CPD-Like Newton Slice

## Date

2026-05-14

## Status

Complete; partially superseded by later clean-environment and geometry-only CPD-like records.

## Decision

Add a minimal CPD-like baseline execution slice before implementing decomposition logic.

## Changes

- Load a CPD-like baseline config through the existing compiler config path.
- Track smoke asset paths, sizes, and hashes without committing raw USD assets.
- Inspect the locally installed Newton source checkout and emit a JSON environment report.
- Keep generated report output under the ignored `reports/generated/cpd_like_baseline/` path.

## Verification

- `python -m pytest -q`: exit 0.
- `python scripts/validate_docs.py`: exit 0.
- `git diff --check`: exit 0.
- `PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-newton`: exit 0, status `dependency_gap`.

The active Python environment currently has an editable install pointing at
`/cpfs/user/zhuzihou/dev/physics-primitive-agent`, not this feature worktree. Until the worktree is
installed, run manual CLI checks with explicit source precedence:

```bash
PYTHONPATH=src python -m primitive_collision_compiler.cli --config configs/experiments/cpd_like_baseline.yaml --check-newton
```

## Artifacts

- Config: `configs/experiments/cpd_like_baseline.yaml`
- Manifest: `assets/manifests/cpd_like_smoke_assets.yaml`
- Newton diagnostic CLI: `npc-compile --config <config> --check-newton`
- Generated report target: `reports/generated/cpd_like_baseline/` (ignored)
- Raw USD assets: not committed; referenced only by manifest path and hash.

## Claim Impact

- This is environment and config evidence only.
- It does not show CPD reproduction.
- It does not show collision detection quality or benchmark superiority.
- It does not show runtime Newton simulation checks on the bed or Franka assets.

## Observed Newton Runtime State

Newton source is expected at `/cpfs/user/zhuzihou/dev/newton`.

- Remote: `https://github.com/newton-physics/newton.git`
- Commit: `96713fa965463b69c229a4d30582c733ff3526bb`
- CLI diagnostic status: `dependency_gap`
- Import detail: `No module named 'warp'`

The `dependency_gap` status is an acceptable current result because this slice only records source
availability and Python import readiness. It is not a CPD reproduction result.

Later clean-environment work resolved this local dependency gap for the recommended Python
environment. See
[2026-05-14 Clean Newton Environment Readiness](2026-05-14-clean-newton-environment-readiness.md)
and [2026-05-14 CPD Reproduction Slice](2026-05-14-cpd-reproduction-slice.md) for current
`smoke_passed` evidence. This historical record still does not represent Newton simulation probe
evidence.

## Next Action

- Install Newton Python dependencies in a reproducible environment.
- Add USD import smoke checks for the bed and Franka assets.
- Implement a restricted primitive proposal/evaluation loop only after import smoke checks pass.
