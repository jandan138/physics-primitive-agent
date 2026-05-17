import json
from math import isfinite, pi, sqrt

import pytest

from primitive_collision_compiler.baselines.cpd_like.primitives import SUPPORTED_PRIMITIVES
from primitive_collision_compiler.baselines.cpd_paper.offline import (
    CPD_PAPER_OFFLINE_CLAIM_BOUNDARY,
    _paper_mapped_subset_adapter_preflight_contract_payload,
    _paper_mapped_subset_primitivespec_dry_run_contract_payload,
    _paper_mapped_subset_primitivespec_generation_contract_payload,
    _paper_mapped_subset_primitivespec_generation_preflight_contract_payload,
    _paper_mapped_subset_primitivespec_validation_contract_payload,
    _paper_package_adapter_contract_payload,
    _paper_require_unique_generation_preflight_row_ids,
    _paper_require_unique_generation_row_ids,
    build_cpd_paper_offline_report,
)

EXPECTED_GENERALIZATION_NEXT_ACTION = (
    "Proceed to paper_package_adapter_contract after the changed-decomposition "
    "output contract; keep package/Newton wording blocked."
)
EXPECTED_CLOSED_SOURCE_POLICY_GATE = "paper_generalization_batch_a_source_policy"
EXPECTED_CLOSED_PRIMITIVE_FIT_GATE = "paper_generalization_batch_b_primitive_fit_engine"
EXPECTED_CLOSED_SEARCH_ENGINE_GATE = "paper_generalization_batch_c_search_engine"
EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE = "paper_generalization_batch_d_postprocess_policy"
EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE = (
    "paper_generalization_batch_e_package_boundary_readiness"
)
EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY = "paper_offline_changed_decomposition_output_contract"
EXPECTED_PACKAGE_GENERATION_CONTRACT = "paper_package_generation_contract"
EXPECTED_PACKAGE_ADAPTER_CONTRACT = "paper_package_adapter_contract"
EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY = (
    "paper_package_adapter_unsupported_primitive_policy"
)
EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN = (
    "paper_package_conversion_mapped_subset_plan"
)
EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX = (
    "paper_mapped_subset_conversion_candidate_matrix"
)
EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_adapter_preflight_contract"
)
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT = (
    "paper_mapped_subset_primitivespec_dry_run_contract"
)
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_validation_contract"
)
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_primitivespec_generation_preflight_contract"
)
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_generation_contract"
)
EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT = (
    "paper_mapped_subset_primitivespec_candidate_source_contract"
)
EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT = (
    "paper_offline_changed_decomposition_output_contract"
)
EXPECTED_CLOSED_GENERALIZATION_GATES = [
    EXPECTED_CLOSED_SOURCE_POLICY_GATE,
    EXPECTED_CLOSED_PRIMITIVE_FIT_GATE,
    EXPECTED_CLOSED_SEARCH_ENGINE_GATE,
    EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE,
    EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE,
]
EXPECTED_CURRENT_GENERALIZATION_GATES = [
    EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY,
    EXPECTED_PACKAGE_GENERATION_CONTRACT,
]
EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
]
EXPECTED_PACKAGE_ADAPTER_REMAINING_GAPS = [
    EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
]
EXPECTED_UNSUPPORTED_POLICY_REMAINING_GAPS = [
    EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
]
EXPECTED_CONVERSION_MAPPED_SUBSET_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
]
EXPECTED_CANDIDATE_MATRIX_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
]
EXPECTED_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
]
EXPECTED_PRIMITIVESPEC_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
]
EXPECTED_VALIDATION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT,
]
EXPECTED_GENERATION_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
]
EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT,
]
EXPECTED_PACKAGE_BOUNDARY_REMAINING_GAPS = [
    EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY,
    EXPECTED_PACKAGE_GENERATION_CONTRACT,
]
EXPECTED_SOURCE_POLICY_REMAINING_GAPS = [
    EXPECTED_CLOSED_PRIMITIVE_FIT_GATE,
    EXPECTED_CLOSED_SEARCH_ENGINE_GATE,
    EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE,
    EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE,
]
EXPECTED_PRIMITIVE_FIT_REMAINING_GAPS = [
    EXPECTED_CLOSED_SEARCH_ENGINE_GATE,
    EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE,
    EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE,
]
EXPECTED_SEARCH_ENGINE_REMAINING_GAPS = [
    EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE,
    EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE,
]
EXPECTED_POSTPROCESS_POLICY_REMAINING_GAPS = [
    EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE,
]
EXPECTED_GENERALIZATION_FAILURE_LABELS = [
    f"{gate}_missing" for gate in EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
]

EXPECTED_SCOPE_AUDIT_ROWS = [
    {
        "criterion_id": "source_mesh_and_preprocessing_policy",
        "paper_requirement": (
            "Mesh vertices/faces plus duplicate or overlapped vertex preprocessing "
            "and source-face remap."
        ),
        "current_evidence": (
            "Triangle toy fixtures, fan-triangulated source-face fixtures, and one "
            "exact-coordinate duplicate-vertex fixture; broader unclean-mesh policy is absent."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Exact-overlap toy preprocessing only; no robust arbitrary mesh cleanup."
        ),
        "next_action": EXPECTED_GENERALIZATION_NEXT_ACTION,
    },
    {
        "criterion_id": "source_face_intake_policy",
        "paper_requirement": (
            "Preserve face ownership across triangle, quad, and polygon source faces."
        ),
        "current_evidence": (
            "One quad and one five-vertex polygon fan-triangulation fixture with "
            "source-face remap and operator ownership accounting."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Source-face intake is toy-scoped, not a general polygon mesh implementation."
        ),
        "next_action": EXPECTED_GENERALIZATION_NEXT_ACTION,
    },
    {
        "criterion_id": "operator_q_audit",
        "paper_requirement": (
            "Per-face and merged-group Q operators with eigen decomposition."
        ),
        "current_evidence": (
            "Per-face and merged-group operator rows exist for named toy fixtures, "
            "including source-face aggregate rows."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Operator evidence is named-fixture audit data, not full paper decomposition."
        ),
        "next_action": EXPECTED_GENERALIZATION_NEXT_ACTION,
    },
    {
        "criterion_id": "primitive_vocabulary_and_fit",
        "paper_requirement": (
            "Audit the six paper primitive candidates, containment, formulas, axis "
            "policies, and primitive weights."
        ),
        "current_evidence": (
            "All six paper primitive names have fixture-scoped audit rows, including "
            "Batch B primitive-fit breadth fixtures; capped cylinder, frustum, and "
            "trapezoidal prism remain offline-only."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Primitive rows are audit rows, not Newton runtime support or "
            "collision-quality evidence."
        ),
        "next_action": EXPECTED_GENERALIZATION_NEXT_ACTION,
    },
    {
        "criterion_id": "paper_collapse_cost_and_weighting",
        "paper_requirement": (
            "Use paper base collapse cost, separate weighted priority cost, and no "
            "intersection-volume primary cost."
        ),
        "current_evidence": (
            "One two-face cost fixture plus Batch C cost/search/stop fixtures record "
            "base and weighted costs, weighted priority ordering, and one positive "
            "finite threshold block."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": "Cost rows are toy accounting, not optimizer or benchmark evidence.",
        "next_action": EXPECTED_GENERALIZATION_NEXT_ACTION,
    },
    {
        "criterion_id": "greedy_priority_queue_trace",
        "paper_requirement": (
            "Initialize adjacent face-pair candidates, pop minimum priority cost, "
            "handle stale entries, and merge greedily."
        ),
        "current_evidence": (
            "Topology, deduplicated-topology, component-pair, and Batch C toy traces "
            "exist with deterministic queue keys, weighted-priority ordering, and "
            "equal-cost stale-prune behavior."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Search traces are toy-scoped and do not prove merge-policy superiority."
        ),
        "next_action": EXPECTED_GENERALIZATION_NEXT_ACTION,
    },
    {
        "criterion_id": "target_count_and_threshold_stop",
        "paper_requirement": (
            "Stop at target primitive count or when valid threshold policy blocks "
            "remaining candidates."
        ),
        "current_evidence": (
            "Target-count traces, one zero finite-threshold component-pair block, and "
            "one Batch C positive nonzero finite-threshold component-pair block exist."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": "Threshold evidence is narrow toy accounting.",
        "next_action": EXPECTED_GENERALIZATION_NEXT_ACTION,
    },
    {
        "criterion_id": "component_pair_edge_handling",
        "paper_requirement": (
            "Insert pairwise component candidates when disconnected topology cannot "
            "reach the target."
        ),
        "current_evidence": (
            "Accepted and blocked component-pair toy traces exist, and Batch D records "
            "multi-candidate component-pair ordering plus deterministic skipped-pair "
            "accounting under a fixture cap."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Component merging evidence is diagnostic accounting, not broad asset evidence."
        ),
        "next_action": EXPECTED_GENERALIZATION_NEXT_ACTION,
    },
    {
        "criterion_id": "enclosed_primitive_postprocess",
        "paper_requirement": "Remove primitives enclosed by other primitives.",
        "current_evidence": (
            "Identity-axis and rotated nested OBB cull fixtures exist, and Batch E records "
            "a conservative cross-type unsupported boundary with no silent cull."
        ),
        "status": "partial_fixture_scope",
        "surrogate_or_paper_faithful": "fixture_scoped_paper_shaped",
        "blocking_for_paper_faithful_offline": True,
        "claim_boundary": (
            "Postprocess cull evidence is one offline canary, not a general containment library."
        ),
        "next_action": EXPECTED_GENERALIZATION_NEXT_ACTION,
    },
    {
        "criterion_id": "report_schema_tests_and_records",
        "paper_requirement": (
            "Keep report schema, tests, registry, and dated records reproducible."
        ),
        "current_evidence": (
            "This slice adds RED/GREEN tests, registry metadata, and a dated "
            "record path."
        ),
        "status": "implemented_fixture_scope",
        "surrogate_or_paper_faithful": "paper_aligned_boundary",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": (
            "Reproducibility evidence supports the audit record only, not stronger "
            "algorithm claims."
        ),
        "next_action": "Keep records updated for every future gate.",
    },
    {
        "criterion_id": "package_generation_boundary",
        "paper_requirement": "Keep offline paper mechanics separate from package conversion.",
        "current_evidence": (
            "The report records package-generation false triggers and no CollisionPackage conversion."
        ),
        "status": "blocked_until_later_gate",
        "surrogate_or_paper_faithful": "out_of_offline_scope",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": "Package generation is a later explicit adapter gate.",
        "next_action": (
            "Add package conversion only after a changed offline package boundary exists."
        ),
    },
    {
        "criterion_id": "newton_runtime_boundary",
        "paper_requirement": (
            "Keep offline paper mechanics separate from Newton runtime diagnostics."
        ),
        "current_evidence": "The report records Newton false triggers and no runtime execution.",
        "status": "blocked_until_later_gate",
        "surrogate_or_paper_faithful": "out_of_offline_scope",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": "Newton support requires separate mapping and diagnostic records.",
        "next_action": (
            "Run Newton only after package conversion and runtime admissibility are recorded."
        ),
    },
    {
        "criterion_id": "real_usd_boundary",
        "paper_requirement": "Keep toy fixture audit separate from real asset evidence.",
        "current_evidence": (
            "The report records real-USD false triggers and uses synthetic toy fixtures only."
        ),
        "status": "blocked_until_later_gate",
        "surrogate_or_paper_faithful": "out_of_offline_scope",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": "Real-USD evidence requires separate asset manifests and records.",
        "next_action": (
            "Defer bed/Franka or other real assets until a package-changing gate exists."
        ),
    },
    {
        "criterion_id": "benchmark_evaluation_boundary",
        "paper_requirement": (
            "Keep paper benchmark evaluation separate from offline paper-mechanics audit."
        ),
        "current_evidence": (
            "The report records benchmark false triggers and no timing, surface-distance, "
            "byte-cost, or baseline comparison metrics."
        ),
        "status": "blocked_until_later_gate",
        "surrogate_or_paper_faithful": "out_of_offline_scope",
        "blocking_for_paper_faithful_offline": False,
        "claim_boundary": (
            "Benchmark evidence is not required for bounded offline status and is not claimed here."
        ),
        "next_action": (
            "Defer benchmarks until offline decomposition and runtime package gates are ready."
        ),
    },
]
EXPECTED_SCOPE_AUDIT_CRITERIA = [
    row["criterion_id"] for row in EXPECTED_SCOPE_AUDIT_ROWS
]
EXPECTED_SCOPE_AUDIT_BLOCKERS = [
    row["criterion_id"]
    for row in EXPECTED_SCOPE_AUDIT_ROWS
    if row["blocking_for_paper_faithful_offline"]
]


def test_cpd_paper_offline_report_failure_labels_point_to_candidate_source_gap():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS


def test_cpd_paper_offline_report_next_gate_is_primitivespec_candidate_source_contract():
    report = build_cpd_paper_offline_report()

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )


def _candidate_by_paper_primitive(audit, paper_primitive):
    rows = [
        row for row in audit["candidates"] if row["paper_primitive"] == paper_primitive
    ]
    assert len(rows) == 1
    return rows[0]


def _event_signature(trace):
    return [
        (
            event["event_kind"],
            event["source_faces_left"],
            event["source_faces_right"],
            event["accepted"],
            event["stale_entry"],
            event["blocked"],
        )
        for event in trace["events"]
    ]


def _assert_queue_key_contract(candidate_or_event):
    assert candidate_or_event["queue_key"] == [
        candidate_or_event["weighted_priority_cost"],
        candidate_or_event["paper_base_cost"],
        candidate_or_event["source_faces_left"],
        candidate_or_event["source_faces_right"],
        candidate_or_event["insertion_order"],
    ]


