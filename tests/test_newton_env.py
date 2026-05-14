from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

from primitive_collision_compiler.newton.env import inspect_newton_environment


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


def test_inspect_newton_environment_reports_missing_source(tmp_path):
    missing = tmp_path / "missing-newton"

    report = inspect_newton_environment(missing)

    assert report.status == "missing_source"
    assert report.source_dir == str(missing)
    assert report.source_commit is None
    assert report.checks[0].name == "source_dir"


def test_inspect_newton_environment_records_git_commit_for_source_dir(tmp_path):
    source_dir = tmp_path / "newton-source"
    source_dir.mkdir()
    source_commit = _commit_git_fixture(source_dir)

    report = inspect_newton_environment(source_dir)

    assert report.stage == "newton_import"
    assert report.source_dir == str(source_dir)
    assert report.source_commit == source_commit
    assert report.status == "dependency_gap"
    assert any(check.name == "newton_import" for check in report.checks)


def test_inspect_newton_environment_ignores_cached_newton_from_other_source(tmp_path):
    cached_source = tmp_path / "cached-source"
    cached_package = cached_source / "newton"
    cached_package.mkdir(parents=True)
    (cached_package / "__init__.py").write_text("VALUE = 'cached'\n", encoding="utf-8")
    _commit_git_fixture(cached_source)

    inspected_source = tmp_path / "inspected-source"
    inspected_source.mkdir()
    _commit_git_fixture(inspected_source)

    sys.path.insert(0, str(cached_source))
    try:
        cached_module = importlib.import_module("newton")
        assert str(cached_source) in str(cached_module.__file__)

        report = inspect_newton_environment(inspected_source)
    finally:
        try:
            sys.path.remove(str(cached_source))
        except ValueError:
            pass
        sys.modules.pop("newton", None)

    assert report.status == "import_error"
    assert any("resolved outside source_dir" in check.detail for check in report.checks)
