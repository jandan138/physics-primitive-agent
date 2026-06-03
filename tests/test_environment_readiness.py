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


def _commit_git_fixture(path: Path) -> str:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True, text=True)
    (path / "README.md").write_text("fixture\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True, capture_output=True, text=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=test@example.com",
            "-c",
            "user.name=Test User",
            "commit",
            "-m",
            "init",
        ],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    )
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


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
    code_root = tmp_path / "code"
    code_root.mkdir()
    report = build_configuration_report(
        {
            "NPC_ENV_ROOT": str(tmp_path),
            "NPC_PYTHON": sys.executable,
            "NPC_CODE_ROOT": str(code_root),
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


def test_inspect_python_environment_enforces_env_root_alignment(tmp_path):
    report = inspect_python_environment(sys.executable, env_root=str(tmp_path / "wrong-env-root"))

    assert report["status"] == "configuration_error"
    assert report["environment_alignment"]["status"] == "configuration_error"


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


def test_inspect_newton_source_reports_dirty_checkout_as_configuration_error(tmp_path):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    _commit_git_fixture(source_dir)
    (source_dir / "dirty.txt").write_text("untracked\n", encoding="utf-8")

    report = inspect_newton_source(str(source_dir))

    assert report["status"] == "configuration_error"
    assert report["dirty"] is True


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

    assert report["status"] in {"dependency_gap", "import_error"}
    assert report["python"]["executable"] == sys.executable
    assert report["newton_source"]["status"] == "dependency_gap"
    assert report["output"]["status"] == "smoke_passed"
    if report["status"] == "import_error":
        assert report["modules"]["newton"]["status"] == "import_error"
        assert "outside NEWTON_SOURCE_DIR" in report["modules"]["newton"]["detail"]


def test_run_readiness_check_reports_invalid_code_root_as_configuration_error(tmp_path):
    env = {
        "NPC_ENV_ROOT": sys.prefix,
        "NPC_PYTHON": sys.executable,
        "NPC_CODE_ROOT": str(tmp_path / "missing-code-root"),
        "NEWTON_SOURCE_DIR": str(tmp_path / "missing-newton"),
        "NPC_OUTPUT_DIR": str(tmp_path / "out"),
    }

    report = run_readiness_check(env)

    assert report["status"] == "configuration_error"
    assert any(
        check["name"] == "NPC_CODE_ROOT" and check["status"] == "configuration_error"
        for check in report["checks"]
    )


def test_run_readiness_check_uses_newton_source_dir_for_repository_diagnostic(tmp_path):
    newton_source = tmp_path / "alternate-newton"
    env = {
        "NPC_ENV_ROOT": sys.prefix,
        "NPC_PYTHON": sys.executable,
        "NPC_CODE_ROOT": str(Path(__file__).resolve().parents[1]),
        "NEWTON_SOURCE_DIR": str(newton_source),
        "NPC_OUTPUT_DIR": str(tmp_path / "out"),
    }

    report = run_readiness_check(env)

    diagnostic_payload = report["repository_diagnostics"]["check_newton"]["payload"]
    assert diagnostic_payload["source_dir"] == str(newton_source)


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
    assert file_report["status"] in {"dependency_gap", "import_error"}
    if file_report["status"] == "import_error":
        assert file_report["modules"]["newton"]["status"] == "import_error"
        assert "outside NEWTON_SOURCE_DIR" in file_report["modules"]["newton"]["detail"]


def test_readiness_script_reports_output_write_failure_as_json(tmp_path):
    script = Path(__file__).resolve().parents[1] / "scripts" / "env" / "readiness_check.py"
    file_parent = tmp_path / "not-a-directory"
    file_parent.write_text("blocks directory creation\n", encoding="utf-8")
    output_path = file_parent / "readiness.json"
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
    report = json.loads(result.stdout)
    assert report["report_output"]["status"] == "runtime_failure"
    assert "Traceback" not in result.stderr
