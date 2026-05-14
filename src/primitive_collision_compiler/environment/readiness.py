from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

REQUIRED_ENV_VARS = (
    "NPC_ENV_ROOT",
    "NPC_PYTHON",
    "NPC_CODE_ROOT",
    "NEWTON_SOURCE_DIR",
    "NPC_OUTPUT_DIR",
)

_STATUS_ORDER = {
    "smoke_passed": 0,
    "dependency_gap": 1,
    "import_error": 2,
    "runtime_failure": 3,
    "configuration_error": 4,
}
_NON_READINESS_STATUSES = {"found", "not_configured"}


def pick_report_status(statuses: list[str] | tuple[str, ...]) -> str:
    if not statuses:
        return "smoke_passed"
    normalized = [_normalize_readiness_status(status) for status in statuses]
    return max(normalized, key=lambda status: _STATUS_ORDER.get(status, _STATUS_ORDER["runtime_failure"]))


def build_configuration_report(env: Mapping[str, str], *, scope: str = "local") -> dict[str, object]:
    checks = []
    for name in REQUIRED_ENV_VARS:
        value = env.get(name, "")
        if value:
            checks.append({"name": name, "status": "found", "detail": value})
        else:
            checks.append(
                {
                    "name": name,
                    "status": "configuration_error",
                    "detail": "required variable is not set",
                }
            )

    return {
        "stage": "environment_readiness",
        "status": pick_report_status([check["status"] for check in checks]),
        "scope": scope,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "python": {
            "executable": env.get("NPC_PYTHON"),
            "realpath": None,
            "version": None,
            "prefix": None,
            "site_packages": [],
        },
        "modules": {},
        "newton_source": {
            "path": env.get("NEWTON_SOURCE_DIR"),
            "remote": None,
            "branch": None,
            "commit": None,
            "dirty": None,
        },
        "gpu": {"nvidia_smi": "not_checked"},
        "output": {"path": env.get("NPC_OUTPUT_DIR"), "writable": None},
        "repository_diagnostics": {},
    }


def run_readiness_check(
    env: Mapping[str, str], *, scope: str = "local", include_assets: bool = False
) -> dict[str, object]:
    report = build_configuration_report(env, scope=scope)
    if report["status"] == "configuration_error":
        return report

    python_report = inspect_python_environment(
        env["NPC_PYTHON"],
        env_root=env.get("NPC_ENV_ROOT"),
        newton_source_dir=env.get("NEWTON_SOURCE_DIR"),
    )
    modules = python_report.pop("modules", _empty_module_reports())
    newton_source = inspect_newton_source(env["NEWTON_SOURCE_DIR"])
    output = inspect_output_dir(env["NPC_OUTPUT_DIR"])
    setup_script = inspect_setup_script(env.get("NPC_WORKER_SETUP_SCRIPT"))
    gpu = inspect_gpu_visibility()
    repository_diagnostics = {
        "check_newton": run_repository_diagnostic(
            env,
            "check_newton",
            ["--config", "configs/experiments/cpd_like_baseline.yaml", "--check-newton"],
        )
    }
    if include_assets:
        repository_diagnostics["check_assets"] = run_repository_diagnostic(
            env,
            "check_assets",
            ["--config", "configs/experiments/cpd_like_baseline.yaml", "--check-assets"],
        )

    statuses = [check["status"] for check in report["checks"]]
    statuses.extend(
        [
            str(python_report["status"]),
            str(newton_source["status"]),
            str(output["status"]),
            str(setup_script["status"]),
            str(gpu["status"]),
        ]
    )
    statuses.extend(str(diagnostic["status"]) for diagnostic in repository_diagnostics.values())

    report.update(
        {
            "status": pick_report_status(statuses),
            "python": python_report,
            "modules": modules,
            "newton_source": newton_source,
            "gpu": gpu,
            "output": output,
            "setup_script": setup_script,
            "repository_diagnostics": repository_diagnostics,
        }
    )
    return report


