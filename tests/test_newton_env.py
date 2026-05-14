from pathlib import Path

from primitive_collision_compiler.newton.env import inspect_newton_environment


def test_inspect_newton_environment_reports_missing_source(tmp_path):
    missing = tmp_path / "missing-newton"

    report = inspect_newton_environment(missing)

    assert report.status == "missing_source"
    assert report.source_dir == str(missing)
    assert report.source_commit is None
    assert report.checks[0].name == "source_dir"


def test_inspect_newton_environment_records_git_commit_for_source_dir():
    source_dir = Path("/cpfs/user/zhuzihou/dev/newton")

    report = inspect_newton_environment(source_dir)

    assert report.stage == "newton_import"
    assert report.source_dir == str(source_dir)
    assert report.source_commit == "96713fa965463b69c229a4d30582c733ff3526bb"
    assert report.status in {"dependency_gap", "import_error", "smoke_passed"}
    assert any(check.name == "newton_import" for check in report.checks)
