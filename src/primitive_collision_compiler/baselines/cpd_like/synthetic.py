from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import numpy as np

from primitive_collision_compiler.baselines.cpd_like.decompose import (
    MIN_NORMALIZATION_VOLUME,
    decompose_mesh,
)
from primitive_collision_compiler.baselines.cpd_like.objective import (
    CPDLikeObjectiveOptions,
    build_cpd_like_objective_report,
)
from primitive_collision_compiler.baselines.cpd_like.package import package_from_cpd_like_report
from primitive_collision_compiler.baselines.cpd_like.primitives import fit_primitive_candidates
from primitive_collision_compiler.geometry.mesh import TriangleMesh
from primitive_collision_compiler.newton.shapes import map_package_shapes

SYNTHETIC_COMPARISON_CLAIM_BOUNDARY = (
    "synthetic_objective_comparison_not_collision_quality_validation"
)
SYNTHETIC_COMPARISON_EVIDENCE_LEVEL = "offline_cpd_like_synthetic_comparison_smoke"
COST_GUIDED_SYNTHETIC_COMPARISON_CLAIM_BOUNDARY = (
    "cost_guided_synthetic_comparison_not_collision_quality_validation"
)
COST_GUIDED_SYNTHETIC_COMPARISON_EVIDENCE_LEVEL = (
    "offline_cpd_like_cost_guided_synthetic_comparison_smoke"
)
EXPECTED_FAILURE_WORKBENCH_CLAIM_BOUNDARY = (
    "synthetic_expected_failure_workbench_not_collision_quality_validation"
)
EXPECTED_FAILURE_WORKBENCH_EVIDENCE_LEVEL = (
    "offline_cpd_like_expected_failure_workbench_smoke"
)
EXPECTED_FAILURE_WORKBENCH_STATUS_SEMANTICS = (
    "expected_limitations_reported_not_decomposition_success"
)
NEWTON_NATIVE_FITTING_COMPARISON_CLAIM_BOUNDARY = (
    "native_fitting_comparison_not_collision_quality_validation"
)
NEWTON_NATIVE_FITTING_COMPARISON_EVIDENCE_LEVEL = (
    "offline_synthetic_native_fitting_comparison_smoke"
)
NATIVE_SELECTION_AUDIT_CLAIM_BOUNDARY = (
    "synthetic_selection_audit_not_paper_optimizer_or_collision_quality"
)
NATIVE_SELECTION_POLICY = "min_weighted_volume_surrogate_v0"
NATIVE_SELECTION_RULE = "min_raw_weighted_primitive_volume_tie_break_by_subset_order"
NATIVE_SELECTION_COST_NAME = "weighted_primitive_volume"
NATIVE_SELECTION_COST_UNITS = "source_mesh_volume_units"
NEWTON_NATIVE_LEGACY_SUBSET = ("box", "sphere", "capsule")
NEWTON_NATIVE_EXTENDED_SUBSET = (
    "box",
    "sphere",
    "capsule",
    "cylinder",
    "cone",
    "ellipsoid",
)


@dataclass(frozen=True)
class _PolicySpec:
    label: str
    component_merge: str
    merge_search_policy: str = "topology_then_virtual"
    excess_volume_threshold_fraction: float | None = None


@dataclass(frozen=True)
class _SyntheticCase:
    case_id: str
    description: str
    expectation: str
    mesh: TriangleMesh
    policies: tuple[_PolicySpec, ...]
    target_primitive_count: int = 1


@dataclass(frozen=True)
class _ExpectedFailureCase:
    case_id: str
    description: str
    paper_story_gap: str
    paper_gap_tags: tuple[str, ...]
    limitation_class: str
    next_capability_needed: str
    expected_diagnostic_flags: tuple[str, ...]
    mesh: TriangleMesh
    policy: _PolicySpec
    target_primitive_count: int = 1


@dataclass(frozen=True)
class _NativeFittingCase:
    case_id: str
    description: str
    expected_native_primitive: str
    mesh: TriangleMesh
    target_primitive_count: int = 1


def build_cpd_like_synthetic_comparison_report(
    *,
    primitive_subset: tuple[str, ...] = ("box",),
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=SYNTHETIC_COMPARISON_CLAIM_BOUNDARY,
        evidence_level=SYNTHETIC_COMPARISON_EVIDENCE_LEVEL,
    )
    case_payloads = [
        _case_payload(case, primitive_subset=primitive_subset, options=options)
        for case in _synthetic_cases()
    ]
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_synthetic_objective_comparison",
        "status": status,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "cases": case_payloads,
    }


