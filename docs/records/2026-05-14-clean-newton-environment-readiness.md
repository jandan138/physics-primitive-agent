# 2026-05-14 Clean Newton Environment Readiness

## Date

2026-05-14

## Status

Complete

## Changes

- Created the external Python 3.10 conda environment at
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`.
- Installed this repository in editable dev mode from the stable repository root at
  `/cpfs/user/zhuzihou/dev/physics-primitive-agent`.
- Installed the Newton source checkout in editable mode with the `importers` extra from
  `/cpfs/user/zhuzihou/dev/newton`.
- Preserved the earlier ambient Isaac/DSW Python `dependency_gap` record as historical baseline
  evidence instead of rewriting it.

## Verification

- Conda environment creation:

```bash
/cpfs/user/zhuzihou/conda-managed/miniforge3/bin/conda create -y \
  -p /cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310 \
  python=3.10 pip
```

Observed result: exit `0`, Python `3.10.20`.

- Project install:

```bash
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m pip install -e "/cpfs/user/zhuzihou/dev/physics-primitive-agent[dev]" \
  --index-url https://pypi.org/simple --timeout 60 --retries 3 --progress-bar off
```

Observed result: exit `0`.

- Newton importer install:

```bash
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m pip install -e "/cpfs/user/zhuzihou/dev/newton[importers]" \
  --index-url https://pypi.org/simple \
  --extra-index-url https://pypi.nvidia.com/ \
  --timeout 120 --retries 5 --resume-retries 20 --progress-bar off
```

The first Newton importer install attempt exited `2` because the `warp_lang-1.13.0` wheel download
was interrupted after `45.6/138.3 MB`. The dependency version was not changed. The root cause was
handled as an incomplete network download by preinstalling Warp with resume retries:

```bash
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  -m pip install "warp-lang==1.13.0" \
  --index-url https://pypi.org/simple \
  --extra-index-url https://pypi.nvidia.com/ \
  --timeout 120 --retries 5 --resume-retries 20 --progress-bar off
```

Observed result: exit `0`. Re-running the Newton importer install then exited `0`.

- Import provenance check:

```bash
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python - <<'PY'
import importlib.metadata as md
import sys

import newton
import warp
from pxr import Usd

print(f"python={sys.executable}")
print(f"python_version={sys.version.split()[0]}")
print(f"newton_file={getattr(newton, '__file__', '<missing>')}")
print(f"newton_dist={md.version('newton')}")
print(f"warp_dist={md.version('warp-lang')}")
print(f"warp_module={getattr(warp, '__version__', '<missing>')}")
print(f"usd_core_dist={md.version('usd-core')}")
print(f"usd_version={Usd.GetVersion()}")
print(f"newton_usd_schemas_dist={md.version('newton-usd-schemas')}")
PY
```

```text
python=/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python
python_version=3.10.20
newton_file=/cpfs/user/zhuzihou/dev/newton/newton/__init__.py
newton_dist=1.3.0.dev0
warp_dist=1.13.0
warp_module=1.13.0
usd_core_dist=26.3
usd_version=(0, 26, 3)
newton_usd_schemas_dist=0.2.0
```

- Environment-readiness command from the stable repository root:

```bash
NPC_ENV_ROOT=/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310 \
NPC_PYTHON=/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
NPC_CODE_ROOT=/cpfs/user/zhuzihou/dev/physics-primitive-agent \
NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton \
NPC_OUTPUT_DIR=/cpfs/user/zhuzihou/dev/physics-primitive-agent/reports/generated/environment-readiness/local-newton-py310 \
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python \
  scripts/env/readiness_check.py \
  --output reports/generated/environment-readiness/local-newton-py310/readiness.json
```

Observed summary:

- command return code: `0`;
- report stage: `environment_readiness`;
- report status: `smoke_passed`;
- Python status: `smoke_passed`;
- Newton source status: `smoke_passed`;
- Newton source remote: `https://github.com/newton-physics/newton.git`;
- Newton source branch: `main`;
- Newton source commit: `96713fa965463b69c229a4d30582c733ff3526bb`;
- Newton source dirty state: `false`;
- `check_newton` status: `smoke_passed`;
- `check_newton` source path: `/cpfs/user/zhuzihou/dev/newton`;
- GPU status: `smoke_passed`;
- GPU: `NVIDIA GeForce RTX 4090`, driver `570.153.02`;
- output directory status: `smoke_passed`;
- report output status: `smoke_passed`.

## Artifacts

- Environment path:
  `/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310`
- Stable repository root:
  `/cpfs/user/zhuzihou/dev/physics-primitive-agent`
- Newton source checkout:
  `/cpfs/user/zhuzihou/dev/newton`
- Generated report path:
  `reports/generated/environment-readiness/local-newton-py310/readiness.json` (ignored by git).

## Claim Impact

- Supports the narrow claim that this named local clean Python/Newton environment passed
  environment-readiness diagnostics for the named Newton source checkout and hardware environment.
- Supports using this environment as the local starting point for the next Newton diagnostic
  checker work.
- Does not support claims of Newton simulation execution, CPD reproduction, primitive fitting,
  collision proxy quality, benchmark superiority, deployment readiness, real-world transfer, or
  safety certification.

## Next Action

- Start the Phase 0 non-LLM primitive baseline and Newton diagnostic checker against recorded
  assets, configs, solver settings, seeds, and per-run readiness reports.
