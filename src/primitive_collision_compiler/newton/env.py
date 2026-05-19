from __future__ import annotations

import ast
import importlib
import importlib.util
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


def inspect_newton_warp_provenance(
    source_dir: str | Path | None = None,
) -> dict[str, object]:
    source_path = None if source_dir in (None, "") else Path(str(source_dir))
    source_resolved = source_path.resolve() if source_path is not None else None
    original_path = list(sys.path)
    original_modules = _snapshot_runtime_modules(("newton", "warp"))
    _clear_runtime_modules(("newton", "warp"))
    inserted = False

    try:
        if source_path is None:
            rows = [
                _module_not_run_row(name, "not_run_source_dir_not_configured")
                for name in ("newton", "warp")
            ]
            source_status = "not_configured"
            probe_status = "not_run_source_dir_not_configured"
        elif not source_path.exists():
            rows = [
                _module_not_run_row(name, "not_run_source_dir_missing")
                for name in ("newton", "warp")
            ]
            source_status = "missing"
            probe_status = "not_run_source_dir_missing"
        else:
            sys.path.insert(0, str(source_path))
            inserted = True
            rows = [
                _module_find_spec_row(name, source_resolved)
                for name in ("newton", "warp")
            ]
            source_status = "found"
            probe_status = (
                "provenance_checked"
                if all(row["provenance_status"] == "found_within_source_dir" for row in rows)
                else "dependency_gap"
            )
    finally:
        if inserted:
            try:
                sys.path.remove(str(source_path))
            except ValueError:
                pass
        sys.path[:] = original_path
        _clear_runtime_modules(("newton", "warp"))
        sys.modules.update(original_modules)

    return {
        "probe_mode": "find_spec_provenance_only",
        "probe_status": probe_status,
        "source_dir_configured": source_path is not None,
        "source_dir": None if source_path is None else str(source_path),
        "source_dir_resolved": None if source_resolved is None else str(source_resolved),
        "source_dir_status": source_status,
        "source_commit": _git_commit(source_path) if source_path is not None else None,
        "module_probe_rows": rows,
        "module_probe_row_count": len(rows),
        "runtime_module_import_isolation_checked": True,
        "sys_path_restored": sys.path == original_path,
        "cached_runtime_modules_restored": _runtime_modules_restored(
            original_modules,
            ("newton", "warp"),
        ),
    }