def build_cpd_like_cost_guided_synthetic_comparison_report(
    *,
    primitive_subset: tuple[str, ...] = ("box",),
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=COST_GUIDED_SYNTHETIC_COMPARISON_CLAIM_BOUNDARY,
        evidence_level=COST_GUIDED_SYNTHETIC_COMPARISON_EVIDENCE_LEVEL,
    )
    case_payloads = [
        _case_payload(case, primitive_subset=primitive_subset, options=options)
        for case in _cost_guided_synthetic_cases()
    ]
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_cost_guided_synthetic_objective_comparison",
        "status": status,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "cases": case_payloads,
    }


def build_newton_native_fitting_comparison_report(
    *,
    legacy_subset: tuple[str, ...] = NEWTON_NATIVE_LEGACY_SUBSET,
    native_subset: tuple[str, ...] = NEWTON_NATIVE_EXTENDED_SUBSET,
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=NEWTON_NATIVE_FITTING_COMPARISON_CLAIM_BOUNDARY,
        evidence_level=NEWTON_NATIVE_FITTING_COMPARISON_EVIDENCE_LEVEL,
    )
    case_payloads = [
        _native_fitting_case_payload(
            case,
            legacy_subset=legacy_subset,
            native_subset=native_subset,
            options=options,
        )
        for case in _native_fitting_cases()
    ]
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_newton_native_fitting_comparison",
        "status": status,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "legacy_primitive_subset": list(legacy_subset),
        "native_primitive_subset": list(native_subset),
        "cases": case_payloads,
        "real_usd_scope": _real_usd_scope_payload(),
    }


def build_cpd_like_expected_failure_synthetic_workbench_report(
    *,
    primitive_subset: tuple[str, ...] = ("box",),
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=EXPECTED_FAILURE_WORKBENCH_CLAIM_BOUNDARY,
        evidence_level=EXPECTED_FAILURE_WORKBENCH_EVIDENCE_LEVEL,
    )
    case_payloads = [
        _expected_failure_case_payload(
            case,
            primitive_subset=primitive_subset,
            options=options,
        )
        for case in _expected_failure_cases()
    ]
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_expected_failure_synthetic_workbench",
        "status": status,
        "status_semantics": EXPECTED_FAILURE_WORKBENCH_STATUS_SEMANTICS,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "cases": case_payloads,
    }


def _synthetic_cases() -> tuple[_SyntheticCase, ...]:
    default_policies = (
        _PolicySpec(label="topology_only", component_merge="topology_only"),
        _PolicySpec(label="virtual_pairwise", component_merge="virtual_pairwise"),
    )
    return (
        _SyntheticCase(
            case_id="adjacent_square",
            description="Two adjacent triangles forming one square.",
            expectation="Both policies merge adjacent faces into one primitive.",
            mesh=_adjacent_square_mesh(),
            policies=default_policies,
        ),
        _SyntheticCase(
            case_id="disconnected_pair",
            description="Two separated triangles with no shared edge.",
            expectation=(
                "Topology-only remains partial; virtual pairwise component merge reaches one primitive."
            ),
            mesh=_disconnected_triangles_mesh(),
            policies=default_policies,
        ),
        _SyntheticCase(
            case_id="blocked_disconnected_pair",
            description="Separated triangles with virtual component merge threshold set to zero.",
            expectation="Virtual pairwise merge is blocked and reports component_merge_blocked.",
            mesh=_disconnected_triangles_mesh(),
            policies=(
                _PolicySpec(label="topology_only", component_merge="topology_only"),
                _PolicySpec(
                    label="virtual_pairwise",
                    component_merge="virtual_pairwise",
                    excess_volume_threshold_fraction=0.0,
                ),
            ),
        ),
    )


def _cost_guided_synthetic_cases() -> tuple[_SyntheticCase, ...]:
    return (
        _SyntheticCase(
            case_id="cost_guided_pair_choice",
            description=(
                "Three-face toy mesh where the cheapest merge-excess candidate is a virtual "
                "component pair rather than the available adjacent topology pair."
            ),
            expectation=(
                "The default policy takes the topology merge first; the cost-guided policy takes "
                "the lower-surrogate-cost virtual merge."
            ),
            mesh=_cost_guided_pair_choice_mesh(),
            policies=(
                _PolicySpec(
                    label="topology_then_virtual",
                    component_merge="virtual_pairwise",
                    merge_search_policy="topology_then_virtual",
                ),
                _PolicySpec(
                    label="cost_guided_pairwise",
                    component_merge="virtual_pairwise",
                    merge_search_policy="cost_guided_pairwise",
                ),
            ),
            target_primitive_count=2,
        ),
    )


