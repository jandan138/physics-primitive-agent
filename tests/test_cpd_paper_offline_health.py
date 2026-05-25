import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.paper_offline

MAX_TOPIC_TEST_FILE_LINES = 9000
SHARED_HELPERS = "cpd_paper_offline_shared.py"

ALLOWED_REPORT_BUILDER_FUNCTIONS = {
    "_cached_cpd_paper_offline_report_json",
    "_cached_independent_cpd_paper_offline_report_json_for_determinism_check",
}


def test_cpd_paper_offline_tests_are_split_by_topic():
    topic_files = _topic_test_paths()

    assert len(topic_files) >= 4
    oversized_files = {
        path.name: len(path.read_text(encoding="utf-8").splitlines())
        for path in topic_files
        if len(path.read_text(encoding="utf-8").splitlines()) > MAX_TOPIC_TEST_FILE_LINES
    }
    assert oversized_files == {}


def test_cpd_paper_offline_topic_tests_are_marked_for_paper_lane():
    unmarked_files = []
    for test_path in _topic_test_paths():
        tree = ast.parse(test_path.read_text(encoding="utf-8"))
        if not _module_has_pytestmark(tree, "paper_offline"):
            unmarked_files.append(test_path.name)

    assert unmarked_files == []


def test_cpd_paper_offline_tests_reuse_cached_report_builder():
    unexpected_call_lines = []
    for test_path in [*_topic_test_paths(), _shared_helper_path()]:
        tree = ast.parse(test_path.read_text(encoding="utf-8"))
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if node.name in ALLOWED_REPORT_BUILDER_FUNCTIONS:
                continue
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and _calls_report_builder(child):
                    unexpected_call_lines.append(f"{test_path.name}:{child.lineno}")

    assert unexpected_call_lines == []


def test_cpd_paper_offline_independent_build_is_confined_to_determinism_cache():
    test_path = _shared_helper_path()
    tree = ast.parse(test_path.read_text(encoding="utf-8"))

    builder_functions = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if any(
            isinstance(child, ast.Call) and _calls_report_builder(child) for child in ast.walk(node)
        ):
            builder_functions.append(node.name)

    assert set(builder_functions) == ALLOWED_REPORT_BUILDER_FUNCTIONS


def test_cpd_paper_report_fixture_returns_fresh_copy_from_cached_json():
    test_path = _shared_helper_path()
    tree = ast.parse(test_path.read_text(encoding="utf-8"))

    fresh_report_node = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "_fresh_cpd_paper_offline_report"
    )

    assert any(_calls_json_loads(child) for child in ast.walk(fresh_report_node))


def _topic_test_paths() -> list[Path]:
    return sorted(
        path
        for path in Path(__file__).parent.glob("test_cpd_paper_offline*.py")
        if path.name != "test_cpd_paper_offline_health.py"
    )


def _shared_helper_path() -> Path:
    return Path(__file__).with_name(SHARED_HELPERS)


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


def _module_has_pytestmark(tree: ast.Module, marker_name: str) -> bool:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets
        ):
            continue
        if _is_pytest_mark_attribute(node.value, marker_name):
            return True
    return False


def _is_pytest_mark_attribute(node: ast.AST, marker_name: str) -> bool:
    return (
        isinstance(node, ast.Attribute)
        and node.attr == marker_name
        and isinstance(node.value, ast.Attribute)
        and node.value.attr == "mark"
        and isinstance(node.value.value, ast.Name)
        and node.value.value.id == "pytest"
    )