def _candidate_has_common_fit_fields(row):
    assert row["paper_primitive"]
    assert row["current_implementation_kind"]
    assert row["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert row["fit_model"]
    assert row["axis_selection_policy"]
    assert row["center"]
    assert row["axes"]
    assert row["dimensions"]
    assert row["volume"] > 0.0
    assert row["paper_weight"] > 0.0
    assert row["weighted_volume"] > 0.0
    assert "contains_assigned_points" in row
    assert "fit_failure_reason" in row
    return True


def _axes_are_orthonormal(axes):
    for axis in axes:
        length = sum(value * value for value in axis) ** 0.5
        assert abs(length - 1.0) < 1e-9
    for left_index in range(3):
        for right_index in range(left_index + 1, 3):
            dot = sum(
                axes[left_index][coord] * axes[right_index][coord]
                for coord in range(3)
            )
            assert abs(dot) < 1e-9
    return True


def _axes_are_world_aligned(axes):
    return all(_axis_is_world_basis(axis) for axis in axes)


def _axis_is_world_basis(axis):
    abs_values = [abs(value) for value in axis]
    max_index = max(range(3), key=lambda index: abs_values[index])
    return (
        abs(abs_values[max_index] - 1.0) < 1e-9
        and all(abs_values[index] < 1e-9 for index in range(3) if index != max_index)
    )


def _expected_duplicate_vertex_source_face_remap():
    return [
        {
            "source_face_id": 0,
            "input_vertex_ids": [0, 1, 2],
            "deduplicated_vertex_ids": [0, 1, 2],
            "face_preserved": True,
            "drop_reason": None,
        },
        {
            "source_face_id": 1,
            "input_vertex_ids": [3, 4, 5],
            "deduplicated_vertex_ids": [0, 1, 3],
            "face_preserved": True,
            "drop_reason": None,
        },
    ]


def _assert_duplicate_vertex_preprocessing_case(case):
    audit = case["preprocessing_audit"]
    assert audit["audit_scope"] == "duplicate_vertex_preprocessing_fixture"
    assert audit["preprocessing_policy"] == "exact_coordinate_deduplication_for_fixture"
    assert audit["distance_tolerance"] == 0.0
    assert audit["input_vertex_count"] == 6
    assert audit["deduplicated_vertex_count"] == 4
    assert audit["duplicate_cluster_count"] == 2
    assert audit["duplicate_clusters"] == [[0, 3], [1, 4]]
    assert audit["original_to_deduplicated_vertex_ids"] == [0, 1, 2, 0, 1, 3]
    assert audit["input_faces"] == [[0, 1, 2], [3, 4, 5]]
    assert audit["deduplicated_faces"] == [[0, 1, 2], [0, 1, 3]]
    assert audit["connected_component_count_before"] == 2
    assert audit["connected_component_count_after"] == 1
    assert audit["topology_changed"] is True
    assert audit["degenerate_face_dropped_count"] == 0
    assert audit["retained_source_face_ids"] == [0, 1]
    assert audit["dropped_source_face_ids"] == []
    assert audit["preprocessing_source_face_remap"] == (
        _expected_duplicate_vertex_source_face_remap()
    )
    assert audit["package_generation_triggered"] is False
    assert audit["newton_runtime_triggered"] is False
    assert audit["real_usd_triggered"] is False
    assert audit["benchmark_triggered"] is False

    source_mesh = case["source_mesh"]
    assert source_mesh["duplicate_vertex_preprocessing"] == (
        "exact_coordinate_deduplication_for_fixture"
    )
    assert source_mesh["preprocessed_input_vertex_count"] == 6
    assert source_mesh["deduplicated_vertex_count"] == 4
    assert source_mesh["vertex_count"] == 4
    assert source_mesh["source_face_remap"] == (
        "duplicate_vertex_preprocessing_face_id_preserving"
    )
    assert source_mesh["preprocessing_source_face_remap"] == (
        _expected_duplicate_vertex_source_face_remap()
    )

    trace = case["collapse_trace"]
    assert trace["preprocessing_boundary"] == "exact_coordinate_duplicate_vertex_fixture"
    assert trace["initial_edge_count"] == 1
    assert trace["accepted_merge_count"] == 1
    assert trace["final_active_groups"] == [[0, 1]]
    assert trace["events"][0]["source_faces_left"] == [0]
    assert trace["events"][0]["source_faces_right"] == [1]
    assert trace["events"][0]["resulting_source_faces"] == [0, 1]

    assert case["operator_audit"]["preprocessing_boundary"] == (
        "exact_coordinate_duplicate_vertex_fixture"
    )
    assert case["primitive_fit_audit"]["preprocessing_boundary"] == (
        "exact_coordinate_duplicate_vertex_fixture"
    )
    assert case["package_generation_triggered"] is False
    assert case["newton_runtime_triggered"] is False
    assert case["real_usd_triggered"] is False
    assert case["benchmark_triggered"] is False


def _assert_paper_obb_sphere_rows(case, points):
    audit = case["primitive_fit_audit"]
    box = _candidate_by_paper_primitive(audit, "oriented_bounding_box")
    sphere = _candidate_by_paper_primitive(audit, "sphere")

    assert box["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert box["current_implementation_kind"] == "offline_paper_oriented_bounding_box_fit"
    assert box["fit_model"] == "paper_operator_eigenbasis_projected_bounds"
    assert box["axis_selection_policy"] == "paper_q_eigenbasis"
    assert box["axis_matrix_layout"] == "rows_are_axes"
    assert box["primitive_parameter_lower_clamp"] == 1e-3
    assert box["newton_runtime_kind"] == "box"
    assert box["contains_assigned_points"] is True
    assert box["fit_failure_reason"] is None
    box_dims = box["dimensions"]
    assert box_dims["volume_formula"] == "8*hx*hy*hz"
    assert box_dims["paper_center_world"] == box["center"]
    assert box_dims["axis_order_policy"] == "descending_abs_q_eigenvalue"

    axes = box["axes"]
    local = [
        [sum(point[index] * axis[index] for index in range(3)) for axis in axes]
        for point in points
    ]
    lower = [min(row[index] for row in local) for index in range(3)]
    upper = [max(row[index] for row in local) for index in range(3)]
    center_local = [(lower[index] + upper[index]) * 0.5 for index in range(3)]
    half_extents = [
        max((upper[index] - lower[index]) * 0.5, 1e-3)
        for index in range(3)
    ]
    center = [
        sum(axes[axis_index][coord] * center_local[axis_index] for axis_index in range(3))
        for coord in range(3)
    ]
    assert all(
        abs(box_dims["lower_bounds"][index] - lower[index]) < 1e-9
        for index in range(3)
    )
    assert all(
        abs(box_dims["upper_bounds"][index] - upper[index]) < 1e-9
        for index in range(3)
    )
    assert all(
        abs(box_dims["paper_center_local"][index] - center_local[index]) < 1e-9
        for index in range(3)
    )
    assert all(
        abs(box_dims["paper_center_world"][index] - center[index]) < 1e-9
        for index in range(3)
    )
    assert all(
        abs(box_dims["half_extents"][index] - half_extents[index]) < 1e-9
        for index in range(3)
    )
    assert all(abs(box["center"][index] - center[index]) < 1e-9 for index in range(3))
    expected_box_volume = 8.0 * half_extents[0] * half_extents[1] * half_extents[2]
    assert abs(box["volume"] - expected_box_volume) < 1e-9

    assert sphere["implementation_status"] == "paper_shaped_offline_fit_audit"
    assert sphere["current_implementation_kind"] == "offline_paper_sphere_fit"
    assert sphere["fit_model"] == "paper_obb_center_max_distance_radius"
    assert sphere["axis_selection_policy"] == "paper_obb_center"
    assert sphere["primitive_parameter_lower_clamp"] == 1e-3
    assert sphere["newton_runtime_kind"] == "sphere"
    assert sphere["contains_assigned_points"] is True
    assert sphere["fit_failure_reason"] is None
    assert sphere["axes"] == box["axes"]
    sphere_dims = sphere["dimensions"]
    assert sphere_dims["center_source"] == "paper_obb_center"
    assert sphere_dims["radius_source"] == "max_distance_from_obb_center_clamped"
    assert sphere_dims["volume_formula"] == "4/3*pi*r^3"
    assert sphere["center"] == box["center"]
    unclamped_radius = max(
        sqrt(sum((point[index] - box["center"][index]) ** 2 for index in range(3)))
        for point in points
    )
    expected_radius = max(unclamped_radius, 1e-3)
    assert abs(sphere_dims["unclamped_radius"] - unclamped_radius) < 1e-9
    assert abs(sphere_dims["radius"] - expected_radius) < 1e-9
    assert abs(sphere["volume"] - (4.0 / 3.0) * pi * expected_radius**3) < 1e-9


def _assert_intake_case(case, *, arity, generated_triangles):
    expected_face_ids = list(range(len(generated_triangles)))
    expected_remap = [
        {
            "source_face_id": 0,
            "source_face_arity": arity,
            "source_vertex_ids": list(range(arity)),
            "generated_triangle_face_ids": expected_face_ids,
            "generated_triangle_vertex_ids": [list(triangle) for triangle in generated_triangles],
        }
    ]
    expected_preconditions = [
        "planar",
        "convex",
        "non_degenerate",
        "consistently_wound",
    ]

    source_mesh = case["source_mesh"]
    assert source_mesh["face_arity_policy"] == (
        "fan_triangulate_non_triangle_faces_preserve_source_face_remap"
    )
    assert source_mesh["source_face_count"] == 1
    assert source_mesh["source_face_arities"] == [arity]
    assert source_mesh["triangulated_face_count"] == len(generated_triangles)
    assert source_mesh["executable_triangle_face_count"] == len(generated_triangles)
    assert source_mesh["face_count"] == len(generated_triangles)
    assert source_mesh["executable_triangle_faces"] == [
        list(triangle) for triangle in generated_triangles
    ]
    assert source_mesh["source_face_remap"] == expected_remap
    for remap in source_mesh["source_face_remap"]:
        for generated_face_id, generated_triangle in zip(
            remap["generated_triangle_face_ids"],
            remap["generated_triangle_vertex_ids"],
            strict=True,
        ):
            assert source_mesh["executable_triangle_faces"][generated_face_id] == generated_triangle
    assert source_mesh["operator_ownership_policy"] == (
        "triangulated_subfaces_summed_to_source_face"
    )
    assert source_mesh["source_face_preconditions"] == expected_preconditions

    intake_audit = case["mesh_intake_policy_audit"]
    assert intake_audit["audit_scope"] == "polygon_quad_source_face_intake_policy_fixture"
    assert intake_audit["source_face_count"] == source_mesh["source_face_count"]
    assert intake_audit["source_face_arities"] == source_mesh["source_face_arities"]
    assert intake_audit["triangulated_face_count"] == source_mesh["triangulated_face_count"]
    assert intake_audit["executable_triangle_face_count"] == source_mesh[
        "executable_triangle_face_count"
    ]
    assert intake_audit["source_face_remap"] == source_mesh["source_face_remap"]
    assert intake_audit["source_face_preconditions"] == expected_preconditions
    assert intake_audit["source_face_policy"] == (
        "preserve_source_face_id_after_fan_triangulation"
    )
    assert intake_audit["triangulation_policy"] == "fan_from_first_vertex"
    assert intake_audit["operator_ownership_policy"] == (
        "triangulated_subfaces_summed_to_source_face"
    )
    assert intake_audit["normal_policy"] == (
        "triangle_normals_area_weighted_after_fan_triangulation"
    )
    assert intake_audit["tangent_policy"] == (
        "triangle_edge_tangents_area_weighted_after_fan_triangulation"
    )
    assert intake_audit["package_generation_triggered"] is False
    assert intake_audit["newton_runtime_triggered"] is False
    assert intake_audit["real_usd_triggered"] is False
    assert intake_audit["benchmark_triggered"] is False

    operator_audit = case["operator_audit"]
    assert operator_audit["face_scope"] == "triangle_subfaces_from_source_face"
    assert operator_audit["source_face_operator_aggregates"][0]["source_face_id"] == 0
    assert operator_audit["source_face_operator_aggregates"][0][
        "generated_triangle_face_ids"
    ] == expected_face_ids
    expected_q = [
        [
            sum(face["q_matrix"][row][col] for face in operator_audit["faces"])
            for col in range(3)
        ]
        for row in range(3)
    ]
    assert operator_audit["source_face_operator_aggregates"][0]["q_matrix"] == expected_q
    assert operator_audit["merged_group"]["source_faces"] == [0]
    assert operator_audit["merged_group"]["generated_triangle_face_ids"] == expected_face_ids
    assert operator_audit["merged_group"]["source_face_ids"] == [0]
    assert case["primitive_fit_audit"]["source_faces"] == [0]
    assert case["primitive_fit_audit"]["generated_triangle_face_ids"] == expected_face_ids
    assert case["primitive_fit_audit"]["source_face_ids"] == [0]


def test_cpd_paper_offline_report_records_polygon_quad_intake_policy():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    _assert_intake_case(
        cases["paper_quad_face_intake"],
        arity=4,
        generated_triangles=[(0, 1, 2), (0, 2, 3)],
    )
    _assert_intake_case(
        cases["paper_polygon_face_intake"],
        arity=5,
        generated_triangles=[(0, 1, 2), (0, 2, 3), (0, 3, 4)],
    )


def test_cpd_paper_offline_report_records_fixture_breadth_batch_a():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    mixed = cases["paper_mixed_face_preprocess_operator"]
    assert mixed["fixture_breadth_batch"] == "paper_fixture_breadth_batch_a"
    assert mixed["source_mesh"]["source_face_arities"] == [3, 4, 5]
    assert mixed["source_mesh"]["duplicate_vertex_preprocessing"] == (
        "exact_coordinate_deduplication_for_fixture"
    )
    assert mixed["preprocessing_audit"]["duplicate_cluster_count"] == 1
    assert mixed["preprocessing_audit"]["degenerate_face_dropped_count"] == 0
    assert mixed["mesh_intake_policy_audit"]["source_face_arities"] == [3, 4, 5]
    assert mixed["mesh_intake_policy_audit"]["triangulated_face_count"] == 6
    assert mixed["operator_audit"]["face_scope"] == "triangle_subfaces_from_source_face"
    assert len(mixed["operator_audit"]["source_face_operator_aggregates"]) == 3
    for aggregate in mixed["operator_audit"]["source_face_operator_aggregates"]:
        assert aggregate["q_matrix"]
        assert len(aggregate["eigenvalues"]) == 3
        assert aggregate["eigenvector_matrix_layout"] == "columns_are_eigenvectors"
        assert isinstance(aggregate["degeneracy_labels"], list)

    degenerate = cases["paper_degenerate_preprocess_face_drop"]
    assert degenerate["fixture_breadth_batch"] == "paper_fixture_breadth_batch_a"
    degenerate_audit = degenerate["preprocessing_audit"]
    assert degenerate_audit["degenerate_face_dropped_count"] == 1
    assert degenerate_audit["dropped_source_face_ids"] == [0]
    assert degenerate_audit["retained_source_face_ids"] == [1]
    assert degenerate_audit["preprocessing_source_face_remap"][0]["drop_reason"] == (
        "degenerate_after_deduplication"
    )
    assert degenerate_audit["executable_deduplicated_faces"] == [[2, 3, 4]]
    assert degenerate["source_mesh"]["face_count"] == 1
    assert degenerate["operator_audit"]["preprocessing_degeneracy_labels"] == [
        "dropped_degenerate_faces_after_preprocessing"
    ]
    assert degenerate["operator_audit"]["faces"][0]["source_face_id"] == 1
    assert degenerate["operator_audit"]["merged_group"]["source_faces"] == [1]
    assert degenerate["primitive_fit_audit"]["source_faces"] == [1]
    assert degenerate["primitive_fit_audit"]["source_face_ids"] == [1]
    assert degenerate["primitive_fit_audit"]["generated_triangle_face_ids"] == [0]

    concave = cases["paper_concave_polygon_rejected"]
    assert concave["fixture_breadth_batch"] == "paper_fixture_breadth_batch_a"
    assert concave["case_status"] == "unsupported_fixture_policy"
    intake = concave["mesh_intake_policy_audit"]
    assert intake["failure_label"] == "source_face_intake_unsupported_concave_polygon"
    assert intake["source_face_arities"] == [5]
    assert intake["generated_triangle_face_ids"] == []
    assert intake["triangulated_face_count"] == 0
    assert intake["top_level_failure_label"] is False
    assert "primitive_fit_audits" not in concave
    assert concave["package_generation_triggered"] is False
    assert concave["newton_runtime_triggered"] is False
    assert concave["real_usd_triggered"] is False
    assert concave["benchmark_triggered"] is False


def test_cpd_paper_offline_report_records_fixture_breadth_batch_b():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    expected_case_ids = {
        "paper_rotated_box_fit",
        "paper_offset_sphere_fit",
        "paper_off_axis_capsule_fit",
        "paper_flat_capped_cylinder_axis_fit",
        "paper_tapered_frustum_fit",
        "paper_asymmetric_trapezoid_fit",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_b"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        assert case["primitive_fit_audit"]["missing_paper_primitives"] == []

    rotated_box = cases["paper_rotated_box_fit"]
    obb = _candidate_by_paper_primitive(
        rotated_box["primitive_fit_audit"],
        "oriented_bounding_box",
    )
    assert _candidate_has_common_fit_fields(obb)
    assert obb["contains_assigned_points"] is True
    assert obb["dimensions"]["volume_formula"] == "8*hx*hy*hz"
    assert obb["dimensions"]["axis_order_policy"] == "descending_abs_q_eigenvalue"
    assert obb["dimensions"]["lower_bounds"]
    assert obb["dimensions"]["upper_bounds"]
    assert obb["dimensions"]["paper_center_local"]
    assert obb["dimensions"]["paper_center_world"] == obb["center"]
    assert obb["dimensions"]["half_extents"]
    assert obb["newton_runtime_kind"] == "box"
    assert _axes_are_orthonormal(obb["axes"])
    assert not _axes_are_world_aligned(obb["axes"])

    offset_sphere = cases["paper_offset_sphere_fit"]
    sphere = _candidate_by_paper_primitive(
        offset_sphere["primitive_fit_audit"],
        "sphere",
    )
    assert _candidate_has_common_fit_fields(sphere)
    assert sphere["contains_assigned_points"] is True
    assert sphere["dimensions"]["center_source"] == "paper_obb_center"
    assert sphere["dimensions"]["radius"] >= 1e-3
    assert sphere["dimensions"]["unclamped_radius"] > 0.0
    assert sphere["dimensions"]["volume_formula"] == "4/3*pi*r^3"
    assert sphere["dimensions"]["fixture_center_relation"] == "differs_from_point_centroid"
    assert sphere["dimensions"]["center_differs_from_point_centroid"] is True
    assert sphere["dimensions"]["center_centroid_distance"] > 1e-3
    assert sphere["newton_runtime_kind"] == "sphere"

    off_axis_capsule = cases["paper_off_axis_capsule_fit"]
    capsule = _candidate_by_paper_primitive(
        off_axis_capsule["primitive_fit_audit"],
        "capsule",
    )
    assert _candidate_has_common_fit_fields(capsule)
    assert capsule["contains_assigned_points"] is True
    assert capsule["dimensions"]["axis_selection_policy"] == "min_volume_capsule_axis"
    assert len(capsule["dimensions"]["paper_capsule_axis_candidates"]) == 3
    assert capsule["dimensions"]["height"] > 0.0
    assert capsule["dimensions"]["radius"] > 0.0
    selected_capsule_axis = capsule["axes"][capsule["dimensions"]["selected_axis_index"]]
    assert not _axis_is_world_basis(selected_capsule_axis)

    flat_cylinder = cases["paper_flat_capped_cylinder_axis_fit"]
    capped = _candidate_by_paper_primitive(
        flat_cylinder["primitive_fit_audit"],
        "capped_cylinder",
    )
    assert _candidate_has_common_fit_fields(capped)
    assert capped["contains_assigned_points"] is True
    assert capped["newton_runtime_kind"] == "offline_only_unmapped"
    assert capped["dimensions"]["cap_model"] == "flat_caps"
    assert capped["dimensions"]["volume_formula"] == "pi*r^2*h"
    assert len(capped["dimensions"]["flat_cylinder_axis_candidates"]) == 3
    assert capped["dimensions"]["radius"] > 0.0
    assert capped["dimensions"]["height"] > 0.0
    selected_capped_axis = capped["axes"][capped["dimensions"]["selected_axis_index"]]
    assert not _axis_is_world_basis(selected_capped_axis)

    tapered = cases["paper_tapered_frustum_fit"]
    frustum = _candidate_by_paper_primitive(
        tapered["primitive_fit_audit"],
        "frustum",
    )
    assert _candidate_has_common_fit_fields(frustum)
    assert frustum["contains_assigned_points"] is True
    assert frustum["newton_runtime_kind"] == "offline_only_unmapped"
    assert abs(frustum["dimensions"]["top_radius"] - frustum["dimensions"]["bottom_radius"]) > 0.05
    assert frustum["dimensions"]["height"] > 0.0
    assert frustum["dimensions"]["top_center"]
    assert frustum["dimensions"]["bottom_center"]
    assert frustum["dimensions"]["volume_formula"] == "pi*h/3*(rt^2 + rt*rb + rb^2)"

    trapezoid = cases["paper_asymmetric_trapezoid_fit"]
    prism = _candidate_by_paper_primitive(
        trapezoid["primitive_fit_audit"],
        "trapezoidal_prism",
    )
    assert _candidate_has_common_fit_fields(prism)
    assert prism["contains_assigned_points"] is True
    assert prism["newton_runtime_kind"] == "offline_only_unmapped"
    assert prism["dimensions"]["axis_order_attempt_count"] == 6
    assert len(prism["dimensions"]["axis_order_attempts"]) == 6
    assert prism["dimensions"]["axis_order"]
    assert prism["dimensions"]["h_x"] > 0.0
    assert prism["dimensions"]["h_y"] > 0.0
    assert prism["dimensions"]["h_zt"] > 0.0
    assert prism["dimensions"]["h_zb"] > 0.0
    assert prism["dimensions"]["volume_formula"] == "4*h_x*h_y*(h_zt + h_zb)"


def test_cpd_paper_offline_report_records_fixture_breadth_batch_c():
    report = build_cpd_paper_offline_report()
    report_again = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}
    cases_again = {case["case_id"]: case for case in report_again["cases"]}

    expected_case_ids = {
        "paper_branching_cost_order",
        "paper_equal_cost_queue_tie",
        "paper_nonzero_threshold_block",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_c"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        assert case["collapse_trace"]["package_generation_triggered"] is False
        assert case["collapse_trace"]["newton_runtime_triggered"] is False
        assert case["collapse_trace"]["real_usd_triggered"] is False
        assert case["collapse_trace"]["benchmark_triggered"] is False
        for candidate in case["collapse_trace"]["initial_candidates"]:
            assert isfinite(candidate["paper_base_cost"])
            assert isfinite(candidate["weighted_priority_cost"])
            assert isfinite(candidate["queue_key"][0])
            assert isfinite(candidate["queue_key"][1])
        for event in case["collapse_trace"]["events"]:
            assert isfinite(event["paper_base_cost"])
            assert isfinite(event["weighted_priority_cost"])
            assert isfinite(event["queue_key"][0])
            assert isfinite(event["queue_key"][1])

    branching = cases["paper_branching_cost_order"]["collapse_trace"]
    assert branching["trace_scope"] == "topology_priority_queue_trace_fixture"
    assert branching["initial_edge_count"] == 2
    assert branching["target_primitive_count"] == 3
    assert branching["threshold_policy"] == "disabled"
    assert len(branching["initial_candidates"]) == 2
    assert all(
        candidate["edge_source"] == "topology"
        for candidate in branching["initial_candidates"]
    )
    assert all(
        "paper_base_cost" in candidate for candidate in branching["initial_candidates"]
    )
    assert all(
        "weighted_priority_cost" in candidate
        for candidate in branching["initial_candidates"]
    )
    first_accepted = [event for event in branching["events"] if event["accepted"]][0]
    assert first_accepted["weighted_priority_cost"] == min(
        candidate["weighted_priority_cost"]
        for candidate in branching["initial_candidates"]
    )
    assert first_accepted["queue_key"] == min(
        candidate["queue_key"] for candidate in branching["initial_candidates"]
    )
    min_base_candidate = min(
        branching["initial_candidates"],
        key=lambda candidate: candidate["paper_base_cost"],
    )
    min_weighted_candidate = min(
        branching["initial_candidates"],
        key=lambda candidate: candidate["weighted_priority_cost"],
    )
    assert min_base_candidate["source_faces_merged"] != min_weighted_candidate[
        "source_faces_merged"
    ]
    assert first_accepted["source_faces_merged"] == min_weighted_candidate[
        "source_faces_merged"
    ]
    assert first_accepted["source_faces_merged"] != min_base_candidate[
        "source_faces_merged"
    ]
    assert first_accepted["queue_key"][0] == first_accepted["weighted_priority_cost"]
    assert first_accepted["queue_key"][1] == first_accepted["paper_base_cost"]
    assert first_accepted["updated_neighbor_insertion_count"] == 1
    assert branching["accepted_merge_count"] == 1
    assert branching["stop_reason"] == "target_count_reached"

    tie = cases["paper_equal_cost_queue_tie"]["collapse_trace"]
    tie_again = cases_again["paper_equal_cost_queue_tie"]["collapse_trace"]
    assert tie["trace_scope"] == "topology_priority_queue_trace_fixture"
    assert tie["initial_edge_count"] == 2
    assert tie["target_primitive_count"] == 1
    first_candidate, second_candidate = tie["initial_candidates"]
    assert first_candidate["weighted_priority_cost"] == second_candidate[
        "weighted_priority_cost"
    ]
    assert first_candidate["paper_base_cost"] == second_candidate["paper_base_cost"]
    assert first_candidate["queue_key"][2:] < second_candidate["queue_key"][2:]
    assert first_candidate["left_primitive"] == second_candidate["left_primitive"]
    assert first_candidate["right_primitive"] == second_candidate["right_primitive"]
    assert first_candidate["merged_primitive"] == second_candidate["merged_primitive"]
    assert tie["events"][0]["event_kind"] == "accepted_merge"
    assert tie["events"][0]["source_faces_left"] == [0]
    assert tie["events"][0]["source_faces_right"] == [1]
    assert tie["events"][1]["event_kind"] == "eager_stale_prune"
    assert tie["events"][1]["stale_entry"] is True
    assert tie["events"][1]["source_faces_left"] == [0]
    assert tie["events"][1]["source_faces_right"] == [2]
    assert tie["events"][2]["event_kind"] == "accepted_merge"
    assert tie["events"][2]["source_faces_left"] == [0, 1]
    assert tie["events"][2]["source_faces_right"] == [2]
    assert len(tie["events"]) == 3
    assert tie["accepted_merge_count"] == 2
    assert tie["stale_entry_skipped_count"] == 1
    assert tie["final_active_groups"] == [[0, 1, 2]]
    assert _event_signature(tie) == [
        ("accepted_merge", [0], [1], True, False, False),
        ("eager_stale_prune", [0], [2], False, True, False),
        ("accepted_merge", [0, 1], [2], True, False, False),
    ]
    assert _event_signature(tie) == _event_signature(tie_again)

    blocked = cases["paper_nonzero_threshold_block"]["collapse_trace"]
    assert blocked["trace_scope"] == "component_pair_priority_queue_trace_fixture"
    assert blocked["component_pair_edge_insertion_triggered"] is True
    assert blocked["topology_queue_exhausted_before_component_pair_insertion"] is True
    assert blocked["threshold_policy"] == "component_pair_paper_base_cost_lte_threshold"
    assert blocked["excess_volume_threshold"] == 1e-6
    assert blocked["accepted_merge_count"] == 0
    assert blocked["blocked_merge_count"] == 1
    assert blocked["stop_reason"] == "all_remaining_edges_blocked_by_threshold"
    blocked_events = [
        event
        for event in blocked["events"]
        if event["event_kind"] == "blocked_by_threshold"
    ]
    assert len(blocked_events) == 1
    blocked_event = blocked_events[0]
    assert blocked_event["edge_source"] == "component_pair"
    assert blocked_event["threshold_metric"] == "paper_base_cost"
    assert blocked_event["threshold_value"] == 1e-6
    assert blocked_event["paper_base_cost"] > blocked_event["threshold_value"] > 0.0
    assert blocked_event["blocked_reason"] == "component_pair_threshold_exceeded"


def test_cpd_paper_offline_report_records_fixture_breadth_batch_d():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    expected_case_ids = {
        "paper_component_pair_multi_candidate_order",
        "paper_component_pair_cap_skipped",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_d"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        trace = case["collapse_trace"]
        assert trace["trace_scope"] == "component_pair_priority_queue_trace_fixture"
        assert trace["component_pair_edge_insertion_triggered"] is True
        assert trace["topology_queue_exhausted_before_component_pair_insertion"] is True
        assert trace["initial_edge_count"] == 0
        assert trace["initial_candidates"] == []
        assert trace["package_generation_triggered"] is False
        assert trace["newton_runtime_triggered"] is False
        assert trace["real_usd_triggered"] is False
        assert trace["benchmark_triggered"] is False

    multi = cases["paper_component_pair_multi_candidate_order"]["collapse_trace"]
    assert multi["target_primitive_count"] == 2
    assert multi["threshold_policy"] == "disabled"
    assert multi["component_pair_candidate_cap"] == "all_pairs_for_fixture"
    assert multi["component_pair_available_pair_count"] == 3
    assert multi["component_pair_candidate_count"] == 3
    assert multi["skipped_component_pair_count"] == 0
    assert multi["skipped_component_pair_keys"] == []
    assert len(multi["component_pair_candidates"]) == 3
    assert all(
        candidate["edge_source"] == "component_pair"
        for candidate in multi["component_pair_candidates"]
    )
    selected = [event for event in multi["events"] if event["accepted"]][0]
    min_candidate = min(
        multi["component_pair_candidates"],
        key=lambda candidate: candidate["queue_key"],
    )
    assert selected["queue_key"] == min_candidate["queue_key"]
    assert selected["source_faces_merged"] == min_candidate["source_faces_merged"]
    assert multi["accepted_merge_count"] == 1
    assert multi["blocked_merge_count"] == 0
    assert multi["component_pair_attempted_pair_count"] == 1
    assert multi["stop_reason"] == "target_count_reached"
    assert len(multi["final_active_groups"]) == 2

    capped = cases["paper_component_pair_cap_skipped"]["collapse_trace"]
    assert capped["target_primitive_count"] == 3
    assert capped["threshold_policy"] == "disabled"
    assert capped["component_pair_candidate_cap"] == 2
    assert capped["component_pair_available_pair_count"] == 6
    assert capped["component_pair_candidate_count"] == 2
    assert capped["skipped_component_pair_count"] == 4
    assert len(capped["skipped_component_pair_keys"]) == 4
    assert len(capped["component_pair_candidates"]) == 2
    assert all(
        candidate["edge_source"] == "component_pair"
        for candidate in capped["component_pair_candidates"]
    )
    assert all(
        skipped["skip_reason"] == "component_pair_candidate_cap_reached"
        for skipped in capped["skipped_component_pair_keys"]
    )
    assert capped["component_pair_attempted_pair_count"] == 1
    assert capped["accepted_merge_count"] == 1
    assert capped["blocked_merge_count"] == 0
    assert capped["stop_reason"] == "target_count_reached"
    assert len(capped["final_active_groups"]) == 3


def test_cpd_paper_offline_report_records_fixture_breadth_batch_e():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    expected_case_ids = {
        "paper_rotated_nested_primitive",
        "paper_cross_type_enclosure_boundary",
    }
    assert expected_case_ids.issubset(cases)
    for case_id in expected_case_ids:
        case = cases[case_id]
        assert case["fixture_breadth_batch"] == "paper_fixture_breadth_batch_e"
        assert case["package_generation_triggered"] is False
        assert case["newton_runtime_triggered"] is False
        assert case["real_usd_triggered"] is False
        assert case["benchmark_triggered"] is False
        postprocess = case["postprocess_audit"]
        assert postprocess["package_generation_triggered"] is False
        assert postprocess["newton_runtime_triggered"] is False
        assert postprocess["real_usd_triggered"] is False
        assert postprocess["benchmark_triggered"] is False

    rotated = cases["paper_rotated_nested_primitive"]["postprocess_audit"]
    assert rotated["audit_scope"] == "enclosed_primitive_culling_fixture"
    assert rotated["fixture_variant"] == "rotated_nested_obb"
    assert rotated["containment_test_type"] == "obb_corners_inside_obb"
    assert rotated["axis_policy"] == "shared_rotated_axes"
    assert rotated["input_primitive_count"] == 2
    assert rotated["output_primitive_count"] == 1
    assert rotated["culled_primitive_ids"] == [1]
    assert rotated["kept_primitive_ids"] == [0]
    assert rotated["rotation_degrees_about_z"] == 30.0
    assert rotated["rotated_axes_non_identity"] is True
    assert rotated["input_primitives"][0]["axes"] == rotated["input_primitives"][1]["axes"]
    assert rotated["input_primitives"][0]["axes"] != [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    assert rotated["cull_records"] == [
        {
            "culled_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "cull_reason": "primitive_enclosed_by_larger_primitive",
            "containment_passed": True,
            "tested_corner_count": 8,
        }
    ]

    cross_type = cases["paper_cross_type_enclosure_boundary"]["postprocess_audit"]
    assert cross_type["audit_scope"] == "enclosed_primitive_cross_type_boundary_fixture"
    assert cross_type["fixture_variant"] == "cross_type_unsupported_boundary"
    assert cross_type["containment_test_type"] == "cross_type_containment_unsupported"
    assert cross_type["cross_type_culling_supported"] is False
    assert cross_type["unsupported_containment_label"] == (
        "cross_type_enclosure_boundary_not_supported"
    )
    assert cross_type["top_level_failure_label"] is False
    assert cross_type["input_primitive_count"] == 2
    assert cross_type["output_primitive_count"] == 2
    assert cross_type["culled_primitive_ids"] == []
    assert cross_type["kept_primitive_ids"] == [0, 1]
    assert cross_type["cull_records"] == []
    assert cross_type["unsupported_records"] == [
        {
            "candidate_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "candidate_kind": "sphere",
            "enclosing_kind": "oriented_bounding_box",
            "unsupported_reason": "cross_type_containment_not_implemented_for_fixture",
        }
    ]


def test_cpd_paper_offline_report_records_fixture_breadth_completion_review():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert "paper_fixture_breadth_completion_review" in report["paper_faithfulness"][
        "implemented_fixture_scope"
    ]

    review = report["paper_fixture_breadth_completion_review"]
    assert review["review_scope"] == "synthetic_fixture_breadth_batches_a_to_e"
    assert review["closed_gate"] == "paper_fixture_breadth_expansion"
    assert review["decision"] == "remain_partial"
    assert review["decision_reason"] == "fixture_breadth_complete_but_generalization_missing"
    assert review["fixture_breadth_plan_complete"] is True
    assert review["paper_faithful_offline_allowed"] is False
    assert review["next_required_gate"] == "paper_faithful_offline_generalization_plan"
    assert review["package_generation_triggered"] is False
    assert review["newton_runtime_triggered"] is False
    assert review["real_usd_triggered"] is False
    assert review["benchmark_triggered"] is False

    expected_batches = [
        {
            "batch_id": "paper_fixture_breadth_batch_a",
            "purpose": "source_preprocess_intake_operator_breadth",
            "case_ids": [
                "paper_mixed_face_preprocess_operator",
                "paper_degenerate_preprocess_face_drop",
                "paper_concave_polygon_rejected",
            ],
            "primary_criteria": [
                "source_mesh_and_preprocessing_policy",
                "source_face_intake_policy",
                "operator_q_audit",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_b",
            "purpose": "primitive_fit_breadth",
            "case_ids": [
                "paper_rotated_box_fit",
                "paper_offset_sphere_fit",
                "paper_off_axis_capsule_fit",
                "paper_flat_capped_cylinder_axis_fit",
                "paper_tapered_frustum_fit",
                "paper_asymmetric_trapezoid_fit",
            ],
            "primary_criteria": [
                "primitive_vocabulary_and_fit",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_c",
            "purpose": "cost_search_stop_breadth",
            "case_ids": [
                "paper_branching_cost_order",
                "paper_equal_cost_queue_tie",
                "paper_nonzero_threshold_block",
            ],
            "primary_criteria": [
                "paper_collapse_cost_and_weighting",
                "greedy_priority_queue_trace",
                "target_count_and_threshold_stop",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_d",
            "purpose": "component_pair_breadth",
            "case_ids": [
                "paper_component_pair_multi_candidate_order",
                "paper_component_pair_cap_skipped",
            ],
            "primary_criteria": [
                "component_pair_edge_handling",
                "target_count_and_threshold_stop",
            ],
        },
        {
            "batch_id": "paper_fixture_breadth_batch_e",
            "purpose": "postprocess_breadth",
            "case_ids": [
                "paper_rotated_nested_primitive",
                "paper_cross_type_enclosure_boundary",
            ],
            "primary_criteria": [
                "enclosed_primitive_postprocess",
            ],
        },
    ]
    assert review["completed_batches"] == expected_batches
    cases_by_batch = {}
    for case in report["cases"]:
        batch = case.get("fixture_breadth_batch")
        if batch is not None:
            cases_by_batch.setdefault(batch, []).append(case["case_id"])
    assert cases_by_batch == {
        batch["batch_id"]: batch["case_ids"] for batch in expected_batches
    }
    assert review["remaining_blocking_criteria_ids"] == EXPECTED_SCOPE_AUDIT_BLOCKERS
    assert [row["criterion_id"] for row in review["criteria_after_completion"]] == (
        EXPECTED_SCOPE_AUDIT_BLOCKERS
    )
    assert all(
        row["status_after_completion"] == "partial_fixture_scope"
        for row in review["criteria_after_completion"]
    )
    assert all(
        row["remaining_gap"] == "paper_faithful_offline_generalization"
        for row in review["criteria_after_completion"]
    )


def test_cpd_paper_offline_report_records_generalization_plan_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert "paper_faithful_offline_generalization_plan" not in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_faithful_offline_generalization_plan" in report[
        "paper_faithfulness"
    ]["implemented_planning_scope"]

    plan = report["paper_faithful_offline_generalization_plan"]
    assert (
        plan["plan_scope"]
        == "offline_algorithm_generalization_beyond_named_toy_fixtures"
    )
    assert plan["closed_gate"] == "paper_faithful_offline_generalization_plan"
    assert plan["decision"] == "remain_partial"
    assert (
        plan["decision_reason"]
        == "changed_decomposition_output_contract_complete_package_adapter_contract_missing"
    )
    assert plan["generalization_plan_complete"] is True
    assert plan["paper_faithful_offline_allowed"] is False
    assert plan["next_required_gate"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert plan["package_generation_triggered"] is False
    assert plan["newton_runtime_triggered"] is False
    assert plan["real_usd_triggered"] is False
    assert plan["benchmark_triggered"] is False

    expected_batches = [
        {
            "batch_id": "paper_generalization_batch_a_source_policy",
            "purpose": "generalize_source_mesh_preprocess_intake_operator_policy",
            "primary_criteria": [
                "source_mesh_and_preprocessing_policy",
                "source_face_intake_policy",
                "operator_q_audit",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "source_policy_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_b_primitive_fit_engine",
            "purpose": "generalize_paper_primitive_fit_engine_beyond_named_cases",
            "primary_criteria": [
                "primitive_vocabulary_and_fit",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "primitive_fit_engine_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_c_search_engine",
            "purpose": "generalize_cost_queue_threshold_and_component_pair_search",
            "primary_criteria": [
                "paper_collapse_cost_and_weighting",
                "greedy_priority_queue_trace",
                "target_count_and_threshold_stop",
                "component_pair_edge_handling",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "search_engine_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_d_postprocess_policy",
            "purpose": "generalize_enclosed_primitive_postprocess_policy",
            "primary_criteria": [
                "enclosed_primitive_postprocess",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "postprocess_policy_generalization_report",
        },
        {
            "batch_id": "paper_generalization_batch_e_package_boundary_readiness",
            "purpose": "review_offline_package_boundary_readiness_after_changed_decomposition",
            "primary_criteria": [
                "package_generation_boundary",
                "newton_runtime_boundary",
                "real_usd_boundary",
                "benchmark_evaluation_boundary",
            ],
            "implementation_boundary": "planning_only_no_package_or_newton",
            "required_output": "package_boundary_readiness_review",
        },
    ]
    assert plan["planned_batches"] == expected_batches
    assert plan["first_unresolved_gate"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert plan["remaining_generalization_gates"] == []
    assert plan["blocked_runtime_gates"] == [
        "package_generation_boundary",
        "newton_runtime_boundary",
        "real_usd_boundary",
        "benchmark_evaluation_boundary",
    ]


def test_cpd_paper_offline_report_records_source_policy_generalization_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert EXPECTED_CLOSED_SOURCE_POLICY_GATE in report["paper_faithfulness"][
        "implemented_generalization_scope"
    ]
    assert EXPECTED_CLOSED_PRIMITIVE_FIT_GATE in report["paper_faithfulness"][
        "implemented_generalization_scope"
    ]
    assert EXPECTED_CLOSED_SEARCH_ENGINE_GATE in report["paper_faithfulness"][
        "implemented_generalization_scope"
    ]
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"

    payload = report["paper_generalization_batch_a_source_policy"]
    assert payload["gate_id"] == "paper_generalization_batch_a_source_policy"
    assert payload["gate_status"] == "implemented_offline_report_only_partial"
    assert payload["closed_gate"] == "paper_generalization_batch_a_source_policy"
    assert payload["next_required_gate"] == "paper_generalization_batch_b_primitive_fit_engine"
    assert payload["decision"] == "remain_partial"
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["source_scope"] == "synthetic_in_memory_source_mesh_policy_matrix"
    assert payload["implementation_boundary"] == "offline_report_only_no_package_or_newton"
    assert payload["source_mesh_contract"] == {
        "accepted_source_representation": "vertices_plus_variable_arity_source_faces",
        "source_face_id_policy": "preserve_source_face_ids_distinct_from_generated_triangle_ids",
        "general_mesh_cleanup_supported": False,
    }
    assert payload["preprocessing_policy"]["deduplication_policy"] == (
        "exact_coordinate_first_occurrence_only"
    )
    assert payload["preprocessing_policy"]["distance_tolerance"] == 0.0
    assert payload["preprocessing_policy"]["degenerate_face_policy"] == (
        "drop_after_exact_deduplication_from_executable_rows"
    )
    assert payload["source_face_intake_policy"]["accepted_preconditions"] == [
        "planar",
        "convex",
        "non_degenerate",
        "consistently_wound",
    ]
    assert payload["source_face_intake_policy"]["triangulation_policy"] == (
        "fan_from_first_vertex"
    )
    assert payload["source_face_intake_policy"]["unsupported_policy"] == (
        "reject_concave_polygon_without_top_level_failure_label"
    )
    assert payload["operator_policy"]["triangle_operator_policy"] == (
        "compute_q_on_executable_triangles"
    )
    assert payload["operator_policy"]["source_face_aggregate_policy"] == (
        "sum_generated_triangle_q_rows_to_source_face"
    )
    assert [row["policy_row_id"] for row in payload["policy_matrix"]] == [
        "accepted_mixed_triangle_quad_polygon_exact_dedup",
        "accepted_degenerate_after_exact_dedup_drop",
        "rejected_concave_polygon",
    ]
    assert payload["coverage_summary"] == {
        "evidence_case_count": 3,
        "accepted_policy_row_count": 2,
        "unsupported_policy_row_count": 1,
        "closed_gate_count": 1,
        "remaining_generalization_gate_count": 4,
    }
    assert payload["remaining_gaps"] == EXPECTED_SOURCE_POLICY_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False


def test_cpd_paper_offline_report_records_primitive_fit_engine_generalization_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"

    payload = report["paper_generalization_batch_b_primitive_fit_engine"]
    assert payload["gate_id"] == EXPECTED_CLOSED_PRIMITIVE_FIT_GATE
    assert payload["gate_status"] == "implemented_offline_report_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_PRIMITIVE_FIT_GATE
    assert payload["next_required_gate"] == "paper_generalization_batch_c_search_engine"
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "primitive_fit_engine_generalization_complete_search_engine_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["source_scope"] == "deterministic_in_memory_parametric_primitive_fit_probes"
    assert payload["implementation_boundary"] == "offline_report_only_no_package_or_newton"
    assert payload["engine_contract"] == {
        "input_contract": "TriangleMesh_plus_face_group",
        "candidate_set": [
            "oriented_bounding_box",
            "sphere",
            "capsule",
            "capped_cylinder",
            "frustum",
            "trapezoidal_prism",
        ],
        "candidate_evaluation_policy": "evaluate_all_candidates_no_runtime_mapping",
        "selection_rule": "min_paper_weighted_volume_then_candidate_order",
        "containment_scope": "assigned_vertices_only_not_surface_or_collision_quality",
        "axis_policy": "paper_q_eigenbasis_with_candidate_axis_enumeration",
        "offline_only_unmapped_primitives": [
            "capped_cylinder",
            "frustum",
            "trapezoidal_prism",
        ],
    }
    assert payload["coverage_summary"] == {
        "primitive_count": 6,
        "probe_family_count": 6,
        "generated_probe_count": 6,
        "candidate_row_count": 36,
        "closed_gate_count": 2,
        "remaining_generalization_gate_count": 3,
    }
    assert payload["remaining_gaps"] == EXPECTED_PRIMITIVE_FIT_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "timing" not in payload
    assert "surface_distance" not in payload
    assert "collision_quality" not in payload
    assert "benchmark" not in payload

    expected_target_primitives = [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    rows = payload["primitive_family_matrix"]
    assert [row["target_paper_primitive"] for row in rows] == expected_target_primitives
    assert {row["probe_id"] for row in rows} == {
        "paper_fit_engine_rotated_obb_probe",
        "paper_fit_engine_offset_sphere_probe",
        "paper_fit_engine_off_axis_capsule_probe",
        "paper_fit_engine_flat_capped_cylinder_probe",
        "paper_fit_engine_tapered_frustum_probe",
        "paper_fit_engine_asymmetric_trapezoid_probe",
    }
    for row in rows:
        assert row["candidate_row_count"] == 6
        assert row["candidate_order"] == expected_target_primitives
        assert row["missing_paper_primitives"] == []
        assert row["target_candidate"]["paper_primitive"] == row["target_paper_primitive"]
        assert row["selected_candidate"]["paper_primitive"] in expected_target_primitives
        assert "target_candidate_selected" in row
        assert row["contains_assigned_points"] is True
        assert row["finite_numeric_fields"] is True
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False
        assert _axes_are_orthonormal(row["target_candidate"]["axes"])

    runtime_by_primitive = {
        row["target_paper_primitive"]: row["newton_runtime_kind"] for row in rows
    }
    assert runtime_by_primitive["oriented_bounding_box"] == "box"
    assert runtime_by_primitive["sphere"] == "sphere"
    assert runtime_by_primitive["capsule"] == "capsule"
    assert runtime_by_primitive["capped_cylinder"] == "offline_only_unmapped"
    assert runtime_by_primitive["frustum"] == "offline_only_unmapped"
    assert runtime_by_primitive["trapezoidal_prism"] == "offline_only_unmapped"


def test_cpd_paper_offline_report_records_search_engine_generalization_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"

    payload = report["paper_generalization_batch_c_search_engine"]
    assert payload["gate_id"] == EXPECTED_CLOSED_SEARCH_ENGINE_GATE
    assert payload["gate_status"] == "implemented_offline_report_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_SEARCH_ENGINE_GATE
    assert payload["next_required_gate"] == "paper_generalization_batch_d_postprocess_policy"
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "search_engine_generalization_complete_postprocess_policy_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["source_scope"] == "deterministic_in_memory_search_trace_probes"
    assert payload["implementation_boundary"] == "offline_report_only_no_package_or_newton"
    assert payload["search_engine_contract"] == {
        "input_contract": (
            "TriangleMesh_plus_initial_face_groups_target_count_and_search_policy"
        ),
        "primary_policy": "paper_greedy_min_weighted_priority_cost_no_lookahead",
        "cost_fields": ["paper_base_cost", "weighted_priority_cost"],
        "queue_key_fields": [
            "weighted_priority_cost",
            "paper_base_cost",
            "source_faces_left",
            "source_faces_right",
            "insertion_order",
        ],
        "candidate_sources": ["topology", "component_pair"],
        "component_pair_insertion_policy": (
            "insert_when_topology_queue_exhausted_before_target"
        ),
        "threshold_metric": "paper_base_cost",
        "stop_reasons": [
            "target_count_reached",
            "all_remaining_edges_blocked_by_threshold",
            "queue_exhausted_before_target_count",
        ],
        "lookahead_used": False,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
    }
    assert payload["coverage_summary"] == {
        "search_trace_row_count": 8,
        "topology_trace_row_count": 3,
        "component_pair_trace_row_count": 5,
        "threshold_blocked_row_count": 2,
        "closed_gate_count": 3,
        "remaining_generalization_gate_count": 2,
    }
    assert payload["remaining_gaps"] == EXPECTED_SEARCH_ENGINE_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "timing" not in payload
    assert "surface_distance" not in payload
    assert "collision_quality" not in payload
    assert "benchmark" not in payload

    assert [row["row_id"] for row in payload["search_trace_matrix"]] == [
        "topology_chain_target_count",
        "weighted_priority_over_base_cost",
        "equal_cost_queue_tie",
        "component_pair_threshold_disabled_accept",
        "component_pair_zero_threshold_block",
        "component_pair_positive_threshold_block",
        "component_pair_multi_candidate_order",
        "component_pair_candidate_cap_skipped",
    ]
    for row in payload["search_trace_matrix"]:
        assert row["row_status"] == "implemented_offline_search_trace_fixture"
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_search_engine_generalization_rows_match_case_payloads():
    report = build_cpd_paper_offline_report()
    report_again = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}
    rows = {
        row["row_id"]: row
        for row in report["paper_generalization_batch_c_search_engine"][
            "search_trace_matrix"
        ]
    }

    expected_case_by_row = {
        "topology_chain_target_count": "paper_three_face_chain",
        "weighted_priority_over_base_cost": "paper_branching_cost_order",
        "equal_cost_queue_tie": "paper_equal_cost_queue_tie",
        "component_pair_threshold_disabled_accept": "paper_disconnected_components",
        "component_pair_zero_threshold_block": "paper_component_pair_threshold_blocked",
        "component_pair_positive_threshold_block": "paper_nonzero_threshold_block",
        "component_pair_multi_candidate_order": (
            "paper_component_pair_multi_candidate_order"
        ),
        "component_pair_candidate_cap_skipped": "paper_component_pair_cap_skipped",
    }
    assert set(rows) == set(expected_case_by_row)

    for row_id, case_id in expected_case_by_row.items():
        row = rows[row_id]
        trace = cases[case_id]["collapse_trace"]
        assert row["evidence_case_id"] == case_id
        assert row["trace_scope"] == trace["trace_scope"]
        assert row["priority_queue_policy"] == trace["priority_queue_policy"]
        assert row["target_primitive_count"] == trace["target_primitive_count"]
        assert row["initial_edge_count"] == trace["initial_edge_count"]
        assert row["initial_candidate_count"] == len(trace["initial_candidates"])
        assert row["component_pair_candidate_count"] == trace[
            "component_pair_candidate_count"
        ]
        assert row["component_pair_available_pair_count"] == trace[
            "component_pair_available_pair_count"
        ]
        assert row["component_pair_candidate_cap"] == trace[
            "component_pair_candidate_cap"
        ]
        assert row["skipped_component_pair_count"] == trace[
            "skipped_component_pair_count"
        ]
        assert row["threshold_policy"] == trace["threshold_policy"]
        assert row["excess_volume_threshold"] == trace["excess_volume_threshold"]
        assert row["accepted_merge_count"] == trace["accepted_merge_count"]
        assert row["blocked_merge_count"] == trace["blocked_merge_count"]
        assert row["stale_entry_skipped_count"] == trace[
            "stale_entry_skipped_count"
        ]
        assert row["event_count"] == len(trace["events"])
        assert row["event_kinds"] == [event["event_kind"] for event in trace["events"]]
        assert row["stop_reason"] == trace["stop_reason"]
        assert row["final_active_groups"] == trace["final_active_groups"]
        assert row["component_pair_edge_insertion_triggered"] == trace[
            "component_pair_edge_insertion_triggered"
        ]
        assert row["topology_queue_exhausted_before_component_pair_insertion"] == (
            trace["topology_queue_exhausted_before_component_pair_insertion"]
        )
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

        first_accepted = next(
            (event for event in trace["events"] if event["accepted"]), None
        )
        if first_accepted is None:
            assert row["first_accepted_queue_key"] is None
        else:
            assert row["first_accepted_queue_key"] == first_accepted["queue_key"]

        blocked_events = [
            event
            for event in trace["events"]
            if event["event_kind"] == "blocked_by_threshold"
        ]
        assert row["threshold_metric"] == (
            blocked_events[0]["threshold_metric"] if blocked_events else None
        )
        for candidate in [
            *trace["initial_candidates"],
            *trace["component_pair_candidates"],
            *trace["events"],
        ]:
            _assert_queue_key_contract(candidate)
            assert isfinite(candidate["paper_base_cost"])
            assert isfinite(candidate["weighted_priority_cost"])
        for event in trace["events"]:
            if event["accepted"]:
                assert event["resulting_source_faces"]
            if event["event_kind"] == "blocked_by_threshold":
                assert event["threshold_metric"] == "paper_base_cost"
                assert event["active_primitive_count_before"] == event[
                    "active_primitive_count_after"
                ]
                assert "resulting_source_faces" not in event

    branching = cases["paper_branching_cost_order"]["collapse_trace"]
    first_accepted = [event for event in branching["events"] if event["accepted"]][0]
    min_weighted = min(
        branching["initial_candidates"], key=lambda candidate: candidate["queue_key"]
    )
    min_base = min(
        branching["initial_candidates"],
        key=lambda candidate: candidate["paper_base_cost"],
    )
    assert first_accepted["queue_key"] == min_weighted["queue_key"]
    assert min_weighted["queue_key"] != min_base["queue_key"]

    equal_cost = cases["paper_equal_cost_queue_tie"]["collapse_trace"]
    equal_cost_again = {
        case["case_id"]: case for case in report_again["cases"]
    }["paper_equal_cost_queue_tie"]["collapse_trace"]
    assert "eager_stale_prune" in rows["equal_cost_queue_tie"]["event_kinds"]
    assert _event_signature(equal_cost) == _event_signature(equal_cost_again)

    nonzero_block = rows["component_pair_positive_threshold_block"]
    assert nonzero_block["threshold_metric"] == "paper_base_cost"
    assert nonzero_block["first_accepted_queue_key"] is None
    assert nonzero_block["blocked_merge_count"] == 1
    assert nonzero_block["stop_reason"] == "all_remaining_edges_blocked_by_threshold"

    zero_block = rows["component_pair_zero_threshold_block"]
    assert zero_block["threshold_metric"] == "paper_base_cost"
    assert zero_block["first_accepted_queue_key"] is None
    assert zero_block["blocked_merge_count"] == 1

    multi_candidate = rows["component_pair_multi_candidate_order"]
    assert multi_candidate["component_pair_candidate_count"] == 3
    assert multi_candidate["component_pair_available_pair_count"] == 3
    assert multi_candidate["topology_queue_exhausted_before_component_pair_insertion"] is True

    capped = rows["component_pair_candidate_cap_skipped"]
    assert capped["component_pair_candidate_cap"] == 2
    assert capped["component_pair_candidate_count"] == 2
    assert capped["skipped_component_pair_count"] == 4


def test_cpd_paper_offline_report_records_postprocess_policy_generalization_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"

    payload = report["paper_generalization_batch_d_postprocess_policy"]
    assert payload["gate_id"] == EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE
    assert payload["gate_status"] == "implemented_offline_report_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE
    assert (
        payload["next_required_gate"]
        == "paper_generalization_batch_e_package_boundary_readiness"
    )
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "postprocess_policy_generalization_complete_package_boundary_readiness_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["source_scope"] == "deterministic_in_memory_postprocess_audit_fixtures"
    assert payload["implementation_boundary"] == "offline_report_only_no_package_or_newton"
    assert payload["postprocess_policy_contract"] == {
        "input_contract": "explicit_offline_postprocess_audit_primitives_not_search_output",
        "supported_containment_tests": ["obb_corners_inside_obb"],
        "supported_axis_policies": ["shared_identity_axes", "shared_rotated_axes"],
        "unsupported_boundary_policy": "record_cross_type_unsupported_without_silent_cull",
        "unsupported_boundary_label": "cross_type_enclosure_boundary_not_supported",
        "output_accounting_fields": [
            "input_primitive_count",
            "output_primitive_count",
            "kept_primitive_ids",
            "culled_primitive_ids",
            "cull_records",
            "unsupported_records",
        ],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
    }
    assert payload["coverage_summary"] == {
        "postprocess_row_count": 3,
        "obb_cull_row_count": 2,
        "rotated_obb_row_count": 1,
        "unsupported_cross_type_row_count": 1,
        "cull_record_count": 2,
        "unsupported_record_count": 1,
        "closed_gate_count": 4,
        "remaining_generalization_gate_count": 1,
    }
    assert payload["remaining_gaps"] == EXPECTED_POSTPROCESS_POLICY_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "timing" not in payload
    assert "surface_distance" not in payload
    assert "collision_quality" not in payload
    assert "benchmark" not in payload

    assert [row["row_id"] for row in payload["postprocess_policy_matrix"]] == [
        "identity_nested_obb_cull",
        "rotated_nested_obb_cull",
        "cross_type_enclosure_no_silent_cull_boundary",
    ]
    for row in payload["postprocess_policy_matrix"]:
        assert row["row_status"] == "implemented_offline_postprocess_fixture"
        assert (
            row["claim_boundary"]
            == "summarizes_named_postprocess_audits_not_general_containment_library"
        )
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False
        assert "input_primitives" not in row


def test_cpd_paper_postprocess_policy_generalization_rows_match_case_payloads():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}
    rows = {
        row["row_id"]: row
        for row in report["paper_generalization_batch_d_postprocess_policy"][
            "postprocess_policy_matrix"
        ]
    }

    expected_case_by_row = {
        "identity_nested_obb_cull": "paper_nested_primitive",
        "rotated_nested_obb_cull": "paper_rotated_nested_primitive",
        "cross_type_enclosure_no_silent_cull_boundary": (
            "paper_cross_type_enclosure_boundary"
        ),
    }
    assert set(rows) == set(expected_case_by_row)

    for row_id, case_id in expected_case_by_row.items():
        row = rows[row_id]
        postprocess = cases[case_id]["postprocess_audit"]
        assert row["evidence_case_id"] == case_id
        assert row["audit_scope"] == postprocess["audit_scope"]
        assert row["fixture_variant"] == postprocess["fixture_variant"]
        assert row["postprocess_input_source"] == postprocess[
            "postprocess_input_source"
        ]
        assert row["postprocess_policy"] == postprocess["postprocess_policy"]
        assert row["containment_test_type"] == postprocess["containment_test_type"]
        assert row["axis_policy"] == postprocess.get("axis_policy")
        assert row["rotation_degrees_about_z"] == postprocess.get(
            "rotation_degrees_about_z"
        )
        assert row["rotated_axes_non_identity"] == postprocess.get(
            "rotated_axes_non_identity"
        )
        assert row["cross_type_culling_supported"] == postprocess.get(
            "cross_type_culling_supported"
        )
        assert row["unsupported_containment_label"] == postprocess.get(
            "unsupported_containment_label"
        )
        assert row["input_primitive_count"] == postprocess["input_primitive_count"]
        assert row["output_primitive_count"] == postprocess["output_primitive_count"]
        assert row["culled_primitive_ids"] == postprocess["culled_primitive_ids"]
        assert row["kept_primitive_ids"] == postprocess["kept_primitive_ids"]
        assert row["enclosed_primitive_ids"] == postprocess["enclosed_primitive_ids"]
        assert row["enclosing_primitive_ids"] == postprocess["enclosing_primitive_ids"]
        assert row["cull_record_count"] == len(postprocess["cull_records"])
        assert row["unsupported_record_count"] == len(
            postprocess.get("unsupported_records", [])
        )
        assert row["top_level_failure_label"] == postprocess.get(
            "top_level_failure_label", False
        )
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    identity = rows["identity_nested_obb_cull"]
    assert identity["axis_policy"] == "shared_identity_axes"
    assert identity["cull_record_count"] == 1
    assert identity["culled_primitive_ids"] == [1]
    assert identity["output_primitive_count"] == identity["input_primitive_count"] - 1

    rotated = rows["rotated_nested_obb_cull"]
    assert rotated["axis_policy"] == "shared_rotated_axes"
    assert rotated["rotated_axes_non_identity"] is True
    assert rotated["rotation_degrees_about_z"] == 30.0
    assert rotated["cull_record_count"] == 1
    assert rotated["culled_primitive_ids"] == [1]

    cross_type = rows["cross_type_enclosure_no_silent_cull_boundary"]
    assert cross_type["cross_type_culling_supported"] is False
    assert (
        cross_type["unsupported_containment_label"]
        == "cross_type_enclosure_boundary_not_supported"
    )
    assert cross_type["cull_record_count"] == 0
    assert cross_type["unsupported_record_count"] == 1
    assert cross_type["top_level_failure_label"] is False
    assert cross_type["culled_primitive_ids"] == []
    assert cross_type["kept_primitive_ids"] == [0, 1]


def test_cpd_paper_offline_report_records_package_boundary_readiness_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"
    assert "paper_generalization_batch_e_package_boundary_readiness_missing" not in (
        report["failure_labels"]
    )

    payload = report["paper_generalization_batch_e_package_boundary_readiness"]
    assert payload["gate_id"] == EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE
    assert payload["gate_status"] == "implemented_planning_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE
    assert payload["next_required_gate"] == EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "package_boundary_readiness_review_complete_changed_decomposition_output_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["source_scope"] == "offline_generalization_payloads_after_batches_a_to_d"
    assert payload["implementation_boundary"] == "planning_only_no_package_or_newton"
    assert payload["boundary_review_contract"] == {
        "input_scope": "implemented_offline_generalization_payloads_a_to_d",
        "review_output": "package_boundary_readiness_matrix_not_package_generation",
        "changed_decomposition_output_contract_required": True,
        "package_generation_contract_required": True,
        "runtime_admissibility_required_after_package_conversion": True,
        "package_generation_allowed": False,
        "newton_runtime_allowed": False,
        "real_usd_allowed": False,
        "benchmark_allowed": False,
    }
    assert payload["coverage_summary"] == {
        "boundary_review_row_count": 5,
        "blocked_row_count": 5,
        "closed_gate_count": 5,
        "remaining_generalization_gate_count": 0,
        "package_generation_allowed_row_count": 0,
        "newton_runtime_allowed_row_count": 0,
        "real_usd_allowed_row_count": 0,
        "benchmark_allowed_row_count": 0,
    }
    assert payload["remaining_gaps"] == EXPECTED_PACKAGE_BOUNDARY_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "collision_quality" not in payload
    assert "surface_distance" not in payload
    assert "timing" not in payload

    assert [row["row_id"] for row in payload["boundary_review_matrix"]] == [
        "changed_decomposition_output_contract",
        "package_generation_boundary",
        "newton_runtime_boundary",
        "real_usd_boundary",
        "benchmark_evaluation_boundary",
    ]


def test_cpd_paper_package_boundary_readiness_keeps_runtime_work_blocked():
    report = build_cpd_paper_offline_report()
    payload = report["paper_generalization_batch_e_package_boundary_readiness"]

    forbidden_statuses = {
        "package_ready",
        "newton_ready",
        "runtime_ready",
        "benchmark_ready",
        "paper_faithful_offline",
    }
    for row in payload["boundary_review_matrix"]:
        assert row["row_status"] not in forbidden_statuses
        assert row["required_before_unlock"]
        assert row["current_evidence"]
        assert row["blocked_reason"]
        assert row["next_gate_if_blocked"]
        assert row["claim_boundary"]
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    rows = {row["row_id"]: row for row in payload["boundary_review_matrix"]}
    assert rows["changed_decomposition_output_contract"]["next_gate_if_blocked"] == (
        EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY
    )
    assert rows["package_generation_boundary"]["next_gate_if_blocked"] == (
        EXPECTED_PACKAGE_GENERATION_CONTRACT
    )
    assert rows["newton_runtime_boundary"]["next_gate_if_blocked"] == (
        "paper_newton_runtime_admissibility_gate"
    )
    assert rows["real_usd_boundary"]["next_gate_if_blocked"] == (
        "paper_real_usd_asset_scope_gate"
    )
    assert rows["benchmark_evaluation_boundary"]["next_gate_if_blocked"] == (
        "paper_benchmark_evaluation_design_gate"
    )


def test_cpd_paper_offline_report_records_changed_decomposition_output_contract_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert report["paper_faithfulness"]["implemented_output_contract_scope"] == [
        EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT,
        EXPECTED_PACKAGE_ADAPTER_CONTRACT,
        EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
        EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
        EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
        EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
    ]
    assert (
        report["paper_faithfulness"]["implemented_generalization_scope"]
        == EXPECTED_CLOSED_GENERALIZATION_GATES
    )
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"
    assert "paper_offline_changed_decomposition_output_contract_missing" not in (
        report["failure_labels"]
    )

    payload = report["paper_offline_changed_decomposition_output_contract"]
    assert payload["gate_id"] == EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT
    assert payload["gate_status"] == "implemented_offline_contract_only_partial"
    assert payload["closed_gate"] == EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT
    assert payload["next_required_gate"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "changed_decomposition_output_contract_complete_package_adapter_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == "offline_changed_decomposition_output_not_collision_package"
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert (
        payload["implementation_boundary"]
        == "offline_report_contract_no_collision_package_no_newton"
    )
    assert payload["output_contract"] == {
        "required_output_fields": [
            "output_id",
            "evidence_case_id",
            "source_mesh_summary",
            "search_summary",
            "primitive_records",
            "postprocess_state",
            "unsupported_boundaries",
            "claim_boundary",
        ],
        "primitive_record_fields": [
            "offline_primitive_id",
            "source_faces",
            "generated_triangle_face_ids",
            "source_face_ids",
            "paper_primitive",
            "center",
            "axes",
            "dimensions",
            "volume",
            "paper_weight",
            "weighted_volume",
            "contains_assigned_points",
            "newton_runtime_kind",
            "conversion_status",
        ],
        "conversion_status": "offline_contract_only_not_package_candidate",
    }
    assert payload["coverage_summary"] == {
        "decomposition_output_row_count": 9,
        "primitive_record_count": 16,
        "postprocess_state_row_count": 3,
        "source_policy_summary_row_count": 3,
        "primitive_family_count": 6,
        "search_trace_summary_row_count": 8,
        "package_boundary_row_count": 5,
    }
    assert payload["remaining_gaps"] == [EXPECTED_PACKAGE_ADAPTER_CONTRACT]
    assert len(payload["decomposition_output_rows"]) == 9
    assert len(payload["postprocess_state_rows"]) == 3
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "CollisionPackage" not in payload
    assert "PrimitiveSpec" not in payload
    assert "collision_quality" not in payload
    assert "surface_distance" not in payload
    assert "timing" not in payload


def test_cpd_paper_changed_decomposition_output_rows_match_search_case_payloads():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}
    payload = report["paper_offline_changed_decomposition_output_contract"]
    rows = payload["decomposition_output_rows"]

    assert [row["evidence_case_id"] for row in rows] == [
        "paper_three_face_chain",
        "paper_disconnected_components",
        "paper_component_pair_threshold_blocked",
        "paper_duplicate_vertex_preprocessing",
        "paper_branching_cost_order",
        "paper_equal_cost_queue_tie",
        "paper_nonzero_threshold_block",
        "paper_component_pair_multi_candidate_order",
        "paper_component_pair_cap_skipped",
    ]

    for row in rows:
        case = cases[row["evidence_case_id"]]
        trace = case["collapse_trace"]
        selected = case["primitive_fit_audit"]["selected"]
        assert row["output_id"] == f"{case['case_id']}:changed_decomposition_output"
        assert row["row_status"] == "implemented_offline_contract_row"
        assert row["source_mesh_summary"]["vertex_count"] == case["source_mesh"][
            "vertex_count"
        ]
        assert row["source_mesh_summary"]["face_count"] == case["source_mesh"][
            "face_count"
        ]
        assert row["source_mesh_summary"]["connected_component_count"] == case[
            "source_mesh"
        ]["connected_component_count"]
        assert row["search_summary"]["final_active_groups"] == trace[
            "final_active_groups"
        ]
        assert row["search_summary"]["target_primitive_count"] == trace[
            "target_primitive_count"
        ]
        assert row["search_summary"]["stop_reason"] == trace["stop_reason"]
        assert row["search_summary"]["accepted_merge_count"] == trace[
            "accepted_merge_count"
        ]
        assert row["search_summary"]["blocked_merge_count"] == trace[
            "blocked_merge_count"
        ]
        assert len(row["primitive_records"]) == len(trace["final_active_groups"])
        for index, primitive in enumerate(row["primitive_records"]):
            final_group = trace["final_active_groups"][index]
            assert primitive["offline_primitive_id"] == (
                f"{case['case_id']}:offline_primitive:{index}"
            )
            assert primitive["source_faces"] == final_group
            assert primitive["generated_triangle_face_ids"] == final_group
            assert primitive["source_face_ids"] == final_group
            assert primitive["paper_primitive"] == selected["paper_primitive"]
            assert primitive["center"] == selected["center"]
            assert primitive["axes"] == selected["axes"]
            assert primitive["dimensions"] == selected["dimensions"]
            assert primitive["volume"] == selected["volume"]
            assert primitive["paper_weight"] == selected["paper_weight"]
            assert primitive["weighted_volume"] == selected["weighted_volume"]
            assert primitive["contains_assigned_points"] == selected[
                "contains_assigned_points"
            ]
            assert primitive["newton_runtime_kind"] == selected["newton_runtime_kind"]
            assert (
                primitive["primitive_fit_scope"]
                == "case_selected_candidate_reused_for_contract_row_not_group_refit"
            )
            assert (
                primitive["conversion_status"]
                == "offline_contract_only_not_package_candidate"
            )
        assert row["postprocess_state"] == "not_applied_to_search_output"
        assert row["unsupported_boundaries"]["package_adapter_contract_required"] is True
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_changed_decomposition_contract_records_postprocess_state_without_applying_to_search_output():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}
    payload = report["paper_offline_changed_decomposition_output_contract"]
    rows = {row["evidence_case_id"]: row for row in payload["postprocess_state_rows"]}

    assert set(rows) == {
        "paper_nested_primitive",
        "paper_rotated_nested_primitive",
        "paper_cross_type_enclosure_boundary",
    }
    for case_id, row in rows.items():
        postprocess = cases[case_id]["postprocess_audit"]
        assert row["state_id"] == f"{case_id}:postprocess_state"
        assert (
            row["state_scope"]
            == "explicit_postprocess_audit_fixture_not_search_output"
        )
        assert row["postprocess_input_source"] == postprocess[
            "postprocess_input_source"
        ]
        assert row["postprocess_policy"] == postprocess["postprocess_policy"]
        assert row["kept_primitive_ids"] == postprocess["kept_primitive_ids"]
        assert row["culled_primitive_ids"] == postprocess["culled_primitive_ids"]
        assert row["cull_record_count"] == len(postprocess["cull_records"])
        assert row["unsupported_record_count"] == len(
            postprocess.get("unsupported_records", [])
        )
        assert row["unsupported_containment_label"] == postprocess.get(
            "unsupported_containment_label"
        )
        assert "input_primitives" not in row
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_offline_report_records_package_adapter_contract_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert report["paper_faithfulness"]["implemented_output_contract_scope"] == [
        EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT,
        EXPECTED_PACKAGE_ADAPTER_CONTRACT,
        EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
        EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
        EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
        EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT,
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT,
    ]
    assert report["paper_faithful_offline_supported"] is False
    assert report["status"] == "partial"
    assert "paper_package_adapter_contract_missing" not in report["failure_labels"]

    payload = report["paper_package_adapter_contract"]
    assert payload["gate_id"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert payload["gate_status"] == "implemented_offline_adapter_contract_only_partial"
    assert payload["closed_gate"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert payload["input_gate_id"] == EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT
    assert (
        payload["next_required_gate"]
        == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
    )
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "package_adapter_contract_complete_unsupported_primitive_policy_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == "offline_package_adapter_contract_not_collision_package"
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert (
        payload["implementation_boundary"]
        == "offline_adapter_contract_no_collision_package_no_newton"
    )
    assert payload["remaining_gaps"] == EXPECTED_PACKAGE_ADAPTER_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert "CollisionPackage" not in payload
    assert "PrimitiveSpec" not in payload


def test_cpd_paper_package_adapter_contract_summarizes_changed_decomposition_contract():
    report = build_cpd_paper_offline_report()
    changed = report["paper_offline_changed_decomposition_output_contract"]
    adapter = report["paper_package_adapter_contract"]

    assert adapter["input_contract_summary"] == {
        "input_gate_id": EXPECTED_CLOSED_CHANGED_DECOMPOSITION_CONTRACT,
        "input_artifact_kind": "offline_changed_decomposition_output_not_collision_package",
        "decomposition_output_row_count": changed["coverage_summary"][
            "decomposition_output_row_count"
        ],
        "primitive_record_count": changed["coverage_summary"]["primitive_record_count"],
        "postprocess_state_row_count": changed["coverage_summary"][
            "postprocess_state_row_count"
        ],
    }
    assert adapter["adapter_decision_contract"] == {
        "decision_values": [
            "adapter_eligible",
            "blocked",
            "later_policy_required",
        ],
        "current_direct_adapter_policy": "none_for_current_changed_decomposition_rows",
        "unsupported_primitive_policy_required": True,
        "package_generation_allowed": False,
    }
    assert adapter["coverage_summary"]["decomposition_output_row_count"] == len(
        changed["decomposition_output_rows"]
    )
    assert adapter["coverage_summary"]["primitive_decision_row_count"] == 16
    assert len(adapter["primitive_adapter_decision_rows"]) == 16


def test_cpd_paper_package_adapter_decision_counts_partition_current_records():
    report = build_cpd_paper_offline_report()
    adapter = report["paper_package_adapter_contract"]
    summary = adapter["coverage_summary"]

    assert summary["adapter_eligible_record_count"] == 0
    assert summary["blocked_record_count"] == 0
    assert summary["later_policy_required_record_count"] == 16
    assert summary["offline_only_unmapped_record_count"] == 16
    assert (
        summary["adapter_eligible_record_count"]
        + summary["blocked_record_count"]
        + summary["later_policy_required_record_count"]
        == summary["primitive_decision_row_count"]
    )
    assert summary["primitive_decision_row_count"] == len(
        adapter["primitive_adapter_decision_rows"]
    )

    expected_source_ids = {
        primitive["offline_primitive_id"]
        for output_row in report["paper_offline_changed_decomposition_output_contract"][
            "decomposition_output_rows"
        ]
        for primitive in output_row["primitive_records"]
    }
    adapter_source_ids = {
        row["offline_primitive_id"] for row in adapter["primitive_adapter_decision_rows"]
    }
    assert adapter_source_ids == expected_source_ids

    for row in adapter["primitive_adapter_decision_rows"]:
        assert row["adapter_decision_id"] == (
            f"{row['offline_primitive_id']}:adapter_decision"
        )
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["record_field_status"] == "complete"
        assert row["postprocess_state"] == "not_applied_to_search_output"
        assert row["adapter_decision"] == "later_policy_required"
        assert (
            row["adapter_decision_reason"]
            == "unsupported_paper_primitive_requires_adapter_policy"
        )
        assert (
            row["required_later_gate"]
            == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
        )


def test_cpd_paper_package_adapter_contract_stays_report_only():
    report = build_cpd_paper_offline_report()
    payload = report["paper_package_adapter_contract"]

    assert payload["package_generation_allowed"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
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
    for row in payload["primitive_adapter_decision_rows"]:
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_records_unsupported_primitive_policy_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert (
        EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    payload = report["paper_package_adapter_unsupported_primitive_policy"]
    assert payload["gate_id"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
    assert (
        payload["gate_status"]
        == "implemented_offline_unsupported_primitive_policy_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
    assert payload["input_gate_id"] == EXPECTED_PACKAGE_ADAPTER_CONTRACT
    assert payload["next_required_gate"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "unsupported_primitive_policy_complete_mapped_subset_plan_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_unsupported_primitive_policy_not_collision_package"
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_unsupported_primitive_policy_no_collision_package_no_newton"
    )
    assert payload["remaining_gaps"] == EXPECTED_UNSUPPORTED_POLICY_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False


def test_cpd_paper_unsupported_primitive_policy_classifies_paper_families():
    report = build_cpd_paper_offline_report()
    payload = report["paper_package_adapter_unsupported_primitive_policy"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["paper_primitive_family_policy_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    assert rows["oriented_bounding_box"]["newton_runtime_kind"] == "box"
    assert rows["sphere"]["newton_runtime_kind"] == "sphere"
    assert rows["capsule"]["newton_runtime_kind"] == "capsule"
    for primitive_name in ("oriented_bounding_box", "sphere", "capsule"):
        row = rows[primitive_name]
        assert row["paper_family_status"] == "direct_newton_native_candidate"
        assert row["adapter_policy"] == "candidate_for_mapped_subset_plan"
        assert row["direct_adapter_allowed_after_mapped_subset_plan"] is True
        assert row["package_conversion_enabled_by_this_gate"] is False
        assert row["fallback_generation_allowed"] is False
        assert row["drop_allowed"] is False

    for primitive_name in ("capped_cylinder", "frustum", "trapezoidal_prism"):
        row = rows[primitive_name]
        assert row["paper_family_status"] == "offline_only_unmapped"
        assert row["newton_runtime_kind"] == "offline_only_unmapped"
        assert (
            row["adapter_policy"]
            == "keep_offline_until_explicit_mapping_or_approximation_policy"
        )
        assert row["direct_adapter_allowed_after_mapped_subset_plan"] is False
        assert row["package_conversion_enabled_by_this_gate"] is False
        assert row["requires_explicit_mapping_or_approximation_policy"] is True
        assert row["fallback_generation_allowed"] is False
        assert row["drop_allowed"] is False

    assert rows["trapezoidal_prism"]["current_row_evidence_count"] == 16
    assert rows["capped_cylinder"]["current_row_evidence_count"] == 0
    assert rows["frustum"]["current_row_evidence_count"] == 0


def test_cpd_paper_unsupported_primitive_policy_blocks_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    adapter = report["paper_package_adapter_contract"]
    payload = report["paper_package_adapter_unsupported_primitive_policy"]
    summary = payload["coverage_summary"]
    rows = payload["current_adapter_decision_policy_rows"]

    assert summary["decomposition_output_row_count"] == 9
    assert summary["primitive_decision_row_count"] == 16
    assert summary["paper_primitive_family_policy_row_count"] == 6
    assert summary["current_adapter_decision_policy_row_count"] == 16
    assert summary["direct_policy_eligible_record_count"] == 0
    assert summary["unsupported_policy_blocked_record_count"] == 16
    assert summary["adapter_contract_blocked_record_count"] == 0
    assert summary["dropped_record_count"] == 0
    assert summary["package_candidate_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }
    assert (
        summary["direct_policy_eligible_record_count"]
        + summary["unsupported_policy_blocked_record_count"]
        + summary["adapter_contract_blocked_record_count"]
        + summary["dropped_record_count"]
        == summary["current_adapter_decision_policy_row_count"]
    )

    assert len(rows) == len(adapter["primitive_adapter_decision_rows"]) == 16
    for row, adapter_row in zip(rows, adapter["primitive_adapter_decision_rows"]):
        assert row["policy_decision_id"] == (
            f"{adapter_row['adapter_decision_id']}:unsupported_policy"
        )
        assert row["source_adapter_decision_id"] == adapter_row["adapter_decision_id"]
        assert row["source_output_id"] == adapter_row["source_output_id"]
        assert row["evidence_case_id"] == adapter_row["evidence_case_id"]
        assert row["offline_primitive_id"] == adapter_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_adapter_decision"] == "later_policy_required"
        assert row["unsupported_policy_decision"] == "block_package_conversion"
        assert row["adapter_action"] == "keep_offline"
        assert row["package_candidate_status"] == (
            "not_package_candidate_unsupported_policy_block"
        )
        assert row["required_later_gate"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_unsupported_primitive_policy_stays_report_only():
    report = build_cpd_paper_offline_report()
    payload = report["paper_package_adapter_unsupported_primitive_policy"]

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
    for row in payload["paper_primitive_family_policy_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_adapter_decision_policy_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_records_package_conversion_mapped_subset_plan_gate():
    report = build_cpd_paper_offline_report()

    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert (
        EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    payload = report["paper_package_conversion_mapped_subset_plan"]
    assert payload["gate_id"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
    assert (
        payload["gate_status"]
        == "implemented_offline_mapped_subset_plan_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
    assert payload["input_gate_id"] == EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    )
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "mapped_subset_plan_complete_candidate_matrix_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_mapped_subset_plan_not_collision_package"
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_conversion_plan_no_collision_package_no_primitivespec_no_newton"
    )
    assert payload["remaining_gaps"] == EXPECTED_CONVERSION_MAPPED_SUBSET_REMAINING_GAPS
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False


def test_cpd_paper_mapped_subset_plan_classifies_paper_families():
    report = build_cpd_paper_offline_report()
    payload = report["paper_package_conversion_mapped_subset_plan"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["paper_primitive_family_conversion_plan_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    expected_native = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    for primitive_name, runtime_kind in expected_native.items():
        row = rows[primitive_name]
        assert row["planned_runtime_kind"] == runtime_kind
        assert row["conversion_plan_decision"] == "plan_direct_native_mapping_later"
        assert row["package_candidate_status"] == (
            "future_candidate_family_no_current_rows"
        )
        assert row["current_row_evidence_count"] == 0
        assert row["package_conversion_enabled_by_this_gate"] is False

    for primitive_name in ("capped_cylinder", "frustum", "trapezoidal_prism"):
        row = rows[primitive_name]
        assert row["planned_runtime_kind"] == "offline_only_unmapped"
        assert row["conversion_plan_decision"] == (
            "exclude_requires_explicit_mapping_or_approximation_policy"
        )
        assert row["package_candidate_status"] == (
            "not_package_candidate_unsupported_policy_block"
        )
        assert row["package_conversion_enabled_by_this_gate"] is False
        assert row["requires_explicit_mapping_or_approximation_policy"] is True
    assert rows["trapezoidal_prism"]["current_row_evidence_count"] == 16


def test_cpd_paper_mapped_subset_plan_excludes_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    unsupported = report["paper_package_adapter_unsupported_primitive_policy"]
    payload = report["paper_package_conversion_mapped_subset_plan"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_conversion_plan_rows"]

    assert summary["decomposition_output_row_count"] == 9
    assert summary["primitive_decision_row_count"] == 16
    assert summary["paper_primitive_family_conversion_plan_row_count"] == 6
    assert summary["current_row_conversion_plan_row_count"] == 16
    assert summary["direct_mapped_current_candidate_record_count"] == 0
    assert summary["future_candidate_family_without_current_rows_count"] == 3
    assert summary["excluded_requires_policy_record_count"] == 16
    assert summary["adapter_contract_blocked_record_count"] == 0
    assert summary["package_candidate_record_count"] == 0
    assert summary["dropped_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }
    assert (
        summary["direct_mapped_current_candidate_record_count"]
        + summary["excluded_requires_policy_record_count"]
        + summary["adapter_contract_blocked_record_count"]
        + summary["dropped_record_count"]
        == summary["current_row_conversion_plan_row_count"]
    )

    unsupported_rows = unsupported["current_adapter_decision_policy_rows"]
    assert len(rows) == len(unsupported_rows) == 16
    for row, upstream_row in zip(rows, unsupported_rows):
        assert row["conversion_plan_row_id"] == (
            f"{upstream_row['policy_decision_id']}:mapped_subset_plan"
        )
        assert row["source_policy_decision_id"] == upstream_row["policy_decision_id"]
        assert row["source_adapter_decision_id"] == (
            upstream_row["source_adapter_decision_id"]
        )
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_unsupported_policy_decision"] == "block_package_conversion"
        assert row["conversion_plan_decision"] == (
            "exclude_requires_explicit_mapping_or_approximation_policy"
        )
        assert row["conversion_plan_action"] == "keep_offline"
        assert row["package_conversion_candidate"] is False
        assert row["package_candidate_status"] == (
            "not_package_candidate_unsupported_policy_block"
        )
        assert row["required_later_gate"] == (
            EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
        )
        assert row["package_generation_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_mapped_subset_plan_stays_report_only():
    report = build_cpd_paper_offline_report()
    payload = report["paper_package_conversion_mapped_subset_plan"]

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
    assert payload["mapped_subset_plan_contract"][
        "primitive_spec_generation_allowed"
    ] is False
    assert payload["mapped_subset_plan_contract"][
        "collision_package_generation_allowed"
    ] is False
    assert payload["mapped_subset_plan_contract"]["newton_runtime_allowed"] is False
    assert payload["mapped_subset_plan_contract"][
        "runtime_admissibility_supported"
    ] is False
    for row in payload["paper_primitive_family_conversion_plan_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_conversion_plan_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_records_mapped_subset_conversion_candidate_matrix_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]

    assert report["next_required_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    assert (
        payload["gate_status"]
        == "implemented_offline_candidate_matrix_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    assert payload["input_gate_id"] == EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "candidate_matrix_complete_adapter_preflight_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_mapped_subset_candidate_matrix_not_collision_package"
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_candidate_matrix_no_primitivespec_no_collision_package_no_newton"
    )
    assert payload["remaining_gaps"] == EXPECTED_CANDIDATE_MATRIX_REMAINING_GAPS
    assert payload["primitive_spec_generated"] is False
    assert payload["collision_package_generated"] is False
    assert payload["runtime_admissibility_checked"] is False
    assert payload["newton_support_claimed"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False


def test_cpd_paper_candidate_matrix_records_future_family_review_rows():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["future_family_candidate_matrix_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    expected_native = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    for primitive_name, runtime_kind in expected_native.items():
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == runtime_kind
        assert row["candidate_matrix_decision"] == "native_family_review_only"
        assert row["future_family_review_candidate"] is True
        assert row["current_row_evidence_count"] == 0
        assert row["current_package_conversion_candidate_count"] == 0
        assert row["package_candidate_status"] == (
            "future_family_review_candidate_no_current_rows"
        )
        assert row["package_conversion_enabled_by_this_gate"] is False
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    for primitive_name in ("capped_cylinder", "frustum"):
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == "offline_only_unmapped"
        assert row["candidate_matrix_decision"] == "blocked_approximation_policy_missing"
        assert row["future_family_review_candidate"] is False
        assert row["package_candidate_status"] == (
            "not_current_candidate_mapping_or_approximation_missing"
        )
        assert row["package_conversion_enabled_by_this_gate"] is False

    trapezoid = rows["trapezoidal_prism"]
    assert trapezoid["candidate_runtime_kind"] == "offline_only_unmapped"
    assert trapezoid["candidate_matrix_decision"] == "blocked_unmapped_current_rows"
    assert trapezoid["future_family_review_candidate"] is False
    assert trapezoid["current_row_evidence_count"] == 16
    assert trapezoid["current_package_conversion_candidate_count"] == 0
    assert trapezoid["package_candidate_status"] == (
        "not_current_candidate_unsupported_policy_block"
    )


def test_cpd_paper_candidate_matrix_blocks_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    plan = report["paper_package_conversion_mapped_subset_plan"]
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_candidate_matrix_rows"]

    assert summary["future_family_candidate_matrix_row_count"] == 6
    assert summary["future_family_review_candidate_count"] == 3
    assert summary["excluded_family_review_row_count"] == 3
    assert summary["current_row_candidate_matrix_row_count"] == 16
    assert summary["current_package_conversion_candidate_count"] == 0
    assert summary["current_blocked_requires_policy_count"] == 16
    assert summary["package_candidate_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }
    assert (
        summary["current_package_conversion_candidate_count"]
        + summary["current_blocked_requires_policy_count"]
        == summary["current_row_candidate_matrix_row_count"]
    )

    plan_rows = plan["current_row_conversion_plan_rows"]
    assert len(rows) == len(plan_rows) == 16
    for row, upstream_row in zip(rows, plan_rows):
        assert row["source_conversion_plan_row_id"] == (
            upstream_row["conversion_plan_row_id"]
        )
        assert row["source_policy_decision_id"] == upstream_row[
            "source_policy_decision_id"
        ]
        assert row["source_adapter_decision_id"] == (
            upstream_row["source_adapter_decision_id"]
        )
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_conversion_plan_decision"] == (
            "exclude_requires_explicit_mapping_or_approximation_policy"
        )
        assert row["candidate_matrix_decision"] == "blocked_unmapped_current_rows"
        assert row["candidate_matrix_action"] == "keep_offline"
        assert row["current_package_conversion_candidate"] is False
        assert row["package_candidate_status"] == (
            "not_current_candidate_unsupported_policy_block"
        )
        assert row["required_later_gate"] == (
            EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
        )
        assert row["required_future_policy"] == (
            "explicit_mapping_or_approximation_policy_before_package_generation"
        )
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_candidate_matrix_stays_report_only():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_conversion_candidate_matrix"]

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
    assert payload["candidate_matrix_contract"][
        "primitive_spec_generation_allowed"
    ] is False
    assert payload["candidate_matrix_contract"][
        "collision_package_generation_allowed"
    ] is False
    assert payload["candidate_matrix_contract"]["newton_runtime_allowed"] is False
    assert payload["candidate_matrix_contract"][
        "runtime_admissibility_supported"
    ] is False
    for row in payload["future_family_candidate_matrix_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_candidate_matrix_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_records_mapped_subset_adapter_preflight_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_adapter_preflight_contract"]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert (
        payload["gate_status"]
        == "implemented_offline_adapter_preflight_contract_only_partial"
    )
    assert payload["closed_gate"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert (
        payload["decision_reason"]
        == "adapter_preflight_contract_complete_primitivespec_dry_run_contract_missing"
    )
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_adapter_preflight_contract_not_primitivespec_not_collision_package"
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_adapter_preflight_no_primitivespec_no_collision_package_no_newton"
    )
    assert payload["candidate_count_at_preflight"] == 0
    assert payload["preflight_action"] == "no_op_keep_offline"
    assert payload["remaining_gaps"] == EXPECTED_PREFLIGHT_REMAINING_GAPS


def test_cpd_paper_adapter_preflight_records_family_requirements():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_adapter_preflight_contract"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["adapter_preflight_requirement_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    expected_native = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    for primitive_name, runtime_kind in expected_native.items():
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == runtime_kind
        assert (
            row["adapter_preflight_decision"]
            == "future_native_family_preflight_recorded_only"
        )
        assert row["future_native_family_preflight_recorded"] is True
        assert row["current_row_evidence_count"] == 0
        assert row["current_package_conversion_candidate_count"] == 0
        assert row["package_generation_enabled_by_this_gate"] is False
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    for primitive_name in ("capped_cylinder", "frustum"):
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == "offline_only_unmapped"
        assert (
            row["adapter_preflight_decision"]
            == "blocked_approximation_policy_missing"
        )
        assert row["future_native_family_preflight_recorded"] is False
        assert row["package_generation_enabled_by_this_gate"] is False

    trapezoid = rows["trapezoidal_prism"]
    assert trapezoid["candidate_runtime_kind"] == "offline_only_unmapped"
    assert (
        trapezoid["adapter_preflight_decision"]
        == "noop_current_unmapped_rows_keep_offline"
    )
    assert trapezoid["future_native_family_preflight_recorded"] is False
    assert trapezoid["current_row_evidence_count"] == 16
    assert trapezoid["current_package_conversion_candidate_count"] == 0


def test_cpd_paper_adapter_preflight_noops_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    matrix = report["paper_mapped_subset_conversion_candidate_matrix"]
    payload = report["paper_mapped_subset_adapter_preflight_contract"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_adapter_preflight_rows"]

    assert summary["family_preflight_requirement_row_count"] == 6
    assert summary["future_native_family_preflight_record_count"] == 3
    assert summary["blocked_family_preflight_record_count"] == 3
    assert summary["current_row_adapter_preflight_row_count"] == 16
    assert summary["current_preflight_pass_record_count"] == 0
    assert summary["current_preflight_noop_record_count"] == 16
    assert summary["current_package_conversion_candidate_count"] == 0
    assert summary["package_candidate_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }

    matrix_rows = matrix["current_row_candidate_matrix_rows"]
    assert len(rows) == len(matrix_rows) == 16
    for row, upstream_row in zip(rows, matrix_rows):
        assert row["source_candidate_matrix_row_id"] == (
            upstream_row["candidate_matrix_row_id"]
        )
        assert row["source_conversion_plan_row_id"] == (
            upstream_row["source_conversion_plan_row_id"]
        )
        assert row["source_policy_decision_id"] == upstream_row[
            "source_policy_decision_id"
        ]
        assert row["source_adapter_decision_id"] == (
            upstream_row["source_adapter_decision_id"]
        )
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["evidence_case_id"] == upstream_row["evidence_case_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_candidate_matrix_decision"] == "blocked_unmapped_current_rows"
        assert (
            row["adapter_preflight_decision"]
            == "noop_keep_offline_unmapped_current_row"
        )
        assert row["adapter_preflight_action"] == "keep_offline"
        assert row["current_package_conversion_candidate"] is False
        assert row["adapter_preflight_passed"] is False
        assert row["package_generation_enabled_by_this_gate"] is False
        assert (
            row["required_later_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
        )
        assert row["required_future_policy"] == upstream_row["required_future_policy"]
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_adapter_preflight_stays_report_only():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_adapter_preflight_contract"]

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
    assert payload["primitive_spec_generation_allowed"] is False
    assert payload["collision_package_generation_allowed"] is False
    assert payload["newton_runtime_allowed"] is False
    assert payload["runtime_admissibility_supported"] is False
    assert payload["approximation_policy_enabled"] is False
    assert payload["silent_drop_allowed"] is False
    assert payload["adapter_preflight_contract"][
        "primitive_spec_generation_allowed"
    ] is False
    assert payload["adapter_preflight_contract"][
        "collision_package_generation_allowed"
    ] is False
    assert payload["adapter_preflight_contract"]["newton_runtime_allowed"] is False
    assert payload["adapter_preflight_contract"][
        "runtime_admissibility_supported"
    ] is False
    assert payload["adapter_preflight_contract"]["silent_drop_allowed"] is False
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["primitive_spec_generated"] is False
    assert payload["collision_package_generated"] is False
    assert payload["runtime_admissibility_checked"] is False
    assert payload["newton_support_claimed"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    for row in payload["adapter_preflight_requirement_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_adapter_preflight_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_adapter_preflight_rejects_wrong_candidate_matrix_gate():
    report = build_cpd_paper_offline_report()
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    candidate_matrix["gate_id"] = "stale_gate"

    with pytest.raises(ValueError, match="candidate_matrix_gate_id_mismatch"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_true_input_trigger_flags():
    report = build_cpd_paper_offline_report()
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    candidate_matrix["package_generation_triggered"] = True

    with pytest.raises(ValueError, match="input_trigger_flag_true"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_nonzero_input_candidates():
    report = build_cpd_paper_offline_report()
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    candidate_matrix["coverage_summary"] = {
        **candidate_matrix["coverage_summary"],
        "current_package_conversion_candidate_count": 1,
    }

    with pytest.raises(ValueError, match="input_package_candidate_count_nonzero"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_row_level_current_candidate():
    report = build_cpd_paper_offline_report()
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    current_rows = [
        dict(row) for row in candidate_matrix["current_row_candidate_matrix_rows"]
    ]
    current_rows[0]["current_package_conversion_candidate"] = True
    candidate_matrix["current_row_candidate_matrix_rows"] = current_rows

    with pytest.raises(ValueError, match="input_package_candidate_count_nonzero"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_family_level_candidate_count():
    report = build_cpd_paper_offline_report()
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    family_rows = [
        dict(row) for row in candidate_matrix["future_family_candidate_matrix_rows"]
    ]
    family_rows[0]["current_package_conversion_candidate_count"] = 1
    candidate_matrix["future_family_candidate_matrix_rows"] = family_rows

    with pytest.raises(ValueError, match="input_package_candidate_count_nonzero"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_unknown_family_decision():
    report = build_cpd_paper_offline_report()
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    family_rows = [
        dict(row) for row in candidate_matrix["future_family_candidate_matrix_rows"]
    ]
    family_rows[0]["candidate_matrix_decision"] = "misspelled_decision"
    candidate_matrix["future_family_candidate_matrix_rows"] = family_rows

    with pytest.raises(ValueError, match="unknown_family_candidate_matrix_decision"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_adapter_preflight_rejects_duplicate_input_row_ids():
    report = build_cpd_paper_offline_report()
    candidate_matrix = dict(report["paper_mapped_subset_conversion_candidate_matrix"])
    current_rows = [
        dict(row) for row in candidate_matrix["current_row_candidate_matrix_rows"]
    ]
    current_rows[1]["candidate_matrix_row_id"] = current_rows[0][
        "candidate_matrix_row_id"
    ]
    candidate_matrix["current_row_candidate_matrix_rows"] = current_rows

    with pytest.raises(ValueError, match="duplicate_candidate_matrix_row_id"):
        _paper_mapped_subset_adapter_preflight_contract_payload(candidate_matrix)


def test_cpd_paper_records_mapped_subset_primitivespec_dry_run_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_dry_run_contract"]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert report["failure_labels"] == EXPECTED_GENERALIZATION_FAILURE_LABELS
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )

    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    assert (
        payload["gate_status"]
        == "implemented_offline_primitivespec_dry_run_contract_only_partial"
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    )
    assert payload["input_gate_id"] == EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_dry_run_contract_complete_"
        "primitivespec_validation_contract_missing"
    )
    assert payload["remaining_gaps"] == EXPECTED_PRIMITIVESPEC_REMAINING_GAPS
    assert payload["paper_faithful_offline_allowed"] is False
    assert payload["package_generation_allowed"] is False
    assert payload["artifact_kind"] == (
        "offline_primitivespec_dry_run_contract_not_primitivespec_"
        "not_collision_package"
    )
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_primitivespec_dry_run_no_primitivespec_no_collision_package_no_newton"
    )
    assert payload["candidate_count_at_dry_run"] == 0
    assert payload["dry_run_action"] == "no_op_keep_offline"
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["generated_collision_package_count"] == 0
    assert payload["runtime_admissibility_check_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_PRIMITIVESPEC_REMAINING_GAPS


def test_cpd_paper_primitivespec_dry_run_records_family_requirements():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_dry_run_contract"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["primitive_spec_dry_run_requirement_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    expected_native = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    expected_fields = [
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
    for primitive_name, primitive_kind in expected_native.items():
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == primitive_kind
        assert row["future_primitive_spec_kind"] == primitive_kind
        assert row["primitive_spec_dry_run_decision"] == (
            "future_native_family_primitivespec_shape_recorded_only"
        )
        assert row["future_primitive_spec_shape_recorded"] is True
        assert row["required_primitive_spec_fields"] == expected_fields
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False

    for primitive_name in ("capped_cylinder", "frustum"):
        row = rows[primitive_name]
        assert row["candidate_runtime_kind"] == "offline_only_unmapped"
        assert row["future_primitive_spec_kind"] is None
        assert (
            row["primitive_spec_dry_run_decision"]
            == "blocked_approximation_policy_missing"
        )
        assert row["future_primitive_spec_shape_recorded"] is False

    trapezoid = rows["trapezoidal_prism"]
    assert trapezoid["candidate_runtime_kind"] == "offline_only_unmapped"
    assert trapezoid["future_primitive_spec_kind"] is None
    assert (
        trapezoid["primitive_spec_dry_run_decision"]
        == "noop_current_unmapped_rows_keep_offline"
    )
    assert trapezoid["future_primitive_spec_shape_recorded"] is False
    assert trapezoid["current_row_evidence_count"] == 16


def test_cpd_paper_primitivespec_dry_run_noops_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    preflight = report["paper_mapped_subset_adapter_preflight_contract"]
    payload = report["paper_mapped_subset_primitivespec_dry_run_contract"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_primitivespec_dry_run_rows"]

    assert summary["primitive_spec_requirement_row_count"] == 6
    assert summary["future_native_primitivespec_shape_record_count"] == 3
    assert summary["blocked_primitivespec_requirement_row_count"] == 2
    assert summary["noop_primitivespec_requirement_row_count"] == 1
    assert summary["current_row_primitivespec_dry_run_row_count"] == 16
    assert summary["current_primitivespec_dry_run_pass_record_count"] == 0
    assert summary["current_primitivespec_noop_record_count"] == 16
    assert summary["primitive_spec_candidate_record_count"] == 0
    assert summary["generated_primitive_spec_record_count"] == 0
    assert summary["current_paper_primitive_distribution"] == {
        "trapezoidal_prism": 16,
    }
    assert summary["current_runtime_kind_distribution"] == {
        "offline_only_unmapped": 16,
    }

    preflight_rows = preflight["current_row_adapter_preflight_rows"]
    assert len(rows) == len(preflight_rows) == 16
    for row, upstream_row in zip(rows, preflight_rows):
        assert row["source_adapter_preflight_row_id"] == (
            upstream_row["adapter_preflight_row_id"]
        )
        assert row["source_candidate_matrix_row_id"] == (
            upstream_row["source_candidate_matrix_row_id"]
        )
        assert row["source_conversion_plan_row_id"] == (
            upstream_row["source_conversion_plan_row_id"]
        )
        assert row["source_policy_decision_id"] == upstream_row[
            "source_policy_decision_id"
        ]
        assert row["source_adapter_decision_id"] == (
            upstream_row["source_adapter_decision_id"]
        )
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["evidence_case_id"] == upstream_row["evidence_case_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["paper_primitive"] == "trapezoidal_prism"
        assert row["offline_runtime_kind_label"] == "offline_only_unmapped"
        assert row["input_adapter_preflight_decision"] == (
            "noop_keep_offline_unmapped_current_row"
        )
        assert row["primitive_spec_dry_run_decision"] == "skip_unmapped_current_row"
        assert row["primitive_spec_dry_run_action"] == "keep_offline"
        assert row["primitive_spec_dry_run_passed"] is False
        assert row["primitive_spec_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_primitivespec_dry_run_stays_report_only():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_dry_run_contract"]

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
    assert payload["primitive_spec_generation_allowed"] is False
    assert payload["collision_package_generation_allowed"] is False
    assert payload["newton_runtime_allowed"] is False
    assert payload["runtime_admissibility_supported"] is False
    assert payload["approximation_policy_enabled"] is False
    assert payload["silent_drop_allowed"] is False
    assert payload["primitive_spec_dry_run_contract"][
        "primitive_spec_generation_allowed"
    ] is False
    assert payload["primitive_spec_dry_run_contract"][
        "collision_package_generation_allowed"
    ] is False
    assert payload["primitive_spec_generated"] is False
    assert payload["collision_package_generated"] is False
    assert payload["runtime_admissibility_checked"] is False
    assert payload["newton_support_claimed"] is False
    assert payload["approximation_policy_applied"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert payload["collision_quality_measured"] is False
    assert payload["deployment_or_certification_claimed"] is False
    for row in payload["primitive_spec_dry_run_requirement_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_primitivespec_dry_run_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_primitivespec_dry_run_rejects_wrong_input_gate():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    preflight["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_dry_run_input_gate_id_mismatch",
    ):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_true_input_trigger_flags():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    preflight["package_generation_triggered"] = True

    with pytest.raises(ValueError, match="input_trigger_flag_true"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_nonzero_input_candidates():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    preflight["candidate_count_at_preflight"] = 1

    with pytest.raises(
        ValueError,
        match="input_primitivespec_candidate_count_nonzero",
    ):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_preflight_pass_count():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    preflight["coverage_summary"] = {
        **preflight["coverage_summary"],
        "current_preflight_pass_record_count": 1,
    }

    with pytest.raises(ValueError, match="input_preflight_pass_count_nonzero"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_row_level_preflight_pass():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [
        dict(row) for row in preflight["current_row_adapter_preflight_rows"]
    ]
    current_rows[0]["adapter_preflight_passed"] = True
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="input_preflight_pass_count_nonzero"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_row_level_candidate():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [
        dict(row) for row in preflight["current_row_adapter_preflight_rows"]
    ]
    current_rows[0]["current_package_conversion_candidate"] = True
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="input_primitivespec_candidate_count_nonzero",
    ):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_family_real_usd_flag():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    family_rows = [
        dict(row) for row in preflight["adapter_preflight_requirement_rows"]
    ]
    family_rows[0]["real_usd_loaded"] = True
    preflight["adapter_preflight_requirement_rows"] = family_rows

    with pytest.raises(ValueError, match="input_trigger_flag_true:real_usd_loaded"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_current_benchmark_flag():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [
        dict(row) for row in preflight["current_row_adapter_preflight_rows"]
    ]
    current_rows[0]["benchmark_run"] = True
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="input_trigger_flag_true:benchmark_run"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_duplicate_preflight_row_ids():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [
        dict(row) for row in preflight["current_row_adapter_preflight_rows"]
    ]
    current_rows[1]["adapter_preflight_row_id"] = current_rows[0][
        "adapter_preflight_row_id"
    ]
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="duplicate_adapter_preflight_row_id"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_unknown_family_decision():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    family_rows = [
        dict(row) for row in preflight["adapter_preflight_requirement_rows"]
    ]
    family_rows[0]["adapter_preflight_decision"] = "misspelled_decision"
    preflight["adapter_preflight_requirement_rows"] = family_rows

    with pytest.raises(ValueError, match="unknown_adapter_preflight_family_decision"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_missing_current_source_id():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [
        dict(row) for row in preflight["current_row_adapter_preflight_rows"]
    ]
    current_rows[0].pop("source_output_id")
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="missing_current_row_source_id"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_blank_current_source_id():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [
        dict(row) for row in preflight["current_row_adapter_preflight_rows"]
    ]
    current_rows[0]["source_output_id"] = " "
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="missing_current_row_source_id"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_primitivespec_dry_run_rejects_wrong_required_later_gate():
    report = build_cpd_paper_offline_report()
    preflight = dict(report["paper_mapped_subset_adapter_preflight_contract"])
    current_rows = [
        dict(row) for row in preflight["current_row_adapter_preflight_rows"]
    ]
    current_rows[0]["required_later_gate"] = "stale_gate"
    preflight["current_row_adapter_preflight_rows"] = current_rows

    with pytest.raises(ValueError, match="current_row_required_later_gate_mismatch"):
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(preflight)


def test_cpd_paper_records_mapped_subset_primitivespec_validation_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_validation_contract"]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_candidate_source_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert payload["gate_id"] == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_validation_contract_only_partial"
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    )
    assert (
        payload["input_gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["decision"] == "remain_partial"
    assert payload["decision_reason"] == (
        "primitivespec_validation_contract_complete_"
        "primitivespec_generation_preflight_contract_missing"
    )
    assert payload["artifact_kind"] == (
        "offline_primitivespec_validation_contract_not_primitivespec_"
        "not_collision_package"
    )
    assert payload["validated_primitive_spec_candidate_count"] == 0
    assert payload["generated_primitive_spec_count"] == 0
    assert payload["remaining_gaps"] == EXPECTED_VALIDATION_REMAINING_GAPS


def test_cpd_paper_primitivespec_validation_records_family_requirements():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_validation_contract"]
    rows = {
        row["paper_primitive"]: row
        for row in payload["primitive_spec_validation_requirement_rows"]
    }

    assert list(rows) == [
        "oriented_bounding_box",
        "sphere",
        "capsule",
        "capped_cylinder",
        "frustum",
        "trapezoidal_prism",
    ]
    assert rows["oriented_bounding_box"][
        "primitive_spec_validation_decision"
    ] == "future_native_family_primitivespec_shape_requirement_validated"
    assert rows["oriented_bounding_box"][
        "validated_future_primitive_spec_kind"
    ] == "box"
    assert rows["sphere"]["validated_future_primitive_spec_kind"] == "sphere"
    assert rows["capsule"]["validated_future_primitive_spec_kind"] == "capsule"
    assert rows["capped_cylinder"]["primitive_spec_validation_decision"] == (
        "blocked_approximation_policy_validation_recorded"
    )
    assert rows["frustum"]["primitive_spec_validation_decision"] == (
        "blocked_approximation_policy_validation_recorded"
    )
    assert rows["trapezoidal_prism"]["primitive_spec_validation_decision"] == (
        "noop_unmapped_family_validation_recorded"
    )
    for primitive_name in ("capped_cylinder", "frustum", "trapezoidal_prism"):
        assert rows[primitive_name]["validated_future_primitive_spec_kind"] is None
        assert rows[primitive_name]["primitive_spec_generation_triggered"] is False
        assert rows[primitive_name]["collision_package_generation_triggered"] is False
        assert rows[primitive_name]["runtime_admissibility_triggered"] is False
        assert rows[primitive_name]["newton_runtime_triggered"] is False
        assert rows[primitive_name]["real_usd_triggered"] is False
        assert rows[primitive_name]["benchmark_triggered"] is False


def test_cpd_paper_primitivespec_validation_noops_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    dry_run = report["paper_mapped_subset_primitivespec_dry_run_contract"]
    payload = report["paper_mapped_subset_primitivespec_validation_contract"]
    summary = payload["coverage_summary"]
    rows = payload["current_row_primitivespec_validation_rows"]

    assert summary["primitive_spec_validation_requirement_row_count"] == 6
    assert summary["future_native_primitivespec_shape_validation_count"] == 3
    assert summary["blocked_primitivespec_validation_requirement_count"] == 2
    assert summary["noop_primitivespec_validation_requirement_count"] == 1
    assert summary["current_row_primitivespec_validation_row_count"] == 16
    assert summary["current_primitivespec_validation_pass_record_count"] == 0
    assert summary["current_primitivespec_validation_noop_record_count"] == 16
    assert summary["validated_primitive_spec_candidate_record_count"] == 0
    assert summary["generated_primitive_spec_record_count"] == 0

    dry_run_rows = dry_run["current_row_primitivespec_dry_run_rows"]
    assert len(rows) == len(dry_run_rows) == 16
    for row, upstream_row in zip(rows, dry_run_rows):
        assert row["source_primitivespec_dry_run_row_id"] == (
            upstream_row["primitive_spec_dry_run_row_id"]
        )
        assert row["source_adapter_preflight_row_id"] == (
            upstream_row["source_adapter_preflight_row_id"]
        )
        assert row["source_candidate_matrix_row_id"] == (
            upstream_row["source_candidate_matrix_row_id"]
        )
        assert row["source_conversion_plan_row_id"] == (
            upstream_row["source_conversion_plan_row_id"]
        )
        assert row["source_policy_decision_id"] == upstream_row[
            "source_policy_decision_id"
        ]
        assert row["source_adapter_decision_id"] == (
            upstream_row["source_adapter_decision_id"]
        )
        assert row["source_output_id"] == upstream_row["source_output_id"]
        assert row["evidence_case_id"] == upstream_row["evidence_case_id"]
        assert row["offline_primitive_id"] == upstream_row["offline_primitive_id"]
        assert row["primitive_spec_validation_decision"] == (
            "skip_unmapped_current_row_validated"
        )
        assert row["primitive_spec_validation_action"] == "keep_offline"
        assert row["primitive_spec_validation_passed"] is False
        assert row["primitive_spec_candidate"] is False
        assert row["generated_primitive_spec"] is None
        assert row["silent_drop_detected"] is False
        assert row["primitive_spec_generation_triggered"] is False
        assert row["collision_package_generation_triggered"] is False
        assert row["runtime_admissibility_triggered"] is False
        assert row["newton_runtime_triggered"] is False
        assert row["real_usd_triggered"] is False
        assert row["benchmark_triggered"] is False


def test_cpd_paper_primitivespec_validation_stays_report_only():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_validation_contract"]

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
    assert payload["primitive_spec_generation_allowed"] is False
    assert payload["collision_package_generation_allowed"] is False
    assert payload["newton_runtime_allowed"] is False
    assert payload["runtime_admissibility_supported"] is False
    assert payload["approximation_policy_enabled"] is False
    assert payload["silent_drop_allowed"] is False
    assert payload["primitive_spec_validation_contract"][
        "primitive_spec_generation_allowed"
    ] is False
    assert payload["primitive_spec_validation_contract"][
        "collision_package_generation_allowed"
    ] is False
    assert payload["primitive_spec_generated"] is False
    assert payload["collision_package_generated"] is False
    assert payload["runtime_admissibility_checked"] is False
    assert payload["newton_support_claimed"] is False
    assert payload["approximation_policy_applied"] is False
    assert payload["package_generation_triggered"] is False
    assert payload["newton_runtime_triggered"] is False
    assert payload["real_usd_triggered"] is False
    assert payload["benchmark_triggered"] is False
    assert payload["collision_quality_measured"] is False
    assert payload["deployment_or_certification_claimed"] is False
    for row in payload["primitive_spec_validation_requirement_rows"]:
        assert forbidden_keys.isdisjoint(row)
    for row in payload["current_row_primitivespec_validation_rows"]:
        assert forbidden_keys.isdisjoint(row)


def test_cpd_paper_primitivespec_validation_rejects_wrong_input_gate():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    dry_run["gate_id"] = "stale_gate"

    with pytest.raises(
        ValueError,
        match="primitivespec_validation_input_gate_id_mismatch",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_true_input_trigger_flags():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    dry_run["newton_runtime_triggered"] = True

    with pytest.raises(ValueError, match="validation_input_trigger_flag_true"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_nonzero_input_candidates():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    dry_run["candidate_count_at_dry_run"] = 1

    with pytest.raises(
        ValueError,
        match="validation_input_candidate_count_nonzero",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_required_field_mismatch():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    contract = dict(dry_run["primitive_spec_dry_run_contract"])
    contract["required_primitive_spec_fields"] = contract[
        "required_primitive_spec_fields"
    ][:-1]
    dry_run["primitive_spec_dry_run_contract"] = contract

    with pytest.raises(ValueError, match="validation_required_fields_mismatch"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_allowed_kind_mismatch():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    contract = dict(dry_run["primitive_spec_dry_run_contract"])
    contract["allowed_future_runtime_kinds"] = [
        *contract["allowed_future_runtime_kinds"],
        "cylinder",
    ]
    dry_run["primitive_spec_dry_run_contract"] = contract

    with pytest.raises(ValueError, match="validation_allowed_runtime_kinds_mismatch"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_coverage_count_mismatch():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    coverage = dict(dry_run["coverage_summary"])
    coverage["current_row_primitivespec_dry_run_row_count"] = 15
    dry_run["coverage_summary"] = coverage

    with pytest.raises(ValueError, match="validation_coverage_count_mismatch"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_duplicate_dry_run_row_ids():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[1]["primitive_spec_dry_run_row_id"] = current_rows[0][
        "primitive_spec_dry_run_row_id"
    ]
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(ValueError, match="duplicate_primitivespec_dry_run_row_id"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_unknown_family_decision():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [
        dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    requirement_rows[0]["primitive_spec_dry_run_decision"] = "misspelled_decision"
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="unknown_primitivespec_dry_run_family_decision",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_missing_future_native_kind():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [
        dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    requirement_rows[0]["future_primitive_spec_kind"] = None
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(ValueError, match="future_native_primitivespec_kind_missing"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_mutated_family_semantics():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [
        dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    capped_cylinder = next(
        row for row in requirement_rows if row["paper_primitive"] == "capped_cylinder"
    )
    capped_cylinder["primitive_spec_dry_run_decision"] = (
        "future_native_family_primitivespec_shape_recorded_only"
    )
    capped_cylinder["candidate_runtime_kind"] = "box"
    capped_cylinder["future_primitive_spec_kind"] = "box"
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_family_contract_mismatch:capped_cylinder",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_duplicate_family_identity():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [
        dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    requirement_rows[1]["paper_primitive"] = "oriented_bounding_box"
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_family_primitive_sequence_mismatch",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_future_mapping_label_mismatch():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [
        dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    requirement_rows[0]["candidate_runtime_kind"] = "offline_only_unmapped"
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_future_mapping_label_mismatch:oriented_bounding_box",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_blank_requirement_source_id():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [
        dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    requirement_rows[0]["source_adapter_preflight_row_id"] = ""
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_requirement_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_whitespace_requirement_source_id():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [
        dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    requirement_rows[0]["source_adapter_preflight_row_id"] = "   "
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_requirement_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_blank_requirement_row_id():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [
        dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    requirement_rows[0]["primitive_spec_dry_run_row_id"] = " "
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_primitivespec_dry_run_row_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_requirement_real_usd_flag():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    requirement_rows = [
        dict(row) for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    requirement_rows[0]["real_usd_loaded"] = True
    dry_run["primitive_spec_dry_run_requirement_rows"] = requirement_rows

    with pytest.raises(
        ValueError,
        match="validation_input_trigger_flag_true:real_usd_loaded",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_blank_current_source_id():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[0]["source_output_id"] = ""
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_current_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_whitespace_current_source_id():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[0]["source_output_id"] = " "
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_current_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_blank_current_row_id():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[0]["primitive_spec_dry_run_row_id"] = ""
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_primitivespec_dry_run_row_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_current_benchmark_flag():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[0]["benchmark_run"] = True
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_input_trigger_flag_true:benchmark_run",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_generated_collision_package_count():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    dry_run["generated_collision_package_count"] = 1

    with pytest.raises(
        ValueError,
        match="validation_input_generated_collision_package_nonzero",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_row_level_pass():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[0]["primitive_spec_dry_run_passed"] = True
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(ValueError, match="validation_input_pass_count_nonzero"):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_row_level_candidate():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[0]["primitive_spec_candidate"] = True
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_input_candidate_count_nonzero",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_generated_spec():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[0]["generated_primitive_spec"] = {"kind": "box"}
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_input_generated_spec_nonzero",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_missing_current_source_id():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[0].pop("source_output_id")
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_missing_current_row_source_id",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def test_cpd_paper_primitivespec_validation_rejects_wrong_required_later_gate():
    report = build_cpd_paper_offline_report()
    dry_run = dict(report["paper_mapped_subset_primitivespec_dry_run_contract"])
    current_rows = [
        dict(row) for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    current_rows[0]["required_later_gate"] = "stale_gate"
    dry_run["current_row_primitivespec_dry_run_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="validation_current_row_required_later_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_validation_contract_payload(dry_run)


def _generation_preflight_validation_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_primitivespec_validation_contract"])
    )


def _generation_contract_preflight_input() -> dict[str, object]:
    report = build_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_primitivespec_generation_preflight_contract"
            ]
        )
    )


GENERATION_PREFLIGHT_ROW_FALSE_FLAGS = (
    "primitive_spec_generated",
    "collision_package_generated",
    "runtime_admissibility_checked",
    "newton_support_claimed",
    "approximation_policy_applied",
    "primitive_spec_generation_triggered",
    "collision_package_generation_triggered",
    "runtime_admissibility_triggered",
    "real_usd_loaded",
    "benchmark_run",
    "collision_quality_measured",
    "deployment_or_certification_claimed",
    "package_generation_triggered",
    "newton_runtime_triggered",
    "real_usd_triggered",
    "benchmark_triggered",
    "primitive_spec_generation_allowed",
    "collision_package_generation_allowed",
    "runtime_admissibility_supported",
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
)


PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS = (
    "primitive_spec_generated",
    "collision_package_generated",
    "runtime_admissibility_checked",
    "newton_support_claimed",
    "approximation_policy_applied",
    "real_usd_loaded",
    "benchmark_run",
    "collision_quality_measured",
    "deployment_or_certification_claimed",
    "package_generation_triggered",
    "newton_runtime_triggered",
    "real_usd_triggered",
    "benchmark_triggered",
    "primitive_spec_generation_allowed",
    "collision_package_generation_allowed",
    "runtime_admissibility_supported",
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "primitive_spec_generation_triggered",
    "collision_package_generation_triggered",
    "runtime_admissibility_triggered",
)


PRIMITIVESPEC_GENERATION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "package_generation_allowed",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "primitive_spec_generation_action",
    "primitive_spec_generation_candidate_count",
    "offline_primitivespec_template_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "input_contract_summary",
    "primitive_spec_generation_contract",
    "native_family_primitivespec_template_rows",
    "blocked_primitivespec_generation_requirement_rows",
    "noop_primitivespec_generation_requirement_rows",
    "current_row_primitivespec_generation_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}


PRIMITIVESPEC_GENERATION_NATIVE_TEMPLATE_ROW_REQUIRED_KEYS = {
    "primitive_spec_generation_template_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "input_primitivespec_generation_preflight_decision",
    "required_primitive_spec_fields",
    "template_only",
    "runtime_instance_generated",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "silent_drop_detected",
    "primitive_spec_generation_decision",
    "required_current_candidate_source_gate",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}


PRIMITIVESPEC_GENERATION_REQUIREMENT_ROW_REQUIRED_KEYS = {
    "primitive_spec_generation_requirement_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "paper_primitive",
    "candidate_mapping_label",
    "input_primitivespec_generation_preflight_decision",
    "primitive_spec_generation_decision",
    "primitive_spec_generation_action",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "required_later_gate",
    "required_future_policy",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}


PRIMITIVESPEC_GENERATION_CURRENT_ROW_REQUIRED_KEYS = {
    "primitive_spec_generation_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "source_policy_decision_id",
    "source_adapter_decision_id",
    "source_output_id",
    "evidence_case_id",
    "offline_primitive_id",
    "paper_primitive",
    "offline_mapping_label",
    "primitive_spec_generation_decision",
    "primitive_spec_generation_action",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "silent_drop_detected",
    "required_later_gate",
    "required_future_policy",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}


def test_cpd_paper_records_mapped_subset_primitivespec_generation_preflight_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_candidate_source_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS
    )
    assert (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        in report["paper_faithfulness"]["implemented_output_contract_scope"]
    )
    assert (
        report["paper_mapped_subset_primitivespec_validation_contract"][
            "next_required_gate"
        ]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert (
        payload["gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_generation_preflight_contract_only_partial"
    )
    assert payload["closed_gate"] == (
        EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
    )
    assert (
        payload["input_gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    )
    assert (
        payload["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )
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


def test_cpd_paper_primitivespec_generation_preflight_records_family_requirements():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]
    rows = {
        row["paper_primitive"]: row
        for row in payload[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
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
            row["required_later_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        )
    assert rows["capped_cylinder"][
        "primitive_spec_generation_preflight_decision"
    ] == "blocked_approximation_policy_generation_preflight_recorded"
    assert rows["frustum"][
        "primitive_spec_generation_preflight_decision"
    ] == "blocked_approximation_policy_generation_preflight_recorded"
    assert rows["trapezoidal_prism"][
        "primitive_spec_generation_preflight_decision"
    ] == "noop_unmapped_family_generation_preflight_recorded"


def test_cpd_paper_primitivespec_generation_preflight_noops_current_unmapped_rows():
    report = build_cpd_paper_offline_report()
    validation = report["paper_mapped_subset_primitivespec_validation_contract"]
    payload = report[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]
    summary = payload["coverage_summary"]
    rows = payload["current_row_primitivespec_generation_preflight_rows"]

    assert summary["primitive_spec_generation_preflight_requirement_row_count"] == 6
    assert summary["future_native_primitivespec_generation_preflight_count"] == 3
    assert summary["blocked_primitivespec_generation_preflight_requirement_count"] == 2
    assert summary["noop_primitivespec_generation_preflight_requirement_count"] == 1
    assert summary["current_row_primitivespec_generation_preflight_row_count"] == 16
    assert (
        summary["current_primitivespec_generation_preflight_pass_record_count"]
        == 0
    )
    assert (
        summary["current_primitivespec_generation_preflight_noop_record_count"]
        == 16
    )
    assert summary["generation_preflight_candidate_record_count"] == 0
    assert summary["generated_primitive_spec_record_count"] == 0

    validation_rows = validation["current_row_primitivespec_validation_rows"]
    assert len(rows) == len(validation_rows) == 16
    for row, upstream_row in zip(rows, validation_rows):
        assert row["source_primitivespec_validation_row_id"] == (
            upstream_row["primitive_spec_validation_row_id"]
        )
        assert row["source_primitivespec_dry_run_row_id"] == (
            upstream_row["source_primitivespec_dry_run_row_id"]
        )
        assert row["source_adapter_preflight_row_id"] == (
            upstream_row["source_adapter_preflight_row_id"]
        )
        assert row["source_candidate_matrix_row_id"] == (
            upstream_row["source_candidate_matrix_row_id"]
        )
        assert row["source_conversion_plan_row_id"] == (
            upstream_row["source_conversion_plan_row_id"]
        )
        assert row["source_policy_decision_id"] == (
            upstream_row["source_policy_decision_id"]
        )
        assert row["source_adapter_decision_id"] == (
            upstream_row["source_adapter_decision_id"]
        )
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
            row["required_later_gate"]
            == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        )


def test_cpd_paper_primitivespec_generation_preflight_stays_report_only():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
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
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_true_input_trigger_flags():
    validation = _generation_preflight_validation_input()
    validation["real_usd_loaded"] = True

    with pytest.raises(
        ValueError,
        match="generation_preflight_input_trigger_flag_true:real_usd_loaded",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


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
            "generation_preflight_input_trigger_flag_true:"
            "runtime_admissibility_check_count",
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
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


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
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_family_order_mismatch():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["primitive_spec_validation_requirement_rows"]
    ]
    rows[1]["paper_primitive"] = "oriented_bounding_box"
    validation["primitive_spec_validation_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="generation_preflight_family_primitive_sequence_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_future_label_mismatch():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["primitive_spec_validation_requirement_rows"]
    ]
    rows[0]["candidate_mapping_label"] = "offline_only_unmapped"
    validation["primitive_spec_validation_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "generation_preflight_future_mapping_label_mismatch:"
            "oriented_bounding_box"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_mutated_family_semantics():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["primitive_spec_validation_requirement_rows"]
    ]
    capped_cylinder = next(
        row for row in rows if row["paper_primitive"] == "capped_cylinder"
    )
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
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_unknown_family_decision():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["primitive_spec_validation_requirement_rows"]
    ]
    rows[0]["primitive_spec_validation_decision"] = "misspelled_decision"
    validation["primitive_spec_validation_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="unknown_primitivespec_validation_family_decision:misspelled_decision",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_blank_validation_row_id():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["primitive_spec_validation_requirement_rows"]
    ]
    rows[0]["primitive_spec_validation_row_id"] = " "
    validation["primitive_spec_validation_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "generation_preflight_missing_validation_row_id:"
            "primitive_spec_validation_row_id"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_duplicate_validation_row_id():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["current_row_primitivespec_validation_rows"]
    ]
    rows[1]["primitive_spec_validation_row_id"] = rows[0][
        "primitive_spec_validation_row_id"
    ]
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_validation_row_id",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_current_source_id_gap():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["current_row_primitivespec_validation_rows"]
    ]
    rows[0]["source_output_id"] = ""
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="generation_preflight_missing_current_row_source_id:source_output_id",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_unknown_current_decision():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["current_row_primitivespec_validation_rows"]
    ]
    rows[0]["primitive_spec_validation_decision"] = "misspelled_current_decision"
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "unknown_primitivespec_validation_current_decision:"
            "misspelled_current_decision"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_row_level_flag():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["current_row_primitivespec_validation_rows"]
    ]
    rows[0]["benchmark_run"] = True
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="generation_preflight_input_trigger_flag_true:benchmark_run",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


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
    rows = [
        dict(row)
        for row in validation["current_row_primitivespec_validation_rows"]
    ]
    rows[0][field_name] = field_value
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


def test_cpd_paper_primitivespec_generation_preflight_rejects_current_row_gate_mismatch():
    validation = _generation_preflight_validation_input()
    rows = [
        dict(row)
        for row in validation["current_row_primitivespec_validation_rows"]
    ]
    rows[0]["required_later_gate"] = "stale_gate"
    validation["current_row_primitivespec_validation_rows"] = rows

    with pytest.raises(
        ValueError,
        match="generation_preflight_current_row_required_later_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            validation
        )


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


def test_cpd_paper_records_mapped_subset_primitivespec_generation_contract_gate():
    report = build_cpd_paper_offline_report()
    payload = report["paper_mapped_subset_primitivespec_generation_contract"]

    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert report["failure_labels"] == [
        "paper_mapped_subset_primitivespec_candidate_source_contract_missing",
    ]
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_GENERATION_CONTRACT_REMAINING_GAPS
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

    preflight = report[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]
    assert (
        preflight["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )

    assert (
        payload["gate_id"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )
    assert payload["gate_status"] == (
        "implemented_offline_primitivespec_generation_contract_only_partial"
    )
    assert (
        payload["closed_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
    )
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


def test_cpd_paper_primitivespec_generation_payload_schema_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
    ]

    assert set(payload) == PRIMITIVESPEC_GENERATION_PAYLOAD_REQUIRED_KEYS
    assert payload["schema_version"] == 1
    assert payload["source_scope"] == "synthetic_toy_fixtures_only"
    assert payload["implementation_boundary"] == (
        "offline_primitivespec_generation_templates_only_no_runtime_"
        "primitivespec_no_collision_package_no_newton"
    )
    assert payload["input_contract_summary"] == {
        "input_gate_id": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ),
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
        "input_gate_required": (
            EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ),
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


def test_cpd_paper_primitivespec_generation_emits_native_family_templates_only():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
    ]
    rows = {
        row["paper_primitive"]: row
        for row in payload["native_family_primitivespec_template_rows"]
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


def test_cpd_paper_primitivespec_generation_records_blocked_and_noop_family_rows():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
    ]
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
        assert row["primitive_spec_generation_action"] == (
            "require_explicit_approximation_policy"
        )
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
        row["required_later_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert row["required_future_policy"] == "mapped_current_candidate_source"


def test_cpd_paper_primitivespec_generation_keeps_current_rows_no_generation():
    report = build_cpd_paper_offline_report()
    preflight = report[
        "paper_mapped_subset_primitivespec_generation_preflight_contract"
    ]
    payload = report["paper_mapped_subset_primitivespec_generation_contract"]
    rows = payload["current_row_primitivespec_generation_rows"]
    upstream_rows = preflight["current_row_primitivespec_generation_preflight_rows"]

    assert len(rows) == len(upstream_rows) == 16
    for row, upstream_row in zip(rows, upstream_rows):
        assert set(row) == PRIMITIVESPEC_GENERATION_CURRENT_ROW_REQUIRED_KEYS
        assert row["source_primitivespec_generation_preflight_row_id"] == (
            upstream_row["primitive_spec_generation_preflight_row_id"]
        )
        assert row["source_primitivespec_validation_row_id"] == (
            upstream_row["source_primitivespec_validation_row_id"]
        )
        assert row["source_primitivespec_dry_run_row_id"] == (
            upstream_row["source_primitivespec_dry_run_row_id"]
        )
        assert row["source_adapter_preflight_row_id"] == (
            upstream_row["source_adapter_preflight_row_id"]
        )
        assert row["source_candidate_matrix_row_id"] == (
            upstream_row["source_candidate_matrix_row_id"]
        )
        assert row["source_conversion_plan_row_id"] == (
            upstream_row["source_conversion_plan_row_id"]
        )
        assert row["source_policy_decision_id"] == (
            upstream_row["source_policy_decision_id"]
        )
        assert row["source_adapter_decision_id"] == (
            upstream_row["source_adapter_decision_id"]
        )
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


def test_cpd_paper_primitivespec_generation_coverage_summary_is_exact():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
    ]
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


def test_cpd_paper_primitivespec_generation_stays_report_only():
    payload = build_cpd_paper_offline_report()[
        "paper_mapped_subset_primitivespec_generation_contract"
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
        match=(
            "primitivespec_generation_input_contract_mismatch:"
            "expected_current_row_count"
        ),
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
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["paper_primitive"] = "sphere"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_family_primitive_sequence_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_future_family_contract_drift():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["candidate_mapping_label"] = "sphere"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_generation_future_family_contract_mismatch:"
            "oriented_bounding_box"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_blocked_family_contract_drift():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    capped_cylinder = next(
        row for row in rows if row["paper_primitive"] == "capped_cylinder"
    )
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
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["source_conversion_plan_row_id"] = ""
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_generation_missing_preflight_row_id:"
            "source_conversion_plan_row_id"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_unknown_family_decision():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["primitive_spec_generation_preflight_decision"] = "misspelled"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="unknown_primitivespec_generation_preflight_family_decision:misspelled",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_unknown_current_decision():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
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
            "primitivespec_generation_template_runtime_leak:"
            "generation_preflight_candidate",
        ),
        (
            "generated_primitive_spec",
            {"kind": "box"},
            "primitivespec_generation_template_runtime_leak:"
            "generated_primitive_spec",
        ),
    ],
)
def test_cpd_paper_primitivespec_generation_rejects_native_template_runtime_leaks(
    field_name,
    field_value,
    error_label,
):
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0][field_name] = field_value
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_template_candidate_source_gate_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    rows[0]["required_later_gate"] = "stale_gate"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match=(
            "primitivespec_generation_template_required_current_candidate_"
            "source_gate_mismatch"
        ),
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_requirement_required_later_gate_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    capped_cylinder = next(
        row for row in rows if row["paper_primitive"] == "capped_cylinder"
    )
    capped_cylinder["required_later_gate"] = "stale_gate"
    preflight["primitive_spec_generation_preflight_requirement_rows"] = rows

    with pytest.raises(
        ValueError,
        match="primitivespec_generation_requirement_required_later_gate_mismatch",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_current_source_id_gap():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
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
    rows = [
        dict(row)
        for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
    rows[0][field_name] = field_value
    preflight["current_row_primitivespec_generation_preflight_rows"] = rows

    with pytest.raises(ValueError, match=error_label):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_primitivespec_generation_rejects_current_row_gate_mismatch():
    preflight = _generation_contract_preflight_input()
    rows = [
        dict(row)
        for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
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
        dict(row)
        for row in preflight[
            "primitive_spec_generation_preflight_requirement_rows"
        ]
    ]
    current_rows = [
        dict(row)
        for row in preflight["current_row_primitivespec_generation_preflight_rows"]
    ]
    current_rows[0]["primitive_spec_generation_preflight_row_id"] = (
        requirement_rows[0]["primitive_spec_generation_preflight_row_id"]
    )
    preflight["primitive_spec_generation_preflight_requirement_rows"] = (
        requirement_rows
    )
    preflight["current_row_primitivespec_generation_preflight_rows"] = current_rows

    with pytest.raises(
        ValueError,
        match="duplicate_primitivespec_generation_preflight_row_id",
    ):
        _paper_mapped_subset_primitivespec_generation_contract_payload(preflight)


def test_cpd_paper_package_adapter_contract_blocks_malformed_or_duplicate_records():
    report = build_cpd_paper_offline_report()
    changed = dict(report["paper_offline_changed_decomposition_output_contract"])
    output_rows = [
        dict(row) for row in changed["decomposition_output_rows"][:1]
    ]
    original = dict(output_rows[0]["primitive_records"][0])
    missing_id = {
        key: value for key, value in original.items() if key != "offline_primitive_id"
    }
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


def test_cpd_paper_package_adapter_missing_id_fallback_cannot_collide_with_real_id():
    report = build_cpd_paper_offline_report()
    changed = dict(report["paper_offline_changed_decomposition_output_contract"])
    output_rows = [dict(report["paper_offline_changed_decomposition_output_contract"][
        "decomposition_output_rows"
    ][0])]
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
    assert rows[1]["offline_primitive_id"].startswith(
        "__missing_offline_primitive_id__:"
    )


def test_cpd_paper_source_policy_generalization_rows_match_case_payloads():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}
    payload = report["paper_generalization_batch_a_source_policy"]
    rows = {row["policy_row_id"]: row for row in payload["policy_matrix"]}

    mixed = cases["paper_mixed_face_preprocess_operator"]
    mixed_row = rows["accepted_mixed_triangle_quad_polygon_exact_dedup"]
    assert mixed_row["evidence_case_id"] == mixed["case_id"]
    assert mixed_row["row_status"] == "accepted_offline_policy_fixture"
    assert mixed_row["source_face_arities"] == mixed["source_mesh"]["source_face_arities"]
    assert mixed_row["source_face_count"] == mixed["source_mesh"]["source_face_count"]
    assert mixed_row["triangulated_face_count"] == mixed["source_mesh"][
        "triangulated_face_count"
    ]
    assert mixed_row["duplicate_vertex_preprocessing"] == mixed["source_mesh"][
        "duplicate_vertex_preprocessing"
    ]
    assert mixed_row["operator_aggregate_count"] == len(
        mixed["operator_audit"]["source_face_operator_aggregates"]
    )
    assert mixed_row["source_face_remap_count"] == len(
        mixed["source_mesh"]["source_face_remap"]
    )
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
    face_q_by_id = {
        face["face_id"]: face["q_matrix"] for face in mixed["operator_audit"]["faces"]
    }
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
    assert degenerate_row["dropped_source_face_ids"] == degenerate["preprocessing_audit"][
        "dropped_source_face_ids"
    ]
    assert degenerate_row["retained_source_face_ids"] == degenerate["preprocessing_audit"][
        "retained_source_face_ids"
    ]
    assert degenerate_row["executable_source_face_ids"] == degenerate["source_mesh"][
        "executable_source_face_ids"
    ]
    assert degenerate_row["operator_source_faces"] == degenerate["operator_audit"][
        "merged_group"
    ]["source_faces"]
    assert degenerate_row["primitive_fit_source_faces"] == degenerate[
        "primitive_fit_audit"
    ]["source_faces"]

    concave = cases["paper_concave_polygon_rejected"]
    concave_row = rows["rejected_concave_polygon"]
    assert concave_row["evidence_case_id"] == concave["case_id"]
    assert concave_row["row_status"] == "unsupported_offline_policy_fixture"
    assert concave_row["case_status"] == concave["case_status"]
    assert concave_row["failure_label"] == concave["mesh_intake_policy_audit"][
        "failure_label"
    ]
    assert concave_row["top_level_failure_label"] is False
    assert concave_row["source_face_arities"] == concave["source_mesh"][
        "source_face_arities"
    ]
    assert concave_row["triangulated_face_count"] == 0
    assert concave_row["operator_row_count"] == 0
    assert concave_row["primitive_fit_row_count"] == 0


def test_cpd_paper_offline_report_covers_first_toy_slice():
    report = build_cpd_paper_offline_report()

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
    assert (
        report["next_required_gate"]
        == EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_CANDIDATE_SOURCE_CONTRACT
    )
    assert (
        report["paper_faithfulness"]["missing_before_paper_faithful_offline"]
        == EXPECTED_CURRENT_OUTPUT_CONTRACT_GAPS
    )
    assert "paper_faithful_offline_generalization_plan" not in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_faithful_offline_generalization_plan" in report[
        "paper_faithfulness"
    ]["implemented_planning_scope"]
    assert "priority_queue_trace_audit_topology_only" in report["paper_faithfulness"][
        "implemented_fixture_scope"
    ]
    assert "component_pair_edge_insertion_audit_threshold_disabled" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "component_pair_threshold_blocking_audit" in report["paper_faithfulness"][
        "implemented_fixture_scope"
    ]
    assert "postprocess_enclosed_primitive_culling_audit" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_polygon_quad_intake_policy_audit" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_obb_sphere_fit_faithfulness_audit" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_duplicate_vertex_preprocessing_audit" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_faithful_offline_scope_audit" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_fixture_breadth_batch_a_source_preprocess_intake_operator" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_fixture_breadth_batch_b_primitive_fit" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_fixture_breadth_batch_c_cost_search_stop" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_fixture_breadth_batch_d_component_pair" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_fixture_breadth_batch_e_postprocess" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]
    assert "paper_fixture_breadth_completion_review" in report[
        "paper_faithfulness"
    ]["implemented_fixture_scope"]

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
    _assert_duplicate_vertex_preprocessing_case(
        cases["paper_duplicate_vertex_preprocessing"]
    )

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
        row["capsule_volume"]
        for row in capsule_dims["paper_capsule_axis_candidates"]
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
            radial = [
                relative[index] - projected * axis[index]
                for index in range(3)
            ]
            radial_distance_squared = sum(value * value for value in radial)
            cap_allowance = sqrt(
                max(candidate["radius"] ** 2 - radial_distance_squared, 0.0)
            )
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
        row["flat_cylinder_volume"]
        for row in capped_dims["flat_cylinder_axis_candidates"]
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
    assert [
        audit["source_faces"] for audit in merge_case["primitive_fit_audits"]
    ] == [[0], [1], [0, 1]]
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
    assert (
        postprocess["postprocess_input_source"]
        == "explicit_audit_primitives_not_search_trace"
    )
    assert (
        postprocess["postprocess_policy"]
        == "remove_primitives_enclosed_by_another_primitive"
    )
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


def test_cpd_paper_offline_report_is_strict_json_serializable():
    report = build_cpd_paper_offline_report()

    encoded = json.dumps(report, allow_nan=False, sort_keys=True)

    assert "cpd_paper_offline_report" in encoded


def test_cpd_paper_offline_report_audits_frustum_and_trapezoidal_prism_candidates():
    report = build_cpd_paper_offline_report()
    cases = {case["case_id"]: case for case in report["cases"]}

    frustum_case = cases["paper_frustum_like"]
    frustum_rows = {
        row["paper_primitive"]: row
        for row in frustum_case["primitive_fit_audit"]["candidates"]
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
        row["flat_cylinder_volume"]
        for row in frustum_dims["flat_cylinder_axis_candidates"]
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
        row["paper_primitive"]: row
        for row in trap_case["primitive_fit_audit"]["candidates"]
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
        4.0
        * trap_dims["h_x"]
        * trap_dims["h_y"]
        * (trap_dims["h_zt"] + trap_dims["h_zb"])
    )
    assert abs(trap["volume"] - expected_trap_volume) < 1e-9
    assert abs(trap["weighted_volume"] - trap["volume"] * 1.4) < 1e-9


def test_cpd_paper_frustum_and_trapezoidal_prism_stay_out_of_runtime_primitives():
    assert "frustum" not in SUPPORTED_PRIMITIVES
    assert "trapezoidal_prism" not in SUPPORTED_PRIMITIVES