def _native_fitting_cases() -> tuple[_NativeFittingCase, ...]:
    return (
        _NativeFittingCase(
            case_id="cylindrical_rod",
            description="Closed cylinder-like mesh with rings at both ends.",
            expected_native_primitive="cylinder",
            mesh=_cylindrical_rod_mesh(),
        ),
        _NativeFittingCase(
            case_id="tapered_cone",
            description="Cone-like mesh with one apex and one circular base ring.",
            expected_native_primitive="cone",
            mesh=_tapered_cone_mesh(),
        ),
        _NativeFittingCase(
            case_id="ellipsoid_blob",
            description="Axis-scaled octahedron used as an ellipsoid-like proxy fixture.",
            expected_native_primitive="ellipsoid",
            mesh=_ellipsoid_blob_mesh(),
        ),
        _NativeFittingCase(
            case_id="squat_cylinder",
            description="Short cylinder-like puck where cylinder fitting must choose the short axis.",
            expected_native_primitive="cylinder",
            mesh=_squat_cylinder_mesh(),
        ),
    )


def _expected_failure_cases() -> tuple[_ExpectedFailureCase, ...]:
    return (
        _ExpectedFailureCase(
            case_id="restricted_primitive_vocabulary_gap",
            description="Adjacent square under the current restricted primitive vocabulary.",
            paper_story_gap="restricted_primitive_vocabulary",
            paper_gap_tags=(
                "restricted_primitive_vocabulary",
                "paper_scope_primitive_fitting",
            ),
            limitation_class="expected_primitive_fit_gap",
            next_capability_needed="primitive_fit_extension",
            expected_diagnostic_flags=(
                "unsupported_paper_primitives_present",
                "paper_alignment_surrogate_not_paper_faithful",
            ),
            mesh=_adjacent_square_mesh(),
            policy=_PolicySpec(label="topology_only", component_merge="topology_only"),
        ),
        _ExpectedFailureCase(
            case_id="single_proxy_wraps_disconnected_components",
            description="Disconnected triangles merged into one proxy by virtual component merge.",
            paper_story_gap="empty_space_wrapping_proxy",
            paper_gap_tags=(
                "assigned_vertex_containment_proxy_only",
                "no_surface_distance_or_collision_benchmark",
            ),
            limitation_class="expected_empty_wrapper_proxy",
            next_capability_needed="primitive_fit_extension",
            expected_diagnostic_flags=(
                "unsupported_paper_primitives_present",
                "paper_alignment_surrogate_not_paper_faithful",
                "virtual_component_merge_used",
                "empty_space_wrap_proxy_present",
            ),
            mesh=_disconnected_triangles_mesh(),
            policy=_PolicySpec(label="virtual_pairwise", component_merge="virtual_pairwise"),
        ),
        _ExpectedFailureCase(
            case_id="threshold_blocks_component_merge",
            description="Disconnected triangles with virtual component merge threshold set to zero.",
            paper_story_gap="threshold_blocked_component_merge",
            paper_gap_tags=(
                "threshold_applies_only_to_virtual_component_merges",
                "candidate_graph_restricted",
            ),
            limitation_class="expected_threshold_block",
            next_capability_needed="merge_search_extension",
            expected_diagnostic_flags=(
                "unsupported_paper_primitives_present",
                "paper_alignment_surrogate_not_paper_faithful",
                "component_merge_blocked",
                "unmerged_components",
                "primitive_budget_not_met",
            ),
            mesh=_disconnected_triangles_mesh(),
            policy=_PolicySpec(
                label="virtual_pairwise",
                component_merge="virtual_pairwise",
                excess_volume_threshold_fraction=0.0,
            ),
        ),
    )


def _case_payload(
    case: _SyntheticCase,
    *,
    primitive_subset: tuple[str, ...],
    options: CPDLikeObjectiveOptions,
) -> dict[str, object]:
    policies = {
        policy.label: _policy_summary(
            case,
            policy,
            primitive_subset=primitive_subset,
            options=options,
        )
        for policy in case.policies
    }
    expectation_status = _expectation_status(case.case_id, policies)
    return {
        "case_id": case.case_id,
        "description": case.description,
        "expectation": case.expectation,
        "expectation_status": expectation_status,
        "policies": policies,
        "comparison": _comparison(policies),
    }


