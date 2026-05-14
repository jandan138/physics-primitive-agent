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
    source_resolved = source_path.resolve()
    original_modules = _snapshot_newton_modules()
    _clear_newton_modules()
    sys.path.insert(0, source_str)

    try:
        module = importlib.import_module("newton")
    except ModuleNotFoundError as exc:
        checks.append(EnvironmentCheck("newton_import", "dependency_gap", str(exc)))
        return "dependency_gap"
    except Exception as exc:
        checks.append(EnvironmentCheck("newton_import", "import_error", f"{type(exc).__name__}: {exc}"))
        return "import_error"
    else:
        module_file = getattr(module, "__file__", None)
        if not module_file or not _is_relative_to(Path(module_file), source_resolved):
            detail = f"newton resolved outside source_dir: {module_file}"
            checks.append(EnvironmentCheck("newton_import", "import_error", detail))
            return "import_error"

        checks.append(EnvironmentCheck("newton_import", "smoke_passed", "import newton succeeded"))
        return "smoke_passed"
    finally:
        try:
            sys.path.remove(source_str)
        except ValueError:
            pass
        _clear_newton_modules()
        sys.modules.update(original_modules)


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


def _snapshot_newton_modules() -> dict[str, object]:
    return {
        name: module
        for name, module in sys.modules.items()
        if name == "newton" or name.startswith("newton.")
    }


def _clear_newton_modules():
    for name in list(sys.modules):
        if name == "newton" or name.startswith("newton."):
            sys.modules.pop(name, None)


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent)
    except ValueError:
        return False
    return True