def inspect_newton_source(source_dir: str) -> dict[str, object]:
    source_path = Path(source_dir)
    if not source_path.exists():
        return {
            "status": "dependency_gap",
            "path": source_dir,
            "realpath": None,
            "exists": False,
            "remote": None,
            "branch": None,
            "commit": None,
            "dirty": None,
            "submodules": None,
            "detail": "source directory does not exist",
        }

    if not source_path.is_dir():
        return {
            "status": "configuration_error",
            "path": source_dir,
            "realpath": str(source_path.resolve()),
            "exists": True,
            "remote": None,
            "branch": None,
            "commit": None,
            "dirty": None,
            "submodules": None,
            "detail": "source path is not a directory",
        }

    remote = _git_output(source_path, ["config", "--get", "remote.origin.url"])
    branch = _git_output(source_path, ["rev-parse", "--abbrev-ref", "HEAD"])
    commit = _git_output(source_path, ["rev-parse", "HEAD"])
    dirty_output = _git_output(source_path, ["status", "--porcelain"])
    submodules = _git_output(source_path, ["submodule", "status", "--recursive"])
    status = "smoke_passed" if commit else "dependency_gap"

    return {
        "status": status,
        "path": source_dir,
        "realpath": str(source_path.resolve()),
        "exists": True,
        "remote": remote,
        "branch": branch,
        "commit": commit,
        "dirty": bool(dirty_output) if dirty_output is not None else None,
        "submodules": submodules.splitlines() if submodules else [],
    }


