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


@dataclass(frozen=True)
class _PolicySpec:
    label: str
    component_merge: str
    excess_volume_threshold_fraction: float | None = None


@dataclass(frozen=True)
class _SyntheticCase:
    case_id: str
    description: str
    expectation: str
    mesh: TriangleMesh
    policies: tuple[_PolicySpec, ...]


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
        max_primitives=1,
        primitive_subset=primitive_subset,
        component_merge=policy.component_merge,
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
    topology = policies["topology_only"]
    virtual = policies["virtual_pairwise"]
    topology_failures = set(topology["failure_labels"])
    virtual_failures = set(virtual["failure_labels"])
    return {
        "primitive_count_delta_virtual_minus_topology": int(
            virtual["primitive_count"] - topology["primitive_count"]
        ),
        "virtual_pairwise_clears_topology_failure_labels": bool(
            topology_failures and not virtual_failures
        ),
        "topology_failure_labels": sorted(topology_failures),
        "virtual_pairwise_failure_labels": sorted(virtual_failures),
    }


def _expectation_status(case_id: str, policies: dict[str, dict[str, object]]) -> str:
    topology = policies["topology_only"]
    virtual = policies["virtual_pairwise"]
    if case_id == "adjacent_square":
        matched = (
            topology["status"] == "smoke_passed"
            and virtual["status"] == "smoke_passed"
            and topology["primitive_count"] == 1
            and virtual["primitive_count"] == 1
        )
    elif case_id == "disconnected_pair":
        matched = (
            topology["status"] == "partial"
            and virtual["status"] == "smoke_passed"
            and topology["primitive_count"] == 2
            and virtual["primitive_count"] == 1
            and "unmerged_components" in topology["failure_labels"]
            and not virtual["failure_labels"]
        )
    elif case_id == "blocked_disconnected_pair":
        matched = (
            topology["status"] == "partial"
            and virtual["status"] == "partial"
            and "component_merge_blocked" in virtual["failure_labels"]
        )
    else:
        matched = False
    return "matched" if matched else "mismatched"


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
