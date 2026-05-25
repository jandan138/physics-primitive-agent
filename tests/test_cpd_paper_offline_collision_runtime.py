import pytest

from tests.cpd_paper_offline_shared import *

pytestmark = pytest.mark.paper_offline


def test_cpd_paper_records_mapped_subset_collision_package_generation_preflight_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_collision_package_generation_preflight_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert payload["package_generation_preflight_row_count"] == 1
    assert payload["later_collision_package_generation_candidate_count"] == 1
    assert payload["package_generation_allowed_in_current_gate"] is False
    assert payload["generated_runtime_primitive_spec_count"] == 1
    assert payload["generated_primitive_spec_count"] == 1
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert (
        payload["remaining_gaps"] == EXPECTED_COLLISION_PACKAGE_GENERATION_PREFLIGHT_REMAINING_GAPS
    )


def test_cpd_paper_collision_package_generation_preflight_payload_schema_is_exact(cpd_paper_report):
    payload = cpd_paper_report[
        "paper_mapped_subset_collision_package_generation_preflight_contract"
    ]
    source_row = cpd_paper_report[
        "paper_mapped_subset_primitivespec_runtime_construction_contract"
    ]["runtime_construction_rows"][0]

    assert set(payload) == COLLISION_PACKAGE_GENERATION_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == ("collision_package_generation_preflight_not_package")
    assert payload["implementation_boundary"] == (
        "single_synthetic_primitivespec_dict_package_candidate_only_"
        "no_collision_package_no_newton_no_real_usd_no_benchmark"
    )
    assert payload["package_generation_preflight_action"] == (
        "record_one_later_collision_package_generation_candidate"
    )
    assert payload["package_generation_preflight_requirements"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT),
        "package_generation_preflight_gate_closed": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        ),
        "next_collision_package_generation_gate_required": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_primitive_spec_kind_required": "box",
        "later_collision_package_generation_candidates_required": 1,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    }
    assert payload["package_generation_preflight_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT),
        "package_generation_preflight_gate_closed": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        ),
        "next_collision_package_generation_gate_required": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
        ),
        "package_generation_preflight_rows_required": 1,
        "later_collision_package_generation_candidates_required": 1,
        "generated_collision_packages_required": 0,
        "runtime_admissibility_checks_required": 0,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        ),
        "input_runtime_construction_row_count": 1,
        "input_constructed_runtime_primitivespec_count": 1,
        "input_generated_runtime_primitive_spec_count": 1,
        "input_generated_collision_package_count": 0,
        "source_row_id": source_row["runtime_construction_row_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_spec_kind": "box",
    }
    assert payload["coverage_summary"] == {
        "package_generation_preflight_row_count": 1,
        "later_collision_package_generation_candidate_record_count": 1,
        "package_generation_allowed_record_count": 0,
        "generated_collision_package_record_count": 0,
        "runtime_admissibility_check_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "candidate_package_primitive_kind_distribution": {"box": 1},
    }
    for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS:
        assert payload[flag] is False


