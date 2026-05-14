# Environment Normalization Design

## Purpose

This design defines the first environment-normalization slice for the Newton Primitive Collision
Compiler bootstrap. The goal is to make runtime dependency state observable and reproducible enough
for local work and future DLC workers without claiming Newton runtime readiness, CPD reproduction,
or simulation results.

The current repository can run USD asset-open smoke diagnostics, but the active Python interpreter
is an ambient Isaac/DSW Python. That environment contains `pxr` from `usd-core==26.5`, while the
local Newton source importers declare `usd-core>=25.5,<26.5`. The current Newton import diagnostic
still reports `dependency_gap` because `warp` is unavailable. This slice turns those facts into a
clean environment contract instead of relying on accidental package availability.

## Genesis-LLM Lessons To Keep

The useful pattern from `genesis-llm` is not its full DLC training pipeline. The useful pattern is:

- choose the Python executable explicitly;
- forward only deliberate environment variables into remote workers;
- write structured runtime evidence (`run.json` / readiness JSON) from the worker's point of view;
- default to local dry-run, mock-run, and smoke checks before any paid or remote execution;
- preserve claim boundaries by treating dependency gaps as dependency evidence, not algorithm
  evidence.

## Genesis-LLM Patterns To Avoid

This repository should not copy the historical or project-specific parts of `genesis-llm`:

- no long DLC submission framework in Phase 1;
- no hardcoded DLC workspace, resource, region, image, or data-source IDs in canonical docs;
- no training-gate abstractions;
- no Hugging Face token, proxy, or model-cache logic;
- no use of `tmp/` virtual environments as canonical runtime state;
- no promotion of a smoke pass into compiler, benchmark, deployment, or safety claims.

## Phase 1 Scope

Phase 1 is a local environment-readiness contract and diagnostic tool. It does not install or mutate
the runtime environment.

Phase 1 includes:

- an operation document at `docs/operations/environment.md`;
- a read-only readiness checker at `scripts/env/readiness_check.py`;
- structured readiness JSON written to an ignored generated path by default;
- a dated decision record under `docs/records/`;
- tests for readiness status classification and JSON shape.

Phase 1 excludes:

- creating or installing the conda environment;
- installing `uv`;
- implementing a DLC wrapper;
- running real DLC jobs;
- running Newton simulation;
- implementing CPD or collision proxy generation.

## Canonical Runtime Contract

The recommended local runtime is an external clean Python 3.10 environment:

```text
/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310
```

The path is a current-environment recommendation, not a portable global rule. Other machines may use
different paths, but they must provide equivalent environment variables and readiness evidence.

Required local variables:

- `NPC_ENV_ROOT`: root directory of the canonical environment;
- `NPC_PYTHON`: Python executable for the canonical environment;
- `NPC_CODE_ROOT`: checkout path for this repository;
- `NEWTON_SOURCE_DIR`: Newton source checkout path;
- `NPC_OUTPUT_DIR`: writable directory for readiness reports and future run records.

Optional local variable:

- `NPC_WORKER_SETUP_SCRIPT`: sourceable setup script for compiler, CUDA, or worker-specific
  environment setup.

Future DLC submit-side records may additionally include:

- `DLC_IMAGE`;
- `DLC_CODE_ROOT`;
- DLC workspace, resource, region, and data-source or mount-set identifiers;
- `CUDA_VISIBLE_DEVICES`.

Those DLC fields belong in run records or local operator docs, not in global claim documents.

## Dependency Strategy

Use Python 3.10 first. It matches this repository's current target, the current successful USD smoke
environment, and known local Genesis-LLM managed-environment precedent.

The recommended initial dependency shape for the future canonical environment is:

```text
python -m pip install -e ".[dev]"
python -m pip install -e "/cpfs/user/zhuzihou/dev/newton[importers]" --extra-index-url https://pypi.nvidia.com/
```

This should let Newton's resolver choose a compatible `usd-core` version, expected to be below
`26.5` for the current Newton importers contract. Do not downgrade or modify the ambient
Isaac/DSW Python to satisfy Newton.

Do not require `uv` for Phase 1. Newton's upstream source supports `uv`, and `uv.lock` may become
useful later, but `uv` does not solve the immediate DLC-readiness risks: worker mount visibility,
symlinked Python executables, module provenance, setup-script trust boundaries, CUDA visibility, and
output-path writability.

## Readiness Checker

`scripts/env/readiness_check.py` should be read-only except for writing its report file. It should
not install packages, modify environment variables globally, run real DLC jobs, or execute arbitrary
commands supplied by users.

The checker should inspect:

