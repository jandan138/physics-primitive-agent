import pytest

from tests.cpd_paper_offline_shared import *

pytestmark = pytest.mark.paper_offline


def test_cpd_paper_records_mapped_subset_primitivespec_generation_preflight_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_generation_preflight_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert (
        report["paper_mapped_subset_primitivespec_validation_contract"]["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_generation_preflight_contract_only_partial"
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    assert payload["next_required_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_generation_preflight_contract_complete_"
        "primitivespec_generation_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_primitivespec_generation_preflight_contract_not_primitivespec_"
        "not_collision_package"
    )
    assert payload["generation_preflight_candidate_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_GENERATION_PREFLIGHT_REMAINING_GAPS


def test_cpd_paper_primitivespec_generation_preflight_records_family_requirements(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_generation_preflight_contract"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["primitive_spec_generation_preflight_requirement_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    for primitive_name, kind in (
        ("oriented_bounding_box", "box"),
        ("sphere", "sphere"),
        ("capsule", "capsule"),
    ):
        row = rows[primitive_name]
        assert row["primitive_spec_generation_preflight_decision"] == (
            "future_native_family_generation_requirement_preflighted"
        )
        assert row["candidate_mapping_label"] == kind
        assert row["validated_future_primitive_spec_kind"] == kind
        assert row["generation_preflight_candidate"] is False
        assert (
            row["required_later_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        )
    assert (
        rows["capped_cylinder"]["primitive_spec_generation_preflight_decision"]
        == "blocked_approximation_policy_generation_preflight_recorded"
    )
    assert (
        rows["frustum"]["primitive_spec_generation_preflight_decision"]
        == "blocked_approximation_policy_generation_preflight_recorded"
    )
    assert (
        rows["trapezoidal_prism"]["primitive_spec_generation_preflight_decision"]
        == "noop_unmapped_family_generation_preflight_recorded"
    )


def test_cpd_paper_primitivespec_generation_preflight_noops_current_unmapped_rows(cpd_paper_report):
    report = cpd_paper_report
    validation = report["paper_mapped_subset_primitivespec_validation_contract"]
    payload = report["paper_mapped_subset_primitivespec_generation_preflight_contract"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_primitivespec_generation_preflight_rows"]

    assert summary["primitive_spec_generation_preflight_requirement_row_count"] == 6
    assert summary["future_native_primitivespec_generation_preflight_count"] == 3
    assert summary["blocked_primitivespec_generation_preflight_requirement_count"] == 2
    assert summary["noop_primitivespec_generation_preflight_requirement_count"] == 1
    assert summary["current_row_primitivespec_generation_preflight_row_count"] == 16
    assert summary["current_primitivespec_generation_preflight_pass_record_count"] == 0
    assert summary["current_primitivespec_generation_preflight_noop_record_count"] == 16
    assert summary["generation_preflight_candidate_record_count"] == 0
    assert summary["generated_primitive_spec_record_count"] == 0

    validation_rows = validation["current_row_primitivespec_validation_rows"]
    assert len(rows) == len(validation_rows) == 16
    for row, upstream_row in zip(rows, validation_rows):
        assert (
            row["source_primitivespec_validation_row_id"]
            == (upstream_row["primitive_spec_validation_row_id"])
        )
        assert (
            row["source_primitivespec_dry_run_row_id"]
            == (upstream_row["source_primitivespec_dry_run_row_id"])
        )
        assert (
            row["source_adapter_preflight_row_id"]
            == (upstream_row["source_adapter_preflight_row_id"])
        )
        assert (
            row["source_candidate_matrix_row_id"]
            == (upstream_row["source_candidate_matrix_row_id"])
        )
        assert (
            row["source_conversion_plan_row_id"] == (upstream_row["source_conversion_plan_row_id"])
        )
        assert row["source_policy_decision_id"] == (upstream_row["source_policy_decision_id"])
        assert row["source_adapter_decision_id"] == (upstream_row["source_adapter_decision_id"])
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["evidence_case_id"] == upstream_row["evidence_case_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["primitive_spec_generation_preflight_decision"] == (
            "skip_unmapped_current_row_preflighted"
        )
        assert row["primitive_spec_generation_preflight_action"] == "keep_offline"
        assert row["primitive_spec_generation_preflight_passed"] is False
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["silent_drop_detected"] is False
        assert (
            row["required_later_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        )


def test_cpd_paper_primitivespec_generation_preflight_stays_report_only(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_generation_preflight_contract"]

    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    for flag in GENERATION_PREFLIGHT_ROW_FALSE_FLAGS:
        assert payload[flag] is False
    for row in (
        payload["primitive_spec_generation_preflight_requirement_rows"]
        + payload["current_row_primitivespec_generation_preflight_rows"]
    ):
        assert forbidden_keys.isdisjoint(row)
        for flag in GENERATION_PREFLIGHT_ROW_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_primitivespec_generation_preflight_rejects_wrong_input_gate():
    validation = _generation_preflight_validation_input()
    validation["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_preflight_input_gate_id_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_true_input_trigger_flags():
    validation = _generation_preflight_validation_input()
    validation["real_usd_loaded"] = True

    with pytest.raises(
        ValueError,
        match="generation_preflight_input_trigger_flag_true:real_usd_loaded",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


@pytest.mark.parametrize(
    ("field_name", "error_label"),
    [
        (
            "validated_primitive_spec_candidate_count",
            "generation_preflight_input_candidate_count_nonzero",
        ),
        (
            "generated_primitive_spec_count",
            "generation_preflight_input_generated_spec_nonzero",
        ),
        (
            "generated_collision_package_count",
            "generation_preflight_input_generated_collision_package_nonzero",
        ),
        (
            "runtime_admissibility_check_count",
            "generation_preflight_input_trigger_flag_true:runtime_admissibility_check_count",
        ),
    ],
)
def test_cpd_paper_primitivespec_generation_preflight_rejects_nonzero_counts(
    field_name,
    error_label,
):
    validation = _generation_preflight_validation_input()
    validation[field_name] = 1

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_coverage_mismatch():
    validation = _generation_preflight_validation_input()
    coverage = dict(validation["coverage_summary"])
    coverage["current_row_primitivespec_validation_row_count"] = 15
    validation["coverage_summary"] = coverage

    with pytest.raises(
        ValueError,
        match=(
            "generation_preflight_coverage_count_mismatch:"
            "current_row_primitivespec_validation_row_count"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_family_order_mismatch():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["primitive_spec_validation_requirement_rows"]]
    rows[1]["paper_primitive"] = "oriented_bounding_box"
    validation["primitive_spec_validation_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="generation_preflight_family_primitive_sequence_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_future_label_mismatch():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["primitive_spec_validation_requirement_rows"]]
    rows[0]["candidate_mapping_label"] = "offline_only_unmapped"
    validation["primitive_spec_validation_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=("generation_preflight_future_mapping_label_mismatch:oriented_bounding_box"),
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_mutated_family_semantics():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["primitive_spec_validation_requirement_rows"]]
    capped_cylinder = next(row for row in rows if row["paper_primitive"] == "capped_cylinder")
    capped_cylinder["primitive_spec_validation_decision"] = (
        "future_native_family_primitivespec_shape_requirement_validated"
    )
    capped_cylinder["candidate_mapping_label"] = "box"
    capped_cylinder["validated_future_primitive_spec_kind"] = "box"
    validation["primitive_spec_validation_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="generation_preflight_family_contract_mismatch:capped_cylinder",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_unknown_family_decision():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["primitive_spec_validation_requirement_rows"]]
    rows[0]["primitive_spec_validation_decision"] = "misspelled_decision"
    validation["primitive_spec_validation_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="unknown_primitivespec_validation_family_decision:misspelled_decision",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_blank_validation_row_id():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["primitive_spec_validation_requirement_rows"]]
    rows[0]["primitive_spec_validation_row_id"] = " "
    validation["primitive_spec_validation_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=("generation_preflight_missing_validation_row_id:primitive_spec_validation_row_id"),
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_duplicate_validation_row_id():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["current_row_primitivespec_validation_rows"]]
    rows[1]["primitive_spec_validation_row_id"] = rows[0]["primitive_spec_validation_row_id"]
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_validation_row_id",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_current_source_id_gap():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["current_row_primitivespec_validation_rows"]]
    rows[0]["source_output_id"] = ""
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="generation_preflight_missing_current_row_source_id:source_output_id",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_unknown_current_decision():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["current_row_primitivespec_validation_rows"]]
    rows[0]["primitive_spec_validation_decision"] = "misspelled_current_decision"
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match=("unknown_primitivespec_validation_current_decision:misspelled_current_decision"),
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_row_level_flag():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["current_row_primitivespec_validation_rows"]]
    rows[0]["benchmark_run"] = True
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="generation_preflight_input_trigger_flag_true:benchmark_run",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


@pytest.mark.parametrize(
    ("field_name", "field_value", "error_label"),
    [
        (
            "primitive_spec_validation_passed",
            True,
            "generation_preflight_input_candidate_count_nonzero",
        ),
        (
            "primitive_spec_candidate",
            True,
            "generation_preflight_input_candidate_count_nonzero",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "generation_preflight_input_generated_spec_nonzero",
        ),
    ],
)
def test_cpd_paper_primitivespec_generation_preflight_rejects_current_row_generation_leaks(
    field_name,
    field_value,
    error_label,
):
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["current_row_primitivespec_validation_rows"]]
    rows[0][field_name] = field_value
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_current_row_gate_mismatch():
    validation = _generation_preflight_validation_input()
    rows = [dict(row) for row in validation["current_row_primitivespec_validation_rows"]]
    rows[0]["required_later_gate"] = "stale_gate"
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="generation_preflight_current_row_required_later_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(validation)


def test_cpd_paper_primitivespec_generation_preflight_rejects_duplicate_emitted_row_ids():
    rows = [
        {"primitive_spec_generation_preflight_row_id": "duplicate"},
        {"primitive_spec_generation_preflight_row_id": "duplicate"},
    ]

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_generation_preflight_row_id",
    ):
        _paper_require_unique_generation_preflight_row_ids(rows)


def test_cpd_paper_records_mapped_subset_primitivespec_generation_contract_gate(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_generation_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["status"] == "partial"
    assert report["paper_faithful_offline_supported"] is False
    assert report["package_generation_triggered"] is False
    assert report["newton_runtime_triggered"] is False
    assert report["real_usd_triggered"] is False
    assert report["benchmark_triggered"] is False
    assert report["collision_quality_measured"] is False
    assert report["deployment_or_certification_claimed"] is False

    preflight = report["paper_mapped_subset_primitivespec_generation_preflight_contract"]
    assert (
        preflight["next_required_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_generation_contract_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    assert (
        payload["input_gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_generation_contract_complete_"
        "mapped_current_candidate_source_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_primitivespec_generation_contract_template_rows_"
        "not_runtime_primitivespec_not_collision_package"
    )
    assert payload["primitive_spec_generation_action"] == (
        "emit_offline_templates_and_keep_current_rows_offline"
    )
    assert payload["primitive_spec_generation_candidate_count"] == 0
    assert payload["offline_primitivespec_template_count"] == 3
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS


def test_cpd_paper_primitivespec_generation_payload_schema_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_generation_contract"]

    assert set(payload) == PRIMITIVESPEC_GENERATION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_primitivespec_generation_templates_only_no_runtime_"
        "primitivespec_no_collision_package_no_newton"
    )
    assert payload["input_contract_summary"] == {
        "input_gate_id": (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT),
        "input_artifact_kind": (
            "offline_primitivespec_generation_preflight_contract_not_"
            "primitivespec_not_collision_package"
        ),
        "primitive_spec_generation_preflight_requirement_row_count": 6,
        "current_row_primitivespec_generation_preflight_row_count": 16,
        "generation_preflight_candidate_record_count": 0,
        "generated_primitive_spec_record_count": 0,
    }
    assert payload["primitive_spec_generation_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT),
        "current_candidate_source_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
        "template_only_native_families": ["box", "sphere", "capsule"],
        "zero_runtime_primitivespecs_required": True,
        "zero_collision_packages_required": True,
        "zero_runtime_admissibility_checks_required": True,
        "runtime_primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "approximation_policy_enabled": False,
        "silent_drop_allowed": False,
    }


def test_cpd_paper_primitivespec_generation_emits_native_family_templates_only(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_generation_contract"]
    rows = {
        row["paper_primitive"]: row for row in payload["native_family_primitivespec_template_rows"]
    }

    assert list(rows) == ["oriented_bounding_box", "sphere", "capsule"]
    for primitive_name, kind in (
        ("oriented_bounding_box", "box"),
        ("sphere", "sphere"),
        ("capsule", "capsule"),
    ):
        row = rows[primitive_name]
        assert set(row) == PRIMITIVESPEC_GENERATION_NATIVE_TEMPLATE_ROW_REQUIRED_KEYS
        assert row["primitive_spec_kind"] == kind
        assert row["candidate_mapping_label"] == kind
        assert row["input_primitivespec_generation_preflight_decision"] == (
            "future_native_family_generation_requirement_preflighted"
        )
        assert row["required_primitive_spec_fields"] == [
            "primitive_id",
            "kind",
            "center",
            "axes",
            "dimensions",
            "frame",
            "source_faces",
            "contains_assigned_points",
            "volume",
            "weighted_volume",
            "conversion_status",
        ]
        assert row["template_only"] is True
        assert row["runtime_instance_generated"] is False
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["silent_drop_detected"] is False
        assert row["primitive_spec_generation_decision"] == (
            "native_family_primitivespec_template_generated_offline_only"
        )
        assert (
            row["required_current_candidate_source_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        )
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_primitivespec_generation_records_blocked_and_noop_family_rows(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_generation_contract"]
    blocked = {
        row["paper_primitive"]: row
        for row in payload["blocked_primitivespec_generation_requirement_rows"]
    }
    noop = {
        row["paper_primitive"]: row
        for row in payload["noop_primitivespec_generation_requirement_rows"]
    }

    assert list(blocked) == ["capped_cylinder", "frustum"]
    for row in blocked.values():
        assert set(row) == PRIMITIVESPEC_GENERATION_REQUIREMENT_ROW_REQUIRED_KEYS
        assert row["candidate_mapping_label"] == "offline_only_unmapped"
        assert row["input_primitivespec_generation_preflight_decision"] == (
            "blocked_approximation_policy_generation_preflight_recorded"
        )
        assert row["primitive_spec_generation_decision"] == (
            "blocked_approximation_policy_before_primitivespec_generation"
        )
        assert row["primitive_spec_generation_action"] == ("require_explicit_approximation_policy")
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert (
            row["required_later_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        )
        assert row["required_future_policy"] == "approximation_policy"
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False

    assert list(noop) == ["trapezoidal_prism"]
    row = noop["trapezoidal_prism"]
    assert set(row) == PRIMITIVESPEC_GENERATION_REQUIREMENT_ROW_REQUIRED_KEYS
    assert row["candidate_mapping_label"] == "offline_only_unmapped"
    assert row["input_primitivespec_generation_preflight_decision"] == (
        "noop_unmapped_family_generation_preflight_recorded"
    )
    assert row["primitive_spec_generation_decision"] == (
        "noop_unmapped_family_before_primitivespec_generation"
    )
    assert row["primitive_spec_generation_action"] == "keep_unmapped_family_offline"
    assert row["primitive_spec_generation_candidate"] is False
    assert row["generated_primitive_spec"] is None
    assert (
        row["required_later_gate"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert row["required_future_policy"] == "mapped_current_candidate_source"


def test_cpd_paper_primitivespec_generation_keeps_current_rows_no_generation(cpd_paper_report):
    report = cpd_paper_report
    preflight = report["paper_mapped_subset_primitivespec_generation_preflight_contract"]
    payload = report["paper_mapped_subset_primitivespec_generation_contract"]
    rows = payload["current_row_primitivespec_generation_rows"]
    upstream_rows = preflight["current_row_primitivespec_generation_preflight_rows"]

    assert len(rows) == len(upstream_rows) == 16
    for row, upstream_row in zip(rows, upstream_rows):
        assert set(row) == PRIMITIVESPEC_GENERATION_CURRENT_ROW_REQUIRED_KEYS
        assert (
            row["source_primitivespec_generation_preflight_row_id"]
            == (upstream_row["primitive_spec_generation_preflight_row_id"])
        )
        assert (
            row["source_primitivespec_validation_row_id"]
            == (upstream_row["source_primitivespec_validation_row_id"])
        )
        assert (
            row["source_primitivespec_dry_run_row_id"]
            == (upstream_row["source_primitivespec_dry_run_row_id"])
        )
        assert (
            row["source_adapter_preflight_row_id"]
            == (upstream_row["source_adapter_preflight_row_id"])
        )
        assert (
            row["source_candidate_matrix_row_id"]
            == (upstream_row["source_candidate_matrix_row_id"])
        )
        assert (
            row["source_conversion_plan_row_id"] == (upstream_row["source_conversion_plan_row_id"])
        )
        assert row["source_policy_decision_id"] == (upstream_row["source_policy_decision_id"])
        assert row["source_adapter_decision_id"] == (upstream_row["source_adapter_decision_id"])
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["evidence_case_id"] == upstream_row["evidence_case_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_mapping_label"] == "offline_only_unmapped"
        assert row["primitive_spec_generation_decision"] == (
            "skip_unmapped_current_row_no_primitivespec_generated"
        )
        assert row["primitive_spec_generation_action"] == (
            "keep_offline_until_mapped_current_candidate_exists"
        )
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["silent_drop_detected"] is False
        assert (
            row["required_later_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        )
        assert row["required_future_policy"] == "mapped_current_candidate_source"
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_primitivespec_generation_coverage_summary_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_generation_contract"]
    assert payload["coverage_summary"] == {
        "primitive_spec_generation_requirement_row_count": 6,
        "native_family_primitivespec_template_row_count": 3,
        "blocked_primitivespec_generation_requirement_row_count": 2,
        "noop_primitivespec_generation_requirement_row_count": 1,
        "current_row_primitivespec_generation_row_count": 16,
        "current_primitivespec_generation_pass_record_count": 0,
        "primitive_spec_generation_candidate_record_count": 0,
        "offline_primitivespec_template_record_count": 3,
        "generated_primitive_spec_record_count": 0,
        "generated_collision_package_record_count": 0,
        "runtime_admissibility_check_record_count": 0,
        "current_primitivespec_generation_noop_record_count": 16,
        "current_paper_primitive_distribution": {"trapezoidal_prism": 16},
        "current_mapping_label_distribution": {"offline_only_unmapped": 16},
    }


def test_cpd_paper_primitivespec_generation_stays_report_only(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_generation_contract"]

    forbidden_keys = {
        "CollisionPackage",
        "PrimitiveSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False
    rows = (
        payload["native_family_primitivespec_template_rows"]
        + payload["blocked_primitivespec_generation_requirement_rows"]
        + payload["noop_primitivespec_generation_requirement_rows"]
        + payload["current_row_primitivespec_generation_rows"]
    )
    for row in rows:
        assert forbidden_keys.isdisjoint(row)
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_primitivespec_generation_rejects_wrong_input_gate():
    preflight = _generation_contract_preflight_input()
    preflight["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_input_gate_id_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_stale_input_next_gate():
    preflight = _generation_contract_preflight_input()
    preflight["next_required_gate"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_input_next_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_true_input_trigger_flags():
    preflight = _generation_contract_preflight_input()
    preflight["real_usd_loaded"] = True

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_input_trigger_flag_true:real_usd_loaded",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


@pytest.mark.parametrize(
    ("row_collection_name", "flag_name"),
    [
        ("primitive_spec_generation_preflight_requirement_rows", "benchmark_run"),
        ("current_row_primitivespec_generation_preflight_rows", "real_usd_loaded"),
    ],
)
def test_cpd_paper_primitivespec_generation_rejects_row_level_true_trigger_flags(
    row_collection_name,
    flag_name,
):
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight[row_collection_name]]
    rows[0][flag_name] = True
    preflight[row_collection_name] = rows

    with pytest.raises(
        ValueError,
        match=f"primitivespec_generation_input_trigger_flag_true:{flag_name}",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


@pytest.mark.parametrize(
    ("field_name", "error_label"),
    [
        (
            "generation_preflight_candidate_count",
            "primitivespec_generation_input_candidate_count_nonzero",
        ),
        (
            "generated_primitive_spec_count",
            "primitivespec_generation_input_generated_spec_nonzero",
        ),
        (
            "generated_collision_package_count",
            "primitivespec_generation_input_generated_collision_package_nonzero",
        ),
        (
            "runtime_admissibility_check_count",
            "primitivespec_generation_input_runtime_admissibility_nonzero",
        ),
    ],
)
def test_cpd_paper_primitivespec_generation_rejects_nonzero_counts(
    field_name,
    error_label,
):
    preflight = _generation_contract_preflight_input()
    preflight[field_name] = 1

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_input_contract_drift():
    preflight = _generation_contract_preflight_input()
    contract = dict(preflight["primitive_spec_generation_preflight_contract"])
    contract["expected_current_row_count"] = 15
    preflight["primitive_spec_generation_preflight_contract"] = contract

    with pytest.raises(
        ValueError,
        match=("primitivespec_generation_input_contract_mismatch:expected_current_row_count"),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_coverage_mismatch():
    preflight = _generation_contract_preflight_input()
    coverage = dict(preflight["coverage_summary"])
    coverage["current_row_primitivespec_generation_preflight_row_count"] = 15
    preflight["coverage_summary"] = coverage

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_generation_coverage_count_mismatch:"
            "current_row_primitivespec_generation_preflight_row_count"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_family_order_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["primitive_spec_generation_preflight_requirement_rows"]]
    rows[0]["paper_primitive"] = "sphere"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_family_primitive_sequence_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_future_family_contract_drift():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["primitive_spec_generation_preflight_requirement_rows"]]
    rows[0]["candidate_mapping_label"] = "sphere"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=("primitivespec_generation_future_family_contract_mismatch:oriented_bounding_box"),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_blocked_family_contract_drift():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["primitive_spec_generation_preflight_requirement_rows"]]
    capped_cylinder = next(row for row in rows if row["paper_primitive"] == "capped_cylinder")
    capped_cylinder["primitive_spec_generation_preflight_decision"] = (
        "future_native_family_generation_requirement_preflighted"
    )
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_family_contract_mismatch:capped_cylinder",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_missing_family_source_id():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["primitive_spec_generation_preflight_requirement_rows"]]
    rows[0]["source_conversion_plan_row_id"] = ""
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=("primitivespec_generation_missing_preflight_row_id:source_conversion_plan_row_id"),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_unknown_family_decision():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["primitive_spec_generation_preflight_requirement_rows"]]
    rows[0]["primitive_spec_generation_preflight_decision"] = "misspelled"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="unknown_primitivespec_generation_preflight_family_decision:misspelled",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_unknown_current_decision():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["current_row_primitivespec_generation_preflight_rows"]]
    rows[0]["primitive_spec_generation_preflight_decision"] = "misspelled"
    preflight["current_row_primitivespec_generation_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match="unknown_primitivespec_generation_preflight_current_decision:misspelled",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


@pytest.mark.parametrize(
    ("field_name", "field_value", "error_label"),
    [
        (
            "generation_preflight_candidate",
            True,
            "primitivespec_generation_template_runtime_leak:generation_preflight_candidate",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "primitivespec_generation_template_runtime_leak:generated_primitive_spec",
        ),
    ],
)
def test_cpd_paper_primitivespec_generation_rejects_native_template_runtime_leaks(
    field_name,
    field_value,
    error_label,
):
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["primitive_spec_generation_preflight_requirement_rows"]]
    rows[0][field_name] = field_value
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_template_candidate_source_gate_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["primitive_spec_generation_preflight_requirement_rows"]]
    rows[0]["required_later_gate"] = "stale_gate"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=("primitivespec_generation_template_required_current_candidate_source_gate_mismatch"),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_requirement_required_later_gate_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["primitive_spec_generation_preflight_requirement_rows"]]
    capped_cylinder = next(row for row in rows if row["paper_primitive"] == "capped_cylinder")
    capped_cylinder["required_later_gate"] = "stale_gate"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_requirement_required_later_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_current_source_id_gap():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["current_row_primitivespec_generation_preflight_rows"]]
    rows[0]["source_output_id"] = ""
    preflight["current_row_primitivespec_generation_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_missing_current_row_source_id:source_output_id",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


@pytest.mark.parametrize(
    ("field_name", "field_value", "error_label"),
    [
        (
            "primitive_spec_generation_candidate",
            True,
            "primitivespec_generation_current_row_candidate_nonzero",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "primitivespec_generation_current_row_generated_spec_nonzero",
        ),
        (
            "silent_drop_detected",
            True,
            "primitivespec_generation_current_row_silent_drop_detected",
        ),
    ],
)
def test_cpd_paper_primitivespec_generation_rejects_current_row_generation_leaks(
    field_name,
    field_value,
    error_label,
):
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["current_row_primitivespec_generation_preflight_rows"]]
    rows[0][field_name] = field_value
    preflight["current_row_primitivespec_generation_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_current_row_gate_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [dict(row) for row in preflight["current_row_primitivespec_generation_preflight_rows"]]
    rows[0]["required_later_gate"] = "stale_gate"
    preflight["current_row_primitivespec_generation_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_current_row_required_later_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_duplicate_emitted_row_ids():
    rows = [
        {"primitive_spec_generation_row_id": "duplicate"},
        {"primitive_spec_generation_row_id": "duplicate"},
    ]

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_generation_row_id",
    ):
        _paper_require_unique_generation_row_ids(rows)


def test_cpd_paper_primitivespec_generation_rejects_duplicate_input_preflight_row_ids():
    preflight = _generation_contract_preflight_input()
    requirement_rows = [
        dict(row) for row in preflight["primitive_spec_generation_preflight_requirement_rows"]
    ]
    current_rows = [
        dict(row) for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
    current_rows[0]["primitive_spec_generation_preflight_row_id"] = requirement_rows[0][
        "primitive_spec_generation_preflight_row_id"
    ]
    preflight["primitive_spec_generation_preflight_requirement_rows"] = requirement_rows
    preflight["current_row_primitivespec_generation_preflight_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_generation_preflight_row_id",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_records_mapped_subset_primitivespec_candidate_source_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_candidate_source_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert (
        report["paper_mapped_subset_primitivespec_generation_contract"]["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert report["status"] == "partial"
    assert report["package_generation_triggered"] is False
    assert report["newton_runtime_triggered"] is False
    assert report["real_usd_triggered"] is False
    assert report["benchmark_triggered"] is False
    assert report["collision_quality_measured"] is False
    assert report["deployment_or_certification_claimed"] is False

    assert payload["gate_id"] == (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT)
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_candidate_source_contract_only_partial"
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert payload["input_gate_id"] == (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT)
    assert payload["next_required_gate"] == EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_candidate_source_contract_complete_native_current_fixture_contract_missing"
    )
    assert payload["primitive_spec_generation_candidate_count"] == 0
    assert payload["eligible_current_candidate_source_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_CANDIDATE_SOURCE_REMAINING_GAPS