def test_cpd_paper_collision_package_generation_preflight_records_one_lineage_row(cpd_paper_report):
    report = cpd_paper_report
    source_row = report["paper_mapped_subset_primitivespec_runtime_construction_contract"][
        "runtime_construction_rows"
    ][0]
    payload = report["paper_mapped_subset_collision_package_generation_preflight_contract"]
    rows = payload["package_generation_preflight_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == COLLISION_PACKAGE_GENERATION_PREFLIGHT_ROW_REQUIRED_KEYS
    assert row["package_generation_preflight_row_id"] == (
        "collision_package_generation_preflight__paper_single_box__box"
    )
    assert row["source_runtime_construction_row_id"] == (source_row["runtime_construction_row_id"])
    assert (
        row["source_runtime_boundary_preflight_row_id"]
        == (source_row["source_runtime_boundary_preflight_row_id"])
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
    assert row["generated_primitive_spec"] == source_row["generated_primitive_spec"]
    assert row["constructed_primitivespec_dict"] == (source_row["constructed_primitivespec_dict"])
    assert row["candidate_primitivespec_dict"] == source_row["generated_primitive_spec"]
    assert row["candidate_primitivespec_dict"] == (source_row["constructed_primitivespec_dict"])
    assert row["candidate_package_primitive_kind"] == "box"
    assert row["candidate_package_scope"] == "single_primitivespec_dict_candidate_only"
    assert row["later_collision_package_generation_candidate"] is True
    assert row["package_generation_allowed_in_current_gate"] is False
    assert row["required_later_gate"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert row["preflight_decision"] == (
        "later_collision_package_generation_contract_may_be_proposed"
    )
    assert row["preflight_reason"] == (
        "runtime_primitivespec_dict_available_but_current_gate_is_preflight_only"
    )
    assert row["collision_package_generated"] is False
    assert row["generated_collision_package"] is None
    assert row["runtime_admissibility_checked"] is False
    for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS:
        assert payload[flag] is False
        assert row[flag] is False


def test_cpd_paper_collision_package_generation_preflight_stays_package_newton_and_metric_free(
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_collision_package_generation_preflight_contract"
    ]

    json.dumps(payload, allow_nan=False, sort_keys=True)
    forbidden_tokens = {
        "CollisionPackage(",
        "FallbackSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "surface_distance",
        "timing_result",
        "collision_quality_score",
    }
    assert forbidden_tokens.isdisjoint(set(_recursive_key_value_strings(payload)))
    assert payload["generated_runtime_primitive_spec_count"] == 1
    assert payload["generated_primitive_spec_count"] == 1
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    for row in payload["package_generation_preflight_rows"]:
        assert isinstance(row["candidate_primitivespec_dict"], dict)
        assert row["generated_collision_package"] is None
        for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_collision_package_generation_preflight_static_boundaries():
    source = Path(cpd_paper_offline.__file__).read_text(encoding="utf-8")
    preflight_block = source[
        source.index("_COLLISION_PACKAGE_GENERATION_PREFLIGHT_PAYLOAD_FALSE_FLAGS") : source.index(
            "_COLLISION_PACKAGE_GENERATION_CONTRACT_PAYLOAD_TRUE_FLAGS"
        )
    ]

    forbidden_patterns = [
        "CollisionPackage",
        "FallbackSpec",
        "PrimitiveSpec(",
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
        "check_runtime_admissibility",
        "run_runtime_admissibility",
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
        assert pattern not in preflight_block


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "collision_package_generation_preflight_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "collision_package_generation_preflight_input_next_gate_mismatch",
        ),
        (
            "package_generation_allowed",
            True,
            (
                "collision_package_generation_preflight_input_trigger_flag_true:"
                "package_generation_allowed"
            ),
        ),
        (
            "newton_runtime_triggered",
            True,
            (
                "collision_package_generation_preflight_input_trigger_flag_true:"
                "newton_runtime_triggered"
            ),
        ),
    ],
)
def test_cpd_paper_collision_package_generation_preflight_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    runtime_construction = _collision_package_generation_preflight_input()
    runtime_construction[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


@pytest.mark.parametrize("field_name", RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_collision_package_generation_preflight_rejects_missing_payload_false_flags(
    field_name,
):
    runtime_construction = _collision_package_generation_preflight_input()
    del runtime_construction[field_name]

    with pytest.raises(
        ValueError,
        match=(f"collision_package_generation_preflight_input_trigger_flag_missing:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "runtime_construction_row_count",
            2,
            "collision_package_generation_preflight_input_count_mismatch:runtime_construction_row_count",
        ),
        (
            "constructed_runtime_primitivespec_count",
            0,
            "collision_package_generation_preflight_input_count_mismatch:constructed_runtime_primitivespec_count",
        ),
        (
            "generated_runtime_primitive_spec_count",
            0,
            "collision_package_generation_preflight_input_count_mismatch:generated_runtime_primitive_spec_count",
        ),
        (
            "generated_collision_package_count",
            1,
            "collision_package_generation_preflight_input_count_mismatch:generated_collision_package_count",
        ),
        (
            "runtime_admissibility_check_count",
            1,
            "collision_package_generation_preflight_input_count_mismatch:runtime_admissibility_check_count",
        ),
    ],
)
def test_cpd_paper_collision_package_generation_preflight_rejects_input_count_drift(
    field_name,
    bad_value,
    error_label,
):
    runtime_construction = _collision_package_generation_preflight_input()
    runtime_construction[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "collision_package_generation_preflight_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "collision_package_generation_preflight_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_collision_package_generation_preflight_rejects_row_count_mismatch(
    mutate_rows,
    error_label,
):
    runtime_construction = _collision_package_generation_preflight_input()
    runtime_construction["runtime_construction_rows"] = mutate_rows(
        runtime_construction["runtime_construction_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "fixture_id",
            "paper_two_boxes",
            "collision_package_generation_preflight_source_kind_mismatch",
        ),
        (
            "kind",
            "sphere",
            "collision_package_generation_preflight_source_kind_mismatch",
        ),
        (
            "runtime_instance_generated",
            False,
            "collision_package_generation_preflight_runtime_primitivespec_missing",
        ),
        (
            "runtime_primitivespec_construction_triggered",
            False,
            "collision_package_generation_preflight_runtime_primitivespec_missing",
        ),
        (
            "generated_primitive_spec",
            None,
            "collision_package_generation_preflight_runtime_primitivespec_missing",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "collision_package_generation_preflight_primitivespec_dict_mismatch",
        ),
        (
            "collision_package_generated",
            True,
            "collision_package_generation_preflight_input_trigger_flag_true:collision_package_generated",
        ),
        (
            "runtime_admissibility_checked",
            True,
            "collision_package_generation_preflight_input_trigger_flag_true:runtime_admissibility_checked",
        ),
        (
            "package_generation_allowed",
            True,
            "collision_package_generation_preflight_input_trigger_flag_true:package_generation_allowed",
        ),
    ],
)
def test_cpd_paper_collision_package_generation_preflight_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    runtime_construction = _collision_package_generation_preflight_input()
    rows = [dict(row) for row in runtime_construction["runtime_construction_rows"]]
    rows[0][field_name] = bad_value
    runtime_construction["runtime_construction_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


@pytest.mark.parametrize(
    ("mutate_spec", "error_label"),
    [
        (
            lambda source: {"kind": "box"},
            "collision_package_generation_preflight_primitivespec_dict_schema_mismatch",
        ),
        (
            lambda source: {**source, "kind": "sphere"},
            "collision_package_generation_preflight_primitivespec_dict_mismatch:kind",
        ),
    ],
)
def test_cpd_paper_collision_package_generation_preflight_rejects_lockstep_primitivespec_dict_drift(
    mutate_spec,
    error_label,
):
    runtime_construction = _collision_package_generation_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in runtime_construction["runtime_construction_rows"]
    ]
    bad_spec = mutate_spec(rows[0]["generated_primitive_spec"])
    rows[0]["generated_primitive_spec"] = bad_spec
    rows[0]["constructed_primitivespec_dict"] = bad_spec
    runtime_construction["runtime_construction_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


def test_cpd_paper_collision_package_generation_preflight_rejects_coherent_canonical_payload_drift():
    runtime_construction = _collision_package_generation_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in runtime_construction["runtime_construction_rows"]
    ]
    source_payload = rows[0]["loaded_primitivespec_payload"]
    runtime_payload = rows[0]["generated_primitive_spec"]
    drifted_source_payload = {**source_payload, "center": [1.25, 0.5, 0.25]}
    drifted_runtime_payload = {**runtime_payload, "center": [1.25, 0.5, 0.25]}
    rows[0]["loaded_primitivespec_payload"] = drifted_source_payload
    rows[0]["canonical_primitivespec_json"] = json.dumps(
        drifted_source_payload,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    rows[0]["generated_primitive_spec"] = drifted_runtime_payload
    rows[0]["constructed_primitivespec_dict"] = drifted_runtime_payload
    runtime_construction["runtime_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "collision_package_generation_preflight_anchored_source_row_mismatch:"
            "loaded_primitivespec_payload"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


def test_cpd_paper_collision_package_generation_preflight_rejects_missing_source_row_lineage_key():
    runtime_construction = _collision_package_generation_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in runtime_construction["runtime_construction_rows"]
    ]
    del rows[0]["runtime_construction_row_id"]
    runtime_construction["runtime_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "collision_package_generation_preflight_source_row_schema_mismatch:"
            "runtime_construction_row_id"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


def test_cpd_paper_collision_package_generation_preflight_rejects_drifted_source_row_lineage_value():
    runtime_construction = _collision_package_generation_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in runtime_construction["runtime_construction_rows"]
    ]
    rows[0]["source_candidate_matrix_row_id"] = "candidate_matrix__wrong_source"
    runtime_construction["runtime_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "collision_package_generation_preflight_anchored_source_row_mismatch:"
            "source_candidate_matrix_row_id"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


@pytest.mark.parametrize("field_name", RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_collision_package_generation_preflight_rejects_missing_source_row_false_flags(
    field_name,
):
    runtime_construction = _collision_package_generation_preflight_input()
    rows = [dict(row) for row in runtime_construction["runtime_construction_rows"]]
    del rows[0][field_name]
    runtime_construction["runtime_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(f"collision_package_generation_preflight_input_trigger_flag_missing:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_preflight_contract_payload(
            runtime_construction
        )


def test_cpd_paper_records_mapped_subset_collision_package_generation_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_collision_package_generation_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["generated_collision_package_count"] == 1
    assert report["runtime_admissibility_check_count"] == 1
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT)
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
    )
    assert payload["collision_package_generation_row_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 1
    assert payload["generated_primitive_spec_count"] == 1
    assert payload["generated_collision_package_count"] == 1
    assert payload["runtime_admissibility_check_count"] == 0
    assert (
        payload["remaining_gaps"] == EXPECTED_COLLISION_PACKAGE_GENERATION_CONTRACT_REMAINING_GAPS
    )


def test_cpd_paper_collision_package_generation_contract_payload_schema_is_exact(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_collision_package_generation_contract"]
    preflight_row = report["paper_mapped_subset_collision_package_generation_preflight_contract"][
        "package_generation_preflight_rows"
    ][0]

    assert set(payload) == COLLISION_PACKAGE_GENERATION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["paper_faithful_offline_supported"] is False
    assert payload["artifact_kind"] == ("single_fixture_offline_collision_package_to_dict_artifact")
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_package_dict_only_no_runtime_admissibility_"
        "no_newton_no_real_usd_no_benchmark"
    )
    assert payload["package_generation_action"] == (
        "construct_one_report_scoped_collisionpackage_to_dict_artifact"
    )
    assert payload["package_generation_requirements"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        ),
        "package_generation_gate_closed": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
        ),
        "next_runtime_admissibility_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_primitive_spec_kind_required": "box",
        "generated_collision_packages_required": 1,
        "runtime_admissibility_checks_required": 0,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    }
    assert payload["package_generation_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT
        ),
        "package_generation_gate_closed": (
            EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
        ),
        "next_runtime_admissibility_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
        ),
        "collision_package_generation_rows_required": 1,
        "generated_collision_packages_required": 1,
        "runtime_admissibility_checks_required": 0,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT),
        "input_next_required_gate": (EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT),
        "input_package_generation_preflight_row_count": 1,
        "input_later_collision_package_generation_candidate_count": 1,
        "input_generated_collision_package_count": 0,
        "source_row_id": preflight_row["package_generation_preflight_row_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_spec_kind": "box",
    }
    assert payload["coverage_summary"] == {
        "collision_package_generation_row_count": 1,
        "generated_collision_package_record_count": 1,
        "runtime_admissibility_check_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "primitive_subset_distribution": {"box": 1},
    }


def test_cpd_paper_collision_package_generation_contract_records_one_package_dict(cpd_paper_report):
    report = cpd_paper_report
    preflight_row = report["paper_mapped_subset_collision_package_generation_preflight_contract"][
        "package_generation_preflight_rows"
    ][0]
    payload = report["paper_mapped_subset_collision_package_generation_contract"]
    rows = payload["collision_package_generation_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == COLLISION_PACKAGE_GENERATION_ROW_REQUIRED_KEYS
    package = row["generated_collision_package"]
    assert set(package) == GENERATED_COLLISION_PACKAGE_REQUIRED_KEYS
    assert package["package_id"] == (
        "paper_single_box:paper_mapped_subset_collision_package_generation_contract"
    )
    assert package["asset_id"] == "paper_single_box"
    assert package["source_path"] == "synthetic://cpd-paper/paper_single_box"
    assert package["method"] == "cpd_paper_mapped_subset_offline"
    assert package["stage"] == EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    assert package["status"] == ("offline_synthetic_candidate_runtime_admissibility_not_checked")
    assert package["claim_boundary"] == (
        "single_fixture_box_only_offline_collision_package_artifact_"
        "not_paper_vocabulary_runtime_admissibility_or_newton"
    )
    assert "not_paper_vocabulary" in package["claim_boundary"]
    assert package["mesh_point_count"] == 8
    assert package["mesh_face_count"] == 12
    assert package["max_source_faces"] == 12
    assert package["primitive_subset"] == ["box"]
    assert package["unsupported_primitives"] == []
    assert package["fallback"] is None
    assert package["primitives"] == [preflight_row["candidate_primitivespec_dict"]]
    assert row["unsupported_primitives_in_this_single_fixture"] == []
    assert row["primitive_families_not_evaluated_by_this_gate"] == [
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]


def test_cpd_paper_collision_package_generation_contract_stores_package_dict_once(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"]

    packages = list(_recursive_package_dicts(payload))

    assert len(packages) == 1
    assert (
        packages[0]
        is payload["collision_package_generation_rows"][0]["generated_collision_package"]
    )


def test_cpd_paper_collision_package_generation_contract_source_manifest_sha_is_exact(
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"]
    row = payload["collision_package_generation_rows"][0]
    package = row["generated_collision_package"]
    expected_manifest = {
        "contract_gate": "paper_mapped_subset_collision_package_generation_contract",
        "fixture_id": "paper_single_box",
        "fixture_scope": "synthetic_toy_mesh",
        "mesh_face_count": 12,
        "mesh_point_count": 8,
        "primitive_id": "paper_single_box__oriented_bounding_box__box",
        "primitive_kind": "box",
        "source_faces": list(range(12)),
    }
    expected_json = json.dumps(
        expected_manifest,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )

    assert row["synthetic_source_manifest"] == expected_manifest
    assert row["synthetic_source_manifest_canonical_json"] == expected_json
    assert package["source_sha256"] == hashlib.sha256(expected_json.encode("utf-8")).hexdigest()


@pytest.mark.parametrize("field_name", COLLISION_PACKAGE_GENERATION_ALLOWED_TRUE_FLAGS)
def test_cpd_paper_collision_package_generation_contract_allowed_package_flags_are_true(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"]

    assert payload[field_name] is True
    assert payload["collision_package_generation_rows"][0][field_name] is True


@pytest.mark.parametrize("field_name", COLLISION_PACKAGE_GENERATION_BOUNDARY_FALSE_FLAGS)
def test_cpd_paper_collision_package_generation_contract_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"]

    assert payload[field_name] is False
    assert payload["collision_package_generation_rows"][0][field_name] is False


def test_cpd_paper_collision_package_generation_contract_stays_newton_usd_and_metric_free(
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"]

    json.dumps(payload, allow_nan=False, sort_keys=True)
    forbidden_tokens = {
        "FallbackSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "surface_distance",
        "timing_result",
        "collision_quality_score",
    }
    assert forbidden_tokens.isdisjoint(set(_recursive_key_value_strings(payload)))
    assert payload["generated_collision_package_count"] == 1
    assert payload["runtime_admissibility_check_count"] == 0
    for row in payload["collision_package_generation_rows"]:
        assert isinstance(row["generated_collision_package"], dict)
        for flag in COLLISION_PACKAGE_GENERATION_BOUNDARY_FALSE_FLAGS:
            assert row[flag] is False


def test_cpd_paper_collision_package_generation_contract_static_boundaries():
    source = Path(cpd_paper_offline.__file__).read_text(encoding="utf-8")
    generation_block = source[
        source.index("_COLLISION_PACKAGE_GENERATION_CONTRACT_PAYLOAD_TRUE_FLAGS") : source.index(
            "_RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS"
        )
    ]

    assert generation_block.count("CollisionPackage") >= 1
    assert generation_block.count("PrimitiveSpec(") == 1
    forbidden_patterns = [
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
        "check_runtime_admissibility",
        "run_runtime_admissibility",
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
        assert pattern not in generation_block


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "collision_package_generation_contract_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "collision_package_generation_contract_input_next_gate_mismatch",
        ),
        (
            "later_collision_package_generation_candidate_count",
            0,
            "collision_package_generation_contract_input_count_mismatch:later_collision_package_generation_candidate_count",
        ),
        (
            "generated_collision_package_count",
            1,
            "collision_package_generation_contract_input_count_mismatch:generated_collision_package_count",
        ),
        (
            "runtime_admissibility_check_count",
            1,
            "collision_package_generation_contract_input_count_mismatch:runtime_admissibility_check_count",
        ),
    ],
)
def test_cpd_paper_collision_package_generation_contract_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    preflight = _collision_package_generation_contract_input()
    preflight[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_contract_payload(
            preflight
        )


@pytest.mark.parametrize("field_name", RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_collision_package_generation_contract_rejects_input_forbidden_flags(
    field_name,
):
    preflight = _collision_package_generation_contract_input()
    preflight[field_name] = True

    with pytest.raises(
        ValueError,
        match=(f"collision_package_generation_contract_input_trigger_flag_true:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_contract_payload(
            preflight
        )


@pytest.mark.parametrize("field_name", RUNTIME_CONSTRUCTION_FALSE_FLAGS)
def test_cpd_paper_collision_package_generation_contract_rejects_row_forbidden_flags(
    field_name,
):
    preflight = _collision_package_generation_contract_input()
    rows = [json.loads(json.dumps(row)) for row in preflight["package_generation_preflight_rows"]]
    rows[0][field_name] = True
    preflight["package_generation_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(f"collision_package_generation_contract_input_trigger_flag_true:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_contract_payload(
            preflight
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "collision_package_generation_contract_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "collision_package_generation_contract_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_collision_package_generation_contract_rejects_row_count_mismatch(
    mutate_rows,
    error_label,
):
    preflight = _collision_package_generation_contract_input()
    preflight["package_generation_preflight_rows"] = mutate_rows(
        preflight["package_generation_preflight_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_contract_payload(
            preflight
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "later_collision_package_generation_candidate",
            False,
            "collision_package_generation_contract_candidate_missing",
        ),
        (
            "package_generation_allowed_in_current_gate",
            True,
            "collision_package_generation_contract_prior_gate_boundary_mismatch",
        ),
        (
            "source_candidate_matrix_row_id",
            "candidate_matrix__wrong_source",
            "collision_package_generation_contract_anchored_preflight_row_mismatch:source_candidate_matrix_row_id",
        ),
        (
            "constructed_primitivespec_dict",
            {"kind": "box"},
            "collision_package_generation_contract_primitivespec_dict_mismatch",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "collision_package_generation_contract_primitivespec_dict_mismatch",
        ),
    ],
)
def test_cpd_paper_collision_package_generation_contract_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    preflight = _collision_package_generation_contract_input()
    rows = [json.loads(json.dumps(row)) for row in preflight["package_generation_preflight_rows"]]
    rows[0][field_name] = bad_value
    preflight["package_generation_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_contract_payload(
            preflight
        )


@pytest.mark.parametrize(
    ("mutate_spec", "error_label"),
    [
        (
            lambda source: {"kind": "box"},
            "collision_package_generation_contract_primitivespec_dict_schema_mismatch",
        ),
        (
            lambda source: {**source, "kind": "sphere"},
            "collision_package_generation_contract_primitivespec_dict_mismatch:kind",
        ),
        (
            lambda source: {
                **source,
                "dimensions": {"half_extents": [0.5, 0.5]},
            },
            "collision_package_generation_contract_primitivespec_dict_mismatch:shape",
        ),
    ],
)
def test_cpd_paper_collision_package_generation_contract_rejects_candidate_dict_drift(
    mutate_spec,
    error_label,
):
    preflight = _collision_package_generation_contract_input()
    rows = [json.loads(json.dumps(row)) for row in preflight["package_generation_preflight_rows"]]
    rows[0]["candidate_primitivespec_dict"] = mutate_spec(rows[0]["candidate_primitivespec_dict"])
    preflight["package_generation_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_collision_package_generation_contract_payload(
            preflight
        )


def test_cpd_paper_records_mapped_subset_runtime_admissibility_preflight_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_runtime_admissibility_preflight_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["generated_collision_package_count"] == 1
    assert report["runtime_admissibility_check_count"] == 1
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == (EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT)
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert payload["next_required_gate"] == (EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT)
    assert payload["runtime_admissibility_preflight_row_count"] == 1
    assert payload["later_runtime_admissibility_candidate_count"] == 1
    assert payload["generated_runtime_primitive_spec_count"] == 1
    assert payload["generated_primitive_spec_count"] == 1
    assert payload["generated_collision_package_count"] == 1
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["source_collision_package_available"] is True
    assert payload["runtime_admissibility_preflight_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT),
        "preflight_gate_closed": (EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT),
        "next_runtime_admissibility_gate_required": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
        ),
        "runtime_admissibility_preflight_rows_required": 1,
        "later_runtime_admissibility_candidates_required": 1,
        "generated_collision_packages_required": 1,
        "runtime_admissibility_checks_required": 0,
    }
    assert payload["remaining_gaps"] == EXPECTED_RUNTIME_ADMISSIBILITY_PREFLIGHT_REMAINING_GAPS


def test_cpd_paper_runtime_admissibility_preflight_payload_schema_is_exact(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_runtime_admissibility_preflight_contract"]

    assert set(payload) == RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["paper_faithful_offline_supported"] is False
    assert payload["artifact_kind"] == ("runtime_admissibility_preflight_not_runtime_check")
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_package_preflight_only_no_runtime_admissibility_"
        "no_newton_no_real_usd_no_benchmark"
    )
    assert payload["runtime_admissibility_preflight_action"] == (
        "record_one_later_runtime_admissibility_candidate_without_running_check"
    )
    assert payload["runtime_admissibility_preflight_requirements"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT),
        "preflight_gate_closed": (EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT),
        "next_runtime_admissibility_gate_required": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
        ),
        "source_fixture_required": "paper_single_box",
        "source_primitive_spec_kind_required": "box",
        "generated_collision_packages_required": 1,
        "runtime_admissibility_checks_required": 0,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
        "silent_drop_allowed": False,
    }
    assert payload["input_contract_summary"] == {
        "input_gate_id": (EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
        ),
        "input_collision_package_generation_row_count": 1,
        "input_generated_collision_package_count": 1,
        "input_runtime_admissibility_check_count": 0,
        "source_row_id": ("collision_package_generation__paper_single_box__box"),
        "source_package_id": (
            "paper_single_box:paper_mapped_subset_collision_package_generation_contract"
        ),
        "source_fixture_id": "paper_single_box",
        "source_primitive_spec_kind": "box",
    }
    assert payload["coverage_summary"] == {
        "runtime_admissibility_preflight_row_count": 1,
        "later_runtime_admissibility_candidate_record_count": 1,
        "generated_collision_package_record_count": 1,
        "runtime_admissibility_check_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "primitive_subset_distribution": {"box": 1},
    }


def test_cpd_paper_runtime_admissibility_preflight_records_one_candidate_without_copying_package(
    cpd_paper_report,
):
    report = cpd_paper_report
    source_payload = report["paper_mapped_subset_collision_package_generation_contract"]
    source_row = source_payload["collision_package_generation_rows"][0]
    source_package = source_row["generated_collision_package"]
    payload = report["paper_mapped_subset_runtime_admissibility_preflight_contract"]
    rows = payload["runtime_admissibility_preflight_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == RUNTIME_ADMISSIBILITY_PREFLIGHT_ROW_REQUIRED_KEYS
    assert row["runtime_admissibility_preflight_row_id"] == (
        "runtime_admissibility_preflight__paper_single_box__box"
    )
    assert (
        row["source_collision_package_generation_row_id"]
        == (source_row["collision_package_generation_row_id"])
    )
    assert row["source_package_id"] == source_package["package_id"]
    assert row["source_asset_id"] == "paper_single_box"
    assert row["source_package_stage"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert row["source_package_status"] == (
        "offline_synthetic_candidate_runtime_admissibility_not_checked"
    )
    assert row["source_package_method"] == "cpd_paper_mapped_subset_offline"
    assert row["source_package_source_path"] == ("synthetic://cpd-paper/paper_single_box")
    assert row["source_package_source_sha256"] == source_package["source_sha256"]
    assert row["source_package_claim_boundary"] == source_package["claim_boundary"]
    assert row["source_package_primitive_count"] == 1
    assert row["source_package_primitive_subset"] == ["box"]
    assert row["source_package_unsupported_primitives"] == []
    assert row["source_package_runtime_admissibility_status"] == ("not_checked")
    assert row["candidate_primitivespec_dict"] == (source_row["candidate_primitivespec_dict"])
    assert row["source_collision_package_available"] is True
    assert row["later_runtime_admissibility_candidate"] is True
    assert row["runtime_admissibility_preflight_decision"] == (
        "eligible_for_later_runtime_admissibility_contract"
    )
    assert row["required_later_gate"] == (EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT)
    assert list(_recursive_package_dicts(payload)) == []


@pytest.mark.parametrize("field_name", RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS)
def test_cpd_paper_runtime_admissibility_preflight_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_runtime_admissibility_preflight_contract"]

    assert payload[field_name] is False
    assert payload["runtime_admissibility_preflight_rows"][0][field_name] is False


def test_cpd_paper_runtime_admissibility_preflight_stays_newton_usd_and_metric_free(
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_runtime_admissibility_preflight_contract"]

    json.dumps(payload, allow_nan=False, sort_keys=True)
    forbidden_tokens = {
        "FallbackSpec",
        "runtime_result",
        "usd_asset_path",
        "benchmark_metric",
        "surface_distance",
        "timing_result",
        "collision_quality_score",
    }
    assert forbidden_tokens.isdisjoint(set(_recursive_key_value_strings(payload)))
    assert list(_recursive_package_dicts(payload)) == []
    assert payload["generated_collision_package_count"] == 1
    assert payload["runtime_admissibility_check_count"] == 0


def test_cpd_paper_runtime_admissibility_preflight_static_boundaries():
    source = Path(cpd_paper_offline.__file__).read_text(encoding="utf-8")
    preflight_block = source[
        source.index("_RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS") : source.index(
            "_RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS"
        )
    ]

    assert "CollisionPackage(" not in preflight_block
    assert "PrimitiveSpec(" not in preflight_block
    forbidden_patterns = [
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
        "check_runtime_admissibility",
        "run_runtime_admissibility",
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
        assert pattern not in preflight_block


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "runtime_admissibility_preflight_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "runtime_admissibility_preflight_input_next_gate_mismatch",
        ),
        (
            "collision_package_generation_row_count",
            2,
            "runtime_admissibility_preflight_input_count_mismatch:collision_package_generation_row_count",
        ),
        (
            "generated_collision_package_count",
            2,
            "runtime_admissibility_preflight_input_count_mismatch:generated_collision_package_count",
        ),
        (
            "runtime_admissibility_check_count",
            1,
            "runtime_admissibility_preflight_input_count_mismatch:runtime_admissibility_check_count",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_preflight_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    generation = _runtime_admissibility_preflight_input()
    generation[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


@pytest.mark.parametrize("field_name", RUNTIME_ADMISSIBILITY_PREFLIGHT_INPUT_FALSE_FLAGS)
def test_cpd_paper_runtime_admissibility_preflight_rejects_input_forbidden_flags(
    field_name,
):
    generation = _runtime_admissibility_preflight_input()
    generation[field_name] = True

    with pytest.raises(
        ValueError,
        match=(f"runtime_admissibility_preflight_input_trigger_flag_true:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


@pytest.mark.parametrize("field_name", RUNTIME_ADMISSIBILITY_PREFLIGHT_INPUT_FALSE_FLAGS)
def test_cpd_paper_runtime_admissibility_preflight_rejects_row_forbidden_flags(
    field_name,
):
    generation = _runtime_admissibility_preflight_input()
    rows = [json.loads(json.dumps(row)) for row in generation["collision_package_generation_rows"]]
    rows[0][field_name] = True
    generation["collision_package_generation_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(f"runtime_admissibility_preflight_input_trigger_flag_true:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "runtime_admissibility_preflight_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "runtime_admissibility_preflight_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_preflight_rejects_source_row_count_drift(
    mutate_rows,
    error_label,
):
    generation = _runtime_admissibility_preflight_input()
    generation["collision_package_generation_rows"] = mutate_rows(
        generation["collision_package_generation_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "fixture_id",
            "wrong_fixture",
            "runtime_admissibility_preflight_source_row_mismatch:fixture_id",
        ),
        (
            "paper_primitive",
            "sphere",
            "runtime_admissibility_preflight_source_row_mismatch:paper_primitive",
        ),
        (
            "primitive_spec_kind",
            "sphere",
            "runtime_admissibility_preflight_source_row_mismatch:primitive_spec_kind",
        ),
        (
            "candidate_mapping_label",
            "sphere",
            "runtime_admissibility_preflight_source_row_mismatch:candidate_mapping_label",
        ),
        (
            "newton_runtime_kind",
            "sphere",
            "runtime_admissibility_preflight_source_row_mismatch:newton_runtime_kind",
        ),
        (
            "primitive_id",
            "wrong_primitive",
            "runtime_admissibility_preflight_source_row_mismatch:primitive_id",
        ),
        (
            "kind",
            "sphere",
            "runtime_admissibility_preflight_source_row_mismatch:kind",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_preflight_rejects_source_row_identity_drift(
    field_name,
    bad_value,
    error_label,
):
    generation = _runtime_admissibility_preflight_input()
    rows = [json.loads(json.dumps(row)) for row in generation["collision_package_generation_rows"]]
    rows[0][field_name] = bad_value
    generation["collision_package_generation_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


def test_cpd_paper_runtime_admissibility_preflight_rejects_extra_source_package_copy():
    generation = _runtime_admissibility_preflight_input()
    source_package = generation["collision_package_generation_rows"][0][
        "generated_collision_package"
    ]
    generation["unexpected_package_copy"] = json.loads(json.dumps(source_package))

    with pytest.raises(
        ValueError,
        match="runtime_admissibility_preflight_source_package_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "asset_id",
            "wrong_asset",
            "runtime_admissibility_preflight_package_mismatch:asset_id",
        ),
        (
            "package_id",
            "wrong_package",
            "runtime_admissibility_preflight_package_mismatch:package_id",
        ),
        (
            "source_path",
            "synthetic://wrong",
            "runtime_admissibility_preflight_package_mismatch:source_path",
        ),
        (
            "method",
            "wrong_method",
            "runtime_admissibility_preflight_package_mismatch:method",
        ),
        (
            "stage",
            "wrong_stage",
            "runtime_admissibility_preflight_package_mismatch:stage",
        ),
        (
            "status",
            "runtime_admissible",
            "runtime_admissibility_preflight_package_mismatch:status",
        ),
        (
            "source_sha256",
            "0" * 64,
            "runtime_admissibility_preflight_package_mismatch:source_sha256",
        ),
        (
            "primitive_subset",
            ["sphere"],
            "runtime_admissibility_preflight_package_mismatch:primitive_subset",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_preflight_rejects_package_drift(
    field_name,
    bad_value,
    error_label,
):
    generation = _runtime_admissibility_preflight_input()
    rows = [json.loads(json.dumps(row)) for row in generation["collision_package_generation_rows"]]
    rows[0]["generated_collision_package"][field_name] = bad_value
    generation["collision_package_generation_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


def test_cpd_paper_runtime_admissibility_preflight_rejects_package_key_drift():
    generation = _runtime_admissibility_preflight_input()
    rows = [json.loads(json.dumps(row)) for row in generation["collision_package_generation_rows"]]
    del rows[0]["generated_collision_package"]["asset_id"]
    generation["collision_package_generation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="runtime_admissibility_preflight_package_schema_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


def test_cpd_paper_runtime_admissibility_preflight_rejects_primitive_drift():
    generation = _runtime_admissibility_preflight_input()
    rows = [json.loads(json.dumps(row)) for row in generation["collision_package_generation_rows"]]
    rows[0]["generated_collision_package"]["primitives"][0]["kind"] = "sphere"
    generation["collision_package_generation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="runtime_admissibility_preflight_package_mismatch:primitives",
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


def test_cpd_paper_runtime_admissibility_preflight_rejects_coupled_source_and_package_primitive_drift():
    generation = _runtime_admissibility_preflight_input()
    rows = [json.loads(json.dumps(row)) for row in generation["collision_package_generation_rows"]]
    drifted_candidate = {
        **rows[0]["candidate_primitivespec_dict"],
        "kind": "sphere",
    }
    rows[0]["candidate_primitivespec_dict"] = drifted_candidate
    rows[0]["generated_collision_package"]["primitives"][0] = drifted_candidate
    generation["collision_package_generation_rows"] = rows

    with pytest.raises(
        ValueError,
        match=("runtime_admissibility_preflight_source_row_mismatch:candidate_primitivespec_dict"),
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_preflight_contract_payload(
            generation
        )


def test_cpd_paper_records_mapped_subset_runtime_admissibility_contract_gate(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_runtime_admissibility_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["generated_collision_package_count"] == 1
    assert report["runtime_admissibility_check_count"] == 1
    assert (
        EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT
    assert (
        payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
    )
    assert payload["runtime_admissibility_row_count"] == 1
    assert payload["offline_static_runtime_admissibility_check_count"] == 1
    assert payload["offline_static_runtime_admissibility_checked"] is True
    assert payload["runtime_admissibility_check_count"] == 1
    assert payload["runtime_execution_count"] == 0
    assert payload["newton_mapping_record_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["generated_collision_package_count"] == 1
    assert payload["source_collision_package_available"] is True
    assert payload["remaining_gaps"] == EXPECTED_RUNTIME_ADMISSIBILITY_CONTRACT_REMAINING_GAPS


def test_cpd_paper_runtime_admissibility_contract_payload_schema_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_runtime_admissibility_contract"]

    assert set(payload) == RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_REQUIRED_KEYS
    assert payload["gate_status"] == (
        "implemented_single_fixture_runtime_admissibility_contract_static_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "runtime_admissibility_contract_complete_newton_shape_mapping_preflight_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_static_runtime_admissibility_contract_not_newton_mapping"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_package_static_admissibility_only_"
        "no_newton_no_real_usd_no_benchmark_no_metrics"
    )
    assert payload["runtime_admissibility_action"] == (
        "run_one_offline_static_runtime_admissibility_check_for_paper_single_box_box_package"
    )
    assert payload["runtime_admissibility_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT),
        "closed_gate": EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT,
        "next_newton_shape_mapping_preflight_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
        ),
        "runtime_admissibility_rows_required": 1,
        "offline_static_runtime_admissibility_checks_required": 1,
        "runtime_execution_allowed": False,
        "newton_mapping_allowed": False,
    }
    assert payload["coverage_summary"] == {
        "runtime_admissibility_row_count": 1,
        "offline_static_runtime_admissibility_check_count": 1,
        "passed_static_runtime_admissibility_check_count": 1,
        "runtime_execution_count": 0,
        "newton_mapping_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "primitive_subset_distribution": {"box": 1},
    }


def test_cpd_paper_runtime_admissibility_contract_records_static_check_row(cpd_paper_report):
    report = cpd_paper_report
    source_payload = report["paper_mapped_subset_runtime_admissibility_preflight_contract"]
    source_row = source_payload["runtime_admissibility_preflight_rows"][0]
    payload = report["paper_mapped_subset_runtime_admissibility_contract"]
    rows = payload["runtime_admissibility_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == RUNTIME_ADMISSIBILITY_CONTRACT_ROW_REQUIRED_KEYS
    assert row["runtime_admissibility_row_id"] == ("runtime_admissibility__paper_single_box__box")
    assert (
        row["source_runtime_admissibility_preflight_row_id"]
        == (source_row["runtime_admissibility_preflight_row_id"])
    )
    assert row["candidate_primitivespec_dict"] == (source_row["candidate_primitivespec_dict"])
    assert row["source_package_id"] == source_row["source_package_id"]
    assert row["source_package_stage"] == (
        EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT
    )
    assert row["source_package_primitive_subset"] == ["box"]
    assert row["source_package_unsupported_primitives"] == []
    assert row["runtime_admissibility_static_check_kind"] == (
        "offline_static_primitivespec_box_schema_check"
    )
    assert row["runtime_admissibility_decision"] == (
        "admissible_for_later_newton_shape_mapping_preflight"
    )
    assert row["runtime_admissibility_status"] == (
        "offline_static_admissible_for_later_newton_shape_mapping_preflight"
    )
    assert row["required_later_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
    )
    assert row["finite_center_check_passed"] is True
    assert row["finite_axes_check_passed"] is True
    assert row["orthonormal_axes_check_passed"] is True
    assert row["right_handed_axes_check_passed"] is True
    assert row["positive_dimensions_check_passed"] is True
    assert row["target_shape_schema_check_passed"] is True
    assert row["source_faces_check_passed"] is True
    assert row["contains_assigned_points_check_passed"] is True
    assert row["volume_check_passed"] is True
    assert row["weighted_volume_check_passed"] is True
    assert row["offline_static_runtime_admissibility_check_passed"] is True
    assert row["offline_static_runtime_admissibility_checked"] is True
    assert list(_recursive_package_dicts(payload)) == []


@pytest.mark.parametrize("field_name", RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS)
def test_cpd_paper_runtime_admissibility_contract_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_runtime_admissibility_contract"]

    assert payload[field_name] is False
    assert payload["runtime_admissibility_rows"][0][field_name] is False


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "runtime_admissibility_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "runtime_admissibility_input_next_gate_mismatch",
        ),
        (
            "input_gate_id",
            "stale_gate",
            "runtime_admissibility_input_metadata_mismatch:input_gate_id",
        ),
        (
            "closed_gate",
            "stale_gate",
            "runtime_admissibility_input_metadata_mismatch:closed_gate",
        ),
        (
            "runtime_admissibility_preflight_contract",
            {},
            "runtime_admissibility_input_metadata_mismatch:"
            "runtime_admissibility_preflight_contract",
        ),
        (
            "runtime_admissibility_preflight_row_count",
            2,
            "runtime_admissibility_input_count_mismatch:runtime_admissibility_preflight_row_count",
        ),
        (
            "runtime_admissibility_check_count",
            1,
            "runtime_admissibility_input_count_mismatch:runtime_admissibility_check_count",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_contract_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    preflight = _runtime_admissibility_contract_input()
    preflight[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_contract_payload(preflight)


@pytest.mark.parametrize("field_name", RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS)
def test_cpd_paper_runtime_admissibility_contract_rejects_input_forbidden_flags(
    field_name,
):
    preflight = _runtime_admissibility_contract_input()
    preflight[field_name] = True

    with pytest.raises(
        ValueError,
        match=f"runtime_admissibility_input_trigger_flag_true:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_contract_payload(preflight)


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "runtime_admissibility_preflight_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "runtime_admissibility_preflight_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_contract_rejects_row_count_drift(
    mutate_rows,
    error_label,
):
    preflight = _runtime_admissibility_contract_input()
    preflight["runtime_admissibility_preflight_rows"] = mutate_rows(
        preflight["runtime_admissibility_preflight_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_contract_payload(preflight)


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "fixture_id",
            "wrong_fixture",
            "runtime_admissibility_preflight_row_mismatch:fixture_id",
        ),
        (
            "source_package_id",
            "wrong_package",
            "runtime_admissibility_preflight_row_mismatch:source_package_id",
        ),
        (
            "source_package_claim_boundary",
            "wrong_boundary",
            "runtime_admissibility_preflight_row_mismatch:source_package_claim_boundary",
        ),
        (
            "source_package_primitive_subset",
            ["sphere"],
            "runtime_admissibility_preflight_row_mismatch:source_package_primitive_subset",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_contract_rejects_preflight_row_drift(
    field_name,
    bad_value,
    error_label,
):
    preflight = _runtime_admissibility_contract_input()
    rows = [
        json.loads(json.dumps(row)) for row in preflight["runtime_admissibility_preflight_rows"]
    ]
    rows[0][field_name] = bad_value
    preflight["runtime_admissibility_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_contract_payload(preflight)


def test_cpd_paper_runtime_admissibility_contract_rejects_source_package_copy(cpd_paper_report):
    preflight = _runtime_admissibility_contract_input()
    source_package = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"][
        "collision_package_generation_rows"
    ][0]["generated_collision_package"]
    preflight["unexpected_package_copy"] = json.loads(json.dumps(source_package))

    with pytest.raises(
        ValueError,
        match="runtime_admissibility_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_contract_payload(preflight)


@pytest.mark.parametrize(
    ("mutate_candidate", "error_label"),
    [
        (
            lambda candidate: {**candidate, "kind": "sphere"},
            "runtime_admissibility_primitivespec_mismatch:kind",
        ),
        (
            lambda candidate: {**candidate, "center": [float("nan"), 0.0, 0.0]},
            "runtime_admissibility_primitivespec_invalid_center",
        ),
        (
            lambda candidate: {**candidate, "center": [10.0, 20.0, 30.0]},
            "runtime_admissibility_primitivespec_mismatch:center",
        ),
        (
            lambda candidate: {**candidate, "axes": [[1.0, 0.0, 0.0]]},
            "runtime_admissibility_primitivespec_invalid_axes",
        ),
        (
            lambda candidate: {
                **candidate,
                "axes": [[2.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            },
            "runtime_admissibility_primitivespec_axes_not_orthonormal",
        ),
        (
            lambda candidate: {
                **candidate,
                "axes": [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]],
            },
            "runtime_admissibility_primitivespec_axes_not_right_handed",
        ),
        (
            lambda candidate: {**candidate, "dimensions": {}},
            "runtime_admissibility_primitivespec_invalid_dimensions",
        ),
        (
            lambda candidate: {
                **candidate,
                "dimensions": {"half_extents": [-1.0, 1.0, 1.0]},
            },
            "runtime_admissibility_primitivespec_invalid_dimensions",
        ),
        (
            lambda candidate: {
                **candidate,
                "dimensions": {"half_extents": [2.0, 2.0, 2.0]},
                "volume": 64.0,
                "weighted_volume": 64.0,
            },
            "runtime_admissibility_primitivespec_mismatch:dimensions",
        ),
        (
            lambda candidate: {**candidate, "source_faces": [0, 1]},
            "runtime_admissibility_primitivespec_mismatch:source_faces",
        ),
        (
            lambda candidate: {**candidate, "contains_assigned_points": False},
            "runtime_admissibility_primitivespec_mismatch:contains_assigned_points",
        ),
        (
            lambda candidate: {**candidate, "volume": 999.0},
            "runtime_admissibility_primitivespec_mismatch:volume",
        ),
        (
            lambda candidate: {**candidate, "weighted_volume": 999.0},
            "runtime_admissibility_primitivespec_mismatch:weighted_volume",
        ),
        (
            lambda candidate: {**candidate, "conversion_status": "candidate"},
            "runtime_admissibility_primitivespec_mismatch:conversion_status",
        ),
    ],
)
def test_cpd_paper_runtime_admissibility_contract_rejects_primitivespec_drift(
    mutate_candidate,
    error_label,
):
    preflight = _runtime_admissibility_contract_input()
    rows = [
        json.loads(json.dumps(row)) for row in preflight["runtime_admissibility_preflight_rows"]
    ]
    rows[0]["candidate_primitivespec_dict"] = mutate_candidate(
        rows[0]["candidate_primitivespec_dict"]
    )
    preflight["runtime_admissibility_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_runtime_admissibility_contract_payload(preflight)


def test_cpd_paper_runtime_admissibility_contract_static_boundaries():
    source = Path(cpd_paper_offline.__file__).read_text(encoding="utf-8")
    contract_block = source[
        source.index("_RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS") : source.index(
            "_NEWTON_SHAPE_MAPPING_PREFLIGHT_PAYLOAD_FALSE_FLAGS"
        )
    ]

    assert "CollisionPackage(" not in contract_block
    assert "PrimitiveSpec(" not in contract_block
    forbidden_patterns = [
        "FallbackSpec",
        "primitive_collision_compiler.newton",
        "import newton",
        "import newton_warp",
        "Newton",
        "run_newton",
        "map_package_shapes",
        "check_runtime_admissibility",
        "run_runtime_admissibility",
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
        assert pattern not in contract_block


def test_cpd_paper_records_mapped_subset_newton_shape_mapping_preflight_gate(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_mapping_preflight_contract"]

    assert report["next_required_gate"] == (EXPECTED_CURRENT_REPORT_NEXT_GATE)
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["generated_collision_package_count"] == 1
    assert report["runtime_admissibility_check_count"] == 1
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert payload["gate_id"] == (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT)
    assert payload["input_gate_id"] == (EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT)
    assert payload["next_required_gate"] == (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT)
    assert payload["newton_shape_mapping_preflight_row_count"] == 1
    assert payload["source_runtime_admissibility_row_count"] == 1
    assert payload["source_runtime_admissibility_check_passed"] is True
    assert payload["newton_shape_mapping_preflight_passed"] is True
    assert payload["mapping_attempt_count"] == 0
    assert payload["newton_mapping_record_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_NEWTON_SHAPE_MAPPING_PREFLIGHT_REMAINING_GAPS


def test_cpd_paper_newton_shape_mapping_preflight_payload_schema_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_newton_shape_mapping_preflight_contract"]

    assert set(payload) == NEWTON_SHAPE_MAPPING_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_shape_mapping_preflight_static_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_shape_mapping_preflight_complete_newton_shape_mapping_contract_missing"
    )
    assert payload["artifact_kind"] == ("offline_static_newton_shape_mapping_preflight_not_mapping")
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_mapping_preflight_only_"
        "no_mapper_no_newton_no_real_usd_no_benchmark_no_metrics"
    )
    assert payload["newton_shape_mapping_preflight_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT),
        "closed_gate": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT),
        "next_newton_shape_mapping_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
        ),
        "newton_shape_mapping_preflight_rows_required": 1,
        "mapping_attempt_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["coverage_summary"] == {
        "newton_shape_mapping_preflight_row_count": 1,
        "source_runtime_admissibility_row_count": 1,
        "passed_source_runtime_admissibility_check_count": 1,
        "mapping_attempt_count": 0,
        "newton_mapping_record_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "target_newton_shape_kind_distribution": {"box": 1},
    }


def test_cpd_paper_newton_shape_mapping_preflight_records_static_row(cpd_paper_report):
    report = cpd_paper_report
    source_payload = report["paper_mapped_subset_runtime_admissibility_contract"]
    source_row = source_payload["runtime_admissibility_rows"][0]
    payload = report["paper_mapped_subset_newton_shape_mapping_preflight_contract"]
    rows = payload["newton_shape_mapping_preflight_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NEWTON_SHAPE_MAPPING_PREFLIGHT_ROW_REQUIRED_KEYS
    assert row["newton_shape_mapping_preflight_row_id"] == (
        "newton_shape_mapping_preflight__paper_single_box__box"
    )
    assert (
        row["source_runtime_admissibility_row_id"] == (source_row["runtime_admissibility_row_id"])
    )
    assert row["candidate_primitivespec_dict"] == (source_row["candidate_primitivespec_dict"])
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["target_newton_shape_kind"] == "box"
    assert row["target_newton_shape_kind_declared"] is True
    assert row["newton_shape_support_evidence_status"] == (
        "pending_later_mapping_contract_no_support_claim"
    )
    assert row["target_newton_shape_kind_handoff_source"] == (
        "static_current_report_lane_declares_box_target_schema_for_later_mapper"
    )
    assert row["center_transfer_field"] == "candidate_primitivespec_dict.center"
    assert row["axes_transfer_field"] == "candidate_primitivespec_dict.axes"
    assert row["dimensions_transfer_field"] == "candidate_primitivespec_dict.dimensions"
    assert row["box_half_extents_transfer_field"] == (
        "candidate_primitivespec_dict.dimensions.half_extents"
    )
    assert row["target_kind_declared_check_passed"] is True
    assert row["center_transfer_check_passed"] is True
    assert row["axes_transfer_check_passed"] is True
    assert row["box_dimensions_transfer_check_passed"] is True
    assert row["source_runtime_admissibility_check_passed"] is True
    assert row["source_package_lineage_check_passed"] is True
    assert row["newton_shape_mapping_preflight_passed"] is True
    assert row["mapping_attempt_count"] == 0
    assert row["newton_mapping_record_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    assert list(_recursive_package_dicts(payload)) == []


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_MAPPING_PREFLIGHT_FALSE_FLAGS)
def test_cpd_paper_newton_shape_mapping_preflight_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_newton_shape_mapping_preflight_contract"]

    assert payload[field_name] is False
    assert payload["newton_shape_mapping_preflight_rows"][0][field_name] is False


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_mapping_preflight_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_mapping_preflight_input_next_gate_mismatch",
        ),
        (
            "runtime_admissibility_row_count",
            2,
            "newton_shape_mapping_preflight_input_count_mismatch:runtime_admissibility_row_count",
        ),
        (
            "offline_static_runtime_admissibility_check_count",
            0,
            "newton_shape_mapping_preflight_input_count_mismatch:"
            "offline_static_runtime_admissibility_check_count",
        ),
        (
            "runtime_admissibility_check_count",
            0,
            "newton_shape_mapping_preflight_input_count_mismatch:runtime_admissibility_check_count",
        ),
        (
            "generated_runtime_primitive_spec_count",
            0,
            "newton_shape_mapping_preflight_input_count_mismatch:"
            "generated_runtime_primitive_spec_count",
        ),
        (
            "generated_primitive_spec_count",
            0,
            "newton_shape_mapping_preflight_input_count_mismatch:generated_primitive_spec_count",
        ),
        (
            "generated_collision_package_count",
            0,
            "newton_shape_mapping_preflight_input_count_mismatch:generated_collision_package_count",
        ),
        (
            "newton_mapping_record_count",
            1,
            "newton_shape_mapping_preflight_input_count_mismatch:newton_mapping_record_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_mapping_preflight_input_count_mismatch:newton_runtime_execution_count",
        ),
        (
            "offline_static_runtime_admissibility_checked",
            False,
            "newton_shape_mapping_preflight_input_count_mismatch:"
            "offline_static_runtime_admissibility_checked",
        ),
    ],
)
def test_cpd_paper_newton_shape_mapping_preflight_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    runtime_admissibility = _newton_shape_mapping_preflight_input()
    runtime_admissibility[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_preflight_contract_payload(
            runtime_admissibility
        )


@pytest.mark.parametrize("field_name", RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS)
def test_cpd_paper_newton_shape_mapping_preflight_rejects_input_forbidden_flags(
    field_name,
):
    runtime_admissibility = _newton_shape_mapping_preflight_input()
    runtime_admissibility[field_name] = True

    with pytest.raises(
        ValueError,
        match=f"newton_shape_mapping_preflight_input_flag_true:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_preflight_contract_payload(
            runtime_admissibility
        )


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "newton_shape_mapping_preflight_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "newton_shape_mapping_preflight_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_newton_shape_mapping_preflight_rejects_row_count_drift(
    mutate_rows,
    error_label,
):
    runtime_admissibility = _newton_shape_mapping_preflight_input()
    runtime_admissibility["runtime_admissibility_rows"] = mutate_rows(
        runtime_admissibility["runtime_admissibility_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_preflight_contract_payload(
            runtime_admissibility
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "runtime_admissibility_row_id",
            "wrong_row",
            "newton_shape_mapping_preflight_source_row_mismatch:runtime_admissibility_row_id",
        ),
        (
            "fixture_id",
            "wrong_fixture",
            "newton_shape_mapping_preflight_source_row_mismatch:fixture_id",
        ),
        (
            "primitive_spec_kind",
            "sphere",
            "newton_shape_mapping_preflight_source_row_mismatch:primitive_spec_kind",
        ),
        (
            "offline_static_runtime_admissibility_check_passed",
            False,
            "newton_shape_mapping_preflight_source_row_mismatch:"
            "offline_static_runtime_admissibility_check_passed",
        ),
        (
            "offline_static_runtime_admissibility_checked",
            False,
            "newton_shape_mapping_preflight_source_row_mismatch:"
            "offline_static_runtime_admissibility_checked",
        ),
    ],
)
def test_cpd_paper_newton_shape_mapping_preflight_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    runtime_admissibility = _newton_shape_mapping_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in runtime_admissibility["runtime_admissibility_rows"]
    ]
    rows[0][field_name] = bad_value
    runtime_admissibility["runtime_admissibility_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_preflight_contract_payload(
            runtime_admissibility
        )


def test_cpd_paper_newton_shape_mapping_preflight_rejects_source_package_copy(cpd_paper_report):
    runtime_admissibility = _newton_shape_mapping_preflight_input()
    source_package = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"][
        "collision_package_generation_rows"
    ][0]["generated_collision_package"]
    runtime_admissibility["unexpected_package_copy"] = json.loads(json.dumps(source_package))

    with pytest.raises(
        ValueError,
        match="newton_shape_mapping_preflight_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_preflight_contract_payload(
            runtime_admissibility
        )


@pytest.mark.parametrize(
    ("mutate_candidate", "error_label"),
    [
        (
            lambda candidate: {**candidate, "kind": "sphere"},
            "newton_shape_mapping_preflight_primitivespec_mismatch:kind",
        ),
        (
            lambda candidate: {**candidate, "center": None},
            "newton_shape_mapping_preflight_primitivespec_invalid:center",
        ),
        (
            lambda candidate: {**candidate, "axes": None},
            "newton_shape_mapping_preflight_primitivespec_invalid:axes",
        ),
        (
            lambda candidate: {**candidate, "dimensions": {}},
            "newton_shape_mapping_preflight_primitivespec_invalid:dimensions",
        ),
        (
            lambda candidate: {
                **candidate,
                "dimensions": {"half_extents": [1.0, 1.0]},
            },
            "newton_shape_mapping_preflight_primitivespec_invalid:half_extents",
        ),
    ],
)
def test_cpd_paper_newton_shape_mapping_preflight_rejects_primitivespec_drift(
    mutate_candidate,
    error_label,
):
    runtime_admissibility = _newton_shape_mapping_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in runtime_admissibility["runtime_admissibility_rows"]
    ]
    rows[0]["candidate_primitivespec_dict"] = mutate_candidate(
        rows[0]["candidate_primitivespec_dict"]
    )
    runtime_admissibility["runtime_admissibility_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_preflight_contract_payload(
            runtime_admissibility
        )


def test_cpd_paper_newton_shape_mapping_preflight_rejects_missing_primitivespec_candidate():
    runtime_admissibility = _newton_shape_mapping_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in runtime_admissibility["runtime_admissibility_rows"]
    ]
    rows[0].pop("candidate_primitivespec_dict")
    runtime_admissibility["runtime_admissibility_rows"] = rows

    with pytest.raises(
        ValueError,
        match="newton_shape_mapping_preflight_primitivespec_invalid:candidate",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_preflight_contract_payload(
            runtime_admissibility
        )


@pytest.mark.parametrize("candidate_value", [None, "box", ["box"]])
def test_cpd_paper_newton_shape_mapping_preflight_rejects_non_dict_primitivespec_candidate(
    candidate_value,
):
    runtime_admissibility = _newton_shape_mapping_preflight_input()
    rows = [
        json.loads(json.dumps(row)) for row in runtime_admissibility["runtime_admissibility_rows"]
    ]
    rows[0]["candidate_primitivespec_dict"] = candidate_value
    runtime_admissibility["runtime_admissibility_rows"] = rows

    with pytest.raises(
        ValueError,
        match="newton_shape_mapping_preflight_primitivespec_invalid:candidate",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_preflight_contract_payload(
            runtime_admissibility
        )


def test_cpd_paper_newton_shape_mapping_preflight_static_boundaries():
    source = Path(cpd_paper_offline.__file__).read_text(encoding="utf-8")
    contract_block = source[
        source.index("_NEWTON_SHAPE_MAPPING_PREFLIGHT_PAYLOAD_FALSE_FLAGS") : source.index(
            "_NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_FALSE_FLAGS"
        )
    ]

    assert "CollisionPackage(" not in contract_block
    assert "PrimitiveSpec(" not in contract_block
    forbidden_patterns = [
        "FallbackSpec",
        "primitive_collision_compiler.newton",
        "NewtonShapeMapping",
        "map_package_shapes",
        "import newton",
        "import newton_warp",
        "Newton",
        "run_newton",
        "newton.",
        "check_runtime_admissibility",
        "run_runtime_admissibility",
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
        assert pattern not in contract_block


def test_cpd_paper_records_mapped_subset_newton_shape_mapping_contract_gate(cpd_paper_report):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_mapping_contract"]

    assert report["next_required_gate"] == (EXPECTED_CURRENT_REPORT_NEXT_GATE)
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT)
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["shape_mapping_contract_row_count"] == 1
    assert payload["source_newton_shape_mapping_preflight_row_count"] == 1
    assert payload["report_scoped_newton_shape_descriptor_count"] == 1
    assert payload["source_preflight_check_passed"] is True
    assert payload["mapping_attempt_count"] == 0
    assert payload["newton_mapping_record_count"] == 0
    assert payload["newton_shape_object_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_NEWTON_SHAPE_MAPPING_CONTRACT_REMAINING_GAPS


def test_cpd_paper_newton_shape_mapping_contract_payload_schema_is_exact(cpd_paper_report):
    payload = cpd_paper_report["paper_mapped_subset_newton_shape_mapping_contract"]

    assert set(payload) == NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_REQUIRED_KEYS
    assert payload["gate_status"] == ("implemented_offline_static_shape_descriptor_contract_only")
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_shape_mapping_contract_complete_newton_shape_runtime_boundary_preflight_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_static_newton_shape_descriptor_contract_not_runtime_mapping"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_shape_descriptor_contract_only_"
        "no_newton_object_no_runtime_no_real_usd_no_benchmark_no_metrics"
    )
    assert payload["newton_shape_mapping_contract"] == {
        "input_gate_required": (EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT),
        "closed_gate": EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT,
        "next_newton_shape_runtime_boundary_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "shape_mapping_contract_rows_required": 1,
        "report_scoped_newton_shape_descriptors_required": 1,
        "newton_shape_object_allowed": False,
        "newton_runtime_allowed": False,
        "newton_support_claim_allowed": False,
    }
    assert payload["coverage_summary"] == {
        "shape_mapping_contract_row_count": 1,
        "source_newton_shape_mapping_preflight_row_count": 1,
        "report_scoped_newton_shape_descriptor_count": 1,
        "passed_source_preflight_check_count": 1,
        "mapping_attempt_count": 0,
        "newton_mapping_record_count": 0,
        "newton_shape_object_count": 0,
        "newton_runtime_execution_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "target_newton_shape_kind_distribution": {"box": 1},
    }


def test_cpd_paper_newton_shape_mapping_contract_records_descriptor_row(cpd_paper_report):
    report = cpd_paper_report
    preflight_row = report["paper_mapped_subset_newton_shape_mapping_preflight_contract"][
        "newton_shape_mapping_preflight_rows"
    ][0]
    payload = report["paper_mapped_subset_newton_shape_mapping_contract"]
    rows = payload["shape_mapping_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == NEWTON_SHAPE_MAPPING_CONTRACT_ROW_REQUIRED_KEYS
    assert row["shape_mapping_row_id"] == ("newton_shape_mapping__paper_single_box__box")
    assert (
        row["source_newton_shape_mapping_preflight_row_id"]
        == (preflight_row["newton_shape_mapping_preflight_row_id"])
    )
    assert (
        row["source_runtime_admissibility_row_id"]
        == (preflight_row["source_runtime_admissibility_row_id"])
    )
    assert row["source_package_id"] == preflight_row["source_package_id"]
    assert row["source_asset_id"] == preflight_row["source_asset_id"]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["primitive_id"] == ("paper_single_box__oriented_bounding_box__box")
    assert row["target_newton_shape_kind"] == "box"
    assert row["descriptor_contract_passed"] is True
    assert row["descriptor_kind_check_passed"] is True
    assert row["target_kind_check_passed"] is True
    assert row["center_descriptor_check_passed"] is True
    assert row["axes_descriptor_check_passed"] is True
    assert row["half_extents_descriptor_check_passed"] is True
    assert row["source_preflight_check_passed"] is True
    assert row["source_lineage_check_passed"] is True
    assert row["mapping_attempt_count"] == 0
    assert row["newton_mapping_record_count"] == 0
    assert row["newton_shape_object_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    candidate = preflight_row["candidate_primitivespec_dict"]
    assert row["newton_shape_descriptor_dict"] == {
        "descriptor_kind": "newton_shape_descriptor",
        "target_newton_shape_kind": "box",
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": ("paper_single_box__oriented_bounding_box__box"),
        "center": candidate["center"],
        "axes": candidate["axes"],
        "half_extents": candidate["dimensions"]["half_extents"],
        "mapping_contract": "report_scoped_static_descriptor_no_newton_call",
    }
    assert list(_recursive_package_dicts(payload)) == []


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS)
def test_cpd_paper_newton_shape_mapping_contract_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report["paper_mapped_subset_newton_shape_mapping_contract"]

    assert payload[field_name] is False
    assert payload["shape_mapping_rows"][0][field_name] is False


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_mapping_contract_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_mapping_contract_input_next_gate_mismatch",
        ),
        (
            "newton_shape_mapping_preflight_row_count",
            2,
            "newton_shape_mapping_contract_input_count_mismatch:"
            "newton_shape_mapping_preflight_row_count",
        ),
        (
            "mapping_attempt_count",
            1,
            "newton_shape_mapping_contract_input_count_mismatch:mapping_attempt_count",
        ),
        (
            "newton_mapping_record_count",
            1,
            "newton_shape_mapping_contract_input_count_mismatch:newton_mapping_record_count",
        ),
        (
            "newton_runtime_execution_count",
            1,
            "newton_shape_mapping_contract_input_count_mismatch:newton_runtime_execution_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_mapping_contract_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    preflight = _newton_shape_mapping_contract_input()
    preflight[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_contract_payload(preflight)


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_MAPPING_PREFLIGHT_FALSE_FLAGS)
def test_cpd_paper_newton_shape_mapping_contract_rejects_input_forbidden_flags(
    field_name,
):
    preflight = _newton_shape_mapping_contract_input()
    preflight[field_name] = True

    with pytest.raises(
        ValueError,
        match=f"newton_shape_mapping_contract_input_flag_true:{field_name}",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_contract_payload(preflight)


@pytest.mark.parametrize(
    ("mutate_rows", "error_label"),
    [
        (
            lambda rows: [],
            "newton_shape_mapping_contract_row_count_mismatch",
        ),
        (
            lambda rows: [rows[0], json.loads(json.dumps(rows[0]))],
            "newton_shape_mapping_contract_row_count_mismatch",
        ),
    ],
)
def test_cpd_paper_newton_shape_mapping_contract_rejects_row_count_drift(
    mutate_rows,
    error_label,
):
    preflight = _newton_shape_mapping_contract_input()
    preflight["newton_shape_mapping_preflight_rows"] = mutate_rows(
        preflight["newton_shape_mapping_preflight_rows"]
    )

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_contract_payload(preflight)


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "newton_shape_mapping_preflight_row_id",
            "wrong_row",
            "newton_shape_mapping_contract_source_row_mismatch:"
            "newton_shape_mapping_preflight_row_id",
        ),
        (
            "fixture_id",
            "wrong_fixture",
            "newton_shape_mapping_contract_source_row_mismatch:fixture_id",
        ),
        (
            "target_newton_shape_kind",
            "sphere",
            "newton_shape_mapping_contract_source_row_mismatch:target_newton_shape_kind",
        ),
        (
            "newton_shape_mapping_preflight_passed",
            False,
            "newton_shape_mapping_contract_source_row_mismatch:"
            "newton_shape_mapping_preflight_passed",
        ),
    ],
)
def test_cpd_paper_newton_shape_mapping_contract_rejects_source_row_drift(
    field_name,
    bad_value,
    error_label,
):
    preflight = _newton_shape_mapping_contract_input()
    rows = [json.loads(json.dumps(row)) for row in preflight["newton_shape_mapping_preflight_rows"]]
    rows[0][field_name] = bad_value
    preflight["newton_shape_mapping_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_contract_payload(preflight)


def test_cpd_paper_newton_shape_mapping_contract_rejects_source_package_copy(cpd_paper_report):
    preflight = _newton_shape_mapping_contract_input()
    source_package = cpd_paper_report["paper_mapped_subset_collision_package_generation_contract"][
        "collision_package_generation_rows"
    ][0]["generated_collision_package"]
    preflight["unexpected_package_copy"] = json.loads(json.dumps(source_package))

    with pytest.raises(
        ValueError,
        match="newton_shape_mapping_contract_source_package_copy_forbidden",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_contract_payload(preflight)


@pytest.mark.parametrize(
    ("mutate_candidate", "error_label"),
    [
        (
            lambda candidate: {**candidate, "kind": "sphere"},
            "newton_shape_mapping_contract_primitivespec_mismatch:kind",
        ),
        (
            lambda candidate: {**candidate, "center": None},
            "newton_shape_mapping_contract_primitivespec_invalid:center",
        ),
        (
            lambda candidate: {**candidate, "axes": None},
            "newton_shape_mapping_contract_primitivespec_invalid:axes",
        ),
        (
            lambda candidate: {**candidate, "dimensions": {}},
            "newton_shape_mapping_contract_primitivespec_invalid:dimensions",
        ),
        (
            lambda candidate: {
                **candidate,
                "dimensions": {"half_extents": [1.0, 1.0]},
            },
            "newton_shape_mapping_contract_primitivespec_invalid:half_extents",
        ),
    ],
)
def test_cpd_paper_newton_shape_mapping_contract_rejects_primitivespec_drift(
    mutate_candidate,
    error_label,
):
    preflight = _newton_shape_mapping_contract_input()
    rows = [json.loads(json.dumps(row)) for row in preflight["newton_shape_mapping_preflight_rows"]]
    rows[0]["candidate_primitivespec_dict"] = mutate_candidate(
        rows[0]["candidate_primitivespec_dict"]
    )
    preflight["newton_shape_mapping_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_mapping_contract_payload(preflight)


def test_cpd_paper_newton_shape_mapping_contract_static_boundaries():
    source = Path(cpd_paper_offline.__file__).read_text(encoding="utf-8")
    contract_block = source[
        source.index("_NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_FALSE_FLAGS") : source.index(
            "_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_FALSE_FLAGS"
        )
    ]

    forbidden_patterns = [
        "CollisionPackage(",
        "PrimitiveSpec(",
        "FallbackSpec",
        "primitive_collision_compiler.newton",
        "NewtonShapeMapping",
        "map_package_shapes",
        "import newton",
        "import newton_warp",
        "Newton",
        "run_newton",
        "newton.",
        "check_runtime_admissibility",
        "run_runtime_admissibility",
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
        assert pattern not in contract_block
