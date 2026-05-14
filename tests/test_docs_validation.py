from pathlib import Path

from scripts.validate_docs import (
    find_claim_boundary_issues,
    validate_local_markdown_links,
    validate_required_paths,
)


def test_claim_boundary_lint_flags_unscoped_guarantee():
    issues = find_claim_boundary_issues("This system guarantees real-world safety.")

    assert issues
    assert issues[0].term == "guarantees"


def test_claim_boundary_lint_allows_guardrail_language():
    text = "Do not claim this system guarantees real-world safety."

    assert find_claim_boundary_issues(text) == []


def test_required_path_validation_flags_missing_reference_docs(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Test Repo\n", encoding="utf-8")

    issues = validate_required_paths(tmp_path)

    assert any("docs/reference/claim-boundaries.md" in issue for issue in issues)


def test_local_markdown_link_validation_flags_missing_target(tmp_path: Path):
    doc = tmp_path / "docs" / "index.md"
    doc.parent.mkdir()
    doc.write_text("[Missing](missing.md)\n", encoding="utf-8")

    issues = validate_local_markdown_links(tmp_path, [doc])

    assert issues == ["docs/index.md:1: missing local link target: missing.md"]
