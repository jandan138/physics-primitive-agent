import pytest

from tests.cpd_paper_offline_shared import *

pytestmark = pytest.mark.paper_offline


def test_cpd_paper_primitivespec_candidate_source_payload_schema_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_candidate_source_contract"]

    assert set(payload) == PRIMITIVESPEC_CANDIDATE_SOURCE_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_primitivespec_candidate_source_audit_not_primitivespec_not_collision_package"
    )
    assert payload["implementation_boundary"] == (
        "offline_primitivespec_candidate_source_audit_only_no_runtime_"
        "primitivespec_no_collision_package_no_newton"
    )
    assert payload["candidate_source_action"] == (
        "audit_sources_and_keep_current_candidate_count_zero"
    )
    assert payload["input_contract_summary"] == {
        "input_gate_id": EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
        "input_artifact_kind": (
            "offline_primitivespec_generation_contract_template_rows_"
            "not_runtime_primitivespec_not_collision_package"
        ),
        "native_family_primitivespec_template_row_count": 3,
        "blocked_primitivespec_generation_requirement_row_count": 2,
        "noop_primitivespec_generation_requirement_row_count": 1,
        "current_row_primitivespec_generation_row_count": 16,
        "primitive_spec_generation_candidate_record_count": 0,
        "generated_primitive_spec_record_count": 0,
    }
    assert payload["candidate_source_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT),
        "current_candidate_source_gate_closed": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
        ),
        "next_current_candidate_gate_required": (
            EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
        ),
        "native_template_rows_are_future_only": True,
        "current_rows_must_be_mapped_native_family": True,
        "eligible_current_candidate_source_required_before_runtime_generation": True,
        "zero_runtime_primitivespecs_required": True,
        "zero_collision_packages_required": True,
        "zero_runtime_admissibility_checks_required": True,
        "runtime_primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "approximation_policy_enabled": False,
        "silent_drop_allowed": False,
    }
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False


def test_cpd_paper_primitivespec_candidate_source_classifies_sources(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_candidate_source_contract"]
    native = payload["native_template_candidate_source_audit_rows"]
    blocked = payload["blocked_family_candidate_source_audit_rows"]
    noop = payload["noop_family_candidate_source_audit_rows"]
    current = payload["current_row_candidate_source_audit_rows"]

    assert [row["paper_primitive"] for row in native] == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
    ]
    assert [row["primitive_spec_kind"] for row in native] == [
        "box",
        "sphere",
        "capsule",
    ]
    for row in native:
        assert set(row) == PRIMITIVESPEC_CANDIDATE_SOURCE_AUDIT_ROW_REQUIRED_KEYS
        assert row["source_role"] == "future_native_template"
        assert row["candidate_source_decision"] == ("template_only_not_current_candidate_source")
        assert row["candidate_source_reason"] == (
            "native_family_template_has_no_current_decomposition_row"
        )
        assert row["required_future_policy"] == "native_current_fixture"

    assert [row["paper_primitive"] for row in blocked] == [
        "capped_cylinder",
        "frustum",
    ]
    for row in blocked:
        assert set(row) == PRIMITIVESPEC_CANDIDATE_SOURCE_AUDIT_ROW_REQUIRED_KEYS
        assert row["primitive_spec_kind"] is None
        assert row["source_role"] == "blocked_paper_family"
        assert row["candidate_source_decision"] == ("blocked_until_approximation_policy")
        assert row["candidate_source_reason"] == (
            "paper_family_requires_explicit_approximation_policy_before_runtime_source"
        )
        assert row["required_future_policy"] == "approximation_policy"

    assert [row["paper_primitive"] for row in noop] == ["trapezoidal_prism"]
    row = noop[0]
    assert set(row) == PRIMITIVESPEC_CANDIDATE_SOURCE_AUDIT_ROW_REQUIRED_KEYS
    assert row["primitive_spec_kind"] is None
    assert row["source_role"] == "unmapped_paper_family"
    assert row["candidate_source_decision"] == "no_current_native_candidate_source"
    assert row["candidate_source_reason"] == (
        "paper_family_has_no_newton_native_mapping_in_current_policy"
    )
    assert row["required_future_policy"] == "native_current_fixture_or_explicit_mapping_policy"

    assert len(current) == 16
    for row in current:
        assert set(row) == PRIMITIVESPEC_CANDIDATE_SOURCE_AUDIT_ROW_REQUIRED_KEYS
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["primitive_spec_kind"] is None
        assert row["candidate_mapping_label"] == "offline_only_unmapped"
        assert row["source_role"] == "current_unmapped_row"
        assert row["candidate_source_decision"] == (
            "current_row_ineligible_unmapped_paper_primitive"
        )
        assert row["candidate_source_reason"] == (
            "current_row_is_trapezoidal_prism_offline_only_unmapped"
        )
        assert row["required_future_policy"] == "native_current_fixture"

    for row in _all_candidate_source_rows(payload):
        assert row["eligible_current_candidate_source"] is False
        assert row["primitive_spec_generation_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["required_later_gate"] == EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_primitivespec_candidate_source_coverage_summary_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_candidate_source_contract"]

    assert payload["coverage_summary"] == {
        "candidate_source_requirement_row_count": 6,
        "native_template_candidate_source_audit_row_count": 3,
        "blocked_family_candidate_source_audit_row_count": 2,
        "noop_family_candidate_source_audit_row_count": 1,
        "current_row_candidate_source_audit_row_count": 16,
        "eligible_current_candidate_source_count": 0,
        "ineligible_current_candidate_source_count": 16,
        "future_template_only_source_count": 3,
        "blocked_policy_source_count": 2,
        "noop_unmapped_family_source_count": 1,
        "primitive_spec_generation_candidate_record_count": 0,
        "generated_primitive_spec_record_count": 0,
        "generated_collision_package_record_count": 0,
        "runtime_admissibility_check_record_count": 0,
        "current_paper_primitive_distribution": {"trapezoidal_prism": 16},
        "current_mapping_label_distribution": {"offline_only_unmapped": 16},
        "candidate_source_decision_distribution": {
            "template_only_not_current_candidate_source": 3,
            "blocked_until_approximation_policy": 2,
            "no_current_native_candidate_source": 1,
            "current_row_ineligible_unmapped_paper_primitive": 16,
        },
    }


