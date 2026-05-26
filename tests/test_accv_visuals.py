from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from primitive_collision_compiler.paper.accv_visuals import (
    PDF_METADATA,
    _load_mesh,
    _load_result_entry,
    _split_evidence_sources,
    _source_record_hashes,
    outcome_matrix,
    primitive_vertices,
    summarize_probe_outcomes,
)


def test_box_primitive_vertices_uses_center_and_half_extents() -> None:
    primitive = {
        "kind": "box",
        "center": [10.0, 20.0, 30.0],
        "dimensions": {"half_extents": [1.0, 2.0, 3.0]},
    }

    vertices = primitive_vertices(primitive)

    assert vertices.shape == (8, 3)
    np.testing.assert_allclose(vertices.min(axis=0), [9.0, 18.0, 27.0])
    np.testing.assert_allclose(vertices.max(axis=0), [11.0, 22.0, 33.0])


def test_convex_mesh_primitive_vertices_passes_report_vertices_through() -> None:
    primitive = {
        "kind": "convex_mesh",
        "dimensions": {"vertices": [[0, 0, 0], [1, 2, 3], [-1, 0, 4]]},
    }

    vertices = primitive_vertices(primitive)

    assert vertices.shape == (3, 3)
    np.testing.assert_allclose(vertices[1], [1, 2, 3])


def test_unknown_primitive_kind_returns_empty_vertices() -> None:
    vertices = primitive_vertices({"kind": "capsule", "dimensions": {"radius": 1.0}})

    assert vertices.shape == (0, 3)


def test_outcome_matrix_and_summary_count_selected_probe_outcomes() -> None:
    report = {
        "cases": [
            {
                "asset_role": "container",
                "asset_id": "grscenes_bowl_fixture",
                "probe_results": {
                    "bounding_primitive": {
                        "contact_canary": {"outcome": "accept"},
                        "body_state_drop_settle": {"outcome": "accept"},
                        "stack_or_slide": {"outcome": "failure"},
                        "sphere_rain": {"outcome": "accept"},
                    },
                    "cpd_style_primitive_candidate_if_available": {
                        "contact_canary": {"outcome": "accept"},
                        "body_state_drop_settle": {"outcome": "failure"},
                        "stack_or_slide": {"outcome": "failure"},
                    },
                    "coacd_or_vhacd_if_available": {
                        "contact_canary": {"outcome": "accept"},
                        "body_state_drop_settle": {"outcome": "fallback"},
                        "stack_or_slide": {"outcome": "fallback"},
                        "sphere_rain": {"outcome": "accept"},
                    },
                    "single_convex_hull": {
                        "contact_canary": {"outcome": "fallback"},
                        "body_state_drop_settle": {"outcome": "fallback"},
                        "stack_or_slide": {"outcome": "fallback"},
                        "sphere_rain": {"outcome": "fallback"},
                    },
                    "vhacd_if_available": {
                        "contact_canary": {"outcome": "accept"},
                        "body_state_drop_settle": {"outcome": "failure"},
                        "stack_or_slide": {"outcome": "failure"},
                        "sphere_rain": {"outcome": "accept"},
                    },
                },
            }
        ]
    }

    rows, columns, matrix = outcome_matrix(report)
    summary = summarize_probe_outcomes(report)

    assert rows == ["container\nbowl"]
    assert len(columns) == 20
    assert matrix.shape == (1, 20)
    assert summary["accept"] == 8
    assert summary["failure"] == 5
    assert summary["fallback"] == 6
    assert summary["not_applicable"] == 1


def test_load_mesh_failure_is_not_silent(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="failed to load source mesh"):
        _load_mesh(tmp_path / "missing.usd", max_faces=1)


def test_mechanism_result_entry_is_structured_for_figure_generation() -> None:
    entry = _load_result_entry("bed_franka_cylinder_mechanism")
    metrics = entry["metrics"]

    assert metrics["bed_final_speed_mps"] == pytest.approx(0.082304)
    assert metrics["franka_final_speed_mps"] == pytest.approx(0.0007108)
    assert metrics["settle_gate_mps"] == pytest.approx(0.05)
    assert len(metrics["audit_rows"]) == 5


def test_manifest_helpers_keep_source_records_and_pdf_metadata_stable() -> None:
    records = _split_evidence_sources("a.md; b.md; ; c.md")

    assert records == ("a.md", "b.md", "c.md")
    assert PDF_METADATA["Creator"] == "primitive_collision_compiler.paper.accv_visuals"
    assert PDF_METADATA["CreationDate"] == PDF_METADATA["ModDate"]


def test_source_record_hashes_fail_closed_for_missing_records() -> None:
    with pytest.raises(RuntimeError, match="missing source record"):
        _source_record_hashes(("docs/records/does-not-exist.md",))