- `NPC_ENV_ROOT`, `NPC_PYTHON`, `Path(NPC_PYTHON).resolve()`, `sys.executable`, `sys.prefix`, and
  site-package paths as observed through `NPC_PYTHON`;
- selected `sys.path` entries to detect ambient Isaac/DSW leakage;
- `NEWTON_SOURCE_DIR` existence, remote URL, branch, commit, dirty state, and submodule status when
  available;
- module import provenance and versions for `newton`, `warp`, `pxr.Usd`, and `usd-core`;
- whether `newton.__file__` resolves under `NEWTON_SOURCE_DIR`;
- whether `pxr` and `warp` resolve under the canonical environment rather than an ambient
  interpreter prefix;
- GPU and CUDA visibility from `nvidia-smi` when available;
- compiler visibility and a small C/C++ compile smoke when a setup script is configured;
- `NPC_OUTPUT_DIR` real path, writability, free space, inode availability, and ability to write and
  fsync a tiny file;
- existing repository diagnostics: `npc-compile --check-newton` and, when requested,
  `npc-compile --check-assets`.

The setup script is a trust boundary. The checker should record `NPC_WORKER_SETUP_SCRIPT` path,
realpath, SHA-256, and mtime when present. It should not print or store the script contents.

## Status Contract

Readiness statuses must stay narrower than capability claims:

- `smoke_passed`: all checks for the selected readiness scope passed.
- `dependency_gap`: a required package, source directory, executable, version contract, or optional
  dependency for the selected scope is missing.
- `import_error`: a module exists but import fails, resolves outside the expected source or
  environment, or raises an ABI/symbol/runtime import exception.
- `runtime_failure`: imports pass, but a minimal runtime action such as CUDA/Warp device probing,
  compiler smoke, output write, or repository diagnostic execution fails.
- `configuration_error`: required readiness inputs are malformed or internally inconsistent.

Only `smoke_passed` means the selected readiness scope passed. It does not imply CPD reproduction,
Newton simulation readiness, collision quality, benchmark quality, deployment readiness, or safety
certification.

## Readiness JSON Shape

The report should be small and structured:

```json
{
  "stage": "environment_readiness",
  "status": "dependency_gap",
  "scope": "local",
  "checks": [
    {"name": "npc_python", "status": "found", "detail": "..."}
  ],
  "python": {
    "executable": "...",
    "realpath": "...",
    "version": "...",
    "prefix": "...",
    "site_packages": []
  },
  "modules": {
    "newton": {"status": "dependency_gap", "version": null, "file": null},
    "warp": {"status": "dependency_gap", "version": null, "file": null},
    "pxr_usd": {"status": "smoke_passed", "version": "...", "file": "..."}
  },
  "newton_source": {
    "path": "...",
    "remote": "...",
    "branch": "...",
    "commit": "...",
    "dirty": false
  },
  "gpu": {
    "nvidia_smi": "available",
    "driver": "...",
    "cuda": "..."
  },
  "output": {
    "path": "...",
    "writable": true
  },
  "repository_diagnostics": {
    "check_newton": {"status": "dependency_gap"},
    "check_assets": {"status": "smoke_passed"}
  }
}
```

The exact field values may vary by platform, but the checker should preserve this top-level shape.

## Artifact Policy

Commit-safe artifacts:

- `scripts/env/readiness_check.py`;
- tests;
- `docs/operations/environment.md`;
- dated Markdown records;
- small example summaries or schema notes.

Do not commit:

- external environment directories;
- raw or generated 3D assets;
- full generated readiness/run directories;
- large stdout/stderr logs;
- complete `pip freeze` or `conda env export` snapshots unless reduced to a small curated summary;
- tokens, proxy settings, credentials, private registry auth, or setup-script contents.

Generated reports should default to an ignored path under `reports/generated/` or an explicit
`NPC_OUTPUT_DIR`.

## Future Phases

Phase 2 can add run-record helpers and an `env-snapshot/` layout for real experiment attempts.
Phase 3 can add a minimal DLC wrapper that defaults to dry-run/mock-run and records what the worker
actually sees. Real DLC submit must remain explicit and separate from local readiness.

`uv` can be evaluated after Phase 1 and the first clean canonical runtime smoke. Its role would be
dependency locking, not worker-path discovery or DLC mount validation.

## Claim Boundary

This design supports only environment-readiness diagnostics. It does not support claims of:

- a working collision compiler;
- CPD reproduction;
- Newton simulation execution;
- collision proxy quality;
- benchmark superiority;
- deployment readiness;
- real-world transfer;
- safety certification.
