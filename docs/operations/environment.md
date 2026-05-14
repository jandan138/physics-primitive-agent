# Environment Readiness

This page defines the local runtime contract for Newton Primitive Collision Compiler diagnostics.
It is an operator guide for dependency evidence, not a claim that Newton simulation, CPD
reproduction, or collision compilation is implemented.

## Recommended Local Runtime

Use an external clean Python 3.10 environment for Newton work. The current recommended local path is:

```text
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310
```

This path is local to this machine. Other machines may use a different path if they provide the
same environment variables and readiness JSON.

## Required Variables

Set these variables before running readiness checks:

```bash
export NPC_ENV_ROOT=/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310
export NPC_PYTHON="$NPC_ENV_ROOT/bin/python"
export NPC_CODE_ROOT=/cpfs/user/zhuzihou/dev/physics-primitive-agent
export NEWTON_SOURCE_DIR=/cpfs/user/zhuzihou/dev/newton
export NPC_OUTPUT_DIR="$NPC_CODE_ROOT/reports/generated/environment-readiness/local"
```

Optional:

```bash
export NPC_WORKER_SETUP_SCRIPT=/path/to/worker_setup.sh
```

The readiness checker records the setup script path, realpath, SHA-256, mtime, and size. Phase 1
does not source the setup script and does not run compiler smoke commands through it.

## Future Environment Installation

The Phase 1 checker does not create or mutate environments. When a clean environment is created,
the intended first dependency shape is:

```bash
python -m pip install -e ".[dev]"
python -m pip install -e "/cpfs/user/zhuzihou/dev/newton[importers]" --extra-index-url https://pypi.nvidia.com/
```

Do not downgrade or modify the ambient Isaac/DSW Python to satisfy Newton. Keep the canonical
runtime outside this repository so future DLC workers can point at the same interpreter path.

`uv` is optional after Phase 1. It can help lock dependencies later, but it does not replace the
readiness checks for mount visibility, interpreter realpaths, module provenance, GPU visibility, or
output writability.

## Run The Check

From the repository root:

```bash
python scripts/env/readiness_check.py
```

To write a specific report path:

```bash
python scripts/env/readiness_check.py --output "$NPC_OUTPUT_DIR/readiness.json"
```

The script always prints JSON to stdout. It returns `0` only when the selected readiness scope has
status `smoke_passed`; dependency gaps return nonzero while still producing a report.

Generated readiness reports belong under `reports/generated/` or another explicit
`NPC_OUTPUT_DIR`. Do not commit generated report directories, experiment run directories, full logs,
environment directories, raw or generated 3D assets, videos, or credentials.

## Current Local Observation

The latest merged `master` readiness record is
[2026-05-14 Environment Readiness Master Verification](../records/2026-05-14-environment-readiness-master-verification.md).
It records status `dependency_gap` for the active Isaac/DSW Python path and local Newton source.
Treat that as the baseline to improve, not as Newton simulation readiness.

## Status Meaning

- `smoke_passed`: the selected readiness scope passed.
- `dependency_gap`: a required package, source checkout, executable, or selected optional dependency
  is missing.
- `import_error`: a module exists but import or source provenance is wrong.
- `runtime_failure`: imports/configuration passed, but a minimal runtime action failed.
- `configuration_error`: required readiness inputs are missing or internally inconsistent.

These statuses are diagnostics only. They do not support claims of CPD reproduction, Newton
simulation execution, collision proxy quality, benchmark superiority, deployment readiness,
real-world transfer, or safety certification.
