from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping

from primitive_collision_compiler.baselines.cpd_like.decompose import CPDLikeDecompositionReport

DEFAULT_CLAIM_BOUNDARY = "offline_objective_report_not_collision_quality_validation"
DEFAULT_EVIDENCE_LEVEL = "offline_cpd_like_objective_smoke"
DEFAULT_OBJECTIVE_VERSION = "cpd_paper_aligned_surrogate_v0"
MIN_NORMALIZER_VOLUME = 1e-12


@dataclass(frozen=True)
class CPDLikeObjectiveOptions:
    objective_version: str = DEFAULT_OBJECTIVE_VERSION
    primitive_type_weights: Mapping[str, float] | None = None
    claim_boundary: str = DEFAULT_CLAIM_BOUNDARY
    evidence_level: str = DEFAULT_EVIDENCE_LEVEL


@dataclass(frozen=True)
class CPDLikeObjectiveReport:
    stage: str
    status: str
    asset_id: str
    source_path: str
    decomposition_stage: str
    objective_version: str
    claim_boundary: str
    evidence_level: str
    metrics: dict[str, object]
    failure_labels: tuple[str, ...]
    decomposition: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "stage": self.stage,
            "status": self.status,
            "asset_id": self.asset_id,
            "source_path": self.source_path,
            "decomposition_stage": self.decomposition_stage,
            "objective_version": self.objective_version,
            "claim_boundary": self.claim_boundary,
            "evidence_level": self.evidence_level,
            "metrics": self.metrics,
            "failure_labels": list(self.failure_labels),
            "decomposition": self.decomposition,
        }


