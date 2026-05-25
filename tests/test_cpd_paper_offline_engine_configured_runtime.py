import pytest

from tests.cpd_paper_offline_shared import *

pytestmark = pytest.mark.paper_offline


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_entry_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
    )
    assert payload["entry_decision"] == "defer_real_runtime_entry"
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
    assert (
        payload["remaining_gaps"]
        == EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_REMAINING_GAPS
    )


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
    )
    assert payload["smoke_decision"] == "skip_real_runtime_smoke"
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


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert payload["runtime_execution_decision"] == ("skip_real_runtime_execution")
    assert payload["runtime_execution_allowed_count"] == 0
    assert payload["runtime_execution_attempted_count"] == 0
    assert payload["runtime_execution_passed_count"] == 0
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_REMAINING_GAPS
    )


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
    )
    assert payload["runtime_lane_review_decision"] == "keep_real_runtime_execution_blocked"
    assert payload["runtime_lane_review_status"] == "claim_boundary_preserved"
    assert payload["real_runtime_execution_evidence"] is False
    assert payload["runtime_compatibility_validated"] is False
    assert payload["runtime_lane_review_recorded_count"] == 1
    assert payload["runtime_lane_claim_boundary_preserved_count"] == 1
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_REMAINING_GAPS
    )


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
    )
    assert payload["configured_runtime_design_decision"] == (
        "define_configured_runtime_inputs_keep_real_runtime_blocked"
    )
    assert payload["configured_runtime_design_status"] == ("input_design_recorded")
    assert payload["configured_runtime_design_recorded_count"] == 1
    assert payload["configured_runtime_preflight_ready_count"] == 0
    assert payload["runtime_source_configuration_required_count"] == 1
    assert payload["runtime_device_configuration_required_count"] == 1
    assert payload["runtime_entry_decision_required_count"] == 1
    assert payload["runtime_smoke_policy_required_count"] == 1
    assert payload["runtime_execution_policy_required_count"] == 1
    assert payload["required_config_keys"] == [
        "newton.source_dir",
        "newton_diagnostic.device",
    ]
    assert payload["required_runtime_input_count"] == 6
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_design_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
    ]
    runtime_lane_review = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
    ]
    source_row = runtime_lane_review[
        "newton_shape_runtime_engine_builder_runtime_lane_review_rows"
    ][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_"
        "runtime_design_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_configured_runtime_design_recorded_"
        "configured_runtime_preflight_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_design_record_not_runtime_config_validation"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_design_contract_"
        "no_config_read_no_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["configured_runtime_design_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
        ),
        "next_configured_runtime_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
        ),
        "required_config_keys": [
            "newton.source_dir",
            "newton_diagnostic.device",
        ],
        "required_runtime_inputs": [
            "newton_source_dir",
            "newton_diagnostic_device",
            "runtime_entry_decision",
            "runtime_smoke_policy",
            "runtime_execution_policy",
            "package_lineage_id",
        ],
        "runtime_entry_decision_policy": ("require_configured_runtime_preflight_before_entry"),
        "runtime_smoke_policy": ("skip_until_configured_runtime_preflight_passes"),
        "runtime_execution_policy": ("skip_until_configured_runtime_preflight_passes"),
        "runtime_lane_review_decision_required": ("keep_real_runtime_execution_blocked"),
        "runtime_config_validation_allowed": False,
        "real_runtime_import_allowed": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_id": source_row[
            "newton_shape_runtime_engine_builder_runtime_lane_review_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_runtime_execution_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_runtime_execution_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_runtime_lane_review_decision": ("keep_real_runtime_execution_blocked"),
        "source_runtime_lane_review_status": "claim_boundary_preserved",
    }
    assert payload["newton_shape_runtime_engine_builder_configured_runtime_design_row_count"] == 1
    assert payload["source_newton_shape_runtime_engine_builder_runtime_lane_review_row_count"] == 1
    assert payload["configured_runtime_design_recorded_count"] == 1
    assert payload["configured_runtime_preflight_ready_count"] == 0
    assert payload["runtime_source_configuration_required_count"] == 1
    assert payload["runtime_device_configuration_required_count"] == 1
    assert payload["runtime_entry_decision_required_count"] == 1
    assert payload["runtime_smoke_policy_required_count"] == 1
    assert payload["runtime_execution_policy_required_count"] == 1
    assert payload["required_config_keys"] == [
        "newton.source_dir",
        "newton_diagnostic.device",
    ]
    assert payload["required_runtime_inputs"] == [
        "newton_source_dir",
        "newton_diagnostic_device",
        "runtime_entry_decision",
        "runtime_smoke_policy",
        "runtime_execution_policy",
        "package_lineage_id",
    ]
    assert payload["required_config_key_count"] == 2
    assert payload["required_runtime_input_count"] == 6
    assert payload["runtime_entry_decision_policy"] == (
        "require_configured_runtime_preflight_before_entry"
    )
    assert payload["runtime_smoke_policy"] == ("skip_until_configured_runtime_preflight_passes")
    assert payload["runtime_execution_policy"] == ("skip_until_configured_runtime_preflight_passes")
    assert payload["configured_runtime_preflight_ready"] is False
    assert payload["runtime_config_validated"] is False
    assert payload["runtime_source_config_resolved"] is False
    assert payload["runtime_device_config_resolved"] is False
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
        "newton_shape_runtime_engine_builder_configured_runtime_design_row_count": 1,
        "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_count": 1,
        "configured_runtime_design_recorded_count": 1,
        "configured_runtime_preflight_ready_count": 0,
        "runtime_source_configuration_required_count": 1,
        "runtime_device_configuration_required_count": 1,
        "runtime_entry_decision_required_count": 1,
        "runtime_smoke_policy_required_count": 1,
        "runtime_execution_policy_required_count": 1,
        "required_config_key_count": 2,
        "required_runtime_input_count": 6,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "configured_runtime_design_decision_distribution": {
            "define_configured_runtime_inputs_keep_real_runtime_blocked": 1
        },
        "configured_runtime_design_status_distribution": {"input_design_recorded": 1},
    }
    row = payload["newton_shape_runtime_engine_builder_configured_runtime_design_rows"][0]
    assert set(row) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_ROW_REQUIRED_KEYS
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_runtime_lane_review_row_id"]
        == (source_row["newton_shape_runtime_engine_builder_runtime_lane_review_row_id"])
    )
    assert row["runtime_lane_review_decision"] == ("keep_real_runtime_execution_blocked")
    assert row["runtime_lane_review_status"] == "claim_boundary_preserved"
    assert row["configured_runtime_design_recorded"] is True
    assert row["configured_runtime_preflight_ready"] is False
    assert row["source_package_copy_forbidden"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_REMAINING_GAPS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT
    )
    assert payload["configured_runtime_preflight_decision"] == (
        "record_configured_runtime_preflight_keep_real_runtime_blocked"
    )
    assert payload["configured_runtime_preflight_status"] == (
        "preflight_recorded_config_validation_missing"
    )
    assert payload["configured_runtime_preflight_recorded_count"] == 1
    assert payload["configured_runtime_preflight_passed_count"] == 1
    assert payload["configured_runtime_validation_ready_count"] == 0
    assert payload["runtime_config_validated"] is False
    assert payload["runtime_source_config_resolved"] is False
    assert payload["runtime_device_config_resolved"] is False
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_preflight_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
    ]
    configured_runtime_design = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
    ]
    source_row = configured_runtime_design[
        "newton_shape_runtime_engine_builder_configured_runtime_design_rows"
    ][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_"
        "runtime_preflight_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_configured_runtime_preflight_recorded_"
        "configured_runtime_validation_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_preflight_record_not_runtime_config_validation"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_preflight_contract_"
        "no_config_read_no_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["configured_runtime_preflight_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
        ),
        "next_configured_runtime_validation_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT
        ),
        "required_config_keys": [
            "newton.source_dir",
            "newton_diagnostic.device",
        ],
        "required_runtime_inputs": [
            "newton_source_dir",
            "newton_diagnostic_device",
            "runtime_entry_decision",
            "runtime_smoke_policy",
            "runtime_execution_policy",
            "package_lineage_id",
        ],
        "runtime_config_validation_allowed": False,
        "real_runtime_import_allowed": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id": source_row[
            "newton_shape_runtime_engine_builder_configured_runtime_design_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_configured_runtime_design_decision": (
            "define_configured_runtime_inputs_keep_real_runtime_blocked"
        ),
        "source_configured_runtime_design_status": "input_design_recorded",
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_configured_runtime_preflight_row_count": 1,
        "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_count": 1,
        "configured_runtime_design_recorded_count": 1,
        "configured_runtime_preflight_recorded_count": 1,
        "configured_runtime_preflight_passed_count": 1,
        "configured_runtime_validation_ready_count": 0,
        "runtime_source_configuration_required_count": 1,
        "runtime_device_configuration_required_count": 1,
        "runtime_entry_decision_required_count": 1,
        "runtime_smoke_policy_required_count": 1,
        "runtime_execution_policy_required_count": 1,
        "required_config_key_count": 2,
        "required_runtime_input_count": 6,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "configured_runtime_preflight_decision_distribution": {
            "record_configured_runtime_preflight_keep_real_runtime_blocked": 1
        },
        "configured_runtime_preflight_status_distribution": {
            "preflight_recorded_config_validation_missing": 1
        },
    }
    row = payload["newton_shape_runtime_engine_builder_configured_runtime_preflight_rows"][0]
    assert set(row) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_ROW_REQUIRED_KEYS
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id"]
        == (source_row["newton_shape_runtime_engine_builder_configured_runtime_design_row_id"])
    )
    assert row["configured_runtime_preflight_recorded"] is True
    assert row["configured_runtime_preflight_passed"] is True
    assert row["configured_runtime_validation_ready"] is False
    assert row["runtime_config_validated"] is False
    assert row["runtime_source_config_resolved"] is False
    assert row["runtime_device_config_resolved"] is False
    assert row["source_package_copy_forbidden"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_REMAINING_GAPS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_preflight_rejects_input_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_design = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
            ]
        )
    )
    configured_runtime_design["unexpected_configured_runtime_preflight_input_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_preflight_input_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract_payload(
            configured_runtime_design
        )

    configured_runtime_design = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
            ]
        )
    )
    configured_runtime_design.pop("coverage_summary")

    with pytest.raises(
        ValueError,
        match="configured_runtime_preflight_input_missing_keys:coverage_summary",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract_payload(
            configured_runtime_design
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_preflight_rejects_source_row_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_design = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
            ]
        )
    )
    configured_runtime_design["newton_shape_runtime_engine_builder_configured_runtime_design_rows"][
        0
    ]["unexpected_configured_runtime_preflight_source_row_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_preflight_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract_payload(
            configured_runtime_design
        )

    configured_runtime_design = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
            ]
        )
    )
    configured_runtime_design["newton_shape_runtime_engine_builder_configured_runtime_design_rows"][
        0
    ].pop("configured_runtime_design_reason")

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_preflight_source_row_missing_keys:configured_runtime_design_reason"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract_payload(
            configured_runtime_design
        )


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT
    )
    assert payload["configured_runtime_validation_decision"] == (
        "record_configured_runtime_validation_keep_real_runtime_blocked"
    )
    assert payload["configured_runtime_validation_status"] == (
        "runtime_config_validation_failed_missing_required_config"
    )
    assert payload["configured_runtime_validation_recorded_count"] == 1
    assert payload["configured_runtime_validation_passed_count"] == 0
    assert payload["configured_runtime_validation_failed_count"] == 1
    assert payload["runtime_config_validated_count"] == 0
    assert payload["runtime_source_config_resolved_count"] == 0
    assert payload["runtime_device_config_resolved_count"] == 0
    assert payload["newton_source_dir_configured"] is False
    assert payload["newton_source_dir"] is None
    assert payload["newton_source_dir_status"] == "not_configured"
    assert payload["newton_diagnostic_device_configured"] is False
    assert payload["newton_diagnostic_device"] is None
    assert payload["newton_diagnostic_device_status"] == "not_configured"
    assert payload["runtime_config_validated"] is False
    assert payload["runtime_source_config_resolved"] is False
    assert payload["runtime_device_config_resolved"] is False
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_validation_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract"
    ]
    configured_runtime_preflight = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
    ]
    source_row = configured_runtime_preflight[
        "newton_shape_runtime_engine_builder_configured_runtime_preflight_rows"
    ][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_"
        "runtime_validation_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_configured_runtime_validation_recorded_"
        "source_resolution_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_validation_record_not_runtime_source_resolution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_validation_contract_"
        "no_config_file_read_no_env_read_no_import_no_model_builder_no_shape_call_"
        "no_finalize_no_runtime"
    )
    assert payload["configured_runtime_validation_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT
        ),
        "next_configured_runtime_source_resolution_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT
        ),
        "required_config_keys": [
            "newton.source_dir",
            "newton_diagnostic.device",
        ],
        "required_runtime_inputs": [
            "newton_source_dir",
            "newton_diagnostic_device",
            "runtime_entry_decision",
            "runtime_smoke_policy",
            "runtime_execution_policy",
            "package_lineage_id",
        ],
        "validation_mode": "report_only_explicit_argument_presence_check",
        "config_file_read_allowed": False,
        "environment_variable_read_allowed": False,
        "source_resolution_allowed": False,
        "real_runtime_import_allowed": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id": source_row[
            "newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_configured_runtime_preflight_decision": (
            "record_configured_runtime_preflight_keep_real_runtime_blocked"
        ),
        "source_configured_runtime_preflight_status": (
            "preflight_recorded_config_validation_missing"
        ),
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_configured_runtime_validation_row_count": 1,
        "source_newton_shape_runtime_engine_builder_configured_runtime_preflight_row_count": 1,
        "configured_runtime_preflight_recorded_count": 1,
        "configured_runtime_preflight_passed_count": 1,
        "configured_runtime_validation_recorded_count": 1,
        "configured_runtime_validation_passed_count": 0,
        "configured_runtime_validation_failed_count": 1,
        "runtime_config_validated_count": 0,
        "runtime_source_config_resolved_count": 0,
        "runtime_device_config_resolved_count": 0,
        "required_config_key_count": 2,
        "required_runtime_input_count": 6,
        "newton_source_dir_configured_count": 0,
        "newton_diagnostic_device_configured_count": 0,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "configured_runtime_validation_decision_distribution": {
            "record_configured_runtime_validation_keep_real_runtime_blocked": 1
        },
        "configured_runtime_validation_status_distribution": {
            "runtime_config_validation_failed_missing_required_config": 1
        },
    }
    row = payload["newton_shape_runtime_engine_builder_configured_runtime_validation_rows"][0]
    assert set(row) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_ROW_REQUIRED_KEYS
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id"]
        == (source_row["newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id"])
    )
    assert row["configured_runtime_validation_recorded"] is True
    assert row["configured_runtime_validation_passed"] is False
    assert row["configured_runtime_validation_failed"] is True
    assert row["configured_runtime_validation_ready"] is True
    assert row["runtime_config_validated"] is False
    assert row["runtime_source_config_resolved"] is False
    assert row["runtime_device_config_resolved"] is False
    assert row["newton_source_dir_configured"] is False
    assert row["newton_source_dir"] is None
    assert row["newton_source_dir_status"] == "not_configured"
    assert row["newton_diagnostic_device_configured"] is False
    assert row["newton_diagnostic_device"] is None
    assert row["newton_diagnostic_device_status"] == "not_configured"
    assert row["newton_diagnostic_device_allowed_values"] == ["cpu", "cuda"]
    assert row["source_package_copy_forbidden"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_REMAINING_GAPS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
    )
    assert payload["configured_runtime_source_resolution_decision"] == (
        "record_configured_runtime_source_resolution_keep_real_runtime_blocked"
    )
    assert payload["configured_runtime_source_resolution_status"] == (
        "runtime_source_resolution_failed_missing_newton_source_dir"
    )
    assert payload["configured_runtime_source_resolution_recorded_count"] == 1
    assert payload["configured_runtime_source_resolution_passed_count"] == 0
    assert payload["configured_runtime_source_resolution_failed_count"] == 1
    assert payload["runtime_config_validated_count"] == 0
    assert payload["runtime_source_config_resolved_count"] == 0
    assert payload["runtime_device_config_resolved_count"] == 0
    assert payload["newton_source_dir_resolution_attempted_count"] == 0
    assert payload["newton_source_dir_configured_count"] == 0
    assert payload["newton_source_dir_resolved_count"] == 0
    assert payload["newton_source_dir_configured"] is False
    assert payload["newton_source_dir"] is None
    assert payload["newton_source_dir_status"] == "not_configured"
    assert payload["newton_source_dir_resolution_attempted"] is False
    assert payload["newton_source_dir_resolution_status"] == ("not_attempted_missing_config")
    assert payload["newton_source_dir_resolution_reason"] == ("newton.source_dir_not_configured")
    assert payload["newton_source_dir_filesystem_probe_allowed"] is False
    assert payload["newton_source_dir_exists"] is None
    assert payload["newton_diagnostic_device_configured"] is False
    assert payload["runtime_config_validated"] is False
    assert payload["runtime_source_config_resolved"] is False
    assert payload["runtime_device_config_resolved"] is False
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract"
    ]
    configured_runtime_validation = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract"
    ]
    source_row = configured_runtime_validation[
        "newton_shape_runtime_engine_builder_configured_runtime_validation_rows"
    ][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_"
        "runtime_source_resolution_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_configured_runtime_source_resolution_recorded_"
        "device_resolution_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_source_resolution_record_"
        "not_runtime_device_resolution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_source_resolution_"
        "contract_no_config_file_read_no_env_read_no_filesystem_probe_no_import_"
        "no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["configured_runtime_source_resolution_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT
        ),
        "next_configured_runtime_device_resolution_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
        ),
        "required_source_config_key": "newton.source_dir",
        "required_config_keys": [
            "newton.source_dir",
            "newton_diagnostic.device",
        ],
        "required_runtime_inputs": [
            "newton_source_dir",
            "newton_diagnostic_device",
            "runtime_entry_decision",
            "runtime_smoke_policy",
            "runtime_execution_policy",
            "package_lineage_id",
        ],
        "source_resolution_mode": "report_only_missing_config_resolution_record",
        "config_file_read_allowed": False,
        "environment_variable_read_allowed": False,
        "filesystem_probe_allowed": False,
        "real_runtime_import_allowed": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_configured_runtime_validation_row_id": source_row[
            "newton_shape_runtime_engine_builder_configured_runtime_validation_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_configured_runtime_validation_status": (
            "runtime_config_validation_failed_missing_required_config"
        ),
        "source_newton_source_dir_status": "not_configured",
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_count": 1,
        "source_newton_shape_runtime_engine_builder_configured_runtime_validation_row_count": 1,
        "configured_runtime_validation_recorded_count": 1,
        "configured_runtime_validation_passed_count": 0,
        "configured_runtime_validation_failed_count": 1,
        "configured_runtime_source_resolution_recorded_count": 1,
        "configured_runtime_source_resolution_passed_count": 0,
        "configured_runtime_source_resolution_failed_count": 1,
        "runtime_config_validated_count": 0,
        "runtime_source_config_resolved_count": 0,
        "runtime_device_config_resolved_count": 0,
        "newton_source_dir_resolution_attempted_count": 0,
        "newton_source_dir_configured_count": 0,
        "newton_source_dir_resolved_count": 0,
        "required_config_key_count": 2,
        "required_runtime_input_count": 6,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "configured_runtime_source_resolution_decision_distribution": {
            "record_configured_runtime_source_resolution_keep_real_runtime_blocked": 1
        },
        "configured_runtime_source_resolution_status_distribution": {
            "runtime_source_resolution_failed_missing_newton_source_dir": 1
        },
        "newton_source_dir_resolution_status_distribution": {"not_attempted_missing_config": 1},
    }
    row = payload["newton_shape_runtime_engine_builder_configured_runtime_source_resolution_rows"][
        0
    ]
    assert set(row) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_ROW_REQUIRED_KEYS
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_configured_runtime_validation_row_id"]
        == (source_row["newton_shape_runtime_engine_builder_configured_runtime_validation_row_id"])
    )
    assert row["configured_runtime_source_resolution_recorded"] is True
    assert row["configured_runtime_source_resolution_passed"] is False
    assert row["configured_runtime_source_resolution_failed"] is True
    assert row["configured_runtime_source_resolution_ready"] is True
    assert row["runtime_config_validated"] is False
    assert row["runtime_source_config_resolved"] is False
    assert row["runtime_device_config_resolved"] is False
    assert row["newton_source_dir_configured"] is False
    assert row["newton_source_dir"] is None
    assert row["newton_source_dir_status"] == "not_configured"
    assert row["newton_source_dir_resolution_attempted"] is False
    assert row["newton_source_dir_resolution_status"] == ("not_attempted_missing_config")
    assert row["newton_source_dir_resolution_reason"] == ("newton.source_dir_not_configured")
    assert row["newton_source_dir_filesystem_probe_allowed"] is False
    assert row["newton_source_dir_exists"] is None
    assert row["configured_runtime_device_resolution_gate_required"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
    )
    assert row["source_package_copy_forbidden"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_REMAINING_GAPS
    )
    for (
        flag
    ) in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_rejects_input_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_validation = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract"
            ]
        )
    )
    configured_runtime_validation["unexpected_configured_runtime_source_resolution_input_key"] = (
        True
    )

    with pytest.raises(
        ValueError,
        match="configured_runtime_source_resolution_input_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract_payload(
            configured_runtime_validation
        )

    configured_runtime_validation = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract"
            ]
        )
    )
    configured_runtime_validation.pop("coverage_summary")

    with pytest.raises(
        ValueError,
        match=("configured_runtime_source_resolution_input_missing_keys:coverage_summary"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract_payload(
            configured_runtime_validation
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_rejects_source_row_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_validation = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract"
            ]
        )
    )
    configured_runtime_validation[
        "newton_shape_runtime_engine_builder_configured_runtime_validation_rows"
    ][0]["unexpected_configured_runtime_source_resolution_source_row_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_source_resolution_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract_payload(
            configured_runtime_validation
        )

    configured_runtime_validation = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract"
            ]
        )
    )
    configured_runtime_validation[
        "newton_shape_runtime_engine_builder_configured_runtime_validation_rows"
    ][0].pop("configured_runtime_validation_reason")

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_source_resolution_source_row_missing_keys:"
            "configured_runtime_validation_reason"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract_payload(
            configured_runtime_validation
        )


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == [
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_run_contract_missing"
        ),
    ]
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_REMAINING_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
    )
    assert payload["configured_runtime_device_resolution_decision"] == (
        "record_configured_runtime_device_resolution_keep_real_runtime_blocked"
    )
    assert payload["configured_runtime_device_resolution_status"] == (
        "runtime_device_resolution_failed_missing_newton_diagnostic_device"
    )
    assert payload["configured_runtime_device_resolution_recorded_count"] == 1
    assert payload["configured_runtime_device_resolution_passed_count"] == 0
    assert payload["configured_runtime_device_resolution_failed_count"] == 1
    assert payload["runtime_config_validated_count"] == 0
    assert payload["runtime_source_config_resolved_count"] == 0
    assert payload["runtime_device_config_resolved_count"] == 0
    assert payload["newton_diagnostic_device_resolution_attempted_count"] == 0
    assert payload["newton_diagnostic_device_configured_count"] == 0
    assert payload["newton_diagnostic_device_resolved_count"] == 0
    assert payload["newton_diagnostic_device_configured"] is False
    assert payload["newton_diagnostic_device"] is None
    assert payload["newton_diagnostic_device_status"] == "not_configured"
    assert payload["newton_diagnostic_device_resolution_attempted"] is False
    assert payload["newton_diagnostic_device_resolution_status"] == ("not_attempted_missing_config")
    assert payload["newton_diagnostic_device_resolution_reason"] == (
        "newton_diagnostic.device_not_configured"
    )
    assert payload["runtime_config_validated"] is False
    assert payload["runtime_source_config_resolved"] is False
    assert payload["runtime_device_config_resolved"] is False
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
    ]
    configured_runtime_source_resolution = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract"
    ]
    source_row = configured_runtime_source_resolution[
        "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_rows"
    ][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_"
        "runtime_device_resolution_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_configured_runtime_device_resolution_recorded_"
        "entry_decision_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_device_resolution_record_"
        "not_runtime_entry_decision"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_device_resolution_"
        "contract_no_config_file_read_no_env_read_no_filesystem_probe_no_import_"
        "no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["configured_runtime_device_resolution_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
        ),
        "next_configured_runtime_entry_decision_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
        ),
        "required_device_config_key": "newton_diagnostic.device",
        "allowed_device_values": ["cpu", "cuda"],
        "device_resolution_mode": "report_only_missing_config_resolution_record",
        "config_file_read_allowed": False,
        "environment_variable_read_allowed": False,
        "filesystem_probe_allowed": False,
        "real_runtime_import_allowed": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_id": source_row[
            "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_configured_runtime_validation_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_validation_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_configured_runtime_source_resolution_status": (
            "runtime_source_resolution_failed_missing_newton_source_dir"
        ),
        "source_newton_diagnostic_device_status": "not_configured",
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_count": 1,
        "source_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_count": 1,
        "configured_runtime_source_resolution_recorded_count": 1,
        "configured_runtime_source_resolution_passed_count": 0,
        "configured_runtime_source_resolution_failed_count": 1,
        "configured_runtime_device_resolution_recorded_count": 1,
        "configured_runtime_device_resolution_passed_count": 0,
        "configured_runtime_device_resolution_failed_count": 1,
        "runtime_config_validated_count": 0,
        "runtime_source_config_resolved_count": 0,
        "runtime_device_config_resolved_count": 0,
        "newton_source_dir_resolution_attempted_count": 0,
        "newton_source_dir_configured_count": 0,
        "newton_source_dir_resolved_count": 0,
        "newton_diagnostic_device_resolution_attempted_count": 0,
        "newton_diagnostic_device_configured_count": 0,
        "newton_diagnostic_device_resolved_count": 0,
        "required_config_key_count": 2,
        "required_runtime_input_count": 6,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "configured_runtime_device_resolution_decision_distribution": {
            "record_configured_runtime_device_resolution_keep_real_runtime_blocked": 1
        },
        "configured_runtime_device_resolution_status_distribution": {
            "runtime_device_resolution_failed_missing_newton_diagnostic_device": 1
        },
        "newton_diagnostic_device_resolution_status_distribution": {
            "not_attempted_missing_config": 1
        },
    }
    row = payload["newton_shape_runtime_engine_builder_configured_runtime_device_resolution_rows"][
        0
    ]
    assert set(row) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_ROW_REQUIRED_KEYS
    )
    assert (
        row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_id"
        ]
        == (
            source_row[
                "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_id"
            ]
        )
    )
    assert row["configured_runtime_device_resolution_recorded"] is True
    assert row["configured_runtime_device_resolution_passed"] is False
    assert row["configured_runtime_device_resolution_failed"] is True
    assert row["configured_runtime_device_resolution_ready"] is True
    assert row["runtime_config_validated"] is False
    assert row["runtime_source_config_resolved"] is False
    assert row["runtime_device_config_resolved"] is False
    assert row["newton_diagnostic_device_configured"] is False
    assert row["newton_diagnostic_device"] is None
    assert row["newton_diagnostic_device_status"] == "not_configured"
    assert row["newton_diagnostic_device_resolution_attempted"] is False
    assert row["newton_diagnostic_device_resolution_status"] == ("not_attempted_missing_config")
    assert row["newton_diagnostic_device_resolution_reason"] == (
        "newton_diagnostic.device_not_configured"
    )
    assert row["configured_runtime_entry_decision_gate_required"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
    )
    assert row["source_package_copy_forbidden"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_REMAINING_GAPS
    )
    for (
        flag
    ) in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_rejects_input_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_source_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract"
            ]
        )
    )
    configured_runtime_source_resolution[
        "unexpected_configured_runtime_device_resolution_input_key"
    ] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_device_resolution_input_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract_payload(
            configured_runtime_source_resolution
        )

    configured_runtime_source_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract"
            ]
        )
    )
    configured_runtime_source_resolution.pop("coverage_summary")

    with pytest.raises(
        ValueError,
        match=("configured_runtime_device_resolution_input_missing_keys:coverage_summary"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract_payload(
            configured_runtime_source_resolution
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_rejects_source_row_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_source_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract"
            ]
        )
    )
    configured_runtime_source_resolution[
        "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_rows"
    ][0]["unexpected_configured_runtime_device_resolution_source_row_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_device_resolution_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract_payload(
            configured_runtime_source_resolution
        )

    configured_runtime_source_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract"
            ]
        )
    )
    configured_runtime_source_resolution[
        "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_rows"
    ][0].pop("configured_runtime_source_resolution_reason")

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_device_resolution_source_row_missing_keys:"
            "configured_runtime_source_resolution_reason"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract_payload(
            configured_runtime_source_resolution
        )


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == [
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_run_contract_missing"
        ),
    ]
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_REMAINING_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
    )
    assert payload["configured_runtime_entry_decision"] == (
        "defer_real_runtime_entry_missing_configured_runtime_source_or_device"
    )
    assert payload["configured_runtime_entry_decision_status"] == (
        "runtime_entry_deferred_missing_configured_runtime_source_or_device"
    )
    assert payload["configured_runtime_entry_decision_recorded_count"] == 1
    assert payload["configured_runtime_entry_decision_passed_count"] == 0
    assert payload["configured_runtime_entry_decision_failed_count"] == 1
    assert payload["runtime_entry_allowed_count"] == 0
    assert payload["runtime_entry_attempted_count"] == 0
    assert payload["runtime_entry_passed_count"] == 0
    assert payload["runtime_entry_allowed"] is False
    assert payload["runtime_entry_attempted"] is False
    assert payload["runtime_entry_passed"] is False
    assert payload["runtime_config_validated_count"] == 0
    assert payload["runtime_source_config_resolved_count"] == 0
    assert payload["runtime_device_config_resolved_count"] == 0
    assert payload["newton_source_dir_configured"] is False
    assert payload["newton_source_dir"] is None
    assert payload["newton_diagnostic_device_configured"] is False
    assert payload["newton_diagnostic_device"] is None
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
    ]
    configured_runtime_device_resolution = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
    ]
    source_row = configured_runtime_device_resolution[
        "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_rows"
    ][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_"
        "runtime_entry_decision_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_configured_runtime_entry_decision_recorded_smoke_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_entry_decision_record_not_runtime_smoke"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_entry_decision_"
        "contract_no_config_file_read_no_env_read_no_filesystem_probe_no_import_"
        "no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["configured_runtime_entry_decision_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
        ),
        "next_configured_runtime_smoke_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
        ),
        "entry_decision_mode": ("report_only_missing_source_or_device_runtime_entry_decision"),
        "runtime_entry_allowed_when": ("runtime_config_validated_and_source_and_device_resolved"),
        "config_file_read_allowed": False,
        "environment_variable_read_allowed": False,
        "filesystem_probe_allowed": False,
        "real_runtime_import_allowed": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id": source_row[
            "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_configured_runtime_device_resolution_status": (
            "runtime_device_resolution_failed_missing_newton_diagnostic_device"
        ),
        "source_runtime_source_config_resolved": False,
        "source_runtime_device_config_resolved": False,
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_count": 1,
        "source_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_count": 1,
        "configured_runtime_source_resolution_recorded_count": 1,
        "configured_runtime_source_resolution_passed_count": 0,
        "configured_runtime_source_resolution_failed_count": 1,
        "configured_runtime_device_resolution_recorded_count": 1,
        "configured_runtime_device_resolution_passed_count": 0,
        "configured_runtime_device_resolution_failed_count": 1,
        "configured_runtime_entry_decision_recorded_count": 1,
        "configured_runtime_entry_decision_passed_count": 0,
        "configured_runtime_entry_decision_failed_count": 1,
        "runtime_config_validated_count": 0,
        "runtime_source_config_resolved_count": 0,
        "runtime_device_config_resolved_count": 0,
        "runtime_entry_allowed_count": 0,
        "runtime_entry_attempted_count": 0,
        "runtime_entry_passed_count": 0,
        "newton_source_dir_resolution_attempted_count": 0,
        "newton_source_dir_configured_count": 0,
        "newton_source_dir_resolved_count": 0,
        "newton_diagnostic_device_resolution_attempted_count": 0,
        "newton_diagnostic_device_configured_count": 0,
        "newton_diagnostic_device_resolved_count": 0,
        "required_config_key_count": 2,
        "required_runtime_input_count": 6,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "configured_runtime_entry_decision_distribution": {
            "defer_real_runtime_entry_missing_configured_runtime_source_or_device": 1
        },
        "configured_runtime_entry_decision_status_distribution": {
            "runtime_entry_deferred_missing_configured_runtime_source_or_device": 1
        },
    }
    row = payload["newton_shape_runtime_engine_builder_configured_runtime_entry_decision_rows"][0]
    assert set(row) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_ROW_REQUIRED_KEYS
    )
    assert (
        row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id"
        ]
        == (
            source_row[
                "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id"
            ]
        )
    )
    assert row["configured_runtime_entry_decision"] == (
        "defer_real_runtime_entry_missing_configured_runtime_source_or_device"
    )
    assert row["configured_runtime_entry_decision_reason"] == (
        "configured_runtime_source_or_device_not_resolved"
    )
    assert row["configured_runtime_entry_decision_status"] == (
        "runtime_entry_deferred_missing_configured_runtime_source_or_device"
    )
    assert row["configured_runtime_entry_decision_recorded"] is True
    assert row["configured_runtime_entry_decision_passed"] is False
    assert row["configured_runtime_entry_decision_failed"] is True
    assert row["configured_runtime_entry_decision_ready"] is True
    assert row["runtime_entry_allowed"] is False
    assert row["runtime_entry_attempted"] is False
    assert row["runtime_entry_passed"] is False
    assert row["runtime_config_validated"] is False
    assert row["runtime_source_config_resolved"] is False
    assert row["runtime_device_config_resolved"] is False
    assert row["configured_runtime_smoke_gate_required"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
    )
    assert row["source_package_copy_forbidden"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_REMAINING_GAPS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_rejects_input_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_device_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
            ]
        )
    )
    configured_runtime_device_resolution[
        "unexpected_configured_runtime_entry_decision_input_key"
    ] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_entry_decision_input_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract_payload(
            configured_runtime_device_resolution
        )

    configured_runtime_device_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
            ]
        )
    )
    configured_runtime_device_resolution.pop("coverage_summary")

    with pytest.raises(
        ValueError,
        match=("configured_runtime_entry_decision_input_missing_keys:coverage_summary"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract_payload(
            configured_runtime_device_resolution
        )

    configured_runtime_device_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
            ]
        )
    )
    configured_runtime_device_resolution["coverage_summary"]["real_newton_import_count"] = 1

    with pytest.raises(
        ValueError,
        match=("configured_runtime_entry_decision_input_nested_mismatch:coverage_summary"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract_payload(
            configured_runtime_device_resolution
        )

    configured_runtime_device_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
            ]
        )
    )
    configured_runtime_device_resolution["input_contract_summary"]["input_gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match=("configured_runtime_entry_decision_input_nested_mismatch:input_contract_summary"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract_payload(
            configured_runtime_device_resolution
        )

    configured_runtime_device_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
            ]
        )
    )
    configured_runtime_device_resolution["configured_runtime_device_resolution_contract"][
        "real_runtime_import_allowed"
    ] = True

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_entry_decision_input_nested_mismatch:"
            "configured_runtime_device_resolution_contract"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract_payload(
            configured_runtime_device_resolution
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_rejects_source_row_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_device_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
            ]
        )
    )
    configured_runtime_device_resolution[
        "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_rows"
    ][0]["unexpected_configured_runtime_entry_decision_source_row_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_entry_decision_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract_payload(
            configured_runtime_device_resolution
        )

    configured_runtime_device_resolution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"
            ]
        )
    )
    configured_runtime_device_resolution[
        "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_rows"
    ][0].pop("configured_runtime_device_resolution_reason")

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_entry_decision_source_row_missing_keys:"
            "configured_runtime_device_resolution_reason"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract_payload(
            configured_runtime_device_resolution
        )


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == [
        (
            "paper_mapped_subset_newton_shape_runtime_engine_builder_"
            "configured_runtime_run_contract_missing"
        ),
    ]
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_REMAINING_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
    )
    assert payload["configured_runtime_smoke_decision"] == (
        "skip_real_runtime_smoke_missing_configured_runtime_entry"
    )
    assert payload["configured_runtime_smoke_status"] == (
        "runtime_smoke_skipped_missing_configured_runtime_entry"
    )
    assert payload["configured_runtime_smoke_recorded_count"] == 1
    assert payload["configured_runtime_smoke_passed_count"] == 0
    assert payload["configured_runtime_smoke_failed_count"] == 1
    assert payload["configured_runtime_smoke_allowed_count"] == 0
    assert payload["configured_runtime_smoke_attempted_count"] == 0
    assert payload["runtime_entry_allowed_count"] == 0
    assert payload["runtime_entry_attempted_count"] == 0
    assert payload["runtime_entry_passed_count"] == 0
    assert payload["configured_runtime_smoke_allowed"] is False
    assert payload["configured_runtime_smoke_attempted"] is False
    assert payload["configured_runtime_smoke_passed"] is False
    assert payload["runtime_entry_allowed"] is False
    assert payload["runtime_entry_attempted"] is False
    assert payload["runtime_entry_passed"] is False
    assert payload["runtime_config_validated_count"] == 0
    assert payload["runtime_source_config_resolved_count"] == 0
    assert payload["runtime_device_config_resolved_count"] == 0
    assert payload["newton_source_dir_configured"] is False
    assert payload["newton_source_dir"] is None
    assert payload["newton_diagnostic_device_configured"] is False
    assert payload["newton_diagnostic_device"] is None
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_smoke_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
    ]
    configured_runtime_entry_decision = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
    ]
    source_row = configured_runtime_entry_decision[
        "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_rows"
    ][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_"
        "runtime_smoke_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_configured_runtime_smoke_recorded_execution_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_smoke_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_smoke_contract_"
        "no_config_file_read_no_env_read_no_filesystem_probe_no_import_"
        "no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["configured_runtime_smoke_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
        ),
        "next_configured_runtime_execution_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
        ),
        "smoke_mode": "report_only_skip_missing_runtime_entry",
        "runtime_smoke_allowed_when": ("runtime_entry_allowed_and_attempted_and_passed"),
        "config_file_read_allowed": False,
        "environment_variable_read_allowed": False,
        "filesystem_probe_allowed": False,
        "real_runtime_import_allowed": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_id": source_row[
            "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_configured_runtime_entry_decision_status": (
            "runtime_entry_deferred_missing_configured_runtime_source_or_device"
        ),
        "source_runtime_entry_allowed": False,
        "source_runtime_entry_passed": False,
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_configured_runtime_smoke_row_count": 1,
        "source_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_count": 1,
        "configured_runtime_source_resolution_recorded_count": 1,
        "configured_runtime_source_resolution_passed_count": 0,
        "configured_runtime_source_resolution_failed_count": 1,
        "configured_runtime_device_resolution_recorded_count": 1,
        "configured_runtime_device_resolution_passed_count": 0,
        "configured_runtime_device_resolution_failed_count": 1,
        "configured_runtime_entry_decision_recorded_count": 1,
        "configured_runtime_entry_decision_passed_count": 0,
        "configured_runtime_entry_decision_failed_count": 1,
        "configured_runtime_smoke_recorded_count": 1,
        "configured_runtime_smoke_passed_count": 0,
        "configured_runtime_smoke_failed_count": 1,
        "runtime_config_validated_count": 0,
        "runtime_source_config_resolved_count": 0,
        "runtime_device_config_resolved_count": 0,
        "runtime_entry_allowed_count": 0,
        "runtime_entry_attempted_count": 0,
        "runtime_entry_passed_count": 0,
        "configured_runtime_smoke_allowed_count": 0,
        "configured_runtime_smoke_attempted_count": 0,
        "newton_source_dir_resolution_attempted_count": 0,
        "newton_source_dir_configured_count": 0,
        "newton_source_dir_resolved_count": 0,
        "newton_diagnostic_device_resolution_attempted_count": 0,
        "newton_diagnostic_device_configured_count": 0,
        "newton_diagnostic_device_resolved_count": 0,
        "required_config_key_count": 2,
        "required_runtime_input_count": 6,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "configured_runtime_smoke_decision_distribution": {
            "skip_real_runtime_smoke_missing_configured_runtime_entry": 1
        },
        "configured_runtime_smoke_status_distribution": {
            "runtime_smoke_skipped_missing_configured_runtime_entry": 1
        },
    }
    row = payload["newton_shape_runtime_engine_builder_configured_runtime_smoke_rows"][0]
    assert set(row) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_ROW_REQUIRED_KEYS
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_id"]
        == (
            source_row[
                "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_id"
            ]
        )
    )
    assert row["configured_runtime_smoke_decision"] == (
        "skip_real_runtime_smoke_missing_configured_runtime_entry"
    )
    assert row["configured_runtime_smoke_reason"] == ("configured_runtime_entry_not_allowed")
    assert row["configured_runtime_smoke_status"] == (
        "runtime_smoke_skipped_missing_configured_runtime_entry"
    )
    assert row["configured_runtime_smoke_recorded"] is True
    assert row["configured_runtime_smoke_passed"] is False
    assert row["configured_runtime_smoke_failed"] is True
    assert row["configured_runtime_smoke_ready"] is True
    assert row["configured_runtime_smoke_allowed"] is False
    assert row["configured_runtime_smoke_attempted"] is False
    assert row["runtime_entry_allowed"] is False
    assert row["runtime_entry_attempted"] is False
    assert row["runtime_entry_passed"] is False
    assert row["configured_runtime_execution_gate_required"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
    )
    assert row["source_package_copy_forbidden"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_REMAINING_GAPS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_smoke_rejects_input_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision["unexpected_configured_runtime_smoke_input_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_smoke_input_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )

    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision.pop("coverage_summary")

    with pytest.raises(
        ValueError,
        match="configured_runtime_smoke_input_missing_keys:coverage_summary",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )

    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision["coverage_summary"]["real_newton_import_count"] = 1

    with pytest.raises(
        ValueError,
        match="configured_runtime_smoke_input_nested_mismatch:coverage_summary",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )

    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision["input_contract_summary"]["input_gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="configured_runtime_smoke_input_nested_mismatch:input_contract_summary",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )

    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision["configured_runtime_entry_decision_contract"][
        "real_runtime_import_allowed"
    ] = True

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_smoke_input_nested_mismatch:"
            "configured_runtime_entry_decision_contract"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        ("gate_id", "stale_gate", "configured_runtime_smoke_input_gate_id_mismatch"),
        (
            "next_required_gate",
            "stale_gate",
            "configured_runtime_smoke_input_next_gate_mismatch",
        ),
        (
            "remaining_gaps",
            ["stale_gate"],
            "configured_runtime_smoke_input_remaining_gaps_mismatch",
        ),
        (
            "configured_runtime_entry_decision_status",
            "runtime_entry_allowed",
            "configured_runtime_smoke_input_metadata_mismatch:"
            "configured_runtime_entry_decision_status",
        ),
        (
            "runtime_entry_allowed_count",
            1,
            "configured_runtime_smoke_input_metadata_mismatch:runtime_entry_allowed_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "configured_runtime_smoke_input_count_mismatch:newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_smoke_rejects_input_value_drift(
    field_name,
    bad_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision[field_name] = bad_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        (
            "runtime_entry_allowed",
            True,
            "configured_runtime_smoke_input_flag_true:runtime_entry_allowed",
        ),
        (
            "configured_runtime_entry_decision_ready",
            False,
            "configured_runtime_smoke_input_flag_false:configured_runtime_entry_decision_ready",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_smoke_rejects_input_flag_drift(
    field_name,
    bad_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision[field_name] = bad_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_smoke_rejects_source_row_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision[
        "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_rows"
    ][0]["unexpected_configured_runtime_smoke_source_row_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_smoke_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )

    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision[
        "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_rows"
    ][0].pop("configured_runtime_entry_decision_reason")

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_smoke_source_row_missing_keys:"
            "configured_runtime_entry_decision_reason"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )


@pytest.mark.parametrize(
    ("rows_value", "message"),
    [
        ([], "configured_runtime_smoke_row_count_mismatch"),
        ("not_rows", "configured_runtime_smoke_row_count_mismatch"),
        ([None], "configured_runtime_smoke_row_count_mismatch"),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_smoke_rejects_row_count_drift(
    rows_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision[
        "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_rows"
    ] = rows_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        (
            "source_package_id",
            "stale_package",
            "configured_runtime_smoke_source_row_mismatch:source_package_id",
        ),
        (
            "configured_runtime_entry_decision_reason",
            "runtime_entry_allowed",
            "configured_runtime_smoke_source_row_mismatch:configured_runtime_entry_decision_reason",
        ),
        (
            "runtime_entry_allowed",
            True,
            "configured_runtime_smoke_source_row_mismatch:runtime_entry_allowed",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "configured_runtime_smoke_source_row_count_mismatch:newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_smoke_rejects_source_row_value_drift(
    field_name,
    bad_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_entry_decision = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"
            ]
        )
    )
    configured_runtime_entry_decision[
        "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_rows"
    ][0][field_name] = bad_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract_payload(
            configured_runtime_entry_decision
        )


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == [(EXPECTED_CURRENT_REPORT_NEXT_GATE + "_missing")]
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert (
        report[
            "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
        ]["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
    )
    assert (
        payload["gate_id"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
    )
    assert (
        payload["input_gate_id"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert payload["configured_runtime_execution_decision"] == (
        "skip_real_runtime_execution_configured_runtime_smoke_not_allowed"
    )
    assert payload["configured_runtime_execution_recorded_count"] == 1
    assert payload["configured_runtime_execution_passed_count"] == 0
    assert payload["configured_runtime_execution_failed_count"] == 1
    assert payload["configured_runtime_execution_allowed_count"] == 0
    assert payload["configured_runtime_execution_attempted_count"] == 0
    assert payload["configured_runtime_smoke_allowed_count"] == 0
    assert payload["configured_runtime_smoke_attempted_count"] == 0
    assert payload["runtime_entry_allowed_count"] == 0
    assert payload["runtime_entry_attempted_count"] == 0
    assert payload["runtime_entry_passed_count"] == 0
    assert payload["configured_runtime_execution_allowed"] is False
    assert payload["configured_runtime_execution_attempted"] is False
    assert payload["configured_runtime_execution_passed"] is False
    assert payload["configured_runtime_smoke_allowed"] is False
    assert payload["configured_runtime_smoke_attempted"] is False
    assert payload["configured_runtime_smoke_passed"] is False
    assert payload["runtime_entry_allowed"] is False
    assert payload["runtime_entry_attempted"] is False
    assert payload["runtime_entry_passed"] is False
    assert payload["runtime_source_config_resolved"] is False
    assert payload["runtime_device_config_resolved"] is False
    assert payload["newton_source_dir"] is None
    assert payload["newton_diagnostic_device"] is None
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_execution_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
    ]
    configured_runtime_smoke = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
    ]
    source_row = configured_runtime_smoke[
        "newton_shape_runtime_engine_builder_configured_runtime_smoke_rows"
    ][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_"
        "runtime_execution_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_configured_runtime_execution_recorded_lane_review_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_execution_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_execution_contract_"
        "no_config_file_read_no_env_read_no_filesystem_probe_no_import_"
        "no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["configured_runtime_execution_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
        ),
        "next_configured_runtime_lane_review_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT
        ),
        "execution_mode": "report_only_skip_smoke_not_allowed",
        "runtime_execution_allowed_when": (
            "configured_runtime_smoke_allowed_and_attempted_and_passed"
        ),
        "config_file_read_allowed": False,
        "environment_variable_read_allowed": False,
        "filesystem_probe_allowed": False,
        "real_runtime_import_allowed": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_configured_runtime_smoke_row_id": source_row[
            "newton_shape_runtime_engine_builder_configured_runtime_smoke_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_configured_runtime_smoke_status": (
            "runtime_smoke_skipped_missing_configured_runtime_entry"
        ),
        "source_configured_runtime_smoke_allowed": False,
        "source_configured_runtime_smoke_passed": False,
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_configured_runtime_execution_row_count": 1,
        "source_newton_shape_runtime_engine_builder_configured_runtime_smoke_row_count": 1,
        "configured_runtime_source_resolution_recorded_count": 1,
        "configured_runtime_source_resolution_passed_count": 0,
        "configured_runtime_source_resolution_failed_count": 1,
        "configured_runtime_device_resolution_recorded_count": 1,
        "configured_runtime_device_resolution_passed_count": 0,
        "configured_runtime_device_resolution_failed_count": 1,
        "configured_runtime_entry_decision_recorded_count": 1,
        "configured_runtime_entry_decision_passed_count": 0,
        "configured_runtime_entry_decision_failed_count": 1,
        "configured_runtime_smoke_recorded_count": 1,
        "configured_runtime_smoke_passed_count": 0,
        "configured_runtime_smoke_failed_count": 1,
        "configured_runtime_execution_recorded_count": 1,
        "configured_runtime_execution_passed_count": 0,
        "configured_runtime_execution_failed_count": 1,
        "runtime_config_validated_count": 0,
        "runtime_source_config_resolved_count": 0,
        "runtime_device_config_resolved_count": 0,
        "runtime_entry_allowed_count": 0,
        "runtime_entry_attempted_count": 0,
        "runtime_entry_passed_count": 0,
        "configured_runtime_smoke_allowed_count": 0,
        "configured_runtime_smoke_attempted_count": 0,
        "configured_runtime_execution_allowed_count": 0,
        "configured_runtime_execution_attempted_count": 0,
        "newton_source_dir_resolution_attempted_count": 0,
        "newton_source_dir_configured_count": 0,
        "newton_source_dir_resolved_count": 0,
        "newton_diagnostic_device_resolution_attempted_count": 0,
        "newton_diagnostic_device_configured_count": 0,
        "newton_diagnostic_device_resolved_count": 0,
        "required_config_key_count": 2,
        "required_runtime_input_count": 6,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "configured_runtime_execution_decision_distribution": {
            "skip_real_runtime_execution_configured_runtime_smoke_not_allowed": 1
        },
        "configured_runtime_execution_status_distribution": {
            "runtime_execution_skipped_configured_runtime_smoke_not_allowed": 1
        },
    }
    row = payload["newton_shape_runtime_engine_builder_configured_runtime_execution_rows"][0]
    assert set(row) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_ROW_REQUIRED_KEYS
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_configured_runtime_smoke_row_id"]
        == (source_row["newton_shape_runtime_engine_builder_configured_runtime_smoke_row_id"])
    )
    assert row["configured_runtime_execution_decision"] == (
        "skip_real_runtime_execution_configured_runtime_smoke_not_allowed"
    )
    assert row["configured_runtime_execution_reason"] == ("configured_runtime_smoke_not_allowed")
    assert row["configured_runtime_execution_status"] == (
        "runtime_execution_skipped_configured_runtime_smoke_not_allowed"
    )
    assert row["configured_runtime_execution_recorded"] is True
    assert row["configured_runtime_execution_passed"] is False
    assert row["configured_runtime_execution_failed"] is True
    assert row["configured_runtime_execution_ready"] is True
    assert row["configured_runtime_execution_allowed"] is False
    assert row["configured_runtime_execution_attempted"] is False
    assert row["configured_runtime_smoke_allowed"] is False
    assert row["configured_runtime_smoke_attempted"] is False
    assert row["configured_runtime_smoke_passed"] is False
    assert row["runtime_entry_allowed"] is False
    assert row["runtime_entry_attempted"] is False
    assert row["runtime_entry_passed"] is False
    assert row["real_newton_import_count"] == 0
    assert row["real_warp_import_count"] == 0
    assert row["newton_model_builder_instantiated_count"] == 0
    assert row["newton_engine_shape_object_count"] == 0
    assert row["newton_builder_shape_call_count"] == 0
    assert row["newton_model_finalized_count"] == 0
    assert row["newton_collision_pipeline_created_count"] == 0
    assert row["newton_collision_pipeline_collide_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    assert row["configured_runtime_lane_review_gate_required"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert row["source_package_copy_forbidden"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_REMAINING_GAPS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_execution_rejects_input_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
            ]
        )
    )
    configured_runtime_smoke["unexpected_configured_runtime_execution_input_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_execution_input_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload(
            configured_runtime_smoke
        )

    configured_runtime_smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
            ]
        )
    )
    configured_runtime_smoke.pop("coverage_summary")

    with pytest.raises(
        ValueError,
        match="configured_runtime_execution_input_missing_keys:coverage_summary",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload(
            configured_runtime_smoke
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        (
            "gate_id",
            "stale_gate",
            "configured_runtime_execution_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "configured_runtime_execution_input_next_gate_mismatch",
        ),
        (
            "remaining_gaps",
            ["stale_gate"],
            "configured_runtime_execution_input_remaining_gaps_mismatch",
        ),
        (
            "configured_runtime_smoke_status",
            "runtime_smoke_allowed",
            "configured_runtime_execution_input_metadata_mismatch:configured_runtime_smoke_status",
        ),
        (
            "configured_runtime_smoke_allowed_count",
            1,
            "configured_runtime_execution_input_metadata_mismatch:"
            "configured_runtime_smoke_allowed_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "configured_runtime_execution_input_count_mismatch:newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_execution_rejects_input_value_drift(
    field_name,
    bad_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
            ]
        )
    )
    configured_runtime_smoke[field_name] = bad_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload(
            configured_runtime_smoke
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        (
            "configured_runtime_smoke_allowed",
            True,
            "configured_runtime_execution_input_flag_true:configured_runtime_smoke_allowed",
        ),
        (
            "configured_runtime_smoke_ready",
            False,
            "configured_runtime_execution_input_flag_false:configured_runtime_smoke_ready",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_execution_rejects_input_flag_drift(
    field_name,
    bad_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
            ]
        )
    )
    configured_runtime_smoke[field_name] = bad_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload(
            configured_runtime_smoke
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_execution_rejects_source_row_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
            ]
        )
    )
    configured_runtime_smoke["newton_shape_runtime_engine_builder_configured_runtime_smoke_rows"][
        0
    ]["unexpected_configured_runtime_execution_source_row_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_execution_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload(
            configured_runtime_smoke
        )

    configured_runtime_smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
            ]
        )
    )
    configured_runtime_smoke["newton_shape_runtime_engine_builder_configured_runtime_smoke_rows"][
        0
    ].pop("configured_runtime_smoke_reason")

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_execution_source_row_missing_keys:configured_runtime_smoke_reason"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload(
            configured_runtime_smoke
        )


