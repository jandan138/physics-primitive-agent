import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.paper_offline

ALLOWED_REPORT_BUILDER_FUNCTIONS = {
    "_cached_cpd_paper_offline_report_json",
    "_cached_independent_cpd_paper_offline_report_json_for_determinism_check",
}


def test_cpd_paper_offline_tests_reuse_cached_report_builder():
    test_path = Path(__file__).with_name("test_cpd_paper_offline.py")
    tree = ast.parse(test_path.read_text(encoding="utf-8"))

    unexpected_call_lines = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name in ALLOWED_REPORT_BUILDER_FUNCTIONS:
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and _calls_report_builder(child):
                unexpected_call_lines.append(child.lineno)

    assert unexpected_call_lines == []


def test_cpd_paper_offline_independent_build_is_confined_to_determinism_cache():
    test_path = Path(__file__).with_name("test_cpd_paper_offline.py")
    tree = ast.parse(test_path.read_text(encoding="utf-8"))

    builder_functions = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if any(
            isinstance(child, ast.Call) and _calls_report_builder(child)
            for child in ast.walk(node)
        ):
            builder_functions.append(node.name)

    assert set(builder_functions) == ALLOWED_REPORT_BUILDER_FUNCTIONS


def test_cpd_paper_report_fixture_returns_fresh_copy_from_cached_json():
    test_path = Path(__file__).with_name("test_cpd_paper_offline.py")
    tree = ast.parse(test_path.read_text(encoding="utf-8"))

    fresh_report_node = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "_fresh_cpd_paper_offline_report"
    )

    assert any(_calls_json_loads(child) for child in ast.walk(fresh_report_node))


def _calls_report_builder(node: ast.Call) -> bool:
    if isinstance(node.func, ast.Name):
        return node.func.id == "build_cpd_paper_offline_report"
    if isinstance(node.func, ast.Attribute):
        return node.func.attr == "build_cpd_paper_offline_report"
    return False


def _calls_json_loads(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "json"
        and node.func.attr == "loads"
    )
