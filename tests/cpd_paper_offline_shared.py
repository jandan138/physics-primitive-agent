import ast
import hashlib
import inspect
import json
import sys
import types
from functools import lru_cache
from math import isfinite, pi, sqrt
from pathlib import Path

import pytest

import primitive_collision_compiler.baselines.cpd_paper.offline as cpd_paper_offline
import primitive_collision_compiler.newton.diagnostics as newton_diagnostics
import primitive_collision_compiler.newton.env as newton_env
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


@lru_cache(maxsize=1)
def _cached_cpd_paper_offline_report_json():
    return json.dumps(build_cpd_paper_offline_report(), allow_nan=False, sort_keys=True)


@lru_cache(maxsize=1)
def _cached_independent_cpd_paper_offline_report_json_for_determinism_check():
    return json.dumps(build_cpd_paper_offline_report(), allow_nan=False, sort_keys=True)


def _fresh_cpd_paper_offline_report():
    return json.loads(_cached_cpd_paper_offline_report_json())


def _fresh_independent_cpd_paper_offline_report_for_determinism_check():
    return json.loads(_cached_independent_cpd_paper_offline_report_json_for_determinism_check())


@pytest.fixture
def cpd_paper_report():
    return _fresh_cpd_paper_offline_report()


EXPECTED_GENERALIZATION_NEXT_ACTION = (
    "Proceed to paper_package_adapter_contract after the changed-decomposition "
    "output contract; keep package/Newton wording blocked."
)

EXPECTED_CLOSED_SOURCE_POLICY_GATE = "paper_generalization_batch_a_source_policy"

EXPECTED_CLOSED_PRIMITIVE_FIT_GATE = "paper_generalization_batch_b_primitive_fit_engine"

EXPECTED_CLOSED_SEARCH_ENGINE_GATE = "paper_generalization_batch_c_search_engine"

EXPECTED_CLOSED_POSTPROCESS_POLICY_GATE = "paper_generalization_batch_d_postprocess_policy"

EXPECTED_CLOSED_PACKAGE_BOUNDARY_GATE = "paper_generalization_batch_e_package_boundary_readiness"

EXPECTED_NEXT_AFTER_PACKAGE_BOUNDARY = "paper_offline_changed_decomposition_output_contract"

EXPECTED_PACKAGE_GENERATION_CONTRACT = "paper_package_generation_contract"

EXPECTED_PACKAGE_ADAPTER_CONTRACT = "paper_package_adapter_contract"

EXPECTED_PACKAGE_ADAPTER_UNSUPPORTED_PRIMITIVE_POLICY = (
    "paper_package_adapter_unsupported_primitive_policy"
)

EXPECTED_PACKAGE_CONVERSION_MAPPED_SUBSET_PLAN = "paper_package_conversion_mapped_subset_plan"

EXPECTED_MAPPED_SUBSET_CONVERSION_CANDIDATE_MATRIX = (
    "paper_mapped_subset_conversion_candidate_matrix"
)

EXPECTED_MAPPED_SUBSET_ADAPTER_PREFLIGHT_CONTRACT = "paper_mapped_subset_adapter_preflight_contract"

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

EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT = (
    "paper_mapped_subset_native_current_fixture_contract"
)

EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_native_fixture_generation_contract"
)

EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT = (
    "paper_mapped_subset_primitivespec_native_fixture_serialization_contract"
)

EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"
)

EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT = (
    "paper_mapped_subset_primitivespec_runtime_construction_contract"
)

EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_collision_package_generation_preflight_contract"
)

EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT = (
    "paper_mapped_subset_collision_package_generation_contract"
)

EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_runtime_admissibility_preflight_contract"
)

EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT = (
    "paper_mapped_subset_runtime_admissibility_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_mapping_preflight_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT = (
    "paper_mapped_subset_newton_shape_mapping_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_construction_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_builder_construction_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_api_surface_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_entry_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_smoke_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_execution_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_runtime_lane_review_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_design_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_preflight_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT = "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_validation_contract"

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT = "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_contract"

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT = "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_contract"

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT = "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_contract"

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_smoke_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_execution_contract"
)

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT = "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_lane_review_contract"

EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_RUN_CONTRACT = (
    "paper_mapped_subset_newton_shape_runtime_engine_builder_configured_runtime_run_contract"
)

EXPECTED_CURRENT_REPORT_NEXT_GATE = (
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_RUN_CONTRACT
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
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_RUN_CONTRACT,
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

EXPECTED_CANDIDATE_SOURCE_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NATIVE_CURRENT_FIXTURE_CONTRACT,
]

EXPECTED_NATIVE_CURRENT_FIXTURE_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_GENERATION_CONTRACT,
]

EXPECTED_NATIVE_FIXTURE_GENERATION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_NATIVE_FIXTURE_SERIALIZATION_CONTRACT,
]

EXPECTED_NATIVE_FIXTURE_SERIALIZATION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT,
]

EXPECTED_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_PRIMITIVESPEC_RUNTIME_CONSTRUCTION_CONTRACT,
]

EXPECTED_RUNTIME_CONSTRUCTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_PREFLIGHT_CONTRACT,
]

EXPECTED_COLLISION_PACKAGE_GENERATION_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_COLLISION_PACKAGE_GENERATION_CONTRACT,
]

EXPECTED_COLLISION_PACKAGE_GENERATION_CONTRACT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_PREFLIGHT_CONTRACT,
]

EXPECTED_RUNTIME_ADMISSIBILITY_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_RUNTIME_ADMISSIBILITY_CONTRACT,
]

EXPECTED_RUNTIME_ADMISSIBILITY_CONTRACT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_PREFLIGHT_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_MAPPING_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_MAPPING_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_MAPPING_CONTRACT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_CONSTRUCTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_CONTRACT,
]

EXPECTED_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_REMAINING_GAPS = [
    EXPECTED_MAPPED_SUBSET_NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_RUN_CONTRACT,
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
        "paper_requirement": ("Per-face and merged-group Q operators with eigen decomposition."),
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
            "This slice adds RED/GREEN tests, registry metadata, and a dated record path."
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

EXPECTED_SCOPE_AUDIT_CRITERIA = [row["criterion_id"] for row in EXPECTED_SCOPE_AUDIT_ROWS]

EXPECTED_SCOPE_AUDIT_BLOCKERS = [
    row["criterion_id"]
    for row in EXPECTED_SCOPE_AUDIT_ROWS
    if row["blocking_for_paper_faithful_offline"]
]


def _candidate_by_paper_primitive(audit, paper_primitive):
    rows = [row for row in audit["candidates"] if row["paper_primitive"] == paper_primitive]
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
            dot = sum(axes[left_index][coord] * axes[right_index][coord] for coord in range(3))
            assert abs(dot) < 1e-9
    return True


def _axes_are_world_aligned(axes):
    return all(_axis_is_world_basis(axis) for axis in axes)


def _axis_is_world_basis(axis):
    abs_values = [abs(value) for value in axis]
    max_index = max(range(3), key=lambda index: abs_values[index])
    return abs(abs_values[max_index] - 1.0) < 1e-9 and all(
        abs_values[index] < 1e-9 for index in range(3) if index != max_index
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
    assert source_mesh["source_face_remap"] == ("duplicate_vertex_preprocessing_face_id_preserving")
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
        [sum(point[index] * axis[index] for index in range(3)) for axis in axes] for point in points
    ]
    lower = [min(row[index] for row in local) for index in range(3)]
    upper = [max(row[index] for row in local) for index in range(3)]
    center_local = [(lower[index] + upper[index]) * 0.5 for index in range(3)]
    half_extents = [max((upper[index] - lower[index]) * 0.5, 1e-3) for index in range(3)]
    center = [
        sum(axes[axis_index][coord] * center_local[axis_index] for axis_index in range(3))
        for coord in range(3)
    ]
    assert all(abs(box_dims["lower_bounds"][index] - lower[index]) < 1e-9 for index in range(3))
    assert all(abs(box_dims["upper_bounds"][index] - upper[index]) < 1e-9 for index in range(3))
    assert all(
        abs(box_dims["paper_center_local"][index] - center_local[index]) < 1e-9
        for index in range(3)
    )
    assert all(
        abs(box_dims["paper_center_world"][index] - center[index]) < 1e-9 for index in range(3)
    )
    assert all(
        abs(box_dims["half_extents"][index] - half_extents[index]) < 1e-9 for index in range(3)
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
    assert (
        intake_audit["executable_triangle_face_count"]
        == source_mesh["executable_triangle_face_count"]
    )
    assert intake_audit["source_face_remap"] == source_mesh["source_face_remap"]
    assert intake_audit["source_face_preconditions"] == expected_preconditions
    assert intake_audit["source_face_policy"] == ("preserve_source_face_id_after_fan_triangulation")
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
    assert (
        operator_audit["source_face_operator_aggregates"][0]["generated_triangle_face_ids"]
        == expected_face_ids
    )
    expected_q = [
        [sum(face["q_matrix"][row][col] for face in operator_audit["faces"]) for col in range(3)]
        for row in range(3)
    ]
    assert operator_audit["source_face_operator_aggregates"][0]["q_matrix"] == expected_q
    assert operator_audit["merged_group"]["source_faces"] == [0]
    assert operator_audit["merged_group"]["generated_triangle_face_ids"] == expected_face_ids
    assert operator_audit["merged_group"]["source_face_ids"] == [0]
    assert case["primitive_fit_audit"]["source_faces"] == [0]
    assert case["primitive_fit_audit"]["generated_triangle_face_ids"] == expected_face_ids
    assert case["primitive_fit_audit"]["source_face_ids"] == [0]


def _generation_preflight_validation_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(json.dumps(report["paper_mapped_subset_primitivespec_validation_contract"]))


def _generation_contract_preflight_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_primitivespec_generation_preflight_contract"])
    )


def _candidate_source_generation_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(json.dumps(report["paper_mapped_subset_primitivespec_generation_contract"]))


def _native_current_fixture_candidate_source_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_primitivespec_candidate_source_contract"])
    )


def _native_current_fixture_cases_input() -> list[dict[str, object]]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(json.dumps(report["cases"]))


def _native_fixture_primitivespec_generation_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(json.dumps(report["paper_mapped_subset_native_current_fixture_contract"]))


