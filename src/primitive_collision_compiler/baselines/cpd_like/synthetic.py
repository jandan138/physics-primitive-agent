from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.objective import (
    CPDLikeObjectiveOptions,
    build_cpd_like_objective_report,
)
from primitive_collision_compiler.geometry.mesh import TriangleMesh

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


def _policy_summary(
    case: _SyntheticCase,
    policy: _PolicySpec,
    *,
    primitive_subset: tuple[str, ...],
    options: CPDLikeObjectiveOptions,
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
    return {
        "status": objective["status"],
        "decomposition_stage": objective["decomposition_stage"],
        "primitive_count": primitive_budget["primitive_count"],
        "failure_labels": objective["failure_labels"],
        "primitive_budget": primitive_budget,
        "merge_excess_terms": merge_excess_terms,
        "component_accounting": component_accounting,
    }


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