def _native_fitting_case_payload(
    case: _NativeFittingCase,
    *,
    legacy_subset: tuple[str, ...],
    native_subset: tuple[str, ...],
    options: CPDLikeObjectiveOptions,
) -> dict[str, object]:
    legacy = _native_fitting_policy_summary(
        case,
        label="legacy_box_sphere_capsule",
        primitive_subset=legacy_subset,
        options=options,
    )
    native = _native_fitting_policy_summary(
        case,
        label="native_six_kind",
        primitive_subset=native_subset,
        options=options,
    )
    comparison = _native_fitting_comparison(case, legacy, native)
    expectation_status = "matched" if comparison["expectation_matched"] else "mismatched"
    return {
        "case_id": case.case_id,
        "description": case.description,
        "expected_native_primitive": case.expected_native_primitive,
        "expectation_status": expectation_status,
        "legacy": legacy,
        "native": native,
        "comparison": comparison,
    }


def _native_fitting_policy_summary(
    case: _NativeFittingCase,
    *,
    label: str,
    primitive_subset: tuple[str, ...],
    options: CPDLikeObjectiveOptions,
) -> dict[str, object]:
    decomposition = decompose_mesh(
        case.mesh,
        max_primitives=case.target_primitive_count,
        primitive_subset=primitive_subset,
    )
    objective = build_cpd_like_objective_report(
        decomposition,
        asset_id=case.case_id,
        source_path=f"synthetic://{case.case_id}/{label}",
        options=options,
    ).to_dict()
    package = package_from_cpd_like_report(
        decomposition,
        asset_id=f"{case.case_id}_{label}",
        source_path=f"synthetic://{case.case_id}/{label}",
        claim_boundary=options.claim_boundary,
    )
    metrics = objective["metrics"]
    selected_kind = (
        decomposition.primitives[0].primitive_type if decomposition.primitives else ""
    )
    selected_source_faces = (
        set(decomposition.primitives[0].source_faces) if decomposition.primitives else set()
    )
    candidate_audit = _native_candidate_audit(
        case.mesh,
        primitive_subset=primitive_subset,
        selected_kind=selected_kind,
        normalizer_volume=float(metrics["geometric_excess_proxy"]["normalizer_volume"]),
    )
    return {
        "label": label,
        "status": objective["status"],
        "primitive_subset": list(primitive_subset),
        "selection_policy": NATIVE_SELECTION_POLICY,
        "selection_rule": NATIVE_SELECTION_RULE,
        "selection_cost_name": NATIVE_SELECTION_COST_NAME,
        "selection_cost_units": NATIVE_SELECTION_COST_UNITS,
        "candidate_audit_scope": "single_primitive_full_mesh_fixture",
        "candidate_audit_face_count": case.mesh.face_count,
        "candidate_audit_matches_selection_scope": bool(
            decomposition.primitive_count == 1
            and selected_source_faces == set(range(case.mesh.face_count))
        ),
        "candidate_audit": candidate_audit,
        "selected_candidate_rank": _selected_candidate_rank(candidate_audit),
        "selected_primitive_kind": selected_kind,
        "primitive_count": decomposition.primitive_count,
        "failure_labels": objective["failure_labels"],
        "geometric_excess_proxy": metrics["geometric_excess_proxy"],
        "paper_primitive_gap": metrics["paper_primitive_gap"],
        "package_mapping": _package_mapping_summary(package),
    }


def _native_candidate_audit(
    mesh: TriangleMesh,
    *,
    primitive_subset: tuple[str, ...],
    selected_kind: str,
    normalizer_volume: float,
) -> list[dict[str, object]]:
    normalizer = max(float(normalizer_volume), MIN_NORMALIZATION_VOLUME)
    candidates = fit_primitive_candidates(
        mesh,
        frozenset(range(mesh.face_count)),
        primitive_subset,
    )
    rows: list[tuple[float, int, dict[str, object]]] = []
    for candidate_order, candidate in enumerate(candidates):
        normalized_weighted_volume = float(candidate.weighted_volume / normalizer)
        rows.append(
            (
                candidate.weighted_volume,
                candidate_order,
                {
                    "primitive_type": candidate.primitive_type,
                    "candidate_order": candidate_order,
                    "selection_objective": NATIVE_SELECTION_COST_NAME,
                    "selection_objective_units": "raw_weighted_primitive_volume_proxy",
                    "volume": candidate.volume,
                    "weighted_volume": candidate.weighted_volume,
                    "normalized_weighted_volume": normalized_weighted_volume,
                    "contains_assigned_points": candidate.contains_assigned_points,
                    "dimensions": candidate.dimensions,
                    "selected": candidate.primitive_type == selected_kind,
                },
            )
        )
    return [
        {
            **row,
            "rank": rank,
        }
        for rank, (_, _, row) in enumerate(
            sorted(rows, key=lambda item: (item[0], item[1])),
            start=1,
        )
    ]


