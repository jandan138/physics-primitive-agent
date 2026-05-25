import pytest

from tests.cpd_paper_offline_shared import *

pytestmark = pytest.mark.paper_offline


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
    )
    assert payload["newton_shape_runtime_engine_builder_boundary_preflight_row_count"] == 1
    assert payload["source_newton_shape_runtime_builder_construction_row_count"] == 1
    assert payload["recording_builder_shape_call_count"] == 1
    assert payload["recorded_builder_call_count"] == 1
    assert payload["repo_local_static_shape_helper_call_count"] == 1
    assert payload["required_before_engine_builder_boundary_count"] == 10
    assert payload["real_newton_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_model_finalized_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert payload["newton_collision_pipeline_created_count"] == 0
    assert payload["newton_collision_pipeline_collide_count"] == 0
    assert (
        payload["remaining_gaps"]
        == EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ]
    construction = report["paper_mapped_subset_newton_shape_runtime_builder_construction_contract"]
    source_row = construction["newton_shape_runtime_builder_construction_rows"][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_boundary_preflight_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_boundary_preflight_complete_environment_probe_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_boundary_preflight_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_boundary_preflight_only_"
        "no_real_newton_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["runtime_engine_builder_boundary_preflight_action"] == (
        "record_real_newton_engine_builder_boundary_requirements_without_importing_newton"
    )
    assert payload["newton_shape_runtime_engine_builder_boundary_preflight_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "next_engine_builder_environment_probe_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
        ),
        "source_builder_construction_rows_required": 1,
        "repo_local_recording_builder_calls_required": 1,
        "required_before_engine_builder_boundary_count": 10,
        "real_newton_import_allowed": False,
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
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "source_newton_shape_runtime_builder_construction_row_id": source_row[
            "newton_shape_runtime_builder_construction_row_id"
        ],
        "source_newton_shape_runtime_builder_preflight_row_id": source_row[
            "source_newton_shape_runtime_builder_preflight_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_recorded_builder_method_name": "add_shape_box",
        "input_recorded_builder_call_count": 1,
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_boundary_preflight_row_count": 1,
        "source_newton_shape_runtime_builder_construction_row_count": 1,
        "recording_builder_shape_call_count": 1,
        "recorded_builder_call_count": 1,
        "repo_local_static_shape_helper_call_count": 1,
        "required_before_engine_builder_boundary_count": 10,
        "real_newton_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_model_finalized_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_runtime_execution_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "target_newton_shape_kind_distribution": {"box": 1},
        "future_builder_method_distribution": {"add_shape_box": 1},
    }


def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_records_one_static_boundary_row(
    cpd_paper_report,
):
    report = cpd_paper_report
    construction_row = report[
        "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
    ]["newton_shape_runtime_builder_construction_rows"][0]
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ]
    rows = payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == (NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS)
    assert row["newton_shape_runtime_engine_builder_boundary_preflight_row_id"] == (
        "newton_shape_runtime_engine_builder_boundary_preflight__paper_single_box__box"
    )
    assert (
        row["source_newton_shape_runtime_builder_construction_row_id"]
        == (construction_row["newton_shape_runtime_builder_construction_row_id"])
    )
    assert (
        row["source_newton_shape_runtime_builder_preflight_row_id"]
        == (construction_row["source_newton_shape_runtime_builder_preflight_row_id"])
    )
    assert row["source_shape_mapping_row_id"] == construction_row["source_shape_mapping_row_id"]
    assert row["source_package_id"] == construction_row["source_package_id"]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["primitive_id"] == ("paper_single_box__oriented_bounding_box__box")
    assert row["target_newton_shape_kind"] == "box"
    assert (
        row["constructed_newton_shape_mapping_dict"]
        == (construction_row["constructed_newton_shape_mapping_dict"])
    )
    assert row["recorded_builder_method_name"] == "add_shape_box"
    assert row["recorded_builder_call"] == construction_row["recorded_builder_call"]
    assert row["recorded_builder_call_count"] == 1
    assert row["recording_builder_kind"] == (
        "repo_local_recording_builder_not_newton_model_builder"
    )
    assert row["recording_builder_shape_call_count"] == 1
    assert row["repo_local_static_shape_helper"] == "_add_static_shape"
    assert row["repo_local_static_shape_helper_called"] is True
    assert row["builder_call_plan"] == construction_row["builder_call_plan"]
    assert row["builder_method_name"] == "add_shape_box"
    assert row["builder_body_argument"] == -1
    assert row["builder_dimension_arguments"] == construction_row["builder_dimension_arguments"]
    assert row["builder_xform_descriptor"] == construction_row["builder_xform_descriptor"]
    assert row["future_newton_builder_constructor_name"] == "newton.ModelBuilder"
    assert row["future_newton_builder_method_name"] == "add_shape_box"
    assert row["future_runtime_module_names"] == ["newton", "warp"]
    assert row["boundary_status"] == "preflight_recorded_not_crossed"
    assert row["boundary_decision"] == (
        "defer_real_engine_builder_boundary_to_environment_probe_gate"
    )
    assert row["blocked_until_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
    )
    assert row["required_before_engine_builder_boundary"] == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_REQUIRED_CHECKS
    )
    assert row["required_before_engine_builder_boundary_count"] == 10
    assert row["real_newton_import_count"] == 0
    assert row["newton_model_builder_instantiated_count"] == 0
    assert row["newton_model_finalized_count"] == 0
    assert row["newton_engine_shape_object_count"] == 0
    assert row["newton_builder_shape_call_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    assert row["newton_collision_pipeline_created_count"] == 0
    assert row["newton_collision_pipeline_collide_count"] == 0
    assert list(_recursive_package_dicts(payload)) == []
    json.dumps(row)
    assert _contains_callable(row) is False


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ]

    assert payload[field_name] is False
    assert (
        payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"][0][field_name]
        is False
    )


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_TRUE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_record_flags_are_true(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ]

    assert payload[field_name] is True
    assert (
        payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"][0][field_name]
        is True
    )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_runtime_engine_builder_boundary_preflight_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_runtime_engine_builder_boundary_preflight_input_next_gate_mismatch",
        ),
        (
            "newton_shape_runtime_builder_construction_row_count",
            2,
            "newton_shape_runtime_engine_builder_boundary_preflight_input_count_mismatch:"
            "newton_shape_runtime_builder_construction_row_count",
        ),
        (
            "recorded_builder_call_count",
            2,
            "newton_shape_runtime_engine_builder_boundary_preflight_input_count_mismatch:"
            "recorded_builder_call_count",
        ),
        (
            "newton_builder_shape_call_count",
            1,
            "newton_shape_runtime_engine_builder_boundary_preflight_input_count_mismatch:"
            "newton_builder_shape_call_count",
        ),
        (
            "newton_engine_shape_object_count",
            1,
            "newton_shape_runtime_engine_builder_boundary_preflight_input_count_mismatch:"
            "newton_engine_shape_object_count",
        ),
        (
            "real_newton_import_count",
            1,
            "newton_shape_runtime_engine_builder_boundary_preflight_input_count_mismatch:"
            "real_newton_import_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_engine_builder_boundary_preflight_input()
    payload[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize("field_name", NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_TRUE_FLAGS)
@pytest.mark.parametrize("scope", ("payload", "row"))
@pytest.mark.parametrize(
    ("mutation", "error_suffix"),
    [
        ("missing", "missing"),
        ("false", "false"),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_rejects_input_true_flag_drift(
    field_name,
    scope,
    mutation,
    error_suffix,
):
    payload = _newton_shape_runtime_engine_builder_boundary_preflight_input()
    target = payload
    if scope == "row":
        rows = [
            json.loads(json.dumps(row))
            for row in payload["newton_shape_runtime_builder_construction_rows"]
        ]
        target = rows[0]
        payload["newton_shape_runtime_builder_construction_rows"] = rows
    if mutation == "missing":
        target.pop(field_name)
    else:
        target[field_name] = False

    with pytest.raises(
        ValueError,
        match=(
            "newton_shape_runtime_engine_builder_boundary_preflight_input_flag_"
            f"{error_suffix}:{field_name}"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize("case", ("empty", "not_rows", "non_dict_row", "two_rows"))
def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_rejects_row_list_drift(
    case,
):
    payload = _newton_shape_runtime_engine_builder_boundary_preflight_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_builder_construction_rows"]
    ]
    if case == "empty":
        payload["newton_shape_runtime_builder_construction_rows"] = []
    elif case == "not_rows":
        payload["newton_shape_runtime_builder_construction_rows"] = "not_rows"
    elif case == "non_dict_row":
        payload["newton_shape_runtime_builder_construction_rows"] = [None]
    else:
        payload["newton_shape_runtime_builder_construction_rows"] = rows + rows

    with pytest.raises(
        ValueError,
        match="newton_shape_runtime_engine_builder_boundary_preflight_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_FALSE_FLAGS,
)
@pytest.mark.parametrize("scope", ("payload", "row"))
def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_rejects_input_flags(
    field_name,
    scope,
):
    payload = _newton_shape_runtime_engine_builder_boundary_preflight_input()
    if scope == "payload":
        payload[field_name] = True
    else:
        rows = [
            json.loads(json.dumps(row))
            for row in payload["newton_shape_runtime_builder_construction_rows"]
        ]
        rows[0][field_name] = True
        payload["newton_shape_runtime_builder_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            f"newton_shape_runtime_engine_builder_boundary_preflight_input_flag_true:{field_name}"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("newton_shape_runtime_builder_construction_row_id", "wrong_row"),
        ("source_newton_shape_runtime_builder_preflight_row_id", "wrong_row"),
        ("source_newton_shape_mapping_preflight_row_id", "wrong_mapping_preflight"),
        ("source_runtime_admissibility_row_id", "wrong_runtime_admissibility"),
        ("source_shape_mapping_row_id", "wrong_mapping_row"),
        ("source_package_id", "wrong_package"),
        ("source_asset_id", "wrong_asset"),
        ("fixture_id", "wrong_fixture"),
        ("paper_primitive", "sphere"),
        ("primitive_spec_kind", "sphere"),
        ("primitive_id", "wrong_primitive"),
        ("target_newton_shape_kind", "sphere"),
        ("recorded_builder_method_name", "add_shape_sphere"),
        ("recorded_builder_call_count", 2),
        ("recording_builder_shape_call_count", 2),
        ("newton_builder_shape_call_count", 1),
        ("newton_engine_shape_object_count", 1),
        ("newton_runtime_execution_count", 1),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_rejects_source_row_drift(
    field_name,
    bad_value,
):
    payload = _newton_shape_runtime_engine_builder_boundary_preflight_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_builder_construction_rows"]
    ]
    rows[0][field_name] = bad_value
    payload["newton_shape_runtime_builder_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "newton_shape_runtime_engine_builder_boundary_preflight_source_row_mismatch:"
            f"{field_name}"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_rejects_malformed_builder_dimensions():
    payload = _newton_shape_runtime_engine_builder_boundary_preflight_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_builder_construction_rows"]
    ]
    rows[0]["builder_dimension_arguments"] = ["hx", "hy", "hz"]
    payload["newton_shape_runtime_builder_construction_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "newton_shape_runtime_engine_builder_boundary_preflight_source_row_mismatch:"
            "builder_dimension_arguments"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_boundary_preflight_static_boundary_is_plan_only():
    helpers = (
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_boundary_preflight_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_boundary_preflight_row,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        'importlib.import_module("newton")',
        'importlib.import_module("warp")',
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
        "_import_newton_runtime",
        "inspect_newton_environment",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
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


def test_newton_warp_provenance_helper_records_specs_without_importing_modules(
    tmp_path, monkeypatch
):
    source_dir = tmp_path / "newton-source"
    (source_dir / "newton").mkdir(parents=True)
    (source_dir / "warp").mkdir()
    (source_dir / "newton" / "__init__.py").write_text("__version__ = 'fake'\n")
    (source_dir / "warp" / "__init__.py").write_text("__version__ = 'fake'\n")
    cached_newton = types.ModuleType("newton")
    cached_warp = types.ModuleType("warp")
    monkeypatch.setitem(sys.modules, "newton", cached_newton)
    monkeypatch.setitem(sys.modules, "warp", cached_warp)

    probe = newton_env.inspect_newton_warp_provenance(source_dir)

    assert probe["probe_mode"] == "find_spec_provenance_only"
    assert probe["source_dir_configured"] is True
    assert probe["source_dir"] == str(source_dir)
    assert probe["source_dir_resolved"] == str(source_dir.resolve())
    assert probe["source_dir_status"] == "found"
    assert probe["runtime_module_import_isolation_checked"] is True
    assert probe["sys_path_restored"] is True
    assert probe["cached_runtime_modules_restored"] is True
    assert sys.modules["newton"] is cached_newton
    assert sys.modules["warp"] is cached_warp
    rows = {row["module_name"]: row for row in probe["module_probe_rows"]}
    assert set(rows) == {"newton", "warp"}
    for module_name, row in rows.items():
        assert row["module_available"] is True
        assert row["provenance_status"] == "found_within_source_dir"
        assert row["resolved_within_source_dir"] is True
        assert row["module_origin_resolved"].endswith(f"/{module_name}/__init__.py")
        assert row["module_search_locations_resolved"] == [
            str((source_dir / module_name).resolve())
        ]
        assert row["import_attempted"] is False
    json.dumps(probe)


def test_newton_warp_provenance_helper_records_unconfigured_source_without_lookup():
    probe = newton_env.inspect_newton_warp_provenance(None)

    assert probe["probe_mode"] == "find_spec_provenance_only"
    assert probe["source_dir_configured"] is False
    assert probe["source_dir"] is None
    assert probe["source_dir_resolved"] is None
    assert probe["source_dir_status"] == "not_configured"
    assert probe["runtime_module_import_isolation_checked"] is True
    assert probe["sys_path_restored"] is True
    assert probe["cached_runtime_modules_restored"] is True
    assert [row["module_name"] for row in probe["module_probe_rows"]] == [
        "newton",
        "warp",
    ]
    for row in probe["module_probe_rows"]:
        assert row["module_available"] is False
        assert row["module_origin"] is None
        assert row["provenance_status"] == "not_run_source_dir_not_configured"
        assert row["import_attempted"] is False


def test_newton_engine_builder_api_surface_helper_records_unconfigured_source_without_import():
    probe = newton_env.inspect_newton_engine_builder_api_surface(None)

    assert probe["probe_mode"] == "source_ast_api_surface_only_no_import"
    assert probe["api_surface_status"] == "not_run_source_dir_not_configured"
    assert probe["source_dir_configured"] is False
    assert probe["source_dir"] is None
    assert probe["source_dir_resolved"] is None
    assert probe["source_dir_status"] == "not_configured"
    assert probe["source_files_checked"] == []
    assert probe["model_builder_exported_from_newton_init"] is False
    assert probe["model_builder_class_found"] is False
    assert probe["add_shape_box_found"] is False
    assert probe["finalize_method_found"] is False
    assert probe["collision_pipeline_exported_from_newton_init"] is False
    assert probe["real_newton_import_count"] == 0
    assert probe["real_warp_import_count"] == 0
    assert probe["newton_model_builder_instantiated_count"] == 0
    assert probe["newton_builder_shape_call_count"] == 0
    assert probe["newton_model_finalized_count"] == 0
    assert probe["newton_runtime_execution_count"] == 0
    assert probe["import_attempted"] is False
    json.dumps(probe)


def test_newton_engine_builder_api_surface_helper_reads_source_ast_without_importing_modules(
    tmp_path, monkeypatch
):
    source_dir = tmp_path / "newton-source"
    newton_pkg = source_dir / "newton"
    sim_dir = newton_pkg / "_src" / "sim"
    sim_dir.mkdir(parents=True)
    (newton_pkg / "__init__.py").write_text(
        "from ._src.sim import CollisionPipeline, ModelBuilder\n"
        "__all__ = ['CollisionPipeline', 'ModelBuilder']\n"
    )
    (sim_dir / "builder.py").write_text(
        "class ModelBuilder:\n"
        "    def __init__(self, up_axis='Z', gravity=-9.81):\n"
        "        pass\n"
        "    def add_shape_box(self, body, xform=None, hx=0.5, hy=0.5, hz=0.5, cfg=None):\n"
        "        return 1\n"
        "    def finalize(self, device=None):\n"
        "        return object()\n"
    )
    cached_newton = types.ModuleType("newton")
    cached_warp = types.ModuleType("warp")
    monkeypatch.setitem(sys.modules, "newton", cached_newton)
    monkeypatch.setitem(sys.modules, "warp", cached_warp)
    monkeypatch.setattr(
        newton_env,
        "_git_commit",
        lambda source_path: (_ for _ in ()).throw(
            AssertionError("api surface helper must stay source-AST only")
        ),
    )

    probe = newton_env.inspect_newton_engine_builder_api_surface(source_dir)

    assert probe["probe_mode"] == "source_ast_api_surface_only_no_import"
    assert probe["api_surface_status"] == "source_api_surface_checked"
    assert probe["source_dir_configured"] is True
    assert probe["source_commit"] is None
    assert probe["source_dir_status"] == "found"
    assert probe["source_files_checked"] == [
        "newton/__init__.py",
        "newton/_src/sim/builder.py",
    ]
    assert probe["model_builder_exported_from_newton_init"] is True
    assert probe["collision_pipeline_exported_from_newton_init"] is True
    assert probe["model_builder_class_found"] is True
    assert probe["model_builder_class_file"] == "newton/_src/sim/builder.py"
    assert probe["model_builder_constructor_signature"]["parameters"] == [
        "self",
        "up_axis",
        "gravity",
    ]
    assert probe["add_shape_box_found"] is True
    assert probe["add_shape_box_signature"]["parameters"] == [
        "self",
        "body",
        "xform",
        "hx",
        "hy",
        "hz",
        "cfg",
    ]
    assert probe["add_shape_box_signature"]["planned_call_fields_present"] == [
        "body",
        "xform",
        "hx",
        "hy",
        "hz",
    ]
    assert probe["finalize_method_found"] is True
    assert probe["import_attempted"] is False
    assert probe["real_newton_import_count"] == 0
    assert probe["real_warp_import_count"] == 0
    assert probe["newton_model_builder_instantiated_count"] == 0
    assert probe["newton_builder_shape_call_count"] == 0
    assert probe["newton_model_finalized_count"] == 0
    assert probe["newton_runtime_execution_count"] == 0
    assert sys.modules["newton"] is cached_newton
    assert sys.modules["warp"] is cached_warp
    json.dumps(probe)


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
    )
    assert payload["newton_shape_runtime_engine_builder_environment_probe_row_count"] == 1
    assert payload["source_newton_shape_runtime_engine_builder_boundary_preflight_row_count"] == 1
    assert payload["module_probe_row_count"] == 2
    assert payload["source_dir_configured_count"] == 0
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert (
        payload["remaining_gaps"]
        == EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ]
    boundary = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ]
    source_row = boundary["newton_shape_runtime_engine_builder_boundary_preflight_rows"][0]

    assert set(payload) == (
        NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_PAYLOAD_REQUIRED_KEYS
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_environment_probe_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_environment_probe_complete_api_surface_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_environment_probe_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_environment_probe_only_"
        "no_model_builder_no_shape_call_no_finalize_no_collision_pipeline_no_runtime"
    )
    assert payload["environment_probe_action"] == (
        "record_newton_warp_find_spec_provenance_without_importing_runtime_modules"
    )
    assert payload["environment_probe_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
        ),
        "next_engine_builder_api_surface_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
        ),
        "source_boundary_preflight_rows_required": 1,
        "runtime_module_names_required": ["newton", "warp"],
        "probe_method": "importlib_util_find_spec_without_import_module",
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
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id": source_row[
            "newton_shape_runtime_engine_builder_boundary_preflight_row_id"
        ],
        "source_newton_shape_runtime_builder_construction_row_id": source_row[
            "source_newton_shape_runtime_builder_construction_row_id"
        ],
        "source_shape_mapping_row_id": source_row["source_shape_mapping_row_id"],
        "source_package_id": source_row["source_package_id"],
        "source_fixture_id": "paper_single_box",
        "source_primitive_id": source_row["primitive_id"],
        "source_target_newton_shape_kind": "box",
        "source_future_runtime_module_names": ["newton", "warp"],
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_environment_probe_row_count": 1,
        "source_newton_shape_runtime_engine_builder_boundary_preflight_row_count": 1,
        "module_probe_row_count": 2,
        "source_dir_configured_count": 0,
        "newton_module_available_count": 0,
        "warp_module_available_count": 0,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_model_finalized_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_runtime_execution_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "target_newton_shape_kind_distribution": {"box": 1},
        "environment_probe_status_distribution": {"not_run_source_dir_not_configured": 1},
    }


def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_records_one_provenance_row(
    cpd_paper_report,
):
    report = cpd_paper_report
    source_row = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
    ]["newton_shape_runtime_engine_builder_boundary_preflight_rows"][0]
    payload = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ]
    rows = payload["newton_shape_runtime_engine_builder_environment_probe_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == (NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_ROW_REQUIRED_KEYS)
    assert row["newton_shape_runtime_engine_builder_environment_probe_row_id"] == (
        "newton_shape_runtime_engine_builder_environment_probe__paper_single_box__box"
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"]
        == source_row["newton_shape_runtime_engine_builder_boundary_preflight_row_id"]
    )
    assert (
        row["source_newton_shape_runtime_builder_construction_row_id"]
        == (source_row["source_newton_shape_runtime_builder_construction_row_id"])
    )
    assert row["source_shape_mapping_row_id"] == source_row["source_shape_mapping_row_id"]
    assert row["source_package_id"] == source_row["source_package_id"]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["primitive_id"] == ("paper_single_box__oriented_bounding_box__box")
    assert row["target_newton_shape_kind"] == "box"
    assert row["future_newton_builder_constructor_name"] == "newton.ModelBuilder"
    assert row["future_newton_builder_method_name"] == "add_shape_box"
    assert row["future_runtime_module_names"] == ["newton", "warp"]
    assert row["environment_probe_status"] == "not_run_source_dir_not_configured"
    assert row["environment_probe_mode"] == "find_spec_provenance_only"
    assert row["environment_probe_claim_boundary"] == (
        "bounded_environment_provenance_probe_only_not_newton_runtime_execution"
    )
    assert row["newton_source_dir_config_key"] == "newton.source_dir"
    assert row["newton_source_dir_configured"] is False
    assert row["newton_source_dir"] is None
    assert row["newton_source_dir_resolved"] is None
    assert row["newton_source_dir_status"] == "not_configured"
    assert row["module_probe_row_count"] == 2
    assert row["newton_module_name"] == "newton"
    assert row["newton_module_available"] is False
    assert row["newton_module_origin"] is None
    assert row["newton_module_origin_resolved"] is None
    assert row["newton_module_provenance_status"] == ("not_run_source_dir_not_configured")
    assert row["warp_module_name"] == "warp"
    assert row["warp_module_available"] is False
    assert row["warp_module_origin"] is None
    assert row["warp_module_origin_resolved"] is None
    assert row["warp_module_provenance_status"] == ("not_run_source_dir_not_configured")
    assert row["module_probe_rows"] == [
        {
            "module_name": "newton",
            "module_available": False,
            "module_origin": None,
            "module_origin_resolved": None,
            "module_search_locations": [],
            "module_search_locations_resolved": [],
            "provenance_status": "not_run_source_dir_not_configured",
            "provenance_detail": "newton.source_dir not configured for offline report",
            "resolved_within_source_dir": False,
            "import_attempted": False,
        },
        {
            "module_name": "warp",
            "module_available": False,
            "module_origin": None,
            "module_origin_resolved": None,
            "module_search_locations": [],
            "module_search_locations_resolved": [],
            "provenance_status": "not_run_source_dir_not_configured",
            "provenance_detail": "newton.source_dir not configured for offline report",
            "resolved_within_source_dir": False,
            "import_attempted": False,
        },
    ]
    assert row["sys_path_restored"] is True
    assert row["cached_runtime_modules_restored"] is True
    assert row["runtime_module_import_isolation_checked"] is True
    assert row["real_newton_import_count"] == 0
    assert row["real_warp_import_count"] == 0
    assert row["newton_model_builder_instantiated_count"] == 0
    assert row["newton_builder_shape_call_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    assert list(_recursive_package_dicts(payload)) == []
    json.dumps(row)
    assert _contains_callable(row) is False


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_FALSE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ]

    assert payload[field_name] is False
    assert (
        payload["newton_shape_runtime_engine_builder_environment_probe_rows"][0][field_name]
        is False
    )


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_TRUE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_record_flags_are_true(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ]

    assert payload[field_name] is True
    assert (
        payload["newton_shape_runtime_engine_builder_environment_probe_rows"][0][field_name] is True
    )


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_runtime_engine_builder_environment_probe_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_runtime_engine_builder_environment_probe_input_next_gate_mismatch",
        ),
        (
            "newton_shape_runtime_engine_builder_boundary_preflight_row_count",
            2,
            "newton_shape_runtime_engine_builder_environment_probe_input_count_mismatch:"
            "newton_shape_runtime_engine_builder_boundary_preflight_row_count",
        ),
        (
            "recorded_builder_call_count",
            2,
            "newton_shape_runtime_engine_builder_environment_probe_input_count_mismatch:"
            "recorded_builder_call_count",
        ),
        (
            "newton_builder_shape_call_count",
            1,
            "newton_shape_runtime_engine_builder_environment_probe_input_count_mismatch:"
            "newton_builder_shape_call_count",
        ),
        (
            "newton_engine_shape_object_count",
            1,
            "newton_shape_runtime_engine_builder_environment_probe_input_count_mismatch:"
            "newton_engine_shape_object_count",
        ),
        (
            "real_newton_import_count",
            1,
            "newton_shape_runtime_engine_builder_environment_probe_input_count_mismatch:"
            "real_newton_import_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_engine_builder_environment_probe_input()
    payload[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_TRUE_FLAGS,
)
@pytest.mark.parametrize("scope", ("payload", "row"))
@pytest.mark.parametrize(
    ("mutation", "error_suffix"),
    [
        ("missing", "missing"),
        ("false", "false"),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_rejects_input_true_flag_drift(
    field_name,
    scope,
    mutation,
    error_suffix,
):
    payload = _newton_shape_runtime_engine_builder_environment_probe_input()
    target = payload
    if scope == "row":
        rows = [
            json.loads(json.dumps(row))
            for row in payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"]
        ]
        target = rows[0]
        payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"] = rows
    if mutation == "missing":
        target.pop(field_name)
    else:
        target[field_name] = False

    with pytest.raises(
        ValueError,
        match=(
            "newton_shape_runtime_engine_builder_environment_probe_input_flag_"
            f"{error_suffix}:{field_name}"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_payload(
            payload
        )


@pytest.mark.parametrize("case", ("empty", "not_rows", "non_dict_row", "two_rows"))
def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_rejects_row_list_drift(
    case,
):
    payload = _newton_shape_runtime_engine_builder_environment_probe_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"]
    ]
    if case == "empty":
        payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"] = []
    elif case == "not_rows":
        payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"] = "not_rows"
    elif case == "non_dict_row":
        payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"] = [None]
    else:
        payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"] = rows + rows

    with pytest.raises(
        ValueError,
        match="newton_shape_runtime_engine_builder_environment_probe_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
)
@pytest.mark.parametrize("scope", ("payload", "row"))
def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_rejects_input_flags(
    field_name,
    scope,
):
    payload = _newton_shape_runtime_engine_builder_environment_probe_input()
    if scope == "payload":
        payload[field_name] = True
    else:
        rows = [
            json.loads(json.dumps(row))
            for row in payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"]
        ]
        rows[0][field_name] = True
        payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            f"newton_shape_runtime_engine_builder_environment_probe_input_flag_true:{field_name}"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        (
            "newton_shape_runtime_engine_builder_boundary_preflight_row_id",
            "wrong_row",
        ),
        ("source_newton_shape_runtime_builder_construction_row_id", "wrong_row"),
        ("source_newton_shape_mapping_preflight_row_id", "wrong_mapping_preflight"),
        ("source_runtime_admissibility_row_id", "wrong_runtime_admissibility"),
        ("source_shape_mapping_row_id", "wrong_mapping_row"),
        ("source_package_id", "wrong_package"),
        ("source_asset_id", "wrong_asset"),
        ("fixture_id", "wrong_fixture"),
        ("paper_primitive", "sphere"),
        ("primitive_spec_kind", "sphere"),
        ("primitive_id", "wrong_primitive"),
        ("target_newton_shape_kind", "sphere"),
        ("future_newton_builder_constructor_name", "wrong.Builder"),
        ("future_newton_builder_method_name", "add_shape_sphere"),
        ("future_runtime_module_names", ["newton"]),
        ("newton_builder_shape_call_count", 1),
        ("newton_engine_shape_object_count", 1),
        ("newton_runtime_execution_count", 1),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_rejects_source_row_drift(
    field_name,
    bad_value,
):
    payload = _newton_shape_runtime_engine_builder_environment_probe_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"]
    ]
    rows[0][field_name] = bad_value
    payload["newton_shape_runtime_engine_builder_boundary_preflight_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "newton_shape_runtime_engine_builder_environment_probe_source_row_mismatch:"
            f"{field_name}"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_environment_probe_static_boundary_is_environment_only():
    helpers = (
        newton_env.inspect_newton_warp_provenance,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_environment_probe_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_environment_probe_row,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        'importlib.import_module("newton")',
        'importlib.import_module("warp")',
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
        "_import_newton_runtime",
        "inspect_newton_environment",
        "run_newton_contact_smoke",
        "run_newton_drop_settle",
        "run_newton_sphere_rain",
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


def test_cpd_paper_records_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract_gate(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]

    assert report["next_required_gate"] == EXPECTED_CURRENT_REPORT_NEXT_GATE
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert report["paper_faithfulness"]["runtime_lane_remaining_gates"] == (
        EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert payload["gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
    )
    assert payload["input_gate_id"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
    )
    assert payload["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
    )
    assert payload["newton_shape_runtime_engine_builder_api_surface_row_count"] == 1
    assert payload["source_newton_shape_runtime_engine_builder_environment_probe_row_count"] == 1
    assert payload["api_surface_probe_count"] == 1
    assert payload["source_dir_configured_count"] == 0
    assert payload["newton_model_builder_symbol_found_count"] == 0
    assert payload["newton_add_shape_box_symbol_found_count"] == 0
    assert payload["real_newton_import_count"] == 0
    assert payload["real_warp_import_count"] == 0
    assert payload["newton_model_builder_instantiated_count"] == 0
    assert payload["newton_engine_shape_object_count"] == 0
    assert payload["newton_builder_shape_call_count"] == 0
    assert payload["newton_runtime_execution_count"] == 0
    assert (
        payload["remaining_gaps"]
        == EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_REMAINING_GAPS
    )


def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_payload_schema_is_exact(
    cpd_paper_report,
):
    report = cpd_paper_report
    payload = report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
    environment = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ]
    source_row = environment["newton_shape_runtime_engine_builder_environment_probe_rows"][0]

    assert set(payload) == (NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_PAYLOAD_REQUIRED_KEYS)
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["gate_status"] == (
        "implemented_single_fixture_newton_engine_builder_api_surface_only_partial"
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "newton_engine_builder_source_api_surface_recorded_engine_builder_entry_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "newton_engine_builder_api_surface_record_not_runtime_execution"
    )
    assert payload["implementation_boundary"] == (
        "single_synthetic_box_engine_builder_api_surface_only_"
        "source_ast_no_import_no_model_builder_no_shape_call_no_finalize_no_runtime"
    )
    assert payload["api_surface_action"] == (
        "record_newton_source_ast_api_surface_without_importing_runtime_modules"
    )
    assert payload["api_surface_contract"] == {
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
        ),
        "closed_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
        ),
        "next_engine_builder_entry_gate_required": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT
        ),
        "source_environment_probe_rows_required": 1,
        "probe_method": "source_ast_only_no_import",
        "source_files_expected": [
            "newton/__init__.py",
            "newton/_src/sim/builder.py",
        ],
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
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT
        ),
        "input_next_required_gate": (
            EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT
        ),
        "source_newton_shape_runtime_engine_builder_environment_probe_row_id": source_row[
            "newton_shape_runtime_engine_builder_environment_probe_row_id"
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
        "source_environment_probe_status": "not_run_source_dir_not_configured",
    }
    assert payload["coverage_summary"] == {
        "newton_shape_runtime_engine_builder_api_surface_row_count": 1,
        "source_newton_shape_runtime_engine_builder_environment_probe_row_count": 1,
        "api_surface_probe_count": 1,
        "module_probe_row_count": 2,
        "source_dir_configured_count": 0,
        "newton_module_available_count": 0,
        "warp_module_available_count": 0,
        "newton_model_builder_symbol_found_count": 0,
        "newton_add_shape_box_symbol_found_count": 0,
        "newton_model_finalize_symbol_found_count": 0,
        "collision_pipeline_symbol_found_count": 0,
        "real_newton_import_count": 0,
        "real_warp_import_count": 0,
        "newton_model_builder_instantiated_count": 0,
        "newton_model_finalized_count": 0,
        "newton_engine_shape_object_count": 0,
        "newton_builder_shape_call_count": 0,
        "newton_runtime_execution_count": 0,
        "newton_collision_pipeline_created_count": 0,
        "newton_collision_pipeline_collide_count": 0,
        "fixture_id_distribution": {"paper_single_box": 1},
        "target_newton_shape_kind_distribution": {"box": 1},
        "api_surface_status_distribution": {"not_run_source_dir_not_configured": 1},
    }


def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_records_one_source_ast_row(
    cpd_paper_report,
):
    report = cpd_paper_report
    source_row = report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
    ]["newton_shape_runtime_engine_builder_environment_probe_rows"][0]
    payload = report["paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"]
    rows = payload["newton_shape_runtime_engine_builder_api_surface_rows"]

    assert len(rows) == 1
    row = rows[0]
    assert set(row) == (NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_ROW_REQUIRED_KEYS)
    assert row["newton_shape_runtime_engine_builder_api_surface_row_id"] == (
        "newton_shape_runtime_engine_builder_api_surface__paper_single_box__box"
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_environment_probe_row_id"]
        == source_row["newton_shape_runtime_engine_builder_environment_probe_row_id"]
    )
    assert (
        row["source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"]
        == source_row["source_newton_shape_runtime_engine_builder_boundary_preflight_row_id"]
    )
    assert row["source_shape_mapping_row_id"] == source_row["source_shape_mapping_row_id"]
    assert row["source_package_id"] == source_row["source_package_id"]
    assert row["fixture_id"] == "paper_single_box"
    assert row["paper_primitive"] == "oriented_bounding_box"
    assert row["primitive_spec_kind"] == "box"
    assert row["target_newton_shape_kind"] == "box"
    assert row["future_newton_builder_constructor_name"] == "newton.ModelBuilder"
    assert row["future_newton_builder_method_name"] == "add_shape_box"
    assert row["future_runtime_module_names"] == ["newton", "warp"]
    assert row["environment_probe_status"] == "not_run_source_dir_not_configured"
    assert row["newton_source_dir_configured"] is False
    assert row["newton_source_dir_status"] == "not_configured"
    assert row["module_probe_row_count"] == 2
    assert row["newton_module_available"] is False
    assert row["newton_module_provenance_status"] == ("not_run_source_dir_not_configured")
    assert row["warp_module_available"] is False
    assert row["warp_module_provenance_status"] == ("not_run_source_dir_not_configured")
    assert row["api_surface_probe_status"] == "not_run_source_dir_not_configured"
    assert row["api_surface_probe_mode"] == "source_ast_api_surface_only_no_import"
    assert row["api_surface_claim_boundary"] == (
        "bounded_source_api_surface_probe_only_not_newton_runtime_execution"
    )
    assert row["source_files_checked"] == []
    assert row["source_file_rows"] == []
    assert row["model_builder_exported_from_newton_init"] is False
    assert row["collision_pipeline_exported_from_newton_init"] is False
    assert row["model_builder_class_found"] is False
    assert row["model_builder_class_file"] is None
    assert row["model_builder_constructor_found"] is False
    assert row["model_builder_constructor_signature"] == {
        "parameters": [],
        "required_parameters": [],
        "defaults": {},
    }
    assert row["add_shape_box_found"] is False
    assert row["add_shape_box_signature"] == {
        "parameters": [],
        "required_parameters": [],
        "planned_call_fields_present": [],
        "defaults": {},
    }
    assert row["planned_builder_call_fields_present"] == []
    assert row["finalize_method_found"] is False
    assert row["collision_pipeline_symbol_found"] is False
    assert row["import_attempted"] is False
    assert row["real_newton_import_count"] == 0
    assert row["real_warp_import_count"] == 0
    assert row["newton_model_builder_instantiated_count"] == 0
    assert row["newton_builder_shape_call_count"] == 0
    assert row["newton_runtime_execution_count"] == 0
    assert list(_recursive_package_dicts(payload)) == []
    json.dumps(row)
    assert _contains_callable(row) is False


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_FALSE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_boundary_flags_stay_false(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
    ]

    assert payload[field_name] is False
    assert payload["newton_shape_runtime_engine_builder_api_surface_rows"][0][field_name] is False


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_TRUE_FLAGS,
)
def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_record_flags_are_true(
    field_name,
    cpd_paper_report,
):
    payload = cpd_paper_report[
        "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
    ]

    assert payload[field_name] is True
    assert payload["newton_shape_runtime_engine_builder_api_surface_rows"][0][field_name] is True


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_label"),
    [
        (
            "gate_id",
            "stale_gate",
            "newton_shape_runtime_engine_builder_api_surface_input_gate_id_mismatch",
        ),
        (
            "next_required_gate",
            "stale_gate",
            "newton_shape_runtime_engine_builder_api_surface_input_next_gate_mismatch",
        ),
        (
            "newton_shape_runtime_engine_builder_environment_probe_row_count",
            2,
            "newton_shape_runtime_engine_builder_api_surface_input_count_mismatch:"
            "newton_shape_runtime_engine_builder_environment_probe_row_count",
        ),
        (
            "newton_builder_shape_call_count",
            1,
            "newton_shape_runtime_engine_builder_api_surface_input_count_mismatch:"
            "newton_builder_shape_call_count",
        ),
        (
            "real_newton_import_count",
            1,
            "newton_shape_runtime_engine_builder_api_surface_input_count_mismatch:"
            "real_newton_import_count",
        ),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_rejects_input_drift(
    field_name,
    bad_value,
    error_label,
):
    payload = _newton_shape_runtime_engine_builder_api_surface_input()
    payload[field_name] = bad_value

    with pytest.raises(ValueError, match=error_label):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_TRUE_FLAGS,
)
@pytest.mark.parametrize("scope", ("payload", "row"))
@pytest.mark.parametrize(
    ("mutation", "error_suffix"),
    [
        ("missing", "missing"),
        ("false", "false"),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_rejects_input_true_flag_drift(
    field_name,
    scope,
    mutation,
    error_suffix,
):
    payload = _newton_shape_runtime_engine_builder_api_surface_input()
    target = payload
    if scope == "row":
        rows = [
            json.loads(json.dumps(row))
            for row in payload["newton_shape_runtime_engine_builder_environment_probe_rows"]
        ]
        target = rows[0]
        payload["newton_shape_runtime_engine_builder_environment_probe_rows"] = rows
    if mutation == "missing":
        target.pop(field_name)
    else:
        target[field_name] = False

    with pytest.raises(
        ValueError,
        match=(
            "newton_shape_runtime_engine_builder_api_surface_input_flag_"
            f"{error_suffix}:{field_name}"
        ),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract_payload(
            payload
        )


@pytest.mark.parametrize("case", ("empty", "not_rows", "non_dict_row", "two_rows"))
def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_rejects_row_list_drift(
    case,
):
    payload = _newton_shape_runtime_engine_builder_api_surface_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_engine_builder_environment_probe_rows"]
    ]
    if case == "empty":
        payload["newton_shape_runtime_engine_builder_environment_probe_rows"] = []
    elif case == "not_rows":
        payload["newton_shape_runtime_engine_builder_environment_probe_rows"] = "not_rows"
    elif case == "non_dict_row":
        payload["newton_shape_runtime_engine_builder_environment_probe_rows"] = [None]
    else:
        payload["newton_shape_runtime_engine_builder_environment_probe_rows"] = rows + rows

    with pytest.raises(
        ValueError,
        match="newton_shape_runtime_engine_builder_api_surface_row_count_mismatch",
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    "field_name",
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_FALSE_FLAGS,
)
@pytest.mark.parametrize("scope", ("payload", "row"))
def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_rejects_input_flags(
    field_name,
    scope,
):
    payload = _newton_shape_runtime_engine_builder_api_surface_input()
    if scope == "payload":
        payload[field_name] = True
    else:
        rows = [
            json.loads(json.dumps(row))
            for row in payload["newton_shape_runtime_engine_builder_environment_probe_rows"]
        ]
        rows[0][field_name] = True
        payload["newton_shape_runtime_engine_builder_environment_probe_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(f"newton_shape_runtime_engine_builder_api_surface_input_flag_true:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract_payload(
            payload
        )


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        (
            "newton_shape_runtime_engine_builder_environment_probe_row_id",
            "wrong_row",
        ),
        (
            "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
            "wrong_row",
        ),
        ("source_newton_shape_mapping_preflight_row_id", "wrong_mapping_preflight"),
        ("source_runtime_admissibility_row_id", "wrong_runtime_admissibility"),
        ("source_shape_mapping_row_id", "wrong_mapping_row"),
        ("source_package_id", "wrong_package"),
        ("source_asset_id", "wrong_asset"),
        ("fixture_id", "wrong_fixture"),
        ("paper_primitive", "sphere"),
        ("primitive_spec_kind", "sphere"),
        ("primitive_id", "wrong_primitive"),
        ("target_newton_shape_kind", "sphere"),
        ("future_newton_builder_constructor_name", "wrong.Builder"),
        ("future_newton_builder_method_name", "add_shape_sphere"),
        ("future_runtime_module_names", ["newton"]),
        ("newton_builder_shape_call_count", 1),
        ("newton_engine_shape_object_count", 1),
        ("newton_runtime_execution_count", 1),
    ],
)
def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_rejects_source_row_drift(
    field_name,
    bad_value,
):
    payload = _newton_shape_runtime_engine_builder_api_surface_input()
    rows = [
        json.loads(json.dumps(row))
        for row in payload["newton_shape_runtime_engine_builder_environment_probe_rows"]
    ]
    rows[0][field_name] = bad_value
    payload["newton_shape_runtime_engine_builder_environment_probe_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(f"newton_shape_runtime_engine_builder_api_surface_source_row_mismatch:{field_name}"),
    ):
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract_payload(
            payload
        )


def test_cpd_paper_newton_shape_runtime_engine_builder_api_surface_static_boundary_is_source_ast_only():
    helpers = (
        newton_env.inspect_newton_engine_builder_api_surface,
        newton_env._parse_source_ast,
        newton_env._module_exports_name,
        newton_env._literal_list_contains,
        newton_env._find_class_definition,
        newton_env._find_class_method,
        newton_env._function_signature,
        newton_env._ast_default_label,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_api_surface_source_row,
        cpd_paper_offline._paper_newton_shape_runtime_engine_builder_api_surface_row,
        cpd_paper_offline._paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract_payload,
    )
    source = "\n".join(inspect.getsource(helper) for helper in helpers)

    forbidden_patterns = (
        'importlib.import_module("newton")',
        'importlib.import_module("warp")',
        "importlib.import_module",
        "module_from_spec",
        "exec_module",
        "__import__",
        "_git_commit",
        "subprocess",
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
