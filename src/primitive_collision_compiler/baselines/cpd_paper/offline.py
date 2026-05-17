from __future__ import annotations

from dataclasses import dataclass
from math import pi

import numpy as np
from numpy.typing import NDArray

from primitive_collision_compiler.baselines.cpd_like.primitives import (
    MIN_DIMENSION,
)
from primitive_collision_compiler.geometry.mesh import TriangleMesh

CPD_PAPER_OFFLINE_CLAIM_BOUNDARY = (
    "fixture_scoped_cpd_paper_offline_report_not_runtime_or_benchmark"
)
CPD_PAPER_OFFLINE_EVIDENCE_LEVEL = "offline_cpd_paper_toy_fixture_audit"
CPD_PAPER_OFFLINE_STATUS_SEMANTICS = (
    "fixture_scoped_paper_mechanics_audit_not_full_reproduction"
)
PAPER_Q_EPSILON = 1e-6
PAPER_PRIMITIVE_MIN_DIMENSION = 1e-3
PAPER_PRIMITIVE_WEIGHTS = {
    "oriented_bounding_box": 1.0,
    "sphere": 1.0,
    "capsule": 1.0,
    "capped_cylinder": 1.05,
    "frustum": 2.1,
    "trapezoidal_prism": 1.4,
}
_AUDITED_PAPER_PRIMITIVES = (
    "oriented_bounding_box",
    "sphere",
    "capsule",
    "capped_cylinder",
    "frustum",
    "trapezoidal_prism",
)
_PAPER_PRIMITIVE_NAMES = {
    "box": "oriented_bounding_box",
    "sphere": "sphere",
}
_NEWTON_RUNTIME_KIND = {
    "box": "box",
    "sphere": "sphere",
}
_SCOPE_AUDIT_ALLOWED_STATUSES = {
    "implemented_fixture_scope",
    "partial_fixture_scope",
    "not_started",
    "blocked_until_later_gate",
}
_SCOPE_AUDIT_ALLOWED_ALIGNMENT_LABELS = {
    "fixture_scoped_paper_shaped",
    "paper_aligned_boundary",
    "not_paper_faithful",
    "out_of_offline_scope",
}
_PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY = "paper_generalization_batch_a_source_policy"
_PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT = (
    "paper_generalization_batch_b_primitive_fit_engine"
)
_PAPER_GENERALIZATION_BATCH_C_SEARCH = "paper_generalization_batch_c_search_engine"
_PAPER_GENERALIZATION_BATCH_D_POSTPROCESS = "paper_generalization_batch_d_postprocess_policy"
_PAPER_GENERALIZATION_BATCH_E_PACKAGE_BOUNDARY = (
    "paper_generalization_batch_e_package_boundary_readiness"
)
_PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT = (
    "paper_offline_changed_decomposition_output_contract"
)
_PAPER_PACKAGE_GENERATION_CONTRACT = "paper_package_generation_contract"
_PAPER_PACKAGE_ADAPTER_CONTRACT = "paper_package_adapter_contract"
_PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY = (
    "paper_package_adapter_unsupported_primitive_policy"
)
_PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN = (
    "paper_package_conversion_mapped_subset_plan"
)
_PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX = (
    "paper_mapped_subset_conversion_candidate_matrix"
)
_PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_adapter_preflight_contract"
)
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT = (
    "paper_mapped_subset_primitivespec_dry_run_contract"
)
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_validation_contract"
)
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_primitivespec_generation_preflight_contract"
)
_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_generation_contract"
)
_PAPER_GENERALIZATION_NEXT_ACTION = (
    "Proceed to paper_package_adapter_contract after the changed-decomposition "
    "output contract; keep package/Newton wording blocked."
)


@dataclass(frozen=True)
class _SourceFaceRemap:
    source_face_id: int
    source_face_arity: int
    source_vertex_ids: tuple[int, ...]
    generated_triangle_face_ids: tuple[int, ...]
    generated_triangle_vertex_ids: tuple[tuple[int, int, int], ...]


@dataclass(frozen=True)
class _SourceFaceIntakeAudit:
    source_face_arities: tuple[int, ...]
    source_face_remap: tuple[_SourceFaceRemap, ...]
    face_arity_policy: str = "fan_triangulate_non_triangle_faces_preserve_source_face_remap"
    operator_ownership_policy: str = "triangulated_subfaces_summed_to_source_face"


@dataclass(frozen=True)
class _DuplicateVertexPreprocessingAudit:
    input_points: tuple[tuple[float, float, float], ...]
    input_faces: tuple[tuple[int, int, int], ...]
    deduplicated_points: tuple[tuple[float, float, float], ...]
    deduplicated_faces: tuple[tuple[int, int, int], ...]
    original_to_deduplicated_vertex_ids: tuple[int, ...]
    duplicate_clusters: tuple[tuple[int, ...], ...]
    distance_tolerance: float = 0.0


@dataclass(frozen=True)
class _UnsupportedSourceFaceIntakeAudit:
    source_face_id: int
    source_face_arity: int
    source_vertex_ids: tuple[int, ...]
    failure_label: str = "source_face_intake_unsupported_concave_polygon"
    case_status: str = "unsupported_fixture_policy"
    rejection_reason: str = "concave_non_triangle_source_face"


@dataclass(frozen=True)
class _PaperToyCase:
    case_id: str
    description: str
    mesh: TriangleMesh
    face_groups: tuple[frozenset[int], ...]
    collapse_pair: tuple[frozenset[int], frozenset[int]] | None = None
    priority_queue_target_count: int | None = None
    component_pair_edge_insertion: bool = False
    component_pair_excess_volume_threshold: float | None = None
    component_pair_candidate_cap: int | None = None
    postprocess_fixture: bool = False
    postprocess_audit_variant: str | None = None
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None
    duplicate_vertex_preprocessing_audit: _DuplicateVertexPreprocessingAudit | None = None
    unsupported_source_face_intake_audit: _UnsupportedSourceFaceIntakeAudit | None = None
    fixture_breadth_batch: str | None = None
    executable_source_face_ids: tuple[int, ...] | None = None


@dataclass(frozen=True)
class _PaperPrimitiveFitProbe:
    probe_id: str
    target_paper_primitive: str
    mesh: TriangleMesh
    variant_parameters: dict[str, object]