def _selected_candidate_rank(candidate_audit: list[dict[str, object]]) -> int | None:
    for candidate in candidate_audit:
        if candidate["selected"]:
            return int(candidate["rank"])
    return None


def _package_mapping_summary(package) -> dict[str, object]:
    mappings = map_package_shapes(package)
    status_counts = dict(Counter(mapping.status for mapping in mappings))
    return {
        "package_id": package.package_id,
        "primitive_kinds": [primitive.kind for primitive in package.primitives],
        "status_counts": status_counts,
        "mapping_details": [mapping.to_dict() for mapping in mappings],
    }


def _native_fitting_comparison(
    case: _NativeFittingCase,
    legacy: dict[str, object],
    native: dict[str, object],
) -> dict[str, object]:
    legacy_volume = float(
        legacy["geometric_excess_proxy"]["normalized_weighted_primitive_volume"]
    )
    native_volume = float(
        native["geometric_excess_proxy"]["normalized_weighted_primitive_volume"]
    )
    native_selected_extension = (
        native["selected_primitive_kind"] == case.expected_native_primitive
        and native["selected_primitive_kind"] not in set(legacy["primitive_subset"])
    )
    native_fully_mapped = native["package_mapping"]["status_counts"] == {"mapped": 1}
    legacy_candidates = legacy["candidate_audit"]
    native_candidates = native["candidate_audit"]
    legacy_best_cost = _best_candidate_normalized_cost(legacy_candidates)
    native_best_cost = _best_candidate_normalized_cost(native_candidates)
    native_next_cost = _next_candidate_normalized_cost(native_candidates)
    native_cost_explained = bool(
        native["selected_candidate_rank"] == 1
        and native_candidates
        and native_candidates[0]["selected"] is True
        and native_candidates[0]["primitive_type"] == native["selected_primitive_kind"]
    )
    return {
        "native_selected_newton_extension": native_selected_extension,
        "native_package_fully_mapped": native_fully_mapped,
        "native_normalized_volume_delta": float(native_volume - legacy_volume),
        "legacy_normalized_weighted_volume": legacy_volume,
        "native_normalized_weighted_volume": native_volume,
        "native_selection_margin_vs_legacy_best": float(native_best_cost - legacy_best_cost),
        "native_selection_margin_vs_next_native_candidate": (
            None if native_next_cost is None else float(native_best_cost - native_next_cost)
        ),
        "native_selected_kind_cost_explained": native_cost_explained,
        "selection_claim_boundary": NATIVE_SELECTION_AUDIT_CLAIM_BOUNDARY,
        "expectation_matched": bool(
            native_selected_extension
            and native_fully_mapped
            and native_volume <= legacy_volume
            and native_cost_explained
        ),
    }


def _best_candidate_normalized_cost(candidate_audit: list[dict[str, object]]) -> float:
    if not candidate_audit:
        return 0.0
    return float(candidate_audit[0]["normalized_weighted_volume"])


def _next_candidate_normalized_cost(candidate_audit: list[dict[str, object]]) -> float | None:
    if len(candidate_audit) < 2:
        return None
    return float(candidate_audit[1]["normalized_weighted_volume"])


def _real_usd_scope_payload() -> dict[str, object]:
    return {
        "status": "scope_declared_not_run",
        "manifest": "assets/manifests/cpd_like_smoke_assets.yaml",
        "claim_boundary": "real_usd_scope_manifest_only_not_experiment_evidence",
        "assets": [
            {
                "role": "bed_dev_smoke",
                "asset_family": "furniture",
                "max_source_faces": 256,
                "purpose": "bed_usd_cpd_like_geometry_scope",
            },
            {
                "role": "franka_import_smoke",
                "asset_family": "robot",
                "max_source_faces": 128,
                "purpose": "franka_usd_cpd_like_geometry_scope",
            },
        ],
    }