def test_cpd_paper_primitivespec_candidate_source_stays_report_only(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_candidate_source_contract"]

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
    for row in _all_candidate_source_rows(payload):
        assert forbidden_keys.isdisjoint(row)
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_primitivespec_candidate_source_rejects_wrong_input_gate():
    generation = _candidate_source_generation_input()
    generation["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_candidate_source_input_gate_id_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_stale_input_next_gate():
    generation = _candidate_source_generation_input()
    generation["next_required_gate"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_candidate_source_input_next_gate_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_true_input_trigger_flags():
    generation = _candidate_source_generation_input()
    generation["real_usd_loaded"] = True

    with pytest.raises(
        ValueError,
        match="primitivespec_candidate_source_input_trigger_flag_true:real_usd_loaded",
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "paper_faithful_offline_allowed",
        "package_generation_allowed",
    ],
)
def test_cpd_paper_primitivespec_candidate_source_rejects_top_level_boundary_flags(
    field_name,
):
    generation = _candidate_source_generation_input()
    generation[field_name] = True

    with pytest.raises(
        ValueError,
        match=f"primitivespec_candidate_source_input_boundary_flag_true:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("field_name", "error_label"),
    [
        (
            "primitive_spec_generation_candidate_count",
            "primitivespec_candidate_source_input_candidate_count_nonzero",
        ),
        (
            "offline_primitivespec_template_count",
            "primitivespec_candidate_source_input_template_count_mismatch",
        ),
        (
            "generated_primitive_spec_count",
            "primitivespec_candidate_source_input_generated_spec_nonzero",
        ),
        (
            "generated_collision_package_count",
            "primitivespec_candidate_source_input_generated_collision_package_nonzero",
        ),
        (
            "runtime_admissibility_check_count",
            "primitivespec_candidate_source_input_runtime_admissibility_nonzero",
        ),
    ],
)
def test_cpd_paper_primitivespec_candidate_source_rejects_bad_counts(
    field_name,
    error_label,
):
    generation = _candidate_source_generation_input()
    generation[field_name] = 1 if field_name != "offline_primitivespec_template_count" else 2

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_contract_drift():
    generation = _candidate_source_generation_input()
    contract = dict(generation["primitive_spec_generation_contract"])
    contract["current_candidate_source_gate_required"] = "stale_gate"
    generation["primitive_spec_generation_contract"] = contract

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_candidate_source_input_contract_mismatch:"
            "current_candidate_source_gate_required"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_coverage_mismatch():
    generation = _candidate_source_generation_input()
    coverage = dict(generation["coverage_summary"])
    coverage["current_row_primitivespec_generation_row_count"] = 15
    generation["coverage_summary"] = coverage

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_candidate_source_coverage_count_mismatch:"
            "current_row_primitivespec_generation_row_count"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_native_template_sequence_drift():
    generation = _candidate_source_generation_input()
    rows = [dict(row) for row in generation["native_family_primitivespec_template_rows"]]
    rows[0]["paper_primitive"] = "sphere"
    generation["native_family_primitivespec_template_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_candidate_source_native_template_sequence_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "template_only",
            False,
            "primitivespec_candidate_source_template_runtime_leak:template_only",
        ),
        (
            "runtime_instance_generated",
            True,
            "primitivespec_candidate_source_template_runtime_leak:runtime_instance_generated",
        ),
        (
            "primitive_spec_kind",
            "capsule",
            "primitivespec_candidate_source_template_kind_mismatch:oriented_bounding_box",
        ),
        (
            "candidate_mapping_label",
            "capsule",
            "primitivespec_candidate_source_template_mapping_mismatch:oriented_bounding_box",
        ),
    ],
)
def test_cpd_paper_primitivespec_candidate_source_rejects_native_template_drift(
    field_name,
    bad_value,
    error_label,
):
    generation = _candidate_source_generation_input()
    rows = [dict(row) for row in generation["native_family_primitivespec_template_rows"]]
    rows[0][field_name] = bad_value
    generation["native_family_primitivespec_template_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_current_row_not_unmapped():
    generation = _candidate_source_generation_input()
    rows = [dict(row) for row in generation["current_row_primitivespec_generation_rows"]]
    rows[0]["offline_mapping_label"] = "box"
    generation["current_row_primitivespec_generation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_candidate_source_current_row_not_unmapped",
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_missing_template_source_id():
    generation = _candidate_source_generation_input()
    rows = [dict(row) for row in generation["native_family_primitivespec_template_rows"]]
    rows[0]["source_conversion_plan_row_id"] = ""
    generation["native_family_primitivespec_template_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_candidate_source_missing_template_source_id:"
            "source_conversion_plan_row_id"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_current_row_runtime_leak():
    generation = _candidate_source_generation_input()
    rows = [dict(row) for row in generation["current_row_primitivespec_generation_rows"]]
    rows[0]["primitive_spec_generation_candidate"] = True
    generation["current_row_primitivespec_generation_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_candidate_source_current_row_runtime_leak:"
            "primitive_spec_generation_candidate"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_primitivespec_candidate_source_rejects_duplicate_row_ids():
    rows = [
        {"candidate_source_audit_row_id": "duplicate"},
        {"candidate_source_audit_row_id": "duplicate"},
    ]

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_candidate_source_row_id",
    ):
        cpd_paper_offline._paper_require_unique_candidate_source_row_ids(rows)


def test_cpd_paper_primitivespec_candidate_source_rejects_duplicate_input_row_ids():
    generation = _candidate_source_generation_input()
    native_rows = [dict(row) for row in generation["native_family_primitivespec_template_rows"]]
    current_rows = [dict(row) for row in generation["current_row_primitivespec_generation_rows"]]
    current_rows[0]["primitive_spec_generation_row_id"] = native_rows[0][
        "primitive_spec_generation_template_row_id"
    ]
    generation["native_family_primitivespec_template_rows"] = native_rows
    generation["current_row_primitivespec_generation_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_candidate_source_input_row_id",
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_candidate_source_contract_payload(
            generation
        )


def test_cpd_paper_records_mapped_subset_native_current_fixture_contract_gate(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_native_current_fixture_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["status"] == "partial"
    assert report["package_generation_triggered"] is False
    assert report["newton_runtime_triggered"] is False
    assert report["real_usd_triggered"] is False
    assert report["benchmark_triggered"] is False
    assert report["collision_quality_measured"] is False
    assert report["deployment_or_certification_claimed"] is False

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
    assert payload["gate_status"] == (
        "implemented_offline_native_current_fixture_contract_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
    assert (
        payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "native_current_fixture_contract_complete_"
        "primitivespec_native_fixture_generation_contract_missing"
    )
    assert payload["eligible_current_candidate_source_count"] == 1
    assert payload["primitive_spec_generation_candidate_count"] == 1
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_NATIVE_CURRENT_FIXTURE_REMAINING_GAPS


def test_cpd_paper_native_current_fixture_payload_schema_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_native_current_fixture_contract"]

    assert set(payload) == NATIVE_CURRENT_FIXTURE_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_native_current_fixture_source_not_primitivespec_not_collision_package"
    )
    assert payload["implementation_boundary"] == (
        "offline_native_current_fixture_source_only_no_runtime_primitivespec_"
        "no_collision_package_no_newton"
    )
    assert payload["native_current_fixture_action"] == (
        "record_one_synthetic_native_current_fixture_source"
    )
    assert payload["native_current_fixture_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT),
        "native_current_fixture_gate_closed": (
            EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT
        ),
        "next_generation_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_fit_selected_paper_primitive_required": "oriented_bounding_box",
        "source_template_row_required": ("candidate_source_template__oriented_bounding_box"),
        "native_fixture_rows_required": 1,
        "eligible_current_candidate_sources_required": 1,
        "primitive_spec_generation_candidates_required": 1,
        "generated_primitivespecs_required": 0,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
        "runtime_primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "approximation_policy_enabled": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
        "input_next_required_gate": (EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT),
        "input_eligible_current_candidate_source_count": 0,
        "input_primitive_spec_generation_candidate_count": 0,
        "input_generated_primitive_spec_count": 0,
        "input_generated_collision_package_count": 0,
        "input_runtime_admissibility_check_count": 0,
        "native_template_candidate_source_audit_row_count": 3,
        "current_row_candidate_source_audit_row_count": 16,
    }
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False


def test_cpd_paper_native_current_fixture_records_one_box_source_row(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_native_current_fixture_contract"]

    rows = payload["native_current_fixture_source_rows"]
    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NATIVE_CURRENT_FIXTURE_SOURCE_ROW_REQUIRED_KEYS
    assert row["native_current_fixture_source_row_id"] == (
        "native_current_fixture__paper_single_box__oriented_bounding_box"
    )
    assert (
        row["source_candidate_source_audit_row_id"]
        == "candidate_source_template__oriented_bounding_box"
    )
    assert row["fixture_id"] == "paper_single_box"
    assert row["fixture_source_faces"] == list(range(12))
    assert row["source_fit_selected_paper_primitive"] == "oriented_bounding_box"
    assert row["source_fit_candidate_scope"] == "paper_primitive_set_offline_audit_slice"
    assert row["source_fit_selection_rule"] == ("min_paper_weighted_volume_for_fixture_audit")
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["candidate_mapping_label"] == "box"
    assert row["newton_runtime_kind"] == "box"
    assert row["source_role"] == "synthetic_native_current_fixture"
    assert row["candidate_source_decision"] == ("eligible_synthetic_native_current_fixture_source")
    assert row["candidate_source_reason"] == (
        "paper_single_box_selected_obb_fixture_is_newton_native_box_source"
    )
    assert row["eligible_current_candidate_source"] is True
    assert row["primitive_spec_generation_candidate"] is True
    assert row["generated_primitive_spec"] is None
    assert (
        row["required_later_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    )
    assert row["required_future_policy"] == ("report_only_primitivespec_native_fixture_generation")
    assert row["fit_model"] == "paper_operator_eigenbasis_projected_bounds"
    assert row["axis_selection_policy"] == "paper_q_eigenbasis"
    assert len(row["center"]) == 3
    assert len(row["axes"]) == 3
    assert all(len(axis) == 3 for axis in row["axes"])
    assert len(row["half_extents"]) == 3
    assert all(value > 0.0 for value in row["half_extents"])
    assert row["volume"] > 0.0
    assert row["weighted_volume"] > 0.0
    assert row["contains_assigned_points"] is True
    assert row["primitive_parameter_lower_clamp"] == 0.001
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert row[flag] is False


def test_cpd_paper_native_current_fixture_coverage_summary_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_native_current_fixture_contract"]

    assert payload["fixture_source_summary"] == {
        "fixture_id": "paper_single_box",
        "fixture_source_faces": list(range(12)),
        "selected_paper_primitive": "oriented_bounding_box",
        "selected_newton_runtime_kind": "box",
        "contains_assigned_points": True,
    }
    assert payload["coverage_summary"] == {
        "native_current_fixture_source_row_count": 1,
        "eligible_current_candidate_source_count": 1,
        "primitive_spec_generation_candidate_record_count": 1,
        "generated_primitive_spec_record_count": 0,
        "generated_collision_package_record_count": 0,
        "runtime_admissibility_check_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "paper_primitive_distribution": {"oriented_bounding_box": 1},
        "candidate_mapping_label_distribution": {"box": 1},
        "native_current_fixture_decision_distribution": {
            "eligible_synthetic_native_current_fixture_source": 1,
        },
    }


def test_cpd_paper_native_current_fixture_stays_report_only(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_native_current_fixture_contract"]

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
    assert payload["primitive_spec_generation_candidate_count"] == 1
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False
    for row in payload["native_current_fixture_source_rows"]:
        assert forbidden_keys.isdisjoint(row)
        assert row["primitive_spec_generation_candidate"] is True
        assert row["generated_primitive_spec"] is None
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_native_current_fixture_rejects_wrong_candidate_source_gate():
    candidate_source = _native_current_fixture_candidate_source_input()
    candidate_source["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="native_current_fixture_input_gate_id_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_stale_candidate_source_next_gate():
    candidate_source = _native_current_fixture_candidate_source_input()
    candidate_source["next_required_gate"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="native_current_fixture_input_next_gate_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "eligible_current_candidate_source_count",
            1,
            "native_current_fixture_input_candidate_count_nonzero",
        ),
        (
            "primitive_spec_generation_candidate_count",
            1,
            "native_current_fixture_input_generation_candidate_count_nonzero",
        ),
        (
            "generated_primitive_spec_count",
            1,
            "native_current_fixture_input_generated_spec_nonzero",
        ),
        (
            "generated_collision_package_count",
            1,
            "native_current_fixture_input_generated_collision_package_nonzero",
        ),
        (
            "runtime_admissibility_check_count",
            1,
            "native_current_fixture_input_runtime_admissibility_nonzero",
        ),
    ],
)
def test_cpd_paper_native_current_fixture_rejects_nonzero_input_counts(
    field_name,
    bad_value,
    error_label,
):
    candidate_source = _native_current_fixture_candidate_source_input()
    candidate_source[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_true_input_runtime_flags():
    candidate_source = _native_current_fixture_candidate_source_input()
    candidate_source["newton_runtime_triggered"] = True

    with pytest.raises(
        ValueError,
        match="native_current_fixture_input_trigger_flag_true:newton_runtime_triggered",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "eligible_current_candidate_source",
            True,
            "native_current_fixture_current_row_runtime_leak:eligible_current_candidate_source",
        ),
        (
            "primitive_spec_generation_candidate",
            True,
            "native_current_fixture_current_row_runtime_leak:primitive_spec_generation_candidate",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "native_current_fixture_current_row_runtime_leak:generated_primitive_spec",
        ),
        (
            "newton_runtime_triggered",
            True,
            "native_current_fixture_input_trigger_flag_true:newton_runtime_triggered",
        ),
    ],
)
def test_cpd_paper_native_current_fixture_rejects_current_row_runtime_leaks(
    field_name,
    bad_value,
    error_label,
):
    candidate_source = _native_current_fixture_candidate_source_input()
    rows = [dict(row) for row in candidate_source["current_row_candidate_source_audit_rows"]]
    rows[0][field_name] = bad_value
    candidate_source["current_row_candidate_source_audit_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_coverage_mismatch():
    candidate_source = _native_current_fixture_candidate_source_input()
    coverage = dict(candidate_source["coverage_summary"])
    coverage["native_template_candidate_source_audit_row_count"] = 2
    candidate_source["coverage_summary"] = coverage

    with pytest.raises(
        ValueError,
        match=(
            "native_current_fixture_coverage_count_mismatch:"
            "native_template_candidate_source_audit_row_count"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "primitive_spec_kind",
            "capsule",
            "native_current_fixture_template_row_mismatch:primitive_spec_kind",
        ),
        (
            "source_role",
            "current_unmapped_row",
            "native_current_fixture_template_row_mismatch:source_role",
        ),
        (
            "eligible_current_candidate_source",
            True,
            "native_current_fixture_template_row_runtime_leak:eligible_current_candidate_source",
        ),
        (
            "primitive_spec_generation_candidate",
            True,
            "native_current_fixture_template_row_runtime_leak:primitive_spec_generation_candidate",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "native_current_fixture_template_row_runtime_leak:generated_primitive_spec",
        ),
        (
            "newton_runtime_triggered",
            True,
            "native_current_fixture_input_trigger_flag_true:newton_runtime_triggered",
        ),
    ],
)
def test_cpd_paper_native_current_fixture_rejects_template_drift(
    field_name,
    bad_value,
    error_label,
):
    candidate_source = _native_current_fixture_candidate_source_input()
    rows = [dict(row) for row in candidate_source["native_template_candidate_source_audit_rows"]]
    rows[0][field_name] = bad_value
    candidate_source["native_template_candidate_source_audit_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_missing_obb_template_row():
    candidate_source = _native_current_fixture_candidate_source_input()
    rows = [dict(row) for row in candidate_source["native_template_candidate_source_audit_rows"]]
    rows[0]["candidate_source_audit_row_id"] = "stale_template"
    candidate_source["native_template_candidate_source_audit_rows"] = rows

    with pytest.raises(
        ValueError,
        match="native_current_fixture_obb_template_row_missing",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            candidate_source,
            _native_current_fixture_cases_input(),
        )


def test_cpd_paper_native_current_fixture_rejects_missing_single_box_case():
    cases = [
        case
        for case in _native_current_fixture_cases_input()
        if case["case_id"] != "paper_single_box"
    ]

    with pytest.raises(
        ValueError,
        match="native_current_fixture_source_case_missing:paper_single_box",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


def test_cpd_paper_native_current_fixture_rejects_duplicate_single_box_case():
    cases = _native_current_fixture_cases_input()
    single_box = next(case for case in cases if case["case_id"] == "paper_single_box")
    cases.append(json.loads(json.dumps(single_box)))

    with pytest.raises(
        ValueError,
        match="native_current_fixture_source_case_missing:paper_single_box",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


def test_cpd_paper_native_current_fixture_rejects_missing_primitive_fit_audit():
    cases = _native_current_fixture_cases_input()
    case = next(case for case in cases if case["case_id"] == "paper_single_box")
    del case["primitive_fit_audit"]

    with pytest.raises(
        ValueError,
        match="native_current_fixture_missing_primitive_fit_audit",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        ("paper_primitive", "sphere", "native_current_fixture_selected_fit_not_obb"),
        (
            "newton_runtime_kind",
            "capsule",
            "native_current_fixture_selected_fit_not_newton_box",
        ),
        (
            "current_implementation_kind",
            "offline_paper_sphere_fit",
            "native_current_fixture_selected_fit_not_obb",
        ),
        (
            "fit_model",
            "stale_fit_model",
            "native_current_fixture_fit_model_mismatch",
        ),
        (
            "axis_selection_policy",
            "stale_axis_policy",
            "native_current_fixture_axis_policy_mismatch",
        ),
        (
            "contains_assigned_points",
            False,
            "native_current_fixture_selected_fit_not_containing_points",
        ),
        (
            "primitive_parameter_lower_clamp",
            0.2,
            "native_current_fixture_clamp_mismatch",
        ),
        ("volume", float("nan"), "native_current_fixture_invalid_volume"),
        (
            "weighted_volume",
            float("inf"),
            "native_current_fixture_invalid_weighted_volume",
        ),
    ],
)
def test_cpd_paper_native_current_fixture_rejects_selected_fit_drift(
    field_name,
    bad_value,
    error_label,
):
    cases = _native_current_fixture_cases_input()
    case = next(case for case in cases if case["case_id"] == "paper_single_box")
    selected = dict(case["primitive_fit_audit"]["selected"])
    selected[field_name] = bad_value
    case["primitive_fit_audit"]["selected"] = selected

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "center",
            [123.0, 456.0, 789.0],
            "native_current_fixture_selected_fit_geometry_mismatch:center",
        ),
        (
            "axes",
            [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            "native_current_fixture_selected_fit_geometry_mismatch:axes",
        ),
        (
            "half_extents",
            [0.5, 0.75, 1.25],
            "native_current_fixture_selected_fit_geometry_mismatch:half_extents",
        ),
        (
            "volume",
            42.0,
            "native_current_fixture_selected_fit_geometry_mismatch:volume",
        ),
        (
            "weighted_volume",
            43.0,
            "native_current_fixture_selected_fit_geometry_mismatch:weighted_volume",
        ),
    ],
)
def test_cpd_paper_native_current_fixture_rejects_valid_selected_geometry_drift(
    field_name,
    bad_value,
    error_label,
):
    cases = _native_current_fixture_cases_input()
    case = next(case for case in cases if case["case_id"] == "paper_single_box")
    selected = dict(case["primitive_fit_audit"]["selected"])
    if field_name == "half_extents":
        dimensions = dict(selected["dimensions"])
        dimensions["half_extents"] = bad_value
        selected["dimensions"] = dimensions
    else:
        selected[field_name] = bad_value
    case["primitive_fit_audit"]["selected"] = selected

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


def test_cpd_paper_native_current_fixture_rejects_empty_source_faces():
    cases = _native_current_fixture_cases_input()
    case = next(case for case in cases if case["case_id"] == "paper_single_box")
    case["primitive_fit_audit"]["source_faces"] = []

    with pytest.raises(
        ValueError,
        match="native_current_fixture_selected_fit_missing_source_faces",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        ("center", [0.0, float("nan"), 0.0], "native_current_fixture_invalid_center"),
        (
            "axes",
            [[1.0, 0.0, 0.0], [0.0, float("inf"), 0.0], [0.0, 0.0, 1.0]],
            "native_current_fixture_invalid_axes",
        ),
    ],
)
def test_cpd_paper_native_current_fixture_rejects_invalid_top_level_geometry(
    field_name,
    bad_value,
    error_label,
):
    cases = _native_current_fixture_cases_input()
    case = next(case for case in cases if case["case_id"] == "paper_single_box")
    selected = dict(case["primitive_fit_audit"]["selected"])
    selected[field_name] = bad_value
    case["primitive_fit_audit"]["selected"] = selected

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


def test_cpd_paper_native_current_fixture_rejects_invalid_half_extents():
    cases = _native_current_fixture_cases_input()
    case = next(case for case in cases if case["case_id"] == "paper_single_box")
    selected = dict(case["primitive_fit_audit"]["selected"])
    dimensions = dict(selected["dimensions"])
    dimensions["half_extents"] = [0.0, 0.5, 1.0]
    selected["dimensions"] = dimensions
    case["primitive_fit_audit"]["selected"] = selected

    with pytest.raises(
        ValueError,
        match="native_current_fixture_invalid_half_extents",
    ):
        cpd_paper_offline._paper_mapped_subset_native_current_fixture_contract_payload(
            _native_current_fixture_candidate_source_input(),
            cases,
        )


def test_cpd_paper_records_mapped_subset_primitivespec_native_fixture_generation_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_native_fixture_generation_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_offline_native_fixture_primitivespec_generation_contract_only_partial"
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    )
    assert payload["input_gate_id"] == (EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT)
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "native_fixture_primitivespec_generation_contract_complete_serialization_contract_missing"
    )
    assert payload["primitive_spec_generation_candidate_count"] == 1
    assert payload["offline_serialized_primitivespec_like_dict_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_NATIVE_FIXTURE_GENERATION_REMAINING_GAPS


def test_cpd_paper_primitivespec_native_fixture_generation_payload_schema_is_exact(
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
    ]

    assert set(payload) == NATIVE_FIXTURE_PRIMITIVESPEC_GENERATION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_native_fixture_primitivespec_like_dict_not_runtime_"
        "primitivespec_not_collision_package"
    )
    assert payload["implementation_boundary"] == (
        "offline_native_fixture_primitivespec_like_dict_only_no_runtime_"
        "primitivespec_no_collision_package_no_newton_no_real_usd_no_benchmark"
    )
    assert payload["native_fixture_primitivespec_generation_action"] == (
        "emit_one_report_only_serialized_primitivespec_like_dict"
    )
    assert payload["native_fixture_primitivespec_generation_contract"] == {
        "input_gate_required": EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
        "native_fixture_generation_gate_closed": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
        ),
        "next_serialization_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_paper_primitive_required": "oriented_bounding_box",
        "source_primitive_spec_kind_required": "box",
        "offline_serialized_primitivespec_like_dicts_required": 1,
        "generated_runtime_primitivespecs_required": 0,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
        "runtime_primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    }
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False


def test_cpd_paper_primitivespec_native_fixture_generation_emits_one_serialized_box_spec(
    cpd_paper_report,
):
    report = cpd_paper_report
    source_row = report["paper_mapped_subset_native_current_fixture_contract"][
        "native_current_fixture_source_rows"
    ][0]
    payload = report["paper_mapped_subset_primitivespec_native_fixture_generation_contract"]

    rows = payload["native_fixture_primitivespec_generation_rows"]
    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NATIVE_FIXTURE_PRIMITIVESPEC_GENERATION_ROW_REQUIRED_KEYS
    assert row["native_fixture_primitivespec_generation_row_id"] == (
        "native_fixture_primitivespec_generation__paper_single_box__oriented_bounding_box__box"
    )
    assert (
        row["source_native_current_fixture_source_row_id"]
        == (source_row["native_current_fixture_source_row_id"])
    )
    assert row["fixture_id"] == "paper_single_box"
    assert row["fixture_source_faces"] == source_row["fixture_source_faces"]
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["candidate_mapping_label"] == "box"
    assert row["newton_runtime_kind"] == "box"
    assert row["generation_decision"] == (
        "report_only_serialized_primitivespec_like_dict_generated"
    )
    assert row["generation_action"] == "emit_offline_serialized_dict_only"
    assert row["primitive_spec_generation_candidate"] is True
    assert row["runtime_instance_generated"] is False
    assert row["generated_primitive_spec"] is None
    assert row["required_later_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
    )
    assert row["required_future_policy"] == (
        "report_only_primitivespec_payload_serialization_contract"
    )
    assert row["center"] == source_row["center"]
    assert row["axes"] == source_row["axes"]
    assert row["half_extents"] == source_row["half_extents"]
    assert row["volume"] == source_row["volume"]
    assert row["weighted_volume"] == source_row["weighted_volume"]
    assert row["contains_assigned_points"] == source_row["contains_assigned_points"]

    spec = row["offline_serialized_primitivespec_like_dict"]
    assert isinstance(spec, dict)
    json.dumps(spec)
    assert set(spec) == SERIALIZED_PRIMITIVESPEC_LIKE_DICT_REQUIRED_KEYS
    assert spec == {
        "primitive_id": "paper_single_box__oriented_bounding_box__box",
        "kind": "box",
        "pose": [],
        "center": source_row["center"],
        "axes": source_row["axes"],
        "dimensions": {"half_extents": source_row["half_extents"]},
        "frame": "asset",
        "source_faces": source_row["fixture_source_faces"],
        "contains_assigned_points": True,
        "volume": source_row["volume"],
        "weighted_volume": source_row["weighted_volume"],
        "conversion_status": (
            "report_only_offline_serialized_primitivespec_like_dict_not_runtime_object"
        ),
    }


def test_cpd_paper_primitivespec_native_fixture_generation_coverage_summary_is_exact(
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
    ]

    assert payload["coverage_summary"] == {
        "native_current_fixture_source_row_count": 1,
        "primitive_spec_generation_candidate_record_count": 1,
        "offline_serialized_primitivespec_like_dict_record_count": 1,
        "generated_runtime_primitive_spec_record_count": 0,
        "generated_primitive_spec_record_count": 0,
        "generated_collision_package_record_count": 0,
        "runtime_admissibility_check_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "paper_primitive_distribution": {"oriented_bounding_box": 1},
        "primitive_spec_kind_distribution": {"box": 1},
        "generation_decision_distribution": {
            "report_only_serialized_primitivespec_like_dict_generated": 1,
        },
    }


def test_cpd_paper_primitivespec_native_fixture_generation_stays_report_only(cpd_paper_report):
    payload = cpd_paper_report[
        "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
    ]

    forbidden_keys = {
        "CollisionPackage",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "timing",
        "surface_distance",
        "collision_quality",
    }
    assert forbidden_keys.isdisjoint(payload)
    assert payload["offline_serialized_primitivespec_like_dict_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False
    for row in payload["native_fixture_primitivespec_generation_rows"]:
        assert forbidden_keys.isdisjoint(row)
        assert row["generated_primitive_spec"] is None
        assert row["runtime_instance_generated"] is False
        for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_primitivespec_native_fixture_generation_rejects_wrong_input_gate():
    native_fixture = _native_fixture_primitivespec_generation_input()
    native_fixture["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_native_fixture_generation_input_gate_id_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_generation_contract_payload(
            native_fixture
        )


def test_cpd_paper_primitivespec_native_fixture_generation_rejects_stale_next_gate():
    native_fixture = _native_fixture_primitivespec_generation_input()
    native_fixture["next_required_gate"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_native_fixture_generation_input_next_gate_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_generation_contract_payload(
            native_fixture
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "primitivespec_native_fixture_generation_source_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "primitivespec_native_fixture_generation_source_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_primitivespec_native_fixture_generation_rejects_row_count_mismatch(
    mutate_rows,
    error_label,
):
    native_fixture = _native_fixture_primitivespec_generation_input()
    native_fixture["native_current_fixture_source_rows"] = mutate_rows(
        native_fixture["native_current_fixture_source_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_generation_contract_payload(
            native_fixture
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "eligible_current_candidate_source",
            False,
            "primitivespec_native_fixture_generation_source_not_eligible",
        ),
        (
            "primitive_spec_generation_candidate",
            False,
            "primitivespec_native_fixture_generation_source_not_candidate",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "primitivespec_native_fixture_generation_input_generated_spec_nonzero",
        ),
        (
            "primitive_spec_kind",
            "sphere",
            "primitivespec_native_fixture_generation_source_kind_mismatch",
        ),
        (
            "newton_runtime_kind",
            "capsule",
            "primitivespec_native_fixture_generation_source_runtime_kind_mismatch",
        ),
        (
            "newton_runtime_triggered",
            True,
            (
                "primitivespec_native_fixture_generation_input_trigger_flag_true:"
                "newton_runtime_triggered"
            ),
        ),
    ],
)
def test_cpd_paper_primitivespec_native_fixture_generation_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    native_fixture = _native_fixture_primitivespec_generation_input()
    rows = [dict(row) for row in native_fixture["native_current_fixture_source_rows"]]
    rows[0][field_name] = bad_value
    native_fixture["native_current_fixture_source_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_generation_contract_payload(
            native_fixture
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "center",
            [0.0, float("nan"), 0.0],
            "primitivespec_native_fixture_generation_invalid_center",
        ),
        (
            "axes",
            [[1.0, 0.0, 0.0], [0.0, float("inf"), 0.0], [0.0, 0.0, 1.0]],
            "primitivespec_native_fixture_generation_invalid_axes",
        ),
        (
            "half_extents",
            [0.0, 0.5, 1.0],
            "primitivespec_native_fixture_generation_invalid_half_extents",
        ),
        (
            "volume",
            -1.0,
            "primitivespec_native_fixture_generation_invalid_volume",
        ),
        (
            "weighted_volume",
            float("nan"),
            "primitivespec_native_fixture_generation_invalid_weighted_volume",
        ),
        (
            "fixture_source_faces",
            [],
            "primitivespec_native_fixture_generation_missing_source_faces",
        ),
        (
            "fixture_source_faces",
            [0, 1.9],
            "primitivespec_native_fixture_generation_invalid_source_face_id",
        ),
        (
            "fixture_source_faces",
            [0, True],
            "primitivespec_native_fixture_generation_invalid_source_face_id",
        ),
    ],
)
def test_cpd_paper_primitivespec_native_fixture_generation_rejects_invalid_geometry(
    field_name,
    bad_value,
    error_label,
):
    native_fixture = _native_fixture_primitivespec_generation_input()
    rows = [dict(row) for row in native_fixture["native_current_fixture_source_rows"]]
    rows[0][field_name] = bad_value
    native_fixture["native_current_fixture_source_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_generation_contract_payload(
            native_fixture
        )


def test_cpd_paper_records_mapped_subset_primitivespec_native_fixture_serialization_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_native_fixture_serialization_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["serialized_primitivespec_like_dict_count"] == 1
    assert payload["json_serialization_check_count"] == 1
    assert payload["json_round_trip_match_count"] == 1
    assert payload["schema_stability_check_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_NATIVE_FIXTURE_SERIALIZATION_REMAINING_GAPS


def test_cpd_paper_primitivespec_native_fixture_serialization_payload_schema_is_exact(
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    ]

    assert set(payload) == NATIVE_FIXTURE_PRIMITIVESPEC_SERIALIZATION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_json_serialization_audit_not_runtime_primitivespec_not_collision_package"
    )
    assert payload["implementation_boundary"] == (
        "offline_primitivespec_like_dict_serialization_only_no_runtime_"
        "primitivespec_no_collision_package_no_newton_no_real_usd_no_benchmark"
    )
    assert payload["serialization_action"] == (
        "verify_one_report_only_primitivespec_like_dict_json_round_trip"
    )
    assert payload["canonical_json_policy"] == {
        "json_allow_nan": False,
        "json_sort_keys": True,
        "json_separators": [",", ":"],
    }
    assert payload["native_fixture_primitivespec_serialization_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT
        ),
        "native_fixture_serialization_gate_closed": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
        ),
        "next_runtime_boundary_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_paper_primitive_required": "oriented_bounding_box",
        "source_primitive_spec_kind_required": "box",
        "serialized_primitivespec_like_dicts_required": 1,
        "json_serialization_checks_required": 1,
        "json_round_trip_matches_required": 1,
        "schema_stability_checks_required": 1,
        "generated_runtime_primitivespecs_required": 0,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
        "runtime_primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    }
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False


def test_cpd_paper_primitivespec_native_fixture_serialization_records_one_canonical_row(
    cpd_paper_report,
):
    report = cpd_paper_report
    generation_row = report["paper_mapped_subset_primitivespec_native_fixture_generation_contract"][
        "native_fixture_primitivespec_generation_rows"
    ][0]
    payload = report["paper_mapped_subset_primitivespec_native_fixture_serialization_contract"]
    rows = payload["serialization_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NATIVE_FIXTURE_PRIMITIVESPEC_SERIALIZATION_ROW_REQUIRED_KEYS
    assert row["native_fixture_primitivespec_serialization_row_id"] == (
        "native_fixture_primitivespec_serialization__paper_single_box__oriented_bounding_box__box"
    )
    assert (
        row["source_native_fixture_primitivespec_generation_row_id"]
        == (generation_row["native_fixture_primitivespec_generation_row_id"])
    )
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["candidate_mapping_label"] == "box"
    assert row["newton_runtime_kind"] == "box"
    assert row["primitive_id"] == "paper_single_box__oriented_bounding_box__box"
    assert row["kind"] == "box"
    assert row["schema_keys"] == sorted(SERIALIZED_PRIMITIVESPEC_LIKE_DICT_REQUIRED_KEYS)
    assert row["serialized_payload"] == generation_row["offline_serialized_primitivespec_like_dict"]
    expected_json = json.dumps(
        row["serialized_payload"],
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    assert row["canonical_primitivespec_json"] == expected_json
    assert json.loads(row["canonical_primitivespec_json"]) == row["serialized_payload"]
    assert row["json_allow_nan"] is False
    assert row["json_sort_keys"] is True
    assert row["json_separators"] == [",", ":"]
    assert row["json_round_trip_equal"] is True
    assert row["canonical_json_stable"] is True
    assert row["schema_validation_status"] == "passed"
    assert row["serialization_decision"] == (
        "report_only_primitivespec_like_dict_canonical_json_round_trip_passed"
    )
    assert row["runtime_instance_generated"] is False
    assert row["generated_primitive_spec"] is None
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False
        assert row[flag] is False


def test_cpd_paper_primitivespec_native_fixture_serialization_is_deterministic(cpd_paper_report):
    first = cpd_paper_report[
        "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    ]["serialization_rows"][0]["canonical_primitivespec_json"]
    independent_report = _fresh_independent_cpd_paper_offline_report_for_determinism_check()
    assert independent_report is not cpd_paper_report
    second = independent_report[
        "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    ]["serialization_rows"][0]["canonical_primitivespec_json"]

    assert first == second


def test_cpd_paper_primitivespec_native_fixture_serialization_stays_report_only(cpd_paper_report):
    payload = cpd_paper_report[
        "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
    ]

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
    assert payload["serialized_primitivespec_like_dict_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    for row in payload["serialization_rows"]:
        assert forbidden_keys.isdisjoint(row)
        assert row["generated_primitive_spec"] is None
        assert row["runtime_instance_generated"] is False


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "primitivespec_native_fixture_serialization_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "primitivespec_native_fixture_serialization_input_next_gate_mismatch",
        ),
        (
            "newton_runtime_triggered",
            True,
            (
                "primitivespec_native_fixture_serialization_input_trigger_flag_true:"
                "newton_runtime_triggered"
            ),
        ),
    ],
)
def test_cpd_paper_primitivespec_native_fixture_serialization_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    generation = _native_fixture_primitivespec_serialization_input()
    generation[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_serialization_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "primitivespec_native_fixture_serialization_generation_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "primitivespec_native_fixture_serialization_generation_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_primitivespec_native_fixture_serialization_rejects_row_count_mismatch(
    mutate_rows,
    error_label,
):
    generation = _native_fixture_primitivespec_serialization_input()
    generation["native_fixture_primitivespec_generation_rows"] = mutate_rows(
        generation["native_fixture_primitivespec_generation_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_serialization_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "fixture_id",
            "paper_two_boxes",
            "primitivespec_native_fixture_serialization_source_fixture_mismatch",
        ),
        (
            "primitive_spec_kind",
            "sphere",
            "primitivespec_native_fixture_serialization_source_kind_mismatch",
        ),
        (
            "offline_serialized_primitivespec_like_dict",
            None,
            "primitivespec_native_fixture_serialization_missing_payload",
        ),
    ],
)
def test_cpd_paper_primitivespec_native_fixture_serialization_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    generation = _native_fixture_primitivespec_serialization_input()
    rows = [dict(row) for row in generation["native_fixture_primitivespec_generation_rows"]]
    rows[0][field_name] = bad_value
    generation["native_fixture_primitivespec_generation_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_serialization_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("mutate_spec", "error_label"),
    [
        (
            lambda spec: {key: value for key, value in spec.items() if key != "pose"},
            "primitivespec_native_fixture_serialization_payload_schema_mismatch",
        ),
        (
            lambda spec: {**spec, "unexpected": True},
            "primitivespec_native_fixture_serialization_payload_schema_mismatch",
        ),
        (
            lambda spec: {**spec, "kind": "sphere"},
            "primitivespec_native_fixture_serialization_payload_field_drift",
        ),
        (
            lambda spec: {**spec, "volume": float("nan")},
            "primitivespec_native_fixture_serialization_non_strict_json",
        ),
    ],
)
def test_cpd_paper_primitivespec_native_fixture_serialization_rejects_payload_drift(
    mutate_spec,
    error_label,
):
    generation = _native_fixture_primitivespec_serialization_input()
    rows = [dict(row) for row in generation["native_fixture_primitivespec_generation_rows"]]
    rows[0]["offline_serialized_primitivespec_like_dict"] = mutate_spec(
        dict(rows[0]["offline_serialized_primitivespec_like_dict"])
    )
    generation["native_fixture_primitivespec_generation_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_native_fixture_serialization_contract_payload(
            generation
        )


def test_cpd_paper_records_mapped_subset_primitivespec_runtime_boundary_preflight_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["runtime_boundary_preflight_row_count"] == 1
    assert payload["later_runtime_primitivespec_construction_candidate_count"] == 1
    assert payload["runtime_construction_allowed_in_current_gate"] is False
    assert payload["generated_runtime_primitive_spec_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS


def test_cpd_paper_primitivespec_runtime_boundary_preflight_payload_schema_is_exact(
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
    ]

    assert set(payload) == RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_runtime_boundary_preflight_not_runtime_primitivespec_not_collision_package"
    )
    assert payload["implementation_boundary"] == (
        "offline_runtime_boundary_preflight_only_no_runtime_primitivespec_"
        "no_collision_package_no_newton_no_real_usd_no_benchmark"
    )
    assert payload["runtime_boundary_action"] == (
        "record_one_later_runtime_primitivespec_construction_candidate_without_runtime_object"
    )
    assert payload["runtime_boundary_requirements"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT
        ),
        "runtime_boundary_preflight_gate_closed": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "next_runtime_construction_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_paper_primitive_required": "oriented_bounding_box",
        "source_primitive_spec_kind_required": "box",
        "json_round_trip_required": True,
        "schema_validation_required": True,
        "later_runtime_construction_candidates_required": 1,
        "runtime_construction_allowed_in_current_gate": False,
        "generated_runtime_primitivespecs_required": 0,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    }
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False


def test_cpd_paper_primitivespec_runtime_boundary_preflight_records_one_lineage_row(
    cpd_paper_report,
):
    report = cpd_paper_report
    source_row = report["paper_mapped_subset_primitivespec_native_fixture_serialization_contract"][
        "serialization_rows"
    ][0]
    payload = report["paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"]
    rows = payload["runtime_boundary_preflight_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == RUNTIME_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS
    assert row["runtime_boundary_preflight_row_id"] == (
        "runtime_boundary_preflight__paper_single_box__oriented_bounding_box__box"
    )
    assert (
        row["source_native_fixture_primitivespec_serialization_row_id"]
        == (source_row["native_fixture_primitivespec_serialization_row_id"])
    )
    for source_key in (
        "source_native_fixture_primitivespec_generation_row_id",
        "source_native_current_fixture_source_row_id",
        "source_candidate_source_audit_row_id",
        "source_primitivespec_generation_row_id",
        "source_primitivespec_generation_preflight_row_id",
        "source_primitivespec_validation_row_id",
        "source_primitivespec_dry_run_row_id",
        "source_adapter_preflight_row_id",
        "source_candidate_matrix_row_id",
        "source_conversion_plan_row_id",
    ):
        assert row[source_key] == source_row[source_key]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["candidate_mapping_label"] == "box"
    assert row["newton_runtime_kind"] == "box"
    assert row["primitive_id"] == source_row["primitive_id"]
    assert row["kind"] == "box"
    assert row["serialized_payload_schema_keys"] == sorted(source_row["serialized_payload"])
    assert row["canonical_primitivespec_json"] == (source_row["canonical_primitivespec_json"])
    assert (
        row["canonical_primitivespec_json_sha256"]
        == hashlib.sha256(row["canonical_primitivespec_json"].encode("utf-8")).hexdigest()
    )
    assert row["input_json_round_trip_equal"] is True
    assert row["input_canonical_json_stable"] is True
    assert row["input_schema_validation_status"] == "passed"
    assert row["later_runtime_primitivespec_construction_candidate"] is True
    assert row["runtime_construction_allowed_in_current_gate"] is False
    assert row["required_later_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert row["preflight_decision"] == (
        "later_runtime_primitivespec_construction_contract_may_be_proposed"
    )
    assert row["preflight_reason"] == (
        "canonical_json_schema_stable_box_payload_but_current_gate_is_boundary_only"
    )
    assert row["runtime_instance_generated"] is False
    assert row["generated_primitive_spec"] is None
    for flag in PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS:
        assert payload[flag] is False
        assert row[flag] is False


def test_cpd_paper_primitivespec_runtime_boundary_preflight_stays_report_only(cpd_paper_report):
    payload = cpd_paper_report[
        "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
    ]

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
    assert payload["runtime_construction_allowed_in_current_gate"] is False
    assert payload["generated_runtime_primitive_spec_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    for row in payload["runtime_boundary_preflight_rows"]:
        assert forbidden_keys.isdisjoint(row)
        assert row["runtime_construction_allowed_in_current_gate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["runtime_instance_generated"] is False


def test_cpd_paper_runtime_boundary_preflight_helper_has_no_runtime_imports_or_calls():
    source = Path(cpd_paper_offline.__file__).read_text(encoding="utf-8")
    block = source[
        source.index(
            "def _paper_validate_primitivespec_runtime_boundary_preflight_false_flags"
        ) : source.index("def _paper_primitivespec_runtime_construction_source_row")
    ]

    forbidden_patterns = [
        "PrimitiveSpec(",
        "CollisionPackage(",
        "from primitive_collision_compiler.contracts import PrimitiveSpec",
        "from primitive_collision_compiler.contracts import CollisionPackage",
        "primitive_collision_compiler.newton",
        "import newton",
        "import newton_warp",
        "Newton",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in block


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "primitivespec_runtime_boundary_preflight_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "primitivespec_runtime_boundary_preflight_input_next_gate_mismatch",
        ),
        (
            "paper_faithful_offline_allowed",
            True,
            (
                "primitivespec_runtime_boundary_preflight_input_trigger_flag_true:"
                "paper_faithful_offline_allowed"
            ),
        ),
        (
            "package_generation_allowed",
            True,
            (
                "primitivespec_runtime_boundary_preflight_input_trigger_flag_true:"
                "package_generation_allowed"
            ),
        ),
        (
            "newton_runtime_triggered",
            True,
            (
                "primitivespec_runtime_boundary_preflight_input_trigger_flag_true:"
                "newton_runtime_triggered"
            ),
        ),
    ],
)
def test_cpd_paper_primitivespec_runtime_boundary_preflight_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    serialization = _runtime_boundary_preflight_input()
    serialization[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_payload(
            serialization
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "primitivespec_runtime_boundary_preflight_serialization_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "primitivespec_runtime_boundary_preflight_serialization_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_primitivespec_runtime_boundary_preflight_rejects_row_count_mismatch(
    mutate_rows,
    error_label,
):
    serialization = _runtime_boundary_preflight_input()
    serialization["serialization_rows"] = mutate_rows(serialization["serialization_rows"])

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_payload(
            serialization
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "fixture_id",
            "paper_two_boxes",
            "primitivespec_runtime_boundary_preflight_source_fixture_mismatch",
        ),
        (
            "primitive_spec_kind",
            "sphere",
            "primitivespec_runtime_boundary_preflight_source_kind_mismatch",
        ),
        (
            "serialized_payload",
            None,
            "primitivespec_runtime_boundary_preflight_serialized_payload_missing",
        ),
        (
            "json_round_trip_equal",
            False,
            "primitivespec_runtime_boundary_preflight_json_round_trip_missing",
        ),
        (
            "schema_validation_status",
            "failed",
            "primitivespec_runtime_boundary_preflight_schema_validation_missing",
        ),
        (
            "runtime_instance_generated",
            True,
            (
                "primitivespec_runtime_boundary_preflight_runtime_object_leak:"
                "runtime_instance_generated"
            ),
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            (
                "primitivespec_runtime_boundary_preflight_runtime_object_leak:"
                "generated_primitive_spec"
            ),
        ),
    ],
)
def test_cpd_paper_primitivespec_runtime_boundary_preflight_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    serialization = _runtime_boundary_preflight_input()
    rows = [dict(row) for row in serialization["serialization_rows"]]
    rows[0][field_name] = bad_value
    serialization["serialization_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_payload(
            serialization
        )


@pytest.mark.parametrize(
    ("mutate_row", "error_label"),
    [
        (
            lambda row: {
                **row,
                "schema_keys": row["schema_keys"][:-1],
            },
            "primitivespec_runtime_boundary_preflight_serialized_payload_schema_mismatch",
        ),
        (
            lambda row: {
                **row,
                "serialized_payload": {
                    **row["serialized_payload"],
                    "unexpected": True,
                },
            },
            "primitivespec_runtime_boundary_preflight_serialized_payload_schema_mismatch",
        ),
        (
            lambda row: {
                **row,
                "canonical_primitivespec_json": "{}",
            },
            "primitivespec_runtime_boundary_preflight_canonical_json_mismatch",
        ),
        (
            lambda row: {
                **row,
                "canonical_primitivespec_json": json.dumps(
                    {**row["serialized_payload"], "kind": "sphere"},
                    allow_nan=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            },
            "primitivespec_runtime_boundary_preflight_canonical_json_mismatch",
        ),
        (
            lambda row: {
                **row,
                "serialized_payload": {
                    **row["serialized_payload"],
                    "kind": "sphere",
                },
                "canonical_primitivespec_json": json.dumps(
                    {**row["serialized_payload"], "kind": "sphere"},
                    allow_nan=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            },
            "primitivespec_runtime_boundary_preflight_serialized_payload_value_mismatch:kind",
        ),
    ],
)
def test_cpd_paper_primitivespec_runtime_boundary_preflight_rejects_json_schema_drift(
    mutate_row,
    error_label,
):
    serialization = _runtime_boundary_preflight_input()
    rows = [dict(row) for row in serialization["serialization_rows"]]
    rows[0] = mutate_row(rows[0])
    serialization["serialization_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_payload(
            serialization
        )


@pytest.mark.parametrize(
    "field_name",
    [
        "serialized_primitivespec_like_dict_count",
        "json_serialization_check_count",
        "json_round_trip_match_count",
        "schema_stability_check_count",
        "generated_runtime_primitive_spec_count",
        "generated_primitive_spec_count",
        "generated_collision_package_count",
        "runtime_admissibility_check_count",
    ],
)
def test_cpd_paper_primitivespec_runtime_boundary_preflight_rejects_count_drift(
    field_name,
):
    serialization = _runtime_boundary_preflight_input()
    serialization[field_name] = 2

    with pytest.raises(
        ValueError,
        match=(f"primitivespec_runtime_boundary_preflight_input_count_mismatch:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract_payload(
            serialization
        )


def test_cpd_paper_records_mapped_subset_primitivespec_runtime_construction_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_primitivespec_runtime_construction_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    for flag in (
        "package_generation_triggered",
        "newton_runtime_triggered",
        "real_usd_triggered",
        "benchmark_triggered",
        "collision_quality_measured",
        "deployment_or_certification_claimed",
    ):
        assert report[flag] is False
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["runtime_construction_row_count"] == 1
    assert payload["constructed_runtime_primitivespec_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 1
    assert payload["generated_primitive_spec_count"] == 1
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_RUNTIME_CONSTRUCTION_REMAINING_GAPS


def test_cpd_paper_primitivespec_runtime_construction_payload_schema_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_runtime_construction_contract"]

    assert set(payload) == RUNTIME_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == ("runtime_primitivespec_construction_not_collision_package")
    assert payload["implementation_boundary"] == (
        "single_synthetic_runtime_primitivespec_only_no_collision_package_"
        "no_newton_no_real_usd_no_benchmark"
    )
    assert payload["runtime_construction_action"] == (
        "construct_one_runtime_primitivespec_from_canonical_preflight_json"
    )
    assert payload["runtime_construction_requirements"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "runtime_construction_gate_closed": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "next_collision_package_generation_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_paper_primitive_required": "oriented_bounding_box",
        "source_primitive_spec_kind_required": "box",
        "constructed_runtime_primitivespecs_required": 1,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    }
    assert payload["runtime_primitivespec_construction_triggered"] is True
    assert payload["runtime_instance_generated"] is True
    for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS:
        assert payload[flag] is False


def test_cpd_paper_primitivespec_runtime_construction_records_one_lineage_row(cpd_paper_report):
    report = cpd_paper_report
    source_row = report["paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"][
        "runtime_boundary_preflight_rows"
    ][0]
    payload = report["paper_mapped_subset_primitivespec_runtime_construction_contract"]
    rows = payload["runtime_construction_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS
    assert row["runtime_construction_row_id"] == (
        "runtime_construction__paper_single_box__oriented_bounding_box__box"
    )
    assert (
        row["source_runtime_boundary_preflight_row_id"]
        == (source_row["runtime_boundary_preflight_row_id"])
    )
    for source_key in (
        "source_native_fixture_primitivespec_serialization_row_id",
        "source_native_fixture_primitivespec_generation_row_id",
        "source_native_current_fixture_source_row_id",
        "source_candidate_source_audit_row_id",
        "source_primitivespec_generation_row_id",
        "source_primitivespec_generation_preflight_row_id",
        "source_primitivespec_validation_row_id",
        "source_primitivespec_dry_run_row_id",
        "source_adapter_preflight_row_id",
        "source_candidate_matrix_row_id",
        "source_conversion_plan_row_id",
    ):
        assert row[source_key] == source_row[source_key]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["candidate_mapping_label"] == "box"
    assert row["newton_runtime_kind"] == "box"
    assert row["primitive_id"] == source_row["primitive_id"]
    assert row["kind"] == "box"
    loaded_payload = json.loads(source_row["canonical_primitivespec_json"])
    assert row["canonical_primitivespec_json"] == (source_row["canonical_primitivespec_json"])
    assert row["loaded_primitivespec_payload"] == loaded_payload
    assert row["constructed_primitivespec_dict"] == (
        _expected_runtime_constructed_primitivespec_dict(loaded_payload)
    )
    assert row["generated_primitive_spec"] == row["constructed_primitivespec_dict"]
    assert row["conversion_status_transition"] == {
        "from": "report_only_offline_serialized_primitivespec_like_dict_not_runtime_object",
        "to": "runtime_primitivespec_constructed_from_canonical_preflight_payload",
    }
    assert row["runtime_instance_generated"] is True
    assert row["runtime_primitivespec_construction_triggered"] is True
    for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS:
        assert payload[flag] is False
        assert row[flag] is False


def test_cpd_paper_primitivespec_runtime_construction_stays_package_newton_and_metric_free(
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_primitivespec_runtime_construction_contract"]

    json.dumps(payload, allow_nan=False, sort_keys=True)
    forbidden_tokens = {
        "CollisionPackage",
        "FallbackSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "surface_distance",
        "timing_result",
        "collision_quality_score",
    }
    assert forbidden_tokens.isdisjoint(set(_recursive_key_value_strings(payload)))
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    for row in payload["runtime_construction_rows"]:
        assert row["runtime_instance_generated"] is True
        assert isinstance(row["generated_primitive_spec"], dict)
        for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_primitivespec_runtime_construction_static_boundaries():
    source = Path(cpd_paper_offline.__file__).read_text(encoding="utf-8")
    construction_block = source[
        source.index("_RUNTIME_CONSTRUCTION_BOUNDARY_FALSE_FLAGS") : source.index(
            "_COLLISION_PACKAGE_GENERATION_PREFLIGHT_PAYLOAD_FALSE_FLAGS"
        )
    ]

    assert (
        construction_block.count("from primitive_collision_compiler.contracts import PrimitiveSpec")
        == 1
    )
    assert construction_block.count("PrimitiveSpec(") == 1
    forbidden_patterns = [
        "CollisionPackage",
        "FallbackSpec",
        "primitive_collision_compiler.newton",
        "import newton",
        "import newton_warp",
        "Newton",
        "run_newton",
        "map_package_shapes",
        "newton.",
        "pxr",
        "Usd",
        "USD",
        "load_first_mesh",
        "inspect_usd_asset",
        "assets.usd_smoke",
        "real_usd_comparison",
        "timeit",
        "perf_counter",
        "benchmark_metric",
        "surface_distance",
        "timing_result",
        "collision_quality_score",
        "run_benchmark",
        "measure_collision_quality",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in construction_block


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "primitivespec_runtime_construction_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "primitivespec_runtime_construction_input_next_gate_mismatch",
        ),
        (
            "package_generation_allowed",
            True,
            (
                "primitivespec_runtime_construction_input_trigger_flag_true:"
                "package_generation_allowed"
            ),
        ),
        (
            "newton_runtime_triggered",
            True,
            ("primitivespec_runtime_construction_input_trigger_flag_true:newton_runtime_triggered"),
        ),
        (
            "collision_quality_measured",
            True,
            (
                "primitivespec_runtime_construction_input_trigger_flag_true:"
                "collision_quality_measured"
            ),
        ),
    ],
)
def test_cpd_paper_primitivespec_runtime_construction_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    preflight = _runtime_construction_input()
    preflight[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_construction_contract_payload(
            preflight
        )


@pytest.mark.parametrize("field_name", RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_primitivespec_runtime_construction_rejects_missing_payload_false_flags(
    field_name,
):
    preflight = _runtime_construction_input()
    del preflight[field_name]

    with pytest.raises(
        ValueError,
        match=(f"primitivespec_runtime_construction_input_trigger_flag_missing:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_construction_contract_payload(
            preflight
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "primitivespec_runtime_construction_preflight_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "primitivespec_runtime_construction_preflight_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_primitivespec_runtime_construction_rejects_row_count_mismatch(
    mutate_rows,
    error_label,
):
    preflight = _runtime_construction_input()
    preflight["runtime_boundary_preflight_rows"] = mutate_rows(
        preflight["runtime_boundary_preflight_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_construction_contract_payload(
            preflight
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "fixture_id",
            "paper_two_boxes",
            "primitivespec_runtime_construction_source_fixture_mismatch",
        ),
        (
            "primitive_spec_kind",
            "sphere",
            "primitivespec_runtime_construction_source_kind_mismatch",
        ),
        (
            "later_runtime_primitivespec_construction_candidate",
            False,
            "primitivespec_runtime_construction_candidate_missing",
        ),
        (
            "runtime_construction_allowed_in_current_gate",
            True,
            "primitivespec_runtime_construction_prior_gate_boundary_mismatch",
        ),
        (
            "runtime_instance_generated",
            True,
            "primitivespec_runtime_construction_prior_runtime_object_leak:runtime_instance_generated",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "primitivespec_runtime_construction_prior_runtime_object_leak:generated_primitive_spec",
        ),
        (
            "canonical_primitivespec_json_sha256",
            "0" * 64,
            "primitivespec_runtime_construction_canonical_json_fingerprint_mismatch",
        ),
    ],
)
def test_cpd_paper_primitivespec_runtime_construction_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    preflight = _runtime_construction_input()
    rows = [dict(row) for row in preflight["runtime_boundary_preflight_rows"]]
    rows[0][field_name] = bad_value
    preflight["runtime_boundary_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_construction_contract_payload(
            preflight
        )


@pytest.mark.parametrize("field_name", RUNTIME_CONSTRUCTION_SOURCE_ROW_FALSE_FLAGS)
def test_cpd_paper_primitivespec_runtime_construction_rejects_missing_source_row_false_flags(
    field_name,
):
    preflight = _runtime_construction_input()
    rows = [dict(row) for row in preflight["runtime_boundary_preflight_rows"]]
    del rows[0][field_name]
    preflight["runtime_boundary_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(f"primitivespec_runtime_construction_input_trigger_flag_missing:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_construction_contract_payload(
            preflight
        )


@pytest.mark.parametrize(
    ("mutate_row", "error_label"),
    [
        (
            lambda row: {**row, "canonical_primitivespec_json": "not-json"},
            "primitivespec_runtime_construction_canonical_json_mismatch",
        ),
        (
            lambda row: {**row, "canonical_primitivespec_json": "{}"},
            "primitivespec_runtime_construction_serialized_payload_schema_mismatch",
        ),
        (
            lambda row: {
                **row,
                "canonical_primitivespec_json": json.dumps(
                    {
                        **json.loads(row["canonical_primitivespec_json"]),
                        "kind": "sphere",
                    },
                    allow_nan=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
            },
            "primitivespec_runtime_construction_serialized_payload_value_mismatch:kind",
        ),
    ],
)
def test_cpd_paper_primitivespec_runtime_construction_rejects_canonical_json_drift(
    mutate_row,
    error_label,
):
    preflight = _runtime_construction_input()
    rows = [dict(row) for row in preflight["runtime_boundary_preflight_rows"]]
    rows[0] = mutate_row(rows[0])
    preflight["runtime_boundary_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_construction_contract_payload(
            preflight
        )


@pytest.mark.parametrize(
    ("mutate_payload", "error_label"),
    [
        (
            lambda payload: {
                **payload,
                "dimensions": {
                    **payload["dimensions"],
                    "unexpected": 123,
                },
            },
            "primitivespec_runtime_construction_serialized_payload_value_mismatch:dimensions",
        ),
        (
            lambda payload: {**payload, "dimensions": {}},
            "primitivespec_runtime_construction_serialized_payload_value_mismatch:dimensions",
        ),
        (
            lambda payload: {
                **payload,
                "dimensions": {"half_extents": [1.0, 2.0]},
            },
            "primitivespec_runtime_construction_serialized_payload_value_mismatch:dimensions",
        ),
        (
            lambda payload: {**payload, "pose": "not-a-list"},
            "primitivespec_runtime_construction_serialized_payload_value_mismatch:pose",
        ),
        (
            lambda payload: {**payload, "center": [0.0, 0.0]},
            "primitivespec_runtime_construction_serialized_payload_value_mismatch:center",
        ),
        (
            lambda payload: {**payload, "axes": "not-a-matrix"},
            "primitivespec_runtime_construction_serialized_payload_value_mismatch:axes",
        ),
        (
            lambda payload: {**payload, "volume": 42.0},
            "primitivespec_runtime_construction_serialized_payload_value_mismatch:volume",
        ),
        (
            lambda payload: {**payload, "weighted_volume": 42.0},
            "primitivespec_runtime_construction_serialized_payload_value_mismatch:weighted_volume",
        ),
        (
            lambda payload: {**payload, "center": [1.25, 0.5, 0.25]},
            "primitivespec_runtime_construction_canonical_json_fingerprint_mismatch",
        ),
        (
            lambda payload: {
                **payload,
                "axes": [
                    [1.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0],
                    [0.0, 0.0, 1.0],
                ],
            },
            "primitivespec_runtime_construction_canonical_json_fingerprint_mismatch",
        ),
        (
            lambda payload: {
                **payload,
                "dimensions": {"half_extents": [0.5, 0.5, 0.5]},
                "volume": 1.0,
                "weighted_volume": 1.0,
            },
            "primitivespec_runtime_construction_canonical_json_fingerprint_mismatch",
        ),
        (
            lambda payload: {**payload, "source_faces": [0]},
            "primitivespec_runtime_construction_canonical_json_fingerprint_mismatch",
        ),
    ],
)
def test_cpd_paper_primitivespec_runtime_construction_rejects_nested_canonical_payload_drift(
    mutate_payload,
    error_label,
):
    preflight = _runtime_construction_input_with_canonical_payload_drift(mutate_payload)

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_primitivespec_runtime_construction_contract_payload(
            preflight
        )
