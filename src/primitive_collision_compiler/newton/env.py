from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

from primitive_collision_compiler.reports.schema import EnvironmentCheck, EnvironmentReport


def inspect_newton_environment(source_dir: str | Path) -> EnvironmentReport:
    source_path = Path(source_dir)
    if not source_path.exists():
        return EnvironmentReport(
            stage="newton_import",
            status="missing_source",
            source_dir=str(source_path),
            source_commit=None,
            checks=(EnvironmentCheck("source_dir", "missing_source", "path does not exist"),),
        )

    source_commit = _git_commit(source_path)
    checks = [EnvironmentCheck("source_dir", "found", "path exists")]
    status = _inspect_import(source_path, checks)

    return EnvironmentReport(
        stage="newton_import",
        status=status,
        source_dir=str(source_path),
        source_commit=source_commit,
        checks=tuple(checks),
    )


def _inspect_import(source_path: Path, checks: list[EnvironmentCheck]) -> str:
    source_str = str(source_path)
    inserted = source_str not in sys.path
    had_newton = "newton" in sys.modules
    if inserted:
        sys.path.insert(0, source_str)

    try:
        importlib.import_module("newton")
    except ModuleNotFoundError as exc:
        checks.append(EnvironmentCheck("newton_import", "dependency_gap", str(exc)))
        if not had_newton:
            sys.modules.pop("newton", None)
        return "dependency_gap"
    except Exception as exc:
        checks.append(EnvironmentCheck("newton_import", "import_error", f"{type(exc).__name__}: {exc}"))
        if not had_newton:
            sys.modules.pop("newton", None)
        return "import_error"
    finally:
        if inserted:
            try:
                sys.path.remove(source_str)
            except ValueError:
                pass

    checks.append(EnvironmentCheck("newton_import", "smoke_passed", "import newton succeeded"))
    return "smoke_passed"


def _git_commit(source_path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(source_path), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None