@pytest.mark.parametrize(
    ("rows_value", "message"),
    [
        ([], "configured_runtime_execution_row_count_mismatch"),
        ("not_rows", "configured_runtime_execution_row_count_mismatch"),
        ([None], "configured_runtime_execution_row_count_mismatch"),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_execution_rejects_row_count_drift(
    rows_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
            ]
        )
    )
    configured_runtime_smoke[
        "newton_shape_runtime_engine_builder_configured_runtime_smoke_rows"
    ] = rows_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload(
            configured_runtime_smoke
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_execution_rejects_duplicate_source_rows(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
            ]
        )
    )
    row = configured_runtime_smoke[
        "newton_shape_runtime_engine_builder_configured_runtime_smoke_rows"
    ][0]
    configured_runtime_smoke[
        "newton_shape_runtime_engine_builder_configured_runtime_smoke_rows"
    ] = [row, json.loads(json.dumps(row))]

    with pytest.raises(
        ValueError,
        match="configured_runtime_execution_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload(
            configured_runtime_smoke
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        (
            "source_package_id",
            "stale_package",
            "configured_runtime_execution_source_row_mismatch:source_package_id",
        ),
        (
            "configured_runtime_smoke_reason",
            "runtime_smoke_allowed",
            "configured_runtime_execution_source_row_mismatch:configured_runtime_smoke_reason",
        ),
        (
            "configured_runtime_smoke_allowed",
            True,
            "configured_runtime_execution_source_row_mismatch:configured_runtime_smoke_allowed",
        ),
        (
            "configured_runtime_source_resolution_passed",
            True,
            "configured_runtime_execution_source_row_mismatch:"
            "configured_runtime_source_resolution_passed",
        ),
        (
            "configured_runtime_device_resolution_passed",
            True,
            "configured_runtime_execution_source_row_mismatch:"
            "configured_runtime_device_resolution_passed",
        ),
        (
            "runtime_source_config_resolved",
            True,
            "configured_runtime_execution_source_row_mismatch:runtime_source_config_resolved",
        ),
        (
            "runtime_device_config_resolved",
            True,
            "configured_runtime_execution_source_row_mismatch:runtime_device_config_resolved",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "configured_runtime_execution_source_row_count_mismatch:newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_execution_rejects_source_row_value_drift(
    field_name,
    bad_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_smoke = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
            ]
        )
    )
    configured_runtime_smoke["newton_shape_runtime_engine_builder_configured_runtime_smoke_rows"][
        0
    ][field_name] = bad_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract_payload(
            configured_runtime_smoke
        )


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract"
    ]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_RUN_CONTRACT
    )
    assert report["failure_labels"] == [
        (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_RUN_CONTRACT
            + "_missing"
        )
    ]
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert (
        report[
            "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
        ]["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert (
        payload["gate_id"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT
    )
    assert (
        payload["input_gate_id"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_RUN_CONTRACT
    )
    assert payload["configured_runtime_lane_review_decision"] == (
        "keep_real_runtime_execution_blocked_after_configured_runtime_execution_review"
    )
    assert payload["configured_runtime_lane_review_recorded_count"] == 1
    assert payload["configured_runtime_lane_claim_boundary_preserved_count"] == 1
    assert payload["real_runtime_execution_evidence_count"] == 0
    assert payload["runtime_compatibility_validated_count"] == 0
    assert payload["configured_runtime_run_allowed_count"] == 0
    assert payload["configured_runtime_run_attempted_count"] == 0
    assert payload["configured_runtime_run_passed_count"] == 0
    assert payload["real_runtime_execution_evidence"] is False
    assert payload["runtime_compatibility_validated"] is False
    assert payload["configured_runtime_run_allowed"] is False
    assert payload["configured_runtime_run_attempted"] is False
    assert payload["configured_runtime_run_passed"] is False
    assert payload["configured_runtime_execution_allowed"] is False
    assert payload["configured_runtime_execution_attempted"] is False
    assert payload["configured_runtime_execution_passed"] is False
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract"
    ]
    configured_runtime_execution = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
    ]
    source_row = configured_runtime_execution[
        "newton_shape_runtime_engine_builder_configured_runtime_execution_rows"
    ][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_configured_"
        "runtime_lane_review_report_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_configured_runtime_lane_review_recorded_"
        "configured_runtime_run_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_configured_runtime_lane_review_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_configured_runtime_lane_review_contract_"
        "no_config_file_read_no_env_read_no_filesystem_probe_no_import_"
        "no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["configured_runtime_lane_review_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT
        ),
        "next_configured_runtime_run_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_RUN_CONTRACT
        ),
        "configured_runtime_execution_decision_required": (
            "skip_real_runtime_execution_configured_runtime_smoke_not_allowed"
        ),
        "configured_runtime_lane_review_decision": (
            "keep_real_runtime_execution_blocked_after_configured_runtime_execution_review"
        ),
        "configured_runtime_lane_claim_boundary_preserved": True,
        "real_runtime_execution_evidence": False,
        "runtime_compatibility_validated": False,
        "configured_runtime_run_allowed": False,
        "newton_runtime_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_configured_runtime_execution_row_id": source_row[
            "newton_shape_runtime_engine_builder_configured_runtime_execution_row_id"
        ],
        "source_newton_shape_runtime_engine_builder_configured_runtime_smoke_row_id": source_row[
            "source_newton_shape_runtime_engine_builder_configured_runtime_smoke_row_id"
        ],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_configured_runtime_execution_decision": (
            "skip_real_runtime_execution_configured_runtime_smoke_not_allowed"
        ),
        "source_configured_runtime_execution_status": (
            "runtime_execution_skipped_configured_runtime_smoke_not_allowed"
        ),
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_configured_runtime_lane_review_row_count": 1,
        "source_newton_shape_runtime_engine_builder_configured_runtime_execution_row_count": 1,
        "configured_runtime_source_resolution_recorded_count": 1,
        "configured_runtime_source_resolution_passed_count": 0,
        "configured_runtime_source_resolution_failed_count": 1,
        "configured_runtime_device_resolution_recorded_count": 1,
        "configured_runtime_device_resolution_passed_count": 0,
        "configured_runtime_device_resolution_failed_count": 1,
        "configured_runtime_entry_decision_recorded_count": 1,
        "configured_runtime_entry_decision_passed_count": 0,
        "configured_runtime_entry_decision_failed_count": 1,
        "configured_runtime_smoke_recorded_count": 1,
        "configured_runtime_smoke_passed_count": 0,
        "configured_runtime_smoke_failed_count": 1,
        "configured_runtime_execution_recorded_count": 1,
        "configured_runtime_execution_passed_count": 0,
        "configured_runtime_execution_failed_count": 1,
        "configured_runtime_lane_review_recorded_count": 1,
        "configured_runtime_lane_claim_boundary_preserved_count": 1,
        "real_runtime_execution_evidence_count": 0,
        "runtime_compatibility_validated_count": 0,
        "configured_runtime_run_allowed_count": 0,
        "configured_runtime_run_attempted_count": 0,
        "configured_runtime_run_passed_count": 0,
        "runtime_config_validated_count": 0,
        "runtime_source_config_resolved_count": 0,
        "runtime_device_config_resolved_count": 0,
        "runtime_entry_allowed_count": 0,
        "runtime_entry_attempted_count": 0,
        "runtime_entry_passed_count": 0,
        "configured_runtime_smoke_allowed_count": 0,
        "configured_runtime_smoke_attempted_count": 0,
        "configured_runtime_execution_allowed_count": 0,
        "configured_runtime_execution_attempted_count": 0,
        "newton_source_dir_resolution_attempted_count": 0,
        "newton_source_dir_configured_count": 0,
        "newton_source_dir_resolved_count": 0,
        "newton_diagnostic_device_resolution_attempted_count": 0,
        "newton_diagnostic_device_configured_count": 0,
        "newton_diagnostic_device_resolved_count": 0,
        "required_config_key_count": 2,
        "required_runtime_input_count": 6,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_model_finalized_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "newton_runtime_execution_count": 0,
        "configured_runtime_lane_review_decision_distribution": {
            "keep_real_runtime_execution_blocked_after_configured_runtime_execution_review": 1
        },
        "configured_runtime_lane_review_status_distribution": {"claim_boundary_preserved": 1},
    }
    row = payload["newton_shape_runtime_engine_builder_configured_runtime_lane_review_rows"][0]
    assert set(row) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_ROW_REQUIRED_KEYS
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_configured_runtime_execution_row_id"]
        == (source_row["newton_shape_runtime_engine_builder_configured_runtime_execution_row_id"])
    )
    assert row["configured_runtime_lane_review_decision"] == (
        "keep_real_runtime_execution_blocked_after_configured_runtime_execution_review"
    )
    assert row["configured_runtime_lane_review_reason"] == (
        "configured_runtime_execution_skipped_no_runtime_evidence"
    )
    assert row["configured_runtime_lane_review_status"] == ("claim_boundary_preserved")
    assert row["configured_runtime_lane_review_recorded"] is True
    assert row["configured_runtime_lane_claim_boundary_preserved"] is True
    assert row["configured_runtime_run_gate_required"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_RUN_CONTRACT
    )
    assert row["real_runtime_execution_evidence"] is False
    assert row["runtime_compatibility_validated"] is False
    assert row["configured_runtime_run_allowed"] is False
    assert row["configured_runtime_run_attempted"] is False
    assert row["configured_runtime_run_passed"] is False
    assert row["source_package_copy_forbidden"] is True
    assert payload["remaining_gaps"] == (
        EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_REMAINING_GAPS
    )
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_FALSE_FLAGS:
        assert payload[flag] is False
    for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_TRUE_FLAGS:
        assert payload[flag] is True


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_rejects_input_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
            ]
        )
    )
    configured_runtime_execution["unexpected_configured_runtime_lane_review_input_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_lane_review_input_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload(
            configured_runtime_execution
        )

    configured_runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
            ]
        )
    )
    configured_runtime_execution.pop("coverage_summary")

    with pytest.raises(
        ValueError,
        match=("configured_runtime_lane_review_input_missing_keys:coverage_summary"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload(
            configured_runtime_execution
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        (
            "gate_id",
            "stale_gate",
            "configured_runtime_lane_review_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "configured_runtime_lane_review_input_next_gate_mismatch",
        ),
        (
            "remaining_gaps",
            ["stale_gate"],
            "configured_runtime_lane_review_input_remaining_gaps_mismatch",
        ),
        (
            "configured_runtime_execution_decision",
            "run_real_runtime_execution",
            "configured_runtime_lane_review_input_metadata_mismatch:"
            "configured_runtime_execution_decision",
        ),
        (
            "configured_runtime_execution_allowed_count",
            1,
            "configured_runtime_lane_review_input_metadata_mismatch:"
            "configured_runtime_execution_allowed_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "configured_runtime_lane_review_input_count_mismatch:newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_rejects_input_value_drift(
    field_name,
    bad_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
            ]
        )
    )
    configured_runtime_execution[field_name] = bad_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload(
            configured_runtime_execution
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        (
            "configured_runtime_execution_allowed",
            True,
            "configured_runtime_lane_review_input_flag_true:configured_runtime_execution_allowed",
        ),
        (
            "configured_runtime_execution_ready",
            False,
            "configured_runtime_lane_review_input_flag_false:configured_runtime_execution_ready",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_rejects_input_flag_drift(
    field_name,
    bad_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
            ]
        )
    )
    configured_runtime_execution[field_name] = bad_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload(
            configured_runtime_execution
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_rejects_source_row_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
            ]
        )
    )
    configured_runtime_execution[
        "newton_shape_runtime_engine_builder_configured_runtime_execution_rows"
    ][0]["unexpected_configured_runtime_lane_review_source_row_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_lane_review_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload(
            configured_runtime_execution
        )

    configured_runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
            ]
        )
    )
    configured_runtime_execution[
        "newton_shape_runtime_engine_builder_configured_runtime_execution_rows"
    ][0].pop("configured_runtime_execution_reason")

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_lane_review_source_row_missing_keys:"
            "configured_runtime_execution_reason"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload(
            configured_runtime_execution
        )


