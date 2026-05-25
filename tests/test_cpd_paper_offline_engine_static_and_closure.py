import pytest

from tests.cpd_paper_offline_shared import *

pytestmark = pytest.mark.paper_offline


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    ]
    runtime_execution = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    ]
    source_row = runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_PAYLOAD_REQUIRED_KEYS
    )
    assert "runtime_lane_review_passed_count" not in payload
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_runtime_lane_review_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_runtime_lane_review_recorded_"
        "configured_runtime_design_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_runtime_lane_review_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_runtime_lane_review_contract_"
        "no_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["runtime_lane_review_action"] == (
        "record_claim_boundary_review_for_single_synthetic_box_runtime_lane"
    )
    assert payload["runtime_lane_review_decision"] == "keep_real_runtime_execution_blocked"
    assert payload["runtime_lane_review_status"] == "claim_boundary_preserved"
    assert payload["runtime_lane_review_reason"] == (
        "skipped_runtime_execution_is_not_runtime_compatibility"
    )
    assert payload["runtime_lane_review_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
        ),
        "next_configured_runtime_design_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
        ),
        "runtime_execution_decision_required": "skip_real_runtime_execution",
        "runtime_lane_review_decision": "keep_real_runtime_execution_blocked",
        "runtime_lane_claim_boundary_preserved": True,
        "real_runtime_execution_evidence": False,
        "runtime_compatibility_validated": False,
        "configured_runtime_design_ready": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_runtime_execution_row_id": source_row[
            "newton_shape_runtime_engine_builder_runtime_execution_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_smoke_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_smoke_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_entry_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_entry_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_api_surface_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_api_surface_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_environment_probe_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_environment_probe_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_runtime_execution_decision": "skip_real_runtime_execution",
        "source_runtime_execution_result_status": ("not_run_default_no_runtime_smoke"),
    }
    assert payload["newton_shape_runtime_engine_builder_runtime_lane_review_row_count"] == 1
    assert payload["source_newton_shape_runtime_engine_builder_runtime_execution_row_count"] == 1
    assert payload["runtime_execution_allowed_count"] == 0
    assert payload["runtime_execution_attempted_count"] == 0
    assert payload["runtime_execution_passed_count"] == 0
    assert payload["runtime_lane_review_recorded_count"] == 1
    assert payload["runtime_lane_claim_boundary_preserved_count"] == 1
    assert payload["real_runtime_execution_evidence_count"] == 0
    assert payload["runtime_compatibility_validated_count"] == 0
    assert payload["real_runtime_execution_evidence"] is False
    assert payload["runtime_compatibility_validated"] is False
    assert payload["configured_runtime_design_ready"] is False
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_runtime_lane_review_row_count": 1,
        "source_newton_shape_runtime_engine_builder_runtime_execution_row_count": 1,
        "runtime_execution_allowed_count": 0,
        "runtime_execution_attempted_count": 0,
        "runtime_execution_passed_count": 0,
        "runtime_lane_review_recorded_count": 1,
        "runtime_lane_claim_boundary_preserved_count": 1,
        "real_runtime_execution_evidence_count": 0,
        "runtime_compatibility_validated_count": 0,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "runtime_lane_review_decision_distribution": {"keep_real_runtime_execution_blocked": 1},
        "runtime_lane_review_status_distribution": {"claim_boundary_preserved": 1},
    }
    assert payload["newton_shape_runtime_engine_builder_runtime_lane_review_rows"] == [
        {
            "newton_shape_runtime_engine_builder_runtime_lane_review_row_id": (
                "newton_shape_runtime_engine_builder_runtime_lane_review__paper_single_box__box"
            ),
            "source_newton_shape_runtime_engine_builder_runtime_execution_row_id": source_row[
                "newton_shape_runtime_engine_builder_runtime_execution_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_smoke_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_smoke_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_entry_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_entry_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_api_surface_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_api_surface_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_environment_probe_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_environment_probe_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"
            ],
            "source_newton_shape_runtime_builder_construction_row_id": source_row[
                "source_newton_shape_runtime_builder_construction_row_id"
            ],
            "source_newton_shape_runtime_builder_preflight_row_id": source_row[
                "source_newton_shape_runtime_builder_preflight_row_id"
            ],
            "source_newton_shape_runtime_construction_row_id": source_row[
                "source_newton_shape_runtime_construction_row_id"
            ],
            "source_newton_shape_runtime_boundary_preflight_row_id": source_row[
                "source_newton_shape_runtime_boundary_preflight_row_id"
            ],
            "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
            "source_newton_shape_mapping_preflight_row_id": source_row[
                "source_newton_shape_mapping_preflight_row_id"
            ],
            "source_runtime_admissibility_row_id": source_row[
                "source_runtime_admissibility_row_id"
            ],
            "source_package_id": source_row["source_package_id"],
            "source_asset_id": source_row["source_asset_id"],
            "fixture_id": "paper_single_box",
            "paper_primitive": "oriented_bounding_box",
            "primitive_spec_kind": "box",
            "primitive_id": source_row["primitive_id"],
            "target_newton_shape_kind": "box",
            "future_newton_builder_constructor_name": "newton.ModelBuilder",
            "future_newton_builder_method_name": "add_shape_box",
            "future_runtime_module_names": ["newton", "warp"],
            "api_surface_probe_status": "not_run_source_dir_not_configured",
            "entry_decision": "defer_real_runtime_entry",
            "smoke_decision": "skip_real_runtime_smoke",
            "runtime_smoke_result_status": "not_run_default_no_runtime_entry",
            "runtime_execution_decision": "skip_real_runtime_execution",
            "runtime_execution_decision_reason": ("default_no_runtime_smoke_decision_preserved"),
            "runtime_execution_allowed": False,
            "runtime_execution_attempted": False,
            "runtime_execution_passed": False,
            "runtime_execution_result_status": ("not_run_default_no_runtime_smoke"),
            "runtime_lane_review_decision": ("keep_real_runtime_execution_blocked"),
            "runtime_lane_review_reason": (
                "skipped_runtime_execution_is_not_runtime_compatibility"
            ),
            "runtime_lane_review_status": "claim_boundary_preserved",
            "runtime_lane_review_recorded": True,
            "runtime_lane_claim_boundary_preserved": True,
            "configured_runtime_design_gate_required": (
                EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
            ),
            "real_runtime_execution_evidence": False,
            "runtime_compatibility_validated": False,
            "configured_runtime_design_ready": False,
            "source_package_copy_forbidden": True,
            "real_newton_import_count": 0,
            "real_warp_import_count": 0,
            "newton_model_builder_instantiated_count": 0,
            "newton_engine_shape_object_count": 0,
            "newton_builder_shape_call_count": 0,
            "newton_model_finalized_count": 0,
            "newton_collision_pipeline_created_count": 0,
            "newton_collision_pipeline_collide_count": 0,
            "newton_runtime_execution_count": 0,
        }
    ]
    assert (
        set(payload["newton_shape_runtime_engine_builder_runtime_lane_review_rows"][0])
        == NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_ROW_REQUIRED_KEYS
    )
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_REMAINING_GAPS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    ]
    smoke = report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"]
    source_row = smoke["newton_shape_runtime_engine_builder_smoke_rows"][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_runtime_execution_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_runtime_execution_decision_recorded_"
        "runtime_lane_review_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_runtime_execution_decision_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_runtime_execution_contract_"
        "no_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["runtime_execution_action"] == (
        "record_default_no_runtime_execution_decision_for_single_synthetic_box"
    )
    assert payload["runtime_execution_decision"] == ("skip_real_runtime_execution")
    assert payload["runtime_execution_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
        ),
        "next_runtime_lane_review_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
        ),
        "source_smoke_rows_required": 1,
        "smoke_decision_required": "skip_real_runtime_smoke",
        "runtime_execution_decision": "skip_real_runtime_execution",
        "runtime_execution_allowed": False,
        "runtime_execution_attempted": False,
        "runtime_execution_passed": False,
        "real_runtime_import_allowed": False,
        "newton_model_builder_allowed": False,
        "newton_engine_shape_object_allowed": False,
        "newton_builder_shape_call_allowed": False,
        "newton_model_finalize_allowed": False,
        "newton_collision_pipeline_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_smoke_row_id": source_row[
            "newton_shape_runtime_engine_builder_smoke_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_entry_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_entry_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_api_surface_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_api_surface_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_environment_probe_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_environment_probe_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_smoke_decision": "skip_real_runtime_smoke",
        "source_runtime_smoke_result_status": ("not_run_default_no_runtime_entry"),
    }
    assert payload["newton_shape_runtime_engine_builder_runtime_execution_row_count"] == 1
    assert payload["source_newton_shape_runtime_engine_builder_smoke_row_count"] == 1
    assert payload["runtime_execution_allowed_count"] == 0
    assert payload["runtime_execution_attempted_count"] == 0
    assert payload["runtime_execution_passed_count"] == 0
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_REMAINING_GAPS
    )
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_runtime_execution_row_count": 1,
        "source_newton_shape_runtime_engine_builder_smoke_row_count": 1,
        "runtime_execution_allowed_count": 0,
        "runtime_execution_attempted_count": 0,
        "runtime_execution_passed_count": 0,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "runtime_execution_decision_distribution": {"skip_real_runtime_execution": 1},
        "runtime_execution_result_status_distribution": {"not_run_default_no_runtime_smoke": 1},
    }
    assert payload["newton_shape_runtime_engine_builder_runtime_execution_rows"] == [
        {
            "newton_shape_runtime_engine_builder_runtime_execution_row_id": (
                "newton_shape_runtime_engine_builder_runtime_execution__paper_single_box__box"
            ),
            "source_newton_shape_runtime_engine_builder_smoke_row_id": source_row[
                "newton_shape_runtime_engine_builder_smoke_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_entry_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_entry_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_api_surface_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_api_surface_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_environment_probe_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_environment_probe_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"
            ],
            "source_newton_shape_runtime_builder_construction_row_id": source_row[
                "source_newton_shape_runtime_builder_construction_row_id"
            ],
            "source_newton_shape_runtime_builder_preflight_row_id": source_row[
                "source_newton_shape_runtime_builder_preflight_row_id"
            ],
            "source_newton_shape_runtime_construction_row_id": source_row[
                "source_newton_shape_runtime_construction_row_id"
            ],
            "source_newton_shape_runtime_boundary_preflight_row_id": source_row[
                "source_newton_shape_runtime_boundary_preflight_row_id"
            ],
            "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
            "source_newton_shape_mapping_preflight_row_id": source_row[
                "source_newton_shape_mapping_preflight_row_id"
            ],
            "source_runtime_admissibility_row_id": source_row[
                "source_runtime_admissibility_row_id"
            ],
            "source_package_id": source_row["source_package_id"],
            "source_asset_id": source_row["source_asset_id"],
            "fixture_id": "paper_single_box",
            "paper_primitive": "oriented_bounding_box",
            "primitive_spec_kind": "box",
            "primitive_id": source_row["primitive_id"],
            "target_newton_shape_kind": "box",
            "future_newton_builder_constructor_name": "newton.ModelBuilder",
            "future_newton_builder_method_name": "add_shape_box",
            "future_runtime_module_names": ["newton", "warp"],
            "api_surface_probe_status": "not_run_source_dir_not_configured",
            "entry_decision": "defer_real_runtime_entry",
            "smoke_decision": "skip_real_runtime_smoke",
            "runtime_smoke_result_status": ("not_run_default_no_runtime_entry"),
            "runtime_execution_decision": "skip_real_runtime_execution",
            "runtime_execution_decision_reason": ("default_no_runtime_smoke_decision_preserved"),
            "runtime_execution_allowed": False,
            "runtime_execution_attempted": False,
            "runtime_execution_passed": False,
            "runtime_execution_result_status": ("not_run_default_no_runtime_smoke"),
            "runtime_lane_review_gate_required": (
                EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
            ),
            "source_package_copy_forbidden": True,
            "real_newton_import_count": 0,
            "real_warp_import_count": 0,
            "newton_model_builder_instantiated_count": 0,
            "newton_builder_shape_call_count": 0,
            "newton_model_finalized_count": 0,
            "newton_engine_shape_object_count": 0,
            "newton_collision_pipeline_created_count": 0,
            "newton_collision_pipeline_collide_count": 0,
            "newton_runtime_execution_count": 0,
        }
    ]
    assert (
        set(payload["newton_shape_runtime_engine_builder_runtime_execution_rows"][0])
        == NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_ROW_REQUIRED_KEYS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_smoke_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"]
    entry = report["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"]
    source_row = entry["newton_shape_runtime_engine_builder_entry_rows"][0]

    assert set(payload) == (NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_PAYLOAD_REQUIRED_KEYS)
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_smoke_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_smoke_recorded_runtime_execution_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_smoke_decision_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_smoke_contract_"
        "no_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["smoke_action"] == (
        "record_default_no_runtime_smoke_decision_for_single_synthetic_box"
    )
    assert payload["smoke_decision"] == "skip_real_runtime_smoke"
    assert payload["smoke_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
        ),
        "closed_gate": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT),
        "next_runtime_execution_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
        ),
        "source_entry_rows_required": 1,
        "entry_decision_required": "defer_real_runtime_entry",
        "smoke_decision": "skip_real_runtime_smoke",
        "runtime_smoke_allowed": False,
        "runtime_smoke_attempted": False,
        "runtime_smoke_passed": False,
        "real_runtime_import_allowed": False,
        "newton_model_builder_allowed": False,
        "newton_engine_shape_object_allowed": False,
        "newton_builder_shape_call_allowed": False,
        "newton_model_finalize_allowed": False,
        "newton_collision_pipeline_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_entry_row_id": source_row[
            "newton_shape_runtime_engine_builder_entry_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_api_surface_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_api_surface_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_environment_probe_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_environment_probe_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_entry_decision": "defer_real_runtime_entry",
        "source_api_surface_probe_status": "not_run_source_dir_not_configured",
    }
    assert payload["newton_shape_runtime_engine_builder_smoke_row_count"] == 1
    assert payload["source_newton_shape_runtime_engine_builder_entry_row_count"] == 1
    assert payload["runtime_smoke_allowed_count"] == 0
    assert payload["runtime_smoke_attempted_count"] == 0
    assert payload["runtime_smoke_passed_count"] == 0
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_REMAINING_GAPS
    )
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_smoke_row_count": 1,
        "source_newton_shape_runtime_engine_builder_entry_row_count": 1,
        "runtime_smoke_allowed_count": 0,
        "runtime_smoke_attempted_count": 0,
        "runtime_smoke_passed_count": 0,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "smoke_decision_distribution": {"skip_real_runtime_smoke": 1},
        "runtime_smoke_result_status_distribution": {"not_run_default_no_runtime_entry": 1},
    }
    assert payload["newton_shape_runtime_engine_builder_smoke_rows"] == [
        {
            "newton_shape_runtime_engine_builder_smoke_row_id": (
                "newton_shape_runtime_engine_builder_smoke__paper_single_box__box"
            ),
            "source_newton_shape_runtime_engine_builder_entry_row_id": source_row[
                "newton_shape_runtime_engine_builder_entry_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_api_surface_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_api_surface_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_environment_probe_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_environment_probe_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"
            ],
            "source_newton_shape_runtime_builder_construction_row_id": source_row[
                "source_newton_shape_runtime_builder_construction_row_id"
            ],
            "source_newton_shape_runtime_builder_preflight_row_id": source_row[
                "source_newton_shape_runtime_builder_preflight_row_id"
            ],
            "source_newton_shape_runtime_construction_row_id": source_row[
                "source_newton_shape_runtime_construction_row_id"
            ],
            "source_newton_shape_runtime_boundary_preflight_row_id": source_row[
                "source_newton_shape_runtime_boundary_preflight_row_id"
            ],
            "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
            "source_newton_shape_mapping_preflight_row_id": source_row[
                "source_newton_shape_mapping_preflight_row_id"
            ],
            "source_runtime_admissibility_row_id": source_row[
                "source_runtime_admissibility_row_id"
            ],
            "source_package_id": source_row["source_package_id"],
            "source_asset_id": source_row["source_asset_id"],
            "fixture_id": "paper_single_box",
            "paper_primitive": "oriented_bounding_box",
            "primitive_spec_kind": "box",
            "primitive_id": source_row["primitive_id"],
            "target_newton_shape_kind": "box",
            "future_newton_builder_constructor_name": "newton.ModelBuilder",
            "future_newton_builder_method_name": "add_shape_box",
            "future_runtime_module_names": ["newton", "warp"],
            "api_surface_probe_status": "not_run_source_dir_not_configured",
            "entry_decision": "defer_real_runtime_entry",
            "smoke_decision": "skip_real_runtime_smoke",
            "smoke_decision_reason": ("default_no_runtime_entry_decision_preserved"),
            "smoke_observation_scope": ("report_only_single_synthetic_box_lineage"),
            "runtime_smoke_allowed": False,
            "runtime_smoke_attempted": False,
            "runtime_smoke_passed": False,
            "runtime_smoke_result_status": ("not_run_default_no_runtime_entry"),
            "runtime_execution_gate_required": (
                EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
            ),
            "source_package_copy_forbidden": True,
            "real_newton_import_count": 0,
            "real_warp_import_count": 0,
            "newton_model_builder_instantiated_count": 0,
            "newton_builder_shape_call_count": 0,
            "newton_model_finalized_count": 0,
            "newton_engine_shape_object_count": 0,
            "newton_collision_pipeline_created_count": 0,
            "newton_collision_pipeline_collide_count": 0,
            "newton_runtime_execution_count": 0,
        }
    ]
    assert set(payload["newton_shape_runtime_engine_builder_smoke_rows"][0]) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_ROW_REQUIRED_KEYS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_entry_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"]
    api_surface = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
    ]
    source_row = api_surface["newton_shape_runtime_engine_builder_api_surface_rows"][0]

    assert set(payload) == (NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_PAYLOAD_REQUIRED_KEYS)
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_entry_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_entry_recorded_smoke_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_entry_decision_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_entry_only_"
        "no_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["entry_action"] == (
        "record_default_no_runtime_entry_decision_for_single_synthetic_box"
    )
    assert payload["entry_decision"] == "defer_real_runtime_entry"
    assert payload["entry_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
        ),
        "closed_gate": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT),
        "next_engine_builder_smoke_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
        ),
        "source_api_surface_rows_required": 1,
        "entry_decision": "defer_real_runtime_entry",
        "real_runtime_import_allowed": False,
        "newton_model_builder_allowed": False,
        "newton_engine_shape_object_allowed": False,
        "newton_builder_shape_call_allowed": False,
        "newton_model_finalize_allowed": False,
        "newton_collision_pipeline_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_api_surface_row_id": source_row[
            "newton_shape_runtime_engine_builder_api_surface_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_environment_probe_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_environment_probe_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_future_runtime_module_names": ["newton", "warp"],
        "source_api_surface_probe_status": "not_run_source_dir_not_configured",
    }
    assert payload["newton_shape_runtime_engine_builder_entry_row_count"] == 1
    assert payload["source_newton_shape_runtime_engine_builder_api_surface_row_count"] == 1
    assert payload["runtime_entry_allowed_count"] == 0
    assert payload["runtime_entry_attempted_count"] == 0
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_REMAINING_GAPS
    )
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_entry_row_count": 1,
        "source_newton_shape_runtime_engine_builder_api_surface_row_count": 1,
        "runtime_entry_allowed_count": 0,
        "runtime_entry_attempted_count": 0,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "entry_decision_distribution": {"defer_real_runtime_entry": 1},
    }
    assert payload["newton_shape_runtime_engine_builder_entry_rows"] == [
        {
            "newton_shape_runtime_engine_builder_entry_row_id": (
                "newton_shape_runtime_engine_builder_entry__paper_single_box__box"
            ),
            "source_newton_shape_runtime_engine_builder_api_surface_row_id": source_row[
                "newton_shape_runtime_engine_builder_api_surface_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_environment_probe_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_environment_probe_row_id"
            ],
            "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": source_row[
                "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"
            ],
            "source_newton_shape_runtime_builder_construction_row_id": source_row[
                "source_newton_shape_runtime_builder_construction_row_id"
            ],
            "source_newton_shape_runtime_builder_preflight_row_id": source_row[
                "source_newton_shape_runtime_builder_preflight_row_id"
            ],
            "source_newton_shape_runtime_construction_row_id": source_row[
                "source_newton_shape_runtime_construction_row_id"
            ],
            "source_newton_shape_runtime_boundary_preflight_row_id": source_row[
                "source_newton_shape_runtime_boundary_preflight_row_id"
            ],
            "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
            "source_newton_shape_mapping_preflight_row_id": source_row[
                "source_newton_shape_mapping_preflight_row_id"
            ],
            "source_runtime_admissibility_row_id": source_row[
                "source_runtime_admissibility_row_id"
            ],
            "source_package_id": source_row["source_package_id"],
            "source_asset_id": source_row["source_asset_id"],
            "fixture_id": "paper_single_box",
            "paper_primitive": "oriented_bounding_box",
            "primitive_spec_kind": "box",
            "primitive_id": source_row["primitive_id"],
            "target_newton_shape_kind": "box",
            "future_newton_builder_constructor_name": "newton.ModelBuilder",
            "future_newton_builder_method_name": "add_shape_box",
            "future_runtime_module_names": ["newton", "warp"],
            "api_surface_probe_status": "not_run_source_dir_not_configured",
            "entry_decision": "defer_real_runtime_entry",
            "entry_decision_reason": ("default_no_config_source_dir_no_real_runtime_entry"),
            "runtime_entry_allowed": False,
            "runtime_entry_attempted": False,
            "source_package_copy_forbidden": True,
            "real_newton_import_count": 0,
            "real_warp_import_count": 0,
            "newton_model_builder_instantiated_count": 0,
            "newton_builder_shape_call_count": 0,
            "newton_model_finalized_count": 0,
            "newton_engine_shape_object_count": 0,
            "newton_collision_pipeline_created_count": 0,
            "newton_collision_pipeline_collide_count": 0,
            "newton_runtime_execution_count": 0,
        }
    ]
    assert set(payload["newton_shape_runtime_engine_builder_entry_rows"][0]) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_ROW_REQUIRED_KEYS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_TRUE_FLAGS:
        assert payload[flag] is True


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("gate_id", "stale_gate", "entry_input_gate_id_mismatch"),
        ("next_required_gate", "stale_gate", "entry_input_next_gate_mismatch"),
        ("real_newton_import_count", 1, "entry_input_count_mismatch"),
        ("real_warp_import_count", 1, "entry_input_count_mismatch"),
        (
            "newton_model_builder_instantiated_count",
            1,
            "entry_input_count_mismatch",
        ),
        ("newton_builder_shape_call_count", 1, "entry_input_count_mismatch"),
        ("newton_model_finalized_count", 1, "entry_input_count_mismatch"),
        (
            "newton_collision_pipeline_created_count",
            1,
            "entry_input_count_mismatch",
        ),
        (
            "newton_collision_pipeline_collide_count",
            1,
            "entry_input_count_mismatch",
        ),
        ("newton_runtime_execution_count", 1, "entry_input_count_mismatch"),
        ("real_runtime_import_allowed", True, "entry_input_flag_true"),
        ("newton_model_builder_allowed", True, "entry_input_flag_true"),
        ("newton_builder_shape_call_allowed", True, "entry_input_flag_true"),
        ("newton_runtime_allowed", True, "entry_input_flag_true"),
        (
            "newton_shape_runtime_engine_builder_api_surface_recorded",
            False,
            "entry_input_flag_false",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_entry_rejects_input_drift(
    field,
    value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    api_surface = json.loads(
        json.dumps(
            report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
        )
    )
    api_surface[field] = value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload(
            api_surface
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_entry_rejects_source_row_drift_and_copies(
    cpd_paper_report,
):
    report = cpd_paper_report
    api_surface = json.loads(
        json.dumps(
            report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
        )
    )

    api_surface["newton_shape_runtime_engine_builder_api_surface_rows"] = []
    with pytest.raises(ValueError, match="entry_row_count_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload(
            api_surface
        )

    api_surface = json.loads(
        json.dumps(
            report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
        )
    )
    api_surface["newton_shape_runtime_engine_builder_api_surface_rows"][0]["source_package_id"] = (
        "stale_package"
    )
    with pytest.raises(ValueError, match="entry_source_row_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload(
            api_surface
        )

    api_surface = json.loads(
        json.dumps(
            report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
        )
    )
    api_surface["newton_shape_runtime_engine_builder_api_surface_rows"][0]["source_package"] = {}
    with pytest.raises(ValueError, match="entry_source_package_copy_forbidden"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload(
            api_surface
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_entry_static_boundary_is_report_only():
    helpers = (
        cpd_paper_offline._paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_entry,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_false_flags,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_true_flags,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_entry_coverage_summary,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "importlib.import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "import newton",
        "from newton",
        "import warp",
        "from warp",
        "ModelBuilder(",
        "CollisionPipeline(",
        ".add_shape_box(",
        ".finalize(",
        ".collide(",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_environment",
        "_import_newton_runtime",
        "inspect_newton_warp_provenance",
        "load_first_mesh",
        "inspect_usd_asset",
        "timeit",
        "perf_counter",
        "benchmark_metric",
        "measure_collision_quality",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source

    tree = ast.parse(source)
    forbidden_import_roots = {"newton", "warp"}
    forbidden_call_attrs = {
        "ModelBuilder",
        "CollisionPipeline",
        "add_shape_box",
        "finalize",
        "collide",
        "import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "_import_newton_runtime",
        "inspect_newton_environment",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_warp_provenance",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_call_attrs
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_call_attrs


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("gate_id", "stale_gate", "smoke_input_gate_id_mismatch"),
        ("next_required_gate", "stale_gate", "smoke_input_next_gate_mismatch"),
        (
            "entry_decision",
            "allow_real_runtime_entry",
            "smoke_input_entry_decision_mismatch",
        ),
        (
            "remaining_gaps",
            ["stale_gate"],
            "smoke_input_remaining_gaps_mismatch",
        ),
        ("runtime_entry_attempted_count", 1, "smoke_input_count_mismatch"),
        ("real_newton_import_count", 1, "smoke_input_count_mismatch"),
        ("real_warp_import_count", 1, "smoke_input_count_mismatch"),
        (
            "newton_model_builder_instantiated_count",
            1,
            "smoke_input_count_mismatch",
        ),
        ("newton_engine_shape_object_count", 1, "smoke_input_count_mismatch"),
        ("newton_builder_shape_call_count", 1, "smoke_input_count_mismatch"),
        ("newton_model_finalized_count", 1, "smoke_input_count_mismatch"),
        (
            "newton_collision_pipeline_created_count",
            1,
            "smoke_input_count_mismatch",
        ),
        (
            "newton_collision_pipeline_collide_count",
            1,
            "smoke_input_count_mismatch",
        ),
        ("newton_runtime_execution_count", 1, "smoke_input_count_mismatch"),
        ("runtime_entry_allowed", True, "smoke_input_flag_true"),
        ("real_runtime_import_allowed", True, "smoke_input_flag_true"),
        ("newton_model_builder_allowed", True, "smoke_input_flag_true"),
        ("newton_runtime_allowed", True, "smoke_input_flag_true"),
        (
            "newton_shape_runtime_engine_builder_entry_recorded",
            False,
            "smoke_input_flag_false",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_smoke_rejects_input_drift(
    field,
    value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    entry = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"])
    )
    entry[field] = value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_payload(
            entry
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_smoke_rejects_input_coverage_summary_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    entry = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"])
    )
    entry["coverage_summary"]["newton_runtime_execution_count"] = 1

    with pytest.raises(
        ValueError,
        match="smoke_input_coverage_summary_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_payload(
            entry
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_smoke_rejects_source_row_drift_and_copies(
    cpd_paper_report,
):
    report = cpd_paper_report
    entry = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"])
    )

    entry["newton_shape_runtime_engine_builder_entry_rows"] = []
    with pytest.raises(ValueError, match="smoke_row_count_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_payload(
            entry
        )

    entry = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"])
    )
    entry["newton_shape_runtime_engine_builder_entry_rows"][0]["source_package_id"] = (
        "stale_package"
    )
    with pytest.raises(ValueError, match="smoke_source_row_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_payload(
            entry
        )

    entry = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"])
    )
    entry["newton_shape_runtime_engine_builder_entry_rows"][0][
        "newton_engine_shape_object_count"
    ] = 1
    with pytest.raises(ValueError, match="smoke_source_row_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_payload(
            entry
        )

    entry = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"])
    )
    entry["newton_shape_runtime_engine_builder_entry_rows"][0]["source_package"] = {}
    with pytest.raises(ValueError, match="smoke_source_package_copy_forbidden"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_payload(
            entry
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_smoke_static_boundary_is_report_only():
    helpers = (
        cpd_paper_offline._paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_smoke,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_smoke_false_flags,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_smoke_true_flags,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_smoke_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_smoke_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_smoke_coverage_summary,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "importlib.import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr(",
        "eval(",
        "exec(",
        "compile(",
        "import newton",
        "from newton",
        "import warp",
        "from warp",
        "ModelBuilder(",
        "CollisionPipeline(",
        ".add_shape_box(",
        ".finalize(",
        ".collide(",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_environment",
        "_import_newton_runtime",
        "inspect_newton_warp_provenance",
        "load_first_mesh",
        "inspect_usd_asset",
        "timeit",
        "perf_counter",
        "benchmark_metric",
        "measure_collision_quality",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source

    tree = ast.parse(source)
    forbidden_import_roots = {"newton", "warp"}
    forbidden_call_attrs = {
        "ModelBuilder",
        "CollisionPipeline",
        "add_shape_box",
        "finalize",
        "collide",
        "import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr",
        "eval",
        "exec",
        "compile",
        "_import_newton_runtime",
        "inspect_newton_environment",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_warp_provenance",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_call_attrs
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_call_attrs


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("gate_id", "stale_gate", "runtime_execution_input_gate_id_mismatch"),
        (
            "closed_gate",
            "stale_gate",
            "runtime_execution_input_metadata_mismatch:closed_gate",
        ),
        (
            "input_gate_id",
            "stale_gate",
            "runtime_execution_input_metadata_mismatch:input_gate_id",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "runtime_execution_input_next_gate_mismatch",
        ),
        (
            "gate_status",
            "implemented_real_runtime_execution",
            "runtime_execution_input_metadata_mismatch:gate_status",
        ),
        (
            "decision",
            "complete",
            "runtime_execution_input_metadata_mismatch:decision",
        ),
        (
            "decision_reason",
            "real_runtime_execution_passed",
            "runtime_execution_input_metadata_mismatch:decision_reason",
        ),
        (
            "artifact_kind",
            "newton_runtime_execution_result",
            "runtime_execution_input_metadata_mismatch:artifact_kind",
        ),
        (
            "schema_version",
            2,
            "runtime_execution_input_metadata_mismatch:schema_version",
        ),
        (
            "source_scope",
            "real_usd_assets",
            "runtime_execution_input_metadata_mismatch:source_scope",
        ),
        (
            "implementation_boundary",
            "real_runtime_execution",
            "runtime_execution_input_metadata_mismatch:implementation_boundary",
        ),
        (
            "smoke_action",
            "run_real_runtime_smoke",
            "runtime_execution_input_metadata_mismatch:smoke_action",
        ),
        (
            "smoke_contract",
            {},
            "runtime_execution_input_metadata_mismatch:smoke_contract",
        ),
        (
            "input_contract_summary",
            {},
            "runtime_execution_input_metadata_mismatch:input_contract_summary",
        ),
        (
            "remaining_gaps",
            ["stale_gate"],
            "runtime_execution_input_remaining_gaps_mismatch",
        ),
        (
            "smoke_decision",
            "allow_real_runtime_smoke",
            "runtime_execution_input_smoke_decision_mismatch",
        ),
        (
            "runtime_smoke_attempted_count",
            1,
            "runtime_execution_input_count_mismatch",
        ),
        ("real_newton_import_count", 1, "runtime_execution_input_count_mismatch"),
        ("real_warp_import_count", 1, "runtime_execution_input_count_mismatch"),
        (
            "newton_model_builder_instantiated_count",
            1,
            "runtime_execution_input_count_mismatch",
        ),
        (
            "newton_engine_shape_object_count",
            1,
            "runtime_execution_input_count_mismatch",
        ),
        (
            "newton_builder_shape_call_count",
            1,
            "runtime_execution_input_count_mismatch",
        ),
        (
            "newton_model_finalized_count",
            1,
            "runtime_execution_input_count_mismatch",
        ),
        (
            "newton_collision_pipeline_created_count",
            1,
            "runtime_execution_input_count_mismatch",
        ),
        (
            "newton_collision_pipeline_collide_count",
            1,
            "runtime_execution_input_count_mismatch",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "runtime_execution_input_count_mismatch",
        ),
        (
            "runtime_smoke_attempted",
            True,
            "runtime_execution_input_flag_true",
        ),
        (
            "newton_runtime_allowed",
            True,
            "runtime_execution_input_flag_true",
        ),
        (
            "newton_shape_runtime_engine_builder_smoke_recorded",
            False,
            "runtime_execution_input_flag_false",
        ),
        (
            "unexpected_runtime_execution_input_key",
            True,
            "runtime_execution_input_unexpected_keys",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_input_drift(
    field,
    value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke[field] = value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_input_key_drift_and_copies(
    cpd_paper_report,
):
    report = cpd_paper_report

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["source_package"] = {}
    with pytest.raises(
        ValueError,
        match="runtime_execution_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    source_package = report["paper_mapped_subset_collision_package_generation_contract"][
        "collision_package_generation_rows"
    ][0]["generated_collision_package"]
    smoke["unexpected_package_copy"] = source_package
    with pytest.raises(
        ValueError,
        match="runtime_execution_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["gate_id"] = "stale_gate"
    smoke["unexpected_runtime_execution_input_key"] = True
    with pytest.raises(
        ValueError,
        match="runtime_execution_input_gate_id_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke.pop("decision_reason")
    smoke["unexpected_runtime_execution_input_key"] = True
    with pytest.raises(
        ValueError,
        match="runtime_execution_input_missing_keys:decision_reason",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_input_coverage_summary_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["coverage_summary"]["newton_runtime_execution_count"] = 1

    with pytest.raises(
        ValueError,
        match="runtime_execution_input_coverage_summary_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_rejects_source_row_drift_and_copies(
    cpd_paper_report,
):
    report = cpd_paper_report
    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )

    smoke["newton_shape_runtime_engine_builder_smoke_rows"] = []
    with pytest.raises(ValueError, match="runtime_execution_row_count_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["newton_shape_runtime_engine_builder_smoke_rows"].append(
        dict(smoke["newton_shape_runtime_engine_builder_smoke_rows"][0])
    )
    with pytest.raises(ValueError, match="runtime_execution_row_count_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["newton_shape_runtime_engine_builder_smoke_rows"][0]["source_package_id"] = (
        "stale_package"
    )
    with pytest.raises(ValueError, match="runtime_execution_source_row_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["newton_shape_runtime_engine_builder_smoke_rows"][0][
        "source_newton_shape_runtime_engine_builder_entry_row_id"
    ] = "stale_entry_row"
    with pytest.raises(ValueError, match="runtime_execution_source_row_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["newton_shape_runtime_engine_builder_smoke_rows"][0]["newton_runtime_execution_count"] = 1
    with pytest.raises(ValueError, match="runtime_execution_source_row_mismatch"):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["newton_shape_runtime_engine_builder_smoke_rows"][0][
        "unexpected_runtime_execution_source_row_key"
    ] = True
    with pytest.raises(
        ValueError,
        match="runtime_execution_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["newton_shape_runtime_engine_builder_smoke_rows"][0].pop("smoke_observation_scope")
    smoke["newton_shape_runtime_engine_builder_smoke_rows"][0][
        "unexpected_runtime_execution_source_row_key"
    ] = True
    with pytest.raises(
        ValueError,
        match=("runtime_execution_source_row_missing_keys:smoke_observation_scope"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )

    smoke = json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"])
    )
    smoke["newton_shape_runtime_engine_builder_smoke_rows"][0]["source_package"] = {}
    with pytest.raises(
        ValueError,
        match="runtime_execution_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload(
            smoke
        )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("gate_id", "stale_gate", "runtime_lane_review_input_gate_id_mismatch"),
        (
            "closed_gate",
            "stale_gate",
            "runtime_lane_review_input_metadata_mismatch:closed_gate",
        ),
        (
            "input_gate_id",
            "stale_gate",
            "runtime_lane_review_input_metadata_mismatch:input_gate_id",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "runtime_lane_review_input_next_gate_mismatch",
        ),
        (
            "gate_status",
            "implemented_real_runtime_execution",
            "runtime_lane_review_input_metadata_mismatch:gate_status",
        ),
        (
            "decision",
            "complete",
            "runtime_lane_review_input_metadata_mismatch:decision",
        ),
        (
            "decision_reason",
            "real_runtime_execution_passed",
            "runtime_lane_review_input_metadata_mismatch:decision_reason",
        ),
        (
            "artifact_kind",
            "newton_runtime_execution_result",
            "runtime_lane_review_input_metadata_mismatch:artifact_kind",
        ),
        (
            "schema_version",
            2,
            "runtime_lane_review_input_metadata_mismatch:schema_version",
        ),
        (
            "source_scope",
            "real_usd_assets",
            "runtime_lane_review_input_metadata_mismatch:source_scope",
        ),
        (
            "implementation_boundary",
            "real_runtime_execution",
            "runtime_lane_review_input_metadata_mismatch:implementation_boundary",
        ),
        (
            "runtime_execution_action",
            "run_real_runtime_execution",
            "runtime_lane_review_input_metadata_mismatch:runtime_execution_action",
        ),
        (
            "runtime_execution_contract",
            {},
            "runtime_lane_review_input_metadata_mismatch:runtime_execution_contract",
        ),
        (
            "input_contract_summary",
            {},
            "runtime_lane_review_input_metadata_mismatch:input_contract_summary",
        ),
        (
            "remaining_gaps",
            ["stale_gate"],
            "runtime_lane_review_input_remaining_gaps_mismatch",
        ),
        (
            "runtime_execution_decision",
            "run_real_runtime_execution",
            "runtime_lane_review_input_decision_mismatch",
        ),
        (
            "runtime_execution_allowed_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "runtime_execution_attempted_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "runtime_execution_passed_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "real_newton_import_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "real_warp_import_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "newton_model_builder_instantiated_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "newton_engine_shape_object_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "newton_builder_shape_call_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "newton_model_finalized_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "newton_collision_pipeline_created_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "newton_collision_pipeline_collide_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "runtime_lane_review_input_count_mismatch",
        ),
        (
            "runtime_execution_attempted",
            True,
            "runtime_lane_review_input_flag_true",
        ),
        (
            "newton_runtime_allowed",
            True,
            "runtime_lane_review_input_flag_true",
        ),
        (
            "newton_shape_runtime_engine_builder_runtime_execution_decision_recorded",
            False,
            "runtime_lane_review_input_flag_false",
        ),
        (
            "unexpected_runtime_lane_review_input_key",
            True,
            "runtime_lane_review_input_unexpected_keys",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_rejects_input_drift(
    field,
    value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution[field] = value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_rejects_input_key_drift_and_copies(
    cpd_paper_report,
):
    report = cpd_paper_report

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["source_package"] = {}
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    source_package = report["paper_mapped_subset_collision_package_generation_contract"][
        "collision_package_generation_rows"
    ][0]["generated_collision_package"]
    runtime_execution["unexpected_package_copy"] = source_package
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["gate_id"] = "stale_gate"
    runtime_execution["unexpected_runtime_lane_review_input_key"] = True
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_input_gate_id_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution.pop("decision_reason")
    runtime_execution["unexpected_runtime_lane_review_input_key"] = True
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_input_missing_keys:decision_reason",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_rejects_input_coverage_summary_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["coverage_summary"]["newton_runtime_execution_count"] = 1

    with pytest.raises(
        ValueError,
        match="runtime_lane_review_input_coverage_summary_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_rejects_source_row_drift_and_copies(
    cpd_paper_report,
):
    report = cpd_paper_report
    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )

    runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"] = []
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"].append(
        dict(runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"][0])
    )
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"][0][
        "source_package_id"
    ] = "stale_package"
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_source_row_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"][0][
        "source_newton_shape_runtime_engine_builder_smoke_row_id"
    ] = "stale_smoke_row"
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_source_row_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"][0][
        "newton_runtime_execution_count"
    ] = 1
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_source_row_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"][0][
        "unexpected_runtime_lane_review_source_row_key"
    ] = True
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"][0].pop(
        "runtime_execution_decision_reason"
    )
    runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"][0][
        "unexpected_runtime_lane_review_source_row_key"
    ] = True
    with pytest.raises(
        ValueError,
        match=("runtime_lane_review_source_row_missing_keys:runtime_execution_decision_reason"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )

    runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
            ]
        )
    )
    runtime_execution["newton_shape_runtime_engine_builder_runtime_execution_rows"][0][
        "source_package"
    ] = {}
    with pytest.raises(
        ValueError,
        match="runtime_lane_review_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload(
            runtime_execution
        )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "gate_id",
            "stale_gate",
            "configured_runtime_design_input_gate_id_mismatch",
        ),
        (
            "closed_gate",
            "stale_gate",
            "configured_runtime_design_input_metadata_mismatch:closed_gate",
        ),
        (
            "input_gate_id",
            "stale_gate",
            "configured_runtime_design_input_metadata_mismatch:input_gate_id",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "configured_runtime_design_input_next_gate_mismatch",
        ),
        (
            "gate_status",
            "implemented_real_runtime_lane_review",
            "configured_runtime_design_input_metadata_mismatch:gate_status",
        ),
        (
            "decision",
            "complete",
            "configured_runtime_design_input_metadata_mismatch:decision",
        ),
        (
            "decision_reason",
            "real_runtime_execution_passed",
            "configured_runtime_design_input_metadata_mismatch:decision_reason",
        ),
        (
            "artifact_kind",
            "newton_runtime_compatibility_result",
            "configured_runtime_design_input_metadata_mismatch:artifact_kind",
        ),
        (
            "schema_version",
            2,
            "configured_runtime_design_input_metadata_mismatch:schema_version",
        ),
        (
            "source_scope",
            "real_usd_assets",
            "configured_runtime_design_input_metadata_mismatch:source_scope",
        ),
        (
            "implementation_boundary",
            "real_runtime_execution",
            "configured_runtime_design_input_metadata_mismatch:implementation_boundary",
        ),
        (
            "runtime_lane_review_action",
            "allow_real_runtime_execution",
            "configured_runtime_design_input_metadata_mismatch:runtime_lane_review_action",
        ),
        (
            "runtime_lane_review_contract",
            {},
            "configured_runtime_design_input_metadata_mismatch:runtime_lane_review_contract",
        ),
        (
            "input_contract_summary",
            {},
            "configured_runtime_design_input_metadata_mismatch:input_contract_summary",
        ),
        (
            "remaining_gaps",
            ["stale_gate"],
            "configured_runtime_design_input_remaining_gaps_mismatch",
        ),
        (
            "runtime_lane_review_decision",
            "runtime_compatibility_validated",
            "configured_runtime_design_input_metadata_mismatch:runtime_lane_review_decision",
        ),
        (
            "runtime_lane_review_status",
            "runtime_compatibility_validated",
            "configured_runtime_design_input_metadata_mismatch:runtime_lane_review_status",
        ),
        (
            "runtime_execution_allowed_count",
            1,
            "configured_runtime_design_input_count_mismatch",
        ),
        (
            "real_runtime_execution_evidence_count",
            1,
            "configured_runtime_design_input_count_mismatch",
        ),
        (
            "runtime_compatibility_validated_count",
            1,
            "configured_runtime_design_input_count_mismatch",
        ),
        (
            "real_newton_import_count",
            1,
            "configured_runtime_design_input_count_mismatch",
        ),
        (
            "newton_model_builder_instantiated_count",
            1,
            "configured_runtime_design_input_count_mismatch",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "configured_runtime_design_input_count_mismatch",
        ),
        (
            "real_runtime_execution_evidence",
            True,
            "configured_runtime_design_input_flag_true",
        ),
        (
            "runtime_compatibility_validated",
            True,
            "configured_runtime_design_input_flag_true",
        ),
        (
            "configured_runtime_design_ready",
            True,
            "configured_runtime_design_input_flag_true",
        ),
        (
            "newton_shape_runtime_engine_builder_runtime_lane_review_recorded",
            False,
            "configured_runtime_design_input_flag_false",
        ),
        (
            "runtime_lane_claim_boundary_preserved",
            False,
            "configured_runtime_design_input_flag_false",
        ),
        (
            "unexpected_configured_runtime_design_input_key",
            True,
            "configured_runtime_design_input_unexpected_keys",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_rejects_input_drift(
    field,
    value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review[field] = value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_rejects_input_key_drift_and_copies(
    cpd_paper_report,
):
    report = cpd_paper_report

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["source_package"] = {}
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    source_package = report["paper_mapped_subset_collision_package_generation_contract"][
        "collision_package_generation_rows"
    ][0]["generated_collision_package"]
    runtime_lane_review["unexpected_package_copy"] = source_package
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["gate_id"] = "stale_gate"
    runtime_lane_review["unexpected_configured_runtime_design_input_key"] = True
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_input_gate_id_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review.pop("decision_reason")
    runtime_lane_review["unexpected_configured_runtime_design_input_key"] = True
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_input_missing_keys:decision_reason",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_rejects_input_coverage_summary_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["coverage_summary"]["newton_runtime_execution_count"] = 1

    with pytest.raises(
        ValueError,
        match="configured_runtime_design_input_coverage_summary_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_rejects_source_row_drift_and_copies(
    cpd_paper_report,
):
    report = cpd_paper_report
    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )

    runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"] = []
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"].append(
        dict(runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"][0])
    )
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"][0][
        "source_package_id"
    ] = "stale_package"
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_source_row_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"][0][
        "runtime_lane_review_decision"
    ] = "runtime_compatibility_validated"
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_source_row_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"][0][
        "newton_runtime_execution_count"
    ] = 1
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_source_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"][0][
        "unexpected_configured_runtime_design_source_row_key"
    ] = True
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"][0].pop(
        "runtime_lane_review_status"
    )
    runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"][0][
        "unexpected_configured_runtime_design_source_row_key"
    ] = True
    with pytest.raises(
        ValueError,
        match=("configured_runtime_design_source_row_missing_keys:runtime_lane_review_status"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )

    runtime_lane_review = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
            ]
        )
    )
    runtime_lane_review["newton_shape_runtime_engine_builder_runtime_lane_review_rows"][0][
        "source_package"
    ] = {}
    with pytest.raises(
        ValueError,
        match="configured_runtime_design_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload(
            runtime_lane_review
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_static_boundary_is_report_only():
    helpers = (
        cpd_paper_offline._paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_design_false_flags,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_design_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_design_input_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_design_input_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_design_input_required_keys_present,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_design_source_row_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_design_source_row_required_keys_present,
        cpd_paper_offline._paper_runtime_engine_builder_configured_runtime_design_has_source_package_key,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_design_source_package_copies_absent,
        cpd_paper_offline._paper_validate_primitivespec_runtime_construction_false_flags,
        cpd_paper_offline._paper_runtime_admissibility_preflight_package_dicts,
        cpd_paper_offline._paper_policy_distribution,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_design_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_design_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_design_coverage_summary,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "importlib.import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr(",
        "eval(",
        "exec(",
        "compile(",
        "import newton",
        "from newton",
        "import warp",
        "from warp",
        "import pxr",
        "from pxr",
        "import yaml",
        "from yaml",
        "import tomllib",
        "from tomllib",
        "import configparser",
        "from configparser",
        "ConfigParser",
        "os.environ",
        "getenv",
        "open(",
        ".read_text(",
        ".read_bytes(",
        ".open(",
        ".load(",
        ".safe_load(",
        "ModelBuilder(",
        "CollisionPipeline(",
        ".add_shape_box(",
        ".finalize(",
        ".collide(",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_environment",
        "_import_newton_runtime",
        "inspect_newton_warp_provenance",
        "inspect_real_usd",
        "load_first_mesh",
        "inspect_usd_asset",
        "timeit",
        "perf_counter",
        "process_time",
        "benchmark_metric",
        "measure_collision_quality",
        "collision_quality",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source

    tree = ast.parse(source)
    forbidden_import_roots = {
        "configparser",
        "newton",
        "tomllib",
        "warp",
        "yaml",
        "pxr",
    }
    forbidden_call_attrs = {
        "ModelBuilder",
        "CollisionPipeline",
        "add_shape_box",
        "finalize",
        "collide",
        "ConfigParser",
        "import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr",
        "eval",
        "exec",
        "compile",
        "getenv",
        "open",
        "load",
        "safe_load",
        "read_text",
        "read_bytes",
        "_import_newton_runtime",
        "inspect_newton_environment",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_warp_provenance",
        "inspect_real_usd",
        "inspect_usd_asset",
        "perf_counter",
        "process_time",
        "collision_quality",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_call_attrs
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_call_attrs
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            assert (node.value.id, node.attr) != ("os", "environ")


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_execution_static_boundary_is_report_only():
    helpers = (
        cpd_paper_offline._paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_execution_false_flags,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_execution_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_execution_input_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_execution_source_row_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_execution_input_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_execution_input_nested_values,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_execution_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_execution_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_execution_coverage_summary,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "importlib.import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr(",
        "eval(",
        "exec(",
        "compile(",
        "import newton",
        "from newton",
        "import warp",
        "from warp",
        "import pxr",
        "from pxr",
        "import yaml",
        "from yaml",
        "import tomllib",
        "from tomllib",
        "import configparser",
        "from configparser",
        "ConfigParser",
        "os.environ",
        "getenv",
        "open(",
        ".read_text(",
        ".read_bytes(",
        ".open(",
        ".load(",
        ".safe_load(",
        "ModelBuilder(",
        "CollisionPipeline(",
        ".add_shape_box(",
        ".finalize(",
        ".collide(",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_environment",
        "_import_newton_runtime",
        "inspect_newton_warp_provenance",
        "inspect_real_usd",
        "load_first_mesh",
        "inspect_usd_asset",
        "timeit",
        "perf_counter",
        "process_time",
        "benchmark_metric",
        "measure_collision_quality",
        "collision_quality",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source

    tree = ast.parse(source)
    forbidden_import_roots = {
        "configparser",
        "newton",
        "tomllib",
        "warp",
        "yaml",
        "pxr",
    }
    forbidden_call_attrs = {
        "ModelBuilder",
        "CollisionPipeline",
        "add_shape_box",
        "finalize",
        "collide",
        "ConfigParser",
        "import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr",
        "eval",
        "exec",
        "compile",
        "getenv",
        "open",
        "load",
        "safe_load",
        "read_text",
        "read_bytes",
        "_import_newton_runtime",
        "inspect_newton_environment",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_warp_provenance",
        "inspect_real_usd",
        "inspect_usd_asset",
        "perf_counter",
        "process_time",
        "collision_quality",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_call_attrs
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_call_attrs
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            assert (node.value.id, node.attr) != ("os", "environ")


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_static_boundary_is_report_only():
    helpers = (
        cpd_paper_offline._paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_false_flags,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_lane_review_input_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_lane_review_source_row_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_lane_review_input_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_configured_runtime_lane_review_input_nested_values,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_coverage_summary,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "importlib.import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr(",
        "eval(",
        "exec(",
        "compile(",
        "import newton",
        "from newton",
        "import warp",
        "from warp",
        "import pxr",
        "from pxr",
        "import yaml",
        "from yaml",
        "import tomllib",
        "from tomllib",
        "import configparser",
        "from configparser",
        "ConfigParser",
        "os.environ",
        "getenv",
        "open(",
        ".read_text(",
        ".read_bytes(",
        ".open(",
        ".load(",
        ".safe_load(",
        "ModelBuilder(",
        "CollisionPipeline(",
        ".add_shape_box(",
        ".finalize(",
        ".collide(",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_environment",
        "_import_newton_runtime",
        "inspect_newton_warp_provenance",
        "inspect_real_usd",
        "load_first_mesh",
        "inspect_usd_asset",
        "timeit",
        "perf_counter",
        "process_time",
        "benchmark_metric",
        "measure_collision_quality",
        "collision_quality",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source

    tree = ast.parse(source)
    forbidden_import_roots = {
        "configparser",
        "newton",
        "tomllib",
        "warp",
        "yaml",
        "pxr",
    }
    forbidden_call_attrs = {
        "ModelBuilder",
        "CollisionPipeline",
        "add_shape_box",
        "finalize",
        "collide",
        "ConfigParser",
        "import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr",
        "eval",
        "exec",
        "compile",
        "getenv",
        "open",
        "load",
        "safe_load",
        "read_text",
        "read_bytes",
        "_import_newton_runtime",
        "inspect_newton_environment",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_warp_provenance",
        "inspect_real_usd",
        "inspect_usd_asset",
        "perf_counter",
        "process_time",
        "collision_quality",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_call_attrs
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_call_attrs
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            assert (node.value.id, node.attr) != ("os", "environ")


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_execution_static_boundary_is_report_only():
    helpers = (
        cpd_paper_offline._paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_execution_false_flags,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_execution_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_execution_input_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_execution_input_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_execution_input_required_keys_present,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_execution_source_row_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_execution_source_row_required_keys_present,
        cpd_paper_offline._paper_runtime_engine_builder_runtime_execution_has_source_package_key,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_execution_source_package_copies_absent,
        cpd_paper_offline._paper_validate_primitivespec_runtime_construction_false_flags,
        cpd_paper_offline._paper_runtime_admissibility_preflight_package_dicts,
        cpd_paper_offline._paper_policy_distribution,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_execution_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_execution_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_execution_coverage_summary,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "importlib.import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr(",
        "eval(",
        "exec(",
        "compile(",
        "import newton",
        "from newton",
        "import warp",
        "from warp",
        "ModelBuilder(",
        "CollisionPipeline(",
        ".add_shape_box(",
        ".finalize(",
        ".collide(",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_environment",
        "_import_newton_runtime",
        "inspect_newton_warp_provenance",
        "load_first_mesh",
        "inspect_usd_asset",
        "timeit",
        "perf_counter",
        "benchmark_metric",
        "measure_collision_quality",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source

    tree = ast.parse(source)
    forbidden_import_roots = {"newton", "warp"}
    forbidden_call_attrs = {
        "ModelBuilder",
        "CollisionPipeline",
        "add_shape_box",
        "finalize",
        "collide",
        "import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr",
        "eval",
        "exec",
        "compile",
        "_import_newton_runtime",
        "inspect_newton_environment",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_warp_provenance",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_call_attrs
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_call_attrs


def test_cpd_paper_newton_shape_runtime_engine_builder_runtime_lane_review_static_boundary_is_report_only():
    helpers = (
        cpd_paper_offline._paper_remaining_gaps_after_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_lane_review_false_flags,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_lane_review_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_lane_review_input_true_flags,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_lane_review_input_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_lane_review_input_required_keys_present,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_lane_review_source_row_keys,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_lane_review_source_row_required_keys_present,
        cpd_paper_offline._paper_runtime_engine_builder_runtime_lane_review_has_source_package_key,
        cpd_paper_offline._paper_validate_runtime_engine_builder_runtime_lane_review_source_package_copies_absent,
        cpd_paper_offline._paper_validate_primitivespec_runtime_construction_false_flags,
        cpd_paper_offline._paper_runtime_admissibility_preflight_package_dicts,
        cpd_paper_offline._paper_policy_distribution,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_lane_review_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_lane_review_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_runtime_lane_review_coverage_summary,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "importlib.import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr(",
        "eval(",
        "exec(",
        "compile(",
        "import newton",
        "from newton",
        "import warp",
        "from warp",
        "ModelBuilder(",
        "CollisionPipeline(",
        ".add_shape_box(",
        ".finalize(",
        ".collide(",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_environment",
        "_import_newton_runtime",
        "inspect_newton_warp_provenance",
        "load_first_mesh",
        "inspect_usd_asset",
        "timeit",
        "perf_counter",
        "benchmark_metric",
        "measure_collision_quality",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source

    tree = ast.parse(source)
    forbidden_import_roots = {"newton", "warp"}
    forbidden_call_attrs = {
        "ModelBuilder",
        "CollisionPipeline",
        "add_shape_box",
        "finalize",
        "collide",
        "import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "getattr",
        "eval",
        "exec",
        "compile",
        "_import_newton_runtime",
        "inspect_newton_environment",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
        "inspect_newton_warp_provenance",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module.split(".")[0] not in forbidden_import_roots
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_call_attrs
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_call_attrs


def test_cpd_paper_package_adapter_contract_blocks_malformed_or_duplicate_records(cpd_paper_report):
    report = cpd_paper_report
    changed = dict(report["paper_offline_changed_decomposition_output_contract"])
    output_rows = [dict(row) for row in changed["decomposition_output_rows"][:1]]
    original = dict(output_rows[0]["primitive_records"][0])
    missing_id = {key: value for key, value in original.items() if key != "offline_primitive_id"}
    duplicate = dict(original)
    output_rows[0]["primitive_records"] = [original, duplicate, missing_id]
    changed["decomposition_output_rows"] = output_rows
    changed["coverage_summary"] = {
        **changed["coverage_summary"],
        "decomposition_output_row_count": 1,
        "primitive_record_count": 3,
    }

    payload = _paper_package_adapter_contract_payload(changed)
    rows = payload["primitive_adapter_decision_rows"]

    assert payload["coverage_summary"]["primitive_decision_row_count"] == 3
    assert payload["coverage_summary"]["blocked_record_count"] == 3
    assert {row["adapter_decision"] for row in rows} == {"blocked"}
    assert len({row["adapter_decision_id"] for row in rows}) == 3
    assert sorted(row["adapter_decision_reason"] for row in rows) == [
        "adapter_required_fields_missing",
        "duplicate_offline_primitive_id_blocks_adapter_contract",
        "duplicate_offline_primitive_id_blocks_adapter_contract",
    ]
    assert sorted(row["record_field_status"] for row in rows) == [
        "duplicate_offline_primitive_id",
        "duplicate_offline_primitive_id",
        "missing_required_fields",
    ]
    for row in rows:
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_package_adapter_missing_id_fallback_cannot_collide_with_real_id(
    cpd_paper_report,
):
    report = cpd_paper_report
    changed = dict(report["paper_offline_changed_decomposition_output_contract"])
    output_rows = [
        dict(
            report["paper_offline_changed_decomposition_output_contract"][
                "decomposition_output_rows"
            ][0]
        )
    ]
    original = dict(output_rows[0]["primitive_records"][0])
    colliding_real_id = f"{output_rows[0]['output_id']}:missing_offline_primitive_id:1"
    real_id_record = {
        **original,
        "offline_primitive_id": colliding_real_id,
    }
    missing_id_record = {
        key: value for key, value in original.items() if key != "offline_primitive_id"
    }
    output_rows[0]["primitive_records"] = [real_id_record, missing_id_record]
    changed["decomposition_output_rows"] = output_rows
    changed["coverage_summary"] = {
        **changed["coverage_summary"],
        "decomposition_output_row_count": 1,
        "primitive_record_count": 2,
    }

    payload = _paper_package_adapter_contract_payload(changed)
    rows = payload["primitive_adapter_decision_rows"]

    assert len(rows) == 2
    assert len({row["adapter_decision_id"] for row in rows}) == 2
    assert rows[0]["adapter_decision"] == "later_policy_required"
    assert rows[1]["adapter_decision"] == "blocked"
    assert rows[1]["record_field_status"] == "missing_required_fields"
    assert rows[1]["offline_primitive_id"].startswith("__missing_offline_primitive_id__:")


def test_cpd_paper_source_policy_generalization_rows_match_case_payloads(cpd_paper_report):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}
    payload = report["paper_generalization_batch_a_source_policy"]
    rows = {row["policy_row_id"]: row for row in payload["policy_matrix"]}

    mixed = cases["paper_mixed_face_preprocess_operator"]
    mixed_row = rows["accepted_mixed_triangle_quad_polygon_exact_dedup"]
    assert mixed_row["evidence_case_id"] == mixed["case_id"]
    assert mixed_row["row_status"] == "accepted_offline_policy_fixture"
    assert mixed_row["source_face_arities"] == mixed["source_mesh"]["source_face_arities"]
    assert mixed_row["source_face_count"] == mixed["source_mesh"]["source_face_count"]
    assert mixed_row["triangulated_face_count"] == mixed["source_mesh"]["triangulated_face_count"]
    assert (
        mixed_row["duplicate_vertex_preprocessing"]
        == mixed["source_mesh"]["duplicate_vertex_preprocessing"]
    )
    assert mixed_row["operator_aggregate_count"] == len(
        mixed["operator_audit"]["source_face_operator_aggregates"]
    )
    assert mixed_row["source_face_remap_count"] == len(mixed["source_mesh"]["source_face_remap"])
    aggregates = mixed["operator_audit"]["source_face_operator_aggregates"]
    assert mixed_row["operator_aggregate_source_face_ids"] == [
        aggregate["source_face_id"] for aggregate in aggregates
    ]
    assert mixed_row["operator_aggregate_generated_triangle_face_ids"] == [
        aggregate["generated_triangle_face_ids"] for aggregate in aggregates
    ]
    assert mixed_row["operator_q_aggregation_policy"] == (
        "aggregate_q_matrix_equals_sum_generated_triangle_q_rows"
    )
    face_q_by_id = {face["face_id"]: face["q_matrix"] for face in mixed["operator_audit"]["faces"]}
    for aggregate in aggregates:
        expected_q = [
            [
                sum(
                    face_q_by_id[face_id][row_index][col_index]
                    for face_id in aggregate["generated_triangle_face_ids"]
                )
                for col_index in range(3)
            ]
            for row_index in range(3)
        ]
        assert aggregate["q_matrix"] == expected_q

    degenerate = cases["paper_degenerate_preprocess_face_drop"]
    degenerate_row = rows["accepted_degenerate_after_exact_dedup_drop"]
    assert degenerate_row["evidence_case_id"] == degenerate["case_id"]
    assert degenerate_row["row_status"] == "accepted_after_dropping_degenerate_source_face"
    assert (
        degenerate_row["dropped_source_face_ids"]
        == degenerate["preprocessing_audit"]["dropped_source_face_ids"]
    )
    assert (
        degenerate_row["retained_source_face_ids"]
        == degenerate["preprocessing_audit"]["retained_source_face_ids"]
    )
    assert (
        degenerate_row["executable_source_face_ids"]
        == degenerate["source_mesh"]["executable_source_face_ids"]
    )
    assert (
        degenerate_row["operator_source_faces"]
        == degenerate["operator_audit"]["merged_group"]["source_faces"]
    )
    assert (
        degenerate_row["primitive_fit_source_faces"]
        == degenerate["primitive_fit_audit"]["source_faces"]
    )

    concave = cases["paper_concave_polygon_rejected"]
    concave_row = rows["rejected_concave_polygon"]
    assert concave_row["evidence_case_id"] == concave["case_id"]
    assert concave_row["row_status"] == "unsupported_offline_policy_fixture"
    assert concave_row["case_status"] == concave["case_status"]
    assert concave_row["failure_label"] == concave["mesh_intake_policy_audit"]["failure_label"]
    assert concave_row["top_level_failure_label"] is False
    assert concave_row["source_face_arities"] == concave["source_mesh"]["source_face_arities"]
    assert concave_row["triangulated_face_count"] == 0
    assert concave_row["operator_row_count"] == 0
    assert concave_row["primitive_fit_row_count"] == 0


def test_cpd_paper_offline_report_covers_first_toy_slice(cpd_paper_report):
    report = cpd_paper_report

    assert report["stage"] == "cpd_paper_offline_report"
    assert report["status"] == "partial"
    assert report["report_generation_status"] == "smoke_passed"
    assert report["claim_boundary"] == CPD_PAPER_OFFLINE_CLAIM_BOUNDARY
    assert report["package_generation_triggered"] is False
    assert report["newton_runtime_triggered"] is False
    assert report["real_usd_triggered"] is False
    assert report["benchmark_triggered"] is False
    assert report["paper_faithful_offline_supported"] is False
    assert report["paper_faithfulness"]["status"] == "partial"
    assert report["source_scope"] == "synthetic_toy_fixtures_only"
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        "paper_faithful_offline_generalization_plan"
        not in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_faithful_offline_generalization_plan"
        in report["paper_faithfulness"]["implemented_planning_scope"]
    )
    assert (
        "priority_queue_trace_audit_topology_only"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "component_pair_edge_insertion_audit_threshold_disabled"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "component_pair_threshold_blocking_audit"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "postprocess_enclosed_primitive_culling_audit"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_polygon_quad_intake_policy_audit"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_obb_sphere_fit_faithfulness_audit"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_duplicate_vertex_preprocessing_audit"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_faithful_offline_scope_audit"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_fixture_breadth_batch_a_source_preprocess_intake_operator"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_fixture_breadth_batch_b_primitive_fit"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_fixture_breadth_batch_c_cost_search_stop"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_fixture_breadth_batch_d_component_pair"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_fixture_breadth_batch_e_postprocess"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )
    assert (
        "paper_fixture_breadth_completion_review"
        in report["paper_faithfulness"]["implemented_fixture_scope"]
    )

    scope_audit = report["paper_faithful_offline_scope_audit"]
    assert scope_audit["audit_scope"] == "fixture_scoped_offline_paper_lane"
    assert scope_audit["audit_version"] == 1
    assert scope_audit["decision"] == "remain_partial"
    assert scope_audit["paper_faithful_offline_allowed"] is False
    assert scope_audit["decision_reason"] == "fixture_scope_still_partial"
    assert scope_audit["blocking_criteria_ids"] == EXPECTED_SCOPE_AUDIT_BLOCKERS
    assert scope_audit["package_generation_triggered"] is False
    assert scope_audit["newton_runtime_triggered"] is False
    assert scope_audit["real_usd_triggered"] is False
    assert scope_audit["benchmark_triggered"] is False
    criteria = scope_audit["criteria"]
    assert [row["criterion_id"] for row in criteria] == EXPECTED_SCOPE_AUDIT_CRITERIA
    assert criteria == EXPECTED_SCOPE_AUDIT_ROWS
    for row in criteria:
        assert set(row) == {
            "criterion_id",
            "paper_requirement",
            "current_evidence",
            "status",
            "surrogate_or_paper_faithful",
            "blocking_for_paper_faithful_offline",
            "claim_boundary",
            "next_action",
        }
        assert row["status"] in {
            "implemented_fixture_scope",
            "partial_fixture_scope",
            "not_started",
            "blocked_until_later_gate",
        }
        assert row["status"] != "paper_faithful_offline"
        assert row["surrogate_or_paper_faithful"] in {
            "fixture_scoped_paper_shaped",
            "paper_aligned_boundary",
            "not_paper_faithful",
            "out_of_offline_scope",
        }
        assert row["surrogate_or_paper_faithful"] != "paper_faithful_offline"

    cases = {case["case_id"]: case for case in report["cases"]}
    assert set(cases) == {
        "paper_single_box",
        "paper_two_face_merge",
        "paper_three_face_chain",
        "paper_disconnected_components",
        "paper_component_pair_threshold_blocked",
        "paper_tiny_sphere_clamp",
        "paper_duplicate_vertex_preprocessing",
        "paper_frustum_like",
        "paper_trapezoid_prism_like",
        "paper_nested_primitive",
        "paper_quad_face_intake",
        "paper_polygon_face_intake",
        "paper_mixed_face_preprocess_operator",
        "paper_degenerate_preprocess_face_drop",
        "paper_concave_polygon_rejected",
        "paper_rotated_box_fit",
        "paper_offset_sphere_fit",
        "paper_off_axis_capsule_fit",
        "paper_flat_capped_cylinder_axis_fit",
        "paper_tapered_frustum_fit",
        "paper_asymmetric_trapezoid_fit",
        "paper_branching_cost_order",
        "paper_equal_cost_queue_tie",
        "paper_nonzero_threshold_block",
        "paper_component_pair_multi_candidate_order",
        "paper_component_pair_cap_skipped",
        "paper_rotated_nested_primitive",
        "paper_cross_type_enclosure_boundary",
    }
    assert all(case["package_generation_triggered"] is False for case in cases.values())
    for case in cases.values():
        if "primitive_fit_audits" not in case:
            continue
        for audit in case["primitive_fit_audits"]:
            paper_primitives = [row["paper_primitive"] for row in audit["candidates"]]
            assert len(paper_primitives) == len(set(paper_primitives))

    single_box = cases["paper_single_box"]
    assert single_box["source_mesh"]["face_arity_policy"] == "triangle_only_fixture"
    assert single_box["source_mesh"]["connected_component_count"] == 1
    assert single_box["source_mesh"]["source_face_remap"] == "identity"
    assert single_box["operator_audit"]["epsilon"] == 1e-6
    assert single_box["operator_audit"]["faces"][0]["q_matrix"]
    assert single_box["operator_audit"]["merged_group"]["eigenvalues"]
    assert single_box["operator_audit"]["merged_group"]["eigenvector_matrix_layout"] == (
        "columns_are_eigenvectors"
    )
    assert abs(single_box["primitive_fit_audit"]["selected"]["volume"] - 1.0) < 3e-3

    single_box_points = [
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [2.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 0.5],
        [2.0, 0.0, 0.5],
        [2.0, 1.0, 0.5],
        [0.0, 1.0, 0.5],
    ]
    quad_face_points = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
    ]
    tiny_sphere_clamp_points = [
        [0.0, 0.0, 0.0],
        [0.0001, 0.0, 0.0],
        [0.0, 0.0001, 0.0],
    ]
    _assert_paper_obb_sphere_rows(single_box, single_box_points)
    _assert_paper_obb_sphere_rows(cases["paper_quad_face_intake"], quad_face_points)
    _assert_paper_obb_sphere_rows(
        cases["paper_tiny_sphere_clamp"],
        tiny_sphere_clamp_points,
    )
    tiny_sphere = _candidate_by_paper_primitive(
        cases["paper_tiny_sphere_clamp"]["primitive_fit_audit"],
        "sphere",
    )
    assert tiny_sphere["dimensions"]["unclamped_radius"] < 1e-3
    assert tiny_sphere["dimensions"]["radius"] == 1e-3
    _assert_duplicate_vertex_preprocessing_case(cases["paper_duplicate_vertex_preprocessing"])

    primitive_types = {
        row["paper_primitive"] for row in single_box["primitive_fit_audit"]["candidates"]
    }
    assert primitive_types == {
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    }
    box = _candidate_by_paper_primitive(
        single_box["primitive_fit_audit"],
        "oriented_bounding_box",
    )
    capsule = _candidate_by_paper_primitive(single_box["primitive_fit_audit"], "capsule")
    assert capsule["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert capsule["fit_model"] == "paper_capsule_min_volume_over_axes_with_spherical_cap_height"
    assert capsule["axis_selection_policy"] == "min_volume_capsule_axis"
    assert capsule["newton_runtime_kind"] == "capsule"
    assert capsule["contains_assigned_points"] is True
    assert capsule["fit_failure_reason"] is None
    capsule_dims = capsule["dimensions"]
    assert capsule_dims["axis_selection_policy"] == "min_volume_capsule_axis"
    assert capsule_dims["volume_formula"] == "pi*r^2*h + 4/3*pi*r^3"
    assert len(capsule_dims["paper_capsule_axis_candidates"]) == 3
    capsule_axis_volumes = [
        row["capsule_volume"] for row in capsule_dims["paper_capsule_axis_candidates"]
    ]
    capsule_selected_axis = capsule_dims["selected_axis_index"]
    capsule_selected_axis_row = [
        row
        for row in capsule_dims["paper_capsule_axis_candidates"]
        if row["axis_index"] == capsule_selected_axis
    ][0]
    assert capsule_selected_axis_row["capsule_volume"] == min(capsule_axis_volumes)
    assert capsule_selected_axis_row["capsule_volume"] == capsule["volume"]
    assert capsule_selected_axis_row["contains_assigned_points"] is True
    axis_point = box["center"]
    for candidate in capsule_dims["paper_capsule_axis_candidates"]:
        axis = capsule["axes"][candidate["axis_index"]]
        paper_heights = []
        for point in single_box_points:
            relative = [point[index] - axis_point[index] for index in range(3)]
            projected = sum(relative[index] * axis[index] for index in range(3))
            radial = [relative[index] - projected * axis[index] for index in range(3)]
            radial_distance_squared = sum(value * value for value in radial)
            cap_allowance = sqrt(max(candidate["radius"] ** 2 - radial_distance_squared, 0.0))
            paper_heights.append(projected - cap_allowance)
        assert abs(candidate["paper_height_min"] - min(paper_heights)) < 1e-7
        assert abs(candidate["paper_height_max"] - max(paper_heights)) < 1e-7
    expected_capsule_volume = (
        pi * capsule_dims["radius"] ** 2 * capsule_dims["height"]
        + (4.0 / 3.0) * pi * capsule_dims["radius"] ** 3
    )
    assert abs(capsule["volume"] - expected_capsule_volume) < 1e-9
    assert abs(capsule["weighted_volume"] - capsule["volume"]) < 1e-9
    capped = _candidate_by_paper_primitive(single_box["primitive_fit_audit"], "capped_cylinder")
    assert capped["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert capped["fit_model"] == "paper_flat_capped_cylinder_min_volume_over_axes"
    assert capped["newton_runtime_kind"] == "offline_only_unmapped"
    assert capped["contains_assigned_points"] is True
    assert capped["fit_failure_reason"] is None
    capped_dims = capped["dimensions"]
    assert capped_dims["cap_model"] == "flat_caps"
    assert capped_dims["axis_selection_policy"] == "min_volume_flat_cylinder_axis"
    assert len(capped_dims["flat_cylinder_axis_candidates"]) == 3
    capped_axis_volumes = [
        row["flat_cylinder_volume"] for row in capped_dims["flat_cylinder_axis_candidates"]
    ]
    capped_selected_axis = capped_dims["selected_axis_index"]
    capped_selected_axis_row = [
        row
        for row in capped_dims["flat_cylinder_axis_candidates"]
        if row["axis_index"] == capped_selected_axis
    ][0]
    assert capped_selected_axis_row["flat_cylinder_volume"] == min(capped_axis_volumes)
    assert abs(capped["volume"] - pi * capped_dims["radius"] ** 2 * capped_dims["height"]) < 1e-9
    assert abs(capped["weighted_volume"] - capped["volume"] * 1.05) < 1e-9
    assert single_box["primitive_fit_audit"]["missing_paper_primitives"] == []

    merge_case = cases["paper_two_face_merge"]
    assert [audit["source_faces"] for audit in merge_case["primitive_fit_audits"]] == [
        [0],
        [1],
        [0, 1],
    ]
    assert merge_case["collapse_trace"]["edge_source"] == "topology"
    assert merge_case["collapse_trace"]["accepted"] is True
    assert merge_case["collapse_trace"]["stop_reason"] == "target_count_reached"
    assert merge_case["collapse_trace"]["lookahead_used"] is False
    cost = merge_case["collapse_cost_audit"]
    assert cost["paper_base_cost"] == cost["merged_volume"] - (
        cost["left_volume"] + cost["right_volume"]
    )
    assert cost["weighted_priority_cost"] == cost["merged_weighted_volume"] - (
        cost["left_weighted_volume"] + cost["right_weighted_volume"]
    )
    assert cost["primary_cost_normalized_by_aabb"] is False
    assert cost["intersection_volume_term_included"] is False
    assert cost["paper_weights"]["capped_cylinder"] == 1.05
    assert cost["priority_queue_policy"] == "greedy_single_pop_fixture"
    assert cost["left_primitive"] == cost["left_fit_audit"]["selected"]["paper_primitive"]
    assert cost["right_primitive"] == cost["right_fit_audit"]["selected"]["paper_primitive"]
    assert cost["merged_primitive"] == cost["merged_fit_audit"]["selected"]["paper_primitive"]
    assert cost["left_fit_audit"]["source_faces"] == [0]
    assert cost["right_fit_audit"]["source_faces"] == [1]
    assert cost["merged_fit_audit"]["source_faces"] == [0, 1]
    assert cost["left_fit_audit"]["candidates"]
    assert cost["right_fit_audit"]["candidates"]
    assert cost["merged_fit_audit"]["candidates"]
    merge_frustum = _candidate_by_paper_primitive(merge_case["primitive_fit_audit"], "frustum")
    assert merge_frustum["contains_assigned_points"] is True
    assert merge_frustum["fit_failure_reason"] is None

    queue_case = cases["paper_three_face_chain"]
    trace = queue_case["collapse_trace"]
    assert trace["trace_scope"] == "topology_priority_queue_trace_fixture"
    assert trace["priority_queue_policy"] == "paper_greedy_min_weighted_priority_cost"
    assert trace["target_primitive_count"] == 1
    assert trace["excess_volume_threshold"] == "default_inf"
    assert trace["threshold_policy"] == "disabled"
    assert trace["component_pair_edge_policy"] == "disabled"
    assert trace["component_pair_edge_insertion_triggered"] is False
    assert trace["topology_queue_exhausted_before_component_pair_insertion"] is False
    assert trace["component_pair_candidate_count"] == 0
    assert trace["component_pair_candidate_cap"] == "disabled"
    assert trace["initial_active_groups"] == [[0], [1], [2]]
    assert trace["initial_edge_count"] == 2
    assert trace["accepted_merge_count"] == 2
    assert trace["stale_entry_skipped_count"] >= 1
    assert trace["blocked_merge_count"] == 0
    assert trace["stop_reason"] == "target_count_reached"
    assert trace["final_active_groups"] == [[0, 1, 2]]
    assert trace["package_generation_triggered"] is False
    assert trace["newton_runtime_triggered"] is False
    assert trace["real_usd_triggered"] is False
    assert trace["benchmark_triggered"] is False
    events = trace["events"]
    accepted_events = [event for event in events if event["accepted"] is True]
    stale_events = [event for event in events if event["stale_entry"] is True]
    assert len(accepted_events) == 2
    assert stale_events
    assert [
        (
            event["event_kind"],
            event["source_faces_left"],
            event["source_faces_right"],
            event["accepted"],
            event["stale_entry"],
            event.get("resulting_source_faces"),
        )
        for event in events
    ] == [
        ("accepted_merge", [0], [1], True, False, [0, 1]),
        ("eager_stale_prune", [1], [2], False, True, None),
        ("accepted_merge", [0, 1], [2], True, False, [0, 1, 2]),
    ]
    for event in events:
        assert "event_kind" in event
        assert "paper_base_cost" in event
        assert "weighted_priority_cost" in event
        assert "queue_key" in event
        assert event["left_primitive"]
        assert event["right_primitive"]
        assert event["merged_primitive"]
        assert isfinite(event["paper_base_cost"])
        assert isfinite(event["weighted_priority_cost"])
        assert event["queue_key"] == [
            event["weighted_priority_cost"],
            event["paper_base_cost"],
            event["source_faces_left"],
            event["source_faces_right"],
            event["insertion_order"],
        ]
        assert "source_faces_left" in event
        assert "source_faces_right" in event
        assert event["edge_source"] == "topology"
        assert "stale_entry" in event
        assert "accepted" in event
        assert event["blocked"] is False
        assert "active_primitive_count_before" in event
        assert "active_primitive_count_after" in event
        assert "updated_neighbor_insertion_count" in event
        if event["accepted"]:
            assert "resulting_source_faces" in event
    assert accepted_events[-1]["resulting_source_faces"] == [0, 1, 2]
    assert {event["edge_source"] for event in events} == {"topology"}

    disconnected_case = cases["paper_disconnected_components"]
    disconnected_trace = disconnected_case["collapse_trace"]
    assert disconnected_trace["trace_scope"] == "component_pair_priority_queue_trace_fixture"
    assert disconnected_trace["priority_queue_policy"] == "paper_greedy_min_weighted_priority_cost"
    assert disconnected_trace["target_primitive_count"] == 1
    assert disconnected_trace["excess_volume_threshold"] == "default_inf"
    assert disconnected_trace["threshold_policy"] == "disabled"
    assert disconnected_trace["initial_active_groups"] == [[0], [1]]
    assert disconnected_trace["initial_edge_count"] == 0
    assert disconnected_trace["initial_candidates"] == []
    assert disconnected_trace["component_pair_edge_policy"] == (
        "insert_when_topology_queue_exhausted_before_target"
    )
    assert disconnected_trace["topology_queue_exhausted_before_component_pair_insertion"] is True
    assert disconnected_trace["component_pair_edge_insertion_triggered"] is True
    assert disconnected_trace["component_pair_candidate_count"] == 1
    assert disconnected_trace["component_pair_candidate_cap"] == "all_pairs_for_fixture"
    assert disconnected_trace["skipped_component_pair_count"] == 0
    assert disconnected_trace["component_pair_attempted_pair_count"] == 1
    assert disconnected_trace["accepted_merge_count"] == 1
    assert disconnected_trace["stale_entry_skipped_count"] == 0
    assert disconnected_trace["blocked_merge_count"] == 0
    assert disconnected_trace["stop_reason"] == "target_count_reached"
    assert disconnected_trace["final_active_groups"] == [[0, 1]]
    assert disconnected_trace["package_generation_triggered"] is False
    assert disconnected_trace["newton_runtime_triggered"] is False
    assert disconnected_trace["real_usd_triggered"] is False
    assert disconnected_trace["benchmark_triggered"] is False
    assert len(disconnected_trace["events"]) == 1
    component_event = disconnected_trace["events"][0]
    assert component_event["event_kind"] == "accepted_merge"
    assert component_event["edge_source"] == "component_pair"
    assert component_event["source_faces_left"] == [0]
    assert component_event["source_faces_right"] == [1]
    assert component_event["source_faces_merged"] == [0, 1]
    assert isfinite(component_event["paper_base_cost"])
    assert isfinite(component_event["weighted_priority_cost"])
    assert component_event["queue_key"] == [
        component_event["weighted_priority_cost"],
        component_event["paper_base_cost"],
        [0],
        [1],
        component_event["insertion_order"],
    ]
    assert component_event["left_primitive"]
    assert component_event["right_primitive"]
    assert component_event["merged_primitive"]
    assert component_event["accepted"] is True
    assert component_event["blocked"] is False
    assert component_event["stale_entry"] is False
    assert component_event["active_primitive_count_before"] == 2
    assert component_event["active_primitive_count_after"] == 1
    assert component_event["updated_neighbor_insertion_count"] == 0
    assert component_event["resulting_source_faces"] == [0, 1]

    threshold_case = cases["paper_component_pair_threshold_blocked"]
    threshold_trace = threshold_case["collapse_trace"]
    assert threshold_trace["trace_scope"] == "component_pair_priority_queue_trace_fixture"
    assert threshold_trace["target_primitive_count"] == 1
    assert threshold_trace["excess_volume_threshold"] == 0.0
    assert threshold_trace["threshold_policy"] == "component_pair_paper_base_cost_lte_threshold"
    assert threshold_trace["initial_active_groups"] == [[0], [1]]
    assert threshold_trace["initial_edge_count"] == 0
    assert threshold_trace["component_pair_edge_insertion_triggered"] is True
    assert threshold_trace["component_pair_candidate_count"] == 1
    assert threshold_trace["component_pair_candidate_cap"] == "all_pairs_for_fixture"
    assert threshold_trace["skipped_component_pair_count"] == 0
    assert threshold_trace["component_pair_attempted_pair_count"] == 1
    assert threshold_trace["accepted_merge_count"] == 0
    assert threshold_trace["blocked_merge_count"] == 1
    assert threshold_trace["stale_entry_skipped_count"] == 0
    assert threshold_trace["stop_reason"] == "all_remaining_edges_blocked_by_threshold"
    assert threshold_trace["final_active_groups"] == [[0], [1]]
    assert threshold_trace["package_generation_triggered"] is False
    assert threshold_trace["newton_runtime_triggered"] is False
    assert threshold_trace["real_usd_triggered"] is False
    assert threshold_trace["benchmark_triggered"] is False
    assert len(threshold_trace["events"]) == 1
    blocked_event = threshold_trace["events"][0]
    assert blocked_event["event_kind"] == "blocked_by_threshold"
    assert blocked_event["edge_source"] == "component_pair"
    assert blocked_event["source_faces_left"] == [0]
    assert blocked_event["source_faces_right"] == [1]
    assert blocked_event["source_faces_merged"] == [0, 1]
    assert blocked_event["paper_base_cost"] > 0.0
    assert isfinite(blocked_event["paper_base_cost"])
    assert isfinite(blocked_event["weighted_priority_cost"])
    assert blocked_event["queue_key"] == [
        blocked_event["weighted_priority_cost"],
        blocked_event["paper_base_cost"],
        [0],
        [1],
        blocked_event["insertion_order"],
    ]
    assert blocked_event["accepted"] is False
    assert blocked_event["blocked"] is True
    assert blocked_event["blocked_reason"] == "component_pair_threshold_exceeded"
    assert blocked_event["threshold_value"] == 0.0
    assert blocked_event["threshold_metric"] == "paper_base_cost"
    assert blocked_event["stale_entry"] is False
    assert blocked_event["active_primitive_count_before"] == 2
    assert blocked_event["active_primitive_count_after"] == 2
    assert blocked_event["updated_neighbor_insertion_count"] == 0
    assert "resulting_source_faces" not in blocked_event

    nested_case = cases["paper_nested_primitive"]
    assert nested_case["package_generation_triggered"] is False
    assert nested_case["newton_runtime_triggered"] is False
    assert nested_case["real_usd_triggered"] is False
    assert nested_case["benchmark_triggered"] is False
    postprocess = nested_case["postprocess_audit"]
    assert postprocess["audit_scope"] == "enclosed_primitive_culling_fixture"
    assert postprocess["postprocess_input_source"] == "explicit_audit_primitives_not_search_trace"
    assert postprocess["postprocess_policy"] == "remove_primitives_enclosed_by_another_primitive"
    assert postprocess["containment_test_type"] == "obb_corners_inside_obb"
    assert postprocess["axis_policy"] == "shared_identity_axes"
    assert postprocess["input_primitive_count"] == 2
    assert postprocess["output_primitive_count"] == 1
    assert postprocess["enclosed_primitive_ids"] == [1]
    assert postprocess["enclosing_primitive_ids"] == [0]
    assert postprocess["culled_primitive_ids"] == [1]
    assert postprocess["kept_primitive_ids"] == [0]
    assert postprocess["package_generation_triggered"] is False
    assert postprocess["newton_runtime_triggered"] is False
    assert postprocess["real_usd_triggered"] is False
    assert postprocess["benchmark_triggered"] is False

    identity_axes = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    input_primitives = postprocess["input_primitives"]
    assert len(input_primitives) == postprocess["input_primitive_count"]
    assert input_primitives == [
        {
            "primitive_id": 0,
            "kind": "oriented_bounding_box",
            "center": [0.0, 0.0, 0.0],
            "half_extents": [1.0, 1.0, 1.0],
            "axes": identity_axes,
        },
        {
            "primitive_id": 1,
            "kind": "oriented_bounding_box",
            "center": [0.0, 0.0, 0.0],
            "half_extents": [0.25, 0.25, 0.25],
            "axes": identity_axes,
        },
    ]
    assert len(postprocess["kept_primitive_ids"]) == postprocess["output_primitive_count"]
    cull_records = postprocess["cull_records"]
    assert cull_records == [
        {
            "culled_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "cull_reason": "primitive_enclosed_by_larger_primitive",
            "containment_passed": True,
            "tested_corner_count": 8,
        }
    ]
    assert postprocess["culled_primitive_ids"] == [
        record["culled_primitive_id"] for record in cull_records
    ]
    assert postprocess["enclosed_primitive_ids"] == [
        record["culled_primitive_id"] for record in cull_records
    ]
    assert postprocess["enclosing_primitive_ids"] == [
        record["enclosing_primitive_id"] for record in cull_records
    ]


def test_cpd_paper_offline_report_is_strict_json_serializable(cpd_paper_report):
    report = cpd_paper_report

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_paper_offline_report" in encoded


def test_cpd_paper_offline_report_audits_frustum_and_trapezoidal_prism_candidates(cpd_paper_report):
    report = cpd_paper_report
    cases = {case["case_id"]: case for case in report["cases"]}

    frustum_case = cases["paper_frustum_like"]
    frustum_rows = {
        row["paper_primitive"]: row for row in frustum_case["primitive_fit_audit"]["candidates"]
    }
    frustum = frustum_rows["frustum"]
    assert frustum["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert frustum["fit_model"] == "paper_frustum_axis_from_min_cost_flat_cylinder"
    assert frustum["newton_runtime_kind"] == "offline_only_unmapped"
    assert frustum["contains_assigned_points"] is True
    assert frustum["paper_weight"] == 2.1
    frustum_dims = frustum["dimensions"]
    assert frustum_dims["axis_selection_policy"] == "min_volume_flat_cylinder_axis"
    assert frustum_dims["volume_formula"] == "pi*h/3*(rt^2 + rt*rb + rb^2)"
    assert len(frustum_dims["flat_cylinder_axis_candidates"]) == 3
    flat_volumes = [
        row["flat_cylinder_volume"] for row in frustum_dims["flat_cylinder_axis_candidates"]
    ]
    selected_axis = frustum_dims["selected_axis_index"]
    selected_flat = [
        row
        for row in frustum_dims["flat_cylinder_axis_candidates"]
        if row["axis_index"] == selected_axis
    ][0]
    assert selected_flat["flat_cylinder_volume"] == min(flat_volumes)
    assert frustum_dims["height"] > 0.0
    assert frustum_dims["top_radius"] > 0.0
    assert frustum_dims["bottom_radius"] > 0.0
    expected_frustum_volume = (
        pi
        * frustum_dims["height"]
        / 3.0
        * (
            frustum_dims["top_radius"] ** 2
            + frustum_dims["top_radius"] * frustum_dims["bottom_radius"]
            + frustum_dims["bottom_radius"] ** 2
        )
    )
    assert abs(frustum["volume"] - expected_frustum_volume) < 1e-9
    assert abs(frustum["weighted_volume"] - frustum["volume"] * 2.1) < 1e-9

    trap_case = cases["paper_trapezoid_prism_like"]
    trap_rows = {
        row["paper_primitive"]: row for row in trap_case["primitive_fit_audit"]["candidates"]
    }
    trap = trap_rows["trapezoidal_prism"]
    assert trap["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert trap["fit_model"] == "paper_isosceles_trapezoidal_prism_six_axis_orders"
    assert trap["newton_runtime_kind"] == "offline_only_unmapped"
    assert trap["contains_assigned_points"] is True
    assert trap["paper_weight"] == 1.4
    trap_dims = trap["dimensions"]
    assert trap_dims["axis_order_attempt_count"] == 6
    assert sorted(trap_dims["axis_order"]) == [0, 1, 2]
    assert trap_dims["volume_formula"] == "4*h_x*h_y*(h_zt + h_zb)"
    axis_orders = [tuple(row["axis_order"]) for row in trap_dims["axis_order_attempts"]]
    assert set(axis_orders) == {
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2),
        (1, 2, 0),
        (2, 0, 1),
        (2, 1, 0),
    }
    containing_attempts = [
        row for row in trap_dims["axis_order_attempts"] if row["contains_assigned_points"]
    ]
    assert tuple(trap_dims["axis_order"]) in {
        tuple(row["axis_order"])
        for row in containing_attempts
        if row["volume"] == min(attempt["volume"] for attempt in containing_attempts)
    }
    assert all(row["contains_assigned_points"] for row in trap_dims["axis_order_attempts"])
    assert trap_dims["h_x"] > 0.0
    assert trap_dims["h_y"] > 0.0
    assert trap_dims["h_zt"] > 0.0
    assert trap_dims["h_zb"] > 0.0
    expected_trap_volume = (
        4.0 * trap_dims["h_x"] * trap_dims["h_y"] * (trap_dims["h_zt"] + trap_dims["h_zb"])
    )
    assert abs(trap["volume"] - expected_trap_volume) < 1e-9
    assert abs(trap["weighted_volume"] - trap["volume"] * 1.4) < 1e-9


def test_cpd_paper_frustum_and_trapezoidal_prism_stay_out_of_runtime_primitives():
    assert "frustum" not in SUPPORTED_PRIMITIVES
    assert "trapezoidal_prism" not in SUPPORTED_PRIMITIVES