def inspect_newton_engine_builder_api_surface(
    source_dir: str | Path | None = None,
) -> dict[str, object]:
    source_path = None if source_dir in (None, "") else Path(str(source_dir))
    source_resolved = source_path.resolve() if source_path is not None else None
    base = {
        "probe_mode": "source_ast_api_surface_only_no_import",
        "source_dir_configured": source_path is not None,
        "source_dir": None if source_path is None else str(source_path),
        "source_dir_resolved": None if source_resolved is None else str(source_resolved),
        "source_commit": None,
        "source_files_checked": [],
        "source_file_rows": [],
        "model_builder_exported_from_newton_init": False,
        "collision_pipeline_exported_from_newton_init": False,
        "model_builder_class_found": False,
        "model_builder_class_file": None,
        "model_builder_constructor_found": False,
        "model_builder_constructor_signature": {
            "parameters": [],
            "required_parameters": [],
            "defaults": {},
        },
        "add_shape_box_found": False,
        "add_shape_box_signature": {
            "parameters": [],
            "required_parameters": [],
            "planned_call_fields_present": [],
            "defaults": {},
        },
        "finalize_method_found": False,
        "collision_pipeline_symbol_found": False,
        "import_attempted": False,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_runtime_execution_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "real_usd_loaded": False,
        "benchmark_triggered": False,
        "collision_quality_measured": False,
        "claim_boundary": (
            "bounded_source_api_surface_probe_only_not_newton_runtime_execution"
        ),
    }

    if source_path is None:
        return {
            **base,
            "api_surface_status": "not_run_source_dir_not_configured",
            "source_dir_status": "not_configured",
        }
    if not source_path.exists():
        return {
            **base,
            "api_surface_status": "not_run_source_dir_missing",
            "source_dir_status": "missing",
        }

    init_rel = Path("newton") / "__init__.py"
    builder_rel = Path("newton") / "_src" / "sim" / "builder.py"
    init_row, init_tree = _parse_source_ast(source_path, init_rel)
    builder_row, builder_tree = _parse_source_ast(source_path, builder_rel)
    source_file_rows = [init_row, builder_row]
    checked_files = [
        str(row["relative_path"])
        for row in source_file_rows
        if row["parse_status"] == "parsed"
    ]

    model_builder_exported = (
        init_tree is not None and _module_exports_name(init_tree, "ModelBuilder")
    )
    collision_pipeline_exported = (
        init_tree is not None and _module_exports_name(init_tree, "CollisionPipeline")
    )
    model_builder_class = (
        _find_class_definition(builder_tree, "ModelBuilder")
        if builder_tree is not None
        else None
    )
    constructor = (
        _find_class_method(model_builder_class, "__init__")
        if model_builder_class is not None
        else None
    )
    add_shape_box = (
        _find_class_method(model_builder_class, "add_shape_box")
        if model_builder_class is not None
        else None
    )
    finalize = (
        _find_class_method(model_builder_class, "finalize")
        if model_builder_class is not None
        else None
    )
    planned_fields = ("body", "xform", "hx", "hy", "hz")
    add_shape_box_signature = _function_signature(add_shape_box)
    constructor_signature = _function_signature(constructor)
    add_shape_parameters = add_shape_box_signature["parameters"]
    api_surface_found = bool(
        model_builder_exported
        and model_builder_class is not None
        and add_shape_box is not None
        and all(field in add_shape_parameters for field in planned_fields)
    )

    return {
        **base,
        "api_surface_status": (
            "source_api_surface_checked"
            if api_surface_found
            else "source_api_surface_gap"
        ),
        "source_dir_status": "found",
        "source_files_checked": checked_files,
        "source_file_rows": source_file_rows,
        "model_builder_exported_from_newton_init": model_builder_exported,
        "collision_pipeline_exported_from_newton_init": collision_pipeline_exported,
        "model_builder_class_found": model_builder_class is not None,
        "model_builder_class_file": (
            str(builder_rel) if model_builder_class is not None else None
        ),
        "model_builder_constructor_found": constructor is not None,
        "model_builder_constructor_signature": constructor_signature,
        "add_shape_box_found": add_shape_box is not None,
        "add_shape_box_signature": {
            **add_shape_box_signature,
            "planned_call_fields_present": [
                field for field in planned_fields if field in add_shape_parameters
            ],
        },
        "finalize_method_found": finalize is not None,
        "collision_pipeline_symbol_found": collision_pipeline_exported,
    }


def _module_not_run_row(module_name: str, status: str) -> dict[str, object]:
    detail = (
        "newton.source_dir not configured for offline report"
        if status == "not_run_source_dir_not_configured"
        else "newton.source_dir does not exist"
    )
    return {
        "module_name": module_name,
        "module_available": False,
        "module_origin": None,
        "module_origin_resolved": None,
        "module_search_locations": [],
        "module_search_locations_resolved": [],
        "provenance_status": status,
        "provenance_detail": detail,
        "resolved_within_source_dir": False,
        "import_attempted": False,
    }


def _parse_source_ast(
    source_path: Path,
    relative_path: Path,
) -> tuple[dict[str, object], ast.Module | None]:
    path = source_path / relative_path
    row = {
        "relative_path": str(relative_path),
        "path": str(path),
        "path_resolved": str(path.resolve()),
        "file_exists": path.exists(),
        "parse_status": "missing",
        "parse_error": None,
        "import_attempted": False,
    }
    if not path.exists():
        return row, None
    try:
        source = path.read_text()
        tree = ast.parse(source)
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        return {
            **row,
            "parse_status": "parse_error",
            "parse_error": f"{type(exc).__name__}: {exc}",
        }, None
    return {**row, "parse_status": "parsed"}, tree


def _module_exports_name(tree: ast.Module, name: str) -> bool:
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            if any(alias.name == name for alias in node.names):
                return True
        if isinstance(node, ast.Assign):
            targets = [target.id for target in node.targets if isinstance(target, ast.Name)]
            if "__all__" in targets and _literal_list_contains(node.value, name):
                return True
    return False


def _literal_list_contains(node: ast.AST, value: str) -> bool:
    if isinstance(node, ast.List | ast.Tuple):
        return any(
            isinstance(element, ast.Constant) and element.value == value
            for element in node.elts
        )
    return False


def _find_class_definition(
    tree: ast.Module | None,
    class_name: str,
) -> ast.ClassDef | None:
    if tree is None:
        return None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    return None


