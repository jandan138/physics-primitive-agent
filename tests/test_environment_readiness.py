import sys

from primitive_collision_compiler.environment.readiness import (
    REQUIRED_ENV_VARS,
    build_configuration_report,
    inspect_python_environment,
    pick_report_status,
)


def test_required_env_vars_are_the_phase1_contract():
    assert REQUIRED_ENV_VARS == (
        "NPC_ENV_ROOT",
        "NPC_PYTHON",
        "NPC_CODE_ROOT",
        "NEWTON_SOURCE_DIR",
        "NPC_OUTPUT_DIR",
    )


def test_pick_report_status_uses_readiness_precedence():
    assert pick_report_status(["smoke_passed", "dependency_gap"]) == "dependency_gap"
    assert pick_report_status(["dependency_gap", "import_error"]) == "import_error"
    assert pick_report_status(["runtime_failure", "import_error"]) == "runtime_failure"
    assert pick_report_status(["configuration_error", "runtime_failure"]) == "configuration_error"
    assert pick_report_status(["smoke_passed", "smoke_passed"]) == "smoke_passed"


def test_build_configuration_report_preserves_top_level_shape():
    report = build_configuration_report({"NPC_PYTHON": "/usr/bin/python"})

    assert report["stage"] == "environment_readiness"
    assert report["status"] == "configuration_error"
    assert report["scope"] == "local"
    assert "checks" in report
    assert "python" in report
    assert "modules" in report
    assert "newton_source" in report
    assert "gpu" in report
    assert "output" in report
    assert "repository_diagnostics" in report
    assert sorted(
        check["name"] for check in report["checks"] if check["status"] == "configuration_error"
    ) == [
        "NEWTON_SOURCE_DIR",
        "NPC_CODE_ROOT",
        "NPC_ENV_ROOT",
        "NPC_OUTPUT_DIR",
    ]


def test_inspect_python_environment_records_interpreter_identity():
    report = inspect_python_environment(sys.executable)

    assert report["status"] in {"smoke_passed", "dependency_gap", "import_error"}
    assert report["executable"] == sys.executable
    assert report["realpath"]
    assert report["version"].startswith(str(sys.version_info.major))
    assert isinstance(report["site_packages"], list)
    assert set(report["modules"]) == {"newton", "warp", "pxr_usd", "usd_core"}


def test_inspect_python_environment_reports_missing_executable(tmp_path):
    missing_python = tmp_path / "missing-python"

    report = inspect_python_environment(str(missing_python))

    assert report["status"] == "configuration_error"
    assert "does not exist" in report["detail"]
