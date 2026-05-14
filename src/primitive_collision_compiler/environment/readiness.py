from __future__ import annotations

import json
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


def pick_report_status(statuses: list[str] | tuple[str, ...]) -> str:
    if not statuses:
        return "smoke_passed"
    return max(statuses, key=lambda status: _STATUS_ORDER.get(status, _STATUS_ORDER["runtime_failure"]))


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


def run_readiness_check(env: Mapping[str, str], *, scope: str = "local") -> dict[str, object]:
    return build_configuration_report(env, scope=scope)


def inspect_python_environment(python_executable: str) -> dict[str, object]:
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
    payload["status"] = pick_report_status(
        [module.get("status", "runtime_failure") for module in modules.values()]
    )
    return payload


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
        return {
            "status": "dependency_gap",
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