def _find_class_method(
    class_node: ast.ClassDef | None,
    method_name: str,
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    if class_node is None:
        return None
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name == method_name:
            return node
    return None


def _function_signature(
    function: ast.FunctionDef | ast.AsyncFunctionDef | None,
) -> dict[str, object]:
    if function is None:
        return {"parameters": [], "required_parameters": [], "defaults": {}}
    positional = list(function.args.posonlyargs) + list(function.args.args)
    kwonly = list(function.args.kwonlyargs)
    parameters = [argument.arg for argument in positional + kwonly]
    defaults: dict[str, str] = {}
    positional_defaults = [None] * (
        len(positional) - len(function.args.defaults)
    ) + list(function.args.defaults)
    for argument, default in zip(positional, positional_defaults):
        if default is not None:
            defaults[argument.arg] = _ast_default_label(default)
    for argument, default in zip(kwonly, function.args.kw_defaults):
        if default is not None:
            defaults[argument.arg] = _ast_default_label(default)
    required_parameters = [
        argument.arg
        for argument, default in zip(positional, positional_defaults)
        if default is None
    ]
    required_parameters.extend(
        argument.arg
        for argument, default in zip(kwonly, function.args.kw_defaults)
        if default is None
    )
    return {
        "parameters": parameters,
        "required_parameters": required_parameters,
        "defaults": defaults,
    }


def _ast_default_label(node: ast.AST) -> str:
    if isinstance(node, ast.Constant):
        return repr(node.value)
    try:
        return ast.unparse(node)
    except AttributeError:
        return type(node).__name__


def _module_find_spec_row(
    module_name: str,
    source_resolved: Path | None,
) -> dict[str, object]:
    try:
        spec = importlib.util.find_spec(module_name)
    except (ImportError, AttributeError, ValueError) as exc:
        return {
            "module_name": module_name,
            "module_available": False,
            "module_origin": None,
            "module_origin_resolved": None,
            "module_search_locations": [],
            "module_search_locations_resolved": [],
            "provenance_status": "find_spec_error",
            "provenance_detail": f"{type(exc).__name__}: {exc}",
            "resolved_within_source_dir": False,
            "import_attempted": False,
        }

    if spec is None:
        return {
            "module_name": module_name,
            "module_available": False,
            "module_origin": None,
            "module_origin_resolved": None,
            "module_search_locations": [],
            "module_search_locations_resolved": [],
            "provenance_status": "module_not_found",
            "provenance_detail": f"{module_name} spec not found",
            "resolved_within_source_dir": False,
            "import_attempted": False,
        }

    origin = spec.origin
    origin_resolved = _resolve_optional_path(origin)
    locations = [str(path) for path in spec.submodule_search_locations or ()]
    locations_resolved = [
        str(Path(location).resolve()) for location in locations
    ]
    provenance_paths = [
        Path(path)
        for path in ([origin_resolved] if origin_resolved is not None else [])
        + locations_resolved
    ]
    within_source = bool(
        source_resolved is not None
        and provenance_paths
        and all(_is_relative_to(path, source_resolved) for path in provenance_paths)
    )
    return {
        "module_name": module_name,
        "module_available": True,
        "module_origin": origin,
        "module_origin_resolved": origin_resolved,
        "module_search_locations": locations,
        "module_search_locations_resolved": locations_resolved,
        "provenance_status": (
            "found_within_source_dir" if within_source else "found_outside_source_dir"
        ),
        "provenance_detail": (
            "module spec resolved within source_dir"
            if within_source
            else "module spec resolved outside source_dir"
        ),
        "resolved_within_source_dir": within_source,
        "import_attempted": False,
    }


def _resolve_optional_path(path: str | None) -> str | None:
    if not path or path in {"built-in", "frozen", "namespace"}:
        return None
    return str(Path(path).resolve())


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


def _snapshot_runtime_modules(roots: tuple[str, ...]) -> dict[str, object]:
    return {
        name: module
        for name, module in sys.modules.items()
        if any(name == root or name.startswith(f"{root}.") for root in roots)
    }


def _clear_newton_modules():
    for name in list(sys.modules):
        if name == "newton" or name.startswith("newton."):
            sys.modules.pop(name, None)


def _clear_runtime_modules(roots: tuple[str, ...]):
    for name in list(sys.modules):
        if any(name == root or name.startswith(f"{root}.") for root in roots):
            sys.modules.pop(name, None)


def _runtime_modules_restored(
    original_modules: dict[str, object],
    roots: tuple[str, ...],
) -> bool:
    current = _snapshot_runtime_modules(roots)
    return current == original_modules


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent)
    except ValueError:
        return False
    return True