def _native_fixture_primitivespec_serialization_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_primitivespec_native_fixture_generation_contract"])
    )


def _runtime_boundary_preflight_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report["paper_mapped_subset_primitivespec_native_fixture_serialization_contract"]
        )
    )


def _runtime_construction_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_primitivespec_runtime_boundary_preflight_contract"])
    )


def _collision_package_generation_preflight_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_primitivespec_runtime_construction_contract"])
    )


def _collision_package_generation_contract_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_collision_package_generation_preflight_contract"])
    )


def _runtime_admissibility_preflight_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_collision_package_generation_contract"])
    )


def _runtime_admissibility_contract_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_runtime_admissibility_preflight_contract"])
    )


def _newton_shape_mapping_preflight_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(json.dumps(report["paper_mapped_subset_runtime_admissibility_contract"]))


def _newton_shape_mapping_contract_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_mapping_preflight_contract"])
    )


def _newton_shape_runtime_boundary_preflight_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(json.dumps(report["paper_mapped_subset_newton_shape_mapping_contract"]))


def _newton_shape_runtime_construction_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_boundary_preflight_contract"])
    )


def _newton_shape_runtime_builder_preflight_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_construction_contract"])
    )


def _newton_shape_runtime_builder_construction_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_builder_preflight_contract"])
    )


def _newton_shape_runtime_engine_builder_boundary_preflight_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(report["paper_mapped_subset_newton_shape_runtime_builder_construction_contract"])
    )


def _newton_shape_runtime_engine_builder_environment_probe_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_boundary_preflight_contract"
            ]
        )
    )


def _newton_shape_runtime_engine_builder_api_surface_input() -> dict[str, object]:
    report = _fresh_cpd_paper_offline_report()
    return json.loads(
        json.dumps(
            report[
                "paper_mapped_subset_newton_shape_runtime_engine_builder_environment_probe_contract"
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

RUNTIME_CONSTRUCTION_FALSE_FLAGS = (
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
    "package_generation_allowed",
    "collision_package_generation_allowed",
    "runtime_admissibility_supported",
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "collision_package_generation_triggered",
    "runtime_admissibility_triggered",
)

RUNTIME_CONSTRUCTION_SOURCE_ROW_FALSE_FLAGS = tuple(
    flag for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS if flag != "package_generation_allowed"
)

COLLISION_PACKAGE_GENERATION_ALLOWED_TRUE_FLAGS = (
    "collision_package_generated",
    "package_generation_allowed",
    "collision_package_generation_allowed",
    "package_generation_triggered",
    "collision_package_generation_triggered",
)

COLLISION_PACKAGE_GENERATION_BOUNDARY_FALSE_FLAGS = tuple(
    flag
    for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS
    if flag not in COLLISION_PACKAGE_GENERATION_ALLOWED_TRUE_FLAGS
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

PRIMITIVESPEC_CANDIDATE_SOURCE_PAYLOAD_REQUIRED_KEYS = {
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
    "candidate_source_action",
    "primitive_spec_generation_candidate_count",
    "eligible_current_candidate_source_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "candidate_source_contract",
    "input_contract_summary",
    "native_template_candidate_source_audit_rows",
    "blocked_family_candidate_source_audit_rows",
    "noop_family_candidate_source_audit_rows",
    "current_row_candidate_source_audit_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

PRIMITIVESPEC_CANDIDATE_SOURCE_AUDIT_ROW_REQUIRED_KEYS = {
    "candidate_source_audit_row_id",
    "source_primitivespec_generation_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "source_role",
    "candidate_source_decision",
    "candidate_source_reason",
    "eligible_current_candidate_source",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "required_later_gate",
    "required_future_policy",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

NATIVE_CURRENT_FIXTURE_PAYLOAD_REQUIRED_KEYS = {
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
    "native_current_fixture_action",
    "eligible_current_candidate_source_count",
    "primitive_spec_generation_candidate_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "native_current_fixture_contract",
    "input_contract_summary",
    "fixture_source_summary",
    "native_current_fixture_source_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

NATIVE_CURRENT_FIXTURE_SOURCE_ROW_REQUIRED_KEYS = {
    "native_current_fixture_source_row_id",
    "source_candidate_source_audit_row_id",
    "source_primitivespec_generation_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "fixture_id",
    "fixture_source_faces",
    "source_fit_selected_paper_primitive",
    "source_fit_candidate_scope",
    "source_fit_selection_rule",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "source_role",
    "candidate_source_decision",
    "candidate_source_reason",
    "eligible_current_candidate_source",
    "primitive_spec_generation_candidate",
    "generated_primitive_spec",
    "required_later_gate",
    "required_future_policy",
    "fit_model",
    "axis_selection_policy",
    "center",
    "axes",
    "half_extents",
    "volume",
    "weighted_volume",
    "contains_assigned_points",
    "primitive_parameter_lower_clamp",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

SERIALIZED_PRIMITIVESPEC_LIKE_DICT_REQUIRED_KEYS = {
    "primitive_id",
    "kind",
    "pose",
    "center",
    "axes",
    "dimensions",
    "frame",
    "source_faces",
    "contains_assigned_points",
    "volume",
    "weighted_volume",
    "conversion_status",
}

NATIVE_FIXTURE_PRIMITIVESPEC_GENERATION_PAYLOAD_REQUIRED_KEYS = {
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
    "native_fixture_primitivespec_generation_action",
    "primitive_spec_generation_candidate_count",
    "offline_serialized_primitivespec_like_dict_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "native_fixture_primitivespec_generation_contract",
    "input_contract_summary",
    "native_fixture_primitivespec_generation_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

NATIVE_FIXTURE_PRIMITIVESPEC_GENERATION_ROW_REQUIRED_KEYS = {
    "native_fixture_primitivespec_generation_row_id",
    "source_native_current_fixture_source_row_id",
    "source_candidate_source_audit_row_id",
    "source_primitivespec_generation_row_id",
    "source_primitivespec_generation_preflight_row_id",
    "source_primitivespec_validation_row_id",
    "source_primitivespec_dry_run_row_id",
    "source_adapter_preflight_row_id",
    "source_candidate_matrix_row_id",
    "source_conversion_plan_row_id",
    "fixture_id",
    "fixture_source_faces",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "generation_decision",
    "generation_action",
    "primitive_spec_generation_candidate",
    "offline_serialized_primitivespec_like_dict",
    "runtime_instance_generated",
    "generated_primitive_spec",
    "required_later_gate",
    "required_future_policy",
    "fit_model",
    "axis_selection_policy",
    "center",
    "axes",
    "half_extents",
    "volume",
    "weighted_volume",
    "contains_assigned_points",
    "primitive_parameter_lower_clamp",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

NATIVE_FIXTURE_PRIMITIVESPEC_SERIALIZATION_PAYLOAD_REQUIRED_KEYS = {
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
    "serialization_action",
    "canonical_json_policy",
    "serialized_primitivespec_like_dict_count",
    "json_serialization_check_count",
    "json_round_trip_match_count",
    "schema_stability_check_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "native_fixture_primitivespec_serialization_contract",
    "input_contract_summary",
    "serialization_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

NATIVE_FIXTURE_PRIMITIVESPEC_SERIALIZATION_ROW_REQUIRED_KEYS = {
    "native_fixture_primitivespec_serialization_row_id",
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
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "primitive_id",
    "kind",
    "schema_keys",
    "serialized_payload",
    "canonical_primitivespec_json",
    "json_allow_nan",
    "json_sort_keys",
    "json_separators",
    "json_round_trip_equal",
    "canonical_json_stable",
    "schema_validation_status",
    "serialization_decision",
    "runtime_instance_generated",
    "generated_primitive_spec",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
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
    "runtime_boundary_action",
    "runtime_boundary_requirements",
    "runtime_boundary_preflight_row_count",
    "later_runtime_primitivespec_construction_candidate_count",
    "runtime_construction_allowed_in_current_gate",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "runtime_boundary_preflight_contract",
    "input_contract_summary",
    "runtime_boundary_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

RUNTIME_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "runtime_boundary_preflight_row_id",
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
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "primitive_id",
    "kind",
    "serialized_payload_schema_keys",
    "canonical_primitivespec_json",
    "canonical_primitivespec_json_sha256",
    "input_json_round_trip_equal",
    "input_canonical_json_stable",
    "input_schema_validation_status",
    "later_runtime_primitivespec_construction_candidate",
    "runtime_construction_allowed_in_current_gate",
    "required_later_gate",
    "preflight_decision",
    "preflight_reason",
    "runtime_instance_generated",
    "generated_primitive_spec",
    *PRIMITIVESPEC_GENERATION_ROW_FALSE_FLAGS,
}

RUNTIME_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_construction_action",
    "runtime_construction_requirements",
    "runtime_construction_row_count",
    "constructed_runtime_primitivespec_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "runtime_construction_contract",
    "input_contract_summary",
    "runtime_construction_rows",
    "coverage_summary",
    "remaining_gaps",
    "runtime_primitivespec_construction_triggered",
    "runtime_instance_generated",
    *RUNTIME_CONSTRUCTION_FALSE_FLAGS,
}

RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS = {
    "runtime_construction_row_id",
    "source_runtime_boundary_preflight_row_id",
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
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "primitive_id",
    "kind",
    "canonical_primitivespec_json",
    "loaded_primitivespec_payload",
    "constructed_primitivespec_dict",
    "conversion_status_transition",
    "runtime_instance_generated",
    "generated_primitive_spec",
    "runtime_primitivespec_construction_triggered",
    *RUNTIME_CONSTRUCTION_FALSE_FLAGS,
}

COLLISION_PACKAGE_GENERATION_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "package_generation_preflight_action",
    "package_generation_preflight_requirements",
    "package_generation_preflight_row_count",
    "later_collision_package_generation_candidate_count",
    "package_generation_allowed_in_current_gate",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "package_generation_preflight_contract",
    "input_contract_summary",
    "package_generation_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *RUNTIME_CONSTRUCTION_FALSE_FLAGS,
}

COLLISION_PACKAGE_GENERATION_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "package_generation_preflight_row_id",
    "source_runtime_construction_row_id",
    "source_runtime_boundary_preflight_row_id",
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
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "primitive_id",
    "kind",
    "generated_primitive_spec",
    "constructed_primitivespec_dict",
    "candidate_primitivespec_dict",
    "candidate_package_primitive_kind",
    "candidate_package_scope",
    "later_collision_package_generation_candidate",
    "package_generation_allowed_in_current_gate",
    "required_later_gate",
    "preflight_decision",
    "preflight_reason",
    "collision_package_generated",
    "generated_collision_package",
    "runtime_admissibility_checked",
    *RUNTIME_CONSTRUCTION_FALSE_FLAGS,
}

COLLISION_PACKAGE_GENERATION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "package_generation_action",
    "package_generation_requirements",
    "collision_package_generation_row_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "package_generation_contract",
    "input_contract_summary",
    "collision_package_generation_rows",
    "coverage_summary",
    "remaining_gaps",
    *COLLISION_PACKAGE_GENERATION_ALLOWED_TRUE_FLAGS,
    *COLLISION_PACKAGE_GENERATION_BOUNDARY_FALSE_FLAGS,
}

COLLISION_PACKAGE_GENERATION_ROW_REQUIRED_KEYS = {
    "collision_package_generation_row_id",
    "source_package_generation_preflight_row_id",
    "source_runtime_construction_row_id",
    "source_runtime_boundary_preflight_row_id",
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
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "primitive_id",
    "kind",
    "candidate_primitivespec_dict",
    "synthetic_source_manifest",
    "synthetic_source_manifest_canonical_json",
    "unsupported_primitives_in_this_single_fixture",
    "primitive_families_not_evaluated_by_this_gate",
    "generated_collision_package",
    "runtime_admissibility_checked",
    *COLLISION_PACKAGE_GENERATION_ALLOWED_TRUE_FLAGS,
    *COLLISION_PACKAGE_GENERATION_BOUNDARY_FALSE_FLAGS,
}

GENERATED_COLLISION_PACKAGE_REQUIRED_KEYS = {
    "package_id",
    "asset_id",
    "source_path",
    "source_sha256",
    "method",
    "stage",
    "status",
    "claim_boundary",
    "mesh_point_count",
    "mesh_face_count",
    "max_source_faces",
    "primitive_subset",
    "primitives",
    "unsupported_primitives",
    "fallback",
}

RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    *RUNTIME_CONSTRUCTION_FALSE_FLAGS,
)

RUNTIME_ADMISSIBILITY_PREFLIGHT_INPUT_FALSE_FLAGS = (
    *COLLISION_PACKAGE_GENERATION_BOUNDARY_FALSE_FLAGS,
)

RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_admissibility_preflight_action",
    "runtime_admissibility_preflight_requirements",
    "runtime_admissibility_preflight_row_count",
    "later_runtime_admissibility_candidate_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "source_collision_package_available",
    "runtime_admissibility_preflight_contract",
    "input_contract_summary",
    "runtime_admissibility_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS,
}

RUNTIME_ADMISSIBILITY_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "runtime_admissibility_preflight_row_id",
    "source_collision_package_generation_row_id",
    "source_package_generation_preflight_row_id",
    "source_runtime_construction_row_id",
    "source_runtime_boundary_preflight_row_id",
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
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "primitive_id",
    "kind",
    "candidate_primitivespec_dict",
    "source_package_id",
    "source_asset_id",
    "source_package_stage",
    "source_package_status",
    "source_package_method",
    "source_package_source_path",
    "source_package_source_sha256",
    "source_package_claim_boundary",
    "source_package_primitive_count",
    "source_package_primitive_subset",
    "source_package_unsupported_primitives",
    "source_package_runtime_admissibility_status",
    "source_collision_package_available",
    "later_runtime_admissibility_candidate",
    "runtime_admissibility_preflight_decision",
    "required_later_gate",
    *RUNTIME_ADMISSIBILITY_PREFLIGHT_PAYLOAD_FALSE_FLAGS,
}

RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    *(flag for flag in RUNTIME_CONSTRUCTION_FALSE_FLAGS if flag != "runtime_admissibility_checked"),
)

RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_admissibility_action",
    "runtime_admissibility_requirements",
    "runtime_admissibility_row_count",
    "offline_static_runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_checked",
    "runtime_admissibility_check_count",
    "runtime_execution_count",
    "newton_mapping_record_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "source_collision_package_available",
    "runtime_admissibility_contract",
    "input_contract_summary",
    "runtime_admissibility_rows",
    "coverage_summary",
    "remaining_gaps",
    *RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS,
}

RUNTIME_ADMISSIBILITY_CONTRACT_ROW_REQUIRED_KEYS = {
    "runtime_admissibility_row_id",
    "source_runtime_admissibility_preflight_row_id",
    "source_collision_package_generation_row_id",
    "source_package_generation_preflight_row_id",
    "source_runtime_construction_row_id",
    "source_runtime_boundary_preflight_row_id",
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
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "candidate_mapping_label",
    "newton_runtime_kind",
    "primitive_id",
    "kind",
    "candidate_primitivespec_dict",
    "source_package_id",
    "source_asset_id",
    "source_package_stage",
    "source_package_status",
    "source_package_method",
    "source_package_source_path",
    "source_package_source_sha256",
    "source_package_claim_boundary",
    "source_package_primitive_count",
    "source_package_primitive_subset",
    "source_package_unsupported_primitives",
    "source_collision_package_available",
    "runtime_admissibility_static_check_kind",
    "runtime_admissibility_decision",
    "runtime_admissibility_status",
    "required_later_gate",
    "finite_center_check_passed",
    "finite_axes_check_passed",
    "orthonormal_axes_check_passed",
    "right_handed_axes_check_passed",
    "positive_dimensions_check_passed",
    "target_shape_schema_check_passed",
    "source_faces_check_passed",
    "contains_assigned_points_check_passed",
    "volume_check_passed",
    "weighted_volume_check_passed",
    "offline_static_runtime_admissibility_check_passed",
    "offline_static_runtime_admissibility_checked",
    *RUNTIME_ADMISSIBILITY_CONTRACT_PAYLOAD_FALSE_FLAGS,
}

NEWTON_SHAPE_MAPPING_PREFLIGHT_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
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
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "mapping_attempted",
    "newton_shape_mapping_triggered",
    "newton_shape_mapping_record_created",
)

NEWTON_SHAPE_MAPPING_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "newton_shape_mapping_preflight_action",
    "newton_shape_mapping_preflight_contract",
    "input_contract_summary",
    "newton_shape_mapping_preflight_row_count",
    "source_runtime_admissibility_row_count",
    "source_runtime_admissibility_check_passed",
    "newton_shape_mapping_preflight_passed",
    "mapping_attempt_count",
    "newton_mapping_record_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "newton_shape_mapping_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_MAPPING_PREFLIGHT_FALSE_FLAGS,
}