def _squat_cylinder_mesh(segment_count: int = 16) -> TriangleMesh:
    radius = 1.0
    height = 0.1
    points: list[list[float]] = []
    for z in (-height * 0.5, height * 0.5):
        for index in range(segment_count):
            angle = 2.0 * np.pi * index / segment_count
            points.append([radius * np.cos(angle), radius * np.sin(angle), z])
    bottom_center = len(points)
    points.append([0.0, 0.0, -height * 0.5])
    top_center = len(points)
    points.append([0.0, 0.0, height * 0.5])

    faces: list[list[int]] = []
    for index in range(segment_count):
        next_index = (index + 1) % segment_count
        bottom_left = index
        bottom_right = next_index
        top_left = segment_count + index
        top_right = segment_count + next_index
        faces.append([bottom_left, bottom_right, top_right])
        faces.append([bottom_left, top_right, top_left])
        faces.append([bottom_center, bottom_right, bottom_left])
        faces.append([top_center, top_left, top_right])
    return TriangleMesh(points=np.asarray(points, dtype=float), faces=np.asarray(faces, dtype=int))


def _expected_failure_case_payload(
    case: _ExpectedFailureCase,
    *,
    primitive_subset: tuple[str, ...],
    options: CPDLikeObjectiveOptions,
) -> dict[str, object]:
    policy = _policy_summary(
        _SyntheticCase(
            case_id=case.case_id,
            description=case.description,
            expectation="Expected diagnostic flags should be observed.",
            mesh=case.mesh,
            policies=(case.policy,),
            target_primitive_count=case.target_primitive_count,
        ),
        case.policy,
        primitive_subset=primitive_subset,
        options=options,
        include_extended_metrics=True,
    )
    expected = list(case.expected_diagnostic_flags)
    observed = _diagnostic_flags(policy)
    missing = [flag for flag in expected if flag not in observed]
    unexpected = [flag for flag in observed if flag not in expected]
    match_status = "matched" if not missing and not unexpected else "mismatched"
    return {
        "case_id": case.case_id,
        "description": case.description,
        "paper_story_gap": case.paper_story_gap,
        "paper_gap_tags": list(case.paper_gap_tags),
        "limitation_class": case.limitation_class,
        "next_capability_needed": case.next_capability_needed,
        "fixture_geometry_summary": _fixture_geometry_summary(case.mesh, policy),
        "expected_diagnostic_flags": {
            "expected": expected,
            "observed": observed,
            "missing": missing,
            "unexpected": unexpected,
            "match_status": match_status,
        },
        "expectation_status": match_status,
        "policy": policy,
        "metrics": {
            "primitive_budget": policy["primitive_budget"],
            "merge_excess_terms": policy["merge_excess_terms"],
            "component_accounting": policy["component_accounting"],
            "paper_primitive_gap": policy["paper_primitive_gap"],
            "paper_alignment": policy["paper_alignment"],
        },
    }


def _policy_summary(
    case: _SyntheticCase,
    policy: _PolicySpec,
    *,
    primitive_subset: tuple[str, ...],
    options: CPDLikeObjectiveOptions,
    include_extended_metrics: bool = False,
) -> dict[str, object]:
    decomposition = decompose_mesh(
        case.mesh,
        max_primitives=case.target_primitive_count,
        primitive_subset=primitive_subset,
        component_merge=policy.component_merge,
        merge_search_policy=policy.merge_search_policy,
        excess_volume_threshold_fraction=policy.excess_volume_threshold_fraction,
    )
    objective = build_cpd_like_objective_report(
        decomposition,
        asset_id=case.case_id,
        source_path=f"synthetic://{case.case_id}/{policy.label}",
        options=options,
    ).to_dict()
    primitive_budget = objective["metrics"]["primitive_budget"]
    merge_excess_terms = objective["metrics"]["merge_excess_terms"]
    component_accounting = objective["metrics"]["component_accounting"]
    paper_alignment = objective["metrics"]["paper_alignment"]
    summary = {
        "status": objective["status"],
        "decomposition_stage": objective["decomposition_stage"],
        "primitive_count": primitive_budget["primitive_count"],
        "failure_labels": objective["failure_labels"],
        "primitive_budget": primitive_budget,
        "merge_excess_terms": merge_excess_terms,
        "component_accounting": component_accounting,
        "paper_alignment": paper_alignment,
    }
    if include_extended_metrics:
        summary["geometric_excess_proxy"] = objective["metrics"]["geometric_excess_proxy"]
        summary["paper_primitive_gap"] = objective["metrics"]["paper_primitive_gap"]
    return summary


