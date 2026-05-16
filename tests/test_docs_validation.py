from pathlib import Path

from scripts.validate_docs import (
    find_claim_boundary_issues,
    validate_local_markdown_links,
    validate_registry_records,
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
    assert any("AGENTS.md" in issue for issue in issues)
    assert any("assets/manifests/phase0_assets.yaml" in issue for issue in issues)


def test_local_markdown_link_validation_flags_missing_target(tmp_path: Path):
    doc = tmp_path / "docs" / "index.md"
    doc.parent.mkdir()
    doc.write_text("[Missing](missing.md)\n", encoding="utf-8")

    issues = validate_local_markdown_links(tmp_path, [doc])

    assert issues == ["docs/index.md:1: missing local link target: missing.md"]


def test_registry_validation_flags_missing_record_target(tmp_path: Path):
    registry = tmp_path / "experiments" / "registry.yaml"
    registry.parent.mkdir()
    registry.write_text(
        "\n".join(
            [
                "experiments:",
                "  - id: missing-record",
                "    status: complete",
                "    record: docs/records/missing.md",
                "    claims_supported:",
                "      - toy fixture audit only",
                "      - no benchmark claim",
            ]
        ),
        encoding="utf-8",
    )

    issues = validate_registry_records(tmp_path)

    assert issues == [
        "experiments/registry.yaml: missing-record: missing record target: docs/records/missing.md"
    ]


def test_registry_validation_flags_complete_entry_without_complete_record(tmp_path: Path):
    record = tmp_path / "docs" / "records" / "record.md"
    record.parent.mkdir(parents=True)
    record.write_text("# Record\n\n## Status\n\nIn progress\n", encoding="utf-8")
    registry = tmp_path / "experiments" / "registry.yaml"
    registry.parent.mkdir()
    registry.write_text(
        "\n".join(
            [
                "experiments:",
                "  - id: stale-record-status",
                "    status: complete",
                "    record: docs/records/record.md",
                "    claims_supported:",
                "      - toy fixture audit only",
                "      - no benchmark claim",
            ]
        ),
        encoding="utf-8",
    )

    issues = validate_registry_records(tmp_path)

    assert issues == [
        "experiments/registry.yaml: stale-record-status: complete registry entry points to non-complete record: docs/records/record.md"
    ]