@pytest.mark.parametrize(
    ("rows_value", "message"),
    [
        ([], "configured_runtime_lane_review_row_count_mismatch"),
        ("not_rows", "configured_runtime_lane_review_row_count_mismatch"),
        ([None], "configured_runtime_lane_review_row_count_mismatch"),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_rejects_row_count_drift(
    rows_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
            ]
        )
    )
    configured_runtime_execution[
        "newton_shape_runtime_engine_builder_configured_runtime_execution_rows"
    ] = rows_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload(
            configured_runtime_execution
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_rejects_duplicate_source_rows(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
            ]
        )
    )
    row = configured_runtime_execution[
        "newton_shape_runtime_engine_builder_configured_runtime_execution_rows"
    ][0]
    configured_runtime_execution[
        "newton_shape_runtime_engine_builder_configured_runtime_execution_rows"
    ] = [row, json.loads(json.dumps(row))]

    with pytest.raises(
        ValueError,
        match="configured_runtime_lane_review_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload(
            configured_runtime_execution
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "message"),
    [
        (
            "source_package_id",
            "stale_package",
            "configured_runtime_lane_review_source_row_mismatch:source_package_id",
        ),
        (
            "configured_runtime_execution_decision",
            "run_real_runtime_execution",
            "configured_runtime_lane_review_source_row_mismatch:"
            "configured_runtime_execution_decision",
        ),
        (
            "configured_runtime_execution_allowed",
            True,
            "configured_runtime_lane_review_source_row_mismatch:"
            "configured_runtime_execution_allowed",
        ),
        (
            "configured_runtime_execution_failed",
            False,
            "configured_runtime_lane_review_source_row_mismatch:"
            "configured_runtime_execution_failed",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "configured_runtime_lane_review_source_row_count_mismatch:"
            "newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_lane_review_rejects_source_row_value_drift(
    field_name,
    bad_value,
    message,
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_execution = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
            ]
        )
    )
    configured_runtime_execution[
        "newton_shape_runtime_engine_builder_configured_runtime_execution_rows"
    ][0][field_name] = bad_value

    with pytest.raises(ValueError, match=message):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract_payload(
            configured_runtime_execution
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_validation_rejects_input_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_preflight = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
            ]
        )
    )
    configured_runtime_preflight["unexpected_configured_runtime_validation_input_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_validation_input_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract_payload(
            configured_runtime_preflight
        )

    configured_runtime_preflight = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
            ]
        )
    )
    configured_runtime_preflight.pop("coverage_summary")

    with pytest.raises(
        ValueError,
        match="configured_runtime_validation_input_missing_keys:coverage_summary",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract_payload(
            configured_runtime_preflight
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_configured_runtime_validation_rejects_source_row_schema_drift(
    cpd_paper_report,
):
    report = cpd_paper_report
    configured_runtime_preflight = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
            ]
        )
    )
    configured_runtime_preflight[
        "newton_shape_runtime_engine_builder_configured_runtime_preflight_rows"
    ][0]["unexpected_configured_runtime_validation_source_row_key"] = True

    with pytest.raises(
        ValueError,
        match="configured_runtime_validation_source_row_unexpected_keys",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract_payload(
            configured_runtime_preflight
        )

    configured_runtime_preflight = json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
            ]
        )
    )
    configured_runtime_preflight[
        "newton_shape_runtime_engine_builder_configured_runtime_preflight_rows"
    ][0].pop("configured_runtime_preflight_reason")

    with pytest.raises(
        ValueError,
        match=(
            "configured_runtime_validation_source_row_missing_keys:"
            "configured_runtime_preflight_reason"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract_payload(
            configured_runtime_preflight
        )
