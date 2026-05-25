import pytest

from tests.cpd_paper_offline_shared import *

pytestmark = pytest.mark.paper_offline


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_boundary_preflight_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"]

    assert report["next_required_gate"] == (EXPECTED_CURRENT_REPORT_NEXT_GATE)
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT)
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["newton_shape_runtime_boundary_preflight_row_count"] == 1
    assert payload["source_shape_mapping_contract_row_count"] == 1
    assert payload["later_newton_shape_runtime_construction_candidate_count"] == 1
    assert payload["report_scoped_newton_shape_descriptor_count"] == 1
    assert payload["runtime_boundary_preflight_passed"] is True
    assert payload["mapping_attempt_count"] == 0
    assert payload["newton_mapping_record_count"] == 0
    assert payload["newton_shape_object_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert (
        payload["remaining_gaps"] == EXPECTED_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_boundary_preflight_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"]
    source_row = report["paper_mapped_subset_newton_shape_mapping_contract"]["shape_mapping_rows"][
        0
    ]

    assert set(payload) == (NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS)
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_offline_newton_shape_runtime_boundary_preflight_only"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_shape_runtime_boundary_preflight_complete_newton_shape_runtime_construction_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_static_newton_shape_runtime_boundary_preflight_not_shape_object"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_newton_shape_runtime_boundary_preflight_only_"
        "no_newton_shape_object_no_runtime_no_real_usd_no_benchmark_no_metrics"
    )
    assert payload["runtime_boundary_preflight_action"] == (
        "record_one_later_newton_shape_runtime_construction_candidate_without_newton_call"
    )
    assert payload["newton_shape_runtime_boundary_preflight_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT),
        "closed_gate": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT),
        "next_newton_shape_runtime_construction_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "runtime_boundary_preflight_rows_required": 1,
        "later_newton_shape_runtime_construction_candidates_required": 1,
        "newton_shape_object_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "source_shape_mapping_row_id": source_row["shape_mapping_row_id"],
        "source_newton_shape_mapping_preflight_row_id": source_row[
            "source_newton_shape_mapping_preflight_row_id"
        ],
        "source_runtime_admissibility_row_id": source_row["source_runtime_admissibility_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_descriptor_kind": source_row["newton_shape_descriptor_dict"]["descriptor_kind"],
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_boundary_preflight_row_count": 1,
        "source_shape_mapping_contract_row_count": 1,
        "later_newton_shape_runtime_construction_candidate_count": 1,
        "report_scoped_newton_shape_descriptor_count": 1,
        "runtime_boundary_preflight_passed_count": 1,
        "mapping_attempt_count": 0,
        "newton_mapping_record_count": 0,
        "newton_shape_object_count": 0,
        "newton_runtime_execution_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "target_newton_shape_kind_distribution": {"box": 1},
    }