def inspect_output_dir(output_dir: str) -> dict[str, object]:
    output_path = Path(output_dir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        probe_path = output_path / ".readiness-write-test"
        with probe_path.open("w", encoding="utf-8") as handle:
            handle.write("readiness\n")
            handle.flush()
            os.fsync(handle.fileno())
        probe_path.unlink(missing_ok=True)
        stat = os.statvfs(output_path)
    except OSError as exc:
        return {
            "status": "runtime_failure",
            "path": output_dir,
            "realpath": str(output_path.resolve()) if output_path.exists() else None,
            "writable": False,
            "free_bytes": None,
            "available_inodes": None,
            "detail": f"{type(exc).__name__}: {exc}",
        }

    return {
        "status": "smoke_passed",
        "path": output_dir,
        "realpath": str(output_path.resolve()),
        "writable": True,
        "free_bytes": stat.f_bavail * stat.f_frsize,
        "available_inodes": stat.f_favail,
    }


def inspect_setup_script(setup_script: str | None) -> dict[str, object]:
    if not setup_script:
        return {"status": "not_configured", "configured": False, "path": None}

    script_path = Path(setup_script)
    if not script_path.exists():
        return {
            "status": "configuration_error",
            "configured": True,
            "path": setup_script,
            "realpath": None,
            "sha256": None,
            "mtime": None,
            "size_bytes": None,
            "detail": "setup script does not exist",
        }

    stat = script_path.stat()
    return {
        "status": "smoke_passed",
        "configured": True,
        "path": setup_script,
        "realpath": str(script_path.resolve()),
        "sha256": _sha256_file(script_path),
        "mtime": stat.st_mtime,
        "size_bytes": stat.st_size,
    }


def inspect_gpu_visibility() -> dict[str, object]:
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except FileNotFoundError:
        return {
            "status": "dependency_gap",
            "nvidia_smi": "unavailable",
            "driver": None,
            "gpus": [],
            "detail": "nvidia-smi is not on PATH",
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "status": "runtime_failure",
            "nvidia_smi": "error",
            "driver": None,
            "gpus": [],
            "detail": f"{type(exc).__name__}: {exc}",
        }

    if result.returncode != 0:
        return {
            "status": "runtime_failure",
            "nvidia_smi": "error",
            "driver": None,
            "gpus": [],
            "detail": result.stderr.strip(),
        }

    gpus = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = [part.strip() for part in line.split(",", 1)]
        gpus.append({"name": parts[0], "driver": parts[1] if len(parts) > 1 else None})

    return {
        "status": "smoke_passed" if gpus else "dependency_gap",
        "nvidia_smi": "available",
        "driver": gpus[0]["driver"] if gpus else None,
        "gpus": gpus,
    }


def run_repository_diagnostic(
    env: Mapping[str, str], name: str, args: list[str]
) -> dict[str, object]:
    python_executable = env.get("NPC_PYTHON")
    code_root = env.get("NPC_CODE_ROOT")
    if not python_executable or not code_root:
        return {
            "status": "configuration_error",
            "name": name,
            "detail": "NPC_PYTHON and NPC_CODE_ROOT are required",
        }

    code_path = Path(code_root)
    full_args = [str(python_executable), "-m", "primitive_collision_compiler.cli", *args]
    process_env = _python_probe_env()
    for key in (*REQUIRED_ENV_VARS, "NPC_WORKER_SETUP_SCRIPT"):
        if env.get(key):
            process_env[key] = env[key]
    pythonpath_entries = [str(code_path / "src"), str(code_path)]
    process_env["PYTHONPATH"] = os.pathsep.join(pythonpath_entries)

    try:
        result = subprocess.run(
            full_args,
            cwd=code_path,
            env=process_env,
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "status": "runtime_failure",
            "name": name,
            "command": full_args,
            "detail": f"{type(exc).__name__}: {exc}",
        }

    payload = _parse_json_or_none(result.stdout)
    raw_status = payload.get("status") if isinstance(payload, dict) else None
    status = _normalize_status(raw_status)
    if status == "smoke_passed" and result.returncode != 0:
        status = "runtime_failure"

    return {
        "status": status,
        "name": name,
        "command": full_args,
        "returncode": result.returncode,
        "payload": payload,
        "stderr": result.stderr.strip(),
    }


def inspect_python_environment(
    python_executable: str,
    *,
    env_root: str | None = None,
    newton_source_dir: str | None = None,
) -> dict[str, object]:
    python_path = Path(python_executable)
    if not python_path.exists():
        return {
            "status": "configuration_error",
            "executable": python_executable,
            "realpath": None,
            "version": None,
            "prefix": None,
            "site_packages": [],
            "sys_path": [],
            "modules": _empty_module_reports(),
            "detail": "python executable does not exist",
        }

    try:
        result = subprocess.run(
            [str(python_path), "-c", _PYTHON_PROBE],
            check=False,
            capture_output=True,
            env=_python_probe_env(),
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "status": "runtime_failure",
            "executable": python_executable,
            "realpath": str(python_path.resolve()),
            "version": None,
            "prefix": None,
            "site_packages": [],
            "sys_path": [],
            "modules": _empty_module_reports(),
            "detail": f"{type(exc).__name__}: {exc}",
        }

    if result.returncode != 0:
        return {
            "status": "runtime_failure",
            "executable": python_executable,
            "realpath": str(python_path.resolve()),
            "version": None,
            "prefix": None,
            "site_packages": [],
            "sys_path": [],
            "modules": _empty_module_reports(),
            "detail": result.stderr.strip(),
        }

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {
            "status": "runtime_failure",
            "executable": python_executable,
            "realpath": str(python_path.resolve()),
            "version": None,
            "prefix": None,
            "site_packages": [],
            "sys_path": [],
            "modules": _empty_module_reports(),
            "detail": f"invalid python probe JSON: {exc}",
        }

    modules = payload.get("modules", {})
    _annotate_python_expectations(payload, env_root=env_root, newton_source_dir=newton_source_dir)
    payload["status"] = pick_report_status(
        [module.get("status", "runtime_failure") for module in modules.values()]
    )
    return payload


def _normalize_readiness_status(status: str) -> str:
    if status in _NON_READINESS_STATUSES:
        return "smoke_passed"
    if status in _STATUS_ORDER:
        return status
    return "runtime_failure"


def _git_output(source_path: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(source_path), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_json_or_none(value: str) -> object | None:
    if not value.strip():
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def _normalize_status(status: object) -> str:
    if status == "missing_source":
        return "dependency_gap"
    if status == "smoke_failed":
        return "runtime_failure"
    if isinstance(status, str):
        return _normalize_readiness_status(status)
    return "smoke_passed" if status else "runtime_failure"


def _python_probe_env() -> dict[str, str]:
    allowed_keys = {
        "CUDA_VISIBLE_DEVICES",
        "HOME",
        "LANG",
        "LC_ALL",
        "LD_LIBRARY_PATH",
        "LOGNAME",
        "NVIDIA_VISIBLE_DEVICES",
        "PATH",
        "TEMP",
        "TMP",
        "TMPDIR",
        "USER",
    }
    env = {key: value for key, value in os.environ.items() if key in allowed_keys}
    env["PYTHONNOUSERSITE"] = "1"
    return env


def _annotate_python_expectations(
    payload: dict[str, object], *, env_root: str | None, newton_source_dir: str | None
) -> None:
    payload["expected"] = {"env_root": env_root, "newton_source_dir": newton_source_dir}
    modules = payload.get("modules", {})
    if not isinstance(modules, dict):
        return

    if env_root:
        env_root_path = Path(env_root).resolve()
        realpath = payload.get("realpath")
        prefix = payload.get("prefix")
        payload["environment_alignment"] = {
            "python_under_env_root": _path_is_relative_to(realpath, env_root_path),
            "prefix_under_env_root": _path_is_relative_to(prefix, env_root_path),
        }
        for name in ("warp", "pxr_usd"):
            module = modules.get(name)
            if isinstance(module, dict) and module.get("status") == "smoke_passed":
                module_file = module.get("file")
                if module_file and not _path_is_relative_to(str(module_file), env_root_path):
                    module["status"] = "import_error"
                    module["detail"] = f"{name} resolved outside NPC_ENV_ROOT"

    if newton_source_dir:
        source_path = Path(newton_source_dir).resolve()
        module = modules.get("newton")
        if isinstance(module, dict) and module.get("status") == "smoke_passed":
            module_file = module.get("file")
            if module_file and not _path_is_relative_to(str(module_file), source_path):
                module["status"] = "import_error"
                module["detail"] = "newton resolved outside NEWTON_SOURCE_DIR"


def _path_is_relative_to(path_value: object, parent: Path) -> bool:
    if not path_value:
        return False
    try:
        Path(str(path_value)).resolve().relative_to(parent)
    except (OSError, ValueError):
        return False
    return True


def _empty_module_reports() -> dict[str, dict[str, object]]:
    return {
        "newton": {"status": "dependency_gap", "version": None, "file": None},
        "warp": {"status": "dependency_gap", "version": None, "file": None},
        "pxr_usd": {"status": "dependency_gap", "version": None, "file": None},
        "usd_core": {"status": "dependency_gap", "version": None, "file": None},
    }


_PYTHON_PROBE = r"""
from __future__ import annotations

import importlib
import importlib.metadata
import json
import site
import sys
from pathlib import Path


def distribution_version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def module_report(name, import_name, distribution_name=None):
    try:
        module = importlib.import_module(import_name)
    except ModuleNotFoundError as exc:
        missing_names = {import_name, import_name.split(".")[0]}
        status = "dependency_gap" if exc.name in missing_names else "import_error"
        return {
            "status": status,
            "version": distribution_version(distribution_name) if distribution_name else None,
            "file": None,
            "detail": str(exc),
        }
    except Exception as exc:
        return {
            "status": "import_error",
            "version": distribution_version(distribution_name) if distribution_name else None,
            "file": None,
            "detail": f"{type(exc).__name__}: {exc}",
        }

    version = distribution_version(distribution_name) if distribution_name else None
    if version is None:
        version = getattr(module, "__version__", None)

    module_file = getattr(module, "__file__", None)
    if name == "pxr_usd":
        try:
            version = ".".join(str(part) for part in module.GetVersion())
            pxr_module = importlib.import_module("pxr")
            module_file = getattr(pxr_module, "__file__", module_file)
        except Exception as exc:
            return {
                "status": "import_error",
                "version": version,
                "file": module_file,
                "detail": f"{type(exc).__name__}: {exc}",
            }

    return {"status": "smoke_passed", "version": version, "file": module_file}


def usd_core_report():
    version = distribution_version("usd-core")
    status = "smoke_passed" if version else "dependency_gap"
    return {"status": status, "version": version, "file": None}


try:
    site_packages = site.getsitepackages()
except Exception:
    site_packages = []

payload = {
    "status": "smoke_passed",
    "executable": sys.executable,
    "realpath": str(Path(sys.executable).resolve()),
    "version": sys.version,
    "prefix": sys.prefix,
    "base_prefix": sys.base_prefix,
    "site_packages": site_packages,
    "usersite": site.getusersitepackages(),
    "sys_path": sys.path,
    "modules": {
        "newton": module_report("newton", "newton"),
        "warp": module_report("warp", "warp", "warp-lang"),
        "pxr_usd": module_report("pxr_usd", "pxr.Usd", "usd-core"),
        "usd_core": usd_core_report(),
    },
}
print(json.dumps(payload, sort_keys=True))
"""