NEWTON_SHAPE_MAPPING_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "candidate_primitivespec_dict",
    "target_newton_shape_kind",
    "target_newton_shape_kind_declared",
    "newton_shape_support_evidence_status",
    "target_newton_shape_kind_handoff_source",
    "center_transfer_field",
    "axes_transfer_field",
    "dimensions_transfer_field",
    "box_half_extents_transfer_field",
    "target_kind_declared_check_passed",
    "center_transfer_check_passed",
    "axes_transfer_check_passed",
    "box_dimensions_transfer_check_passed",
    "source_runtime_admissibility_check_passed",
    "source_package_lineage_check_passed",
    "newton_shape_mapping_preflight_passed",
    "mapping_attempt_count",
    "newton_mapping_record_count",
    "newton_runtime_execution_count",
    *NEWTON_SHAPE_MAPPING_PREFLIGHT_FALSE_FLAGS,
}

NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
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
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "mapping_attempted",
    "newton_shape_mapping_triggered",
    "newton_shape_mapping_record_created",
    "newton_shape_object_created",
)

NEWTON_SHAPE_MAPPING_CONTRACT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "shape_mapping_contract_action",
    "newton_shape_mapping_contract",
    "input_contract_summary",
    "shape_mapping_contract_row_count",
    "source_newton_shape_mapping_preflight_row_count",
    "report_scoped_newton_shape_descriptor_count",
    "source_preflight_check_passed",
    "mapping_attempt_count",
    "newton_mapping_record_count",
    "newton_shape_object_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "shape_mapping_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS,
}

NEWTON_SHAPE_MAPPING_CONTRACT_ROW_REQUIRED_KEYS = {
    "shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "newton_shape_descriptor_dict",
    "descriptor_contract_passed",
    "descriptor_kind_check_passed",
    "target_kind_check_passed",
    "center_descriptor_check_passed",
    "axes_descriptor_check_passed",
    "half_extents_descriptor_check_passed",
    "source_preflight_check_passed",
    "source_lineage_check_passed",
    "mapping_attempt_count",
    "newton_mapping_record_count",
    "newton_shape_object_count",
    "newton_runtime_execution_count",
    *NEWTON_SHAPE_MAPPING_CONTRACT_FALSE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
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
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "mapping_attempted",
    "newton_shape_mapping_triggered",
    "newton_shape_mapping_record_created",
    "newton_shape_object_created",
    "newton_shape_runtime_construction_triggered",
    "newton_shape_runtime_boundary_crossed",
)

NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_boundary_preflight_action",
    "newton_shape_runtime_boundary_preflight_contract",
    "input_contract_summary",
    "newton_shape_runtime_boundary_preflight_row_count",
    "source_shape_mapping_contract_row_count",
    "later_newton_shape_runtime_construction_candidate_count",
    "report_scoped_newton_shape_descriptor_count",
    "runtime_boundary_preflight_passed",
    "mapping_attempt_count",
    "newton_mapping_record_count",
    "newton_shape_object_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "newton_shape_runtime_boundary_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "descriptor_kind",
    "descriptor_center",
    "descriptor_axes",
    "descriptor_half_extents",
    "runtime_boundary_preflight_passed",
    "descriptor_kind_check_passed",
    "target_kind_check_passed",
    "descriptor_lineage_check_passed",
    "center_descriptor_check_passed",
    "axes_descriptor_check_passed",
    "half_extents_descriptor_check_passed",
    "later_newton_shape_runtime_construction_candidate",
    "mapping_attempt_count",
    "newton_mapping_record_count",
    "newton_shape_object_count",
    "newton_runtime_execution_count",
    *NEWTON_SHAPE_RUNTIME_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_CONSTRUCTION_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
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
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "mapping_attempted",
    "newton_shape_mapping_triggered",
    "newton_shape_object_created",
    "newton_shape_runtime_construction_triggered",
    "newton_shape_runtime_boundary_crossed",
    "newton_engine_shape_object_created",
    "newton_builder_shape_called",
)

NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS = (
    "repo_local_newton_shape_mapping_record_constructed",
    "newton_shape_mapping_record_created",
)

NEWTON_SHAPE_RUNTIME_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_construction_action",
    "newton_shape_runtime_construction_contract",
    "input_contract_summary",
    "newton_shape_runtime_construction_row_count",
    "source_newton_shape_runtime_boundary_preflight_row_count",
    "constructed_newton_shape_mapping_record_count",
    "newton_mapping_record_count",
    "newton_mapper_call_count",
    "newton_shape_object_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "later_newton_shape_runtime_construction_candidate_count",
    "newton_shape_runtime_construction_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_CONSTRUCTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_CONSTRUCTION_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "descriptor_kind",
    "descriptor_center",
    "descriptor_axes",
    "descriptor_half_extents",
    "constructed_newton_shape_mapping_dict",
    "constructed_newton_shape_mapping_status",
    "constructed_newton_shape_mapping_detail",
    "mapping_constructor",
    "mapping_constructor_input_kind",
    "runtime_builder_preflight_candidate",
    "constructed_newton_shape_mapping_record_count",
    "newton_mapping_record_count",
    "newton_mapper_call_count",
    "newton_shape_object_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    *NEWTON_SHAPE_RUNTIME_CONSTRUCTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_CONSTRUCTION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
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
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "mapping_attempted",
    "newton_shape_mapping_triggered",
    "newton_shape_object_created",
    "newton_shape_runtime_construction_triggered",
    "newton_shape_runtime_boundary_crossed",
    "newton_engine_shape_object_created",
    "newton_builder_shape_called",
    "newton_runtime_builder_invoked",
    "newton_model_builder_instantiated",
    "newton_model_finalized",
)

NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS = (
    "newton_shape_runtime_builder_preflight_recorded",
    "repo_local_newton_builder_call_plan_record_created",
)

NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_builder_preflight_action",
    "newton_shape_runtime_builder_preflight_contract",
    "input_contract_summary",
    "newton_shape_runtime_builder_preflight_row_count",
    "source_newton_shape_runtime_construction_row_count",
    "source_newton_shape_mapping_record_count",
    "runtime_builder_preflight_passed",
    "runtime_builder_preflight_passed_count",
    "builder_call_plan_count",
    "builder_call_allowed_count",
    "later_newton_shape_runtime_builder_candidate_count",
    "newton_mapping_record_count",
    "newton_mapper_call_count",
    "newton_shape_object_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "later_newton_shape_runtime_construction_candidate_count",
    "constructed_newton_shape_mapping_record_count",
    "newton_shape_runtime_builder_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "descriptor_kind",
    "descriptor_center",
    "descriptor_axes",
    "descriptor_half_extents",
    "constructed_newton_shape_mapping_dict",
    "constructed_newton_shape_mapping_status",
    "constructed_newton_shape_mapping_detail",
    "mapping_constructor",
    "mapping_constructor_input_kind",
    "runtime_builder_preflight_passed",
    "builder_call_allowed",
    "builder_candidate_kind",
    "builder_shape_kind",
    "builder_method_name",
    "call_signature_fields",
    "body_binding_policy",
    "deferred_xform_policy",
    "deferred_translation_inputs",
    "deferred_rotation_inputs",
    "dimension_source",
    "builder_center",
    "builder_axes",
    "builder_half_extents",
    "builder_dimension_argument_schema",
    "builder_call_plan",
    "builder_call_plan_count",
    "later_newton_shape_runtime_builder_candidate",
    "runtime_builder_construction_contract_candidate",
    "constructed_newton_shape_mapping_record_count",
    "newton_mapping_record_count",
    "newton_mapper_call_count",
    "newton_shape_object_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    *NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_BUILDER_PREFLIGHT_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_FALSE_FLAGS = (
    "paper_faithful_offline_allowed",
    "paper_faithful_offline_supported",
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
    "newton_runtime_allowed",
    "approximation_policy_enabled",
    "silent_drop_allowed",
    "mapping_attempted",
    "newton_shape_mapping_triggered",
    "newton_shape_object_created",
    "newton_shape_runtime_construction_triggered",
    "newton_shape_runtime_boundary_crossed",
    "newton_engine_shape_object_created",
    "newton_builder_shape_called",
    "newton_runtime_builder_invoked",
    "newton_model_builder_instantiated",
    "newton_model_finalized",
    "real_newton_import_triggered",
    "newton_collision_pipeline_created",
    "newton_collision_pipeline_collide_called",
    "newton_contact_diagnostic_triggered",
    "newton_drop_settle_triggered",
    "newton_sphere_rain_triggered",
)

NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_TRUE_FLAGS = (
    "newton_shape_runtime_builder_construction_recorded",
    "repo_local_recording_builder_shape_call_recorded",
    "repo_local_static_shape_helper_called",
)

NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_builder_construction_action",
    "newton_shape_runtime_builder_construction_contract",
    "input_contract_summary",
    "newton_shape_runtime_builder_construction_row_count",
    "source_newton_shape_runtime_builder_preflight_row_count",
    "recording_builder_shape_call_count",
    "recorded_builder_call_count",
    "repo_local_static_shape_helper_call_count",
    "real_newton_import_count",
    "newton_model_builder_instantiated_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "later_newton_shape_runtime_construction_candidate_count",
    "constructed_newton_shape_mapping_record_count",
    "builder_call_plan_count",
    "newton_shape_runtime_builder_construction_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "descriptor_kind",
    "descriptor_center",
    "descriptor_axes",
    "descriptor_half_extents",
    "constructed_newton_shape_mapping_dict",
    "builder_call_plan",
    "builder_method_name",
    "builder_body_argument",
    "builder_dimension_arguments",
    "builder_xform_descriptor",
    "repo_local_static_shape_helper",
    "repo_local_static_shape_helper_called",
    "recording_builder_kind",
    "recording_builder_shape_call_count",
    "recorded_builder_method_name",
    "recorded_builder_call",
    "recorded_builder_call_count",
    "fake_wp_call_summary",
    "real_newton_import_count",
    "newton_model_builder_instantiated_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "later_newton_shape_runtime_construction_candidate_count",
    "constructed_newton_shape_mapping_record_count",
    "newton_mapping_record_count",
    *NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_BUILDER_CONSTRUCTION_FALSE_FLAGS,
    "newton_engine_builder_boundary_crossed",
    "newton_engine_builder_environment_probe_triggered",
    "real_newton_runtime_import_attempted",
    "real_newton_builder_constructed",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_TRUE_FLAGS = (
    "newton_shape_runtime_engine_builder_boundary_preflight_recorded",
    "newton_engine_builder_boundary_requirements_recorded",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_REQUIRED_CHECKS = [
    "newton_source_dir_resolved",
    "newton_module_provenance_checked",
    "warp_module_provenance_checked",
    "runtime_module_import_isolation_checked",
    "model_builder_constructor_signature_checked",
    "static_body_binding_policy_reviewed",
    "shape_call_signature_reviewed",
    "model_finalize_policy_deferred_to_later_gate",
    "collision_pipeline_policy_deferred_to_later_gate",
    "generated_collision_package_artifact_reviewed",
]

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_engine_builder_boundary_preflight_action",
    "newton_shape_runtime_engine_builder_boundary_preflight_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_boundary_preflight_row_count",
    "source_newton_shape_runtime_builder_construction_row_count",
    "recording_builder_shape_call_count",
    "recorded_builder_call_count",
    "repo_local_static_shape_helper_call_count",
    "required_before_engine_builder_boundary_count",
    "real_newton_import_count",
    "newton_model_builder_instantiated_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "constructed_newton_shape_mapping_record_count",
    "builder_call_plan_count",
    "newton_shape_runtime_engine_builder_boundary_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "constructed_newton_shape_mapping_dict",
    "recorded_builder_method_name",
    "recorded_builder_call",
    "recorded_builder_call_count",
    "recording_builder_kind",
    "recording_builder_shape_call_count",
    "repo_local_static_shape_helper",
    "repo_local_static_shape_helper_called",
    "builder_call_plan",
    "builder_method_name",
    "builder_body_argument",
    "builder_dimension_arguments",
    "builder_xform_descriptor",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "boundary_status",
    "boundary_decision",
    "blocked_until_gate",
    "required_before_engine_builder_boundary",
    "required_before_engine_builder_boundary_count",
    "real_newton_import_count",
    "newton_model_builder_instantiated_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "constructed_newton_shape_mapping_record_count",
    "newton_mapping_record_count",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_FALSE_FLAGS = (
    *(
        flag
        for flag in NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_FALSE_FLAGS
        if flag != "newton_engine_builder_environment_probe_triggered"
    ),
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_BOUNDARY_PREFLIGHT_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_environment_probe_recorded",
    "newton_engine_builder_environment_probe_triggered",
    "newton_source_dir_resolution_checked",
    "newton_module_provenance_checked",
    "warp_module_provenance_checked",
    "runtime_module_import_isolation_checked",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "environment_probe_action",
    "environment_probe_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_environment_probe_row_count",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_count",
    "module_probe_row_count",
    "source_dir_configured_count",
    "newton_module_available_count",
    "warp_module_available_count",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "constructed_newton_shape_mapping_record_count",
    "builder_call_plan_count",
    "newton_shape_runtime_engine_builder_environment_probe_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "environment_probe_status",
    "environment_probe_mode",
    "environment_probe_claim_boundary",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_resolved",
    "newton_source_dir_status",
    "module_probe_rows",
    "module_probe_row_count",
    "newton_module_name",
    "newton_module_available",
    "newton_module_origin",
    "newton_module_origin_resolved",
    "newton_module_provenance_status",
    "warp_module_name",
    "warp_module_available",
    "warp_module_origin",
    "warp_module_origin_resolved",
    "warp_module_provenance_status",
    "sys_path_restored",
    "cached_runtime_modules_restored",
    "runtime_module_import_isolation_checked",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "constructed_newton_shape_mapping_record_count",
    "newton_mapping_record_count",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_FALSE_FLAGS,
    "newton_engine_builder_import_boundary_crossed",
    "real_newton_api_import_attempted",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENVIRONMENT_PROBE_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_api_surface_recorded",
    "newton_engine_builder_api_surface_probe_triggered",
    "newton_engine_builder_source_api_surface_policy_recorded",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "api_surface_action",
    "api_surface_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_api_surface_row_count",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_count",
    "module_probe_row_count",
    "source_dir_configured_count",
    "newton_module_available_count",
    "warp_module_available_count",
    "api_surface_probe_count",
    "newton_model_builder_symbol_found_count",
    "newton_add_shape_box_symbol_found_count",
    "newton_model_finalize_symbol_found_count",
    "collision_pipeline_symbol_found_count",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "constructed_newton_shape_mapping_record_count",
    "builder_call_plan_count",
    "newton_shape_runtime_engine_builder_api_surface_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "environment_probe_status",
    "environment_probe_mode",
    "newton_source_dir_configured",
    "newton_source_dir_status",
    "module_probe_row_count",
    "newton_module_available",
    "newton_module_provenance_status",
    "warp_module_available",
    "warp_module_provenance_status",
    "api_surface_probe_status",
    "api_surface_probe_mode",
    "api_surface_claim_boundary",
    "source_files_checked",
    "source_file_rows",
    "model_builder_exported_from_newton_init",
    "collision_pipeline_exported_from_newton_init",
    "model_builder_class_found",
    "model_builder_class_file",
    "model_builder_constructor_found",
    "model_builder_constructor_signature",
    "add_shape_box_found",
    "add_shape_box_signature",
    "planned_builder_call_fields_present",
    "finalize_method_found",
    "collision_pipeline_symbol_found",
    "import_attempted",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_runtime_execution_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "generated_runtime_primitive_spec_count",
    "generated_primitive_spec_count",
    "generated_collision_package_count",
    "runtime_admissibility_check_count",
    "offline_static_runtime_admissibility_check_count",
    "report_scoped_newton_shape_descriptor_count",
    "constructed_newton_shape_mapping_record_count",
    "newton_mapping_record_count",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_FALSE_FLAGS,
    "runtime_entry_allowed",
    "runtime_entry_attempted",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_API_SURFACE_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_entry_recorded",
    "source_package_copy_forbidden",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "entry_action",
    "entry_decision",
    "entry_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_entry_row_count",
    "source_newton_shape_runtime_engine_builder_api_surface_row_count",
    "runtime_entry_allowed_count",
    "runtime_entry_attempted_count",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_entry_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "api_surface_probe_status",
    "entry_decision",
    "entry_decision_reason",
    "runtime_entry_allowed",
    "runtime_entry_attempted",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_FALSE_FLAGS,
    "runtime_smoke_allowed",
    "runtime_smoke_attempted",
    "runtime_smoke_passed",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_ENTRY_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_smoke_recorded",
    "entry_decision_respected",
    "smoke_source_lineage_checked",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "smoke_action",
    "smoke_decision",
    "smoke_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_smoke_row_count",
    "source_newton_shape_runtime_engine_builder_entry_row_count",
    "runtime_smoke_allowed_count",
    "runtime_smoke_attempted_count",
    "runtime_smoke_passed_count",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_smoke_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_smoke_row_id",
    "source_newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "api_surface_probe_status",
    "entry_decision",
    "smoke_decision",
    "smoke_decision_reason",
    "smoke_observation_scope",
    "runtime_smoke_allowed",
    "runtime_smoke_attempted",
    "runtime_smoke_passed",
    "runtime_smoke_result_status",
    "runtime_execution_gate_required",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_FALSE_FLAGS,
    "runtime_execution_allowed",
    "runtime_execution_attempted",
    "runtime_execution_passed",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_SMOKE_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_runtime_execution_decision_recorded",
    "smoke_decision_respected",
    "runtime_execution_source_lineage_checked",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_execution_action",
    "runtime_execution_decision",
    "runtime_execution_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_runtime_execution_row_count",
    "source_newton_shape_runtime_engine_builder_smoke_row_count",
    "runtime_execution_allowed_count",
    "runtime_execution_attempted_count",
    "runtime_execution_passed_count",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_runtime_execution_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_runtime_execution_row_id",
    "source_newton_shape_runtime_engine_builder_smoke_row_id",
    "source_newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "api_surface_probe_status",
    "entry_decision",
    "smoke_decision",
    "runtime_smoke_result_status",
    "runtime_execution_decision",
    "runtime_execution_decision_reason",
    "runtime_execution_allowed",
    "runtime_execution_attempted",
    "runtime_execution_passed",
    "runtime_execution_result_status",
    "runtime_lane_review_gate_required",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_engine_shape_object_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_FALSE_FLAGS,
    "real_runtime_execution_evidence",
    "runtime_compatibility_validated",
    "configured_runtime_design_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_EXECUTION_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_runtime_lane_review_recorded",
    "runtime_execution_decision_reviewed",
    "runtime_lane_claim_boundary_preserved",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "runtime_lane_review_action",
    "runtime_lane_review_decision",
    "runtime_lane_review_status",
    "runtime_lane_review_reason",
    "runtime_lane_review_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_runtime_lane_review_row_count",
    "source_newton_shape_runtime_engine_builder_runtime_execution_row_count",
    "runtime_execution_allowed_count",
    "runtime_execution_attempted_count",
    "runtime_execution_passed_count",
    "runtime_lane_review_recorded_count",
    "runtime_lane_claim_boundary_preserved_count",
    "real_runtime_execution_evidence_count",
    "runtime_compatibility_validated_count",
    "real_runtime_execution_evidence",
    "runtime_compatibility_validated",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_runtime_lane_review_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_runtime_lane_review_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_execution_row_id",
    "source_newton_shape_runtime_engine_builder_smoke_row_id",
    "source_newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "api_surface_probe_status",
    "entry_decision",
    "smoke_decision",
    "runtime_smoke_result_status",
    "runtime_execution_decision",
    "runtime_execution_decision_reason",
    "runtime_execution_allowed",
    "runtime_execution_attempted",
    "runtime_execution_passed",
    "runtime_execution_result_status",
    "runtime_lane_review_decision",
    "runtime_lane_review_reason",
    "runtime_lane_review_status",
    "runtime_lane_review_recorded",
    "runtime_lane_claim_boundary_preserved",
    "configured_runtime_design_gate_required",
    "real_runtime_execution_evidence",
    "runtime_compatibility_validated",
    "configured_runtime_design_ready",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS,
    "configured_runtime_preflight_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_design_recorded",
    "runtime_lane_review_decision_respected",
    "configured_runtime_input_requirements_recorded",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "configured_runtime_design_action",
    "configured_runtime_design_decision",
    "configured_runtime_design_status",
    "configured_runtime_design_reason",
    "configured_runtime_design_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_configured_runtime_design_row_count",
    "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_count",
    "configured_runtime_design_recorded_count",
    "configured_runtime_preflight_ready_count",
    "runtime_source_configuration_required_count",
    "runtime_device_configuration_required_count",
    "runtime_entry_decision_required_count",
    "runtime_smoke_policy_required_count",
    "runtime_execution_policy_required_count",
    "required_config_keys",
    "required_runtime_inputs",
    "required_config_key_count",
    "required_runtime_input_count",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "configured_runtime_preflight_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_configured_runtime_design_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_configured_runtime_design_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_execution_row_id",
    "source_newton_shape_runtime_engine_builder_smoke_row_id",
    "source_newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "runtime_lane_review_decision",
    "runtime_lane_review_status",
    "configured_runtime_design_decision",
    "configured_runtime_design_reason",
    "configured_runtime_design_status",
    "configured_runtime_design_recorded",
    "configured_runtime_preflight_ready",
    "runtime_source_configuration_required",
    "runtime_device_configuration_required",
    "runtime_entry_decision_required",
    "runtime_smoke_policy_required",
    "runtime_execution_policy_required",
    "required_config_keys",
    "required_runtime_inputs",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "configured_runtime_preflight_gate_required",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS,
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "configured_runtime_validation_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DESIGN_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_preflight_recorded",
    "configured_runtime_design_contract_respected",
    "configured_runtime_preflight_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "configured_runtime_preflight_action",
    "configured_runtime_preflight_decision",
    "configured_runtime_preflight_status",
    "configured_runtime_preflight_reason",
    "configured_runtime_preflight_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_configured_runtime_preflight_row_count",
    "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_count",
    "configured_runtime_design_recorded_count",
    "configured_runtime_preflight_recorded_count",
    "configured_runtime_preflight_passed_count",
    "configured_runtime_validation_ready_count",
    "runtime_source_configuration_required_count",
    "runtime_device_configuration_required_count",
    "runtime_entry_decision_required_count",
    "runtime_smoke_policy_required_count",
    "runtime_execution_policy_required_count",
    "required_config_keys",
    "required_runtime_inputs",
    "required_config_key_count",
    "required_runtime_input_count",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "configured_runtime_preflight_ready",
    "configured_runtime_validation_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_configured_runtime_preflight_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_execution_row_id",
    "source_newton_shape_runtime_engine_builder_smoke_row_id",
    "source_newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "runtime_lane_review_decision",
    "runtime_lane_review_status",
    "configured_runtime_design_decision",
    "configured_runtime_design_status",
    "configured_runtime_design_recorded",
    "configured_runtime_preflight_decision",
    "configured_runtime_preflight_reason",
    "configured_runtime_preflight_status",
    "configured_runtime_preflight_recorded",
    "configured_runtime_preflight_passed",
    "configured_runtime_validation_ready",
    "runtime_source_configuration_required",
    "runtime_device_configuration_required",
    "runtime_entry_decision_required",
    "runtime_smoke_policy_required",
    "runtime_execution_policy_required",
    "required_config_keys",
    "required_runtime_inputs",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "configured_runtime_validation_gate_required",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS,
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_PREFLIGHT_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_validation_recorded",
    "configured_runtime_preflight_contract_respected",
    "configured_runtime_validation_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "configured_runtime_validation_action",
    "configured_runtime_validation_decision",
    "configured_runtime_validation_status",
    "configured_runtime_validation_reason",
    "configured_runtime_validation_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_configured_runtime_validation_row_count",
    "source_newton_shape_runtime_engine_builder_configured_runtime_preflight_row_count",
    "configured_runtime_preflight_recorded_count",
    "configured_runtime_preflight_passed_count",
    "configured_runtime_validation_recorded_count",
    "configured_runtime_validation_passed_count",
    "configured_runtime_validation_failed_count",
    "runtime_config_validated_count",
    "runtime_source_config_resolved_count",
    "runtime_device_config_resolved_count",
    "required_config_keys",
    "required_runtime_inputs",
    "required_config_key_count",
    "required_runtime_input_count",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "configured_runtime_preflight_ready",
    "configured_runtime_validation_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_status",
    "newton_diagnostic_device_config_key",
    "newton_diagnostic_device_configured",
    "newton_diagnostic_device",
    "newton_diagnostic_device_status",
    "newton_diagnostic_device_allowed_values",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_configured_runtime_validation_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_configured_runtime_validation_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_execution_row_id",
    "source_newton_shape_runtime_engine_builder_smoke_row_id",
    "source_newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "runtime_lane_review_decision",
    "runtime_lane_review_status",
    "configured_runtime_design_decision",
    "configured_runtime_design_status",
    "configured_runtime_design_recorded",
    "configured_runtime_preflight_decision",
    "configured_runtime_preflight_status",
    "configured_runtime_preflight_recorded",
    "configured_runtime_preflight_passed",
    "configured_runtime_validation_decision",
    "configured_runtime_validation_reason",
    "configured_runtime_validation_status",
    "configured_runtime_validation_recorded",
    "configured_runtime_validation_passed",
    "configured_runtime_validation_failed",
    "configured_runtime_validation_ready",
    "runtime_source_configuration_required",
    "runtime_device_configuration_required",
    "runtime_entry_decision_required",
    "runtime_smoke_policy_required",
    "runtime_execution_policy_required",
    "required_config_keys",
    "required_runtime_inputs",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_status",
    "newton_diagnostic_device_config_key",
    "newton_diagnostic_device_configured",
    "newton_diagnostic_device",
    "newton_diagnostic_device_status",
    "newton_diagnostic_device_allowed_values",
    "configured_runtime_source_resolution_gate_required",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS,
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_VALIDATION_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_recorded",
    "configured_runtime_validation_contract_respected",
    "configured_runtime_source_resolution_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "configured_runtime_source_resolution_action",
    "configured_runtime_source_resolution_decision",
    "configured_runtime_source_resolution_status",
    "configured_runtime_source_resolution_reason",
    "configured_runtime_source_resolution_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_count",
    "source_newton_shape_runtime_engine_builder_configured_runtime_validation_row_count",
    "configured_runtime_validation_recorded_count",
    "configured_runtime_validation_passed_count",
    "configured_runtime_validation_failed_count",
    "configured_runtime_source_resolution_recorded_count",
    "configured_runtime_source_resolution_passed_count",
    "configured_runtime_source_resolution_failed_count",
    "runtime_config_validated_count",
    "runtime_source_config_resolved_count",
    "runtime_device_config_resolved_count",
    "newton_source_dir_resolution_attempted_count",
    "newton_source_dir_configured_count",
    "newton_source_dir_resolved_count",
    "required_config_keys",
    "required_runtime_inputs",
    "required_config_key_count",
    "required_runtime_input_count",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "configured_runtime_preflight_ready",
    "configured_runtime_validation_ready",
    "configured_runtime_source_resolution_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_status",
    "newton_source_dir_resolution_attempted",
    "newton_source_dir_resolution_status",
    "newton_source_dir_resolution_reason",
    "newton_source_dir_filesystem_probe_allowed",
    "newton_source_dir_exists",
    "newton_diagnostic_device_config_key",
    "newton_diagnostic_device_configured",
    "newton_diagnostic_device",
    "newton_diagnostic_device_status",
    "newton_diagnostic_device_allowed_values",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_validation_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_execution_row_id",
    "source_newton_shape_runtime_engine_builder_smoke_row_id",
    "source_newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "runtime_lane_review_decision",
    "runtime_lane_review_status",
    "configured_runtime_design_decision",
    "configured_runtime_design_status",
    "configured_runtime_design_recorded",
    "configured_runtime_preflight_decision",
    "configured_runtime_preflight_status",
    "configured_runtime_preflight_recorded",
    "configured_runtime_preflight_passed",
    "configured_runtime_validation_decision",
    "configured_runtime_validation_reason",
    "configured_runtime_validation_status",
    "configured_runtime_validation_recorded",
    "configured_runtime_validation_passed",
    "configured_runtime_validation_failed",
    "configured_runtime_validation_ready",
    "configured_runtime_source_resolution_decision",
    "configured_runtime_source_resolution_reason",
    "configured_runtime_source_resolution_status",
    "configured_runtime_source_resolution_recorded",
    "configured_runtime_source_resolution_passed",
    "configured_runtime_source_resolution_failed",
    "configured_runtime_source_resolution_ready",
    "runtime_source_configuration_required",
    "runtime_device_configuration_required",
    "runtime_entry_decision_required",
    "runtime_smoke_policy_required",
    "runtime_execution_policy_required",
    "required_config_keys",
    "required_runtime_inputs",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_status",
    "newton_source_dir_resolution_attempted",
    "newton_source_dir_resolution_status",
    "newton_source_dir_resolution_reason",
    "newton_source_dir_filesystem_probe_allowed",
    "newton_source_dir_exists",
    "newton_diagnostic_device_config_key",
    "newton_diagnostic_device_configured",
    "newton_diagnostic_device",
    "newton_diagnostic_device_status",
    "newton_diagnostic_device_allowed_values",
    "configured_runtime_device_resolution_gate_required",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_RUNTIME_LANE_REVIEW_FALSE_FLAGS,
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SOURCE_RESOLUTION_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_recorded",
    "configured_runtime_source_resolution_contract_respected",
    "configured_runtime_device_resolution_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "configured_runtime_device_resolution_action",
    "configured_runtime_device_resolution_decision",
    "configured_runtime_device_resolution_status",
    "configured_runtime_device_resolution_reason",
    "configured_runtime_device_resolution_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_count",
    "source_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_count",
    "configured_runtime_source_resolution_recorded_count",
    "configured_runtime_source_resolution_passed_count",
    "configured_runtime_source_resolution_failed_count",
    "configured_runtime_device_resolution_recorded_count",
    "configured_runtime_device_resolution_passed_count",
    "configured_runtime_device_resolution_failed_count",
    "runtime_config_validated_count",
    "runtime_source_config_resolved_count",
    "runtime_device_config_resolved_count",
    "newton_source_dir_resolution_attempted_count",
    "newton_source_dir_configured_count",
    "newton_source_dir_resolved_count",
    "newton_diagnostic_device_resolution_attempted_count",
    "newton_diagnostic_device_configured_count",
    "newton_diagnostic_device_resolved_count",
    "required_config_keys",
    "required_runtime_inputs",
    "required_config_key_count",
    "required_runtime_input_count",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "configured_runtime_preflight_ready",
    "configured_runtime_validation_ready",
    "configured_runtime_source_resolution_ready",
    "configured_runtime_device_resolution_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_status",
    "newton_source_dir_resolution_attempted",
    "newton_source_dir_resolution_status",
    "newton_source_dir_resolution_reason",
    "newton_source_dir_filesystem_probe_allowed",
    "newton_source_dir_exists",
    "newton_diagnostic_device_config_key",
    "newton_diagnostic_device_configured",
    "newton_diagnostic_device",
    "newton_diagnostic_device_status",
    "newton_diagnostic_device_allowed_values",
    "newton_diagnostic_device_resolution_attempted",
    "newton_diagnostic_device_resolution_status",
    "newton_diagnostic_device_resolution_reason",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_ROW_REQUIRED_KEYS = {
    "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_source_resolution_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_validation_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_preflight_row_id",
    "source_newton_shape_runtime_engine_builder_configured_runtime_design_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_lane_review_row_id",
    "source_newton_shape_runtime_engine_builder_runtime_execution_row_id",
    "source_newton_shape_runtime_engine_builder_smoke_row_id",
    "source_newton_shape_runtime_engine_builder_entry_row_id",
    "source_newton_shape_runtime_engine_builder_api_surface_row_id",
    "source_newton_shape_runtime_engine_builder_environment_probe_row_id",
    "source_newton_shape_runtime_engine_builder_boundary_preflight_row_id",
    "source_newton_shape_runtime_builder_construction_row_id",
    "source_newton_shape_runtime_builder_preflight_row_id",
    "source_newton_shape_runtime_construction_row_id",
    "source_newton_shape_runtime_boundary_preflight_row_id",
    "source_shape_mapping_row_id",
    "source_newton_shape_mapping_preflight_row_id",
    "source_runtime_admissibility_row_id",
    "source_package_id",
    "source_asset_id",
    "fixture_id",
    "paper_primitive",
    "primitive_spec_kind",
    "primitive_id",
    "target_newton_shape_kind",
    "future_newton_builder_constructor_name",
    "future_newton_builder_method_name",
    "future_runtime_module_names",
    "runtime_lane_review_decision",
    "runtime_lane_review_status",
    "configured_runtime_design_decision",
    "configured_runtime_design_status",
    "configured_runtime_design_recorded",
    "configured_runtime_preflight_decision",
    "configured_runtime_preflight_status",
    "configured_runtime_preflight_recorded",
    "configured_runtime_preflight_passed",
    "configured_runtime_validation_decision",
    "configured_runtime_validation_reason",
    "configured_runtime_validation_status",
    "configured_runtime_validation_recorded",
    "configured_runtime_validation_passed",
    "configured_runtime_validation_failed",
    "configured_runtime_validation_ready",
    "configured_runtime_source_resolution_decision",
    "configured_runtime_source_resolution_reason",
    "configured_runtime_source_resolution_status",
    "configured_runtime_source_resolution_recorded",
    "configured_runtime_source_resolution_passed",
    "configured_runtime_source_resolution_failed",
    "configured_runtime_source_resolution_ready",
    "configured_runtime_device_resolution_decision",
    "configured_runtime_device_resolution_reason",
    "configured_runtime_device_resolution_status",
    "configured_runtime_device_resolution_recorded",
    "configured_runtime_device_resolution_passed",
    "configured_runtime_device_resolution_failed",
    "configured_runtime_device_resolution_ready",
    "runtime_source_configuration_required",
    "runtime_device_configuration_required",
    "runtime_entry_decision_required",
    "runtime_smoke_policy_required",
    "runtime_execution_policy_required",
    "required_config_keys",
    "required_runtime_inputs",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_status",
    "newton_source_dir_resolution_attempted",
    "newton_source_dir_resolution_status",
    "newton_source_dir_resolution_reason",
    "newton_source_dir_filesystem_probe_allowed",
    "newton_source_dir_exists",
    "newton_diagnostic_device_config_key",
    "newton_diagnostic_device_configured",
    "newton_diagnostic_device",
    "newton_diagnostic_device_status",
    "newton_diagnostic_device_allowed_values",
    "newton_diagnostic_device_resolution_attempted",
    "newton_diagnostic_device_resolution_status",
    "newton_diagnostic_device_resolution_reason",
    "configured_runtime_entry_decision_gate_required",
    "source_package_copy_forbidden",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_FALSE_FLAGS,
    "runtime_entry_allowed",
    "runtime_entry_attempted",
    "runtime_entry_passed",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_recorded",
    "configured_runtime_device_resolution_contract_respected",
    "configured_runtime_entry_decision_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "configured_runtime_entry_decision_action",
    "configured_runtime_entry_decision",
    "configured_runtime_entry_decision_status",
    "configured_runtime_entry_decision_reason",
    "configured_runtime_entry_decision_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_count",
    "source_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_count",
    "configured_runtime_source_resolution_recorded_count",
    "configured_runtime_source_resolution_passed_count",
    "configured_runtime_source_resolution_failed_count",
    "configured_runtime_device_resolution_recorded_count",
    "configured_runtime_device_resolution_passed_count",
    "configured_runtime_device_resolution_failed_count",
    "configured_runtime_entry_decision_recorded_count",
    "configured_runtime_entry_decision_passed_count",
    "configured_runtime_entry_decision_failed_count",
    "runtime_config_validated_count",
    "runtime_source_config_resolved_count",
    "runtime_device_config_resolved_count",
    "runtime_entry_allowed_count",
    "runtime_entry_attempted_count",
    "runtime_entry_passed_count",
    "newton_source_dir_resolution_attempted_count",
    "newton_source_dir_configured_count",
    "newton_source_dir_resolved_count",
    "newton_diagnostic_device_resolution_attempted_count",
    "newton_diagnostic_device_configured_count",
    "newton_diagnostic_device_resolved_count",
    "required_config_keys",
    "required_runtime_inputs",
    "required_config_key_count",
    "required_runtime_input_count",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "configured_runtime_preflight_ready",
    "configured_runtime_validation_ready",
    "configured_runtime_source_resolution_ready",
    "configured_runtime_device_resolution_ready",
    "configured_runtime_entry_decision_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "runtime_entry_allowed",
    "runtime_entry_attempted",
    "runtime_entry_passed",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_status",
    "newton_source_dir_resolution_attempted",
    "newton_source_dir_resolution_status",
    "newton_source_dir_resolution_reason",
    "newton_source_dir_filesystem_probe_allowed",
    "newton_source_dir_exists",
    "newton_diagnostic_device_config_key",
    "newton_diagnostic_device_configured",
    "newton_diagnostic_device",
    "newton_diagnostic_device_status",
    "newton_diagnostic_device_allowed_values",
    "newton_diagnostic_device_resolution_attempted",
    "newton_diagnostic_device_resolution_status",
    "newton_diagnostic_device_resolution_reason",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_ROW_REQUIRED_KEYS = (
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_DEVICE_RESOLUTION_ROW_REQUIRED_KEYS
    - {
        "newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id",
        "configured_runtime_entry_decision_gate_required",
    }
    | {
        "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_id",
        "source_newton_shape_runtime_engine_builder_configured_runtime_device_resolution_row_id",
        "configured_runtime_entry_decision",
        "configured_runtime_entry_decision_reason",
        "configured_runtime_entry_decision_status",
        "configured_runtime_entry_decision_recorded",
        "configured_runtime_entry_decision_passed",
        "configured_runtime_entry_decision_failed",
        "configured_runtime_entry_decision_ready",
        "runtime_entry_allowed",
        "runtime_entry_attempted",
        "runtime_entry_passed",
        "configured_runtime_smoke_gate_required",
    }
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_FALSE_FLAGS,
    "configured_runtime_smoke_allowed",
    "configured_runtime_smoke_attempted",
    "configured_runtime_smoke_passed",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_smoke_recorded",
    "configured_runtime_entry_decision_contract_respected",
    "configured_runtime_smoke_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "configured_runtime_smoke_action",
    "configured_runtime_smoke_decision",
    "configured_runtime_smoke_status",
    "configured_runtime_smoke_reason",
    "configured_runtime_smoke_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_configured_runtime_smoke_row_count",
    "source_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_count",
    "configured_runtime_source_resolution_recorded_count",
    "configured_runtime_source_resolution_passed_count",
    "configured_runtime_source_resolution_failed_count",
    "configured_runtime_device_resolution_recorded_count",
    "configured_runtime_device_resolution_passed_count",
    "configured_runtime_device_resolution_failed_count",
    "configured_runtime_entry_decision_recorded_count",
    "configured_runtime_entry_decision_passed_count",
    "configured_runtime_entry_decision_failed_count",
    "configured_runtime_smoke_recorded_count",
    "configured_runtime_smoke_passed_count",
    "configured_runtime_smoke_failed_count",
    "runtime_config_validated_count",
    "runtime_source_config_resolved_count",
    "runtime_device_config_resolved_count",
    "runtime_entry_allowed_count",
    "runtime_entry_attempted_count",
    "runtime_entry_passed_count",
    "configured_runtime_smoke_allowed_count",
    "configured_runtime_smoke_attempted_count",
    "configured_runtime_smoke_passed_count",
    "newton_source_dir_resolution_attempted_count",
    "newton_source_dir_configured_count",
    "newton_source_dir_resolved_count",
    "newton_diagnostic_device_resolution_attempted_count",
    "newton_diagnostic_device_configured_count",
    "newton_diagnostic_device_resolved_count",
    "required_config_keys",
    "required_runtime_inputs",
    "required_config_key_count",
    "required_runtime_input_count",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "configured_runtime_preflight_ready",
    "configured_runtime_validation_ready",
    "configured_runtime_source_resolution_ready",
    "configured_runtime_device_resolution_ready",
    "configured_runtime_entry_decision_ready",
    "configured_runtime_smoke_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "runtime_entry_allowed",
    "runtime_entry_attempted",
    "runtime_entry_passed",
    "configured_runtime_smoke_allowed",
    "configured_runtime_smoke_attempted",
    "configured_runtime_smoke_passed",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_status",
    "newton_source_dir_resolution_attempted",
    "newton_source_dir_resolution_status",
    "newton_source_dir_resolution_reason",
    "newton_source_dir_filesystem_probe_allowed",
    "newton_source_dir_exists",
    "newton_diagnostic_device_config_key",
    "newton_diagnostic_device_configured",
    "newton_diagnostic_device",
    "newton_diagnostic_device_status",
    "newton_diagnostic_device_allowed_values",
    "newton_diagnostic_device_resolution_attempted",
    "newton_diagnostic_device_resolution_status",
    "newton_diagnostic_device_resolution_reason",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_configured_runtime_smoke_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_ROW_REQUIRED_KEYS = (
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_ENTRY_DECISION_ROW_REQUIRED_KEYS
    - {
        "newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_id",
        "configured_runtime_smoke_gate_required",
    }
    | {
        "newton_shape_runtime_engine_builder_configured_runtime_smoke_row_id",
        "source_newton_shape_runtime_engine_builder_configured_runtime_entry_decision_row_id",
        "configured_runtime_smoke_decision",
        "configured_runtime_smoke_reason",
        "configured_runtime_smoke_status",
        "configured_runtime_smoke_recorded",
        "configured_runtime_smoke_passed",
        "configured_runtime_smoke_failed",
        "configured_runtime_smoke_ready",
        "configured_runtime_smoke_allowed",
        "configured_runtime_smoke_attempted",
        "configured_runtime_execution_gate_required",
    }
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_FALSE_FLAGS,
    "configured_runtime_execution_allowed",
    "configured_runtime_execution_attempted",
    "configured_runtime_execution_passed",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_execution_recorded",
    "configured_runtime_smoke_contract_respected",
    "configured_runtime_execution_ready",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_PAYLOAD_REQUIRED_KEYS = {
    "gate_id",
    "gate_status",
    "closed_gate",
    "input_gate_id",
    "next_required_gate",
    "decision",
    "decision_reason",
    "artifact_kind",
    "schema_version",
    "source_scope",
    "implementation_boundary",
    "configured_runtime_execution_action",
    "configured_runtime_execution_decision",
    "configured_runtime_execution_status",
    "configured_runtime_execution_reason",
    "configured_runtime_execution_contract",
    "input_contract_summary",
    "newton_shape_runtime_engine_builder_configured_runtime_execution_row_count",
    "source_newton_shape_runtime_engine_builder_configured_runtime_smoke_row_count",
    "configured_runtime_source_resolution_recorded_count",
    "configured_runtime_source_resolution_passed_count",
    "configured_runtime_source_resolution_failed_count",
    "configured_runtime_device_resolution_recorded_count",
    "configured_runtime_device_resolution_passed_count",
    "configured_runtime_device_resolution_failed_count",
    "configured_runtime_entry_decision_recorded_count",
    "configured_runtime_entry_decision_passed_count",
    "configured_runtime_entry_decision_failed_count",
    "configured_runtime_smoke_recorded_count",
    "configured_runtime_smoke_passed_count",
    "configured_runtime_smoke_failed_count",
    "configured_runtime_execution_recorded_count",
    "configured_runtime_execution_passed_count",
    "configured_runtime_execution_failed_count",
    "runtime_config_validated_count",
    "runtime_source_config_resolved_count",
    "runtime_device_config_resolved_count",
    "runtime_entry_allowed_count",
    "runtime_entry_attempted_count",
    "runtime_entry_passed_count",
    "configured_runtime_smoke_allowed_count",
    "configured_runtime_smoke_attempted_count",
    "configured_runtime_execution_allowed_count",
    "configured_runtime_execution_attempted_count",
    "newton_source_dir_resolution_attempted_count",
    "newton_source_dir_configured_count",
    "newton_source_dir_resolved_count",
    "newton_diagnostic_device_resolution_attempted_count",
    "newton_diagnostic_device_configured_count",
    "newton_diagnostic_device_resolved_count",
    "required_config_keys",
    "required_runtime_inputs",
    "required_config_key_count",
    "required_runtime_input_count",
    "runtime_entry_decision_policy",
    "runtime_smoke_policy",
    "runtime_execution_policy",
    "configured_runtime_preflight_ready",
    "configured_runtime_validation_ready",
    "configured_runtime_source_resolution_ready",
    "configured_runtime_device_resolution_ready",
    "configured_runtime_entry_decision_ready",
    "configured_runtime_smoke_ready",
    "configured_runtime_execution_ready",
    "runtime_config_validated",
    "runtime_source_config_resolved",
    "runtime_device_config_resolved",
    "runtime_entry_allowed",
    "runtime_entry_attempted",
    "runtime_entry_passed",
    "configured_runtime_smoke_allowed",
    "configured_runtime_smoke_attempted",
    "configured_runtime_smoke_passed",
    "configured_runtime_execution_allowed",
    "configured_runtime_execution_attempted",
    "configured_runtime_execution_passed",
    "newton_source_dir_config_key",
    "newton_source_dir_configured",
    "newton_source_dir",
    "newton_source_dir_status",
    "newton_source_dir_resolution_attempted",
    "newton_source_dir_resolution_status",
    "newton_source_dir_resolution_reason",
    "newton_source_dir_filesystem_probe_allowed",
    "newton_source_dir_exists",
    "newton_diagnostic_device_config_key",
    "newton_diagnostic_device_configured",
    "newton_diagnostic_device",
    "newton_diagnostic_device_status",
    "newton_diagnostic_device_allowed_values",
    "newton_diagnostic_device_resolution_attempted",
    "newton_diagnostic_device_resolution_status",
    "newton_diagnostic_device_resolution_reason",
    "real_newton_import_count",
    "real_warp_import_count",
    "newton_model_builder_instantiated_count",
    "newton_engine_shape_object_count",
    "newton_builder_shape_call_count",
    "newton_model_finalized_count",
    "newton_collision_pipeline_created_count",
    "newton_collision_pipeline_collide_count",
    "newton_runtime_execution_count",
    "newton_shape_runtime_engine_builder_configured_runtime_execution_rows",
    "coverage_summary",
    "remaining_gaps",
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_FALSE_FLAGS,
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_TRUE_FLAGS,
}

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_ROW_REQUIRED_KEYS = (
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_SMOKE_ROW_REQUIRED_KEYS
    - {
        "newton_shape_runtime_engine_builder_configured_runtime_smoke_row_id",
        "configured_runtime_execution_gate_required",
    }
    | {
        "newton_shape_runtime_engine_builder_configured_runtime_execution_row_id",
        "source_newton_shape_runtime_engine_builder_configured_runtime_smoke_row_id",
        "configured_runtime_execution_decision",
        "configured_runtime_execution_reason",
        "configured_runtime_execution_status",
        "configured_runtime_execution_recorded",
        "configured_runtime_execution_passed",
        "configured_runtime_execution_failed",
        "configured_runtime_execution_ready",
        "configured_runtime_execution_allowed",
        "configured_runtime_execution_attempted",
        "configured_runtime_lane_review_gate_required",
    }
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_FALSE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_FALSE_FLAGS,
    "real_runtime_execution_evidence",
    "runtime_compatibility_validated",
    "configured_runtime_run_allowed",
    "configured_runtime_run_attempted",
    "configured_runtime_run_passed",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_TRUE_FLAGS = (
    *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_TRUE_FLAGS,
    "newton_shape_runtime_engine_builder_configured_runtime_lane_review_recorded",
    "configured_runtime_execution_contract_respected",
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_PAYLOAD_REQUIRED_KEYS = (
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_PAYLOAD_REQUIRED_KEYS
    - {
        "configured_runtime_execution_action",
        "configured_runtime_execution_decision",
        "configured_runtime_execution_status",
        "configured_runtime_execution_reason",
        "configured_runtime_execution_contract",
        "newton_shape_runtime_engine_builder_configured_runtime_execution_row_count",
        "source_newton_shape_runtime_engine_builder_configured_runtime_smoke_row_count",
        "newton_shape_runtime_engine_builder_configured_runtime_execution_rows",
        *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_FALSE_FLAGS,
        *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_TRUE_FLAGS,
    }
    | {
        "configured_runtime_lane_review_action",
        "configured_runtime_lane_review_decision",
        "configured_runtime_lane_review_status",
        "configured_runtime_lane_review_reason",
        "configured_runtime_lane_review_contract",
        "newton_shape_runtime_engine_builder_configured_runtime_lane_review_row_count",
        "source_newton_shape_runtime_engine_builder_configured_runtime_execution_row_count",
        "configured_runtime_lane_review_recorded_count",
        "configured_runtime_lane_claim_boundary_preserved_count",
        "real_runtime_execution_evidence_count",
        "runtime_compatibility_validated_count",
        "configured_runtime_run_allowed_count",
        "configured_runtime_run_attempted_count",
        "configured_runtime_run_passed_count",
        "real_runtime_execution_evidence",
        "runtime_compatibility_validated",
        "configured_runtime_run_allowed",
        "configured_runtime_run_attempted",
        "configured_runtime_run_passed",
        "newton_shape_runtime_engine_builder_configured_runtime_lane_review_rows",
        *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_FALSE_FLAGS,
        *NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_TRUE_FLAGS,
    }
)

NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_LANE_REVIEW_ROW_REQUIRED_KEYS = (
    NEWTON_SHAPE_RUNTIME_ENGINE_BUILDER_CONFIGURED_RUNTIME_EXECUTION_ROW_REQUIRED_KEYS
    - {
        "newton_shape_runtime_engine_builder_configured_runtime_execution_row_id",
        "configured_runtime_lane_review_gate_required",
    }
    | {
        "newton_shape_runtime_engine_builder_configured_runtime_lane_review_row_id",
        "source_newton_shape_runtime_engine_builder_configured_runtime_execution_row_id",
        "configured_runtime_lane_review_decision",
        "configured_runtime_lane_review_reason",
        "configured_runtime_lane_review_status",
        "configured_runtime_lane_review_recorded",
        "configured_runtime_lane_claim_boundary_preserved",
        "configured_runtime_run_gate_required",
        "real_runtime_execution_evidence",
        "runtime_compatibility_validated",
        "configured_runtime_run_allowed",
        "configured_runtime_run_attempted",
        "configured_runtime_run_passed",
    }
)


def _all_candidate_source_rows(payload: dict[str, object]) -> list[dict[str, object]]:
    return (
        payload["native_template_candidate_source_audit_rows"]
        + payload["blocked_family_candidate_source_audit_rows"]
        + payload["noop_family_candidate_source_audit_rows"]
        + payload["current_row_candidate_source_audit_rows"]
    )


def _expected_runtime_constructed_primitivespec_dict(
    loaded_payload: dict[str, object],
) -> dict[str, object]:
    expected = dict(loaded_payload)
    expected["conversion_status"] = (
        "runtime_primitivespec_constructed_from_canonical_preflight_payload"
    )
    return expected


def _recursive_key_value_strings(value):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            yield str(key)
            yield from _recursive_key_value_strings(nested_value)
    elif isinstance(value, list | tuple):
        for item in value:
            yield from _recursive_key_value_strings(item)
    elif isinstance(value, str):
        yield value


def _recursive_keys(value):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            yield str(key)
            yield from _recursive_keys(nested_value)
    elif isinstance(value, list | tuple):
        for item in value:
            yield from _recursive_keys(item)


def _contains_callable(value: object) -> bool:
    if callable(value):
        return True
    if isinstance(value, dict):
        return any(_contains_callable(item) for item in value.values())
    if isinstance(value, list | tuple):
        return any(_contains_callable(item) for item in value)
    return False


def _recursive_package_dicts(value):
    if isinstance(value, dict):
        if {
            "package_id",
            "asset_id",
            "source_path",
            "source_sha256",
            "primitives",
            "fallback",
        }.issubset(value):
            yield value
        for nested_value in value.values():
            yield from _recursive_package_dicts(nested_value)
    elif isinstance(value, list | tuple):
        for item in value:
            yield from _recursive_package_dicts(item)


def _runtime_construction_input_with_canonical_payload_drift(
    mutate_payload,
) -> dict[str, object]:
    preflight = _runtime_construction_input()
    rows = [dict(row) for row in preflight["runtime_boundary_preflight_rows"]]
    payload = json.loads(rows[0]["canonical_primitivespec_json"])
    payload = mutate_payload(payload)
    rows[0]["canonical_primitivespec_json"] = json.dumps(
        payload,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    preflight["runtime_boundary_preflight_rows"] = rows
    return preflight


def _expected_builder_construction_recorded_call(
    mapping: dict[str, object],
) -> dict[str, object]:
    half_extents = mapping["dimensions"]["half_extents"]
    return {
        "method": "add_shape_box",
        "body": -1,
        "xform": {
            "kind": "fake_wp_transform",
            "translation": mapping["center"],
            "rotation": {
                "kind": "fake_wp_quat_from_matrix",
                "matrix": {
                    "kind": "fake_wp_matrix_from_cols",
                    "cols": mapping["axes"],
                },
            },
        },
        "hx": half_extents[0],
        "hy": half_extents[1],
        "hz": half_extents[2],
    }


__all__ = [name for name in globals() if not name.startswith("__")]