def test_cpd_paper_newton_shape_runtime_boundary_preflight_records_one_lineage_row(
    cpd_paper_report,
):
    report = cpd_paper_report
    source_row = report["paper_mapped_subset_newton_shape_mapping_contract"]["shape_mapping_rows"][
        0
    ]
    payload = report["paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"]
    rows = payload["newton_shape_runtime_boundary_preflight_rows"]

    assert len(rows) == 1
    row = rows[0]
    descriptor = source_row["newton_shape_descriptor_dict"]
    assert set(row) == NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS
    assert row["newton_shape_runtime_boundary_preflight_row_id"] == (
        "newton_shape_runtime_boundary_preflight__paper_single_box__box"
    )
    assert row["source_shape_mapping_row_id"] == source_row["shape_mapping_row_id"]
    assert (
        row["source_newton_shape_mapping_preflight_row_id"]
        == (source_row["source_newton_shape_mapping_preflight_row_id"])
    )
    assert (
        row["source_runtime_admissibility_row_id"]
        == (source_row["source_runtime_admissibility_row_id"])
    )
    assert row["source_package_id"] == source_row["source_package_id"]
    assert row["source_asset_id"] == source_row["source_asset_id"]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["primitive_id"] == ("paper_single_box__oriented_bounding_box__box")
    assert row["target_newton_shape_kind"] == "box"
    assert row["descriptor_kind"] == "newton_shape_descriptor"
    assert row["descriptor_center"] == descriptor["center"]
    assert row["descriptor_axes"] == descriptor["axes"]
    assert row["descriptor_half_extents"] == descriptor["half_extents"]
    assert row["runtime_boundary_preflight_passed"] is True
    assert row["descriptor_kind_check_passed"] is True
    assert row["target_kind_check_passed"] is True
    assert row["descriptor_lineage_check_passed"] is True
    assert row["center_descriptor_check_passed"] is True
    assert row["axes_descriptor_check_passed"] is True
    assert row["half_extents_descriptor_check_passed"] is True
    assert row["later_newton_shape_runtime_construction_candidate"] is True
    assert row["mapping_attempt_count"] == 0
    assert row["newton_mapping_record_count"] == 0
    assert row["newton_shape_object_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    assert list(_recursive_package_dicts(payload)) == []


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
    ]

    assert payload[field_name] is False
    assert payload["newton_shape_runtime_boundary_preflight_rows"][0][field_name] is False


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_runtime_boundary_preflight_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_runtime_boundary_preflight_input_next_gate_mismatch",
        ),
        (
            "shape_mapping_contract_row_count",
            2,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "shape_mapping_contract_row_count",
        ),
        (
            "source_newton_shape_mapping_preflight_row_count",
            2,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "source_newton_shape_mapping_preflight_row_count",
        ),
        (
            "report_scoped_newton_shape_descriptor_count",
            2,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "report_scoped_newton_shape_descriptor_count",
        ),
        (
            "mapping_attempt_count",
            1,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:mapping_attempt_count",
        ),
        (
            "newton_mapping_record_count",
            1,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "newton_mapping_record_count",
        ),
        (
            "newton_shape_object_count",
            1,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "newton_shape_object_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "newton_runtime_execution_count",
        ),
        (
            "generated_runtime_primitive_spec_count",
            2,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "generated_runtime_primitive_spec_count",
        ),
        (
            "generated_primitive_spec_count",
            2,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "generated_primitive_spec_count",
        ),
        (
            "generated_collision_package_count",
            2,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "generated_collision_package_count",
        ),
        (
            "runtime_admissibility_check_count",
            2,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "runtime_admissibility_check_count",
        ),
        (
            "offline_static_runtime_admissibility_check_count",
            2,
            "newton_shape_runtime_boundary_preflight_input_count_mismatch:"
            "offline_static_runtime_admissibility_check_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_boundary_preflight_input()
    payload[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_input_forbidden_flags(
    field_name,
):
    payload = _newton_shape_runtime_boundary_preflight_input()
    payload[field_name] = True

    with pytest.raises(
        ValueError,
        match=(f"newton_shape_runtime_boundary_preflight_input_flag_true:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "newton_shape_runtime_boundary_preflight_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "newton_shape_runtime_boundary_preflight_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_row_count_drift(
    mutate_rows,
    error_label,
):
    payload = _newton_shape_runtime_boundary_preflight_input()
    payload["shape_mapping_rows"] = mutate_rows(payload["shape_mapping_rows"])

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "shape_mapping_row_id",
            "wrong_row",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:shape_mapping_row_id",
        ),
        (
            "source_newton_shape_mapping_preflight_row_id",
            "wrong_preflight_row",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:"
            "source_newton_shape_mapping_preflight_row_id",
        ),
        (
            "source_runtime_admissibility_row_id",
            "wrong_runtime_admissibility_row",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:"
            "source_runtime_admissibility_row_id",
        ),
        (
            "source_package_id",
            "wrong_package",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:source_package_id",
        ),
        (
            "source_asset_id",
            "wrong_asset",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:source_asset_id",
        ),
        (
            "fixture_id",
            "wrong_fixture",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:fixture_id",
        ),
        (
            "paper_primitive",
            "sphere",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:paper_primitive",
        ),
        (
            "primitive_spec_kind",
            "sphere",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:primitive_spec_kind",
        ),
        (
            "primitive_id",
            "wrong_primitive",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:primitive_id",
        ),
        (
            "target_newton_shape_kind",
            "sphere",
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:target_newton_shape_kind",
        ),
        (
            "descriptor_contract_passed",
            False,
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:"
            "descriptor_contract_passed",
        ),
        (
            "mapping_attempt_count",
            1,
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:mapping_attempt_count",
        ),
        (
            "newton_mapping_record_count",
            1,
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:"
            "newton_mapping_record_count",
        ),
        (
            "newton_shape_object_count",
            1,
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:newton_shape_object_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_runtime_boundary_preflight_source_row_mismatch:"
            "newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_boundary_preflight_input()
    rows = [json.loads(json.dumps(row)) for row in payload["shape_mapping_rows"]]
    rows[0][field_name] = bad_value
    payload["shape_mapping_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("mutate_descriptor", "error_label"),
    [
        (
            lambda descriptor: None,
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:descriptor",
        ),
        (
            lambda descriptor: [],
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:descriptor",
        ),
        (
            lambda descriptor: {**descriptor, "descriptor_kind": "wrong"},
            "newton_shape_runtime_boundary_preflight_descriptor_mismatch:descriptor_kind",
        ),
        (
            lambda descriptor: {
                **descriptor,
                "target_newton_shape_kind": "sphere",
            },
            "newton_shape_runtime_boundary_preflight_descriptor_mismatch:target_newton_shape_kind",
        ),
        (
            lambda descriptor: {
                **descriptor,
                "source_fixture_id": "wrong_fixture",
            },
            "newton_shape_runtime_boundary_preflight_descriptor_mismatch:source_fixture_id",
        ),
        (
            lambda descriptor: {
                **descriptor,
                "source_primitive_id": "wrong_primitive",
            },
            "newton_shape_runtime_boundary_preflight_descriptor_mismatch:source_primitive_id",
        ),
        (
            lambda descriptor: {
                **descriptor,
                "mapping_contract": "wrong_contract",
            },
            "newton_shape_runtime_boundary_preflight_descriptor_mismatch:mapping_contract",
        ),
        (
            lambda descriptor: {**descriptor, "center": None},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:center",
        ),
        (
            lambda descriptor: {**descriptor, "center": [0.0, 1.0]},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:center",
        ),
        (
            lambda descriptor: {**descriptor, "center": [0.0, "bad", 1.0]},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:center",
        ),
        (
            lambda descriptor: {**descriptor, "center": [0.0, float("inf"), 1.0]},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:center",
        ),
        (
            lambda descriptor: {**descriptor, "axes": None},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:axes",
        ),
        (
            lambda descriptor: {**descriptor, "axes": [[1.0, 0.0, 0.0]]},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:axes",
        ),
        (
            lambda descriptor: {
                **descriptor,
                "axes": [[1.0, 0.0, 0.0], [0.0, "bad", 0.0], [0.0, 0.0, 1.0]],
            },
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:axes",
        ),
        (
            lambda descriptor: {
                **descriptor,
                "axes": [[1.0, 0.0, 0.0], [0.0, float("nan"), 0.0], [0.0, 0.0, 1.0]],
            },
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:axes",
        ),
        (
            lambda descriptor: {**descriptor, "half_extents": [1.0, 0.25]},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:half_extents",
        ),
        (
            lambda descriptor: {**descriptor, "half_extents": [1.0, "bad", 0.25]},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:half_extents",
        ),
        (
            lambda descriptor: {**descriptor, "half_extents": [1.0, float("inf"), 0.25]},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:half_extents",
        ),
        (
            lambda descriptor: {**descriptor, "half_extents": [1.0, 0.0, 0.25]},
            "newton_shape_runtime_boundary_preflight_descriptor_invalid:half_extents",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_descriptor_drift(
    mutate_descriptor,
    error_label,
):
    payload = _newton_shape_runtime_boundary_preflight_input()
    rows = [json.loads(json.dumps(row)) for row in payload["shape_mapping_rows"]]
    rows[0]["newton_shape_descriptor_dict"] = mutate_descriptor(
        rows[0]["newton_shape_descriptor_dict"]
    )
    payload["shape_mapping_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_boundary_preflight_rejects_source_package_copy(
    cpd_paper_report,
):
    payload = _newton_shape_runtime_boundary_preflight_input()
    source_package = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"][
        "collision_package_generation_rows"
    ][0]["generated_collision_package"]
    payload["source_collision_package_dict"] = json.loads(json.dumps(source_package))

    with pytest.raises(
        ValueError,
        match=("newton_shape_runtime_boundary_preflight_source_package_copy_forbidden"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_boundary_preflight_static_boundary_has_no_runtime_calls():
    helpers = (
        cpd_paper_offline._paper_validate_newton_shape_runtime_boundary_descriptor,
        cpd_paper_offline._paper_newton_shape_runtime_boundary_preflight_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_boundary_preflight_row,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract_payload,
        cpd_paper_offline.build_cpd_paper_offline_report,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "CollisionPackage(",
        "PrimitiveSpec(",
        "FallbackSpec",
        "primitive_collision_compiler.newton",
        "NewtonShapeMapping",
        "map_package_shapes",
        "import newton",
        "from newton",
        "import newton_warp",
        "Newton",
        "run_newton",
        "newton.",
        "check_runtime_admissibility",
        "run_runtime_admissibility",
        "pxr",
        "Usd.Stage",
        "USD",
        "load_first_mesh",
        "inspect_usd_asset",
        "assets.usd_smoke",
        "real_usd_comparison",
        ".simulate(",
        "timeit",
        "perf_counter",
        "benchmark_metric",
        "surface_distance",
        "timing_result",
        "collision_quality_score",
        "run_benchmark",
        "measure_collision_quality",
        "create_shape(",
        "create_box(",
        "Shape(",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_construction_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_construction_contract"]

    assert report["next_required_gate"] == (EXPECTED_CURRENT_REPORT_NEXT_GATE)
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT)
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
    )
    assert payload["newton_shape_runtime_construction_row_count"] == 1
    assert payload["source_newton_shape_runtime_boundary_preflight_row_count"] == 1
    assert payload["constructed_newton_shape_mapping_record_count"] == 1
    assert payload["newton_mapping_record_count"] == 1
    assert payload["newton_mapper_call_count"] == 0
    assert payload["newton_shape_object_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_REMAINING_GAPS


def test_cpd_paper_newton_shape_runtime_construction_payload_schema_is_exact(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_construction_contract"]
    source_row = report["paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"][
        "newton_shape_runtime_boundary_preflight_rows"
    ][0]

    assert set(payload) == NEWTON_SHAPE_RUNTIME_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_shape_mapping_record_construction_contract_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_shape_mapping_record_construction_complete_"
        "newton_shape_runtime_builder_preflight_missing"
    )
    assert payload["artifact_kind"] == (
        "repo_local_newton_shape_mapping_to_dict_not_newton_engine_shape"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_newton_shape_mapping_record_only_"
        "no_newton_engine_shape_no_runtime_no_real_usd_no_benchmark_no_metrics"
    )
    assert payload["runtime_construction_action"] == (
        "construct_one_repo_local_newton_shape_mapping_from_static_descriptor_without_newton_import"
    )
    assert payload["newton_shape_runtime_construction_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "closed_gate": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT),
        "next_newton_shape_runtime_builder_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
        ),
        "source_runtime_boundary_preflight_rows_required": 1,
        "newton_shape_mapping_to_dict_records_required": 1,
        "newton_mapper_call_allowed": False,
        "newton_engine_shape_object_allowed": False,
        "newton_builder_shape_call_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
        ),
        "source_newton_shape_runtime_boundary_preflight_row_id": (
            source_row["newton_shape_runtime_boundary_preflight_row_id"]
        ),
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_descriptor_kind": "newton_shape_descriptor",
        "input_construction_candidate_count": 1,
    }


def test_cpd_paper_newton_shape_runtime_construction_records_one_mapping_row(cpd_paper_report):
    report = cpd_paper_report
    source_row = report["paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"][
        "newton_shape_runtime_boundary_preflight_rows"
    ][0]
    payload = report["paper_mapped_subset_newton_shape_runtime_construction_contract"]
    rows = payload["newton_shape_runtime_construction_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NEWTON_SHAPE_RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS
    assert row["newton_shape_runtime_construction_row_id"] == (
        "newton_shape_runtime_construction__paper_single_box__box"
    )
    assert (
        row["source_newton_shape_runtime_boundary_preflight_row_id"]
        == (source_row["newton_shape_runtime_boundary_preflight_row_id"])
    )
    assert row["source_shape_mapping_row_id"] == (source_row["source_shape_mapping_row_id"])
    assert (
        row["source_newton_shape_mapping_preflight_row_id"]
        == (source_row["source_newton_shape_mapping_preflight_row_id"])
    )
    assert (
        row["source_runtime_admissibility_row_id"]
        == (source_row["source_runtime_admissibility_row_id"])
    )
    assert row["source_package_id"] == source_row["source_package_id"]
    assert row["source_asset_id"] == source_row["source_asset_id"]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["primitive_id"] == ("paper_single_box__oriented_bounding_box__box")
    assert row["target_newton_shape_kind"] == "box"
    assert row["descriptor_kind"] == "newton_shape_descriptor"
    assert row["descriptor_center"] == source_row["descriptor_center"]
    assert row["descriptor_axes"] == source_row["descriptor_axes"]
    assert row["descriptor_half_extents"] == source_row["descriptor_half_extents"]
    assert row["constructed_newton_shape_mapping_status"] == "mapped"
    assert row["constructed_newton_shape_mapping_detail"] == "mapped"
    assert row["mapping_constructor"] == "NewtonShapeMapping"
    assert row["mapping_constructor_input_kind"] == "static_descriptor_fields"
    assert row["runtime_builder_preflight_candidate"] is True
    assert row["constructed_newton_shape_mapping_dict"] == {
        "primitive_id": "paper_single_box__oriented_bounding_box__box",
        "kind": "box",
        "status": "mapped",
        "detail": "mapped",
        "center": source_row["descriptor_center"],
        "axes": source_row["descriptor_axes"],
        "dimensions": {
            "half_extents": source_row["descriptor_half_extents"],
        },
    }
    assert list(_recursive_package_dicts(payload)) == []


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_newton_shape_runtime_construction_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_newton_shape_runtime_construction_contract"]

    assert payload[field_name] is False
    assert payload["newton_shape_runtime_construction_rows"][0][field_name] is False


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS)
def test_cpd_paper_newton_shape_runtime_construction_record_flags_are_narrowly_true(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_newton_shape_runtime_construction_contract"]

    assert payload[field_name] is True
    assert payload["newton_shape_runtime_construction_rows"][0][field_name] is True


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_runtime_construction_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_runtime_construction_input_next_gate_mismatch",
        ),
        (
            "newton_shape_runtime_boundary_preflight_row_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "newton_shape_runtime_boundary_preflight_row_count",
        ),
        (
            "source_shape_mapping_contract_row_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "source_shape_mapping_contract_row_count",
        ),
        (
            "later_newton_shape_runtime_construction_candidate_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "later_newton_shape_runtime_construction_candidate_count",
        ),
        (
            "report_scoped_newton_shape_descriptor_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "report_scoped_newton_shape_descriptor_count",
        ),
        (
            "mapping_attempt_count",
            1,
            "newton_shape_runtime_construction_input_count_mismatch:mapping_attempt_count",
        ),
        (
            "newton_mapping_record_count",
            1,
            "newton_shape_runtime_construction_input_count_mismatch:newton_mapping_record_count",
        ),
        (
            "newton_shape_object_count",
            1,
            "newton_shape_runtime_construction_input_count_mismatch:newton_shape_object_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_runtime_construction_input_count_mismatch:newton_runtime_execution_count",
        ),
        (
            "generated_runtime_primitive_spec_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "generated_runtime_primitive_spec_count",
        ),
        (
            "generated_primitive_spec_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:generated_primitive_spec_count",
        ),
        (
            "generated_collision_package_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "generated_collision_package_count",
        ),
        (
            "runtime_admissibility_check_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "runtime_admissibility_check_count",
        ),
        (
            "offline_static_runtime_admissibility_check_count",
            2,
            "newton_shape_runtime_construction_input_count_mismatch:"
            "offline_static_runtime_admissibility_check_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_construction_input()
    payload[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_input_forbidden_flags(
    field_name,
):
    payload = _newton_shape_runtime_construction_input()
    payload[field_name] = True

    with pytest.raises(
        ValueError,
        match=f"newton_shape_runtime_construction_input_flag_true:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "newton_shape_runtime_construction_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "newton_shape_runtime_construction_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_row_count_drift(
    mutate_rows,
    error_label,
):
    payload = _newton_shape_runtime_construction_input()
    payload["newton_shape_runtime_boundary_preflight_rows"] = mutate_rows(
        payload["newton_shape_runtime_boundary_preflight_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "newton_shape_runtime_boundary_preflight_row_id",
            "wrong_row",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "newton_shape_runtime_boundary_preflight_row_id",
        ),
        (
            "source_shape_mapping_row_id",
            "wrong_mapping_row",
            "newton_shape_runtime_construction_source_row_mismatch:source_shape_mapping_row_id",
        ),
        (
            "source_newton_shape_mapping_preflight_row_id",
            "wrong_preflight_row",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "source_newton_shape_mapping_preflight_row_id",
        ),
        (
            "source_runtime_admissibility_row_id",
            "wrong_runtime_admissibility_row",
            "newton_shape_runtime_construction_source_row_mismatch:"
            "source_runtime_admissibility_row_id",
        ),
        (
            "source_package_id",
            "wrong_package",
            "newton_shape_runtime_construction_source_row_mismatch:source_package_id",
        ),
        (
            "source_asset_id",
            "wrong_asset",
            "newton_shape_runtime_construction_source_row_mismatch:source_asset_id",
        ),
        (
            "fixture_id",
            "wrong_fixture",
            "newton_shape_runtime_construction_source_row_mismatch:fixture_id",
        ),
        (
            "paper_primitive",
            "sphere",
            "newton_shape_runtime_construction_source_row_mismatch:paper_primitive",
        ),
        (
            "primitive_spec_kind",
            "sphere",
            "newton_shape_runtime_construction_source_row_mismatch:primitive_spec_kind",
        ),
        (
            "primitive_id",
            "wrong_primitive",
            "newton_shape_runtime_construction_source_row_mismatch:primitive_id",
        ),
        (
            "target_newton_shape_kind",
            "sphere",
            "newton_shape_runtime_construction_source_row_mismatch:target_newton_shape_kind",
        ),
        (
            "descriptor_kind",
            "wrong_descriptor",
            "newton_shape_runtime_construction_source_row_mismatch:descriptor_kind",
        ),
        (
            "runtime_boundary_preflight_passed",
            False,
            "newton_shape_runtime_construction_source_row_mismatch:"
            "runtime_boundary_preflight_passed",
        ),
        (
            "later_newton_shape_runtime_construction_candidate",
            False,
            "newton_shape_runtime_construction_source_row_mismatch:"
            "later_newton_shape_runtime_construction_candidate",
        ),
        (
            "mapping_attempt_count",
            1,
            "newton_shape_runtime_construction_source_row_mismatch:mapping_attempt_count",
        ),
        (
            "newton_mapping_record_count",
            1,
            "newton_shape_runtime_construction_source_row_mismatch:newton_mapping_record_count",
        ),
        (
            "newton_shape_object_count",
            1,
            "newton_shape_runtime_construction_source_row_mismatch:newton_shape_object_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_runtime_construction_source_row_mismatch:newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_construction_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_boundary_preflight_rows"]
    ]
    rows[0][field_name] = bad_value
    payload["newton_shape_runtime_boundary_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "descriptor_center",
            None,
            "newton_shape_runtime_construction_descriptor_invalid:center",
        ),
        (
            "descriptor_center",
            [0.0, 1.0],
            "newton_shape_runtime_construction_descriptor_invalid:center",
        ),
        (
            "descriptor_center",
            [0.0, "bad", 1.0],
            "newton_shape_runtime_construction_descriptor_invalid:center",
        ),
        (
            "descriptor_center",
            [0.0, float("inf"), 1.0],
            "newton_shape_runtime_construction_descriptor_invalid:center",
        ),
        (
            "descriptor_axes",
            None,
            "newton_shape_runtime_construction_descriptor_invalid:axes",
        ),
        (
            "descriptor_axes",
            [[1.0, 0.0, 0.0]],
            "newton_shape_runtime_construction_descriptor_invalid:axes",
        ),
        (
            "descriptor_axes",
            [[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 1.0]],
            "newton_shape_runtime_construction_descriptor_invalid:axes",
        ),
        (
            "descriptor_axes",
            [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]],
            "newton_shape_runtime_construction_descriptor_invalid:axes",
        ),
        (
            "descriptor_half_extents",
            [1.0, 0.25],
            "newton_shape_runtime_construction_descriptor_invalid:half_extents",
        ),
        (
            "descriptor_half_extents",
            [1.0, "bad", 0.25],
            "newton_shape_runtime_construction_descriptor_invalid:half_extents",
        ),
        (
            "descriptor_half_extents",
            [1.0, 0.0, 0.25],
            "newton_shape_runtime_construction_descriptor_invalid:half_extents",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_construction_rejects_descriptor_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_construction_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_boundary_preflight_rows"]
    ]
    rows[0][field_name] = bad_value
    payload["newton_shape_runtime_boundary_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_construction_rejects_source_package_copy(cpd_paper_report):
    payload = _newton_shape_runtime_construction_input()
    source_package = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"][
        "collision_package_generation_rows"
    ][0]["generated_collision_package"]
    payload["source_collision_package_dict"] = json.loads(json.dumps(source_package))

    with pytest.raises(
        ValueError,
        match="newton_shape_runtime_construction_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_construction_static_boundary_is_record_only():
    helpers = (
        cpd_paper_offline._paper_validate_newton_shape_runtime_construction_descriptor,
        cpd_paper_offline._paper_newton_shape_runtime_construction_source_row,
        cpd_paper_offline._paper_constructed_newton_shape_mapping_dict,
        cpd_paper_offline._paper_newton_shape_runtime_construction_row,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_construction_contract_payload,
        cpd_paper_offline.build_cpd_paper_offline_report,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    assert source.count("NewtonShapeMapping(") == 1
    assert source.count("mapping.to_dict()") == 1
    assert "return mapping.to_dict()" in source
    assert "from primitive_collision_compiler.reports.schema import NewtonShapeMapping" in source

    forbidden_patterns = (
        "CollisionPackage(",
        "PrimitiveSpec(",
        "FallbackSpec",
        "primitive_collision_compiler.newton",
        "map_package_shapes",
        "import newton",
        "from newton",
        "import newton_warp",
        "import warp",
        "from warp",
        "warp.",
        "wp.",
        "builder.add_shape_",
        "builder.add_shape",
        "builder.",
        ".add_shape_",
        ".add_shape(",
        "add_box_shape",
        "add_sphere_shape",
        "add_capsule_shape",
        "add_cylinder_shape",
        "add_cone_shape",
        "add_ellipsoid_shape",
        "CollisionPipeline",
        "collide",
        "finalize",
        "run_newton",
        "newton.",
        "check_runtime_admissibility",
        "run_runtime_admissibility",
        "import pxr",
        "from pxr",
        "pxr",
        "Usd",
        "UsdGeom",
        "UsdPhysics",
        "omni.usd",
        "Usd.Stage",
        "load_first_mesh",
        "inspect_usd_asset",
        "assets.usd_smoke",
        "real_usd_comparison",
        ".simulate(",
        "timeit",
        "perf_counter",
        "benchmark_metric",
        "surface_distance",
        "timing_result",
        "collision_quality_score",
        "run_benchmark",
        "measure_collision_quality",
        "create_shape(",
        "create_box(",
        "Shape(",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_builder_preflight_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"]

    assert report["next_required_gate"] == (EXPECTED_CURRENT_REPORT_NEXT_GATE)
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
    )
    assert payload["newton_shape_runtime_builder_preflight_row_count"] == 1
    assert payload["source_newton_shape_runtime_construction_row_count"] == 1
    assert payload["source_newton_shape_mapping_record_count"] == 1
    assert payload["runtime_builder_preflight_passed"] is True
    assert payload["runtime_builder_preflight_passed_count"] == 1
    assert payload["builder_call_plan_count"] == 1
    assert payload["builder_call_allowed_count"] == 0
    assert payload["later_newton_shape_runtime_builder_candidate_count"] == 1
    assert payload["newton_mapping_record_count"] == 1
    assert payload["newton_mapper_call_count"] == 0
    assert payload["newton_shape_object_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert (
        payload["remaining_gaps"] == EXPECTED_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_builder_preflight_payload_schema_is_exact(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"]
    source_row = report["paper_mapped_subset_newton_shape_runtime_construction_contract"][
        "newton_shape_runtime_construction_rows"
    ][0]

    assert set(payload) == NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_shape_runtime_builder_preflight_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_shape_runtime_builder_preflight_complete_"
        "newton_shape_runtime_builder_construction_contract_missing"
    )
    assert payload["artifact_kind"] == ("offline_static_newton_builder_call_plan_not_builder_call")
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_newton_builder_preflight_only_no_builder_call_"
        "no_engine_shape_no_runtime_no_real_usd_no_benchmark_no_metrics"
    )
    assert payload["runtime_builder_preflight_action"] == (
        "record_one_newton_builder_call_plan_from_repo_local_mapping_dict_"
        "without_builder_call_or_newton_runtime_execution"
    )
    assert payload["newton_shape_runtime_builder_preflight_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT),
        "closed_gate": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT),
        "next_newton_shape_runtime_builder_construction_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
        ),
        "source_runtime_construction_rows_required": 1,
        "builder_call_plans_required": 1,
        "newton_engine_shape_object_allowed": False,
        "newton_builder_shape_call_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
        ),
        "source_newton_shape_runtime_construction_row_id": source_row[
            "newton_shape_runtime_construction_row_id"
        ],
        "source_newton_shape_runtime_boundary_preflight_row_id": source_row[
            "source_newton_shape_runtime_boundary_preflight_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_mapping_constructor": "NewtonShapeMapping",
        "input_runtime_builder_preflight_candidate_count": 1,
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_builder_preflight_row_count": 1,
        "source_newton_shape_runtime_construction_row_count": 1,
        "source_newton_shape_mapping_record_count": 1,
        "runtime_builder_preflight_passed_count": 1,
        "builder_call_plan_count": 1,
        "builder_call_allowed_count": 0,
        "later_newton_shape_runtime_builder_candidate_count": 1,
        "constructed_newton_shape_mapping_record_count": 1,
        "newton_mapping_record_count": 1,
        "newton_mapper_call_count": 0,
        "newton_shape_object_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_runtime_execution_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "target_newton_shape_kind_distribution": {"box": 1},
        "builder_method_distribution": {"add_shape_box": 1},
    }


def test_cpd_paper_newton_shape_runtime_builder_preflight_records_one_builder_plan(
    cpd_paper_report,
):
    report = cpd_paper_report
    source_row = report["paper_mapped_subset_newton_shape_runtime_construction_contract"][
        "newton_shape_runtime_construction_rows"
    ][0]
    payload = report["paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"]
    rows = payload["newton_shape_runtime_builder_preflight_rows"]

    assert len(rows) == 1
    row = rows[0]
    mapping = source_row["constructed_newton_shape_mapping_dict"]
    half_extents = mapping["dimensions"]["half_extents"]
    expected_plan = {
        "method": "add_shape_box",
        "call_signature_fields": ["body", "xform", "hx", "hy", "hz"],
        "body_binding_policy": (
            "static_package_or_probe_uses_body_minus_one_drop_settle_uses_created_body_id"
        ),
        "deferred_xform_policy": ("future_runtime_may_derive_xform_from_center_and_axes"),
        "deferred_translation_inputs": ("mapping_center_only_no_runtime_transform_constructed"),
        "deferred_rotation_inputs": ("mapping_axes_only_no_quat_or_runtime_rotation_constructed"),
        "dimension_arguments": {
            "hx": half_extents[0],
            "hy": half_extents[1],
            "hz": half_extents[2],
        },
    }
    assert set(row) == NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_ROW_REQUIRED_KEYS
    assert row["newton_shape_runtime_builder_preflight_row_id"] == (
        "newton_shape_runtime_builder_preflight__paper_single_box__box"
    )
    assert (
        row["source_newton_shape_runtime_construction_row_id"]
        == (source_row["newton_shape_runtime_construction_row_id"])
    )
    assert (
        row["source_newton_shape_runtime_boundary_preflight_row_id"]
        == (source_row["source_newton_shape_runtime_boundary_preflight_row_id"])
    )
    assert row["source_shape_mapping_row_id"] == (source_row["source_shape_mapping_row_id"])
    assert (
        row["source_newton_shape_mapping_preflight_row_id"]
        == (source_row["source_newton_shape_mapping_preflight_row_id"])
    )
    assert (
        row["source_runtime_admissibility_row_id"]
        == (source_row["source_runtime_admissibility_row_id"])
    )
    assert row["source_package_id"] == source_row["source_package_id"]
    assert row["source_asset_id"] == source_row["source_asset_id"]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["primitive_id"] == ("paper_single_box__oriented_bounding_box__box")
    assert row["target_newton_shape_kind"] == "box"
    assert row["descriptor_kind"] == "newton_shape_descriptor"
    assert row["descriptor_center"] == source_row["descriptor_center"]
    assert row["descriptor_axes"] == source_row["descriptor_axes"]
    assert row["descriptor_half_extents"] == source_row["descriptor_half_extents"]
    assert row["constructed_newton_shape_mapping_dict"] == mapping
    assert row["constructed_newton_shape_mapping_status"] == "mapped"
    assert row["constructed_newton_shape_mapping_detail"] == "mapped"
    assert row["mapping_constructor"] == "NewtonShapeMapping"
    assert row["mapping_constructor_input_kind"] == "static_descriptor_fields"
    assert row["runtime_builder_preflight_passed"] is True
    assert row["builder_call_allowed"] is False
    assert row["builder_candidate_kind"] == "static_shape_builder_call"
    assert row["builder_shape_kind"] == "box"
    assert row["builder_method_name"] == "add_shape_box"
    assert row["call_signature_fields"] == ["body", "xform", "hx", "hy", "hz"]
    assert row["body_binding_policy"] == (
        "static_package_or_probe_uses_body_minus_one_drop_settle_uses_created_body_id"
    )
    assert row["deferred_xform_policy"] == ("future_runtime_may_derive_xform_from_center_and_axes")
    assert row["deferred_translation_inputs"] == (
        "mapping_center_only_no_runtime_transform_constructed"
    )
    assert row["deferred_rotation_inputs"] == (
        "mapping_axes_only_no_quat_or_runtime_rotation_constructed"
    )
    assert (
        row["dimension_source"] == "constructed_newton_shape_mapping_dict.dimensions.half_extents"
    )
    assert row["builder_center"] == mapping["center"]
    assert row["builder_axes"] == mapping["axes"]
    assert row["builder_half_extents"] == half_extents
    assert row["builder_dimension_argument_schema"] == {
        "hx": "half_extents[0]",
        "hy": "half_extents[1]",
        "hz": "half_extents[2]",
    }
    assert row["builder_call_plan"] == expected_plan
    assert row["builder_call_plan_count"] == 1
    assert row["later_newton_shape_runtime_builder_candidate"] is True
    assert row["runtime_builder_construction_contract_candidate"] is True
    assert row["constructed_newton_shape_mapping_record_count"] == 1
    assert row["newton_mapping_record_count"] == 1
    assert row["newton_mapper_call_count"] == 0
    assert row["newton_shape_object_count"] == 0
    assert row["newton_engine_shape_object_count"] == 0
    assert row["newton_builder_shape_call_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    assert list(_recursive_package_dicts(payload)) == []
    json.dumps(row["builder_call_plan"])
    assert _contains_callable(row["builder_call_plan"]) is False
    forbidden_runtime_pose_keys = {
        "builder_xform",
        "runtime_xform",
        "xform_value",
        "transform",
        "runtime_transform",
        "quat",
        "quaternion",
        "rotation_quat",
        "orientation_quaternion",
    }
    assert forbidden_runtime_pose_keys.isdisjoint(set(_recursive_keys(row)))


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_FALSE_FLAGS)
def test_cpd_paper_newton_shape_runtime_builder_preflight_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
    ]

    assert payload[field_name] is False
    assert payload["newton_shape_runtime_builder_preflight_rows"][0][field_name] is False


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS)
def test_cpd_paper_newton_shape_runtime_builder_preflight_record_flags_are_true(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
    ]

    assert payload[field_name] is True
    assert payload["newton_shape_runtime_builder_preflight_rows"][0][field_name] is True


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_runtime_builder_preflight_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_runtime_builder_preflight_input_next_gate_mismatch",
        ),
        (
            "newton_shape_runtime_construction_row_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "newton_shape_runtime_construction_row_count",
        ),
        (
            "source_newton_shape_runtime_boundary_preflight_row_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "source_newton_shape_runtime_boundary_preflight_row_count",
        ),
        (
            "constructed_newton_shape_mapping_record_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "constructed_newton_shape_mapping_record_count",
        ),
        (
            "newton_mapping_record_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "newton_mapping_record_count",
        ),
        (
            "newton_mapper_call_count",
            1,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:newton_mapper_call_count",
        ),
        (
            "newton_shape_object_count",
            1,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:newton_shape_object_count",
        ),
        (
            "newton_engine_shape_object_count",
            1,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "newton_engine_shape_object_count",
        ),
        (
            "newton_builder_shape_call_count",
            1,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "newton_builder_shape_call_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "newton_runtime_execution_count",
        ),
        (
            "generated_runtime_primitive_spec_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "generated_runtime_primitive_spec_count",
        ),
        (
            "generated_primitive_spec_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "generated_primitive_spec_count",
        ),
        (
            "generated_collision_package_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "generated_collision_package_count",
        ),
        (
            "runtime_admissibility_check_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "runtime_admissibility_check_count",
        ),
        (
            "offline_static_runtime_admissibility_check_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "offline_static_runtime_admissibility_check_count",
        ),
        (
            "report_scoped_newton_shape_descriptor_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "report_scoped_newton_shape_descriptor_count",
        ),
        (
            "later_newton_shape_runtime_construction_candidate_count",
            2,
            "newton_shape_runtime_builder_preflight_input_count_mismatch:"
            "later_newton_shape_runtime_construction_candidate_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_builder_preflight_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_builder_preflight_input()
    payload[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_newton_shape_runtime_builder_preflight_rejects_input_flags(
    field_name,
):
    payload = _newton_shape_runtime_builder_preflight_input()
    payload[field_name] = True

    with pytest.raises(
        ValueError,
        match=f"newton_shape_runtime_builder_preflight_input_flag_true:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS)
@pytest.mark.parametrize("scope", ("payload", "row"))
def test_cpd_paper_newton_shape_runtime_builder_preflight_rejects_missing_input_record_flags(
    field_name,
    scope,
):
    payload = _newton_shape_runtime_builder_preflight_input()
    if scope == "payload":
        del payload[field_name]
    else:
        rows = [
            json.loads(json.dumps(row)) for row in payload["newton_shape_runtime_construction_rows"]
        ]
        del rows[0][field_name]
        payload["newton_shape_runtime_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=f"newton_shape_runtime_builder_preflight_input_flag_missing:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS)
@pytest.mark.parametrize("scope", ("payload", "row"))
def test_cpd_paper_newton_shape_runtime_builder_preflight_rejects_false_input_record_flags(
    field_name,
    scope,
):
    payload = _newton_shape_runtime_builder_preflight_input()
    if scope == "payload":
        payload[field_name] = False
    else:
        rows = [
            json.loads(json.dumps(row)) for row in payload["newton_shape_runtime_construction_rows"]
        ]
        rows[0][field_name] = False
        payload["newton_shape_runtime_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=f"newton_shape_runtime_builder_preflight_input_flag_false:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "newton_shape_runtime_builder_preflight_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "newton_shape_runtime_builder_preflight_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_builder_preflight_rejects_row_count_drift(
    mutate_rows,
    error_label,
):
    payload = _newton_shape_runtime_builder_preflight_input()
    payload["newton_shape_runtime_construction_rows"] = mutate_rows(
        payload["newton_shape_runtime_construction_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("newton_shape_runtime_construction_row_id", "wrong_row"),
        ("source_newton_shape_runtime_boundary_preflight_row_id", "wrong_row"),
        ("source_shape_mapping_row_id", "wrong_mapping_row"),
        ("source_newton_shape_mapping_preflight_row_id", "wrong_preflight_row"),
        ("source_runtime_admissibility_row_id", "wrong_admissibility_row"),
        ("source_package_id", "wrong_package"),
        ("source_asset_id", "wrong_asset"),
        ("fixture_id", "wrong_fixture"),
        ("paper_primitive", "sphere"),
        ("primitive_spec_kind", "sphere"),
        ("primitive_id", "wrong_primitive"),
        ("target_newton_shape_kind", "sphere"),
        ("descriptor_kind", "wrong_descriptor"),
        ("mapping_constructor", "wrong_constructor"),
        ("mapping_constructor_input_kind", "wrong_input_kind"),
        ("runtime_builder_preflight_candidate", False),
        ("newton_builder_shape_call_count", 1),
        ("newton_engine_shape_object_count", 1),
        ("newton_runtime_execution_count", 1),
    ],
)
def test_cpd_paper_newton_shape_runtime_builder_preflight_rejects_source_row_drift(
    field_name,
    bad_value,
):
    payload = _newton_shape_runtime_builder_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in payload["newton_shape_runtime_construction_rows"]
    ]
    rows[0][field_name] = bad_value
    payload["newton_shape_runtime_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(f"newton_shape_runtime_builder_preflight_source_row_mismatch:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("mutate_mapping", "error_label"),
    [
        (
            lambda mapping: None,
            "newton_shape_runtime_builder_preflight_mapping_invalid:mapping",
        ),
        (
            lambda mapping: {key: value for key, value in mapping.items() if key != "axes"},
            "newton_shape_runtime_builder_preflight_mapping_key_mismatch",
        ),
        (
            lambda mapping: {**mapping, "extra": True},
            "newton_shape_runtime_builder_preflight_mapping_key_mismatch",
        ),
        (
            lambda mapping: {**mapping, "dimensions": {}},
            "newton_shape_runtime_builder_preflight_mapping_dimensions_key_mismatch",
        ),
        (
            lambda mapping: {
                **mapping,
                "dimensions": {
                    **mapping["dimensions"],
                    "extra": True,
                },
            },
            "newton_shape_runtime_builder_preflight_mapping_dimensions_key_mismatch",
        ),
        (
            lambda mapping: {**mapping, "primitive_id": "wrong_primitive"},
            "newton_shape_runtime_builder_preflight_mapping_mismatch:primitive_id",
        ),
        (
            lambda mapping: {**mapping, "kind": "sphere"},
            "newton_shape_runtime_builder_preflight_mapping_mismatch:kind",
        ),
        (
            lambda mapping: {**mapping, "status": "mapping_gap"},
            "newton_shape_runtime_builder_preflight_mapping_mismatch:status",
        ),
        (
            lambda mapping: {**mapping, "detail": "gap"},
            "newton_shape_runtime_builder_preflight_mapping_mismatch:detail",
        ),
        (
            lambda mapping: {**mapping, "center": [1.0, 0.0, 0.0]},
            "newton_shape_runtime_builder_preflight_mapping_mismatch:center",
        ),
        (
            lambda mapping: {
                **mapping,
                "axes": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]],
            },
            "newton_shape_runtime_builder_preflight_mapping_mismatch:axes",
        ),
        (
            lambda mapping: {
                **mapping,
                "dimensions": {"half_extents": [0.1, 0.2, 0.3]},
            },
            "newton_shape_runtime_builder_preflight_mapping_mismatch:half_extents",
        ),
        (
            lambda mapping: {**mapping, "center": [0.0, "bad", 0.0]},
            "newton_shape_runtime_builder_preflight_mapping_invalid:center",
        ),
        (
            lambda mapping: {
                **mapping,
                "axes": [[1.0, 0.0, 0.0], [0.0, "bad", 0.0], [0.0, 0.0, 1.0]],
            },
            "newton_shape_runtime_builder_preflight_mapping_invalid:axes",
        ),
        (
            lambda mapping: {
                **mapping,
                "dimensions": {"half_extents": [1.0, 0.0, 0.25]},
            },
            "newton_shape_runtime_builder_preflight_mapping_invalid:half_extents",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_builder_preflight_rejects_mapping_drift(
    mutate_mapping,
    error_label,
):
    payload = _newton_shape_runtime_builder_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in payload["newton_shape_runtime_construction_rows"]
    ]
    rows[0]["constructed_newton_shape_mapping_dict"] = mutate_mapping(
        rows[0]["constructed_newton_shape_mapping_dict"]
    )
    payload["newton_shape_runtime_construction_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_builder_preflight_static_boundary_is_plan_only():
    helpers = (
        cpd_paper_offline._paper_newton_shape_runtime_builder_preflight_source_row,
        cpd_paper_offline._paper_validate_runtime_builder_preflight_input_true_flags,
        cpd_paper_offline._paper_validate_newton_shape_runtime_builder_preflight_mapping,
        cpd_paper_offline._paper_newton_shape_runtime_builder_call_plan,
        cpd_paper_offline._paper_newton_shape_runtime_builder_preflight_row,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_preflight_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        "primitive_collision_compiler.newton",
        "import newton",
        "from newton",
        "import warp",
        "from warp",
        "import newton_warp",
        "newton_warp",
        "importlib",
        "__import__",
        "getattr(",
        "callable(",
        "eval(",
        "exec(",
        "newton.ModelBuilder",
        "ModelBuilder",
        "CollisionPipeline",
        "add_shape_",
        "builder.",
        "model_builder.",
        "finalize",
        "pipeline.collide",
        "wp.transform",
        "wp.quat",
        "warp.transform",
        "warp.quat",
        "transformf",
        "quat_from",
        "CollisionPackage(",
        "PrimitiveSpec(",
        "load_first_mesh",
        "inspect_usd_asset",
        "real_usd_comparison",
        "timeit",
        "perf_counter",
        "benchmark_metric",
        "collision_quality_score",
        "run_benchmark",
        "measure_collision_quality",
    )
    for pattern in forbidden_patterns:
        assert pattern not in source


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_builder_construction_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_builder_construction_contract"]

    assert report["next_required_gate"] == (EXPECTED_CURRENT_REPORT_NEXT_GATE)
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["newton_shape_runtime_builder_construction_row_count"] == 1
    assert payload["source_newton_shape_runtime_builder_preflight_row_count"] == 1
    assert payload["recording_builder_shape_call_count"] == 1
    assert payload["recorded_builder_call_count"] == 1
    assert payload["repo_local_static_shape_helper_call_count"] == 1
    assert payload["real_newton_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert (
        payload["remaining_gaps"]
        == EXPECTED_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_builder_construction_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_builder_construction_contract"]
    preflight = report["paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"]
    source_row = preflight["newton_shape_runtime_builder_preflight_rows"][0]

    assert set(payload) == NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_repo_local_recording_builder_construction_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "repo_local_recording_builder_construction_complete_"
        "engine_builder_boundary_preflight_contract_missing"
    )
    assert payload["artifact_kind"] == ("repo_local_recording_builder_call_not_newton_engine_shape")
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_repo_local_recording_builder_only_"
        "no_real_newton_import_no_engine_shape_no_model_finalize_no_runtime"
    )
    assert payload["runtime_builder_construction_action"] == (
        "call_repo_local_static_shape_helper_with_recording_builder_and_fake_wp"
    )
    assert payload["newton_shape_runtime_builder_construction_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT
        ),
        "closed_gate": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT),
        "next_engine_builder_boundary_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "source_builder_preflight_rows_required": 1,
        "repo_local_recording_builder_calls_required": 1,
        "real_newton_import_allowed": False,
        "newton_model_builder_allowed": False,
        "newton_engine_shape_object_allowed": False,
        "newton_builder_shape_call_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
        ),
        "source_newton_shape_runtime_builder_preflight_row_id": source_row[
            "newton_shape_runtime_builder_preflight_row_id"
        ],
        "source_newton_shape_runtime_construction_row_id": source_row[
            "source_newton_shape_runtime_construction_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_builder_method_name": "add_shape_box",
        "input_builder_call_plan_count": 1,
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_builder_construction_row_count": 1,
        "source_newton_shape_runtime_builder_preflight_row_count": 1,
        "recording_builder_shape_call_count": 1,
        "recorded_builder_call_count": 1,
        "repo_local_static_shape_helper_call_count": 1,
        "real_newton_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_model_finalized_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_runtime_execution_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "target_newton_shape_kind_distribution": {"box": 1},
        "builder_method_distribution": {"add_shape_box": 1},
    }


def test_cpd_paper_newton_shape_runtime_builder_construction_records_fake_builder_call(
    cpd_paper_report,
):
    report = cpd_paper_report
    preflight_row = report["paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"][
        "newton_shape_runtime_builder_preflight_rows"
    ][0]
    payload = report["paper_mapped_subset_newton_shape_runtime_builder_construction_contract"]
    rows = payload["newton_shape_runtime_builder_construction_rows"]

    assert len(rows) == 1
    row = rows[0]
    mapping = preflight_row["constructed_newton_shape_mapping_dict"]
    expected_call = _expected_builder_construction_recorded_call(mapping)
    assert set(row) == NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_ROW_REQUIRED_KEYS
    assert row["newton_shape_runtime_builder_construction_row_id"] == (
        "newton_shape_runtime_builder_construction__paper_single_box__box"
    )
    assert (
        row["source_newton_shape_runtime_builder_preflight_row_id"]
        == (preflight_row["newton_shape_runtime_builder_preflight_row_id"])
    )
    assert (
        row["source_newton_shape_runtime_construction_row_id"]
        == (preflight_row["source_newton_shape_runtime_construction_row_id"])
    )
    assert (
        row["source_newton_shape_runtime_boundary_preflight_row_id"]
        == (preflight_row["source_newton_shape_runtime_boundary_preflight_row_id"])
    )
    assert row["source_shape_mapping_row_id"] == (preflight_row["source_shape_mapping_row_id"])
    assert row["source_package_id"] == preflight_row["source_package_id"]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["primitive_id"] == ("paper_single_box__oriented_bounding_box__box")
    assert row["target_newton_shape_kind"] == "box"
    assert row["constructed_newton_shape_mapping_dict"] == mapping
    assert row["builder_call_plan"] == preflight_row["builder_call_plan"]
    assert row["builder_method_name"] == "add_shape_box"
    assert row["builder_body_argument"] == -1
    assert row["builder_dimension_arguments"] == {
        "hx": expected_call["hx"],
        "hy": expected_call["hy"],
        "hz": expected_call["hz"],
    }
    assert row["builder_xform_descriptor"] == expected_call["xform"]
    assert row["repo_local_static_shape_helper"] == "_add_static_shape"
    assert row["repo_local_static_shape_helper_called"] is True
    assert row["recording_builder_kind"] == (
        "repo_local_recording_builder_not_newton_model_builder"
    )
    assert row["recording_builder_shape_call_count"] == 1
    assert row["recorded_builder_method_name"] == "add_shape_box"
    assert row["recorded_builder_call"] == expected_call
    assert row["recorded_builder_call_count"] == 1
    assert row["fake_wp_call_summary"] == {
        "vec3_call_count": 4,
        "matrix_from_cols_call_count": 1,
        "quat_from_matrix_call_count": 1,
        "transform_call_count": 1,
    }
    assert row["real_newton_import_count"] == 0
    assert row["newton_model_builder_instantiated_count"] == 0
    assert row["newton_model_finalized_count"] == 0
    assert row["newton_engine_shape_object_count"] == 0
    assert row["newton_builder_shape_call_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    assert list(_recursive_package_dicts(payload)) == []
    json.dumps(row["recorded_builder_call"])
    assert _contains_callable(row["recorded_builder_call"]) is False


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_newton_shape_runtime_builder_construction_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
    ]

    assert payload[field_name] is False
    assert payload["newton_shape_runtime_builder_construction_rows"][0][field_name] is False


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_TRUE_FLAGS)
def test_cpd_paper_newton_shape_runtime_builder_construction_record_flags_are_true(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
    ]

    assert payload[field_name] is True
    assert payload["newton_shape_runtime_builder_construction_rows"][0][field_name] is True


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_runtime_builder_construction_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_runtime_builder_construction_input_next_gate_mismatch",
        ),
        (
            "newton_shape_runtime_builder_preflight_row_count",
            2,
            "newton_shape_runtime_builder_construction_input_count_mismatch:"
            "newton_shape_runtime_builder_preflight_row_count",
        ),
        (
            "builder_call_plan_count",
            2,
            "newton_shape_runtime_builder_construction_input_count_mismatch:"
            "builder_call_plan_count",
        ),
        (
            "builder_call_allowed_count",
            1,
            "newton_shape_runtime_builder_construction_input_count_mismatch:"
            "builder_call_allowed_count",
        ),
        (
            "newton_builder_shape_call_count",
            1,
            "newton_shape_runtime_builder_construction_input_count_mismatch:"
            "newton_builder_shape_call_count",
        ),
        (
            "newton_engine_shape_object_count",
            1,
            "newton_shape_runtime_builder_construction_input_count_mismatch:"
            "newton_engine_shape_object_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_runtime_builder_construction_input_count_mismatch:"
            "newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_builder_construction_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_builder_construction_input()
    payload[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_FALSE_FLAGS)
@pytest.mark.parametrize("scope", ("payload", "row"))
def test_cpd_paper_newton_shape_runtime_builder_construction_rejects_input_flags(
    field_name,
    scope,
):
    payload = _newton_shape_runtime_builder_construction_input()
    if scope == "payload":
        payload[field_name] = True
    else:
        rows = [
            json.loads(json.dumps(row))
            for row in payload["newton_shape_runtime_builder_preflight_rows"]
        ]
        rows[0][field_name] = True
        payload["newton_shape_runtime_builder_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match=f"newton_shape_runtime_builder_construction_input_flag_true:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS)
@pytest.mark.parametrize("scope", ("payload", "row"))
def test_cpd_paper_newton_shape_runtime_builder_construction_rejects_missing_input_record_flags(
    field_name,
    scope,
):
    payload = _newton_shape_runtime_builder_construction_input()
    if scope == "payload":
        del payload[field_name]
    else:
        rows = [
            json.loads(json.dumps(row))
            for row in payload["newton_shape_runtime_builder_preflight_rows"]
        ]
        del rows[0][field_name]
        payload["newton_shape_runtime_builder_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match=f"newton_shape_runtime_builder_construction_input_flag_missing:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS)
@pytest.mark.parametrize("scope", ("payload", "row"))
def test_cpd_paper_newton_shape_runtime_builder_construction_rejects_false_input_record_flags(
    field_name,
    scope,
):
    payload = _newton_shape_runtime_builder_construction_input()
    if scope == "payload":
        payload[field_name] = False
    else:
        rows = [
            json.loads(json.dumps(row))
            for row in payload["newton_shape_runtime_builder_preflight_rows"]
        ]
        rows[0][field_name] = False
        payload["newton_shape_runtime_builder_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match=f"newton_shape_runtime_builder_construction_input_flag_false:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "newton_shape_runtime_builder_construction_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "newton_shape_runtime_builder_construction_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_builder_construction_rejects_row_count_drift(
    mutate_rows,
    error_label,
):
    payload = _newton_shape_runtime_builder_construction_input()
    payload["newton_shape_runtime_builder_preflight_rows"] = mutate_rows(
        payload["newton_shape_runtime_builder_preflight_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("newton_shape_runtime_builder_preflight_row_id", "wrong_row"),
        ("source_newton_shape_runtime_construction_row_id", "wrong_row"),
        ("source_shape_mapping_row_id", "wrong_mapping_row"),
        ("source_package_id", "wrong_package"),
        ("fixture_id", "wrong_fixture"),
        ("paper_primitive", "sphere"),
        ("primitive_spec_kind", "sphere"),
        ("primitive_id", "wrong_primitive"),
        ("target_newton_shape_kind", "sphere"),
        ("builder_method_name", "add_shape_sphere"),
        ("builder_call_plan_count", 2),
        ("builder_call_allowed", True),
        ("newton_builder_shape_call_count", 1),
        ("newton_engine_shape_object_count", 1),
        ("newton_runtime_execution_count", 1),
    ],
)
def test_cpd_paper_newton_shape_runtime_builder_construction_rejects_source_row_drift(
    field_name,
    bad_value,
):
    payload = _newton_shape_runtime_builder_construction_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_builder_preflight_rows"]
    ]
    rows[0][field_name] = bad_value
    payload["newton_shape_runtime_builder_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(f"newton_shape_runtime_builder_construction_source_row_mismatch:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("mutate_plan", "error_label"),
    [
        (
            lambda plan: {**plan, "method": "add_shape_sphere"},
            "newton_shape_runtime_builder_construction_call_plan_mismatch:method",
        ),
        (
            lambda plan: {**plan, "call_signature_fields": ["body", "hx"]},
            "newton_shape_runtime_builder_construction_call_plan_mismatch:call_signature_fields",
        ),
        (
            lambda plan: {
                **plan,
                "dimension_arguments": {"hx": 1.0, "hy": 0.5, "hz": 0.3},
            },
            "newton_shape_runtime_builder_construction_call_plan_mismatch:dimension_arguments",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_builder_construction_rejects_call_plan_drift(
    mutate_plan,
    error_label,
):
    payload = _newton_shape_runtime_builder_construction_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_builder_preflight_rows"]
    ]
    rows[0]["builder_call_plan"] = mutate_plan(rows[0]["builder_call_plan"])
    payload["newton_shape_runtime_builder_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("mutate_mapping", "error_label"),
    [
        (
            lambda mapping: {**mapping, "center": [1.0, 0.0, 0.0]},
            "newton_shape_runtime_builder_construction_mapping_mismatch:center",
        ),
        (
            lambda mapping: {
                **mapping,
                "axes": [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]],
            },
            "newton_shape_runtime_builder_construction_mapping_mismatch:axes",
        ),
        (
            lambda mapping: {
                **mapping,
                "dimensions": {"half_extents": [1.0, 0.5, 0.3]},
            },
            "newton_shape_runtime_builder_construction_mapping_mismatch:half_extents",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_builder_construction_rejects_mapping_drift(
    mutate_mapping,
    error_label,
):
    payload = _newton_shape_runtime_builder_construction_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_builder_preflight_rows"]
    ]
    rows[0]["constructed_newton_shape_mapping_dict"] = mutate_mapping(
        rows[0]["constructed_newton_shape_mapping_dict"]
    )
    payload["newton_shape_runtime_builder_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_builder_construction_static_boundary_uses_recording_builder_only():
    helpers = (
        cpd_paper_offline._PaperFakeWarp,
        cpd_paper_offline._PaperRecordingNewtonBuilder,
        cpd_paper_offline._paper_newton_shape_runtime_builder_construction_source_row,
        cpd_paper_offline._paper_construct_recording_builder_shape_call,
        cpd_paper_offline._paper_newton_shape_runtime_builder_construction_row,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_builder_construction_contract_payload,
        newton_diagnostics._add_static_shape,
        newton_diagnostics._shape_quat,
        newton_diagnostics._axis_shape_axes,
        newton_diagnostics._wp_vec3,
        newton_diagnostics._normalize,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        'importlib.import_module("newton")',
        'importlib.import_module("warp")',
        "import newton",
        "from newton",
        "import warp",
        "from warp",
        "newton.ModelBuilder",
        "ModelBuilder(",
        "CollisionPipeline",
        ".finalize(",
        "pipeline.collide",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
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
    forbidden_call_attrs = {
        "finalize",
        "collide",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in forbidden_call_attrs