def build_cpd_like_objective_report(
    decomposition: CPDLikeDecompositionReport,
    *,
    asset_id: str,
    source_path: str,
    max_source_faces: int | None = None,
    options: CPDLikeObjectiveOptions | None = None,
) -> CPDLikeObjectiveReport:
    options = options or CPDLikeObjectiveOptions()
    primitive_type_weights = _validated_weights(options.primitive_type_weights)
    normalizer_volume = max(float(decomposition.mesh_aabb_volume), MIN_NORMALIZER_VOLUME)
    total_primitive_volume = float(sum(primitive.volume for primitive in decomposition.primitives))
    weighted_primitive_volume = float(
        sum(
            primitive.volume * primitive_type_weights.get(primitive.primitive_type, 1.0)
            for primitive in decomposition.primitives
        )
    )
    contained_primitive_count = sum(
        1 for primitive in decomposition.primitives if primitive.contains_assigned_points
    )
    uncontained_primitive_count = decomposition.primitive_count - contained_primitive_count
    over_budget_count = max(decomposition.primitive_count - decomposition.target_primitive_count, 0)
    merge_cost_summary = dict(decomposition.merge_cost_summary)
    failure_labels = _failure_labels(
        decomposition=decomposition,
        over_budget_count=over_budget_count,
        uncontained_primitive_count=uncontained_primitive_count,
    )
    status = "smoke_passed" if decomposition.status == "smoke_passed" and not failure_labels else "partial"

    metrics = {
        "primitive_budget": {
            "primitive_count": decomposition.primitive_count,
            "target_primitive_count": decomposition.target_primitive_count,
            "within_budget": over_budget_count == 0,
            "over_budget_count": over_budget_count,
            "primitive_count_pressure": float(
                decomposition.primitive_count / max(decomposition.target_primitive_count, 1)
            ),
        },
        "geometric_excess_proxy": {
            "total_primitive_volume": total_primitive_volume,
            "weighted_primitive_volume": weighted_primitive_volume,
            "mesh_aabb_volume": decomposition.mesh_aabb_volume,
            "normalizer_volume": normalizer_volume,
            "normalized_total_primitive_volume": float(total_primitive_volume / normalizer_volume),
            "normalized_weighted_primitive_volume": float(
                weighted_primitive_volume / normalizer_volume
            ),
            "source_normalized_total_weighted_volume": decomposition.normalized_total_weighted_volume,
        },
        "merge_excess_terms": {
            "accepted_merge_count": merge_cost_summary.get("accepted_merge_count", 0),
            "accepted_normalized_excess_sum": merge_cost_summary.get(
                "accepted_normalized_excess_sum",
                None,
            ),
            "accepted_normalized_excess_max": merge_cost_summary.get(
                "accepted_normalized_excess_max",
                None,
            ),
            "blocked_merge_count": decomposition.blocked_merge_count,
            "blocked_normalized_excess_max": merge_cost_summary.get(
                "blocked_normalized_excess_max",
                None,
            ),
        },
        "containment": {
            "contained_primitive_count": contained_primitive_count,
            "uncontained_primitive_count": uncontained_primitive_count,
            "containment_ratio": float(
                contained_primitive_count / max(decomposition.primitive_count, 1)
            ),
        },
        "paper_primitive_gap": {
            "current_primitive_subset": list(decomposition.primitive_subset),
            "unsupported_paper_primitives": list(decomposition.unsupported_primitives),
            "unsupported_paper_primitive_count": len(decomposition.unsupported_primitives),
        },
        "component_accounting": {
            "merge_policy": decomposition.merge_policy,
            "merge_search_policy": decomposition.merge_search_policy,
            "initial_component_count": decomposition.initial_component_count,
            "final_component_count": decomposition.final_component_count,
            "topology_merge_count": decomposition.topology_merge_count,
            "virtual_component_merge_count": decomposition.virtual_component_merge_count,
            "blocked_merge_count": decomposition.blocked_merge_count,
            "fallback_reason": decomposition.fallback_reason,
        },
        "primitive_type_weights": primitive_type_weights,
    }

    return CPDLikeObjectiveReport(
        stage="cpd_like_offline_objective",
        status=status,
        asset_id=asset_id,
        source_path=source_path,
        decomposition_stage=decomposition.stage,
        objective_version=str(options.objective_version),
        claim_boundary=str(options.claim_boundary),
        evidence_level=str(options.evidence_level),
        metrics=metrics,
        failure_labels=failure_labels,
        decomposition={
            "stage": decomposition.stage,
            "status": decomposition.status,
            "primitive_count": decomposition.primitive_count,
            "max_primitives": decomposition.max_primitives,
            "mesh_point_count": decomposition.mesh_point_count,
            "mesh_face_count": decomposition.mesh_face_count,
            "merge_policy": decomposition.merge_policy,
            "fallback_reason": decomposition.fallback_reason,
            "max_source_faces": max_source_faces,
        },
    )


def _validated_weights(value: Mapping[str, float] | None) -> dict[str, float]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError("cpd_like_objective.primitive_type_weights must be a mapping")
    result: dict[str, float] = {}
    for primitive_type, raw_weight in value.items():
        primitive_name = str(primitive_type)
        if not primitive_name:
            raise ValueError("cpd_like_objective.primitive_type_weights keys must be non-empty")
        try:
            weight = float(raw_weight)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "cpd_like_objective.primitive_type_weights values must be numbers"
            ) from exc
        if not math.isfinite(weight) or weight < 0.0:
            raise ValueError(
                "cpd_like_objective.primitive_type_weights values must be finite non-negative numbers"
            )
        result[primitive_name] = weight
    return result


def _failure_labels(
    *,
    decomposition: CPDLikeDecompositionReport,
    over_budget_count: int,
    uncontained_primitive_count: int,
) -> tuple[str, ...]:
    labels: list[str] = []
    if decomposition.status != "smoke_passed":
        labels.append("source_decomposition_partial")
    if over_budget_count > 0:
        labels.append("primitive_budget_not_met")
    if decomposition.final_component_count > decomposition.target_primitive_count:
        labels.append("unmerged_components")
    if decomposition.blocked_merge_count > 0:
        labels.append("component_merge_blocked")
    if uncontained_primitive_count > 0:
        labels.append("uncontained_primitives")
    return tuple(labels)