def _diagnostic_flags(policy: dict[str, object]) -> list[str]:
    flags: list[str] = []
    paper_alignment = policy["paper_alignment"]
    paper_primitive_gap = policy["paper_primitive_gap"]
    merge_excess_terms = policy["merge_excess_terms"]
    component_accounting = policy["component_accounting"]
    failure_labels = set(policy["failure_labels"])

    if paper_primitive_gap["unsupported_paper_primitive_count"] > 0:
        flags.append("unsupported_paper_primitives_present")
    if paper_alignment["paper_faithfulness"] == "surrogate_not_paper_faithful":
        flags.append("paper_alignment_surrogate_not_paper_faithful")
    if component_accounting["virtual_component_merge_count"] > 0:
        flags.append("virtual_component_merge_used")
    if (
        component_accounting["virtual_component_merge_count"] > 0
        and float(merge_excess_terms["accepted_eq4_cost_sum"] or 0.0) > 0.0
    ):
        flags.append("empty_space_wrap_proxy_present")
    if "component_merge_blocked" in failure_labels:
        flags.append("component_merge_blocked")
    if "unmerged_components" in failure_labels:
        flags.append("unmerged_components")
    if "primitive_budget_not_met" in failure_labels:
        flags.append("primitive_budget_not_met")
    return flags


def _fixture_geometry_summary(
    mesh: TriangleMesh,
    policy: dict[str, object],
) -> dict[str, object]:
    mesh_aabb_volume = float(policy["geometric_excess_proxy"]["mesh_aabb_volume"])
    return {
        "point_count": int(mesh.points.shape[0]),
        "face_count": mesh.face_count,
        "connected_component_count": _connected_component_count(mesh),
        "mesh_aabb_volume": mesh_aabb_volume,
        "normalizer_floor_applied": bool(mesh_aabb_volume < MIN_NORMALIZATION_VOLUME),
    }


def _connected_component_count(mesh: TriangleMesh) -> int:
    adjacency = mesh.adjacent_faces()
    unseen = set(adjacency)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            face_id = stack.pop()
            for neighbor in adjacency[face_id]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
    return count


def _comparison(policies: dict[str, dict[str, object]]) -> dict[str, object]:
    if {"topology_then_virtual", "cost_guided_pairwise"}.issubset(policies):
        default = policies["topology_then_virtual"]
        cost_guided = policies["cost_guided_pairwise"]
        default_excess = _accepted_excess_sum(default)
        cost_guided_excess = _accepted_excess_sum(cost_guided)
        default_components = default["component_accounting"]
        cost_guided_components = cost_guided["component_accounting"]
        return {
            "cost_guided_chose_virtual_instead_of_topology": bool(
                default_components["topology_merge_count"] == 1
                and default_components["virtual_component_merge_count"] == 0
                and cost_guided_components["topology_merge_count"] == 0
                and cost_guided_components["virtual_component_merge_count"] == 1
            ),
            "cost_guided_accepted_excess_delta": float(
                cost_guided_excess - default_excess
            ),
            "topology_then_virtual_accepted_normalized_excess_sum": default_excess,
            "cost_guided_accepted_normalized_excess_sum": cost_guided_excess,
            "topology_then_virtual_failure_labels": sorted(default["failure_labels"]),
            "cost_guided_pairwise_failure_labels": sorted(cost_guided["failure_labels"]),
        }

    topology = policies["topology_only"]
    virtual = policies["virtual_pairwise"]
    topology_failures = set(topology["failure_labels"])
    virtual_failures = set(virtual["failure_labels"])
    return {
        "primitive_count_delta_virtual_minus_topology": int(
            virtual["primitive_count"] - topology["primitive_count"]
        ),
        "virtual_pairwise_omits_topology_unmerged_component_label": bool(
            "unmerged_components" in topology_failures
            and "unmerged_components" not in virtual_failures
        ),
        "topology_failure_labels": sorted(topology_failures),
        "virtual_pairwise_failure_labels": sorted(virtual_failures),
    }