def _paper_faithful_offline_scope_criteria() -> list[dict[str, object]]:
    criteria: list[dict[str, object]] = [
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
            "next_action": _PAPER_GENERALIZATION_NEXT_ACTION,
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
            "next_action": _PAPER_GENERALIZATION_NEXT_ACTION,
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
            "next_action": _PAPER_GENERALIZATION_NEXT_ACTION,
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
            "next_action": _PAPER_GENERALIZATION_NEXT_ACTION,
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
            "next_action": _PAPER_GENERALIZATION_NEXT_ACTION,
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
            "next_action": _PAPER_GENERALIZATION_NEXT_ACTION,
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
            "next_action": _PAPER_GENERALIZATION_NEXT_ACTION,
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
            "next_action": _PAPER_GENERALIZATION_NEXT_ACTION,
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
            "next_action": _PAPER_GENERALIZATION_NEXT_ACTION,
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
    for row in criteria:
        if row["status"] not in _SCOPE_AUDIT_ALLOWED_STATUSES:
            raise ValueError(f"unsupported scope audit status: {row['status']}")
        if (
            row["surrogate_or_paper_faithful"]
            not in _SCOPE_AUDIT_ALLOWED_ALIGNMENT_LABELS
        ):
            raise ValueError(
                "unsupported scope audit alignment label: "
                f"{row['surrogate_or_paper_faithful']}"
            )
    return criteria


def _paper_faithful_offline_scope_audit_payload() -> dict[str, object]:
    criteria = _paper_faithful_offline_scope_criteria()
    blocking = [
        str(row["criterion_id"])
        for row in criteria
        if row["blocking_for_paper_faithful_offline"]
    ]
    return {
        "audit_scope": "fixture_scoped_offline_paper_lane",
        "audit_version": 1,
        "decision": "remain_partial",
        "paper_faithful_offline_allowed": False,
        "decision_reason": "fixture_scope_still_partial",
        "criteria": criteria,
        "blocking_criteria_ids": blocking,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_fixture_breadth_completed_batches() -> list[dict[str, object]]:
    return [
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


def _paper_fixture_breadth_completion_review_payload() -> dict[str, object]:
    criteria = [
        row
        for row in _paper_faithful_offline_scope_criteria()
        if row["blocking_for_paper_faithful_offline"]
    ]
    remaining_blockers = [str(row["criterion_id"]) for row in criteria]
    return {
        "review_scope": "synthetic_fixture_breadth_batches_a_to_e",
        "closed_gate": "paper_fixture_breadth_expansion",
        "decision": "remain_partial",
        "decision_reason": "fixture_breadth_complete_but_generalization_missing",
        "fixture_breadth_plan_complete": True,
        "paper_faithful_offline_allowed": False,
        "next_required_gate": "paper_faithful_offline_generalization_plan",
        "completed_batches": _paper_fixture_breadth_completed_batches(),
        "criteria_after_completion": [
            {
                "criterion_id": str(row["criterion_id"]),
                "fixture_breadth_status": "covered_by_named_synthetic_fixtures",
                "status_after_completion": "partial_fixture_scope",
                "remaining_gap": "paper_faithful_offline_generalization",
                "claim_boundary": str(row["claim_boundary"]),
            }
            for row in criteria
        ],
        "remaining_blocking_criteria_ids": remaining_blockers,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_faithful_offline_generalization_batches() -> list[dict[str, object]]:
    return [
        {
            "batch_id": _PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY,
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
            "batch_id": _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
            "purpose": "generalize_paper_primitive_fit_engine_beyond_named_cases",
            "primary_criteria": [
                "primitive_vocabulary_and_fit",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "primitive_fit_engine_generalization_report",
        },
        {
            "batch_id": _PAPER_GENERALIZATION_BATCH_C_SEARCH,
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
            "batch_id": _PAPER_GENERALIZATION_BATCH_D_POSTPROCESS,
            "purpose": "generalize_enclosed_primitive_postprocess_policy",
            "primary_criteria": [
                "enclosed_primitive_postprocess",
            ],
            "implementation_boundary": "offline_report_only_no_package_or_newton",
            "required_output": "postprocess_policy_generalization_report",
        },
        {
            "batch_id": _PAPER_GENERALIZATION_BATCH_E_PACKAGE_BOUNDARY,
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


def _paper_remaining_generalization_gates_after(closed_gates: set[str]) -> list[str]:
    return [
        str(batch["batch_id"])
        for batch in _paper_faithful_offline_generalization_batches()
        if str(batch["batch_id"]) not in closed_gates
    ]


def _paper_remaining_generalization_gates_after_source_policy() -> list[str]:
    return _paper_remaining_generalization_gates_after(
        {_PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY}
    )


def _paper_remaining_generalization_gates_after_primitive_fit() -> list[str]:
    return _paper_remaining_generalization_gates_after(
        {
            _PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY,
            _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
        }
    )


def _paper_remaining_generalization_gates_after_search() -> list[str]:
    return _paper_remaining_generalization_gates_after(
        {
            _PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY,
            _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
            _PAPER_GENERALIZATION_BATCH_C_SEARCH,
        }
    )


def _paper_remaining_generalization_gates_after_postprocess() -> list[str]:
    return _paper_remaining_generalization_gates_after(
        {
            _PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY,
            _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
            _PAPER_GENERALIZATION_BATCH_C_SEARCH,
            _PAPER_GENERALIZATION_BATCH_D_POSTPROCESS,
        }
    )


def _paper_remaining_generalization_gates_after_package_boundary() -> list[str]:
    return _paper_remaining_generalization_gates_after(
        {
            _PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY,
            _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
            _PAPER_GENERALIZATION_BATCH_C_SEARCH,
            _PAPER_GENERALIZATION_BATCH_D_POSTPROCESS,
            _PAPER_GENERALIZATION_BATCH_E_PACKAGE_BOUNDARY,
        }
    )


def _paper_remaining_gaps_after_package_boundary() -> list[str]:
    return [
        _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
        _PAPER_PACKAGE_GENERATION_CONTRACT,
    ]


def _paper_remaining_gaps_after_changed_decomposition_contract() -> list[str]:
    return [_PAPER_PACKAGE_ADAPTER_CONTRACT]


def _paper_remaining_gaps_after_package_adapter_contract() -> list[str]:
    return [_PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY]


def _paper_remaining_gaps_after_unsupported_primitive_policy() -> list[str]:
    return [_PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN]


def _paper_remaining_gaps_after_conversion_mapped_subset_plan() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX]


def _paper_remaining_gaps_after_mapped_subset_candidate_matrix() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT]


def _paper_remaining_gaps_after_mapped_subset_adapter_preflight() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT]


def _paper_remaining_gaps_after_mapped_subset_primitivespec_dry_run() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT]


def _paper_remaining_gaps_after_mapped_subset_primitivespec_validation() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT]


def _paper_remaining_gaps_after_mapped_subset_primitivespec_generation_preflight() -> list[str]:
    return [_PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT]


def _paper_faithful_offline_generalization_plan_payload() -> dict[str, object]:
    planned_batches = _paper_faithful_offline_generalization_batches()
    remaining_generalization_gates = (
        _paper_remaining_generalization_gates_after_package_boundary()
    )
    return {
        "plan_scope": "offline_algorithm_generalization_beyond_named_toy_fixtures",
        "closed_gate": "paper_faithful_offline_generalization_plan",
        "decision": "remain_partial",
        "decision_reason": (
            "changed_decomposition_output_contract_complete_package_adapter_contract_missing"
        ),
        "generalization_plan_complete": True,
        "paper_faithful_offline_allowed": False,
        "next_required_gate": _PAPER_PACKAGE_ADAPTER_CONTRACT,
        "first_unresolved_gate": _PAPER_PACKAGE_ADAPTER_CONTRACT,
        "planned_batches": planned_batches,
        "remaining_generalization_gates": remaining_generalization_gates,
        "blocked_runtime_gates": [
            "package_generation_boundary",
            "newton_runtime_boundary",
            "real_usd_boundary",
            "benchmark_evaluation_boundary",
        ],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_primitive_fit_engine_probe_specs() -> list[_PaperPrimitiveFitProbe]:
    return [
        _PaperPrimitiveFitProbe(
            probe_id="paper_fit_engine_rotated_obb_probe",
            target_paper_primitive="oriented_bounding_box",
            mesh=_paper_rotated_box_fit_mesh(),
            variant_parameters={"shape_family": "rotated_nonuniform_cuboid"},
        ),
        _PaperPrimitiveFitProbe(
            probe_id="paper_fit_engine_offset_sphere_probe",
            target_paper_primitive="sphere",
            mesh=_paper_offset_sphere_fit_mesh(),
            variant_parameters={"shape_family": "offset_cuboid_with_asymmetric_point"},
        ),
        _PaperPrimitiveFitProbe(
            probe_id="paper_fit_engine_off_axis_capsule_probe",
            target_paper_primitive="capsule",
            mesh=_paper_off_axis_capsule_fit_mesh(),
            variant_parameters={"shape_family": "elongated_off_axis_cuboid"},
        ),
        _PaperPrimitiveFitProbe(
            probe_id="paper_fit_engine_flat_capped_cylinder_probe",
            target_paper_primitive="capped_cylinder",
            mesh=_paper_flat_capped_cylinder_axis_fit_mesh(),
            variant_parameters={
                "shape_family": "off_axis_flat_capped_cylinder_like_cuboid"
            },
        ),
        _PaperPrimitiveFitProbe(
            probe_id="paper_fit_engine_tapered_frustum_probe",
            target_paper_primitive="frustum",
            mesh=_paper_tapered_frustum_fit_mesh(),
            variant_parameters={
                "shape_family": "tapered_unequal_radius_frustum_like_mesh"
            },
        ),
        _PaperPrimitiveFitProbe(
            probe_id="paper_fit_engine_asymmetric_trapezoid_probe",
            target_paper_primitive="trapezoidal_prism",
            mesh=_paper_asymmetric_trapezoid_fit_mesh(),
            variant_parameters={
                "shape_family": "asymmetric_trapezoidal_prism_like_wedge"
            },
        ),
    ]


def _numeric_values(value: object) -> list[float]:
    if isinstance(value, bool):
        return []
    if isinstance(value, int | float):
        return [float(value)]
    if isinstance(value, list | tuple):
        values: list[float] = []
        for item in value:
            values.extend(_numeric_values(item))
        return values
    if isinstance(value, dict):
        values = []
        for item in value.values():
            values.extend(_numeric_values(item))
        return values
    return []


def _candidate_numeric_fields_are_finite(candidate: dict[str, object]) -> bool:
    return all(np.isfinite(value) for value in _numeric_values(candidate))


def _paper_primitive_fit_engine_generalization_payload() -> dict[str, object]:
    remaining_generalization_gates = (
        _paper_remaining_generalization_gates_after_primitive_fit()
    )
    matrix: list[dict[str, object]] = []
    for probe in _paper_primitive_fit_engine_probe_specs():
        face_group = frozenset(range(len(probe.mesh.faces)))
        audit = _primitive_fit_audit_payload(probe.mesh, face_group)
        candidates = audit["candidates"]
        target_candidate = next(
            candidate
            for candidate in candidates
            if candidate["paper_primitive"] == probe.target_paper_primitive
        )
        selected_candidate = audit["selected"]
        matrix.append(
            {
                "probe_id": probe.probe_id,
                "target_paper_primitive": probe.target_paper_primitive,
                "variant_parameters": probe.variant_parameters,
                "candidate_row_count": len(candidates),
                "candidate_order": [
                    str(candidate["paper_primitive"]) for candidate in candidates
                ],
                "missing_paper_primitives": audit["missing_paper_primitives"],
                "target_candidate": target_candidate,
                "selected_candidate": selected_candidate,
                "target_candidate_selected": (
                    selected_candidate["paper_primitive"]
                    == probe.target_paper_primitive
                ),
                "contains_assigned_points": bool(
                    target_candidate["contains_assigned_points"]
                ),
                "finite_numeric_fields": all(
                    _candidate_numeric_fields_are_finite(candidate)
                    for candidate in candidates
                ),
                "newton_runtime_kind": target_candidate["newton_runtime_kind"],
                "package_generation_triggered": False,
                "newton_runtime_triggered": False,
                "real_usd_triggered": False,
                "benchmark_triggered": False,
            }
        )
    return {
        "gate_id": _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
        "gate_status": "implemented_offline_report_only_partial",
        "closed_gate": _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
        "next_required_gate": _PAPER_GENERALIZATION_BATCH_C_SEARCH,
        "decision": "remain_partial",
        "decision_reason": (
            "primitive_fit_engine_generalization_complete_search_engine_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "source_scope": "deterministic_in_memory_parametric_primitive_fit_probes",
        "implementation_boundary": "offline_report_only_no_package_or_newton",
        "engine_contract": {
            "input_contract": "TriangleMesh_plus_face_group",
            "candidate_set": list(_AUDITED_PAPER_PRIMITIVES),
            "candidate_evaluation_policy": "evaluate_all_candidates_no_runtime_mapping",
            "selection_rule": "min_paper_weighted_volume_then_candidate_order",
            "containment_scope": (
                "assigned_vertices_only_not_surface_or_collision_quality"
            ),
            "axis_policy": "paper_q_eigenbasis_with_candidate_axis_enumeration",
            "offline_only_unmapped_primitives": [
                "capped_cylinder",
                "frustum",
                "trapezoidal_prism",
            ],
        },
        "primitive_family_matrix": matrix,
        "coverage_summary": {
            "primitive_count": len(_AUDITED_PAPER_PRIMITIVES),
            "probe_family_count": len(matrix),
            "generated_probe_count": len(matrix),
            "candidate_row_count": sum(
                int(row["candidate_row_count"]) for row in matrix
            ),
            "closed_gate_count": 2,
            "remaining_generalization_gate_count": len(remaining_generalization_gates),
        },
        "remaining_gaps": remaining_generalization_gates,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_search_engine_generalization_row_specs() -> list[tuple[str, str]]:
    return [
        ("topology_chain_target_count", "paper_three_face_chain"),
        ("weighted_priority_over_base_cost", "paper_branching_cost_order"),
        ("equal_cost_queue_tie", "paper_equal_cost_queue_tie"),
        ("component_pair_threshold_disabled_accept", "paper_disconnected_components"),
        ("component_pair_zero_threshold_block", "paper_component_pair_threshold_blocked"),
        ("component_pair_positive_threshold_block", "paper_nonzero_threshold_block"),
        (
            "component_pair_multi_candidate_order",
            "paper_component_pair_multi_candidate_order",
        ),
        ("component_pair_candidate_cap_skipped", "paper_component_pair_cap_skipped"),
    ]


def _first_accepted_queue_key(trace: dict[str, object]) -> list[object] | None:
    for event in trace["events"]:
        if bool(event["accepted"]):
            return list(event["queue_key"])
    return None


def _threshold_metric_from_trace(trace: dict[str, object]) -> str | None:
    for event in trace["events"]:
        if event.get("event_kind") == "blocked_by_threshold":
            return str(event["threshold_metric"])
    return None


def _search_trace_summary_row(
    row_id: str,
    case_payload: dict[str, object],
) -> dict[str, object]:
    trace = case_payload["collapse_trace"]
    return {
        "row_id": row_id,
        "evidence_case_id": case_payload["case_id"],
        "row_status": "implemented_offline_search_trace_fixture",
        "trace_scope": trace["trace_scope"],
        "priority_queue_policy": trace["priority_queue_policy"],
        "target_primitive_count": trace["target_primitive_count"],
        "initial_edge_count": trace["initial_edge_count"],
        "initial_candidate_count": len(trace["initial_candidates"]),
        "component_pair_edge_insertion_triggered": trace[
            "component_pair_edge_insertion_triggered"
        ],
        "topology_queue_exhausted_before_component_pair_insertion": trace[
            "topology_queue_exhausted_before_component_pair_insertion"
        ],
        "component_pair_candidate_count": trace["component_pair_candidate_count"],
        "component_pair_available_pair_count": trace[
            "component_pair_available_pair_count"
        ],
        "component_pair_candidate_cap": trace["component_pair_candidate_cap"],
        "skipped_component_pair_count": trace["skipped_component_pair_count"],
        "threshold_policy": trace["threshold_policy"],
        "excess_volume_threshold": trace["excess_volume_threshold"],
        "threshold_metric": _threshold_metric_from_trace(trace),
        "accepted_merge_count": trace["accepted_merge_count"],
        "blocked_merge_count": trace["blocked_merge_count"],
        "stale_entry_skipped_count": trace["stale_entry_skipped_count"],
        "event_count": len(trace["events"]),
        "event_kinds": [event["event_kind"] for event in trace["events"]],
        "first_accepted_queue_key": _first_accepted_queue_key(trace),
        "stop_reason": trace["stop_reason"],
        "final_active_groups": trace["final_active_groups"],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_search_engine_generalization_payload(
    cases: list[dict[str, object]],
) -> dict[str, object]:
    remaining_generalization_gates = _paper_remaining_generalization_gates_after_search()
    cases_by_id = {str(case["case_id"]): case for case in cases}
    matrix = [
        _search_trace_summary_row(row_id, cases_by_id[case_id])
        for row_id, case_id in _paper_search_engine_generalization_row_specs()
    ]
    return {
        "gate_id": _PAPER_GENERALIZATION_BATCH_C_SEARCH,
        "gate_status": "implemented_offline_report_only_partial",
        "closed_gate": _PAPER_GENERALIZATION_BATCH_C_SEARCH,
        "next_required_gate": _PAPER_GENERALIZATION_BATCH_D_POSTPROCESS,
        "decision": "remain_partial",
        "decision_reason": (
            "search_engine_generalization_complete_postprocess_policy_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "source_scope": "deterministic_in_memory_search_trace_probes",
        "implementation_boundary": "offline_report_only_no_package_or_newton",
        "search_engine_contract": {
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
        },
        "search_trace_matrix": matrix,
        "coverage_summary": {
            "search_trace_row_count": len(matrix),
            "topology_trace_row_count": sum(
                row["trace_scope"] == "topology_priority_queue_trace_fixture"
                for row in matrix
            ),
            "component_pair_trace_row_count": sum(
                row["trace_scope"] == "component_pair_priority_queue_trace_fixture"
                for row in matrix
            ),
            "threshold_blocked_row_count": sum(
                row["threshold_metric"] == "paper_base_cost" for row in matrix
            ),
            "closed_gate_count": 3,
            "remaining_generalization_gate_count": len(remaining_generalization_gates),
        },
        "remaining_gaps": remaining_generalization_gates,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_postprocess_policy_generalization_row_specs() -> list[tuple[str, str]]:
    return [
        ("identity_nested_obb_cull", "paper_nested_primitive"),
        ("rotated_nested_obb_cull", "paper_rotated_nested_primitive"),
        (
            "cross_type_enclosure_no_silent_cull_boundary",
            "paper_cross_type_enclosure_boundary",
        ),
    ]


def _postprocess_policy_summary_row(
    row_id: str,
    case_payload: dict[str, object],
) -> dict[str, object]:
    audit = case_payload["postprocess_audit"]
    return {
        "row_id": row_id,
        "evidence_case_id": case_payload["case_id"],
        "row_status": "implemented_offline_postprocess_fixture",
        "audit_scope": audit["audit_scope"],
        "fixture_variant": audit["fixture_variant"],
        "postprocess_input_source": audit["postprocess_input_source"],
        "postprocess_policy": audit["postprocess_policy"],
        "containment_test_type": audit["containment_test_type"],
        "axis_policy": audit.get("axis_policy"),
        "rotation_degrees_about_z": audit.get("rotation_degrees_about_z"),
        "rotated_axes_non_identity": audit.get("rotated_axes_non_identity"),
        "cross_type_culling_supported": audit.get("cross_type_culling_supported"),
        "unsupported_containment_label": audit.get("unsupported_containment_label"),
        "input_primitive_count": audit["input_primitive_count"],
        "output_primitive_count": audit["output_primitive_count"],
        "culled_primitive_ids": audit["culled_primitive_ids"],
        "kept_primitive_ids": audit["kept_primitive_ids"],
        "enclosed_primitive_ids": audit["enclosed_primitive_ids"],
        "enclosing_primitive_ids": audit["enclosing_primitive_ids"],
        "cull_record_count": len(audit["cull_records"]),
        "unsupported_record_count": len(audit.get("unsupported_records", [])),
        "top_level_failure_label": bool(audit.get("top_level_failure_label", False)),
        "claim_boundary": (
            "summarizes_named_postprocess_audits_not_general_containment_library"
        ),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_postprocess_policy_generalization_payload(
    cases: list[dict[str, object]],
) -> dict[str, object]:
    remaining_generalization_gates = (
        _paper_remaining_generalization_gates_after_postprocess()
    )
    cases_by_id = {str(case["case_id"]): case for case in cases}
    matrix = [
        _postprocess_policy_summary_row(row_id, cases_by_id[case_id])
        for row_id, case_id in _paper_postprocess_policy_generalization_row_specs()
    ]
    return {
        "gate_id": _PAPER_GENERALIZATION_BATCH_D_POSTPROCESS,
        "gate_status": "implemented_offline_report_only_partial",
        "closed_gate": _PAPER_GENERALIZATION_BATCH_D_POSTPROCESS,
        "next_required_gate": _PAPER_GENERALIZATION_BATCH_E_PACKAGE_BOUNDARY,
        "decision": "remain_partial",
        "decision_reason": (
            "postprocess_policy_generalization_complete_package_boundary_readiness_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "source_scope": "deterministic_in_memory_postprocess_audit_fixtures",
        "implementation_boundary": "offline_report_only_no_package_or_newton",
        "postprocess_policy_contract": {
            "input_contract": (
                "explicit_offline_postprocess_audit_primitives_not_search_output"
            ),
            "supported_containment_tests": ["obb_corners_inside_obb"],
            "supported_axis_policies": [
                "shared_identity_axes",
                "shared_rotated_axes",
            ],
            "unsupported_boundary_policy": (
                "record_cross_type_unsupported_without_silent_cull"
            ),
            "unsupported_boundary_label": (
                "cross_type_enclosure_boundary_not_supported"
            ),
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
        },
        "postprocess_policy_matrix": matrix,
        "coverage_summary": {
            "postprocess_row_count": len(matrix),
            "obb_cull_row_count": sum(
                row["containment_test_type"] == "obb_corners_inside_obb"
                and int(row["cull_record_count"]) > 0
                for row in matrix
            ),
            "rotated_obb_row_count": sum(
                row["rotated_axes_non_identity"] is True for row in matrix
            ),
            "unsupported_cross_type_row_count": sum(
                row["cross_type_culling_supported"] is False for row in matrix
            ),
            "cull_record_count": sum(int(row["cull_record_count"]) for row in matrix),
            "unsupported_record_count": sum(
                int(row["unsupported_record_count"]) for row in matrix
            ),
            "closed_gate_count": 4,
            "remaining_generalization_gate_count": len(remaining_generalization_gates),
        },
        "remaining_gaps": remaining_generalization_gates,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_package_boundary_readiness_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": "changed_decomposition_output_contract",
            "row_status": "blocked_until_changed_decomposition_output_contract",
            "required_before_unlock": (
                "stable_offline_decomposition_payload_with_primitive_ids_source_faces_"
                "parameters_and_postprocess_state"
            ),
            "current_evidence": (
                "Batches A-D expose source policy, primitive-fit, search, and postprocess "
                "audit matrices, but not a package-adapter-ready decomposition artifact."
            ),
            "blocked_reason": (
                "offline audit rows are review evidence, not a durable changed "
                "decomposition output contract"
            ),
            "next_gate_if_blocked": _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
            "claim_boundary": (
                "readiness review only; no package-ready decomposition output exists"
            ),
            "package_generation_triggered": False,
            "newton_runtime_triggered": False,
            "real_usd_triggered": False,
            "benchmark_triggered": False,
        },
        {
            "row_id": "package_generation_boundary",
            "row_status": "blocked_until_package_generation_contract",
            "required_before_unlock": (
                "explicit_collision_package_schema_mapping_from_changed_decomposition"
            ),
            "current_evidence": (
                "No CPD paper-lane CollisionPackage conversion is emitted by this report."
            ),
            "blocked_reason": (
                "package generation is a later adapter gate, not part of the offline "
                "paper-lane readiness review"
            ),
            "next_gate_if_blocked": _PAPER_PACKAGE_GENERATION_CONTRACT,
            "claim_boundary": "boundary matrix, not CollisionPackage generation",
            "package_generation_triggered": False,
            "newton_runtime_triggered": False,
            "real_usd_triggered": False,
            "benchmark_triggered": False,
        },
        {
            "row_id": "newton_runtime_boundary",
            "row_status": "blocked_until_newton_runtime_admissibility_gate",
            "required_before_unlock": (
                "runtime_admissibility_report_after_package_conversion_and_primitive_mapping"
            ),
            "current_evidence": (
                "Paper-lane primitive rows include offline-only paper primitives and no "
                "Newton runtime adapter pass."
            ),
            "blocked_reason": (
                "Newton execution must wait for package conversion and runtime "
                "admissibility checks"
            ),
            "next_gate_if_blocked": "paper_newton_runtime_admissibility_gate",
            "claim_boundary": "no Newton-ready or runtime-ready claim",
            "package_generation_triggered": False,
            "newton_runtime_triggered": False,
            "real_usd_triggered": False,
            "benchmark_triggered": False,
        },
        {
            "row_id": "real_usd_boundary",
            "row_status": "blocked_until_real_usd_asset_scope_gate",
            "required_before_unlock": (
                "small_real_usd_asset_scope_manifest_after_offline_contracts_exist"
            ),
            "current_evidence": (
                "This report uses deterministic synthetic fixtures and in-memory probes only."
            ),
            "blocked_reason": (
                "bed, Franka, and other real USD assets belong to a later asset-scope gate"
            ),
            "next_gate_if_blocked": "paper_real_usd_asset_scope_gate",
            "claim_boundary": "no real-USD evidence from this report",
            "package_generation_triggered": False,
            "newton_runtime_triggered": False,
            "real_usd_triggered": False,
            "benchmark_triggered": False,
        },
        {
            "row_id": "benchmark_evaluation_boundary",
            "row_status": "blocked_until_benchmark_evaluation_design_gate",
            "required_before_unlock": (
                "benchmark_design_with_metrics_assets_baselines_and_runtime_records"
            ),
            "current_evidence": (
                "No timing, surface-distance, collision-quality, byte-cost, or baseline "
                "comparison metrics are emitted."
            ),
            "blocked_reason": (
                "benchmark evaluation must wait for offline output, package, runtime, and "
                "asset-scope gates"
            ),
            "next_gate_if_blocked": "paper_benchmark_evaluation_design_gate",
            "claim_boundary": "no benchmark or collision-quality evidence",
            "package_generation_triggered": False,
            "newton_runtime_triggered": False,
            "real_usd_triggered": False,
            "benchmark_triggered": False,
        },
    ]


def _paper_package_boundary_readiness_payload() -> dict[str, object]:
    matrix = _paper_package_boundary_readiness_rows()
    remaining_generalization_gates = (
        _paper_remaining_generalization_gates_after_package_boundary()
    )
    return {
        "gate_id": _PAPER_GENERALIZATION_BATCH_E_PACKAGE_BOUNDARY,
        "gate_status": "implemented_planning_only_partial",
        "closed_gate": _PAPER_GENERALIZATION_BATCH_E_PACKAGE_BOUNDARY,
        "next_required_gate": _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
        "decision": "remain_partial",
        "decision_reason": (
            "package_boundary_readiness_review_complete_changed_decomposition_"
            "output_contract_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "source_scope": "offline_generalization_payloads_after_batches_a_to_d",
        "implementation_boundary": "planning_only_no_package_or_newton",
        "boundary_review_contract": {
            "input_scope": "implemented_offline_generalization_payloads_a_to_d",
            "review_output": "package_boundary_readiness_matrix_not_package_generation",
            "changed_decomposition_output_contract_required": True,
            "package_generation_contract_required": True,
            "runtime_admissibility_required_after_package_conversion": True,
            "package_generation_allowed": False,
            "newton_runtime_allowed": False,
            "real_usd_allowed": False,
            "benchmark_allowed": False,
        },
        "boundary_review_matrix": matrix,
        "coverage_summary": {
            "boundary_review_row_count": len(matrix),
            "blocked_row_count": len(matrix),
            "closed_gate_count": 5,
            "remaining_generalization_gate_count": len(remaining_generalization_gates),
            "package_generation_allowed_row_count": 0,
            "newton_runtime_allowed_row_count": 0,
            "real_usd_allowed_row_count": 0,
            "benchmark_allowed_row_count": 0,
        },
        "remaining_gaps": _paper_remaining_gaps_after_package_boundary(),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _source_face_ids_for_contract_group(
    source_mesh: dict[str, object],
    generated_triangle_face_ids: list[int],
) -> list[int]:
    remap = source_mesh.get("source_face_remap")
    if not isinstance(remap, list):
        return list(generated_triangle_face_ids)

    source_face_ids: list[int] = []
    for generated_face_id in generated_triangle_face_ids:
        for row in remap:
            generated_ids = row.get("generated_triangle_face_ids", [])
            if generated_face_id in generated_ids:
                source_face_id = int(row["source_face_id"])
                if source_face_id not in source_face_ids:
                    source_face_ids.append(source_face_id)
    return source_face_ids


def _source_mesh_contract_summary(case_payload: dict[str, object]) -> dict[str, object]:
    source_mesh = case_payload["source_mesh"]
    preprocessing = case_payload.get("preprocessing_audit", {})
    return {
        "vertex_count": source_mesh["vertex_count"],
        "face_count": source_mesh["face_count"],
        "connected_component_count": source_mesh["connected_component_count"],
        "source_face_count": source_mesh.get("source_face_count"),
        "source_face_arities": source_mesh.get("source_face_arities"),
        "duplicate_vertex_preprocessing": source_mesh.get(
            "duplicate_vertex_preprocessing"
        ),
        "source_face_remap_policy": (
            "explicit_generated_triangle_to_source_face_map"
            if isinstance(source_mesh.get("source_face_remap"), list)
            else source_mesh.get("source_face_remap")
        ),
        "retained_source_face_ids": preprocessing.get("retained_source_face_ids"),
        "dropped_source_face_ids": preprocessing.get("dropped_source_face_ids"),
    }


def _search_contract_summary(trace: dict[str, object]) -> dict[str, object]:
    return {
        "target_primitive_count": trace["target_primitive_count"],
        "initial_active_groups": trace["initial_active_groups"],
        "final_active_groups": trace["final_active_groups"],
        "stop_reason": trace["stop_reason"],
        "accepted_merge_count": trace["accepted_merge_count"],
        "blocked_merge_count": trace["blocked_merge_count"],
        "stale_entry_skipped_count": trace["stale_entry_skipped_count"],
        "threshold_policy": trace["threshold_policy"],
        "excess_volume_threshold": trace["excess_volume_threshold"],
        "component_pair_edge_insertion_triggered": trace[
            "component_pair_edge_insertion_triggered"
        ],
        "component_pair_candidate_count": trace["component_pair_candidate_count"],
        "skipped_component_pair_count": trace["skipped_component_pair_count"],
    }


def _offline_decomposition_primitive_records(
    case_payload: dict[str, object],
) -> list[dict[str, object]]:
    trace = case_payload["collapse_trace"]
    source_mesh = case_payload["source_mesh"]
    selected = case_payload["primitive_fit_audit"]["selected"]
    records = []
    for index, final_group in enumerate(trace["final_active_groups"]):
        generated_triangle_face_ids = [int(face_id) for face_id in final_group]
        records.append(
            {
                "offline_primitive_id": (
                    f"{case_payload['case_id']}:offline_primitive:{index}"
                ),
                "source_faces": generated_triangle_face_ids,
                "source_face_ids": _source_face_ids_for_contract_group(
                    source_mesh,
                    generated_triangle_face_ids,
                ),
                "generated_triangle_face_ids": generated_triangle_face_ids,
                "paper_primitive": selected["paper_primitive"],
                "center": selected["center"],
                "axes": selected["axes"],
                "dimensions": selected["dimensions"],
                "volume": selected["volume"],
                "paper_weight": selected["paper_weight"],
                "weighted_volume": selected["weighted_volume"],
                "contains_assigned_points": selected["contains_assigned_points"],
                "newton_runtime_kind": selected["newton_runtime_kind"],
                "primitive_fit_scope": (
                    "case_selected_candidate_reused_for_contract_row_not_group_refit"
                ),
                "conversion_status": "offline_contract_only_not_package_candidate",
            }
        )
    return records


def _offline_changed_decomposition_output_rows(
    cases: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows = []
    for case_payload in cases:
        trace = case_payload.get("collapse_trace")
        if not isinstance(trace, dict) or not isinstance(
            trace.get("final_active_groups"), list
        ):
            continue
        rows.append(
            {
                "output_id": (
                    f"{case_payload['case_id']}:changed_decomposition_output"
                ),
                "evidence_case_id": case_payload["case_id"],
                "row_status": "implemented_offline_contract_row",
                "source_mesh_summary": _source_mesh_contract_summary(case_payload),
                "search_summary": _search_contract_summary(trace),
                "primitive_records": _offline_decomposition_primitive_records(
                    case_payload
                ),
                "postprocess_state": "not_applied_to_search_output",
                "unsupported_boundaries": {
                    "package_adapter_contract_required": True,
                    "runtime_mapping_not_attempted": True,
                    "real_usd_not_loaded": True,
                    "benchmark_not_run": True,
                },
                "claim_boundary": (
                    "offline_changed_decomposition_contract_row_not_collision_package"
                ),
                "package_generation_triggered": False,
                "newton_runtime_triggered": False,
                "real_usd_triggered": False,
                "benchmark_triggered": False,
            }
        )
    return rows


def _paper_postprocess_state_contract_rows(
    cases: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows = []
    for case_payload in cases:
        postprocess = case_payload.get("postprocess_audit")
        if not isinstance(postprocess, dict):
            continue
        rows.append(
            {
                "state_id": f"{case_payload['case_id']}:postprocess_state",
                "evidence_case_id": case_payload["case_id"],
                "state_scope": "explicit_postprocess_audit_fixture_not_search_output",
                "postprocess_input_source": postprocess["postprocess_input_source"],
                "postprocess_policy": postprocess["postprocess_policy"],
                "kept_primitive_ids": postprocess["kept_primitive_ids"],
                "culled_primitive_ids": postprocess["culled_primitive_ids"],
                "cull_record_count": len(postprocess["cull_records"]),
                "unsupported_record_count": len(
                    postprocess.get("unsupported_records", [])
                ),
                "unsupported_containment_label": postprocess.get(
                    "unsupported_containment_label"
                ),
                "package_generation_triggered": False,
                "newton_runtime_triggered": False,
                "real_usd_triggered": False,
                "benchmark_triggered": False,
            }
        )
    return rows


def _paper_changed_decomposition_output_contract_payload(
    cases: list[dict[str, object]],
) -> dict[str, object]:
    decomposition_rows = _offline_changed_decomposition_output_rows(cases)
    postprocess_rows = _paper_postprocess_state_contract_rows(cases)
    source_policy = _paper_source_policy_generalization_payload(cases)
    primitive_fit = _paper_primitive_fit_engine_generalization_payload()
    search_engine = _paper_search_engine_generalization_payload(cases)
    package_boundary = _paper_package_boundary_readiness_payload()
    primitive_record_count = sum(
        len(row["primitive_records"]) for row in decomposition_rows
    )
    return {
        "gate_id": _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
        "gate_status": "implemented_offline_contract_only_partial",
        "closed_gate": _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
        "next_required_gate": _PAPER_PACKAGE_ADAPTER_CONTRACT,
        "decision": "remain_partial",
        "decision_reason": (
            "changed_decomposition_output_contract_complete_package_adapter_"
            "contract_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": "offline_changed_decomposition_output_not_collision_package",
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_report_contract_no_collision_package_no_newton"
        ),
        "output_contract": {
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
        },
        "source_policy_summary": {
            "policy_row_count": len(source_policy["policy_matrix"]),
            "general_mesh_cleanup_supported": False,
        },
        "primitive_vocabulary_summary": {
            "primitive_family_count": len(primitive_fit["primitive_family_matrix"]),
            "offline_only_unmapped_primitives": primitive_fit["engine_contract"][
                "offline_only_unmapped_primitives"
            ],
        },
        "search_contract_summary": {
            "search_trace_summary_row_count": len(
                search_engine["search_trace_matrix"]
            ),
            "search_policy": search_engine["search_engine_contract"][
                "primary_policy"
            ],
        },
        "postprocess_contract_summary": {
            "postprocess_state_row_count": len(postprocess_rows),
            "postprocess_policy_row_count": len(
                _paper_postprocess_policy_generalization_payload(cases)[
                    "postprocess_policy_matrix"
                ]
            ),
        },
        "package_boundary_summary": {
            "boundary_review_row_count": len(
                package_boundary["boundary_review_matrix"]
            ),
            "package_generation_allowed": False,
        },
        "decomposition_output_rows": decomposition_rows,
        "postprocess_state_rows": postprocess_rows,
        "coverage_summary": {
            "decomposition_output_row_count": len(decomposition_rows),
            "primitive_record_count": primitive_record_count,
            "postprocess_state_row_count": len(postprocess_rows),
            "source_policy_summary_row_count": len(source_policy["policy_matrix"]),
            "primitive_family_count": len(primitive_fit["primitive_family_matrix"]),
            "search_trace_summary_row_count": len(
                search_engine["search_trace_matrix"]
            ),
            "package_boundary_row_count": len(
                package_boundary["boundary_review_matrix"]
            ),
        },
        "remaining_gaps": _paper_remaining_gaps_after_changed_decomposition_contract(),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_adapter_required_fields_present(
    primitive_record: dict[str, object],
) -> bool:
    required_fields = (
        "offline_primitive_id",
        "source_face_ids",
        "generated_triangle_face_ids",
        "paper_primitive",
        "center",
        "axes",
        "dimensions",
        "volume",
        "paper_weight",
        "weighted_volume",
        "contains_assigned_points",
        "newton_runtime_kind",
    )
    return all(field in primitive_record for field in required_fields)


def _paper_adapter_numeric_fields_finite(value: object) -> bool:
    if isinstance(value, bool):
        return True
    if isinstance(value, int | float):
        return bool(np.isfinite(value))
    if isinstance(value, list | tuple):
        return all(_paper_adapter_numeric_fields_finite(item) for item in value)
    return True


def _paper_adapter_forbidden_trigger_present(output_row: dict[str, object]) -> bool:
    return any(
        bool(output_row.get(flag))
        for flag in (
            "package_generation_triggered",
            "newton_runtime_triggered",
            "real_usd_triggered",
            "benchmark_triggered",
        )
    )


def _paper_adapter_decision_for_primitive(
    output_row: dict[str, object],
    primitive_record: dict[str, object],
    *,
    duplicate_offline_primitive_id: bool = False,
) -> tuple[str, str, str, str]:
    if _paper_adapter_forbidden_trigger_present(output_row):
        return (
            "blocked",
            "forbidden_runtime_or_package_trigger_present",
            "paper_package_adapter_contract",
            "blocked_forbidden_trigger",
        )
    if not _paper_adapter_required_fields_present(primitive_record):
        return (
            "blocked",
            "adapter_required_fields_missing",
            "paper_package_adapter_contract",
            "missing_required_fields",
        )
    if not primitive_record["source_face_ids"] or not primitive_record[
        "generated_triangle_face_ids"
    ]:
        return (
            "blocked",
            "missing_source_face_mapping_blocks_adapter_contract",
            "paper_package_adapter_contract",
            "missing_source_face_mapping",
        )
    if duplicate_offline_primitive_id:
        return (
            "blocked",
            "duplicate_offline_primitive_id_blocks_adapter_contract",
            "paper_package_adapter_contract",
            "duplicate_offline_primitive_id",
        )
    if not all(
        _paper_adapter_numeric_fields_finite(primitive_record[field])
        for field in (
            "center",
            "axes",
            "dimensions",
            "volume",
            "paper_weight",
            "weighted_volume",
        )
    ):
        return (
            "blocked",
            "nonfinite_adapter_record_fields",
            "paper_package_adapter_contract",
            "invalid_numeric_fields",
        )
    if primitive_record["contains_assigned_points"] is not True:
        return (
            "blocked",
            "containment_false_blocks_adapter_contract",
            "paper_package_adapter_contract",
            "containment_false",
        )
    if primitive_record["newton_runtime_kind"] == "offline_only_unmapped":
        return (
            "later_policy_required",
            "unsupported_paper_primitive_requires_adapter_policy",
            _PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
            "complete",
        )
    return (
        "adapter_eligible",
        "direct_runtime_kind_has_complete_contract_fields",
        "none",
        "complete",
    )


def _paper_adapter_primitive_decision_row(
    output_row: dict[str, object],
    primitive_record: dict[str, object],
    row_index: int,
    duplicate_offline_primitive_id: bool = False,
) -> dict[str, object]:
    decision, reason, later_gate, field_status = _paper_adapter_decision_for_primitive(
        output_row,
        primitive_record,
        duplicate_offline_primitive_id=duplicate_offline_primitive_id,
    )
    offline_primitive_id = primitive_record.get(
        "offline_primitive_id",
        f"__missing_offline_primitive_id__:{output_row['output_id']}:{row_index}",
    )
    adapter_decision_id = f"{offline_primitive_id}:adapter_decision"
    if duplicate_offline_primitive_id:
        adapter_decision_id = (
            f"{offline_primitive_id}:duplicate:{row_index}:adapter_decision"
        )
    return {
        "adapter_decision_id": adapter_decision_id,
        "source_output_id": output_row["output_id"],
        "evidence_case_id": output_row["evidence_case_id"],
        "offline_primitive_id": offline_primitive_id,
        "paper_primitive": primitive_record.get("paper_primitive"),
        "offline_runtime_kind_label": primitive_record.get("newton_runtime_kind"),
        "record_field_status": field_status,
        "postprocess_state": output_row["postprocess_state"],
        "adapter_decision": decision,
        "adapter_decision_reason": reason,
        "required_later_gate": later_gate,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_package_adapter_contract_payload(
    changed_payload: dict[str, object],
) -> dict[str, object]:
    flat_records = [
        (output_row, primitive_record)
        for output_row in changed_payload["decomposition_output_rows"]
        for primitive_record in output_row["primitive_records"]
    ]
    offline_id_counts: dict[object, int] = {}
    for _, primitive_record in flat_records:
        offline_primitive_id = primitive_record.get("offline_primitive_id")
        if offline_primitive_id is not None:
            offline_id_counts[offline_primitive_id] = (
                offline_id_counts.get(offline_primitive_id, 0) + 1
            )
    duplicate_offline_ids = {
        offline_primitive_id
        for offline_primitive_id, count in offline_id_counts.items()
        if count > 1
    }
    rows = [
        _paper_adapter_primitive_decision_row(
            output_row,
            primitive_record,
            row_index,
            primitive_record.get("offline_primitive_id") in duplicate_offline_ids,
        )
        for row_index, (output_row, primitive_record) in enumerate(flat_records)
    ]
    adapter_eligible_count = sum(
        row["adapter_decision"] == "adapter_eligible" for row in rows
    )
    blocked_count = sum(row["adapter_decision"] == "blocked" for row in rows)
    later_policy_count = sum(
        row["adapter_decision"] == "later_policy_required" for row in rows
    )
    offline_only_count = sum(
        row["offline_runtime_kind_label"] == "offline_only_unmapped" for row in rows
    )
    return {
        "gate_id": _PAPER_PACKAGE_ADAPTER_CONTRACT,
        "gate_status": "implemented_offline_adapter_contract_only_partial",
        "closed_gate": _PAPER_PACKAGE_ADAPTER_CONTRACT,
        "input_gate_id": _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
        "next_required_gate": _PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
        "decision": "remain_partial",
        "decision_reason": (
            "package_adapter_contract_complete_unsupported_primitive_policy_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": "offline_package_adapter_contract_not_collision_package",
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_adapter_contract_no_collision_package_no_newton"
        ),
        "input_contract_summary": {
            "input_gate_id": changed_payload["gate_id"],
            "input_artifact_kind": changed_payload["artifact_kind"],
            "decomposition_output_row_count": changed_payload["coverage_summary"][
                "decomposition_output_row_count"
            ],
            "primitive_record_count": changed_payload["coverage_summary"][
                "primitive_record_count"
            ],
            "postprocess_state_row_count": changed_payload["coverage_summary"][
                "postprocess_state_row_count"
            ],
        },
        "adapter_decision_contract": {
            "decision_values": [
                "adapter_eligible",
                "blocked",
                "later_policy_required",
            ],
            "current_direct_adapter_policy": (
                "none_for_current_changed_decomposition_rows"
            ),
            "unsupported_primitive_policy_required": True,
            "package_generation_allowed": False,
        },
        "primitive_adapter_decision_rows": rows,
        "coverage_summary": {
            "decomposition_output_row_count": changed_payload["coverage_summary"][
                "decomposition_output_row_count"
            ],
            "primitive_decision_row_count": len(rows),
            "adapter_eligible_record_count": adapter_eligible_count,
            "blocked_record_count": blocked_count,
            "later_policy_required_record_count": later_policy_count,
            "offline_only_unmapped_record_count": offline_only_count,
        },
        "remaining_gaps": _paper_remaining_gaps_after_package_adapter_contract(),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_policy_distribution(
    rows: list[dict[str, object]],
    key: str,
) -> dict[str, int]:
    distribution: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key))
        distribution[value] = distribution.get(value, 0) + 1
    return distribution


def _paper_primitive_family_policy_rows(
    adapter_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    current_primitive_counts = _paper_policy_distribution(
        adapter_rows,
        "paper_primitive",
    )
    native_runtime_kinds = {
        "oriented_bounding_box": "box",
        "sphere": "sphere",
        "capsule": "capsule",
    }
    rows: list[dict[str, object]] = []
    for primitive_name in _AUDITED_PAPER_PRIMITIVES:
        newton_runtime_kind = native_runtime_kinds.get(
            primitive_name,
            "offline_only_unmapped",
        )
        direct_candidate = primitive_name in native_runtime_kinds
        rows.append(
            {
                "policy_row_id": f"{primitive_name}:unsupported_primitive_policy",
                "paper_primitive": primitive_name,
                "paper_family_status": (
                    "direct_newton_native_candidate"
                    if direct_candidate
                    else "offline_only_unmapped"
                ),
                "paper_fit_audit_available": True,
                "adapter_policy": (
                    "candidate_for_mapped_subset_plan"
                    if direct_candidate
                    else (
                        "keep_offline_until_explicit_mapping_or_"
                        "approximation_policy"
                    )
                ),
                "newton_runtime_kind": newton_runtime_kind,
                "direct_adapter_allowed_after_mapped_subset_plan": direct_candidate,
                "package_conversion_enabled_by_this_gate": False,
                "requires_explicit_mapping_or_approximation_policy": (
                    not direct_candidate
                ),
                "fallback_generation_allowed": False,
                "drop_allowed": False,
                "current_row_evidence_count": current_primitive_counts.get(
                    primitive_name,
                    0,
                ),
                "claim_boundary": (
                    "family_policy_only_not_package_conversion_or_newton_runtime"
                ),
                "package_generation_triggered": False,
                "newton_runtime_triggered": False,
                "real_usd_triggered": False,
                "benchmark_triggered": False,
            }
        )
    return rows


def _paper_current_adapter_policy_row(
    adapter_row: dict[str, object],
) -> dict[str, object]:
    runtime_kind = adapter_row["offline_runtime_kind_label"]
    adapter_decision = adapter_row["adapter_decision"]
    if adapter_decision == "adapter_eligible" and runtime_kind != "offline_only_unmapped":
        policy_decision = "candidate_for_mapped_subset_plan"
        adapter_action = "defer_to_mapped_subset_plan"
        reason = "native_runtime_kind_requires_mapped_subset_plan_before_package"
        package_candidate_status = "not_package_candidate_mapped_subset_plan_missing"
    elif adapter_decision == "blocked":
        policy_decision = "preserve_adapter_contract_block"
        adapter_action = "keep_offline"
        reason = "adapter_contract_already_blocked_record"
        package_candidate_status = "not_package_candidate_adapter_contract_block"
    else:
        policy_decision = "block_package_conversion"
        adapter_action = "keep_offline"
        reason = "offline_only_unmapped_paper_primitive_requires_explicit_policy"
        package_candidate_status = "not_package_candidate_unsupported_policy_block"

    return {
        "policy_decision_id": (
            f"{adapter_row['adapter_decision_id']}:unsupported_policy"
        ),
        "source_adapter_decision_id": adapter_row["adapter_decision_id"],
        "source_output_id": adapter_row["source_output_id"],
        "evidence_case_id": adapter_row["evidence_case_id"],
        "offline_primitive_id": adapter_row["offline_primitive_id"],
        "paper_primitive": adapter_row["paper_primitive"],
        "offline_runtime_kind_label": runtime_kind,
        "input_adapter_decision": adapter_decision,
        "unsupported_policy_decision": policy_decision,
        "adapter_action": adapter_action,
        "unsupported_policy_reason": reason,
        "package_candidate_status": package_candidate_status,
        "required_later_gate": _PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
        "required_future_policy": (
            "mapped_subset_conversion_plan_before_any_package_generation"
        ),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_package_adapter_unsupported_primitive_policy_payload(
    adapter_payload: dict[str, object],
) -> dict[str, object]:
    adapter_rows = adapter_payload["primitive_adapter_decision_rows"]
    family_rows = _paper_primitive_family_policy_rows(adapter_rows)
    policy_rows = [
        _paper_current_adapter_policy_row(adapter_row)
        for adapter_row in adapter_rows
    ]
    direct_policy_eligible_count = sum(
        row["unsupported_policy_decision"] == "candidate_for_mapped_subset_plan"
        for row in policy_rows
    )
    unsupported_policy_blocked_count = sum(
        row["unsupported_policy_decision"] == "block_package_conversion"
        for row in policy_rows
    )
    adapter_contract_blocked_count = sum(
        row["unsupported_policy_decision"] == "preserve_adapter_contract_block"
        for row in policy_rows
    )
    dropped_count = sum(row["adapter_action"] == "drop" for row in policy_rows)
    package_candidate_count = sum(
        row["package_candidate_status"] == "package_candidate"
        for row in policy_rows
    )
    remaining_gaps = _paper_remaining_gaps_after_unsupported_primitive_policy()
    return {
        "gate_id": _PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
        "gate_status": (
            "implemented_offline_unsupported_primitive_policy_only_partial"
        ),
        "closed_gate": _PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
        "input_gate_id": _PAPER_PACKAGE_ADAPTER_CONTRACT,
        "next_required_gate": _PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
        "decision": "remain_partial",
        "decision_reason": (
            "unsupported_primitive_policy_complete_mapped_subset_plan_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": "offline_unsupported_primitive_policy_not_collision_package",
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_unsupported_primitive_policy_no_collision_package_no_newton"
        ),
        "input_contract_summary": {
            "input_gate_id": adapter_payload["gate_id"],
            "input_artifact_kind": adapter_payload["artifact_kind"],
            "primitive_decision_row_count": adapter_payload["coverage_summary"][
                "primitive_decision_row_count"
            ],
            "later_policy_required_record_count": adapter_payload[
                "coverage_summary"
            ]["later_policy_required_record_count"],
            "offline_only_unmapped_record_count": adapter_payload[
                "coverage_summary"
            ]["offline_only_unmapped_record_count"],
        },
        "unsupported_policy_contract": {
            "decision_values": [
                "candidate_for_mapped_subset_plan",
                "block_package_conversion",
                "preserve_adapter_contract_block",
            ],
            "current_unmapped_record_policy": "keep_offline",
            "package_generation_allowed": False,
            "approximation_policy_enabled": False,
            "silent_drop_allowed": False,
            "next_gate_for_native_candidates": (
                _PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN
            ),
        },
        "paper_primitive_family_policy_rows": family_rows,
        "current_adapter_decision_policy_rows": policy_rows,
        "coverage_summary": {
            "decomposition_output_row_count": adapter_payload[
                "coverage_summary"
            ]["decomposition_output_row_count"],
            "primitive_decision_row_count": adapter_payload["coverage_summary"][
                "primitive_decision_row_count"
            ],
            "paper_primitive_family_policy_row_count": len(family_rows),
            "current_adapter_decision_policy_row_count": len(policy_rows),
            "direct_policy_eligible_record_count": direct_policy_eligible_count,
            "unsupported_policy_blocked_record_count": (
                unsupported_policy_blocked_count
            ),
            "adapter_contract_blocked_record_count": adapter_contract_blocked_count,
            "dropped_record_count": dropped_count,
            "package_candidate_record_count": package_candidate_count,
            "current_paper_primitive_distribution": _paper_policy_distribution(
                policy_rows,
                "paper_primitive",
            ),
            "current_runtime_kind_distribution": _paper_policy_distribution(
                policy_rows,
                "offline_runtime_kind_label",
            ),
        },
        "remaining_gaps": remaining_gaps,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_family_conversion_plan_row(
    family_row: dict[str, object],
) -> dict[str, object]:
    paper_primitive = str(family_row["paper_primitive"])
    direct_candidate = (
        family_row["adapter_policy"] == "candidate_for_mapped_subset_plan"
    )
    current_count = int(family_row["current_row_evidence_count"])
    if direct_candidate:
        conversion_decision = "plan_direct_native_mapping_later"
        package_candidate_status = (
            "future_candidate_family_no_current_rows"
            if current_count == 0
            else "future_candidate_family_with_current_rows"
        )
        planned_runtime_kind = family_row["newton_runtime_kind"]
    else:
        conversion_decision = (
            "exclude_requires_explicit_mapping_or_approximation_policy"
        )
        package_candidate_status = (
            "not_package_candidate_unsupported_policy_block"
        )
        planned_runtime_kind = "offline_only_unmapped"

    return {
        "conversion_plan_row_id": f"{paper_primitive}:mapped_subset_family_plan",
        "source_policy_row_id": family_row["policy_row_id"],
        "paper_primitive": paper_primitive,
        "input_adapter_policy": family_row["adapter_policy"],
        "conversion_plan_decision": conversion_decision,
        "planned_runtime_kind": planned_runtime_kind,
        "package_candidate_status": package_candidate_status,
        "current_row_evidence_count": current_count,
        "package_conversion_enabled_by_this_gate": False,
        "requires_explicit_mapping_or_approximation_policy": (
            not direct_candidate
        ),
        "claim_boundary": "family_plan_only_not_package_conversion_or_newton_runtime",
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_current_row_conversion_plan_row(
    policy_row: dict[str, object],
) -> dict[str, object]:
    input_policy_decision = policy_row["unsupported_policy_decision"]
    runtime_kind = policy_row["offline_runtime_kind_label"]
    if input_policy_decision == "candidate_for_mapped_subset_plan":
        conversion_decision = "plan_direct_native_mapping_later"
        action = "defer_to_candidate_matrix"
        status = "future_candidate_row_no_package_conversion"
        package_conversion_candidate = False
    elif input_policy_decision == "preserve_adapter_contract_block":
        conversion_decision = "exclude_adapter_contract_block"
        action = "keep_offline"
        status = "not_package_candidate_adapter_contract_block"
        package_conversion_candidate = False
    else:
        conversion_decision = (
            "exclude_requires_explicit_mapping_or_approximation_policy"
        )
        action = "keep_offline"
        status = "not_package_candidate_unsupported_policy_block"
        package_conversion_candidate = False

    return {
        "conversion_plan_row_id": (
            f"{policy_row['policy_decision_id']}:mapped_subset_plan"
        ),
        "source_policy_decision_id": policy_row["policy_decision_id"],
        "source_adapter_decision_id": policy_row["source_adapter_decision_id"],
        "source_output_id": policy_row["source_output_id"],
        "evidence_case_id": policy_row["evidence_case_id"],
        "offline_primitive_id": policy_row["offline_primitive_id"],
        "paper_primitive": policy_row["paper_primitive"],
        "offline_runtime_kind_label": runtime_kind,
        "input_unsupported_policy_decision": input_policy_decision,
        "conversion_plan_decision": conversion_decision,
        "conversion_plan_action": action,
        "package_conversion_candidate": package_conversion_candidate,
        "package_candidate_status": status,
        "required_later_gate": _PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
        "required_future_policy": (
            "candidate_matrix_before_any_package_conversion_contract"
        ),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_package_conversion_mapped_subset_plan_payload(
    unsupported_payload: dict[str, object],
) -> dict[str, object]:
    family_rows = [
        _paper_family_conversion_plan_row(row)
        for row in unsupported_payload["paper_primitive_family_policy_rows"]
    ]
    current_rows = [
        _paper_current_row_conversion_plan_row(row)
        for row in unsupported_payload["current_adapter_decision_policy_rows"]
    ]
    direct_current_candidate_count = sum(
        row["conversion_plan_decision"] == "plan_direct_native_mapping_later"
        for row in current_rows
    )
    future_candidate_family_no_current_count = sum(
        row["conversion_plan_decision"] == "plan_direct_native_mapping_later"
        and row["current_row_evidence_count"] == 0
        for row in family_rows
    )
    excluded_requires_policy_count = sum(
        row["conversion_plan_decision"]
        == "exclude_requires_explicit_mapping_or_approximation_policy"
        for row in current_rows
    )
    adapter_contract_blocked_count = sum(
        row["conversion_plan_decision"] == "exclude_adapter_contract_block"
        for row in current_rows
    )
    package_candidate_count = sum(
        bool(row["package_conversion_candidate"]) for row in current_rows
    )
    dropped_count = sum(
        row["conversion_plan_action"] == "drop" for row in current_rows
    )
    remaining_gaps = _paper_remaining_gaps_after_conversion_mapped_subset_plan()
    return {
        "gate_id": _PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
        "gate_status": "implemented_offline_mapped_subset_plan_only_partial",
        "closed_gate": _PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
        "input_gate_id": _PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
        "next_required_gate": _PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
        "decision": "remain_partial",
        "decision_reason": "mapped_subset_plan_complete_candidate_matrix_missing",
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": "offline_mapped_subset_plan_not_collision_package",
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_conversion_plan_no_collision_package_no_primitivespec_no_newton"
        ),
        "input_contract_summary": {
            "input_gate_id": unsupported_payload["gate_id"],
            "input_artifact_kind": unsupported_payload["artifact_kind"],
            "paper_primitive_family_policy_row_count": unsupported_payload[
                "coverage_summary"
            ]["paper_primitive_family_policy_row_count"],
            "current_adapter_decision_policy_row_count": unsupported_payload[
                "coverage_summary"
            ]["current_adapter_decision_policy_row_count"],
            "unsupported_policy_blocked_record_count": unsupported_payload[
                "coverage_summary"
            ]["unsupported_policy_blocked_record_count"],
            "package_candidate_record_count": unsupported_payload[
                "coverage_summary"
            ]["package_candidate_record_count"],
        },
        "mapped_subset_plan_contract": {
            "decision_values": [
                "plan_direct_native_mapping_later",
                "exclude_requires_explicit_mapping_or_approximation_policy",
                "exclude_adapter_contract_block",
            ],
            "package_candidate_status_values": [
                "future_candidate_family_no_current_rows",
                "future_candidate_family_with_current_rows",
                "future_candidate_row_no_package_conversion",
                "not_package_candidate_unsupported_policy_block",
                "not_package_candidate_adapter_contract_block",
            ],
            "package_generation_allowed": False,
            "primitive_spec_generation_allowed": False,
            "collision_package_generation_allowed": False,
            "newton_runtime_allowed": False,
            "runtime_admissibility_supported": False,
            "approximation_policy_enabled": False,
            "silent_drop_allowed": False,
        },
        "paper_primitive_family_conversion_plan_rows": family_rows,
        "current_row_conversion_plan_rows": current_rows,
        "coverage_summary": {
            "decomposition_output_row_count": unsupported_payload[
                "coverage_summary"
            ]["decomposition_output_row_count"],
            "primitive_decision_row_count": unsupported_payload[
                "coverage_summary"
            ]["primitive_decision_row_count"],
            "paper_primitive_family_conversion_plan_row_count": len(family_rows),
            "current_row_conversion_plan_row_count": len(current_rows),
            "direct_mapped_current_candidate_record_count": (
                direct_current_candidate_count
            ),
            "future_candidate_family_without_current_rows_count": (
                future_candidate_family_no_current_count
            ),
            "excluded_requires_policy_record_count": excluded_requires_policy_count,
            "adapter_contract_blocked_record_count": adapter_contract_blocked_count,
            "package_candidate_record_count": package_candidate_count,
            "dropped_record_count": dropped_count,
            "current_paper_primitive_distribution": _paper_policy_distribution(
                current_rows,
                "paper_primitive",
            ),
            "current_runtime_kind_distribution": _paper_policy_distribution(
                current_rows,
                "offline_runtime_kind_label",
            ),
        },
        "remaining_gaps": remaining_gaps,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_future_family_candidate_matrix_row(
    family_row: dict[str, object],
) -> dict[str, object]:
    paper_primitive = str(family_row["paper_primitive"])
    input_decision = str(family_row["conversion_plan_decision"])
    runtime_kind = str(family_row["planned_runtime_kind"])
    current_count = int(family_row["current_row_evidence_count"])
    if input_decision == "plan_direct_native_mapping_later":
        decision = "native_family_review_only"
        future_candidate = True
        status = "future_family_review_candidate_no_current_rows"
    elif paper_primitive == "trapezoidal_prism" and current_count:
        decision = "blocked_unmapped_current_rows"
        future_candidate = False
        status = "not_current_candidate_unsupported_policy_block"
    else:
        decision = "blocked_approximation_policy_missing"
        future_candidate = False
        status = "not_current_candidate_mapping_or_approximation_missing"

    return {
        "candidate_matrix_row_id": (
            f"{family_row['conversion_plan_row_id']}:candidate_matrix"
        ),
        "source_conversion_plan_row_id": family_row["conversion_plan_row_id"],
        "paper_primitive": paper_primitive,
        "input_conversion_plan_decision": input_decision,
        "candidate_matrix_decision": decision,
        "candidate_runtime_kind": runtime_kind,
        "future_family_review_candidate": future_candidate,
        "current_row_evidence_count": current_count,
        "current_package_conversion_candidate_count": 0,
        "package_candidate_status": status,
        "package_conversion_enabled_by_this_gate": False,
        "claim_boundary": "review_row_not_package_ready",
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_current_row_candidate_matrix_row(
    current_row: dict[str, object],
) -> dict[str, object]:
    input_decision = str(current_row["conversion_plan_decision"])
    if input_decision == "plan_direct_native_mapping_later":
        decision = "blocked_until_later_adapter_preflight_contract"
        status = "future_current_row_review_only_no_package_conversion"
        future_policy = "adapter_preflight_contract_before_package_generation"
    elif input_decision == "exclude_adapter_contract_block":
        decision = "blocked_adapter_contract_boundary"
        status = "not_current_candidate_adapter_contract_block"
        future_policy = "adapter_contract_cleanup_before_package_generation"
    else:
        decision = "blocked_unmapped_current_rows"
        status = "not_current_candidate_unsupported_policy_block"
        future_policy = (
            "explicit_mapping_or_approximation_policy_before_package_generation"
        )

    return {
        "candidate_matrix_row_id": (
            f"{current_row['conversion_plan_row_id']}:candidate_matrix"
        ),
        "source_conversion_plan_row_id": current_row["conversion_plan_row_id"],
        "source_policy_decision_id": current_row["source_policy_decision_id"],
        "source_adapter_decision_id": current_row["source_adapter_decision_id"],
        "source_output_id": current_row["source_output_id"],
        "evidence_case_id": current_row["evidence_case_id"],
        "offline_primitive_id": current_row["offline_primitive_id"],
        "paper_primitive": current_row["paper_primitive"],
        "offline_runtime_kind_label": current_row["offline_runtime_kind_label"],
        "input_conversion_plan_decision": input_decision,
        "candidate_matrix_decision": decision,
        "candidate_matrix_action": "keep_offline",
        "current_package_conversion_candidate": False,
        "package_candidate_status": status,
        "required_later_gate": _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        "required_future_policy": future_policy,
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_mapped_subset_conversion_candidate_matrix_payload(
    mapped_subset_plan: dict[str, object],
) -> dict[str, object]:
    future_family_rows = [
        _paper_future_family_candidate_matrix_row(row)
        for row in mapped_subset_plan["paper_primitive_family_conversion_plan_rows"]
    ]
    current_rows = [
        _paper_current_row_candidate_matrix_row(row)
        for row in mapped_subset_plan["current_row_conversion_plan_rows"]
    ]
    future_family_candidate_count = sum(
        bool(row["future_family_review_candidate"]) for row in future_family_rows
    )
    excluded_family_count = len(future_family_rows) - future_family_candidate_count
    current_package_candidate_count = sum(
        bool(row["current_package_conversion_candidate"]) for row in current_rows
    )
    current_blocked_requires_policy_count = sum(
        row["candidate_matrix_decision"] == "blocked_unmapped_current_rows"
        for row in current_rows
    )
    remaining_gaps = _paper_remaining_gaps_after_mapped_subset_candidate_matrix()
    return {
        "gate_id": _PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
        "gate_status": "implemented_offline_candidate_matrix_only_partial",
        "closed_gate": _PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
        "input_gate_id": _PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
        "next_required_gate": _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        "decision": "remain_partial",
        "decision_reason": (
            "candidate_matrix_complete_adapter_preflight_contract_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": "offline_mapped_subset_candidate_matrix_not_collision_package",
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_candidate_matrix_no_primitivespec_no_collision_package_no_newton"
        ),
        "input_contract_summary": {
            "input_gate_id": mapped_subset_plan["gate_id"],
            "input_artifact_kind": mapped_subset_plan["artifact_kind"],
            "paper_primitive_family_conversion_plan_row_count": (
                mapped_subset_plan["coverage_summary"][
                    "paper_primitive_family_conversion_plan_row_count"
                ]
            ),
            "current_row_conversion_plan_row_count": mapped_subset_plan[
                "coverage_summary"
            ]["current_row_conversion_plan_row_count"],
            "direct_mapped_current_candidate_record_count": mapped_subset_plan[
                "coverage_summary"
            ]["direct_mapped_current_candidate_record_count"],
            "package_candidate_record_count": mapped_subset_plan["coverage_summary"][
                "package_candidate_record_count"
            ],
        },
        "candidate_matrix_contract": {
            "decision_values": [
                "native_family_review_only",
                "blocked_approximation_policy_missing",
                "blocked_unmapped_current_rows",
                "blocked_adapter_contract_boundary",
                "blocked_until_later_adapter_preflight_contract",
            ],
            "package_candidate_status_values": [
                "future_family_review_candidate_no_current_rows",
                "future_current_row_review_only_no_package_conversion",
                "not_current_candidate_mapping_or_approximation_missing",
                "not_current_candidate_unsupported_policy_block",
                "not_current_candidate_adapter_contract_block",
            ],
            "package_generation_allowed": False,
            "primitive_spec_generation_allowed": False,
            "collision_package_generation_allowed": False,
            "newton_runtime_allowed": False,
            "runtime_admissibility_supported": False,
            "approximation_policy_enabled": False,
            "silent_drop_allowed": False,
        },
        "future_family_candidate_matrix_rows": future_family_rows,
        "current_row_candidate_matrix_rows": current_rows,
        "coverage_summary": {
            "future_family_candidate_matrix_row_count": len(future_family_rows),
            "future_family_review_candidate_count": future_family_candidate_count,
            "excluded_family_review_row_count": excluded_family_count,
            "current_row_candidate_matrix_row_count": len(current_rows),
            "current_package_conversion_candidate_count": (
                current_package_candidate_count
            ),
            "current_blocked_requires_policy_count": (
                current_blocked_requires_policy_count
            ),
            "package_candidate_record_count": current_package_candidate_count,
            "current_paper_primitive_distribution": _paper_policy_distribution(
                current_rows,
                "paper_primitive",
            ),
            "current_runtime_kind_distribution": _paper_policy_distribution(
                current_rows,
                "offline_runtime_kind_label",
            ),
        },
        "remaining_gaps": remaining_gaps,
        "primitive_spec_generated": False,
        "collision_package_generated": False,
        "runtime_admissibility_checked": False,
        "newton_support_claimed": False,
        "approximation_policy_applied": False,
        "real_usd_loaded": False,
        "benchmark_run": False,
        "collision_quality_measured": False,
        "deployment_or_certification_claimed": False,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_adapter_preflight_family_requirement_row(
    family_row: dict[str, object],
) -> dict[str, object]:
    input_decision = str(family_row["candidate_matrix_decision"])
    if input_decision == "native_family_review_only":
        decision = "future_native_family_preflight_recorded_only"
        future_native_recorded = True
    elif input_decision == "blocked_approximation_policy_missing":
        decision = "blocked_approximation_policy_missing"
        future_native_recorded = False
    elif input_decision == "blocked_unmapped_current_rows":
        decision = "noop_current_unmapped_rows_keep_offline"
        future_native_recorded = False
    else:
        raise ValueError(
            f"unknown_family_candidate_matrix_decision:{input_decision}"
        )

    return {
        "adapter_preflight_row_id": (
            f"{family_row['candidate_matrix_row_id']}:adapter_preflight"
        ),
        "source_candidate_matrix_row_id": family_row["candidate_matrix_row_id"],
        "source_conversion_plan_row_id": family_row[
            "source_conversion_plan_row_id"
        ],
        "paper_primitive": family_row["paper_primitive"],
        "candidate_runtime_kind": family_row["candidate_runtime_kind"],
        "input_candidate_matrix_decision": input_decision,
        "adapter_preflight_decision": decision,
        "future_native_family_preflight_recorded": future_native_recorded,
        "current_row_evidence_count": family_row["current_row_evidence_count"],
        "current_package_conversion_candidate_count": family_row[
            "current_package_conversion_candidate_count"
        ],
        "package_generation_enabled_by_this_gate": False,
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_adapter_preflight_current_row(
    current_row: dict[str, object],
) -> dict[str, object]:
    return {
        "adapter_preflight_row_id": (
            f"{current_row['candidate_matrix_row_id']}:adapter_preflight"
        ),
        "source_candidate_matrix_row_id": current_row["candidate_matrix_row_id"],
        "source_conversion_plan_row_id": current_row[
            "source_conversion_plan_row_id"
        ],
        "source_policy_decision_id": current_row["source_policy_decision_id"],
        "source_adapter_decision_id": current_row["source_adapter_decision_id"],
        "source_output_id": current_row["source_output_id"],
        "evidence_case_id": current_row["evidence_case_id"],
        "offline_primitive_id": current_row["offline_primitive_id"],
        "paper_primitive": current_row["paper_primitive"],
        "offline_runtime_kind_label": current_row["offline_runtime_kind_label"],
        "input_candidate_matrix_decision": current_row["candidate_matrix_decision"],
        "adapter_preflight_decision": "noop_keep_offline_unmapped_current_row",
        "adapter_preflight_action": "keep_offline",
        "current_package_conversion_candidate": False,
        "adapter_preflight_passed": False,
        "package_generation_enabled_by_this_gate": False,
        "required_later_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
        "required_future_policy": current_row["required_future_policy"],
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_validate_adapter_preflight_candidate_matrix(
    candidate_matrix: dict[str, object],
) -> None:
    if (
        candidate_matrix.get("gate_id")
        != _PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
    ):
        raise ValueError("candidate_matrix_gate_id_mismatch")

    coverage_summary = candidate_matrix["coverage_summary"]
    if coverage_summary["current_package_conversion_candidate_count"] != 0:
        raise ValueError("input_package_candidate_count_nonzero")
    if coverage_summary["package_candidate_record_count"] != 0:
        raise ValueError("input_package_candidate_count_nonzero")

    trigger_flags = (
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
    )
    for flag in trigger_flags:
        if bool(candidate_matrix.get(flag)):
            raise ValueError(f"input_trigger_flag_true:{flag}")

    row_ids: list[str] = []
    for row_group_name in (
        "future_family_candidate_matrix_rows",
        "current_row_candidate_matrix_rows",
    ):
        for row in candidate_matrix[row_group_name]:
            row_ids.append(str(row["candidate_matrix_row_id"]))
            if (
                row_group_name == "future_family_candidate_matrix_rows"
                and row["current_package_conversion_candidate_count"] != 0
            ):
                raise ValueError("input_package_candidate_count_nonzero")
            if (
                row_group_name == "current_row_candidate_matrix_rows"
                and bool(row["current_package_conversion_candidate"])
            ):
                raise ValueError("input_package_candidate_count_nonzero")
            for flag in (
                "primitive_spec_generation_triggered",
                "collision_package_generation_triggered",
                "runtime_admissibility_triggered",
                "newton_runtime_triggered",
                "real_usd_triggered",
                "benchmark_triggered",
            ):
                if bool(row.get(flag)):
                    raise ValueError(f"input_trigger_flag_true:{flag}")
    if len(row_ids) != len(set(row_ids)):
        raise ValueError("duplicate_candidate_matrix_row_id")


def _paper_mapped_subset_adapter_preflight_contract_payload(
    candidate_matrix: dict[str, object],
) -> dict[str, object]:
    _paper_validate_adapter_preflight_candidate_matrix(candidate_matrix)
    family_rows = [
        _paper_adapter_preflight_family_requirement_row(row)
        for row in candidate_matrix["future_family_candidate_matrix_rows"]
    ]
    current_rows = [
        _paper_adapter_preflight_current_row(row)
        for row in candidate_matrix["current_row_candidate_matrix_rows"]
    ]
    future_native_count = sum(
        bool(row["future_native_family_preflight_recorded"])
        for row in family_rows
    )
    blocked_family_count = len(family_rows) - future_native_count
    current_preflight_pass_count = sum(
        bool(row["adapter_preflight_passed"]) for row in current_rows
    )
    current_preflight_noop_count = sum(
        row["adapter_preflight_decision"]
        == "noop_keep_offline_unmapped_current_row"
        for row in current_rows
    )
    current_package_candidate_count = sum(
        bool(row["current_package_conversion_candidate"]) for row in current_rows
    )
    remaining_gaps = _paper_remaining_gaps_after_mapped_subset_adapter_preflight()
    return {
        "gate_id": _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        "gate_status": "implemented_offline_adapter_preflight_contract_only_partial",
        "closed_gate": _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        "input_gate_id": _PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
        "next_required_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
        "decision": "remain_partial",
        "decision_reason": (
            "adapter_preflight_contract_complete_"
            "primitivespec_dry_run_contract_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": (
            "offline_adapter_preflight_contract_not_primitivespec_"
            "not_collision_package"
        ),
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_adapter_preflight_no_primitivespec_no_collision_package_no_newton"
        ),
        "candidate_count_at_preflight": current_package_candidate_count,
        "preflight_action": "no_op_keep_offline",
        "primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "runtime_admissibility_supported": False,
        "newton_runtime_allowed": False,
        "approximation_policy_enabled": False,
        "silent_drop_allowed": False,
        "input_contract_summary": {
            "input_gate_id": candidate_matrix["gate_id"],
            "input_artifact_kind": candidate_matrix["artifact_kind"],
            "future_family_candidate_matrix_row_count": candidate_matrix[
                "coverage_summary"
            ]["future_family_candidate_matrix_row_count"],
            "current_row_candidate_matrix_row_count": candidate_matrix[
                "coverage_summary"
            ]["current_row_candidate_matrix_row_count"],
            "current_package_conversion_candidate_count": candidate_matrix[
                "coverage_summary"
            ]["current_package_conversion_candidate_count"],
            "package_candidate_record_count": candidate_matrix["coverage_summary"][
                "package_candidate_record_count"
            ],
        },
        "adapter_preflight_contract": {
            "candidate_matrix_required": True,
            "candidate_matrix_input_gate_required": (
                _PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX
            ),
            "unique_row_ids_required": True,
            "complete_source_evidence_ids_required": True,
            "zero_current_package_candidates_required": True,
            "no_silent_drop_required": True,
            "package_generation_allowed": False,
            "primitive_spec_generation_allowed": False,
            "collision_package_generation_allowed": False,
            "newton_runtime_allowed": False,
            "runtime_admissibility_supported": False,
            "approximation_policy_enabled": False,
            "silent_drop_allowed": False,
        },
        "adapter_preflight_requirement_rows": family_rows,
        "current_row_adapter_preflight_rows": current_rows,
        "coverage_summary": {
            "family_preflight_requirement_row_count": len(family_rows),
            "future_native_family_preflight_record_count": future_native_count,
            "blocked_family_preflight_record_count": blocked_family_count,
            "current_row_adapter_preflight_row_count": len(current_rows),
            "current_preflight_pass_record_count": current_preflight_pass_count,
            "current_preflight_noop_record_count": current_preflight_noop_count,
            "current_package_conversion_candidate_count": (
                current_package_candidate_count
            ),
            "package_candidate_record_count": current_package_candidate_count,
            "current_paper_primitive_distribution": _paper_policy_distribution(
                current_rows,
                "paper_primitive",
            ),
            "current_runtime_kind_distribution": _paper_policy_distribution(
                current_rows,
                "offline_runtime_kind_label",
            ),
        },
        "remaining_gaps": remaining_gaps,
        "generated_primitive_spec_count": 0,
        "generated_collision_package_count": 0,
        "runtime_admissibility_check_count": 0,
        "primitive_spec_generated": False,
        "collision_package_generated": False,
        "runtime_admissibility_checked": False,
        "newton_support_claimed": False,
        "approximation_policy_applied": False,
        "real_usd_loaded": False,
        "benchmark_run": False,
        "collision_quality_measured": False,
        "deployment_or_certification_claimed": False,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


_PRIMITIVESPEC_DRY_RUN_REQUIRED_FIELDS = [
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


def _paper_primitivespec_dry_run_requirement_row(
    family_row: dict[str, object],
) -> dict[str, object]:
    input_decision = str(family_row["adapter_preflight_decision"])
    if input_decision == "future_native_family_preflight_recorded_only":
        decision = "future_native_family_primitivespec_shape_recorded_only"
        future_shape_recorded = True
        future_primitive_spec_kind = family_row["candidate_runtime_kind"]
    elif input_decision == "blocked_approximation_policy_missing":
        decision = "blocked_approximation_policy_missing"
        future_shape_recorded = False
        future_primitive_spec_kind = None
    elif input_decision == "noop_current_unmapped_rows_keep_offline":
        decision = "noop_current_unmapped_rows_keep_offline"
        future_shape_recorded = False
        future_primitive_spec_kind = None
    else:
        raise ValueError(
            f"unknown_adapter_preflight_family_decision:{input_decision}"
        )

    return {
        "primitive_spec_dry_run_row_id": (
            f"{family_row['adapter_preflight_row_id']}:primitivespec_dry_run"
        ),
        "source_adapter_preflight_row_id": family_row["adapter_preflight_row_id"],
        "source_candidate_matrix_row_id": family_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": family_row[
            "source_conversion_plan_row_id"
        ],
        "paper_primitive": family_row["paper_primitive"],
        "candidate_runtime_kind": family_row["candidate_runtime_kind"],
        "future_primitive_spec_kind": future_primitive_spec_kind,
        "input_adapter_preflight_decision": input_decision,
        "primitive_spec_dry_run_decision": decision,
        "future_primitive_spec_shape_recorded": future_shape_recorded,
        "current_row_evidence_count": family_row["current_row_evidence_count"],
        "current_package_conversion_candidate_count": family_row[
            "current_package_conversion_candidate_count"
        ],
        "required_primitive_spec_fields": list(
            _PRIMITIVESPEC_DRY_RUN_REQUIRED_FIELDS
        ),
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_primitivespec_dry_run_current_row(
    current_row: dict[str, object],
) -> dict[str, object]:
    input_decision = str(current_row["adapter_preflight_decision"])
    if input_decision != "noop_keep_offline_unmapped_current_row":
        raise ValueError(
            f"unknown_adapter_preflight_current_decision:{input_decision}"
        )

    return {
        "primitive_spec_dry_run_row_id": (
            f"{current_row['adapter_preflight_row_id']}:primitivespec_dry_run"
        ),
        "source_adapter_preflight_row_id": current_row["adapter_preflight_row_id"],
        "source_candidate_matrix_row_id": current_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": current_row[
            "source_conversion_plan_row_id"
        ],
        "source_policy_decision_id": current_row["source_policy_decision_id"],
        "source_adapter_decision_id": current_row["source_adapter_decision_id"],
        "source_output_id": current_row["source_output_id"],
        "evidence_case_id": current_row["evidence_case_id"],
        "offline_primitive_id": current_row["offline_primitive_id"],
        "paper_primitive": current_row["paper_primitive"],
        "offline_runtime_kind_label": current_row["offline_runtime_kind_label"],
        "input_adapter_preflight_decision": input_decision,
        "primitive_spec_dry_run_decision": "skip_unmapped_current_row",
        "primitive_spec_dry_run_action": "keep_offline",
        "primitive_spec_dry_run_passed": False,
        "primitive_spec_candidate": False,
        "generated_primitive_spec": None,
        "required_later_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
        "required_future_policy": current_row["required_future_policy"],
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_validate_primitivespec_dry_run_preflight(
    preflight: dict[str, object],
) -> None:
    if preflight.get("gate_id") != _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT:
        raise ValueError("primitivespec_dry_run_input_gate_id_mismatch")

    trigger_flags = (
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
    )
    for flag in trigger_flags:
        if bool(preflight.get(flag)):
            raise ValueError(f"input_trigger_flag_true:{flag}")

    if preflight["candidate_count_at_preflight"] != 0:
        raise ValueError("input_primitivespec_candidate_count_nonzero")
    if preflight["generated_primitive_spec_count"] != 0:
        raise ValueError("input_primitivespec_candidate_count_nonzero")
    if preflight["generated_collision_package_count"] != 0:
        raise ValueError("input_primitivespec_candidate_count_nonzero")
    if preflight["runtime_admissibility_check_count"] != 0:
        raise ValueError("input_trigger_flag_true:runtime_admissibility_check_count")

    coverage_summary = preflight["coverage_summary"]
    if coverage_summary["current_preflight_pass_record_count"] != 0:
        raise ValueError("input_preflight_pass_count_nonzero")
    if coverage_summary["current_package_conversion_candidate_count"] != 0:
        raise ValueError("input_primitivespec_candidate_count_nonzero")
    if coverage_summary["package_candidate_record_count"] != 0:
        raise ValueError("input_primitivespec_candidate_count_nonzero")

    row_ids: list[str] = []
    for family_row in preflight["adapter_preflight_requirement_rows"]:
        _paper_require_nonempty_source_id(
            family_row,
            "adapter_preflight_row_id",
            "missing_adapter_preflight_row_id",
        )
        row_ids.append(str(family_row["adapter_preflight_row_id"]))
        if family_row["current_package_conversion_candidate_count"] != 0:
            raise ValueError("input_primitivespec_candidate_count_nonzero")
        _paper_validate_primitivespec_dry_run_row_false_flags(family_row)

    required_current_fields = (
        "source_candidate_matrix_row_id",
        "source_conversion_plan_row_id",
        "source_policy_decision_id",
        "source_adapter_decision_id",
        "source_output_id",
        "evidence_case_id",
        "offline_primitive_id",
    )
    for current_row in preflight["current_row_adapter_preflight_rows"]:
        _paper_require_nonempty_source_id(
            current_row,
            "adapter_preflight_row_id",
            "missing_adapter_preflight_row_id",
        )
        row_ids.append(str(current_row["adapter_preflight_row_id"]))
        for field_name in required_current_fields:
            _paper_require_nonempty_source_id(
                current_row,
                field_name,
                "missing_current_row_source_id",
            )
        if bool(current_row["adapter_preflight_passed"]):
            raise ValueError("input_preflight_pass_count_nonzero")
        if bool(current_row["current_package_conversion_candidate"]):
            raise ValueError("input_primitivespec_candidate_count_nonzero")
        if (
            current_row["required_later_gate"]
            != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
        ):
            raise ValueError("current_row_required_later_gate_mismatch")
        _paper_validate_primitivespec_dry_run_row_false_flags(current_row)

    if len(row_ids) != len(set(row_ids)):
        raise ValueError("duplicate_adapter_preflight_row_id")


def _paper_mapped_subset_primitivespec_dry_run_contract_payload(
    preflight: dict[str, object],
) -> dict[str, object]:
    _paper_validate_primitivespec_dry_run_preflight(preflight)
    requirement_rows = [
        _paper_primitivespec_dry_run_requirement_row(row)
        for row in preflight["adapter_preflight_requirement_rows"]
    ]
    current_rows = [
        _paper_primitivespec_dry_run_current_row(row)
        for row in preflight["current_row_adapter_preflight_rows"]
    ]
    future_shape_count = sum(
        bool(row["future_primitive_spec_shape_recorded"])
        for row in requirement_rows
    )
    blocked_requirement_count = sum(
        row["primitive_spec_dry_run_decision"]
        == "blocked_approximation_policy_missing"
        for row in requirement_rows
    )
    noop_requirement_count = sum(
        row["primitive_spec_dry_run_decision"]
        == "noop_current_unmapped_rows_keep_offline"
        for row in requirement_rows
    )
    current_pass_count = sum(
        bool(row["primitive_spec_dry_run_passed"]) for row in current_rows
    )
    current_noop_count = sum(
        row["primitive_spec_dry_run_decision"] == "skip_unmapped_current_row"
        for row in current_rows
    )
    candidate_count = sum(
        bool(row["primitive_spec_candidate"]) for row in current_rows
    )
    generated_count = sum(
        row["generated_primitive_spec"] is not None for row in current_rows
    )
    remaining_gaps = _paper_remaining_gaps_after_mapped_subset_primitivespec_dry_run()
    return {
        "gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
        "gate_status": "implemented_offline_primitivespec_dry_run_contract_only_partial",
        "closed_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
        "input_gate_id": _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
        "next_required_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
        "decision": "remain_partial",
        "decision_reason": (
            "primitivespec_dry_run_contract_complete_"
            "primitivespec_validation_contract_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": (
            "offline_primitivespec_dry_run_contract_not_primitivespec_"
            "not_collision_package"
        ),
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_primitivespec_dry_run_no_primitivespec_"
            "no_collision_package_no_newton"
        ),
        "candidate_count_at_dry_run": candidate_count,
        "dry_run_action": "no_op_keep_offline",
        "primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "runtime_admissibility_supported": False,
        "newton_runtime_allowed": False,
        "approximation_policy_enabled": False,
        "silent_drop_allowed": False,
        "input_contract_summary": {
            "input_gate_id": preflight["gate_id"],
            "input_artifact_kind": preflight["artifact_kind"],
            "family_preflight_requirement_row_count": preflight[
                "coverage_summary"
            ]["family_preflight_requirement_row_count"],
            "current_row_adapter_preflight_row_count": preflight[
                "coverage_summary"
            ]["current_row_adapter_preflight_row_count"],
            "current_preflight_pass_record_count": preflight[
                "coverage_summary"
            ]["current_preflight_pass_record_count"],
            "current_package_conversion_candidate_count": preflight[
                "coverage_summary"
            ]["current_package_conversion_candidate_count"],
            "package_candidate_record_count": preflight["coverage_summary"][
                "package_candidate_record_count"
            ],
        },
        "primitive_spec_dry_run_contract": {
            "adapter_preflight_required": True,
            "adapter_preflight_input_gate_required": (
                _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT
            ),
            "unique_row_ids_required": True,
            "complete_source_evidence_ids_required": True,
            "zero_current_package_candidates_required": True,
            "zero_current_preflight_passes_required": True,
            "allowed_future_runtime_kinds": ["box", "sphere", "capsule"],
            "required_primitive_spec_fields": list(
                _PRIMITIVESPEC_DRY_RUN_REQUIRED_FIELDS
            ),
            "primitive_spec_generation_allowed": False,
            "collision_package_generation_allowed": False,
            "newton_runtime_allowed": False,
            "runtime_admissibility_supported": False,
            "approximation_policy_enabled": False,
            "silent_drop_allowed": False,
        },
        "primitive_spec_dry_run_requirement_rows": requirement_rows,
        "current_row_primitivespec_dry_run_rows": current_rows,
        "coverage_summary": {
            "primitive_spec_requirement_row_count": len(requirement_rows),
            "future_native_primitivespec_shape_record_count": future_shape_count,
            "blocked_primitivespec_requirement_row_count": (
                blocked_requirement_count
            ),
            "noop_primitivespec_requirement_row_count": noop_requirement_count,
            "current_row_primitivespec_dry_run_row_count": len(current_rows),
            "current_primitivespec_dry_run_pass_record_count": current_pass_count,
            "current_primitivespec_noop_record_count": current_noop_count,
            "primitive_spec_candidate_record_count": candidate_count,
            "generated_primitive_spec_record_count": generated_count,
            "current_paper_primitive_distribution": _paper_policy_distribution(
                current_rows,
                "paper_primitive",
            ),
            "current_runtime_kind_distribution": _paper_policy_distribution(
                current_rows,
                "offline_runtime_kind_label",
            ),
        },
        "remaining_gaps": remaining_gaps,
        "generated_primitive_spec_count": generated_count,
        "generated_collision_package_count": 0,
        "runtime_admissibility_check_count": 0,
        "primitive_spec_generated": False,
        "collision_package_generated": False,
        "runtime_admissibility_checked": False,
        "newton_support_claimed": False,
        "approximation_policy_applied": False,
        "real_usd_loaded": False,
        "benchmark_run": False,
        "collision_quality_measured": False,
        "deployment_or_certification_claimed": False,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


_PRIMITIVESPEC_VALIDATION_ALLOWED_FUTURE_KINDS = ["box", "sphere", "capsule"]
_PRIMITIVESPEC_VALIDATION_EXPECTED_FAMILY_ORDER = [
    "oriented_bounding_box",
    "sphere",
    "capsule",
    "capped_cylinder",
    "frustum",
    "trapezoidal_prism",
]
_PRIMITIVESPEC_VALIDATION_EXPECTED_FAMILY_REQUIREMENTS = {
    "oriented_bounding_box": {
        "primitive_spec_dry_run_decision": (
            "future_native_family_primitivespec_shape_recorded_only"
        ),
        "candidate_runtime_kind": "box",
        "future_primitive_spec_kind": "box",
    },
    "sphere": {
        "primitive_spec_dry_run_decision": (
            "future_native_family_primitivespec_shape_recorded_only"
        ),
        "candidate_runtime_kind": "sphere",
        "future_primitive_spec_kind": "sphere",
    },
    "capsule": {
        "primitive_spec_dry_run_decision": (
            "future_native_family_primitivespec_shape_recorded_only"
        ),
        "candidate_runtime_kind": "capsule",
        "future_primitive_spec_kind": "capsule",
    },
    "capped_cylinder": {
        "primitive_spec_dry_run_decision": "blocked_approximation_policy_missing",
        "candidate_runtime_kind": "offline_only_unmapped",
        "future_primitive_spec_kind": None,
    },
    "frustum": {
        "primitive_spec_dry_run_decision": "blocked_approximation_policy_missing",
        "candidate_runtime_kind": "offline_only_unmapped",
        "future_primitive_spec_kind": None,
    },
    "trapezoidal_prism": {
        "primitive_spec_dry_run_decision": (
            "noop_current_unmapped_rows_keep_offline"
        ),
        "candidate_runtime_kind": "offline_only_unmapped",
        "future_primitive_spec_kind": None,
    },
}
_PRIMITIVESPEC_VALIDATION_ROW_FALSE_FLAGS = (
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


def _paper_validate_primitivespec_dry_run_row_false_flags(
    row: dict[str, object],
) -> None:
    for flag in _PRIMITIVESPEC_VALIDATION_ROW_FALSE_FLAGS:
        if bool(row.get(flag)):
            raise ValueError(f"input_trigger_flag_true:{flag}")


def _paper_require_nonempty_source_id(
    row: dict[str, object],
    field_name: str,
    error_prefix: str,
) -> None:
    if (
        field_name not in row
        or row[field_name] is None
        or str(row[field_name]).strip() == ""
    ):
        raise ValueError(f"{error_prefix}:{field_name}")


def _paper_validate_primitivespec_validation_row_false_flags(
    row: dict[str, object],
) -> None:
    for flag in _PRIMITIVESPEC_VALIDATION_ROW_FALSE_FLAGS:
        if bool(row.get(flag)):
            raise ValueError(f"validation_input_trigger_flag_true:{flag}")


def _paper_validate_primitivespec_validation_requirement_semantics(
    requirement_row: dict[str, object],
) -> None:
    paper_primitive = str(requirement_row["paper_primitive"])
    input_decision = str(requirement_row["primitive_spec_dry_run_decision"])
    known_decisions = {
        "future_native_family_primitivespec_shape_recorded_only",
        "blocked_approximation_policy_missing",
        "noop_current_unmapped_rows_keep_offline",
    }
    if input_decision not in known_decisions:
        raise ValueError(
            f"unknown_primitivespec_dry_run_family_decision:{input_decision}"
        )
    expected = _PRIMITIVESPEC_VALIDATION_EXPECTED_FAMILY_REQUIREMENTS[
        paper_primitive
    ]
    future_kind = requirement_row["future_primitive_spec_kind"]
    if (
        input_decision == "future_native_family_primitivespec_shape_recorded_only"
        and future_kind not in _PRIMITIVESPEC_VALIDATION_ALLOWED_FUTURE_KINDS
    ):
        raise ValueError("future_native_primitivespec_kind_missing")
    if (
        requirement_row["candidate_runtime_kind"]
        != expected["candidate_runtime_kind"]
    ):
        if expected["future_primitive_spec_kind"] is not None:
            raise ValueError(
                f"validation_future_mapping_label_mismatch:{paper_primitive}"
            )
        raise ValueError(f"validation_family_contract_mismatch:{paper_primitive}")
    if (
        requirement_row["primitive_spec_dry_run_decision"]
        != expected["primitive_spec_dry_run_decision"]
    ):
        raise ValueError(f"validation_family_contract_mismatch:{paper_primitive}")
    if (
        future_kind != expected["future_primitive_spec_kind"]
    ):
        raise ValueError(f"validation_family_contract_mismatch:{paper_primitive}")


def _paper_primitivespec_validation_requirement_row(
    requirement_row: dict[str, object],
) -> dict[str, object]:
    input_decision = str(requirement_row["primitive_spec_dry_run_decision"])
    future_kind = requirement_row["future_primitive_spec_kind"]
    if input_decision == "future_native_family_primitivespec_shape_recorded_only":
        if future_kind not in _PRIMITIVESPEC_VALIDATION_ALLOWED_FUTURE_KINDS:
            raise ValueError("future_native_primitivespec_kind_missing")
        decision = "future_native_family_primitivespec_shape_requirement_validated"
        shape_requirement_validated = True
        validated_future_kind = future_kind
    elif input_decision == "blocked_approximation_policy_missing":
        if future_kind is not None:
            raise ValueError("blocked_primitivespec_kind_claimed")
        decision = "blocked_approximation_policy_validation_recorded"
        shape_requirement_validated = False
        validated_future_kind = None
    elif input_decision == "noop_current_unmapped_rows_keep_offline":
        if future_kind is not None:
            raise ValueError("noop_primitivespec_kind_claimed")
        decision = "noop_unmapped_family_validation_recorded"
        shape_requirement_validated = False
        validated_future_kind = None
    else:
        raise ValueError(
            f"unknown_primitivespec_dry_run_family_decision:{input_decision}"
        )

    return {
        "primitive_spec_validation_row_id": (
            f"{requirement_row['primitive_spec_dry_run_row_id']}:validation"
        ),
        "source_primitivespec_dry_run_row_id": requirement_row[
            "primitive_spec_dry_run_row_id"
        ],
        "source_adapter_preflight_row_id": requirement_row[
            "source_adapter_preflight_row_id"
        ],
        "source_candidate_matrix_row_id": requirement_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": requirement_row[
            "source_conversion_plan_row_id"
        ],
        "paper_primitive": requirement_row["paper_primitive"],
        "candidate_mapping_label": requirement_row["candidate_runtime_kind"],
        "input_primitivespec_dry_run_decision": input_decision,
        "primitive_spec_validation_decision": decision,
        "validated_future_primitive_spec_kind": validated_future_kind,
        "future_primitive_spec_shape_requirement_validated": (
            shape_requirement_validated
        ),
        "required_primitive_spec_fields": list(
            requirement_row["required_primitive_spec_fields"]
        ),
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_primitivespec_validation_current_row(
    current_row: dict[str, object],
) -> dict[str, object]:
    input_decision = str(current_row["primitive_spec_dry_run_decision"])
    if input_decision != "skip_unmapped_current_row":
        raise ValueError(
            f"unknown_primitivespec_dry_run_current_decision:{input_decision}"
        )

    return {
        "primitive_spec_validation_row_id": (
            f"{current_row['primitive_spec_dry_run_row_id']}:validation"
        ),
        "source_primitivespec_dry_run_row_id": current_row[
            "primitive_spec_dry_run_row_id"
        ],
        "source_adapter_preflight_row_id": current_row[
            "source_adapter_preflight_row_id"
        ],
        "source_candidate_matrix_row_id": current_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": current_row[
            "source_conversion_plan_row_id"
        ],
        "source_policy_decision_id": current_row["source_policy_decision_id"],
        "source_adapter_decision_id": current_row["source_adapter_decision_id"],
        "source_output_id": current_row["source_output_id"],
        "evidence_case_id": current_row["evidence_case_id"],
        "offline_primitive_id": current_row["offline_primitive_id"],
        "paper_primitive": current_row["paper_primitive"],
        "offline_mapping_label": current_row["offline_runtime_kind_label"],
        "input_primitivespec_dry_run_decision": input_decision,
        "primitive_spec_validation_decision": "skip_unmapped_current_row_validated",
        "primitive_spec_validation_action": "keep_offline",
        "primitive_spec_validation_passed": False,
        "primitive_spec_candidate": False,
        "generated_primitive_spec": None,
        "silent_drop_detected": False,
        "required_later_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ),
        "required_future_policy": current_row["required_future_policy"],
        "primitive_spec_generation_triggered": False,
        "collision_package_generation_triggered": False,
        "runtime_admissibility_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _paper_validate_primitivespec_validation_dry_run(
    dry_run: dict[str, object],
) -> None:
    if (
        dry_run.get("gate_id")
        != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
    ):
        raise ValueError("primitivespec_validation_input_gate_id_mismatch")

    false_flags = (
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
    )
    for flag in false_flags:
        if bool(dry_run.get(flag)):
            raise ValueError(f"validation_input_trigger_flag_true:{flag}")

    if dry_run["candidate_count_at_dry_run"] != 0:
        raise ValueError("validation_input_candidate_count_nonzero")
    if dry_run["generated_primitive_spec_count"] != 0:
        raise ValueError("validation_input_generated_spec_nonzero")
    if dry_run["generated_collision_package_count"] != 0:
        raise ValueError("validation_input_generated_collision_package_nonzero")
    if dry_run["runtime_admissibility_check_count"] != 0:
        raise ValueError(
            "validation_input_trigger_flag_true:runtime_admissibility_check_count"
        )

    contract = dry_run["primitive_spec_dry_run_contract"]
    if contract["required_primitive_spec_fields"] != list(
        _PRIMITIVESPEC_DRY_RUN_REQUIRED_FIELDS
    ):
        raise ValueError("validation_required_fields_mismatch")
    if contract["allowed_future_runtime_kinds"] != list(
        _PRIMITIVESPEC_VALIDATION_ALLOWED_FUTURE_KINDS
    ):
        raise ValueError("validation_allowed_runtime_kinds_mismatch")
    for flag in (
        "primitive_spec_generation_allowed",
        "collision_package_generation_allowed",
        "newton_runtime_allowed",
        "runtime_admissibility_supported",
        "approximation_policy_enabled",
        "silent_drop_allowed",
    ):
        if bool(contract.get(flag)):
            raise ValueError(f"validation_input_trigger_flag_true:{flag}")

    requirement_rows = dry_run["primitive_spec_dry_run_requirement_rows"]
    current_rows = dry_run["current_row_primitivespec_dry_run_rows"]
    coverage = dry_run["coverage_summary"]
    expected_coverage = {
        "primitive_spec_requirement_row_count": 6,
        "future_native_primitivespec_shape_record_count": 3,
        "blocked_primitivespec_requirement_row_count": 2,
        "noop_primitivespec_requirement_row_count": 1,
        "current_row_primitivespec_dry_run_row_count": 16,
        "current_primitivespec_dry_run_pass_record_count": 0,
        "current_primitivespec_noop_record_count": 16,
        "primitive_spec_candidate_record_count": 0,
        "generated_primitive_spec_record_count": 0,
    }
    for field_name, expected_value in expected_coverage.items():
        if coverage[field_name] != expected_value:
            raise ValueError(f"validation_coverage_count_mismatch:{field_name}")
    if len(requirement_rows) != 6 or len(current_rows) != 16:
        raise ValueError("validation_coverage_count_mismatch:row_count")
    if [
        row["paper_primitive"] for row in requirement_rows
    ] != _PRIMITIVESPEC_VALIDATION_EXPECTED_FAMILY_ORDER:
        raise ValueError("validation_family_primitive_sequence_mismatch")

    row_ids: list[str] = []
    required_requirement_fields = (
        "source_adapter_preflight_row_id",
        "source_candidate_matrix_row_id",
        "source_conversion_plan_row_id",
    )
    for requirement_row in requirement_rows:
        _paper_require_nonempty_source_id(
            requirement_row,
            "primitive_spec_dry_run_row_id",
            "validation_missing_primitivespec_dry_run_row_id",
        )
        row_ids.append(str(requirement_row["primitive_spec_dry_run_row_id"]))
        for field_name in required_requirement_fields:
            _paper_require_nonempty_source_id(
                requirement_row,
                field_name,
                "validation_missing_requirement_row_source_id",
            )
        _paper_validate_primitivespec_validation_requirement_semantics(
            requirement_row
        )
        if requirement_row["required_primitive_spec_fields"] != list(
            _PRIMITIVESPEC_DRY_RUN_REQUIRED_FIELDS
        ):
            raise ValueError("validation_required_fields_mismatch")
        _paper_validate_primitivespec_validation_row_false_flags(requirement_row)

    required_current_fields = (
        "source_adapter_preflight_row_id",
        "source_candidate_matrix_row_id",
        "source_conversion_plan_row_id",
        "source_policy_decision_id",
        "source_adapter_decision_id",
        "source_output_id",
        "evidence_case_id",
        "offline_primitive_id",
    )
    for current_row in current_rows:
        _paper_require_nonempty_source_id(
            current_row,
            "primitive_spec_dry_run_row_id",
            "validation_missing_primitivespec_dry_run_row_id",
        )
        row_ids.append(str(current_row["primitive_spec_dry_run_row_id"]))
        for field_name in required_current_fields:
            _paper_require_nonempty_source_id(
                current_row,
                field_name,
                "validation_missing_current_row_source_id",
            )
        if bool(current_row["primitive_spec_dry_run_passed"]):
            raise ValueError("validation_input_pass_count_nonzero")
        if bool(current_row["primitive_spec_candidate"]):
            raise ValueError("validation_input_candidate_count_nonzero")
        if current_row["generated_primitive_spec"] is not None:
            raise ValueError("validation_input_generated_spec_nonzero")
        if (
            current_row["required_later_gate"]
            != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
        ):
            raise ValueError(
                "validation_current_row_required_later_gate_mismatch"
            )
        _paper_validate_primitivespec_validation_row_false_flags(current_row)

    if len(row_ids) != len(set(row_ids)):
        raise ValueError("duplicate_primitivespec_dry_run_row_id")


def _paper_mapped_subset_primitivespec_validation_contract_payload(
    dry_run: dict[str, object],
) -> dict[str, object]:
    _paper_validate_primitivespec_validation_dry_run(dry_run)
    requirement_rows = [
        _paper_primitivespec_validation_requirement_row(row)
        for row in dry_run["primitive_spec_dry_run_requirement_rows"]
    ]
    current_rows = [
        _paper_primitivespec_validation_current_row(row)
        for row in dry_run["current_row_primitivespec_dry_run_rows"]
    ]
    future_shape_validation_count = sum(
        bool(row["future_primitive_spec_shape_requirement_validated"])
        for row in requirement_rows
    )
    blocked_requirement_count = sum(
        row["primitive_spec_validation_decision"]
        == "blocked_approximation_policy_validation_recorded"
        for row in requirement_rows
    )
    noop_requirement_count = sum(
        row["primitive_spec_validation_decision"]
        == "noop_unmapped_family_validation_recorded"
        for row in requirement_rows
    )
    current_pass_count = sum(
        bool(row["primitive_spec_validation_passed"]) for row in current_rows
    )
    current_noop_count = sum(
        row["primitive_spec_validation_decision"]
        == "skip_unmapped_current_row_validated"
        for row in current_rows
    )
    candidate_count = sum(
        bool(row["primitive_spec_candidate"]) for row in current_rows
    )
    generated_count = sum(
        row["generated_primitive_spec"] is not None for row in current_rows
    )
    remaining_gaps = (
        _paper_remaining_gaps_after_mapped_subset_primitivespec_validation()
    )
    return {
        "gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
        "gate_status": (
            "implemented_offline_primitivespec_validation_contract_only_partial"
        ),
        "closed_gate": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
        "input_gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
        "next_required_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ),
        "decision": "remain_partial",
        "decision_reason": (
            "primitivespec_validation_contract_complete_"
            "primitivespec_generation_preflight_contract_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": (
            "offline_primitivespec_validation_contract_not_primitivespec_"
            "not_collision_package"
        ),
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_primitivespec_validation_no_primitivespec_"
            "no_collision_package_no_newton"
        ),
        "validation_action": "validate_dry_run_contract_keep_offline",
        "validated_primitive_spec_candidate_count": candidate_count,
        "primitive_spec_generation_allowed": False,
        "collision_package_generation_allowed": False,
        "runtime_admissibility_supported": False,
        "newton_runtime_allowed": False,
        "approximation_policy_enabled": False,
        "silent_drop_allowed": False,
        "input_contract_summary": {
            "input_gate_id": dry_run["gate_id"],
            "input_artifact_kind": dry_run["artifact_kind"],
            "primitive_spec_requirement_row_count": dry_run[
                "coverage_summary"
            ]["primitive_spec_requirement_row_count"],
            "current_row_primitivespec_dry_run_row_count": dry_run[
                "coverage_summary"
            ]["current_row_primitivespec_dry_run_row_count"],
            "current_primitivespec_dry_run_pass_record_count": dry_run[
                "coverage_summary"
            ]["current_primitivespec_dry_run_pass_record_count"],
            "primitive_spec_candidate_record_count": dry_run[
                "coverage_summary"
            ]["primitive_spec_candidate_record_count"],
            "generated_primitive_spec_record_count": dry_run[
                "coverage_summary"
            ]["generated_primitive_spec_record_count"],
        },
        "primitive_spec_validation_contract": {
            "dry_run_input_gate_required": (
                _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT
            ),
            "unique_row_ids_required": True,
            "complete_source_evidence_ids_required": True,
            "zero_current_primitivespec_candidates_required": True,
            "zero_generated_primitivespecs_required": True,
            "zero_runtime_admissibility_checks_required": True,
            "allowed_future_mapping_candidate_labels": list(
                _PRIMITIVESPEC_VALIDATION_ALLOWED_FUTURE_KINDS
            ),
            "required_primitive_spec_fields": list(
                _PRIMITIVESPEC_DRY_RUN_REQUIRED_FIELDS
            ),
            "expected_requirement_row_count": 6,
            "expected_current_row_count": 16,
            "primitive_spec_generation_allowed": False,
            "collision_package_generation_allowed": False,
            "newton_runtime_allowed": False,
            "runtime_admissibility_supported": False,
            "approximation_policy_enabled": False,
            "silent_drop_allowed": False,
        },
        "primitive_spec_validation_requirement_rows": requirement_rows,
        "current_row_primitivespec_validation_rows": current_rows,
        "coverage_summary": {
            "primitive_spec_validation_requirement_row_count": len(
                requirement_rows
            ),
            "future_native_primitivespec_shape_validation_count": (
                future_shape_validation_count
            ),
            "blocked_primitivespec_validation_requirement_count": (
                blocked_requirement_count
            ),
            "noop_primitivespec_validation_requirement_count": (
                noop_requirement_count
            ),
            "current_row_primitivespec_validation_row_count": len(current_rows),
            "current_primitivespec_validation_pass_record_count": current_pass_count,
            "current_primitivespec_validation_noop_record_count": current_noop_count,
            "validated_primitive_spec_candidate_record_count": candidate_count,
            "generated_primitive_spec_record_count": generated_count,
            "current_paper_primitive_distribution": _paper_policy_distribution(
                current_rows,
                "paper_primitive",
            ),
            "current_mapping_label_distribution": _paper_policy_distribution(
                current_rows,
                "offline_mapping_label",
            ),
        },
        "remaining_gaps": remaining_gaps,
        "generated_primitive_spec_count": generated_count,
        "generated_collision_package_count": 0,
        "runtime_admissibility_check_count": 0,
        "primitive_spec_generated": False,
        "collision_package_generated": False,
        "runtime_admissibility_checked": False,
        "newton_support_claimed": False,
        "approximation_policy_applied": False,
        "real_usd_loaded": False,
        "benchmark_run": False,
        "collision_quality_measured": False,
        "deployment_or_certification_claimed": False,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


_PRIMITIVESPEC_GENERATION_PREFLIGHT_EXPECTED_FAMILY_REQUIREMENTS = {
    "oriented_bounding_box": {
        "primitive_spec_validation_decision": (
            "future_native_family_primitivespec_shape_requirement_validated"
        ),
        "candidate_mapping_label": "box",
        "validated_future_primitive_spec_kind": "box",
    },
    "sphere": {
        "primitive_spec_validation_decision": (
            "future_native_family_primitivespec_shape_requirement_validated"
        ),
        "candidate_mapping_label": "sphere",
        "validated_future_primitive_spec_kind": "sphere",
    },
    "capsule": {
        "primitive_spec_validation_decision": (
            "future_native_family_primitivespec_shape_requirement_validated"
        ),
        "candidate_mapping_label": "capsule",
        "validated_future_primitive_spec_kind": "capsule",
    },
    "capped_cylinder": {
        "primitive_spec_validation_decision": (
            "blocked_approximation_policy_validation_recorded"
        ),
        "candidate_mapping_label": "offline_only_unmapped",
        "validated_future_primitive_spec_kind": None,
    },
    "frustum": {
        "primitive_spec_validation_decision": (
            "blocked_approximation_policy_validation_recorded"
        ),
        "candidate_mapping_label": "offline_only_unmapped",
        "validated_future_primitive_spec_kind": None,
    },
    "trapezoidal_prism": {
        "primitive_spec_validation_decision": (
            "noop_unmapped_family_validation_recorded"
        ),
        "candidate_mapping_label": "offline_only_unmapped",
        "validated_future_primitive_spec_kind": None,
    },
}


def _paper_false_primitivespec_generation_preflight_flags() -> dict[str, bool]:
    return {
        flag: False
        for flag in _PRIMITIVESPEC_VALIDATION_ROW_FALSE_FLAGS
    }


def _paper_validate_primitivespec_generation_preflight_false_flags(
    row: dict[str, object],
) -> None:
    for flag in _PRIMITIVESPEC_VALIDATION_ROW_FALSE_FLAGS:
        if bool(row.get(flag)):
            raise ValueError(
                f"generation_preflight_input_trigger_flag_true:{flag}"
            )


def _paper_validate_primitivespec_generation_preflight_requirement_semantics(
    requirement_row: dict[str, object],
) -> None:
    paper_primitive = str(requirement_row["paper_primitive"])
    input_decision = str(requirement_row["primitive_spec_validation_decision"])
    known_decisions = {
        "future_native_family_primitivespec_shape_requirement_validated",
        "blocked_approximation_policy_validation_recorded",
        "noop_unmapped_family_validation_recorded",
    }
    if input_decision not in known_decisions:
        raise ValueError(
            f"unknown_primitivespec_validation_family_decision:{input_decision}"
        )

    expected = _PRIMITIVESPEC_GENERATION_PREFLIGHT_EXPECTED_FAMILY_REQUIREMENTS[
        paper_primitive
    ]
    if (
        requirement_row["candidate_mapping_label"]
        != expected["candidate_mapping_label"]
    ):
        if expected["validated_future_primitive_spec_kind"] is not None:
            raise ValueError(
                "generation_preflight_future_mapping_label_mismatch:"
                f"{paper_primitive}"
            )
        raise ValueError(
            f"generation_preflight_family_contract_mismatch:{paper_primitive}"
        )
    if input_decision != expected["primitive_spec_validation_decision"]:
        raise ValueError(
            f"generation_preflight_family_contract_mismatch:{paper_primitive}"
        )
    if (
        requirement_row["validated_future_primitive_spec_kind"]
        != expected["validated_future_primitive_spec_kind"]
    ):
        raise ValueError(
            f"generation_preflight_family_contract_mismatch:{paper_primitive}"
        )


def _paper_validate_primitivespec_generation_preflight_validation(
    validation: dict[str, object],
) -> None:
    if (
        validation.get("gate_id")
        != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
    ):
        raise ValueError(
            "primitivespec_generation_preflight_input_gate_id_mismatch"
        )

    _paper_validate_primitivespec_generation_preflight_false_flags(validation)
    if validation["validated_primitive_spec_candidate_count"] != 0:
        raise ValueError("generation_preflight_input_candidate_count_nonzero")
    if validation["generated_primitive_spec_count"] != 0:
        raise ValueError("generation_preflight_input_generated_spec_nonzero")
    if validation["generated_collision_package_count"] != 0:
        raise ValueError(
            "generation_preflight_input_generated_collision_package_nonzero"
        )
    if validation["runtime_admissibility_check_count"] != 0:
        raise ValueError(
            "generation_preflight_input_trigger_flag_true:"
            "runtime_admissibility_check_count"
        )

    requirement_rows = validation["primitive_spec_validation_requirement_rows"]
    current_rows = validation["current_row_primitivespec_validation_rows"]
    coverage = validation["coverage_summary"]
    expected_coverage = {
        "primitive_spec_validation_requirement_row_count": 6,
        "future_native_primitivespec_shape_validation_count": 3,
        "blocked_primitivespec_validation_requirement_count": 2,
        "noop_primitivespec_validation_requirement_count": 1,
        "current_row_primitivespec_validation_row_count": 16,
        "current_primitivespec_validation_pass_record_count": 0,
        "current_primitivespec_validation_noop_record_count": 16,
        "validated_primitive_spec_candidate_record_count": 0,
        "generated_primitive_spec_record_count": 0,
    }
    for field_name, expected_value in expected_coverage.items():
        if coverage[field_name] != expected_value:
            raise ValueError(
                f"generation_preflight_coverage_count_mismatch:{field_name}"
            )
    if len(requirement_rows) != 6 or len(current_rows) != 16:
        raise ValueError("generation_preflight_coverage_count_mismatch:row_count")
    if [
        row["paper_primitive"] for row in requirement_rows
    ] != _PRIMITIVESPEC_VALIDATION_EXPECTED_FAMILY_ORDER:
        raise ValueError("generation_preflight_family_primitive_sequence_mismatch")

    row_ids: list[str] = []
    required_requirement_fields = (
        "source_primitivespec_dry_run_row_id",
        "source_adapter_preflight_row_id",
        "source_candidate_matrix_row_id",
        "source_conversion_plan_row_id",
    )
    for requirement_row in requirement_rows:
        _paper_require_nonempty_source_id(
            requirement_row,
            "primitive_spec_validation_row_id",
            "generation_preflight_missing_validation_row_id",
        )
        row_ids.append(str(requirement_row["primitive_spec_validation_row_id"]))
        for field_name in required_requirement_fields:
            _paper_require_nonempty_source_id(
                requirement_row,
                field_name,
                "generation_preflight_missing_validation_row_id",
            )
        _paper_validate_primitivespec_generation_preflight_requirement_semantics(
            requirement_row
        )
        if requirement_row["required_primitive_spec_fields"] != list(
            _PRIMITIVESPEC_DRY_RUN_REQUIRED_FIELDS
        ):
            raise ValueError("generation_preflight_required_fields_mismatch")
        _paper_validate_primitivespec_generation_preflight_false_flags(
            requirement_row
        )

    required_current_fields = (
        "source_primitivespec_dry_run_row_id",
        "source_adapter_preflight_row_id",
        "source_candidate_matrix_row_id",
        "source_conversion_plan_row_id",
        "source_policy_decision_id",
        "source_adapter_decision_id",
        "source_output_id",
        "evidence_case_id",
        "offline_primitive_id",
    )
    for current_row in current_rows:
        _paper_require_nonempty_source_id(
            current_row,
            "primitive_spec_validation_row_id",
            "generation_preflight_missing_validation_row_id",
        )
        row_ids.append(str(current_row["primitive_spec_validation_row_id"]))
        for field_name in required_current_fields:
            _paper_require_nonempty_source_id(
                current_row,
                field_name,
                "generation_preflight_missing_current_row_source_id",
            )
        input_decision = str(current_row["primitive_spec_validation_decision"])
        if input_decision != "skip_unmapped_current_row_validated":
            raise ValueError(
                "unknown_primitivespec_validation_current_decision:"
                f"{input_decision}"
            )
        if bool(current_row["primitive_spec_validation_passed"]):
            raise ValueError("generation_preflight_input_candidate_count_nonzero")
        if bool(current_row["primitive_spec_candidate"]):
            raise ValueError("generation_preflight_input_candidate_count_nonzero")
        if current_row["generated_primitive_spec"] is not None:
            raise ValueError("generation_preflight_input_generated_spec_nonzero")
        if (
            current_row["required_later_gate"]
            != _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ):
            raise ValueError(
                "generation_preflight_current_row_required_later_gate_mismatch"
            )
        _paper_validate_primitivespec_generation_preflight_false_flags(
            current_row
        )

    if len(row_ids) != len(set(row_ids)):
        raise ValueError("duplicate_primitivespec_validation_row_id")


def _paper_primitivespec_generation_preflight_requirement_row(
    requirement_row: dict[str, object],
) -> dict[str, object]:
    input_decision = str(requirement_row["primitive_spec_validation_decision"])
    if input_decision == (
        "future_native_family_primitivespec_shape_requirement_validated"
    ):
        decision = "future_native_family_generation_requirement_preflighted"
    elif input_decision == "blocked_approximation_policy_validation_recorded":
        decision = "blocked_approximation_policy_generation_preflight_recorded"
    elif input_decision == "noop_unmapped_family_validation_recorded":
        decision = "noop_unmapped_family_generation_preflight_recorded"
    else:
        raise ValueError(
            f"unknown_primitivespec_validation_family_decision:{input_decision}"
        )

    return {
        "primitive_spec_generation_preflight_row_id": (
            f"{requirement_row['primitive_spec_validation_row_id']}:"
            "generation_preflight"
        ),
        "source_primitivespec_validation_row_id": requirement_row[
            "primitive_spec_validation_row_id"
        ],
        "source_primitivespec_dry_run_row_id": requirement_row[
            "source_primitivespec_dry_run_row_id"
        ],
        "source_adapter_preflight_row_id": requirement_row[
            "source_adapter_preflight_row_id"
        ],
        "source_candidate_matrix_row_id": requirement_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": requirement_row[
            "source_conversion_plan_row_id"
        ],
        "paper_primitive": requirement_row["paper_primitive"],
        "candidate_mapping_label": requirement_row["candidate_mapping_label"],
        "validated_future_primitive_spec_kind": requirement_row[
            "validated_future_primitive_spec_kind"
        ],
        "input_primitivespec_validation_decision": input_decision,
        "primitive_spec_generation_preflight_decision": decision,
        "generation_preflight_candidate": False,
        "required_later_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        ),
        "required_primitive_spec_fields": list(
            requirement_row["required_primitive_spec_fields"]
        ),
        **_paper_false_primitivespec_generation_preflight_flags(),
    }


def _paper_primitivespec_generation_preflight_current_row(
    current_row: dict[str, object],
) -> dict[str, object]:
    input_decision = str(current_row["primitive_spec_validation_decision"])
    if input_decision != "skip_unmapped_current_row_validated":
        raise ValueError(
            f"unknown_primitivespec_validation_current_decision:{input_decision}"
        )

    return {
        "primitive_spec_generation_preflight_row_id": (
            f"{current_row['primitive_spec_validation_row_id']}:"
            "generation_preflight"
        ),
        "source_primitivespec_validation_row_id": current_row[
            "primitive_spec_validation_row_id"
        ],
        "source_primitivespec_dry_run_row_id": current_row[
            "source_primitivespec_dry_run_row_id"
        ],
        "source_adapter_preflight_row_id": current_row[
            "source_adapter_preflight_row_id"
        ],
        "source_candidate_matrix_row_id": current_row[
            "source_candidate_matrix_row_id"
        ],
        "source_conversion_plan_row_id": current_row[
            "source_conversion_plan_row_id"
        ],
        "source_policy_decision_id": current_row["source_policy_decision_id"],
        "source_adapter_decision_id": current_row["source_adapter_decision_id"],
        "source_output_id": current_row["source_output_id"],
        "evidence_case_id": current_row["evidence_case_id"],
        "offline_primitive_id": current_row["offline_primitive_id"],
        "paper_primitive": current_row["paper_primitive"],
        "offline_mapping_label": current_row["offline_mapping_label"],
        "input_primitivespec_validation_decision": input_decision,
        "primitive_spec_generation_preflight_decision": (
            "skip_unmapped_current_row_preflighted"
        ),
        "primitive_spec_generation_preflight_action": "keep_offline",
        "primitive_spec_generation_preflight_passed": False,
        "primitive_spec_generation_candidate": False,
        "generated_primitive_spec": None,
        "silent_drop_detected": False,
        "required_later_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        ),
        "required_future_policy": current_row["required_future_policy"],
        **_paper_false_primitivespec_generation_preflight_flags(),
    }


def _paper_require_unique_generation_preflight_row_ids(
    rows: list[dict[str, object]],
) -> None:
    row_ids = [
        str(row["primitive_spec_generation_preflight_row_id"])
        for row in rows
    ]
    if len(row_ids) != len(set(row_ids)):
        raise ValueError("duplicate_primitivespec_generation_preflight_row_id")


def _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
    validation: dict[str, object],
) -> dict[str, object]:
    _paper_validate_primitivespec_generation_preflight_validation(validation)
    requirement_rows = [
        _paper_primitivespec_generation_preflight_requirement_row(row)
        for row in validation["primitive_spec_validation_requirement_rows"]
    ]
    current_rows = [
        _paper_primitivespec_generation_preflight_current_row(row)
        for row in validation["current_row_primitivespec_validation_rows"]
    ]
    _paper_require_unique_generation_preflight_row_ids(
        requirement_rows + current_rows
    )

    future_native_count = sum(
        row["primitive_spec_generation_preflight_decision"]
        == "future_native_family_generation_requirement_preflighted"
        for row in requirement_rows
    )
    blocked_count = sum(
        row["primitive_spec_generation_preflight_decision"]
        == "blocked_approximation_policy_generation_preflight_recorded"
        for row in requirement_rows
    )
    noop_requirement_count = sum(
        row["primitive_spec_generation_preflight_decision"]
        == "noop_unmapped_family_generation_preflight_recorded"
        for row in requirement_rows
    )
    current_pass_count = sum(
        bool(row["primitive_spec_generation_preflight_passed"])
        for row in current_rows
    )
    current_noop_count = sum(
        row["primitive_spec_generation_preflight_decision"]
        == "skip_unmapped_current_row_preflighted"
        for row in current_rows
    )
    candidate_count = sum(
        bool(row["primitive_spec_generation_candidate"])
        for row in current_rows
    )
    generated_count = sum(
        row["generated_primitive_spec"] is not None for row in current_rows
    )
    remaining_gaps = (
        _paper_remaining_gaps_after_mapped_subset_primitivespec_generation_preflight()
    )
    return {
        "gate_id": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ),
        "gate_status": (
            "implemented_offline_primitivespec_generation_preflight_contract_"
            "only_partial"
        ),
        "closed_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT
        ),
        "input_gate_id": _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
        "next_required_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        ),
        "decision": "remain_partial",
        "decision_reason": (
            "primitivespec_generation_preflight_contract_complete_"
            "primitivespec_generation_contract_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "package_generation_allowed": False,
        "artifact_kind": (
            "offline_primitivespec_generation_preflight_contract_not_"
            "primitivespec_not_collision_package"
        ),
        "schema_version": 1,
        "source_scope": "synthetic_toy_fixtures_only",
        "implementation_boundary": (
            "offline_primitivespec_generation_preflight_no_primitivespec_"
            "no_collision_package_no_newton"
        ),
        "generation_preflight_action": "preflight_validation_contract_keep_offline",
        "generation_preflight_candidate_count": candidate_count,
        "generated_primitive_spec_count": generated_count,
        "generated_collision_package_count": 0,
        "runtime_admissibility_check_count": 0,
        "input_contract_summary": {
            "input_gate_id": validation["gate_id"],
            "input_artifact_kind": validation["artifact_kind"],
            "primitive_spec_validation_requirement_row_count": validation[
                "coverage_summary"
            ]["primitive_spec_validation_requirement_row_count"],
            "current_row_primitivespec_validation_row_count": validation[
                "coverage_summary"
            ]["current_row_primitivespec_validation_row_count"],
            "current_primitivespec_validation_pass_record_count": validation[
                "coverage_summary"
            ]["current_primitivespec_validation_pass_record_count"],
            "validated_primitive_spec_candidate_record_count": validation[
                "coverage_summary"
            ]["validated_primitive_spec_candidate_record_count"],
            "generated_primitive_spec_record_count": validation[
                "coverage_summary"
            ]["generated_primitive_spec_record_count"],
        },
        "primitive_spec_generation_preflight_contract": {
            "validation_input_gate_required": (
                _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT
            ),
            "unique_row_ids_required": True,
            "complete_source_evidence_ids_required": True,
            "zero_current_generation_candidates_required": True,
            "zero_generated_primitivespecs_required": True,
            "zero_runtime_admissibility_checks_required": True,
            "allowed_future_mapping_candidate_labels": list(
                _PRIMITIVESPEC_VALIDATION_ALLOWED_FUTURE_KINDS
            ),
            "required_primitive_spec_fields": list(
                _PRIMITIVESPEC_DRY_RUN_REQUIRED_FIELDS
            ),
            "expected_requirement_row_count": 6,
            "expected_current_row_count": 16,
            "primitive_spec_generation_allowed": False,
            "collision_package_generation_allowed": False,
            "newton_runtime_allowed": False,
            "runtime_admissibility_supported": False,
            "approximation_policy_enabled": False,
            "silent_drop_allowed": False,
        },
        "primitive_spec_generation_preflight_requirement_rows": requirement_rows,
        "current_row_primitivespec_generation_preflight_rows": current_rows,
        "coverage_summary": {
            "primitive_spec_generation_preflight_requirement_row_count": len(
                requirement_rows
            ),
            "future_native_primitivespec_generation_preflight_count": (
                future_native_count
            ),
            "blocked_primitivespec_generation_preflight_requirement_count": (
                blocked_count
            ),
            "noop_primitivespec_generation_preflight_requirement_count": (
                noop_requirement_count
            ),
            "current_row_primitivespec_generation_preflight_row_count": len(
                current_rows
            ),
            "current_primitivespec_generation_preflight_pass_record_count": (
                current_pass_count
            ),
            "current_primitivespec_generation_preflight_noop_record_count": (
                current_noop_count
            ),
            "generation_preflight_candidate_record_count": candidate_count,
            "generated_primitive_spec_record_count": generated_count,
            "current_paper_primitive_distribution": _paper_policy_distribution(
                current_rows,
                "paper_primitive",
            ),
            "current_mapping_label_distribution": _paper_policy_distribution(
                current_rows,
                "offline_mapping_label",
            ),
        },
        "remaining_gaps": remaining_gaps,
        **_paper_false_primitivespec_generation_preflight_flags(),
    }


def _paper_source_policy_generalization_payload(
    cases: list[dict[str, object]],
) -> dict[str, object]:
    cases_by_id = {str(case["case_id"]): case for case in cases}
    mixed = cases_by_id["paper_mixed_face_preprocess_operator"]
    degenerate = cases_by_id["paper_degenerate_preprocess_face_drop"]
    concave = cases_by_id["paper_concave_polygon_rejected"]
    remaining_generalization_gates = _paper_remaining_generalization_gates_after_source_policy()
    policy_matrix = [
        {
            "policy_row_id": "accepted_mixed_triangle_quad_polygon_exact_dedup",
            "evidence_case_id": mixed["case_id"],
            "row_status": "accepted_offline_policy_fixture",
            "source_face_arities": mixed["source_mesh"]["source_face_arities"],
            "source_face_count": mixed["source_mesh"]["source_face_count"],
            "triangulated_face_count": mixed["source_mesh"][
                "triangulated_face_count"
            ],
            "duplicate_vertex_preprocessing": mixed["source_mesh"][
                "duplicate_vertex_preprocessing"
            ],
            "source_face_remap_count": len(mixed["source_mesh"]["source_face_remap"]),
            "operator_aggregate_count": len(
                mixed["operator_audit"]["source_face_operator_aggregates"]
            ),
            "operator_aggregate_source_face_ids": [
                int(aggregate["source_face_id"])
                for aggregate in mixed["operator_audit"][
                    "source_face_operator_aggregates"
                ]
            ],
            "operator_aggregate_generated_triangle_face_ids": [
                [
                    int(face_id)
                    for face_id in aggregate["generated_triangle_face_ids"]
                ]
                for aggregate in mixed["operator_audit"][
                    "source_face_operator_aggregates"
                ]
            ],
            "operator_q_aggregation_policy": (
                "aggregate_q_matrix_equals_sum_generated_triangle_q_rows"
            ),
        },
        {
            "policy_row_id": "accepted_degenerate_after_exact_dedup_drop",
            "evidence_case_id": degenerate["case_id"],
            "row_status": "accepted_after_dropping_degenerate_source_face",
            "dropped_source_face_ids": degenerate["preprocessing_audit"][
                "dropped_source_face_ids"
            ],
            "retained_source_face_ids": degenerate["preprocessing_audit"][
                "retained_source_face_ids"
            ],
            "executable_source_face_ids": degenerate["source_mesh"][
                "executable_source_face_ids"
            ],
            "operator_source_faces": degenerate["operator_audit"]["merged_group"][
                "source_faces"
            ],
            "primitive_fit_source_faces": degenerate["primitive_fit_audit"][
                "source_faces"
            ],
        },
        {
            "policy_row_id": "rejected_concave_polygon",
            "evidence_case_id": concave["case_id"],
            "row_status": "unsupported_offline_policy_fixture",
            "case_status": concave["case_status"],
            "failure_label": concave["mesh_intake_policy_audit"]["failure_label"],
            "top_level_failure_label": concave["mesh_intake_policy_audit"][
                "top_level_failure_label"
            ],
            "source_face_arities": concave["source_mesh"]["source_face_arities"],
            "triangulated_face_count": concave["source_mesh"][
                "triangulated_face_count"
            ],
            "operator_row_count": 0,
            "primitive_fit_row_count": 0,
        },
    ]
    return {
        "gate_id": _PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY,
        "gate_status": "implemented_offline_report_only_partial",
        "closed_gate": _PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY,
        "next_required_gate": _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
        "decision": "remain_partial",
        "decision_reason": (
            "source_policy_generalization_complete_primitive_fit_engine_missing"
        ),
        "paper_faithful_offline_allowed": False,
        "source_scope": "synthetic_in_memory_source_mesh_policy_matrix",
        "implementation_boundary": "offline_report_only_no_package_or_newton",
        "source_mesh_contract": {
            "accepted_source_representation": (
                "vertices_plus_variable_arity_source_faces"
            ),
            "source_face_id_policy": (
                "preserve_source_face_ids_distinct_from_generated_triangle_ids"
            ),
            "general_mesh_cleanup_supported": False,
        },
        "preprocessing_policy": {
            "deduplication_policy": "exact_coordinate_first_occurrence_only",
            "distance_tolerance": 0.0,
            "degenerate_face_policy": (
                "drop_after_exact_deduplication_from_executable_rows"
            ),
            "nonzero_distance_cleanup_supported": False,
        },
        "source_face_intake_policy": {
            "accepted_preconditions": _source_face_preconditions(),
            "triangulation_policy": "fan_from_first_vertex",
            "unsupported_policy": (
                "reject_concave_polygon_without_top_level_failure_label"
            ),
            "general_polygon_mesh_intake_supported": False,
        },
        "operator_policy": {
            "triangle_operator_policy": "compute_q_on_executable_triangles",
            "source_face_aggregate_policy": (
                "sum_generated_triangle_q_rows_to_source_face"
            ),
            "aggregate_eigen_fields_required": True,
        },
        "policy_matrix": policy_matrix,
        "coverage_summary": {
            "evidence_case_count": len(policy_matrix),
            "accepted_policy_row_count": 2,
            "unsupported_policy_row_count": 1,
            "closed_gate_count": 1,
            "remaining_generalization_gate_count": len(remaining_generalization_gates),
        },
        "remaining_gaps": remaining_generalization_gates,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def build_cpd_paper_offline_report() -> dict[str, object]:
    """Build the first fixture-scoped offline CPD paper mechanics audit."""

    cases = [_case_payload(case) for case in _paper_toy_cases()]
    changed_decomposition_output_contract = (
        _paper_changed_decomposition_output_contract_payload(cases)
    )
    package_adapter_contract = _paper_package_adapter_contract_payload(
        changed_decomposition_output_contract
    )
    package_adapter_unsupported_policy = (
        _paper_package_adapter_unsupported_primitive_policy_payload(
            package_adapter_contract
        )
    )
    package_conversion_mapped_subset_plan = (
        _paper_package_conversion_mapped_subset_plan_payload(
            package_adapter_unsupported_policy
        )
    )
    mapped_subset_candidate_matrix = (
        _paper_mapped_subset_conversion_candidate_matrix_payload(
            package_conversion_mapped_subset_plan
        )
    )
    mapped_subset_adapter_preflight = (
        _paper_mapped_subset_adapter_preflight_contract_payload(
            mapped_subset_candidate_matrix
        )
    )
    mapped_subset_primitivespec_dry_run = (
        _paper_mapped_subset_primitivespec_dry_run_contract_payload(
            mapped_subset_adapter_preflight
        )
    )
    mapped_subset_primitivespec_validation = (
        _paper_mapped_subset_primitivespec_validation_contract_payload(
            mapped_subset_primitivespec_dry_run
        )
    )
    mapped_subset_primitivespec_generation_preflight = (
        _paper_mapped_subset_primitivespec_generation_preflight_contract_payload(
            mapped_subset_primitivespec_validation
        )
    )
    missing_before_paper_faithful = (
        _paper_remaining_gaps_after_mapped_subset_primitivespec_generation_preflight()
    )
    return {
        "stage": "cpd_paper_offline_report",
        "status": "partial",
        "report_generation_status": "smoke_passed",
        "claim_boundary": CPD_PAPER_OFFLINE_CLAIM_BOUNDARY,
        "evidence_level": CPD_PAPER_OFFLINE_EVIDENCE_LEVEL,
        "status_semantics": CPD_PAPER_OFFLINE_STATUS_SEMANTICS,
        "source_scope": "synthetic_toy_fixtures_only",
        "paper_faithful_offline_supported": False,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
        "failure_labels": [
            f"{missing_item}_missing"
            for missing_item in missing_before_paper_faithful
        ],
        "next_required_gate": (
            _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_CONTRACT
        ),
        "paper_faithfulness": {
            "status": "partial",
            "implemented_fixture_scope": [
                "triangle_only_mesh_intake",
                "operator_audit",
                "primitive_fit_audit_all_paper_names_with_surrogate_rows",
                "single_pop_collapse_cost_audit",
                "priority_queue_trace_audit_topology_only",
                "component_pair_edge_insertion_audit_threshold_disabled",
                "component_pair_threshold_blocking_audit",
                "postprocess_enclosed_primitive_culling_audit",
                "paper_polygon_quad_intake_policy_audit",
                "paper_obb_sphere_fit_faithfulness_audit",
                "paper_duplicate_vertex_preprocessing_audit",
                "paper_faithful_offline_scope_audit",
                "paper_fixture_breadth_batch_a_source_preprocess_intake_operator",
                "paper_fixture_breadth_batch_b_primitive_fit",
                "paper_fixture_breadth_batch_c_cost_search_stop",
                "paper_fixture_breadth_batch_d_component_pair",
                "paper_fixture_breadth_batch_e_postprocess",
                "paper_fixture_breadth_completion_review",
            ],
            "implemented_planning_scope": [
                "paper_faithful_offline_generalization_plan",
            ],
            "implemented_generalization_scope": [
                _PAPER_GENERALIZATION_BATCH_A_SOURCE_POLICY,
                _PAPER_GENERALIZATION_BATCH_B_PRIMITIVE_FIT,
                _PAPER_GENERALIZATION_BATCH_C_SEARCH,
                _PAPER_GENERALIZATION_BATCH_D_POSTPROCESS,
                _PAPER_GENERALIZATION_BATCH_E_PACKAGE_BOUNDARY,
            ],
            "implemented_output_contract_scope": [
                _PAPER_CHANGED_DECOMPOSITION_OUTPUT_CONTRACT,
                _PAPER_PACKAGE_ADAPTER_CONTRACT,
                _PAPER_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY,
                _PAPER_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN,
                _PAPER_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX,
                _PAPER_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT,
                _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_DRY_RUN_CONTRACT,
                _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_VALIDATION_CONTRACT,
                _PAPER_MAPPED_SUBSET_PRIMITIVESPEC_GENERATION_PREFLIGHT_CONTRACT,
            ],
            "missing_before_paper_faithful_offline": missing_before_paper_faithful,
        },
        "paper_faithful_offline_scope_audit": (
            _paper_faithful_offline_scope_audit_payload()
        ),
        "paper_fixture_breadth_completion_review": (
            _paper_fixture_breadth_completion_review_payload()
        ),
        "paper_faithful_offline_generalization_plan": (
            _paper_faithful_offline_generalization_plan_payload()
        ),
        "paper_generalization_batch_a_source_policy": (
            _paper_source_policy_generalization_payload(cases)
        ),
        "paper_generalization_batch_b_primitive_fit_engine": (
            _paper_primitive_fit_engine_generalization_payload()
        ),
        "paper_generalization_batch_c_search_engine": (
            _paper_search_engine_generalization_payload(cases)
        ),
        "paper_generalization_batch_d_postprocess_policy": (
            _paper_postprocess_policy_generalization_payload(cases)
        ),
        "paper_generalization_batch_e_package_boundary_readiness": (
            _paper_package_boundary_readiness_payload()
        ),
        "paper_offline_changed_decomposition_output_contract": (
            changed_decomposition_output_contract
        ),
        "paper_package_adapter_contract": package_adapter_contract,
        "paper_package_adapter_unsupported_primitive_policy": (
            package_adapter_unsupported_policy
        ),
        "paper_package_conversion_mapped_subset_plan": (
            package_conversion_mapped_subset_plan
        ),
        "paper_mapped_subset_conversion_candidate_matrix": (
            mapped_subset_candidate_matrix
        ),
        "paper_mapped_subset_adapter_preflight_contract": (
            mapped_subset_adapter_preflight
        ),
        "paper_mapped_subset_primitivespec_dry_run_contract": (
            mapped_subset_primitivespec_dry_run
        ),
        "paper_mapped_subset_primitivespec_validation_contract": (
            mapped_subset_primitivespec_validation
        ),
        "paper_mapped_subset_primitivespec_generation_preflight_contract": (
            mapped_subset_primitivespec_generation_preflight
        ),
        "paper_weights": PAPER_PRIMITIVE_WEIGHTS,
        "cases": cases,
    }


def _case_payload(case: _PaperToyCase) -> dict[str, object]:
    if case.unsupported_source_face_intake_audit is not None:
        return _unsupported_source_face_case_payload(case)

    preprocessing_boundary = (
        "exact_coordinate_duplicate_vertex_fixture"
        if case.duplicate_vertex_preprocessing_audit is not None
        else None
    )
    primitive_fit_audits = [
        _primitive_fit_audit_payload(
            case.mesh,
            face_group,
            case.source_face_intake_audit,
            preprocessing_boundary,
            case.executable_source_face_ids,
        )
        for face_group in case.face_groups
    ]
    payload: dict[str, object] = {
        "case_id": case.case_id,
        "description": case.description,
        "source_mesh": _source_mesh_payload(
            case.mesh,
            case.source_face_intake_audit,
            case.duplicate_vertex_preprocessing_audit,
            case.executable_source_face_ids,
        ),
        "operator_audit": _operator_audit_payload(
            case.mesh,
            case.face_groups,
            case.source_face_intake_audit,
            preprocessing_boundary,
            case.executable_source_face_ids,
        ),
        "primitive_fit_audit": primitive_fit_audits[-1],
        "primitive_fit_audits": primitive_fit_audits,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
    if case.fixture_breadth_batch is not None:
        payload["fixture_breadth_batch"] = case.fixture_breadth_batch
    if case.collapse_pair is not None:
        left, right = case.collapse_pair
        payload["collapse_cost_audit"] = _collapse_cost_payload(case.mesh, left, right)
        payload["collapse_trace"] = _collapse_trace_payload(left, right)
    if case.priority_queue_target_count is not None:
        payload["collapse_trace"] = _priority_queue_trace_payload(
            case.mesh,
            case.face_groups,
            case.priority_queue_target_count,
            allow_component_pair_edges=case.component_pair_edge_insertion,
            component_pair_excess_volume_threshold=case.component_pair_excess_volume_threshold,
            component_pair_candidate_cap=case.component_pair_candidate_cap,
            preprocessing_boundary=preprocessing_boundary,
        )
    if case.postprocess_fixture:
        payload["postprocess_audit"] = _postprocess_audit_payload(
            case.postprocess_audit_variant or "identity_nested_obb"
        )
    if case.source_face_intake_audit is not None:
        payload["mesh_intake_policy_audit"] = _source_face_intake_audit_payload(
            case.source_face_intake_audit
        )
    if case.duplicate_vertex_preprocessing_audit is not None:
        payload["preprocessing_audit"] = _preprocessing_audit_payload(
            case.duplicate_vertex_preprocessing_audit
        )
    return payload


def _unsupported_source_face_case_payload(case: _PaperToyCase) -> dict[str, object]:
    audit = case.unsupported_source_face_intake_audit
    if audit is None:
        raise ValueError("unsupported source face intake audit is required")
    payload: dict[str, object] = {
        "case_id": case.case_id,
        "description": case.description,
        "case_status": audit.case_status,
        "source_mesh": _unsupported_source_mesh_payload(audit),
        "mesh_intake_policy_audit": _unsupported_source_face_intake_audit_payload(audit),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
    if case.fixture_breadth_batch is not None:
        payload["fixture_breadth_batch"] = case.fixture_breadth_batch
    return payload


def _source_mesh_payload(
    mesh: TriangleMesh,
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None,
    duplicate_vertex_preprocessing_audit: _DuplicateVertexPreprocessingAudit | None = None,
    executable_source_face_ids: tuple[int, ...] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "fixture_scope": "synthetic_toy_mesh",
        "face_arity_policy": "triangle_only_fixture",
        "vertex_count": int(len(mesh.points)),
        "face_count": mesh.face_count,
        "source_face_remap": "identity",
        "connected_component_count": _connected_component_count(mesh),
        "duplicate_vertex_preprocessing": "not_applied_fixture_has_unique_vertices",
    }
    if duplicate_vertex_preprocessing_audit is not None:
        audit = duplicate_vertex_preprocessing_audit
        payload.update(
            {
                "duplicate_vertex_preprocessing": (
                    "exact_coordinate_deduplication_for_fixture"
                ),
                "preprocessed_input_vertex_count": len(audit.input_points),
                "deduplicated_vertex_count": len(audit.deduplicated_points),
                "source_face_remap": (
                    "duplicate_vertex_preprocessing_face_id_preserving"
                ),
                "preprocessing_source_face_remap": (
                    _duplicate_vertex_source_face_remap(audit)
                ),
            }
        )
    if executable_source_face_ids is not None:
        payload["executable_source_face_ids"] = [
            int(source_face_id) for source_face_id in executable_source_face_ids
        ]
    if source_face_intake_audit is None:
        return payload

    payload.update(
        {
            "face_arity_policy": source_face_intake_audit.face_arity_policy,
            "source_face_count": len(source_face_intake_audit.source_face_arities),
            "source_face_arities": list(source_face_intake_audit.source_face_arities),
            "triangulated_face_count": mesh.face_count,
            "executable_triangle_face_count": mesh.face_count,
            "executable_triangle_faces": [
                [int(index) for index in mesh.faces[face_id]]
                for face_id in range(mesh.face_count)
            ],
            "source_face_remap": _source_face_remap_payload(
                source_face_intake_audit.source_face_remap
            ),
            "operator_ownership_policy": (
                source_face_intake_audit.operator_ownership_policy
            ),
            "source_face_preconditions": _source_face_preconditions(),
        }
    )
    return payload


def _unsupported_source_mesh_payload(
    audit: _UnsupportedSourceFaceIntakeAudit,
) -> dict[str, object]:
    return {
        "fixture_scope": "synthetic_unsupported_source_face_fixture",
        "face_arity_policy": "reject_unsupported_concave_polygon",
        "vertex_count": len(audit.source_vertex_ids),
        "face_count": 0,
        "source_face_count": 1,
        "source_face_arities": [int(audit.source_face_arity)],
        "source_face_remap": [],
        "triangulated_face_count": 0,
        "executable_triangle_face_count": 0,
        "executable_triangle_faces": [],
        "duplicate_vertex_preprocessing": "not_applied_unsupported_intake_fixture",
        "source_face_preconditions": [
            "planar",
            "concave",
            "non_degenerate",
            "consistently_wound",
        ],
    }


def _duplicate_vertex_source_face_remap(
    audit: _DuplicateVertexPreprocessingAudit,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_face_id, input_face in enumerate(audit.input_faces):
        deduplicated_face = tuple(
            audit.original_to_deduplicated_vertex_ids[vertex_id]
            for vertex_id in input_face
        )
        face_preserved = len(set(deduplicated_face)) == len(deduplicated_face)
        rows.append(
            {
                "source_face_id": int(source_face_id),
                "input_vertex_ids": [int(vertex_id) for vertex_id in input_face],
                "deduplicated_vertex_ids": [
                    int(vertex_id) for vertex_id in deduplicated_face
                ],
                "face_preserved": face_preserved,
                "drop_reason": None if face_preserved else "degenerate_after_deduplication",
            }
        )
    return rows


def _executable_deduplicated_faces(
    audit: _DuplicateVertexPreprocessingAudit,
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        tuple(int(vertex_id) for vertex_id in face)
        for face in audit.deduplicated_faces
        if len(set(face)) == len(face)
    )


def _preprocessing_audit_payload(
    audit: _DuplicateVertexPreprocessingAudit,
) -> dict[str, object]:
    source_face_remap = _duplicate_vertex_source_face_remap(audit)
    retained_source_face_ids = [
        int(row["source_face_id"]) for row in source_face_remap if row["face_preserved"]
    ]
    dropped_source_face_ids = [
        int(row["source_face_id"]) for row in source_face_remap if not row["face_preserved"]
    ]
    input_mesh = TriangleMesh(
        points=np.asarray(audit.input_points, dtype=np.float64),
        faces=np.asarray(audit.input_faces, dtype=np.int64),
    )
    executable_faces = _executable_deduplicated_faces(audit)
    deduplicated_mesh = TriangleMesh(
        points=np.asarray(audit.deduplicated_points, dtype=np.float64),
        faces=np.asarray(executable_faces, dtype=np.int64),
    )
    return {
        "audit_scope": "duplicate_vertex_preprocessing_fixture",
        "preprocessing_policy": "exact_coordinate_deduplication_for_fixture",
        "distance_tolerance": float(audit.distance_tolerance),
        "input_vertex_count": len(audit.input_points),
        "deduplicated_vertex_count": len(audit.deduplicated_points),
        "duplicate_cluster_count": len(audit.duplicate_clusters),
        "duplicate_clusters": [
            [int(vertex_id) for vertex_id in cluster]
            for cluster in audit.duplicate_clusters
        ],
        "original_to_deduplicated_vertex_ids": [
            int(vertex_id) for vertex_id in audit.original_to_deduplicated_vertex_ids
        ],
        "input_faces": [
            [int(vertex_id) for vertex_id in face] for face in audit.input_faces
        ],
        "deduplicated_faces": [
            [int(vertex_id) for vertex_id in face] for face in audit.deduplicated_faces
        ],
        "executable_deduplicated_faces": [
            [int(vertex_id) for vertex_id in face] for face in executable_faces
        ],
        "preprocessing_source_face_remap": source_face_remap,
        "retained_source_face_ids": retained_source_face_ids,
        "dropped_source_face_ids": dropped_source_face_ids,
        "connected_component_count_before": _connected_component_count(input_mesh),
        "connected_component_count_after": _connected_component_count(deduplicated_mesh),
        "topology_changed": True,
        "degenerate_face_dropped_count": len(dropped_source_face_ids),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _operator_audit_payload(
    mesh: TriangleMesh,
    face_groups: tuple[frozenset[int], ...],
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None,
    preprocessing_boundary: str | None = None,
    executable_source_face_ids: tuple[int, ...] | None = None,
) -> dict[str, object]:
    merged_group = face_groups[-1]
    merged_operator = _group_operator(mesh, merged_group)
    payload: dict[str, object] = {
        "operator": "area_weighted_normal_plus_tangent_outer_product",
        "epsilon": PAPER_Q_EPSILON,
        "face_scope": "triangle_only",
        "faces": [
            _face_operator_payload(
                mesh,
                face_id,
                (
                    executable_source_face_ids[face_id]
                    if executable_source_face_ids is not None
                    else None
                ),
            )
            for face_id in range(mesh.face_count)
        ],
        "merged_group": _group_operator_payload(
            merged_operator,
            merged_group,
            source_face_intake_audit,
            executable_source_face_ids,
        ),
    }
    if source_face_intake_audit is not None:
        payload["face_scope"] = "triangle_subfaces_from_source_face"
        payload["source_face_operator_aggregates"] = _source_face_operator_aggregates(
            mesh,
            source_face_intake_audit,
        )
    if preprocessing_boundary is not None:
        payload["preprocessing_boundary"] = preprocessing_boundary
    if executable_source_face_ids is not None:
        payload["preprocessing_degeneracy_labels"] = [
            "dropped_degenerate_faces_after_preprocessing"
        ]
    return payload


def _face_operator_payload(
    mesh: TriangleMesh,
    face_id: int,
    source_face_id: int | None = None,
) -> dict[str, object]:
    area, normal, tangent, operator = _face_operator_terms(mesh, face_id)
    payload: dict[str, object] = {
        "face_id": int(face_id),
        "area": area,
        "normal": _vector(normal),
        "tangent": _vector(tangent),
        "q_matrix": _matrix(operator),
        "degeneracy_labels": _operator_degeneracy_labels(operator),
    }
    if source_face_id is not None:
        payload["source_face_id"] = int(source_face_id)
    return payload


def _source_face_ids_for_generated_group(
    face_group: frozenset[int],
    source_face_intake_audit: _SourceFaceIntakeAudit | None,
) -> list[int]:
    if source_face_intake_audit is None:
        return []
    return [
        int(remap.source_face_id)
        for remap in source_face_intake_audit.source_face_remap
        if set(remap.generated_triangle_face_ids).issubset(face_group)
    ]


def _group_operator_payload(
    operator: NDArray[np.float64],
    face_group: frozenset[int],
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None,
    executable_source_face_ids: tuple[int, ...] | None = None,
) -> dict[str, object]:
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    order = np.argsort(eigenvalues)[::-1]
    sorted_values = eigenvalues[order]
    sorted_vectors = eigenvectors[:, order]
    if np.linalg.det(sorted_vectors) < 0:
        sorted_vectors[:, -1] *= -1.0
    generated_triangle_face_ids = sorted(int(face_id) for face_id in face_group)
    source_face_ids = _source_face_ids_for_generated_group(face_group, source_face_intake_audit)
    if executable_source_face_ids is not None:
        source_face_ids = [
            int(executable_source_face_ids[int(face_id)])
            for face_id in sorted(face_group)
        ]
    payload: dict[str, object] = {
        "source_faces": (
            source_face_ids
            if source_face_intake_audit is not None
            or executable_source_face_ids is not None
            else generated_triangle_face_ids
        ),
        "q_matrix": _matrix(operator),
        "eigenvalues": [float(value) for value in sorted_values],
        "eigenvectors": _matrix(sorted_vectors),
        "eigenvector_matrix_layout": "columns_are_eigenvectors",
        "degeneracy_labels": _operator_degeneracy_labels(operator),
    }
    if source_face_intake_audit is not None:
        payload["generated_triangle_face_ids"] = generated_triangle_face_ids
        payload["source_face_ids"] = source_face_ids
    return payload


def _primitive_fit_audit_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
    source_face_intake_audit: _SourceFaceIntakeAudit | None = None,
    preprocessing_boundary: str | None = None,
    executable_source_face_ids: tuple[int, ...] | None = None,
) -> dict[str, object]:
    rows = _paper_primitive_fit_candidate_rows(mesh, face_group)
    selected = min(rows, key=lambda row: (float(row["weighted_volume"]), row["candidate_order"]))
    generated_triangle_face_ids = sorted(int(face_id) for face_id in face_group)
    source_face_ids = _source_face_ids_for_generated_group(face_group, source_face_intake_audit)
    if executable_source_face_ids is not None:
        source_face_ids = [
            int(executable_source_face_ids[int(face_id)])
            for face_id in sorted(face_group)
        ]
    payload: dict[str, object] = {
        "source_faces": (
            source_face_ids
            if source_face_intake_audit is not None
            or executable_source_face_ids is not None
            else generated_triangle_face_ids
        ),
        "candidate_scope": "paper_primitive_set_offline_audit_slice",
        "selection_rule": "min_paper_weighted_volume_for_fixture_audit",
        "missing_paper_primitives": [],
        "candidates": rows,
        "selected": selected,
    }
    if source_face_intake_audit is not None or executable_source_face_ids is not None:
        payload["generated_triangle_face_ids"] = generated_triangle_face_ids
        payload["source_face_ids"] = source_face_ids
    if preprocessing_boundary is not None:
        payload["preprocessing_boundary"] = preprocessing_boundary
    return payload


def _paper_primitive_fit_candidate_rows(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> list[dict[str, object]]:
    obb_row = _paper_obb_candidate_payload(mesh, face_group)
    return [
        obb_row,
        _paper_sphere_candidate_payload(mesh, face_group, obb_row),
        _paper_capsule_candidate_payload(mesh, face_group),
        _flat_capped_cylinder_candidate_payload(mesh, face_group),
        _frustum_candidate_payload(mesh, face_group),
        _trapezoidal_prism_candidate_payload(mesh, face_group),
    ]


def _paper_obb_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    local = points @ axes
    lower = local.min(axis=0)
    upper = local.max(axis=0)
    center_local = (lower + upper) * 0.5
    half_extents = np.maximum(
        (upper - lower) * 0.5,
        PAPER_PRIMITIVE_MIN_DIMENSION,
    )
    center = axes @ center_local
    volume = float(8.0 * np.prod(half_extents))
    contains = bool(np.all(np.abs(local - center_local) <= half_extents + 1e-8))
    return _offline_paper_candidate_payload(
        paper_primitive="oriented_bounding_box",
        current_implementation_kind="offline_paper_oriented_bounding_box_fit",
        fit_model="paper_operator_eigenbasis_projected_bounds",
        axis_selection_policy="paper_q_eigenbasis",
        center=center,
        axes=axes,
        dimensions={
            "lower_bounds": _vector(lower),
            "upper_bounds": _vector(upper),
            "paper_center_local": _vector(center_local),
            "paper_center_world": _vector(center),
            "half_extents": _vector(half_extents),
            "axis_order_policy": "descending_abs_q_eigenvalue",
            "volume_formula": "8*hx*hy*hz",
        },
        volume=volume,
        contains_assigned_points=contains,
        newton_runtime_kind="box",
        primitive_parameter_lower_clamp=PAPER_PRIMITIVE_MIN_DIMENSION,
    )


def _paper_sphere_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
    obb_row: dict[str, object],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    center = np.asarray(obb_row["center"], dtype=np.float64)
    axes = np.asarray(obb_row["axes"], dtype=np.float64).T
    distances = np.linalg.norm(points - center, axis=1)
    unclamped_radius = float(distances.max(initial=0.0))
    radius = max(unclamped_radius, PAPER_PRIMITIVE_MIN_DIMENSION)
    volume = float((4.0 / 3.0) * pi * radius**3)
    contains = bool(np.all(distances <= radius + 1e-8))
    centroid = points.mean(axis=0)
    center_centroid_distance = float(np.linalg.norm(center - centroid))
    return _offline_paper_candidate_payload(
        paper_primitive="sphere",
        current_implementation_kind="offline_paper_sphere_fit",
        fit_model="paper_obb_center_max_distance_radius",
        axis_selection_policy="paper_obb_center",
        center=center,
        axes=axes,
        dimensions={
            "radius": radius,
            "center_source": "paper_obb_center",
            "radius_source": "max_distance_from_obb_center_clamped",
            "unclamped_radius": unclamped_radius,
            "center_centroid_distance": center_centroid_distance,
            "center_differs_from_point_centroid": center_centroid_distance > 1e-3,
            "fixture_center_relation": (
                "differs_from_point_centroid"
                if center_centroid_distance > 1e-3
                else "matches_point_centroid"
            ),
            "volume_formula": "4/3*pi*r^3",
        },
        volume=volume,
        contains_assigned_points=contains,
        newton_runtime_kind="sphere",
        primitive_parameter_lower_clamp=PAPER_PRIMITIVE_MIN_DIMENSION,
    )


def _candidate_payload(candidate) -> dict[str, object]:
    paper_primitive = _PAPER_PRIMITIVE_NAMES[candidate.primitive_type]
    weight = PAPER_PRIMITIVE_WEIGHTS[paper_primitive]
    return {
        "candidate_order": _AUDITED_PAPER_PRIMITIVES.index(paper_primitive),
        "paper_primitive": paper_primitive,
        "current_implementation_kind": candidate.primitive_type,
        "implementation_status": _implementation_status(candidate.primitive_type),
        "fit_model": _fit_model(candidate.primitive_type),
        "axis_selection_policy": _axis_selection_policy(candidate.primitive_type),
        "primitive_parameter_lower_clamp": MIN_DIMENSION,
        "newton_runtime_kind": _NEWTON_RUNTIME_KIND[candidate.primitive_type],
        "center": list(candidate.center),
        "axes": [list(axis) for axis in candidate.axes],
        "dimensions": candidate.dimensions,
        "volume": float(candidate.volume),
        "paper_weight": float(weight),
        "weighted_volume": float(candidate.volume * weight),
        "contains_assigned_points": bool(candidate.contains_assigned_points),
    }


def _offline_paper_candidate_payload(
    *,
    paper_primitive: str,
    current_implementation_kind: str,
    fit_model: str,
    axis_selection_policy: str,
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
    dimensions: dict[str, object],
    volume: float,
    contains_assigned_points: bool,
    newton_runtime_kind: str = "offline_only_unmapped",
    primitive_parameter_lower_clamp: float = MIN_DIMENSION,
) -> dict[str, object]:
    weight = PAPER_PRIMITIVE_WEIGHTS[paper_primitive]
    return {
        "candidate_order": _AUDITED_PAPER_PRIMITIVES.index(paper_primitive),
        "paper_primitive": paper_primitive,
        "current_implementation_kind": current_implementation_kind,
        "implementation_status": "paper_shaped_offline_fit_audit",
        "fit_model": fit_model,
        "paper_primitive_variant": paper_primitive,
        "axis_selection_policy": axis_selection_policy,
        "primitive_parameter_lower_clamp": primitive_parameter_lower_clamp,
        "containment_tolerance": 1e-8,
        "fit_failure_reason": None if contains_assigned_points else "assigned_points_not_contained",
        "newton_runtime_kind": newton_runtime_kind,
        "center": _vector(center),
        "axes": _matrix(axes.T),
        "axis_matrix_layout": "rows_are_axes",
        "dimensions": dimensions,
        "volume": float(volume),
        "paper_weight": float(weight),
        "weighted_volume": float(volume * weight),
        "contains_assigned_points": bool(contains_assigned_points),
    }


def _frustum_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    center, local = _obb_center_and_local(points, axes)
    relative = local - ((local.min(axis=0) + local.max(axis=0)) * 0.5)
    axis_candidates = _flat_cylinder_axis_candidates(points, center, axes, relative)
    selected_axis = min(
        axis_candidates,
        key=lambda row: (float(row["flat_cylinder_volume"]), int(row["axis_index"])),
    )
    axis_index = int(selected_axis["axis_index"])
    projection = relative[:, axis_index]
    raw_projection_min = float(projection.min())
    raw_projection_max = float(projection.max())
    height = max(raw_projection_max - raw_projection_min, MIN_DIMENSION * 2.0)
    half_height = height * 0.5
    center_projection = (raw_projection_min + raw_projection_max) * 0.5
    center = center + axes[:, axis_index] * center_projection
    radial_axes = [index for index in range(3) if index != axis_index]
    radial_distances = np.linalg.norm(relative[:, radial_axes], axis=1)
    clamped_projection_min = center_projection - half_height
    blend = np.clip((projection - clamped_projection_min) / height, 0.0, 1.0)
    bottom_radius, top_radius = _fit_linear_extent_pair(radial_distances, blend)
    volume = float(
        (pi * height / 3.0)
        * (top_radius**2 + top_radius * bottom_radius + bottom_radius**2)
    )
    axis = axes[:, axis_index]
    contains = _frustum_contains(points, center, axis, half_height, bottom_radius, top_radius)
    bottom_center = center - axis * half_height
    top_center = center + axis * half_height
    return _offline_paper_candidate_payload(
        paper_primitive="frustum",
        current_implementation_kind="offline_frustum_fit_audit",
        fit_model="paper_frustum_axis_from_min_cost_flat_cylinder",
        axis_selection_policy="min_volume_flat_cylinder_axis",
        center=center,
        axes=axes,
        dimensions={
            "axis_index": axis_index,
            "selected_axis_index": axis_index,
            "axis_selection_policy": "min_volume_flat_cylinder_axis",
            "height": height,
            "half_height": half_height,
            "top_radius": top_radius,
            "bottom_radius": bottom_radius,
            "top_center": _vector(top_center),
            "bottom_center": _vector(bottom_center),
            "volume_formula": "pi*h/3*(rt^2 + rt*rb + rb^2)",
            "flat_cylinder_axis_candidates": axis_candidates,
        },
        volume=volume,
        contains_assigned_points=contains,
    )


def _paper_capsule_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    obb_center, _ = _obb_center_and_local(points, axes)
    axis_candidates = _paper_capsule_axis_candidates(points, obb_center, axes)
    selected = min(
        axis_candidates,
        key=lambda row: (float(row["capsule_volume"]), int(row["axis_index"])),
    )
    axis_index = int(selected["axis_index"])
    axis = axes[:, axis_index]
    radius = float(selected["radius"])
    half_height = float(selected["half_height"])
    height = float(selected["height"])
    capsule_center = np.asarray(selected["center"], dtype=np.float64)
    volume = float(selected["capsule_volume"])
    contains = _capsule_contains(points, axis, capsule_center, half_height, radius)
    return _offline_paper_candidate_payload(
        paper_primitive="capsule",
        current_implementation_kind="offline_paper_capsule_fit_audit",
        fit_model="paper_capsule_min_volume_over_axes_with_spherical_cap_height",
        axis_selection_policy="min_volume_capsule_axis",
        center=capsule_center,
        axes=axes,
        dimensions={
            "axis_index": axis_index,
            "selected_axis_index": axis_index,
            "axis_selection_policy": "min_volume_capsule_axis",
            "radius": radius,
            "height": height,
            "half_height": half_height,
            "segment_start": _vector(capsule_center - axis * half_height),
            "segment_end": _vector(capsule_center + axis * half_height),
            "volume_formula": "pi*r^2*h + 4/3*pi*r^3",
            "paper_capsule_axis_candidates": axis_candidates,
        },
        volume=volume,
        contains_assigned_points=contains,
        newton_runtime_kind="capsule",
    )


def _flat_capped_cylinder_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    center, local = _obb_center_and_local(points, axes)
    relative = local - ((local.min(axis=0) + local.max(axis=0)) * 0.5)
    axis_candidates = _flat_cylinder_axis_candidates(points, center, axes, relative)
    selected = min(
        axis_candidates,
        key=lambda row: (float(row["flat_cylinder_volume"]), int(row["axis_index"])),
    )
    axis_index = int(selected["axis_index"])
    axis = axes[:, axis_index]
    half_height = float(selected["half_height"])
    radius = float(selected["radius"])
    cylinder_center = np.asarray(selected["center"], dtype=np.float64)
    height = float(selected["height"])
    bottom_center = cylinder_center - axis * half_height
    top_center = cylinder_center + axis * half_height
    volume = float(selected["flat_cylinder_volume"])
    contains = _flat_cylinder_contains(points, cylinder_center, axis, half_height, radius)
    return _offline_paper_candidate_payload(
        paper_primitive="capped_cylinder",
        current_implementation_kind="offline_flat_capped_cylinder_fit_audit",
        fit_model="paper_flat_capped_cylinder_min_volume_over_axes",
        axis_selection_policy="min_volume_flat_cylinder_axis",
        center=cylinder_center,
        axes=axes,
        dimensions={
            "axis_index": axis_index,
            "selected_axis_index": axis_index,
            "axis_selection_policy": "min_volume_flat_cylinder_axis",
            "cap_model": "flat_caps",
            "radius": radius,
            "height": height,
            "half_height": half_height,
            "top_center": _vector(top_center),
            "bottom_center": _vector(bottom_center),
            "volume_formula": "pi*r^2*h",
            "flat_cylinder_axis_candidates": axis_candidates,
        },
        volume=volume,
        contains_assigned_points=contains,
    )
def _trapezoidal_prism_candidate_payload(
    mesh: TriangleMesh,
    face_group: frozenset[int],
) -> dict[str, object]:
    points = _assigned_points(mesh, face_group)
    axes = _candidate_axes(mesh, face_group)
    center, _ = _obb_center_and_local(points, axes)
    axis_orders = (
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2),
        (1, 2, 0),
        (2, 0, 1),
        (2, 1, 0),
    )
    candidates = [
        _trapezoidal_prism_for_axis_order(points, center, axes, axis_order)
        for axis_order in axis_orders
    ]
    containing_candidates = [row for row in candidates if bool(row["contains_assigned_points"])]
    selected_pool = containing_candidates if containing_candidates else candidates
    selected = min(selected_pool, key=lambda row: (float(row["volume"]), row["axis_order"]))
    ordered_axes = axes[:, selected["axis_order"]]
    contains = _trapezoidal_prism_contains(
        points,
        center,
        ordered_axes,
        float(selected["h_x"]),
        float(selected["h_y"]),
        float(selected["h_zb"]),
        float(selected["h_zt"]),
    )
    return _offline_paper_candidate_payload(
        paper_primitive="trapezoidal_prism",
        current_implementation_kind="offline_trapezoidal_prism_fit_audit",
        fit_model="paper_isosceles_trapezoidal_prism_six_axis_orders",
        axis_selection_policy="min_volume_over_six_axis_orders",
        center=center,
        axes=ordered_axes,
        dimensions={
            "axis_order": [int(index) for index in selected["axis_order"]],
            "axis_order_attempt_count": len(axis_orders),
            "axis_order_attempts": [
                {
                    "axis_order": [int(index) for index in row["axis_order"]],
                    "h_x": float(row["h_x"]),
                    "h_y": float(row["h_y"]),
                    "h_zt": float(row["h_zt"]),
                    "h_zb": float(row["h_zb"]),
                    "volume": float(row["volume"]),
                    "contains_assigned_points": bool(row["contains_assigned_points"]),
                }
                for row in candidates
            ],
            "h_x": float(selected["h_x"]),
            "h_y": float(selected["h_y"]),
            "h_zt": float(selected["h_zt"]),
            "h_zb": float(selected["h_zb"]),
            "volume_formula": "4*h_x*h_y*(h_zt + h_zb)",
        },
        volume=float(selected["volume"]),
        contains_assigned_points=contains,
    )


def _trapezoidal_prism_for_axis_order(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
    axis_order: tuple[int, int, int],
) -> dict[str, object]:
    ordered_axes = axes[:, axis_order]
    local = (points - center) @ ordered_axes
    h_x = max(float(np.abs(local[:, 0]).max(initial=0.0)), MIN_DIMENSION)
    h_y = max(float(np.abs(local[:, 1]).max(initial=0.0)), MIN_DIMENSION)
    z_abs = np.abs(local[:, 2])
    blend = np.clip((local[:, 1] + h_y) / (2.0 * h_y), 0.0, 1.0)
    h_zb, h_zt = _fit_linear_extent_pair(z_abs, blend)
    volume = float(4.0 * h_x * h_y * (h_zt + h_zb))
    contains = _trapezoidal_prism_contains(points, center, ordered_axes, h_x, h_y, h_zb, h_zt)
    return {
        "axis_order": axis_order,
        "h_x": h_x,
        "h_y": h_y,
        "h_zt": h_zt,
        "h_zb": h_zb,
        "volume": volume,
        "contains_assigned_points": contains,
    }


def _fit_linear_extent_pair(
    values: NDArray[np.float64],
    blend: NDArray[np.float64],
) -> tuple[float, float]:
    bottom = MIN_DIMENSION
    top = MIN_DIMENSION
    for value, t in zip(values, blend):
        value = max(float(value), MIN_DIMENSION)
        t = float(np.clip(t, 0.0, 1.0))
        if value <= ((1.0 - t) * bottom + t * top) + 1e-12:
            continue
        if t <= 0.5:
            bottom = max(bottom, (value - t * top) / max(1.0 - t, MIN_DIMENSION))
        else:
            top = max(top, (value - (1.0 - t) * bottom) / max(t, MIN_DIMENSION))

    bottom_fixed = bottom
    top_from_bottom = _required_top_extent(values, blend, bottom_fixed)
    top_fixed = top
    bottom_from_top = _required_bottom_extent(values, blend, top_fixed)
    if bottom_fixed + top_from_bottom <= bottom_from_top + top_fixed:
        return _containment_adjusted_linear_extent_pair(values, blend, bottom_fixed, top_from_bottom)
    return _containment_adjusted_linear_extent_pair(values, blend, bottom_from_top, top_fixed)


def _required_top_extent(
    values: NDArray[np.float64],
    blend: NDArray[np.float64],
    bottom: float,
) -> float:
    top = MIN_DIMENSION
    for value, t in zip(values, blend):
        value = max(float(value), MIN_DIMENSION)
        t = float(np.clip(t, 0.0, 1.0))
        if t <= MIN_DIMENSION:
            top = max(top, value)
            continue
        top = max(top, (value - (1.0 - t) * bottom) / t)
    return float(max(top, MIN_DIMENSION))


def _required_bottom_extent(
    values: NDArray[np.float64],
    blend: NDArray[np.float64],
    top: float,
) -> float:
    bottom = MIN_DIMENSION
    for value, t in zip(values, blend):
        value = max(float(value), MIN_DIMENSION)
        t = float(np.clip(t, 0.0, 1.0))
        if (1.0 - t) <= MIN_DIMENSION:
            bottom = max(bottom, value)
            continue
        bottom = max(bottom, (value - t * top) / (1.0 - t))
    return float(max(bottom, MIN_DIMENSION))


def _containment_adjusted_linear_extent_pair(
    values: NDArray[np.float64],
    blend: NDArray[np.float64],
    bottom: float,
    top: float,
) -> tuple[float, float]:
    for _ in range(2):
        for value, t in zip(values, blend):
            value = max(float(value), MIN_DIMENSION)
            t = float(np.clip(t, 0.0, 1.0))
            allowed = (1.0 - t) * bottom + t * top
            if value <= allowed + 1e-12:
                continue
            gap = value - allowed
            if t <= 0.5:
                bottom += gap / max(1.0 - t, MIN_DIMENSION)
            else:
                top += gap / max(t, MIN_DIMENSION)
    return float(max(bottom, MIN_DIMENSION)), float(max(top, MIN_DIMENSION))


def _flat_cylinder_contains(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axis: NDArray[np.float64],
    half_height: float,
    radius: float,
) -> bool:
    relative = points - center
    projected = relative @ axis
    radial_vectors = relative - np.outer(projected, axis)
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    return bool(
        np.all(np.abs(projected) <= half_height + 1e-8)
        and np.all(radial_distances <= radius + 1e-8)
    )


def _flat_cylinder_axis_candidates(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
    relative: NDArray[np.float64],
) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for axis_index in range(3):
        projection = relative[:, axis_index]
        projection_min = float(projection.min())
        projection_max = float(projection.max())
        height = max(projection_max - projection_min, MIN_DIMENSION * 2.0)
        half_height = height * 0.5
        axis = axes[:, axis_index]
        axis_center = center + axis * ((projection_min + projection_max) * 0.5)
        radial_axes = [index for index in range(3) if index != axis_index]
        radial_distances = np.linalg.norm(relative[:, radial_axes], axis=1)
        radius = max(float(radial_distances.max(initial=0.0)), MIN_DIMENSION)
        volume = float(pi * radius**2 * height)
        candidates.append(
            {
                "axis_index": axis_index,
                "center": _vector(axis_center),
                "radius": radius,
                "height": height,
                "half_height": half_height,
                "flat_cylinder_volume": volume,
                "contains_assigned_points": _flat_cylinder_contains(
                    points,
                    axis_center,
                    axis,
                    half_height,
                    radius,
                ),
            }
        )
    return candidates


def _paper_capsule_axis_candidates(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
) -> list[dict[str, object]]:
    relative = points - center
    candidates: list[dict[str, object]] = []
    for axis_index in range(3):
        axis = axes[:, axis_index]
        projected = relative @ axis
        axial_offsets = np.outer(projected, axis)
        radial_vectors = relative - axial_offsets
        radial_distances = np.linalg.norm(radial_vectors, axis=1)
        radius = max(float(radial_distances.max(initial=0.0)), MIN_DIMENSION)
        cap_allowance = np.sqrt(np.maximum(radius**2 - radial_distances**2, 0.0))
        cap_adjusted = projected - cap_allowance
        segment_min = float(cap_adjusted.min())
        segment_max = float(cap_adjusted.max())
        height = max(segment_max - segment_min, MIN_DIMENSION * 2.0)
        half_height = height * 0.5
        capsule_center = center + axis * ((segment_min + segment_max) * 0.5)
        volume = float(pi * radius**2 * height + (4.0 / 3.0) * pi * radius**3)
        candidates.append(
            {
                "axis_index": axis_index,
                "center": _vector(capsule_center),
                "radius": radius,
                "height": height,
                "half_height": half_height,
                "paper_height_min": segment_min,
                "paper_height_max": segment_max,
                "capsule_volume": volume,
                "contains_assigned_points": _capsule_contains(
                    points,
                    axis,
                    capsule_center,
                    half_height,
                    radius,
                ),
            }
        )
    return candidates


def _capsule_contains(
    points: NDArray[np.float64],
    axis: NDArray[np.float64],
    center: NDArray[np.float64],
    half_height: float,
    radius: float,
) -> bool:
    relative = points - center
    projected = relative @ axis
    clamped = np.clip(projected, -half_height, half_height)
    closest = center + np.outer(clamped, axis)
    distances = np.linalg.norm(points - closest, axis=1)
    return bool(np.all(distances <= radius + 1e-8))


def _frustum_contains(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axis: NDArray[np.float64],
    half_height: float,
    bottom_radius: float,
    top_radius: float,
) -> bool:
    relative = points - center
    projected = relative @ axis
    radial_vectors = relative - np.outer(projected, axis)
    radial_distances = np.linalg.norm(radial_vectors, axis=1)
    height = max(half_height * 2.0, MIN_DIMENSION)
    blend = np.clip((projected + half_height) / height, 0.0, 1.0)
    allowed = (1.0 - blend) * bottom_radius + blend * top_radius
    return bool(
        np.all(projected >= -half_height - 1e-8)
        and np.all(projected <= half_height + 1e-8)
        and np.all(radial_distances <= allowed + 1e-8)
    )


def _trapezoidal_prism_contains(
    points: NDArray[np.float64],
    center: NDArray[np.float64],
    axes: NDArray[np.float64],
    h_x: float,
    h_y: float,
    h_zb: float,
    h_zt: float,
) -> bool:
    local = (points - center) @ axes
    blend = np.clip((local[:, 1] + h_y) / (2.0 * h_y), 0.0, 1.0)
    allowed_z = (1.0 - blend) * h_zb + blend * h_zt
    return bool(
        np.all(np.abs(local[:, 0]) <= h_x + 1e-8)
        and np.all(np.abs(local[:, 1]) <= h_y + 1e-8)
        and np.all(np.abs(local[:, 2]) <= allowed_z + 1e-8)
    )


def _postprocess_audit_payload(variant: str = "identity_nested_obb") -> dict[str, object]:
    if variant == "identity_nested_obb":
        return _nested_obb_postprocess_audit_payload(
            axes=np.eye(3, dtype=np.float64),
            axis_policy="shared_identity_axes",
            fixture_variant="identity_nested_obb",
            rotation_degrees_about_z=0.0,
        )
    if variant == "rotated_nested_obb":
        angle = np.deg2rad(30.0)
        axes = np.array(
            [
                [np.cos(angle), -np.sin(angle), 0.0],
                [np.sin(angle), np.cos(angle), 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )
        return _nested_obb_postprocess_audit_payload(
            axes=axes,
            axis_policy="shared_rotated_axes",
            fixture_variant="rotated_nested_obb",
            rotation_degrees_about_z=30.0,
        )
    if variant == "cross_type_unsupported_boundary":
        return _cross_type_unsupported_postprocess_audit_payload()
    raise ValueError(f"unsupported postprocess audit variant: {variant}")


def _nested_obb_postprocess_audit_payload(
    *,
    axes: NDArray[np.float64],
    axis_policy: str,
    fixture_variant: str,
    rotation_degrees_about_z: float,
) -> dict[str, object]:
    outer = _postprocess_obb_row(
        primitive_id=0,
        center=np.array([0.0, 0.0, 0.0], dtype=np.float64),
        half_extents=np.array([1.0, 1.0, 1.0], dtype=np.float64),
        axes=axes,
    )
    inner = _postprocess_obb_row(
        primitive_id=1,
        center=np.array([0.0, 0.0, 0.0], dtype=np.float64),
        half_extents=np.array([0.25, 0.25, 0.25], dtype=np.float64),
        axes=axes,
    )
    inner_corners = _obb_corners(
        center=np.asarray(inner["center"], dtype=np.float64),
        half_extents=np.asarray(inner["half_extents"], dtype=np.float64),
        axes=np.asarray(inner["axes"], dtype=np.float64),
    )
    containment_passed = _obb_contains_points(
        center=np.asarray(outer["center"], dtype=np.float64),
        half_extents=np.asarray(outer["half_extents"], dtype=np.float64),
        axes=np.asarray(outer["axes"], dtype=np.float64),
        points=inner_corners,
    )
    cull_records = [
        {
            "culled_primitive_id": 1,
            "enclosing_primitive_id": 0,
            "cull_reason": "primitive_enclosed_by_larger_primitive",
            "containment_passed": containment_passed,
            "tested_corner_count": int(len(inner_corners)),
        }
    ]
    return {
        "audit_scope": "enclosed_primitive_culling_fixture",
        "fixture_variant": fixture_variant,
        "postprocess_input_source": "explicit_audit_primitives_not_search_trace",
        "input_primitive_count": 2,
        "output_primitive_count": 1,
        "postprocess_policy": "remove_primitives_enclosed_by_another_primitive",
        "containment_test_type": "obb_corners_inside_obb",
        "axis_policy": axis_policy,
        "rotation_degrees_about_z": float(rotation_degrees_about_z),
        "rotated_axes_non_identity": bool(not np.allclose(axes, np.eye(3))),
        "input_primitives": [outer, inner],
        "cull_records": cull_records,
        "enclosed_primitive_ids": [1],
        "enclosing_primitive_ids": [0],
        "kept_primitive_ids": [0],
        "culled_primitive_ids": [1],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _postprocess_sphere_row(
    *,
    primitive_id: int,
    center: NDArray[np.float64],
    radius: float,
) -> dict[str, object]:
    return {
        "primitive_id": primitive_id,
        "kind": "sphere",
        "center": _vector(center),
        "radius": float(radius),
    }


def _cross_type_unsupported_postprocess_audit_payload() -> dict[str, object]:
    outer = _postprocess_obb_row(
        primitive_id=0,
        center=np.array([0.0, 0.0, 0.0], dtype=np.float64),
        half_extents=np.array([1.0, 1.0, 1.0], dtype=np.float64),
        axes=np.eye(3, dtype=np.float64),
    )
    inner = _postprocess_sphere_row(
        primitive_id=1,
        center=np.array([0.0, 0.0, 0.0], dtype=np.float64),
        radius=0.25,
    )
    return {
        "audit_scope": "enclosed_primitive_cross_type_boundary_fixture",
        "fixture_variant": "cross_type_unsupported_boundary",
        "postprocess_input_source": "explicit_audit_primitives_not_search_trace",
        "input_primitive_count": 2,
        "output_primitive_count": 2,
        "postprocess_policy": "do_not_silently_cull_unsupported_cross_type_boundary",
        "containment_test_type": "cross_type_containment_unsupported",
        "cross_type_culling_supported": False,
        "unsupported_containment_label": "cross_type_enclosure_boundary_not_supported",
        "top_level_failure_label": False,
        "input_primitives": [outer, inner],
        "cull_records": [],
        "unsupported_records": [
            {
                "candidate_primitive_id": 1,
                "enclosing_primitive_id": 0,
                "candidate_kind": "sphere",
                "enclosing_kind": "oriented_bounding_box",
                "unsupported_reason": "cross_type_containment_not_implemented_for_fixture",
            }
        ],
        "enclosed_primitive_ids": [],
        "enclosing_primitive_ids": [],
        "kept_primitive_ids": [0, 1],
        "culled_primitive_ids": [],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _source_face_intake_audit_payload(audit: _SourceFaceIntakeAudit) -> dict[str, object]:
    remap = _source_face_remap_payload(audit.source_face_remap)
    triangulated_count = sum(len(row["generated_triangle_face_ids"]) for row in remap)
    return {
        "audit_scope": "polygon_quad_source_face_intake_policy_fixture",
        "source_face_policy": "preserve_source_face_id_after_fan_triangulation",
        "triangulation_policy": "fan_from_first_vertex",
        "operator_ownership_policy": audit.operator_ownership_policy,
        "normal_policy": "triangle_normals_area_weighted_after_fan_triangulation",
        "tangent_policy": "triangle_edge_tangents_area_weighted_after_fan_triangulation",
        "source_face_count": len(audit.source_face_arities),
        "source_face_arities": list(audit.source_face_arities),
        "triangulated_face_count": triangulated_count,
        "executable_triangle_face_count": triangulated_count,
        "source_face_remap": remap,
        "source_face_preconditions": _source_face_preconditions(),
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _unsupported_source_face_intake_audit_payload(
    audit: _UnsupportedSourceFaceIntakeAudit,
) -> dict[str, object]:
    return {
        "audit_scope": "unsupported_source_face_intake_policy_fixture",
        "source_face_policy": "reject_unsupported_concave_polygon",
        "triangulation_policy": "no_triangulation_for_unsupported_concave_polygon",
        "operator_ownership_policy": "no_executable_operator_rows_for_unsupported_face",
        "source_face_count": 1,
        "source_face_arities": [int(audit.source_face_arity)],
        "source_face_id": int(audit.source_face_id),
        "source_vertex_ids": [int(vertex_id) for vertex_id in audit.source_vertex_ids],
        "generated_triangle_face_ids": [],
        "generated_triangle_vertex_ids": [],
        "triangulated_face_count": 0,
        "executable_triangle_face_count": 0,
        "failure_label": audit.failure_label,
        "top_level_failure_label": False,
        "case_status": audit.case_status,
        "rejection_reason": audit.rejection_reason,
        "source_face_preconditions": [
            "planar",
            "concave",
            "non_degenerate",
            "consistently_wound",
        ],
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }


def _source_face_remap_payload(
    remaps: tuple[_SourceFaceRemap, ...],
) -> list[dict[str, object]]:
    return [
        {
            "source_face_id": int(remap.source_face_id),
            "source_face_arity": int(remap.source_face_arity),
            "source_vertex_ids": [int(index) for index in remap.source_vertex_ids],
            "generated_triangle_face_ids": [
                int(face_id) for face_id in remap.generated_triangle_face_ids
            ],
            "generated_triangle_vertex_ids": [
                [int(index) for index in triangle]
                for triangle in remap.generated_triangle_vertex_ids
            ],
        }
        for remap in remaps
    ]


def _source_face_preconditions() -> list[str]:
    return ["planar", "convex", "non_degenerate", "consistently_wound"]


def _source_face_operator_aggregates(
    mesh: TriangleMesh,
    audit: _SourceFaceIntakeAudit,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for remap in audit.source_face_remap:
        q_matrix = np.zeros((3, 3), dtype=np.float64)
        for face_id in remap.generated_triangle_face_ids:
            q_matrix += _face_operator_terms(mesh, int(face_id))[3]
        eigen_payload = _group_operator_payload(
            q_matrix,
            frozenset(int(face_id) for face_id in remap.generated_triangle_face_ids),
        )
        rows.append(
            {
                "source_face_id": int(remap.source_face_id),
                "source_face_arity": int(remap.source_face_arity),
                "source_vertex_ids": [int(index) for index in remap.source_vertex_ids],
                "generated_triangle_face_ids": [
                    int(face_id) for face_id in remap.generated_triangle_face_ids
                ],
                "generated_triangle_vertex_ids": [
                    [int(index) for index in triangle]
                    for triangle in remap.generated_triangle_vertex_ids
                ],
                "q_matrix": _matrix(q_matrix),
                "eigenvalues": eigen_payload["eigenvalues"],
                "eigenvectors": eigen_payload["eigenvectors"],
                "eigenvector_matrix_layout": eigen_payload["eigenvector_matrix_layout"],
                "degeneracy_labels": eigen_payload["degeneracy_labels"],
            }
        )
    return rows


def _postprocess_obb_row(
    *,
    primitive_id: int,
    center: NDArray[np.float64],
    half_extents: NDArray[np.float64],
    axes: NDArray[np.float64],
) -> dict[str, object]:
    return {
        "primitive_id": primitive_id,
        "kind": "oriented_bounding_box",
        "center": _vector(center),
        "half_extents": _vector(half_extents),
        "axes": _matrix(axes),
    }


def _obb_corners(
    center: NDArray[np.float64],
    half_extents: NDArray[np.float64],
    axes: NDArray[np.float64],
) -> NDArray[np.float64]:
    signs = np.array(
        [
            [-1.0, -1.0, -1.0],
            [-1.0, -1.0, 1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [1.0, -1.0, 1.0],
            [1.0, 1.0, -1.0],
            [1.0, 1.0, 1.0],
        ],
        dtype=np.float64,
    )
    return center + (signs * half_extents) @ axes


def _obb_contains_points(
    center: NDArray[np.float64],
    half_extents: NDArray[np.float64],
    axes: NDArray[np.float64],
    points: NDArray[np.float64],
) -> bool:
    local = (points - center) @ axes.T
    return bool(np.all(np.abs(local) <= half_extents + 1e-8))


def _assigned_points(mesh: TriangleMesh, face_group: frozenset[int]) -> NDArray[np.float64]:
    point_indices = sorted(
        {
            int(point_index)
            for face_id in face_group
            for point_index in mesh.faces[int(face_id)]
        }
    )
    return np.asarray(mesh.points[point_indices], dtype=np.float64)


def _candidate_axes(mesh: TriangleMesh, face_group: frozenset[int]) -> NDArray[np.float64]:
    operator = _group_operator(mesh, face_group)
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    order = np.argsort(np.abs(eigenvalues))[::-1]
    axes = eigenvectors[:, order]
    if np.linalg.det(axes) < 0:
        axes[:, -1] *= -1.0
    return axes


def _obb_center_and_local(
    points: NDArray[np.float64],
    axes: NDArray[np.float64],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    local = points @ axes
    local_min = local.min(axis=0)
    local_max = local.max(axis=0)
    local_center = (local_min + local_max) * 0.5
    return axes @ local_center, local


def _collapse_cost_payload(
    mesh: TriangleMesh,
    left: frozenset[int],
    right: frozenset[int],
) -> dict[str, object]:
    payload = _paper_merge_cost_payload(mesh, left, right)
    payload["priority_queue_policy"] = "greedy_single_pop_fixture"
    return payload


def _paper_merge_cost_payload(
    mesh: TriangleMesh,
    left: frozenset[int],
    right: frozenset[int],
) -> dict[str, object]:
    left_audit = _primitive_fit_audit_payload(mesh, left)
    right_audit = _primitive_fit_audit_payload(mesh, right)
    merged_audit = _primitive_fit_audit_payload(mesh, frozenset(left | right))
    left_fit = left_audit["selected"]
    right_fit = right_audit["selected"]
    merged = merged_audit["selected"]
    paper_base_cost = float(merged["volume"] - (left_fit["volume"] + right_fit["volume"]))
    weighted_priority_cost = float(
        merged["weighted_volume"]
        - (left_fit["weighted_volume"] + right_fit["weighted_volume"])
    )
    return {
        "source_faces_left": sorted(int(face_id) for face_id in left),
        "source_faces_right": sorted(int(face_id) for face_id in right),
        "source_faces_merged": sorted(int(face_id) for face_id in left | right),
        "paper_base_cost": paper_base_cost,
        "weighted_priority_cost": weighted_priority_cost,
        "left_primitive": left_fit["paper_primitive"],
        "right_primitive": right_fit["paper_primitive"],
        "merged_primitive": merged["paper_primitive"],
        "left_volume": left_fit["volume"],
        "right_volume": right_fit["volume"],
        "merged_volume": merged["volume"],
        "left_weighted_volume": left_fit["weighted_volume"],
        "right_weighted_volume": right_fit["weighted_volume"],
        "merged_weighted_volume": merged["weighted_volume"],
        "left_fit_audit": left_audit,
        "right_fit_audit": right_audit,
        "merged_fit_audit": merged_audit,
        "paper_weights": PAPER_PRIMITIVE_WEIGHTS,
        "primary_cost_normalized_by_aabb": False,
        "intersection_volume_term_included": False,
        "newton_runtime_triggered": False,
    }


def _collapse_trace_payload(
    left: frozenset[int],
    right: frozenset[int],
) -> dict[str, object]:
    return {
        "trace_scope": "single_greedy_priority_queue_pop_fixture",
        "edge_source": "topology",
        "initial_edge_count": 1,
        "popped_source_faces_left": sorted(int(face_id) for face_id in left),
        "popped_source_faces_right": sorted(int(face_id) for face_id in right),
        "stale_entry": False,
        "accepted": True,
        "lookahead_used": False,
        "current_primitive_count_after_pop": 1,
        "stop_reason": "target_count_reached",
        "package_generation_triggered": False,
    }


def _priority_queue_trace_payload(
    mesh: TriangleMesh,
    initial_groups: tuple[frozenset[int], ...],
    target_primitive_count: int,
    *,
    allow_component_pair_edges: bool = False,
    component_pair_excess_volume_threshold: float | None = None,
    component_pair_candidate_cap: int | None = None,
    preprocessing_boundary: str | None = None,
) -> dict[str, object]:
    if component_pair_excess_volume_threshold is not None and not np.isfinite(
        component_pair_excess_volume_threshold
    ):
        raise ValueError("component_pair_excess_volume_threshold must be finite")
    if component_pair_candidate_cap is not None and component_pair_candidate_cap < 1:
        raise ValueError("component_pair_candidate_cap must be positive")
    active_groups = set(initial_groups)
    insertion_order = 0
    queue: list[dict[str, object]] = []
    for left, right in _topology_adjacent_group_pairs(mesh, active_groups):
        queue.append(_queue_candidate_payload(mesh, left, right, insertion_order))
        insertion_order += 1

    initial_candidates = [_queue_candidate_summary(entry) for entry in queue]
    events: list[dict[str, object]] = []
    accepted_merge_count = 0
    stale_entry_skipped_count = 0
    blocked_merge_count = 0
    component_pair_edge_insertion_triggered = False
    topology_queue_exhausted_before_component_pair_insertion = False
    component_pair_candidate_count = 0
    component_pair_available_pair_count = 0
    component_pair_candidates: list[dict[str, object]] = []
    skipped_component_pair_keys: list[dict[str, object]] = []
    component_pair_attempted_pairs: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    threshold_blocked = False

    while len(active_groups) > target_primitive_count:
        if not queue:
            if not allow_component_pair_edges:
                break
            component_pairs = [
                (left, right)
                for left, right in _component_pair_group_pairs(active_groups)
                if _component_pair_key(left, right) not in component_pair_attempted_pairs
            ]
            if not component_pairs:
                break
            topology_queue_exhausted_before_component_pair_insertion = True
            component_pair_edge_insertion_triggered = True
            component_pair_available_pair_count += len(component_pairs)
            if component_pair_candidate_cap is None:
                admitted_component_pairs = component_pairs
                skipped_component_pairs: list[tuple[frozenset[int], frozenset[int]]] = []
            else:
                admitted_component_pairs = component_pairs[:component_pair_candidate_cap]
                skipped_component_pairs = component_pairs[component_pair_candidate_cap:]
            for left, right in skipped_component_pairs:
                skipped_component_pair_keys.append(
                    _skipped_component_pair_payload(left, right)
                )
            for left, right in admitted_component_pairs:
                entry = _queue_candidate_payload(
                    mesh,
                    left,
                    right,
                    insertion_order,
                    edge_source="component_pair",
                )
                queue.append(entry)
                component_pair_candidates.append(_queue_candidate_summary(entry))
                insertion_order += 1
                component_pair_candidate_count += 1
            continue

        queue.sort(key=lambda entry: entry["_sort_key"])
        entry = queue.pop(0)
        active_before = len(active_groups)
        left_group = entry["_left_group"]
        right_group = entry["_right_group"]
        if left_group not in active_groups or right_group not in active_groups:
            events.append(
                _queue_event_payload(
                    entry,
                    stale_entry=True,
                    accepted=False,
                    active_primitive_count_before=active_before,
                    active_primitive_count_after=len(active_groups),
                    event_kind="stale_pop",
                )
            )
            stale_entry_skipped_count += 1
            continue

        if entry["edge_source"] == "component_pair":
            component_pair_attempted_pairs.add(_component_pair_key(left_group, right_group))
            if (
                component_pair_excess_volume_threshold is not None
                and float(entry["paper_base_cost"]) > component_pair_excess_volume_threshold
            ):
                events.append(
                    _queue_event_payload(
                        entry,
                        stale_entry=False,
                        accepted=False,
                        blocked=True,
                        active_primitive_count_before=active_before,
                        active_primitive_count_after=active_before,
                        event_kind="blocked_by_threshold",
                        blocked_reason="component_pair_threshold_exceeded",
                        threshold_value=float(component_pair_excess_volume_threshold),
                        threshold_metric="paper_base_cost",
                    )
                )
                blocked_merge_count += 1
                threshold_blocked = True
                continue

        active_groups.remove(left_group)
        active_groups.remove(right_group)
        merged_group = frozenset(left_group | right_group)
        active_groups.add(merged_group)
        active_after = len(active_groups)

        retained_queue: list[dict[str, object]] = []
        stale_events: list[dict[str, object]] = []
        for queued_entry in queue:
            queued_left = queued_entry["_left_group"]
            queued_right = queued_entry["_right_group"]
            if queued_left in active_groups and queued_right in active_groups:
                retained_queue.append(queued_entry)
                continue
            stale_events.append(
                _queue_event_payload(
                    queued_entry,
                    stale_entry=True,
                    accepted=False,
                    active_primitive_count_before=active_after,
                    active_primitive_count_after=active_after,
                    event_kind="eager_stale_prune",
                )
            )
        queue = retained_queue
        stale_entry_skipped_count += len(stale_events)

        updated_insertions = 0
        for other_group in sorted(active_groups - {merged_group}, key=_group_sort_key):
            if not _groups_share_mesh_edge(mesh, merged_group, other_group):
                continue
            queue.append(_queue_candidate_payload(mesh, merged_group, other_group, insertion_order))
            insertion_order += 1
            updated_insertions += 1

        events.append(
            _queue_event_payload(
                entry,
                stale_entry=False,
                accepted=True,
                active_primitive_count_before=active_before,
                active_primitive_count_after=active_after,
                resulting_source_faces=sorted(int(face_id) for face_id in merged_group),
                updated_neighbor_insertion_count=updated_insertions,
                event_kind="accepted_merge",
            )
        )
        events.extend(stale_events)
        accepted_merge_count += 1

    if len(active_groups) <= target_primitive_count:
        stop_reason = "target_count_reached"
    elif threshold_blocked:
        stop_reason = "all_remaining_edges_blocked_by_threshold"
    else:
        stop_reason = "queue_exhausted_before_target_count"
    component_pair_edge_policy = (
        "insert_when_topology_queue_exhausted_before_target"
        if allow_component_pair_edges
        else "disabled"
    )
    component_pair_candidate_cap_value: int | str
    if allow_component_pair_edges and component_pair_candidate_cap is None:
        component_pair_candidate_cap_value = "all_pairs_for_fixture"
    elif allow_component_pair_edges:
        component_pair_candidate_cap_value = int(component_pair_candidate_cap)
    else:
        component_pair_candidate_cap_value = "disabled"
    if component_pair_excess_volume_threshold is None:
        excess_volume_threshold: float | str = "default_inf"
        threshold_policy = "disabled"
    else:
        excess_volume_threshold = float(component_pair_excess_volume_threshold)
        threshold_policy = "component_pair_paper_base_cost_lte_threshold"
    payload: dict[str, object] = {
        "trace_scope": (
            "component_pair_priority_queue_trace_fixture"
            if allow_component_pair_edges
            else "topology_priority_queue_trace_fixture"
        ),
        "priority_queue_policy": "paper_greedy_min_weighted_priority_cost",
        "target_primitive_count": int(target_primitive_count),
        "excess_volume_threshold": excess_volume_threshold,
        "threshold_policy": threshold_policy,
        "component_pair_edge_policy": component_pair_edge_policy,
        "component_pair_edge_insertion_triggered": component_pair_edge_insertion_triggered,
        "topology_queue_exhausted_before_component_pair_insertion": (
            topology_queue_exhausted_before_component_pair_insertion
        ),
        "component_pair_available_pair_count": component_pair_available_pair_count,
        "component_pair_candidate_count": component_pair_candidate_count,
        "component_pair_candidate_cap": component_pair_candidate_cap_value,
        "component_pair_candidates": component_pair_candidates,
        "component_pair_attempted_pair_count": len(component_pair_attempted_pairs),
        "skipped_component_pair_count": len(skipped_component_pair_keys),
        "skipped_component_pair_keys": skipped_component_pair_keys,
        "initial_active_groups": _sorted_group_payload(initial_groups),
        "initial_edge_count": len(initial_candidates),
        "initial_candidates": initial_candidates,
        "events": events,
        "accepted_merge_count": accepted_merge_count,
        "stale_entry_skipped_count": stale_entry_skipped_count,
        "blocked_merge_count": blocked_merge_count,
        "final_active_groups": _sorted_group_payload(active_groups),
        "stop_reason": stop_reason,
        "package_generation_triggered": False,
        "newton_runtime_triggered": False,
        "real_usd_triggered": False,
        "benchmark_triggered": False,
    }
    if preprocessing_boundary is not None:
        payload["preprocessing_boundary"] = preprocessing_boundary
    return payload


def _queue_candidate_payload(
    mesh: TriangleMesh,
    left: frozenset[int],
    right: frozenset[int],
    insertion_order: int,
    *,
    edge_source: str = "topology",
) -> dict[str, object]:
    left, right = _ordered_group_pair(left, right)
    cost = _paper_merge_cost_payload(mesh, left, right)
    queue_key = [
        float(cost["weighted_priority_cost"]),
        float(cost["paper_base_cost"]),
        cost["source_faces_left"],
        cost["source_faces_right"],
        int(insertion_order),
    ]
    return {
        "_left_group": left,
        "_right_group": right,
        "_sort_key": (
            float(cost["weighted_priority_cost"]),
            float(cost["paper_base_cost"]),
            tuple(cost["source_faces_left"]),
            tuple(cost["source_faces_right"]),
            int(insertion_order),
        ),
        "source_faces_left": cost["source_faces_left"],
        "source_faces_right": cost["source_faces_right"],
        "source_faces_merged": cost["source_faces_merged"],
        "left_primitive": cost["left_primitive"],
        "right_primitive": cost["right_primitive"],
        "merged_primitive": cost["merged_primitive"],
        "paper_base_cost": cost["paper_base_cost"],
        "weighted_priority_cost": cost["weighted_priority_cost"],
        "queue_key": queue_key,
        "edge_source": edge_source,
        "insertion_order": int(insertion_order),
    }


def _queue_candidate_summary(entry: dict[str, object]) -> dict[str, object]:
    return {
        "source_faces_left": entry["source_faces_left"],
        "source_faces_right": entry["source_faces_right"],
        "source_faces_merged": entry["source_faces_merged"],
        "paper_base_cost": entry["paper_base_cost"],
        "weighted_priority_cost": entry["weighted_priority_cost"],
        "queue_key": entry["queue_key"],
        "edge_source": entry["edge_source"],
        "insertion_order": entry["insertion_order"],
        "left_primitive": entry["left_primitive"],
        "right_primitive": entry["right_primitive"],
        "merged_primitive": entry["merged_primitive"],
    }


def _queue_event_payload(
    entry: dict[str, object],
    *,
    stale_entry: bool,
    accepted: bool,
    active_primitive_count_before: int,
    active_primitive_count_after: int,
    event_kind: str,
    blocked: bool = False,
    blocked_reason: str | None = None,
    threshold_value: float | None = None,
    threshold_metric: str | None = None,
    resulting_source_faces: list[int] | None = None,
    updated_neighbor_insertion_count: int = 0,
) -> dict[str, object]:
    payload = _queue_candidate_summary(entry)
    payload.update(
        {
            "event_kind": event_kind,
            "stale_entry": bool(stale_entry),
            "accepted": bool(accepted),
            "blocked": bool(blocked),
            "active_primitive_count_before": int(active_primitive_count_before),
            "active_primitive_count_after": int(active_primitive_count_after),
            "updated_neighbor_insertion_count": int(updated_neighbor_insertion_count),
        }
    )
    if blocked_reason is not None:
        payload["blocked_reason"] = blocked_reason
    if threshold_value is not None:
        payload["threshold_value"] = float(threshold_value)
    if threshold_metric is not None:
        payload["threshold_metric"] = threshold_metric
    if resulting_source_faces is not None:
        payload["resulting_source_faces"] = resulting_source_faces
    return payload


def _topology_adjacent_group_pairs(
    mesh: TriangleMesh,
    groups: set[frozenset[int]],
) -> list[tuple[frozenset[int], frozenset[int]]]:
    pairs: list[tuple[frozenset[int], frozenset[int]]] = []
    sorted_groups = sorted(groups, key=_group_sort_key)
    for left_index, left in enumerate(sorted_groups):
        for right in sorted_groups[left_index + 1 :]:
            if _groups_share_mesh_edge(mesh, left, right):
                pairs.append(_ordered_group_pair(left, right))
    return pairs


def _component_pair_group_pairs(
    groups: set[frozenset[int]],
) -> list[tuple[frozenset[int], frozenset[int]]]:
    pairs: list[tuple[frozenset[int], frozenset[int]]] = []
    sorted_groups = sorted(groups, key=_group_sort_key)
    for left_index, left in enumerate(sorted_groups):
        for right in sorted_groups[left_index + 1 :]:
            pairs.append(_ordered_group_pair(left, right))
    return pairs


def _component_pair_key(
    left: frozenset[int],
    right: frozenset[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    left, right = _ordered_group_pair(left, right)
    return _group_sort_key(left), _group_sort_key(right)


def _skipped_component_pair_payload(
    left: frozenset[int],
    right: frozenset[int],
) -> dict[str, object]:
    left, right = _ordered_group_pair(left, right)
    return {
        "source_faces_left": sorted(int(face_id) for face_id in left),
        "source_faces_right": sorted(int(face_id) for face_id in right),
        "source_faces_merged": sorted(int(face_id) for face_id in left | right),
        "skip_reason": "component_pair_candidate_cap_reached",
    }


def _groups_share_mesh_edge(
    mesh: TriangleMesh,
    left: frozenset[int],
    right: frozenset[int],
) -> bool:
    left_edges = _group_edges(mesh, left)
    right_edges = _group_edges(mesh, right)
    return bool(left_edges & right_edges)


def _group_edges(mesh: TriangleMesh, group: frozenset[int]) -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for face_id in group:
        face = [int(index) for index in mesh.faces[int(face_id)]]
        for index, start in enumerate(face):
            end = face[(index + 1) % len(face)]
            edges.add(tuple(sorted((start, end))))
    return edges


def _ordered_group_pair(
    left: frozenset[int],
    right: frozenset[int],
) -> tuple[frozenset[int], frozenset[int]]:
    if _group_sort_key(left) <= _group_sort_key(right):
        return left, right
    return right, left


def _group_sort_key(group: frozenset[int]) -> tuple[int, ...]:
    return tuple(sorted(int(face_id) for face_id in group))


def _sorted_group_payload(groups) -> list[list[int]]:
    return [
        sorted(int(face_id) for face_id in group)
        for group in sorted(groups, key=_group_sort_key)
    ]


def _paper_toy_cases() -> tuple[_PaperToyCase, ...]:
    return (
        _PaperToyCase(
            case_id="paper_single_box",
            description="triangle-only asymmetric cuboid fixture for first OBB/sphere/capsule/capped-cylinder audit",
            mesh=_asymmetric_cuboid_surface_mesh(),
            face_groups=(frozenset(range(12)),),
        ),
        _PaperToyCase(
            case_id="paper_two_face_merge",
            description="two adjacent triangles for first paper base-cost and weighted-priority audit",
            mesh=_two_face_square_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({0, 1})),
            collapse_pair=(frozenset({0}), frozenset({1})),
        ),
        _PaperToyCase(
            case_id="paper_three_face_chain",
            description="three adjacent triangles for topology priority-queue trace audit",
            mesh=_three_face_chain_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({2})),
            priority_queue_target_count=1,
        ),
        _PaperToyCase(
            case_id="paper_disconnected_components",
            description="two disconnected triangles for threshold-disabled component-pair edge insertion audit",
            mesh=_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1})),
            priority_queue_target_count=1,
            component_pair_edge_insertion=True,
        ),
        _PaperToyCase(
            case_id="paper_component_pair_threshold_blocked",
            description="two disconnected triangles for finite-threshold component-pair block audit",
            mesh=_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1})),
            priority_queue_target_count=1,
            component_pair_edge_insertion=True,
            component_pair_excess_volume_threshold=0.0,
        ),
        _PaperToyCase(
            case_id="paper_tiny_sphere_clamp",
            description="tiny triangle fixture exercising paper OBB/sphere primitive-parameter clamp",
            mesh=_tiny_sphere_clamp_mesh(),
            face_groups=(frozenset({0}),),
        ),
        _PaperToyCase(
            case_id="paper_duplicate_vertex_preprocessing",
            description="two triangles with exact-coordinate duplicate vertices for preprocessing audit",
            mesh=_duplicate_vertex_preprocessing_mesh(),
            face_groups=(frozenset({0}), frozenset({1})),
            priority_queue_target_count=1,
            duplicate_vertex_preprocessing_audit=_duplicate_vertex_preprocessing_audit(),
        ),
        _PaperToyCase(
            case_id="paper_frustum_like",
            description="tapered triangle mesh for first offline frustum fit audit",
            mesh=_frustum_like_mesh(),
            face_groups=(frozenset(range(32)),),
        ),
        _PaperToyCase(
            case_id="paper_trapezoid_prism_like",
            description="roof-like triangle mesh for first offline trapezoidal-prism fit audit",
            mesh=_trapezoid_prism_like_mesh(),
            face_groups=(frozenset(range(12)),),
        ),
        _PaperToyCase(
            case_id="paper_nested_primitive",
            description="explicit nested OBB rows for enclosed-primitive postprocess culling audit",
            mesh=_nested_primitive_mesh(),
            face_groups=(frozenset(range(12)),),
            postprocess_fixture=True,
        ),
        _PaperToyCase(
            case_id="paper_quad_face_intake",
            description="one quad source face fan-triangulated for paper intake policy audit",
            mesh=_quad_face_intake_mesh(),
            face_groups=(frozenset({0, 1}),),
            source_face_intake_audit=_quad_face_intake_audit(),
        ),
        _PaperToyCase(
            case_id="paper_polygon_face_intake",
            description="one five-vertex polygon source face fan-triangulated for paper intake policy audit",
            mesh=_polygon_face_intake_mesh(),
            face_groups=(frozenset({0, 1, 2}),),
            source_face_intake_audit=_polygon_face_intake_audit(),
        ),
        _PaperToyCase(
            case_id="paper_mixed_face_preprocess_operator",
            description="Batch A mixed triangle/quad/polygon source-face fixture with exact-coordinate preprocessing",
            mesh=_mixed_face_preprocess_operator_mesh(),
            face_groups=(frozenset(range(6)),),
            source_face_intake_audit=_mixed_face_preprocess_operator_intake_audit(),
            duplicate_vertex_preprocessing_audit=_mixed_face_preprocess_operator_audit(),
            fixture_breadth_batch="paper_fixture_breadth_batch_a",
        ),
        _PaperToyCase(
            case_id="paper_degenerate_preprocess_face_drop",
            description="Batch A exact-coordinate preprocessing fixture that drops one degenerate source face",
            mesh=_degenerate_preprocess_face_drop_mesh(),
            face_groups=(frozenset({0}),),
            duplicate_vertex_preprocessing_audit=_degenerate_preprocess_face_drop_audit(),
            fixture_breadth_batch="paper_fixture_breadth_batch_a",
            executable_source_face_ids=(1,),
        ),
        _PaperToyCase(
            case_id="paper_concave_polygon_rejected",
            description="Batch A concave non-triangle source face rejected by conservative intake policy",
            mesh=_unsupported_source_face_placeholder_mesh(),
            face_groups=(frozenset({0}),),
            unsupported_source_face_intake_audit=_concave_polygon_rejected_audit(),
            fixture_breadth_batch="paper_fixture_breadth_batch_a",
        ),
        _PaperToyCase(
            case_id="paper_rotated_box_fit",
            description="Batch B rotated cuboid fixture for non-identity paper OBB axes",
            mesh=_paper_rotated_box_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_offset_sphere_fit",
            description="Batch B offset cuboid fixture for OBB-centered sphere audit",
            mesh=_paper_offset_sphere_fit_mesh(),
            face_groups=(frozenset(range(13)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_off_axis_capsule_fit",
            description="Batch B elongated off-axis fixture for capsule axis audit",
            mesh=_paper_off_axis_capsule_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_flat_capped_cylinder_axis_fit",
            description="Batch B off-axis flat-capped-cylinder primitive-fit audit",
            mesh=_paper_flat_capped_cylinder_axis_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_tapered_frustum_fit",
            description="Batch B tapered fixture for unequal frustum radii audit",
            mesh=_paper_tapered_frustum_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_asymmetric_trapezoid_fit",
            description="Batch B asymmetric wedge fixture for trapezoidal-prism axis-order audit",
            mesh=_paper_asymmetric_trapezoid_fit_mesh(),
            face_groups=(frozenset(range(12)),),
            fixture_breadth_batch="paper_fixture_breadth_batch_b",
        ),
        _PaperToyCase(
            case_id="paper_branching_cost_order",
            description="Batch C branching topology fixture for weighted priority cost ordering",
            mesh=_paper_branching_cost_order_mesh(),
            face_groups=(
                frozenset({0}),
                frozenset({1}),
                frozenset({2}),
                frozenset({3}),
            ),
            priority_queue_target_count=3,
            fixture_breadth_batch="paper_fixture_breadth_batch_c",
        ),
        _PaperToyCase(
            case_id="paper_equal_cost_queue_tie",
            description="Batch C symmetric topology fixture for deterministic equal-cost queue ties",
            mesh=_paper_equal_cost_queue_tie_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({2})),
            priority_queue_target_count=1,
            fixture_breadth_batch="paper_fixture_breadth_batch_c",
        ),
        _PaperToyCase(
            case_id="paper_nonzero_threshold_block",
            description="Batch C positive finite component-pair threshold block fixture",
            mesh=_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1})),
            priority_queue_target_count=1,
            component_pair_edge_insertion=True,
            component_pair_excess_volume_threshold=1e-6,
            fixture_breadth_batch="paper_fixture_breadth_batch_c",
        ),
        _PaperToyCase(
            case_id="paper_component_pair_multi_candidate_order",
            description="Batch D three disconnected components fixture for component-pair candidate ordering",
            mesh=_three_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({2})),
            priority_queue_target_count=2,
            component_pair_edge_insertion=True,
            fixture_breadth_batch="paper_fixture_breadth_batch_d",
        ),
        _PaperToyCase(
            case_id="paper_component_pair_cap_skipped",
            description="Batch D four disconnected components fixture for capped skipped-pair accounting",
            mesh=_four_disconnected_components_mesh(),
            face_groups=(frozenset({0}), frozenset({1}), frozenset({2}), frozenset({3})),
            priority_queue_target_count=3,
            component_pair_edge_insertion=True,
            component_pair_candidate_cap=2,
            fixture_breadth_batch="paper_fixture_breadth_batch_d",
        ),
        _PaperToyCase(
            case_id="paper_rotated_nested_primitive",
            description="Batch E rotated nested OBB fixture for enclosed-primitive postprocess breadth",
            mesh=_nested_primitive_mesh(),
            face_groups=(frozenset(range(12)),),
            postprocess_fixture=True,
            postprocess_audit_variant="rotated_nested_obb",
            fixture_breadth_batch="paper_fixture_breadth_batch_e",
        ),
        _PaperToyCase(
            case_id="paper_cross_type_enclosure_boundary",
            description="Batch E cross-type postprocess boundary fixture with explicit unsupported no-cull accounting",
            mesh=_nested_primitive_mesh(),
            face_groups=(frozenset(range(12)),),
            postprocess_fixture=True,
            postprocess_audit_variant="cross_type_unsupported_boundary",
            fixture_breadth_batch="paper_fixture_breadth_batch_e",
        ),
    )


def _asymmetric_cuboid_surface_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [2.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.5],
            [2.0, 0.0, 0.5],
            [2.0, 1.0, 0.5],
            [0.0, 1.0, 0.5],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [4, 6, 5],
            [4, 7, 6],
            [0, 4, 5],
            [0, 5, 1],
            [1, 5, 6],
            [1, 6, 2],
            [2, 6, 7],
            [2, 7, 3],
            [3, 7, 4],
            [3, 4, 0],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _two_face_square_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2], [1, 3, 2]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _three_face_chain_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
            [2.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [1, 3, 2],
            [1, 4, 3],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _paper_branching_cost_order_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.732172, 0.0, -0.095874],
            [0.151284, 2.644561, -0.089303],
            [-0.431305, -1.498606, -1.144457],
            [2.581183, 2.350038, -1.790004],
            [10.0, 0.0, 0.0],
            [11.0, 0.0, 0.0],
            [10.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [1, 0, 3],
            [2, 1, 4],
            [5, 6, 7],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _paper_equal_cost_queue_tie_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [-1.0, 0.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 3, 1],
            [0, 2, 4],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _disconnected_components_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _three_disconnected_components_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
            [0.0, 3.0, 0.0],
            [1.0, 3.0, 0.0],
            [0.0, 4.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _four_disconnected_components_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
            [0.0, 3.0, 0.0],
            [1.0, 3.0, 0.0],
            [0.0, 4.0, 0.0],
            [3.0, 3.0, 0.0],
            [4.0, 3.0, 0.0],
            [3.0, 4.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [9, 10, 11],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _tiny_sphere_clamp_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.0001, 0.0, 0.0],
            [0.0, 0.0001, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _rotate_z_then_x(
    point: tuple[float, float, float],
    *,
    z_radians: float,
    x_radians: float,
) -> tuple[float, float, float]:
    x, y, z = point
    cos_z = float(np.cos(z_radians))
    sin_z = float(np.sin(z_radians))
    z_rotated = (cos_z * x - sin_z * y, sin_z * x + cos_z * y, z)
    cos_x = float(np.cos(x_radians))
    sin_x = float(np.sin(x_radians))
    return (
        z_rotated[0],
        cos_x * z_rotated[1] - sin_x * z_rotated[2],
        sin_x * z_rotated[1] + cos_x * z_rotated[2],
    )


def _cuboid_points(
    *,
    center: tuple[float, float, float],
    half_extents: tuple[float, float, float],
) -> tuple[tuple[float, float, float], ...]:
    cx, cy, cz = center
    hx, hy, hz = half_extents
    return (
        (cx - hx, cy - hy, cz - hz),
        (cx + hx, cy - hy, cz - hz),
        (cx + hx, cy + hy, cz - hz),
        (cx - hx, cy + hy, cz - hz),
        (cx - hx, cy - hy, cz + hz),
        (cx + hx, cy - hy, cz + hz),
        (cx + hx, cy + hy, cz + hz),
        (cx - hx, cy + hy, cz + hz),
    )


def _box_surface_mesh_from_points(
    points: tuple[tuple[float, float, float], ...],
) -> TriangleMesh:
    return TriangleMesh(
        points=np.asarray(points, dtype=np.float64),
        faces=np.asarray(
            [
                (0, 1, 2),
                (0, 2, 3),
                (4, 6, 5),
                (4, 7, 6),
                (0, 4, 5),
                (0, 5, 1),
                (1, 5, 6),
                (1, 6, 2),
                (2, 6, 7),
                (2, 7, 3),
                (3, 7, 4),
                (3, 4, 0),
            ],
            dtype=np.int64,
        ),
    )


def _paper_rotated_box_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(0.2, -0.3, 0.4), half_extents=(0.9, 0.35, 0.2))
    rotated = [_rotate_z_then_x(point, z_radians=0.6, x_radians=0.35) for point in base]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_offset_sphere_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(1.1, -0.4, 0.3), half_extents=(0.75, 0.25, 0.18))
    rotated = [
        _rotate_z_then_x(point, z_radians=0.35, x_radians=-0.25)
        for point in base
    ]
    interior = _rotate_z_then_x((1.45, -0.28, 0.34), z_radians=0.35, x_radians=-0.25)
    return TriangleMesh(
        points=np.asarray(tuple(rotated) + (interior,), dtype=np.float64),
        faces=np.asarray(
            [
                (0, 1, 2),
                (0, 2, 3),
                (4, 6, 5),
                (4, 7, 6),
                (0, 4, 5),
                (0, 5, 1),
                (1, 5, 6),
                (1, 6, 2),
                (2, 6, 7),
                (2, 7, 3),
                (3, 7, 4),
                (3, 4, 0),
                (0, 1, 8),
            ],
            dtype=np.int64,
        ),
    )


def _paper_off_axis_capsule_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(0.0, 0.0, 0.0), half_extents=(1.6, 0.18, 0.18))
    rotated = [_rotate_z_then_x(point, z_radians=0.7, x_radians=0.45) for point in base]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_flat_capped_cylinder_axis_fit_mesh() -> TriangleMesh:
    base = _cuboid_points(center=(-0.2, 0.1, 0.0), half_extents=(0.28, 0.28, 1.1))
    rotated = [_rotate_z_then_x(point, z_radians=-0.55, x_radians=0.4) for point in base]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_tapered_frustum_fit_mesh() -> TriangleMesh:
    bottom = [
        (-1.0, -0.65, -1.8),
        (1.0, -0.65, -1.8),
        (1.0, 0.65, -1.8),
        (-1.0, 0.65, -1.8),
    ]
    top = [
        (-0.22, -0.14, 1.8),
        (0.22, -0.14, 1.8),
        (0.22, 0.14, 1.8),
        (-0.22, 0.14, 1.8),
    ]
    rotated = [
        _rotate_z_then_x(point, z_radians=0.45, x_radians=0.25)
        for point in bottom + top
    ]
    return _box_surface_mesh_from_points(tuple(rotated))


def _paper_asymmetric_trapezoid_fit_mesh() -> TriangleMesh:
    points = (
        (-0.9, -0.5, -0.35),
        (0.9, -0.5, -0.25),
        (0.65, 0.5, -0.12),
        (-0.55, 0.5, -0.28),
        (-0.45, -0.5, 0.62),
        (0.5, -0.5, 0.48),
        (0.35, 0.5, 0.22),
        (-0.25, 0.5, 0.52),
    )
    rotated = [
        _rotate_z_then_x(point, z_radians=-0.25, x_radians=0.3)
        for point in points
    ]
    return _box_surface_mesh_from_points(tuple(rotated))


def _duplicate_vertex_preprocessing_audit() -> _DuplicateVertexPreprocessingAudit:
    input_points = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, -1.0, 0.0),
    )
    input_faces = ((0, 1, 2), (3, 4, 5))
    deduplicated_points: list[tuple[float, float, float]] = []
    coordinate_to_deduplicated_id: dict[tuple[float, float, float], int] = {}
    original_to_deduplicated_vertex_ids: list[int] = []
    duplicate_clusters_by_deduplicated_id: dict[int, list[int]] = {}
    for input_vertex_id, point in enumerate(input_points):
        if point not in coordinate_to_deduplicated_id:
            coordinate_to_deduplicated_id[point] = len(deduplicated_points)
            deduplicated_points.append(point)
        deduplicated_id = coordinate_to_deduplicated_id[point]
        original_to_deduplicated_vertex_ids.append(deduplicated_id)
        duplicate_clusters_by_deduplicated_id.setdefault(deduplicated_id, []).append(
            input_vertex_id
        )
    deduplicated_faces = tuple(
        tuple(original_to_deduplicated_vertex_ids[vertex_id] for vertex_id in face)
        for face in input_faces
    )
    duplicate_clusters = tuple(
        tuple(vertex_ids)
        for vertex_ids in duplicate_clusters_by_deduplicated_id.values()
        if len(vertex_ids) > 1
    )
    return _DuplicateVertexPreprocessingAudit(
        input_points=input_points,
        input_faces=input_faces,
        deduplicated_points=tuple(deduplicated_points),
        deduplicated_faces=deduplicated_faces,
        original_to_deduplicated_vertex_ids=tuple(
            original_to_deduplicated_vertex_ids
        ),
        duplicate_clusters=duplicate_clusters,
    )


def _duplicate_vertex_preprocessing_mesh() -> TriangleMesh:
    audit = _duplicate_vertex_preprocessing_audit()
    return TriangleMesh(
        points=np.asarray(audit.deduplicated_points, dtype=np.float64),
        faces=np.asarray(audit.deduplicated_faces, dtype=np.int64),
    )


def _frustum_like_mesh() -> TriangleMesh:
    segment_count = 8
    bottom_radius = 1.0
    top_radius = 0.35
    bottom_z = -1.0
    top_z = 1.0
    points: list[list[float]] = []
    for z, radius in ((bottom_z, bottom_radius), (top_z, top_radius)):
        for index in range(segment_count):
            theta = (2.0 * pi * index) / segment_count
            points.append([radius * np.cos(theta), radius * np.sin(theta), z])
    bottom_center = len(points)
    points.append([0.0, 0.0, bottom_z])
    top_center = len(points)
    points.append([0.0, 0.0, top_z])

    faces: list[list[int]] = []
    top_offset = segment_count
    for index in range(segment_count):
        next_index = (index + 1) % segment_count
        bottom_left = index
        bottom_right = next_index
        top_left = top_offset + index
        top_right = top_offset + next_index
        faces.append([bottom_left, bottom_right, top_right])
        faces.append([bottom_left, top_right, top_left])
        faces.append([bottom_center, bottom_right, bottom_left])
        faces.append([top_center, top_left, top_right])
    return TriangleMesh(
        points=np.asarray(points, dtype=np.float64),
        faces=np.asarray(faces, dtype=np.int64),
    )


def _trapezoid_prism_like_mesh() -> TriangleMesh:
    points = np.array(
        [
            [-1.5, -1.0, -0.35],
            [1.5, -1.0, -0.35],
            [1.5, -1.0, 0.35],
            [-1.5, -1.0, 0.35],
            [-1.5, 1.0, -0.9],
            [1.5, 1.0, -0.9],
            [1.5, 1.0, 0.9],
            [-1.5, 1.0, 0.9],
        ],
        dtype=np.float64,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [4, 6, 5],
            [4, 7, 6],
            [0, 4, 5],
            [0, 5, 1],
            [1, 5, 6],
            [1, 6, 2],
            [2, 6, 7],
            [2, 7, 3],
            [3, 7, 4],
            [3, 4, 0],
        ],
        dtype=np.int64,
    )
    return TriangleMesh(points=points, faces=faces)


def _nested_primitive_mesh() -> TriangleMesh:
    return _asymmetric_cuboid_surface_mesh()


def _quad_face_intake_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _polygon_face_intake_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.25, 0.75, 0.0],
            [0.5, 1.25, 0.0],
            [-0.25, 0.75, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2], [0, 2, 3], [0, 3, 4]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _quad_face_intake_audit() -> _SourceFaceIntakeAudit:
    return _SourceFaceIntakeAudit(
        source_face_arities=(4,),
        source_face_remap=(
            _SourceFaceRemap(
                source_face_id=0,
                source_face_arity=4,
                source_vertex_ids=(0, 1, 2, 3),
                generated_triangle_face_ids=(0, 1),
                generated_triangle_vertex_ids=((0, 1, 2), (0, 2, 3)),
            ),
        ),
    )


def _polygon_face_intake_audit() -> _SourceFaceIntakeAudit:
    return _SourceFaceIntakeAudit(
        source_face_arities=(5,),
        source_face_remap=(
            _SourceFaceRemap(
                source_face_id=0,
                source_face_arity=5,
                source_vertex_ids=(0, 1, 2, 3, 4),
                generated_triangle_face_ids=(0, 1, 2),
                generated_triangle_vertex_ids=((0, 1, 2), (0, 2, 3), (0, 3, 4)),
            ),
        ),
    )


def _mixed_face_preprocess_operator_input_points() -> tuple[tuple[float, float, float], ...]:
    return (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (1.0, 0.0, 0.0),
        (2.0, 0.0, 0.0),
        (2.0, 1.0, 0.0),
        (1.0, 1.0, 0.0),
        (3.0, 0.0, 0.0),
        (4.0, 0.0, 0.0),
        (4.4, 0.6, 0.0),
        (3.7, 1.2, 0.0),
        (3.0, 0.8, 0.0),
    )


def _deduplicate_exact_points(
    input_points: tuple[tuple[float, float, float], ...],
) -> tuple[
    tuple[tuple[float, float, float], ...],
    tuple[int, ...],
    tuple[tuple[int, ...], ...],
]:
    deduplicated_points: list[tuple[float, float, float]] = []
    coordinate_to_deduplicated_id: dict[tuple[float, float, float], int] = {}
    original_to_deduplicated_vertex_ids: list[int] = []
    duplicate_clusters_by_deduplicated_id: dict[int, list[int]] = {}
    for input_vertex_id, point in enumerate(input_points):
        if point not in coordinate_to_deduplicated_id:
            coordinate_to_deduplicated_id[point] = len(deduplicated_points)
            deduplicated_points.append(point)
        deduplicated_id = coordinate_to_deduplicated_id[point]
        original_to_deduplicated_vertex_ids.append(deduplicated_id)
        duplicate_clusters_by_deduplicated_id.setdefault(deduplicated_id, []).append(
            input_vertex_id
        )
    duplicate_clusters = tuple(
        tuple(vertex_ids)
        for vertex_ids in duplicate_clusters_by_deduplicated_id.values()
        if len(vertex_ids) > 1
    )
    return (
        tuple(deduplicated_points),
        tuple(original_to_deduplicated_vertex_ids),
        duplicate_clusters,
    )


def _mixed_face_preprocess_operator_audit() -> _DuplicateVertexPreprocessingAudit:
    input_points = _mixed_face_preprocess_operator_input_points()
    input_faces = (
        (0, 1, 2),
        (3, 4, 5),
        (3, 5, 6),
        (7, 8, 9),
        (7, 9, 10),
        (7, 10, 11),
    )
    deduplicated_points, original_to_deduplicated_vertex_ids, duplicate_clusters = (
        _deduplicate_exact_points(input_points)
    )
    deduplicated_faces = tuple(
        tuple(original_to_deduplicated_vertex_ids[vertex_id] for vertex_id in face)
        for face in input_faces
    )
    return _DuplicateVertexPreprocessingAudit(
        input_points=input_points,
        input_faces=input_faces,
        deduplicated_points=deduplicated_points,
        deduplicated_faces=deduplicated_faces,
        original_to_deduplicated_vertex_ids=original_to_deduplicated_vertex_ids,
        duplicate_clusters=duplicate_clusters,
    )


def _mixed_face_preprocess_operator_mesh() -> TriangleMesh:
    audit = _mixed_face_preprocess_operator_audit()
    return TriangleMesh(
        points=np.asarray(audit.deduplicated_points, dtype=np.float64),
        faces=np.asarray(_executable_deduplicated_faces(audit), dtype=np.int64),
    )


def _mixed_face_preprocess_operator_intake_audit() -> _SourceFaceIntakeAudit:
    return _SourceFaceIntakeAudit(
        source_face_arities=(3, 4, 5),
        source_face_remap=(
            _SourceFaceRemap(
                source_face_id=0,
                source_face_arity=3,
                source_vertex_ids=(0, 1, 2),
                generated_triangle_face_ids=(0,),
                generated_triangle_vertex_ids=((0, 1, 2),),
            ),
            _SourceFaceRemap(
                source_face_id=1,
                source_face_arity=4,
                source_vertex_ids=(3, 4, 5, 6),
                generated_triangle_face_ids=(1, 2),
                generated_triangle_vertex_ids=((1, 3, 4), (1, 4, 5)),
            ),
            _SourceFaceRemap(
                source_face_id=2,
                source_face_arity=5,
                source_vertex_ids=(7, 8, 9, 10, 11),
                generated_triangle_face_ids=(3, 4, 5),
                generated_triangle_vertex_ids=((6, 7, 8), (6, 8, 9), (6, 9, 10)),
            ),
        ),
    )


def _degenerate_preprocess_face_drop_audit() -> _DuplicateVertexPreprocessingAudit:
    input_points = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 0.0),
        (0.0, 2.0, 0.0),
    )
    input_faces = ((0, 1, 2), (3, 4, 5))
    deduplicated_points, original_to_deduplicated_vertex_ids, duplicate_clusters = (
        _deduplicate_exact_points(input_points)
    )
    deduplicated_faces = tuple(
        tuple(original_to_deduplicated_vertex_ids[vertex_id] for vertex_id in face)
        for face in input_faces
    )
    return _DuplicateVertexPreprocessingAudit(
        input_points=input_points,
        input_faces=input_faces,
        deduplicated_points=deduplicated_points,
        deduplicated_faces=deduplicated_faces,
        original_to_deduplicated_vertex_ids=original_to_deduplicated_vertex_ids,
        duplicate_clusters=duplicate_clusters,
    )


def _degenerate_preprocess_face_drop_mesh() -> TriangleMesh:
    audit = _degenerate_preprocess_face_drop_audit()
    return TriangleMesh(
        points=np.asarray(audit.deduplicated_points, dtype=np.float64),
        faces=np.asarray(_executable_deduplicated_faces(audit), dtype=np.int64),
    )


def _unsupported_source_face_placeholder_mesh() -> TriangleMesh:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=np.float64,
    )
    faces = np.array([[0, 1, 2]], dtype=np.int64)
    return TriangleMesh(points=points, faces=faces)


def _concave_polygon_rejected_audit() -> _UnsupportedSourceFaceIntakeAudit:
    return _UnsupportedSourceFaceIntakeAudit(
        source_face_id=0,
        source_face_arity=5,
        source_vertex_ids=(0, 1, 2, 3, 4),
    )


def _face_operator_terms(
    mesh: TriangleMesh,
    face_id: int,
) -> tuple[float, NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    p0, p1, p2 = mesh.face_points(face_id)
    edge0 = p1 - p0
    edge1 = p2 - p0
    cross = np.cross(edge0, edge1)
    cross_norm = np.linalg.norm(cross)
    area = float(cross_norm * 0.5)
    normal = np.array([0.0, 0.0, 1.0], dtype=np.float64)
    if cross_norm != 0.0:
        normal = cross / cross_norm
    edge0_norm = np.linalg.norm(edge0)
    tangent = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    if edge0_norm != 0.0:
        tangent = edge0 / edge0_norm
    operator = area * (
        np.outer(normal, normal) + PAPER_Q_EPSILON * np.outer(tangent, tangent)
    )
    return area, normal, tangent, operator


def _group_operator(mesh: TriangleMesh, face_group: frozenset[int]) -> NDArray[np.float64]:
    operator = np.zeros((3, 3), dtype=np.float64)
    for face_id in face_group:
        operator += _face_operator_terms(mesh, int(face_id))[3]
    return operator


def _connected_component_count(mesh: TriangleMesh) -> int:
    adjacency = mesh.adjacent_faces()
    unseen = set(adjacency)
    component_count = 0
    while unseen:
        component_count += 1
        stack = [unseen.pop()]
        while stack:
            face_id = stack.pop()
            for neighbor in adjacency[face_id]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
    return component_count


def _operator_degeneracy_labels(operator: NDArray[np.float64]) -> list[str]:
    eigenvalues = np.linalg.eigvalsh(operator)
    if float(np.min(np.abs(eigenvalues))) <= 1e-12:
        return ["near_zero_eigenvalue"]
    return []


def _implementation_status(primitive_type: str) -> str:
    if primitive_type == "capped_cylinder":
        return "current_proxy_not_paper_faithful"
    return "current_surrogate_not_paper_faithful"


def _fit_model(primitive_type: str) -> str:
    if primitive_type == "capped_cylinder":
        return "current_axis_span_radial_proxy_with_hemisphere_caps"
    return "current_cpd_like_surrogate_fit"


def _axis_selection_policy(primitive_type: str) -> str:
    if primitive_type == "capsule":
        return "current_max_span_axis_surrogate"
    if primitive_type == "capped_cylinder":
        return "current_max_span_axis_proxy"
    return "operator_eigenvector_axes_from_current_triangle_operator"


def _matrix(values: NDArray[np.float64]) -> list[list[float]]:
    return [[float(value) for value in row] for row in values.tolist()]


def _vector(values: NDArray[np.float64]) -> list[float]:
    return [float(value) for value in values.tolist()]
