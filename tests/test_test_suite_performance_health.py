import ast
from pathlib import Path


def test_newton_native_fitting_tests_do_not_rebuild_report_per_case():
    checked_files = (
        Path(__file__).with_name("test_cpd_like_synthetic.py"),
        Path(__file__).with_name("test_cli.py"),
    )

    direct_call_lines = []
    for test_path in checked_files:
        tree = ast.parse(test_path.read_text(encoding="utf-8"))
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if node.name == "_cached_newton_native_fitting_comparison_report":
                continue
            if node.name == "_cached_custom_legacy_newton_native_fitting_comparison_report":
                continue
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and _calls_newton_native_report_builder(child):
                    direct_call_lines.append(f"{test_path.name}:{child.lineno}")

    assert direct_call_lines == []


def test_newton_native_fitting_cli_tests_stub_expensive_builder():
    test_path = Path(__file__).with_name("test_cli.py")
    tree = ast.parse(test_path.read_text(encoding="utf-8"))

    unstubbed_tests = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_contains_string(node, "--run-newton-native-fitting-comparison"):
            continue
        arg_names = {arg.arg for arg in node.args.args}
        if "monkeypatch" not in arg_names:
            unstubbed_tests.append(node.name)

    assert unstubbed_tests == []


def test_cpd_paper_offline_cli_real_report_tests_are_in_paper_lane():
    test_path = Path(__file__).with_name("test_cli.py")
    tree = ast.parse(test_path.read_text(encoding="utf-8"))

    unmarked_real_report_tests = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_contains_string(node, "--run-cpd-paper-offline-report"):
            continue
        if _function_stubs_builder(node, "build_cpd_paper_offline_report"):
            continue
        if not _function_has_pytest_marker(node, "paper_offline"):
            unmarked_real_report_tests.append(node.name)

    assert unmarked_real_report_tests == []


def _calls_newton_native_report_builder(node: ast.Call) -> bool:
    if isinstance(node.func, ast.Name):
        return node.func.id == "build_newton_native_fitting_comparison_report"
    if isinstance(node.func, ast.Attribute):
        return node.func.attr == "build_newton_native_fitting_comparison_report"
    return False


def _function_contains_string(node: ast.FunctionDef, value: str) -> bool:
    return any(
        isinstance(child, ast.Constant) and child.value == value
        for child in ast.walk(node)
    )


def _function_stubs_builder(node: ast.FunctionDef, builder_name: str) -> bool:
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        if not isinstance(child.func, ast.Attribute):
            continue
        if child.func.attr != "setattr":
            continue
        if not isinstance(child.func.value, ast.Name):
            continue
        if child.func.value.id != "monkeypatch":
            continue
        if any(
            arg.value == builder_name
            for arg in child.args
            if isinstance(arg, ast.Constant)
        ):
            return True
    return False


def _function_has_pytest_marker(node: ast.FunctionDef, marker_name: str) -> bool:
    return any(
        _decorator_is_pytest_marker(decorator, marker_name)
        for decorator in node.decorator_list
    )


def _decorator_is_pytest_marker(decorator: ast.expr, marker_name: str) -> bool:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    return (
        isinstance(target, ast.Attribute)
        and target.attr == marker_name
        and isinstance(target.value, ast.Attribute)
        and target.value.attr == "mark"
        and isinstance(target.value.value, ast.Name)
        and target.value.value.id == "pytest"
    )
