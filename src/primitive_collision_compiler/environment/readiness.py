from __future__ import annotations

from datetime import datetime, timezone
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