def _expectation_status(case_id: str, policies: dict[str, dict[str, object]]) -> str:
    if case_id == "adjacent_square":
        topology = policies["topology_only"]
        virtual = policies["virtual_pairwise"]
        matched = (
            topology["status"] == "smoke_passed"
            and virtual["status"] == "smoke_passed"
            and topology["primitive_count"] == 1
            and virtual["primitive_count"] == 1
        )
    elif case_id == "disconnected_pair":
        topology = policies["topology_only"]
        virtual = policies["virtual_pairwise"]
        matched = (
            topology["status"] == "partial"
            and virtual["status"] == "smoke_passed"
            and topology["primitive_count"] == 2
            and virtual["primitive_count"] == 1
            and "unmerged_components" in topology["failure_labels"]
            and not virtual["failure_labels"]
        )
    elif case_id == "blocked_disconnected_pair":
        topology = policies["topology_only"]
        virtual = policies["virtual_pairwise"]
        matched = (
            topology["status"] == "partial"
            and virtual["status"] == "partial"
            and "component_merge_blocked" in virtual["failure_labels"]
        )
    elif case_id == "cost_guided_pair_choice":
        default = policies["topology_then_virtual"]
        cost_guided = policies["cost_guided_pairwise"]
        default_components = default["component_accounting"]
        cost_guided_components = cost_guided["component_accounting"]
        matched = (
            default["status"] == "smoke_passed"
            and cost_guided["status"] == "smoke_passed"
            and default_components["topology_merge_count"] == 1
            and default_components["virtual_component_merge_count"] == 0
            and cost_guided_components["topology_merge_count"] == 0
            and cost_guided_components["virtual_component_merge_count"] == 1
            and _accepted_excess_sum(cost_guided) < _accepted_excess_sum(default)
        )
    else:
        matched = False
    return "matched" if matched else "mismatched"


def _accepted_excess_sum(policy_summary: dict[str, object]) -> float:
    value = policy_summary["merge_excess_terms"]["accepted_normalized_excess_sum"]
    return 0.0 if value is None else float(value)


def _adjacent_square_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [0, 2, 3]]),
    )


def _disconnected_triangles_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [4.0, 0.0, 0.0],
                [5.0, 0.0, 0.0],
                [4.0, 1.0, 0.0],
            ]
        ),
        faces=np.array([[0, 1, 2], [3, 4, 5]]),
    )


def _cost_guided_pair_choice_mesh() -> TriangleMesh:
    return TriangleMesh(
        points=np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [10.0, 10.0, 10.0],
                [0.05, 0.05, 0.05],
                [1.05, 0.05, 0.05],
                [0.05, 1.05, 0.05],
            ]
        ),
        faces=np.array([[0, 1, 2], [1, 2, 3], [4, 5, 6]]),
    )


def _cylindrical_rod_mesh(segments: int = 12) -> TriangleMesh:
    bottom_z = -2.0
    top_z = 2.0
    radius = 0.4
    points: list[tuple[float, float, float]] = []
    for z in (bottom_z, top_z):
        for index in range(segments):
            angle = 2.0 * np.pi * index / segments
            points.append((radius * float(np.cos(angle)), radius * float(np.sin(angle)), z))
    bottom_center = len(points)
    points.append((0.0, 0.0, bottom_z))
    top_center = len(points)
    points.append((0.0, 0.0, top_z))

    faces: list[tuple[int, int, int]] = []
    for index in range(segments):
        next_index = (index + 1) % segments
        bottom_a = index
        bottom_b = next_index
        top_a = segments + index
        top_b = segments + next_index
        faces.append((bottom_a, bottom_b, top_b))
        faces.append((bottom_a, top_b, top_a))
        faces.append((bottom_center, bottom_b, bottom_a))
        faces.append((top_center, top_a, top_b))
    return TriangleMesh(points=np.asarray(points), faces=np.asarray(faces))


def _tapered_cone_mesh(segments: int = 12) -> TriangleMesh:
    base_z = -2.0
    apex_z = 2.0
    radius = 0.8
    points: list[tuple[float, float, float]] = [(0.0, 0.0, apex_z)]
    for index in range(segments):
        angle = 2.0 * np.pi * index / segments
        points.append((radius * float(np.cos(angle)), radius * float(np.sin(angle)), base_z))
    base_center = len(points)
    points.append((0.0, 0.0, base_z))

    faces: list[tuple[int, int, int]] = []
    for index in range(segments):
        current_index = 1 + index
        next_index = 1 + ((index + 1) % segments)
        faces.append((0, current_index, next_index))
        faces.append((base_center, next_index, current_index))
    return TriangleMesh(points=np.asarray(points), faces=np.asarray(faces))


def _ellipsoid_blob_mesh() -> TriangleMesh:
    points = np.asarray(
        [
            (1.2, 0.0, 0.0),
            (-1.2, 0.0, 0.0),
            (0.0, 0.5, 0.0),
            (0.0, -0.5, 0.0),
            (0.0, 0.0, 0.25),
            (0.0, 0.0, -0.25),
        ]
    )
    faces = np.asarray(
        [
            (0, 2, 4),
            (2, 1, 4),
            (1, 3, 4),
            (3, 0, 4),
            (2, 0, 5),
            (1, 2, 5),
            (3, 1, 5),
            (0, 3, 5),
        ]
    )
    return TriangleMesh(points=points, faces=faces)
