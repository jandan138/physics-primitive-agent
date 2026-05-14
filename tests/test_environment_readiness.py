import json
import os
import subprocess
import sys
from pathlib import Path

from primitive_collision_compiler.environment.readiness import (
    REQUIRED_ENV_VARS,
    build_configuration_report,
    inspect_newton_source,
    inspect_output_dir,
    inspect_python_environment,
    inspect_setup_script,
    pick_report_status,
    run_readiness_check,
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


def test_build_configuration_report_uses_contract_status_when_configured(tmp_path):
    report = build_configuration_report(
        {
            "NPC_ENV_ROOT": str(tmp_path),
            "NPC_PYTHON": sys.executable,
            "NPC_CODE_ROOT": str(tmp_path / "code"),
            "NEWTON_SOURCE_DIR": str(tmp_path / "newton"),
            "NPC_OUTPUT_DIR": str(tmp_path / "out"),
        }
    )

    assert report["status"] == "smoke_passed"


def test_inspect_python_environment_records_interpreter_identity():
    report = inspect_python_environment(sys.executable)

    assert report["status"] in {"smoke_passed", "dependency_gap", "import_error"}
    assert report["executable"] == sys.executable
    assert report["realpath"]
    assert report["version"].startswith(str(sys.version_info.major))
    assert isinstance(report["site_packages"], list)
    assert set(report["modules"]) == {"newton", "warp", "pxr_usd", "usd_core"}


def test_inspect_python_environment_does_not_inherit_pythonpath(tmp_path, monkeypatch):
    ambient_path = tmp_path / "ambient-leak"
    monkeypatch.setenv("PYTHONPATH", str(ambient_path))

    report = inspect_python_environment(sys.executable)

    assert str(ambient_path) not in report["sys_path"]


def test_inspect_python_environment_reports_missing_executable(tmp_path):
    missing_python = tmp_path / "missing-python"

    report = inspect_python_environment(str(missing_python))

    assert report["status"] == "configuration_error"
    assert "does not exist" in report["detail"]


def test_inspect_newton_source_reports_dependency_gap_for_missing_source(tmp_path):
    missing_source = tmp_path / "missing-newton"

    report = inspect_newton_source(str(missing_source))

    assert report["status"] == "dependency_gap"
    assert report["path"] == str(missing_source)
    assert report["exists"] is False


def test_inspect_output_dir_creates_and_fsyncs_tiny_probe(tmp_path):
    output_dir = tmp_path / "readiness-output"

    report = inspect_output_dir(str(output_dir))

    assert report["status"] == "smoke_passed"
    assert report["writable"] is True
    assert output_dir.exists()


def test_inspect_setup_script_records_hash_without_contents(tmp_path):
    setup_script = tmp_path / "setup.sh"
    setup_script.write_text("export TOKEN=secret\n", encoding="utf-8")

    report = inspect_setup_script(str(setup_script))

    assert report["status"] == "smoke_passed"
    assert report["sha256"]
    assert "TOKEN" not in str(report)
    assert "secret" not in str(report)


def test_run_readiness_check_combines_dependency_gap_status(tmp_path):
    output_dir = tmp_path / "out"
    env = {
        "NPC_ENV_ROOT": sys.prefix,
        "NPC_PYTHON": sys.executable,
        "NPC_CODE_ROOT": str(Path(__file__).resolve().parents[1]),
        "NEWTON_SOURCE_DIR": str(tmp_path / "missing-newton"),
        "NPC_OUTPUT_DIR": str(output_dir),
    }

    report = run_readiness_check(env)

    assert report["status"] == "dependency_gap"
    assert report["python"]["executable"] == sys.executable
    assert report["newton_source"]["status"] == "dependency_gap"
    assert report["output"]["status"] == "smoke_passed"


def test_readiness_script_writes_output_file(tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts" / "env" / "readiness_check.py"
    output_path = tmp_path / "readiness.json"
    env = {
        **os.environ,
        "NPC_ENV_ROOT": sys.prefix,
        "NPC_PYTHON": sys.executable,
        "NPC_CODE_ROOT": str(Path(__file__).resolve().parents[1]),
        "NEWTON_SOURCE_DIR": str(tmp_path / "missing-newton"),
        "NPC_OUTPUT_DIR": str(tmp_path / "out"),
    }

    result = subprocess.run(
        [sys.executable, str(script), "--output", str(output_path)],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 1
    stdout_report = json.loads(result.stdout)
    file_report = json.loads(output_path.read_text(encoding="utf-8"))
    assert stdout_report["stage"] == "environment_readiness"
    assert file_report["stage"] == "environment_readiness"
    assert file_report["status"] == "dependency_gap"
