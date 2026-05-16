from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Mapping

import numpy as np

from primitive_collision_compiler.assets.usd_smoke import load_asset_manifest, resolve_asset_path
from primitive_collision_compiler.baselines.cpd_like.decompose import (
    CPDLikeDecompositionReport,
    decompose_mesh,
)
from primitive_collision_compiler.baselines.cpd_like.objective import (
    CPDLikeObjectiveOptions,
    build_cpd_like_objective_report,
)
from primitive_collision_compiler.baselines.cpd_like.package import package_from_cpd_like_report
from primitive_collision_compiler.baselines.cpd_like.primitives import (
    SUPPORT_AWARE_EXTENSION_MIN_SOURCE_FACES,
    SUPPORT_AWARE_EXTENSION_MIN_UNIQUE_POINTS,
    fit_primitive_candidates,
    rank_primitive_candidates_for_selection,
)
from primitive_collision_compiler.baselines.cpd_like.synthetic import (
    NEWTON_NATIVE_EXTENDED_SUBSET,
    NEWTON_NATIVE_LEGACY_SUBSET,
)
from primitive_collision_compiler.baselines.cpd_like.usd import load_first_mesh
from primitive_collision_compiler.contracts import CollisionPackage
from primitive_collision_compiler.geometry.mesh import TriangleMesh
from primitive_collision_compiler.newton.diagnostics import run_newton_contact_smoke
from primitive_collision_compiler.newton.drop_settle import (
    DropSettleOptions,
    run_newton_drop_settle,
)
from primitive_collision_compiler.newton.shapes import map_package_shapes
from primitive_collision_compiler.newton.sphere_rain import (
    SphereRainOptions,
    run_newton_sphere_rain,
)
from primitive_collision_compiler.reports.schema import NewtonDiagnosticReport

REAL_USD_NATIVE_FITTING_STAGE = "cpd_like_real_usd_native_fitting_comparison"
REAL_USD_NATIVE_FITTING_CLAIM_BOUNDARY = (
    "real_usd_native_fitting_comparison_not_collision_quality_validation"
)
REAL_USD_NATIVE_FITTING_EVIDENCE_LEVEL = "offline_real_usd_native_fitting_smoke"
REAL_USD_NATIVE_CONTACT_STAGE = "newton_real_usd_native_contact_comparison"
REAL_USD_NATIVE_CONTACT_CLAIM_BOUNDARY = (
    "real_usd_native_contact_canary_not_collision_quality_validation"
)
REAL_USD_NATIVE_CONTACT_EVIDENCE_LEVEL = "real_usd_native_contact_canary_smoke"
REAL_USD_NATIVE_TASK_STAGE = "newton_real_usd_native_task_comparison"
REAL_USD_NATIVE_TASK_CLAIM_BOUNDARY = (
    "real_usd_native_task_smoke_not_collision_quality_or_safety"
)
REAL_USD_NATIVE_TASK_EVIDENCE_LEVEL = "real_usd_native_drop_settle_sphere_rain_smoke"
REAL_USD_CANDIDATE_LOSS_STAGE = "cpd_like_real_usd_candidate_loss_diagnosis"
REAL_USD_CANDIDATE_LOSS_CLAIM_BOUNDARY = (
    "candidate_loss_diagnosis_not_collision_quality_validation"
)
REAL_USD_CANDIDATE_LOSS_EVIDENCE_LEVEL = "offline_candidate_loss_diagnosis_smoke"
LEGACY_LABEL = "legacy_box_sphere_capsule"
NATIVE_LABEL = "native_newton_bundle"
CANDIDATE_LOSS_TIE_TOLERANCE = 1e-12
CANDIDATE_LOSS_NEAR_MISS_RELATIVE_GAP_THRESHOLD = 0.25
CANDIDATE_LOSS_LOW_SUPPORT_FACE_THRESHOLD = SUPPORT_AWARE_EXTENSION_MIN_SOURCE_FACES - 1
CANDIDATE_LOSS_LOW_SUPPORT_POINT_THRESHOLD = SUPPORT_AWARE_EXTENSION_MIN_UNIQUE_POINTS - 1
CANDIDATE_LOSS_TRIAGE_CLAIM_BOUNDARY = "diagnostic_triage_not_collision_quality"


@dataclass(frozen=True)
class NativeLaneArtifact:
    label: str
    lane: str
    asset_role: str
    asset_path: str
    max_source_faces: int
    mesh: TriangleMesh
    decomposition: CPDLikeDecompositionReport
    objective: dict[str, object]
    package: CollisionPackage

    def to_summary(self) -> dict[str, object]:
        metrics = self.objective["metrics"]
        return {
            "label": self.label,
            "lane": self.lane,
            "status": self.objective["status"],
            "decomposition_status": self.decomposition.status,
            "asset_role": self.asset_role,
            "asset_path": self.asset_path,
            "max_source_faces": self.max_source_faces,
            "primitive_subset": list(self.decomposition.primitive_subset),
            "primitive_count": self.decomposition.primitive_count,
            "primitive_kind_counts": dict(
                Counter(primitive.primitive_type for primitive in self.decomposition.primitives)
            ),
            "failure_labels": self.objective["failure_labels"],
            "geometric_excess_proxy": metrics["geometric_excess_proxy"],
            "merge_excess_terms": metrics["merge_excess_terms"],
            "component_accounting": metrics["component_accounting"],
            "containment": metrics["containment"],
            "paper_primitive_gap": metrics["paper_primitive_gap"],
            "candidate_audit_summary": _candidate_audit_summary(
                self.mesh,
                self.decomposition,
                normalizer_volume=float(
                    metrics["geometric_excess_proxy"]["normalizer_volume"]
                ),
            ),
            "package_mapping": package_mapping_summary(self.package),
            "collision_package": self.package.to_dict(),
        }


@dataclass(frozen=True)
class RealUsdComparisonArtifact:
    asset_role: str
    asset_path: str
    legacy: NativeLaneArtifact
    native: NativeLaneArtifact

    def to_summary(self) -> dict[str, object]:
        return {
            "asset_role": self.asset_role,
            "asset_path": self.asset_path,
            "legacy": self.legacy.to_summary(),
            "native": self.native.to_summary(),
            "comparison": _comparison_summary(self.legacy, self.native),
        }


def build_real_usd_native_artifacts(
    *,
    manifest_path: str,
    roles: tuple[str, ...],
    max_primitives: int,
    legacy_subset: tuple[str, ...] = NEWTON_NATIVE_LEGACY_SUBSET,
    native_subset: tuple[str, ...] = NEWTON_NATIVE_EXTENDED_SUBSET,
    max_source_faces_by_role: Mapping[str, int] | None = None,
    component_merge_options: Mapping[str, object] | None = None,
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> tuple[RealUsdComparisonArtifact, ...]:
    _validate_roles(roles)
    assets = _resolve_manifest_roles(manifest_path, roles)
    face_caps = dict(max_source_faces_by_role or {})
    return tuple(
        _artifact_for_asset(
            asset_role=str(asset["role"]),
            asset_path=str(asset["path"]),
            max_source_faces=int(face_caps.get(str(asset["role"]), 256)),
            max_primitives=max_primitives,
            legacy_subset=legacy_subset,
            native_subset=native_subset,
            component_merge_options=component_merge_options,
            objective_options=objective_options,
        )
        for asset in assets
    )


def build_real_usd_native_fitting_comparison_report(
    *,
    manifest_path: str,
    roles: tuple[str, ...],
    max_primitives: int,
    legacy_subset: tuple[str, ...] = NEWTON_NATIVE_LEGACY_SUBSET,
    native_subset: tuple[str, ...] = NEWTON_NATIVE_EXTENDED_SUBSET,
    max_source_faces_by_role: Mapping[str, int] | None = None,
    component_merge_options: Mapping[str, object] | None = None,
    objective_options: CPDLikeObjectiveOptions | None = None,
    claim_boundary: str = REAL_USD_NATIVE_FITTING_CLAIM_BOUNDARY,
    evidence_level: str = REAL_USD_NATIVE_FITTING_EVIDENCE_LEVEL,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=claim_boundary,
        evidence_level=evidence_level,
    )
    artifacts = build_real_usd_native_artifacts(
        manifest_path=manifest_path,
        roles=roles,
        max_primitives=max_primitives,
        legacy_subset=legacy_subset,
        native_subset=native_subset,
        max_source_faces_by_role=max_source_faces_by_role,
        component_merge_options=component_merge_options,
        objective_options=options,
    )
    cases = [artifact.to_summary() for artifact in artifacts]
    statuses = [
        str(lane["status"])
        for case in cases
        for lane in (case["legacy"], case["native"])
    ]
    return {
        "stage": REAL_USD_NATIVE_FITTING_STAGE,
        "status": "smoke_passed" if all(status == "smoke_passed" for status in statuses) else "partial",
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "manifest": manifest_path,
        "roles": list(roles),
        "legacy_primitive_subset": list(legacy_subset),
        "native_primitive_subset": list(native_subset),
        "cases": cases,
    }


def build_real_usd_candidate_loss_diagnosis_report(
    *,
    manifest_path: str,
    roles: tuple[str, ...],
    max_primitives: int,
    legacy_subset: tuple[str, ...] = NEWTON_NATIVE_LEGACY_SUBSET,
    native_subset: tuple[str, ...] = NEWTON_NATIVE_EXTENDED_SUBSET,
    max_source_faces_by_role: Mapping[str, int] | None = None,
    component_merge_options: Mapping[str, object] | None = None,
    objective_options: CPDLikeObjectiveOptions | None = None,
    claim_boundary: str = REAL_USD_CANDIDATE_LOSS_CLAIM_BOUNDARY,
    evidence_level: str = REAL_USD_CANDIDATE_LOSS_EVIDENCE_LEVEL,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=claim_boundary,
        evidence_level=evidence_level,
    )
    artifacts = build_real_usd_native_artifacts(
        manifest_path=manifest_path,
        roles=roles,
        max_primitives=max_primitives,
        legacy_subset=legacy_subset,
        native_subset=native_subset,
        max_source_faces_by_role=max_source_faces_by_role,
        component_merge_options=component_merge_options,
        objective_options=options,
    )
    cases = []
    statuses = []
    for artifact in artifacts:
        legacy_summary = artifact.legacy.to_summary()
        native_summary = artifact.native.to_summary()
        statuses.extend([str(legacy_summary["status"]), str(native_summary["status"])])
        normalizer_volume = float(
            artifact.native.objective["metrics"]["geometric_excess_proxy"][
                "normalizer_volume"
            ]
        )
        cases.append(
            {
                "asset_role": artifact.asset_role,
                "asset_path": artifact.asset_path,
                "max_source_faces": artifact.native.max_source_faces,
                "baseline_lock": _baseline_lock_summary(artifact.legacy, artifact.native),
                "legacy": legacy_summary,
                "native": native_summary,
                "native_candidate_loss_diagnosis": _candidate_loss_diagnosis(
                    artifact.native.mesh,
                    artifact.native.decomposition,
                    normalizer_volume=normalizer_volume,
                ),
            }
        )
    return {
        "stage": REAL_USD_CANDIDATE_LOSS_STAGE,
        "status": "smoke_passed" if all(status == "smoke_passed" for status in statuses) else "partial",
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "manifest": manifest_path,
        "roles": list(roles),
        "legacy_primitive_subset": list(legacy_subset),
        "native_primitive_subset": list(native_subset),
        "diagnosis_semantics": "surrogate_candidate_accounting_not_collision_quality",
        "cases": cases,
    }


def build_real_usd_native_contact_comparison_report(
    *,
    manifest_path: str,
    roles: tuple[str, ...],
    max_primitives: int,
    source_dir: str,
    device: str = "cpu",
    legacy_subset: tuple[str, ...] = NEWTON_NATIVE_LEGACY_SUBSET,
    native_subset: tuple[str, ...] = NEWTON_NATIVE_EXTENDED_SUBSET,
    max_source_faces_by_role: Mapping[str, int] | None = None,
    component_merge_options: Mapping[str, object] | None = None,
    objective_options: CPDLikeObjectiveOptions | None = None,
    claim_boundary: str = REAL_USD_NATIVE_CONTACT_CLAIM_BOUNDARY,
    evidence_level: str = REAL_USD_NATIVE_CONTACT_EVIDENCE_LEVEL,
) -> dict[str, object]:
    artifacts = build_real_usd_native_artifacts(
        manifest_path=manifest_path,
        roles=roles,
        max_primitives=max_primitives,
        legacy_subset=legacy_subset,
        native_subset=native_subset,
        max_source_faces_by_role=max_source_faces_by_role,
        component_merge_options=component_merge_options,
        objective_options=objective_options
        or CPDLikeObjectiveOptions(
            claim_boundary=REAL_USD_NATIVE_FITTING_CLAIM_BOUNDARY,
            evidence_level=REAL_USD_NATIVE_FITTING_EVIDENCE_LEVEL,
        ),
    )
    cases: list[dict[str, object]] = []
    child_statuses: list[str] = []
    for artifact in artifacts:
        legacy_contact = _contact_or_mapping_gap(
            artifact.legacy,
            source_dir=source_dir,
            device=device,
            claim_boundary=claim_boundary,
        )
        native_contact = _contact_or_mapping_gap(
            artifact.native,
            source_dir=source_dir,
            device=device,
            claim_boundary=claim_boundary,
        )
        child_statuses.extend([str(legacy_contact["status"]), str(native_contact["status"])])
        cases.append(
            {
                "asset_role": artifact.asset_role,
                "asset_path": artifact.asset_path,
                "comparison": _comparison_summary(artifact.legacy, artifact.native),
                "legacy": artifact.legacy.to_summary(),
                "native": artifact.native.to_summary(),
                "legacy_contact": legacy_contact,
                "native_contact": native_contact,
            }
        )

    return {
        "stage": REAL_USD_NATIVE_CONTACT_STAGE,
        "status": _aggregate_probe_status(child_statuses),
        "claim_boundary": claim_boundary,
        "evidence_level": evidence_level,
        "manifest": manifest_path,
        "roles": list(roles),
        "source_dir": source_dir,
        "device": device,
        "cases": cases,
    }


def build_real_usd_native_task_comparison_report(
    *,
    manifest_path: str,
    roles: tuple[str, ...],
    max_primitives: int,
    source_dir: str,
    device: str = "cpu",
    legacy_subset: tuple[str, ...] = NEWTON_NATIVE_LEGACY_SUBSET,
    native_subset: tuple[str, ...] = NEWTON_NATIVE_EXTENDED_SUBSET,
    max_source_faces_by_role: Mapping[str, int] | None = None,
    component_merge_options: Mapping[str, object] | None = None,
    objective_options: CPDLikeObjectiveOptions | None = None,
    drop_settle_options: DropSettleOptions | None = None,
    sphere_rain_options: SphereRainOptions | None = None,
    claim_boundary: str = REAL_USD_NATIVE_TASK_CLAIM_BOUNDARY,
    contact_claim_boundary: str = REAL_USD_NATIVE_CONTACT_CLAIM_BOUNDARY,
    evidence_level: str = REAL_USD_NATIVE_TASK_EVIDENCE_LEVEL,
) -> dict[str, object]:
    artifacts = build_real_usd_native_artifacts(
        manifest_path=manifest_path,
        roles=roles,
        max_primitives=max_primitives,
        legacy_subset=legacy_subset,
        native_subset=native_subset,
        max_source_faces_by_role=max_source_faces_by_role,
        component_merge_options=component_merge_options,
        objective_options=objective_options
        or CPDLikeObjectiveOptions(
            claim_boundary=REAL_USD_NATIVE_FITTING_CLAIM_BOUNDARY,
            evidence_level=REAL_USD_NATIVE_FITTING_EVIDENCE_LEVEL,
        ),
    )
    drop_settle_options = drop_settle_options or DropSettleOptions()
    sphere_rain_options = sphere_rain_options or SphereRainOptions()
    cases: list[dict[str, object]] = []
    child_statuses: list[str] = []
    for artifact in artifacts:
        legacy_contact, legacy_tasks = _task_probe_payloads(
            artifact.legacy,
            source_dir=source_dir,
            device=device,
            contact_claim_boundary=contact_claim_boundary,
            task_claim_boundary=claim_boundary,
            drop_settle_options=drop_settle_options,
            sphere_rain_options=sphere_rain_options,
        )
        native_contact, native_tasks = _task_probe_payloads(
            artifact.native,
            source_dir=source_dir,
            device=device,
            contact_claim_boundary=contact_claim_boundary,
            task_claim_boundary=claim_boundary,
            drop_settle_options=drop_settle_options,
            sphere_rain_options=sphere_rain_options,
        )
        child_statuses.extend(
            [
                str(legacy_contact["status"]),
                str(native_contact["status"]),
                str(legacy_tasks["drop_settle"]["status"]),
                str(legacy_tasks["sphere_rain"]["status"]),
                str(native_tasks["drop_settle"]["status"]),
                str(native_tasks["sphere_rain"]["status"]),
            ]
        )
        cases.append(
            {
                "asset_role": artifact.asset_role,
                "asset_path": artifact.asset_path,
                "comparison": _comparison_summary(artifact.legacy, artifact.native),
                "legacy": artifact.legacy.to_summary(),
                "native": artifact.native.to_summary(),
                "legacy_contact": legacy_contact,
                "native_contact": native_contact,
                "legacy_tasks": legacy_tasks,
                "native_tasks": native_tasks,
            }
        )

    return {
        "stage": REAL_USD_NATIVE_TASK_STAGE,
        "status": _aggregate_probe_status(child_statuses),
        "claim_boundary": claim_boundary,
        "contact_claim_boundary": contact_claim_boundary,
        "evidence_level": evidence_level,
        "manifest": manifest_path,
        "roles": list(roles),
        "source_dir": source_dir,
        "device": device,
        "cases": cases,
    }


def package_mapping_summary(package: CollisionPackage) -> dict[str, object]:
    mappings = map_package_shapes(package)
    status_counts = dict(Counter(mapping.status for mapping in mappings))
    return {
        "package_id": package.package_id,
        "primitive_kinds": [primitive.kind for primitive in package.primitives],
        "status_counts": status_counts,
        "mapping_details": [mapping.to_dict() for mapping in mappings],
        "fully_mapped": bool(
            package.primitives
            and status_counts.get("mapped", 0) == len(package.primitives)
        ),
    }


def _validate_roles(roles: tuple[str, ...]) -> None:
    if not roles:
        raise ValueError("roles must contain at least one asset role")
    if any(not str(role) for role in roles):
        raise ValueError("roles must contain non-empty asset roles")


def _resolve_manifest_roles(manifest_path: str, roles: tuple[str, ...]) -> tuple[dict[str, object], ...]:
    assets = load_asset_manifest(manifest_path)
    by_role = {str(asset.get("role")): asset for asset in assets}
    result: list[dict[str, object]] = []
    for role in roles:
        if role not in by_role:
            raise ValueError(f"asset role {role!r} not found in manifest: {manifest_path}")
        asset = dict(by_role[role])
        asset["path"] = resolve_asset_path(asset).path
        result.append(asset)
    return tuple(result)


def _artifact_for_asset(
    *,
    asset_role: str,
    asset_path: str,
    max_source_faces: int,
    max_primitives: int,
    legacy_subset: tuple[str, ...],
    native_subset: tuple[str, ...],
    component_merge_options: Mapping[str, object] | None,
    objective_options: CPDLikeObjectiveOptions | None,
) -> RealUsdComparisonArtifact:
    legacy = _lane_artifact(
        label=LEGACY_LABEL,
        lane="legacy",
        asset_role=asset_role,
        asset_path=asset_path,
        max_source_faces=max_source_faces,
        max_primitives=max_primitives,
        primitive_subset=legacy_subset,
        component_merge_options=component_merge_options,
        objective_options=objective_options,
    )
    native = _lane_artifact(
        label=NATIVE_LABEL,
        lane="native",
        asset_role=asset_role,
        asset_path=asset_path,
        max_source_faces=max_source_faces,
        max_primitives=max_primitives,
        primitive_subset=native_subset,
        component_merge_options=component_merge_options,
        objective_options=objective_options,
    )
    return RealUsdComparisonArtifact(
        asset_role=asset_role,
        asset_path=asset_path,
        legacy=legacy,
        native=native,
    )


def _lane_artifact(
    *,
    label: str,
    lane: str,
    asset_role: str,
    asset_path: str,
    max_source_faces: int,
    max_primitives: int,
    primitive_subset: tuple[str, ...],
    component_merge_options: Mapping[str, object] | None,
    objective_options: CPDLikeObjectiveOptions | None,
) -> NativeLaneArtifact:
    mesh = load_first_mesh(asset_path, max_faces=max_source_faces)
    decomposition = decompose_mesh(
        mesh,
        max_primitives=max_primitives,
        primitive_subset=primitive_subset,
        **_component_merge_kwargs(component_merge_options),
    )
    package_asset_id = f"{asset_role}_{lane}"
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=REAL_USD_NATIVE_FITTING_CLAIM_BOUNDARY,
        evidence_level=REAL_USD_NATIVE_FITTING_EVIDENCE_LEVEL,
    )
    objective = build_cpd_like_objective_report(
        decomposition,
        asset_id=package_asset_id,
        source_path=asset_path,
        max_source_faces=max_source_faces,
        options=options,
    ).to_dict()
    package = package_from_cpd_like_report(
        decomposition,
        asset_id=package_asset_id,
        source_path=asset_path,
        claim_boundary=options.claim_boundary,
        max_source_faces=max_source_faces,
    )
    return NativeLaneArtifact(
        label=label,
        lane=lane,
        asset_role=asset_role,
        asset_path=asset_path,
        max_source_faces=max_source_faces,
        mesh=mesh,
        decomposition=decomposition,
        objective=objective,
        package=package,
    )


def _component_merge_kwargs(options: Mapping[str, object] | None) -> dict[str, object]:
    raw = dict(options or {})
    allowed = (
        "component_merge",
        "merge_search_policy",
        "excess_volume_threshold_fraction",
        "report_merge_trace",
    )
    return {key: raw[key] for key in allowed if key in raw}


def _comparison_summary(
    legacy: NativeLaneArtifact,
    native: NativeLaneArtifact,
) -> dict[str, object]:
    legacy_metrics = legacy.objective["metrics"]
    native_metrics = native.objective["metrics"]
    legacy_volume = float(
        legacy_metrics["geometric_excess_proxy"]["normalized_weighted_primitive_volume"]
    )
    native_volume = float(
        native_metrics["geometric_excess_proxy"]["normalized_weighted_primitive_volume"]
    )
    legacy_mapping = package_mapping_summary(legacy.package)
    native_mapping = package_mapping_summary(native.package)
    legacy_kinds = {primitive.primitive_type for primitive in legacy.decomposition.primitives}
    native_kinds = {primitive.primitive_type for primitive in native.decomposition.primitives}
    legacy_subset = set(legacy.decomposition.primitive_subset)
    return {
        "legacy_primitive_count": legacy.decomposition.primitive_count,
        "native_primitive_count": native.decomposition.primitive_count,
        "primitive_count_delta_native_minus_legacy": (
            native.decomposition.primitive_count - legacy.decomposition.primitive_count
        ),
        "legacy_primitive_kinds": sorted(legacy_kinds),
        "native_primitive_kinds": sorted(native_kinds),
        "legacy_normalized_weighted_volume": legacy_volume,
        "native_normalized_weighted_volume": native_volume,
        "native_normalized_volume_delta": float(native_volume - legacy_volume),
        "legacy_fully_mapped": legacy_mapping["fully_mapped"],
        "native_fully_mapped": native_mapping["fully_mapped"],
        "native_uses_extended_primitive": bool(native_kinds - legacy_subset),
        "legacy_failure_labels": legacy.objective["failure_labels"],
        "native_failure_labels": native.objective["failure_labels"],
    }


def _candidate_audit_summary(
    mesh: TriangleMesh,
    decomposition: CPDLikeDecompositionReport,
    *,
    normalizer_volume: float,
) -> dict[str, object]:
    extension_kinds = tuple(
        primitive
        for primitive in NEWTON_NATIVE_EXTENDED_SUBSET
        if primitive not in NEWTON_NATIVE_LEGACY_SUBSET
        and primitive in decomposition.primitive_subset
    )
    selected_rank_counts: Counter[str] = Counter()
    selected_kind_counts: Counter[str] = Counter()
    extension_best_kind_counts: Counter[str] = Counter()
    selected_vs_best_nonselected_margins: list[float] = []
    selected_vs_extension_margins: list[float] = []
    clusters_with_extension_best = 0
    clusters_where_extension_beats_selected = 0
    clusters_with_support_blocked_raw_cost_extension_best = 0
    support_blocked_extension_count = 0
    support_blocked_extension_kind_counts: Counter[str] = Counter()
    support_blocked_extension_targets: list[dict[str, object]] = []
    box_selected_cluster_count = 0
    box_selected_with_extension_second_count = 0
    normalizer = max(float(normalizer_volume), 1e-12)

    for cluster_index, primitive in enumerate(decomposition.primitives):
        face_ids = frozenset(primitive.source_faces)
        candidates = fit_primitive_candidates(
            mesh,
            face_ids,
            decomposition.primitive_subset,
        )
        ranked = [
            {
                "primitive_type": ranked_candidate.candidate.primitive_type,
                "candidate_order": ranked_candidate.candidate_order,
                "raw_cost_rank": ranked_candidate.raw_cost_rank,
                "normalized_weighted_volume": float(
                    ranked_candidate.candidate.weighted_volume / normalizer
                ),
                "selection_admissible": ranked_candidate.selection_admissible,
                "selection_admissibility_reason": (
                    ranked_candidate.selection_admissibility_reason
                ),
                "selection_support": ranked_candidate.support,
            }
            for ranked_candidate in rank_primitive_candidates_for_selection(
                mesh,
                face_ids,
                candidates,
            )
        ]
        ranked = [{**row, "rank": rank} for rank, row in enumerate(ranked, start=1)]
        raw_cost_ranked = sorted(
            ranked,
            key=lambda row: (int(row["raw_cost_rank"]), int(row["candidate_order"])),
        )
        selected_rank = _rank_for_primitive(ranked, primitive.primitive_type)
        selected_rank_counts[str(selected_rank)] += 1
        selected_kind_counts[primitive.primitive_type] += 1
        if primitive.primitive_type == "box":
            box_selected_cluster_count += 1

        selected_cost = float(ranked[selected_rank - 1]["normalized_weighted_volume"])
        best_nonselected = _best_nonselected_candidate(ranked, primitive.primitive_type)
        if best_nonselected is not None:
            best_nonselected_cost = float(best_nonselected["normalized_weighted_volume"])
            selected_vs_best_nonselected_margins.append(
                float(selected_cost - best_nonselected_cost)
            )
            if (
                primitive.primitive_type == "box"
                and len(raw_cost_ranked) > 1
                and raw_cost_ranked[1]["primitive_type"] in extension_kinds
            ):
                box_selected_with_extension_second_count += 1

        extension_rows = [
            row for row in raw_cost_ranked if row["primitive_type"] in extension_kinds
        ]
        if extension_rows:
            best_extension = extension_rows[0]
            best_extension_cost = float(best_extension["normalized_weighted_volume"])
            selected_vs_extension_margins.append(float(selected_cost - best_extension_cost))
            if raw_cost_ranked[0]["primitive_type"] in extension_kinds:
                clusters_with_extension_best += 1
                extension_best_kind_counts[str(raw_cost_ranked[0]["primitive_type"])] += 1
                if not bool(raw_cost_ranked[0]["selection_admissible"]):
                    clusters_with_support_blocked_raw_cost_extension_best += 1
            if best_extension_cost < selected_cost:
                clusters_where_extension_beats_selected += 1
            for extension_row in extension_rows:
                if bool(extension_row["selection_admissible"]):
                    continue
                support_blocked_extension_count += 1
                support_blocked_extension_kind_counts[str(extension_row["primitive_type"])] += 1
                if len(support_blocked_extension_targets) < 10:
                    support_blocked_extension_targets.append(
                        {
                            "cluster_index": cluster_index,
                            "source_faces": list(primitive.source_faces),
                            "selected_primitive_type": primitive.primitive_type,
                            "blocked_extension_primitive_type": extension_row["primitive_type"],
                            "raw_cost_rank": int(extension_row["raw_cost_rank"]),
                            "selection_rank": int(extension_row["rank"]),
                            "normalized_weighted_volume": float(
                                extension_row["normalized_weighted_volume"]
                            ),
                            "selected_normalized_weighted_volume": selected_cost,
                            "selection_admissibility_reason": extension_row[
                                "selection_admissibility_reason"
                            ],
                            "selection_support": extension_row["selection_support"],
                        }
                    )

    return {
        "scope": "per_selected_cluster",
        "cost_name": "normalized_weighted_primitive_volume",
        "ranking_semantics": {
            "rank": "support_aware_selection_rank",
            "raw_cost_rank": "cost_only_weighted_volume_rank",
        },
        "cluster_count": decomposition.primitive_count,
        "primitive_subset": list(decomposition.primitive_subset),
        "extension_candidate_kinds": list(extension_kinds),
        "selected_kind_counts": dict(selected_kind_counts),
        "selected_rank_counts": dict(selected_rank_counts),
        "clusters_with_extension_best": clusters_with_extension_best,
        "extension_best_kind_counts": dict(extension_best_kind_counts),
        "clusters_where_extension_beats_selected": clusters_where_extension_beats_selected,
        "clusters_with_support_blocked_raw_cost_extension_best": (
            clusters_with_support_blocked_raw_cost_extension_best
        ),
        "support_blocked_extension_count": support_blocked_extension_count,
        "support_blocked_extension_kind_counts": dict(
            sorted(support_blocked_extension_kind_counts.items())
        ),
        "support_blocked_extension_targets": support_blocked_extension_targets,
        "box_selected_cluster_count": box_selected_cluster_count,
        "box_selected_with_extension_second_count": box_selected_with_extension_second_count,
        "margin_sign_convention": "selected_cost_minus_comparator_cost",
        "mean_selected_minus_best_nonselected_cost": _mean_or_none(
            selected_vs_best_nonselected_margins
        ),
        "mean_selected_minus_best_extension_cost": _mean_or_none(
            selected_vs_extension_margins
        ),
    }


def _baseline_lock_summary(
    legacy: NativeLaneArtifact,
    native: NativeLaneArtifact,
) -> dict[str, object]:
    legacy_counts = Counter(primitive.primitive_type for primitive in legacy.decomposition.primitives)
    native_counts = Counter(primitive.primitive_type for primitive in native.decomposition.primitives)
    legacy_subset = set(legacy.decomposition.primitive_subset)
    native_kinds = set(native_counts)
    return {
        "scope": "current_real_usd_old_new_reference",
        "legacy_status": legacy.objective["status"],
        "native_status": native.objective["status"],
        "legacy_primitive_kind_counts": dict(legacy_counts),
        "native_primitive_kind_counts": dict(native_counts),
        "legacy_primitive_count": legacy.decomposition.primitive_count,
        "native_primitive_count": native.decomposition.primitive_count,
        "native_uses_extended_primitive": bool(native_kinds - legacy_subset),
        "comparison": _comparison_summary(legacy, native),
    }


def _candidate_loss_diagnosis(
    mesh: TriangleMesh,
    decomposition: CPDLikeDecompositionReport,
    *,
    normalizer_volume: float,
) -> dict[str, object]:
    extension_kinds = tuple(
        primitive
        for primitive in NEWTON_NATIVE_EXTENDED_SUBSET
        if primitive not in NEWTON_NATIVE_LEGACY_SUBSET
        and primitive in decomposition.primitive_subset
    )
    normalizer = max(float(normalizer_volume), 1e-12)
    clusters: list[dict[str, object]] = []
    bottleneck_counts: Counter[str] = Counter()
    label_counts: Counter[str] = Counter()

    for cluster_index, primitive in enumerate(decomposition.primitives):
        candidates = fit_primitive_candidates(
            mesh,
            frozenset(primitive.source_faces),
            decomposition.primitive_subset,
        )
        ranked = _ranked_candidate_rows(
            mesh,
            frozenset(primitive.source_faces),
            candidates,
            selected_primitive_type=primitive.primitive_type,
            extension_kinds=extension_kinds,
            normalizer=normalizer,
        )
        selected_rank = _rank_for_primitive(ranked, primitive.primitive_type)
        selected_row = ranked[selected_rank - 1]
        extension_rows = [row for row in ranked if row["is_extension_candidate"]]
        best_extension = extension_rows[0] if extension_rows else None
        labels, likely_bottleneck = _candidate_loss_labels(
            selected_row,
            best_extension,
            extension_rows,
        )
        for label in labels:
            label_counts[label] += 1
        bottleneck_counts[likely_bottleneck] += 1
        clusters.append(
            {
                "cluster_index": cluster_index,
                "source_faces": list(primitive.source_faces),
                "selected_primitive_type": primitive.primitive_type,
                "selected_rank": selected_rank,
                "candidate_ranking": ranked,
                "best_extension_candidate": best_extension,
                "selected_minus_best_extension_cost": (
                    None
                    if best_extension is None
                    else float(
                        selected_row["normalized_weighted_volume"]
                        - best_extension["normalized_weighted_volume"]
                    )
                ),
                "margin_sign_convention": "selected_cost_minus_best_extension_cost",
                "cluster_geometry": _cluster_geometry_summary(mesh, primitive.source_faces),
                "diagnosis_labels": labels,
                "likely_bottleneck": likely_bottleneck,
            }
        )

    return {
        "scope": "per_selected_cluster_candidate_loss",
        "cost_name": "normalized_weighted_primitive_volume",
        "cluster_count": decomposition.primitive_count,
        "primitive_subset": list(decomposition.primitive_subset),
        "extension_candidate_kinds": list(extension_kinds),
        "clusters": clusters,
        "triage": _candidate_loss_triage(clusters),
        "diagnosis_summary": {
            "likely_bottleneck_counts": dict(bottleneck_counts),
            "diagnosis_label_counts": dict(label_counts),
        },
    }


def _candidate_loss_triage(clusters: list[dict[str, object]]) -> dict[str, object]:
    near_miss_targets: list[dict[str, object]] = []
    low_support_targets: list[dict[str, object]] = []
    for cluster in clusters:
        selected_row = _selected_candidate_row(cluster["candidate_ranking"])
        best_extension = cluster["best_extension_candidate"]
        geometry = cluster["cluster_geometry"]
        if best_extension is not None:
            near_miss = _near_miss_target(cluster, selected_row, best_extension)
            if near_miss is not None:
                near_miss_targets.append(near_miss)
        if bool(selected_row["is_extension_candidate"]):
            face_count = int(geometry["face_count"])
            point_count = int(geometry["point_count"])
            if (
                face_count <= CANDIDATE_LOSS_LOW_SUPPORT_FACE_THRESHOLD
                or point_count <= CANDIDATE_LOSS_LOW_SUPPORT_POINT_THRESHOLD
            ):
                low_support_targets.append(
                    {
                        "cluster_index": int(cluster["cluster_index"]),
                        "source_faces": list(cluster["source_faces"]),
                        "selected_extension_primitive_type": selected_row["primitive_type"],
                        "selected_rank": int(selected_row["rank"]),
                        "source_face_count": face_count,
                        "point_count": point_count,
                        "cluster_geometry": geometry,
                        "suggested_next_slice": "native_extension_admissibility_fixture",
                    }
                )

    near_miss_targets.sort(
        key=lambda target: (
            float(target["relative_extension_gap"]),
            int(target["cluster_index"]),
        )
    )
    low_support_targets.sort(
        key=lambda target: (
            int(target["source_face_count"]),
            int(target["point_count"]),
            int(target["cluster_index"]),
        )
    )
    near_miss_kind_counts = Counter(
        target["best_extension_primitive_type"] for target in near_miss_targets
    )
    low_support_kind_counts = Counter(
        target["selected_extension_primitive_type"] for target in low_support_targets
    )
    return {
        "scope": "candidate_loss_next_slice_triage",
        "claim_boundary": CANDIDATE_LOSS_TRIAGE_CLAIM_BOUNDARY,
        "near_miss_relative_gap_threshold": CANDIDATE_LOSS_NEAR_MISS_RELATIVE_GAP_THRESHOLD,
        "low_support_face_threshold": CANDIDATE_LOSS_LOW_SUPPORT_FACE_THRESHOLD,
        "low_support_point_threshold": CANDIDATE_LOSS_LOW_SUPPORT_POINT_THRESHOLD,
        "near_miss_cluster_count": len(near_miss_targets),
        "near_miss_kind_counts": dict(sorted(near_miss_kind_counts.items())),
        "top_near_miss_targets": near_miss_targets[:10],
        "low_support_native_extension_count": len(low_support_targets),
        "low_support_native_extension_kind_counts": dict(
            sorted(low_support_kind_counts.items())
        ),
        "low_support_native_extension_targets": low_support_targets[:10],
        "recommended_next_slice": _recommended_next_slice(
            near_miss_targets,
            low_support_targets,
        ),
    }


def _selected_candidate_row(ranked: list[dict[str, object]]) -> dict[str, object]:
    for row in ranked:
        if row["selected"]:
            return row
    raise ValueError("candidate ranking must contain a selected row")


def _near_miss_target(
    cluster: dict[str, object],
    selected_row: dict[str, object],
    best_extension: dict[str, object],
) -> dict[str, object] | None:
    if bool(selected_row["is_extension_candidate"]):
        return None
    selected_cost = float(selected_row["normalized_weighted_volume"])
    extension_cost = float(best_extension["normalized_weighted_volume"])
    if (
        selected_cost <= 0.0
        or abs(extension_cost - selected_cost) <= CANDIDATE_LOSS_TIE_TOLERANCE
        or extension_cost < selected_cost
    ):
        return None
    relative_gap = float((extension_cost - selected_cost) / selected_cost)
    if relative_gap > CANDIDATE_LOSS_NEAR_MISS_RELATIVE_GAP_THRESHOLD:
        return None
    geometry = cluster["cluster_geometry"]
    return {
        "cluster_index": int(cluster["cluster_index"]),
        "source_faces": list(cluster["source_faces"]),
        "selected_primitive_type": selected_row["primitive_type"],
        "best_extension_primitive_type": best_extension["primitive_type"],
        "selected_normalized_weighted_volume": selected_cost,
        "best_extension_normalized_weighted_volume": extension_cost,
        "selected_minus_best_extension_cost": cluster["selected_minus_best_extension_cost"],
        "relative_extension_gap": relative_gap,
        "source_face_count": int(geometry["face_count"]),
        "point_count": int(geometry["point_count"]),
        "cluster_geometry": geometry,
        "suggested_next_slice": "primitive_fitting_near_miss_fixture",
    }


def _recommended_next_slice(
    near_miss_targets: list[dict[str, object]],
    low_support_targets: list[dict[str, object]],
) -> dict[str, object]:
    if low_support_targets:
        first = low_support_targets[0]
        return {
            "target_type": "native_extension_low_support_admissibility",
            "extension_kind": first["selected_extension_primitive_type"],
            "suggested_synthetic_fixture": "low_support_native_extension_patch",
            "claim_boundary": CANDIDATE_LOSS_TRIAGE_CLAIM_BOUNDARY,
        }
    if near_miss_targets:
        first = near_miss_targets[0]
        return {
            "target_type": "primitive_fitting_near_miss",
            "extension_kind": first["best_extension_primitive_type"],
            "suggested_synthetic_fixture": (
                f"{first['best_extension_primitive_type']}_near_miss_cluster"
            ),
            "claim_boundary": CANDIDATE_LOSS_TRIAGE_CLAIM_BOUNDARY,
        }
    return {
        "target_type": "no_ranked_target",
        "claim_boundary": CANDIDATE_LOSS_TRIAGE_CLAIM_BOUNDARY,
    }


def _ranked_candidate_rows(
    mesh: TriangleMesh,
    face_ids: frozenset[int],
    candidates,
    *,
    selected_primitive_type: str,
    extension_kinds: tuple[str, ...],
    normalizer: float,
) -> list[dict[str, object]]:
    ranked_candidates = rank_primitive_candidates_for_selection(mesh, face_ids, candidates)
    rows = [
        {
            "primitive_type": ranked_candidate.candidate.primitive_type,
            "candidate_order": ranked_candidate.candidate_order,
            "raw_cost_rank": ranked_candidate.raw_cost_rank,
            "weighted_volume": ranked_candidate.candidate.weighted_volume,
            "normalized_weighted_volume": float(
                ranked_candidate.candidate.weighted_volume / normalizer
            ),
            "contains_assigned_points": ranked_candidate.candidate.contains_assigned_points,
            "dimensions": ranked_candidate.candidate.dimensions,
            "selected": ranked_candidate.candidate.primitive_type == selected_primitive_type,
            "is_extension_candidate": (
                ranked_candidate.candidate.primitive_type in extension_kinds
            ),
            "selection_admissible": ranked_candidate.selection_admissible,
            "selection_admissibility_reason": (
                ranked_candidate.selection_admissibility_reason
            ),
            "selection_support": ranked_candidate.support,
        }
        for ranked_candidate in ranked_candidates
    ]
    return [{**row, "rank": rank} for rank, row in enumerate(rows, start=1)]


def _candidate_loss_labels(
    selected_row: dict[str, object],
    best_extension: dict[str, object] | None,
    extension_rows: list[dict[str, object]],
) -> tuple[list[str], str]:
    labels: list[str] = []
    if selected_row["primitive_type"] == "box":
        labels.append("selected_box")
    if not extension_rows:
        labels.append("no_extension_candidates")
        return labels, "no_extension_candidates"
    selected_cost = float(selected_row["normalized_weighted_volume"])
    best_extension_cost = float(best_extension["normalized_weighted_volume"])
    if bool(selected_row["is_extension_candidate"]):
        labels.append("native_extension_selected")
        return labels, "native_extension_selected"
    if (
        best_extension_cost < selected_cost
        and best_extension["selection_admissibility_reason"]
        == "insufficient_extension_support"
    ):
        labels.append("extension_candidate_cheaper_than_selected")
        labels.append("extension_candidate_blocked_by_support")
        return labels, "extension_support_admissibility"
    if abs(best_extension_cost - selected_cost) <= CANDIDATE_LOSS_TIE_TOLERANCE:
        labels.append("extension_tied_selected")
        return labels, "tie_or_subset_order"
    if best_extension_cost > selected_cost:
        labels.append("extension_fit_cost_higher_than_selected")
        return labels, "extension_fit_or_objective_cost"
    if best_extension_cost < selected_cost:
        labels.append("extension_candidate_cheaper_than_selected")
        return labels, "selection_inconsistency"
    raise AssertionError("unreachable candidate-loss comparison state")


def _cluster_geometry_summary(
    mesh: TriangleMesh,
    source_faces: tuple[int, ...],
) -> dict[str, object]:
    indices = sorted(
        {
            int(point_index)
            for face_id in source_faces
            for point_index in mesh.faces[int(face_id)]
        }
    )
    points = np.asarray(mesh.points[indices], dtype=float)
    extents = points.max(axis=0) - points.min(axis=0)
    max_extent = max(float(extents.max(initial=0.0)), 1e-12)
    sorted_extents = sorted((float(value) for value in extents), reverse=True)
    return {
        "face_count": len(source_faces),
        "point_count": len(indices),
        "aabb_extents": [float(value) for value in extents],
        "aabb_extent_ordered": sorted_extents,
        "aabb_aspect_ratios": [float(value / max_extent) for value in sorted_extents],
    }


def _best_nonselected_candidate(
    ranked: list[dict[str, object]],
    primitive_type: str,
) -> dict[str, object] | None:
    for row in ranked:
        if row["primitive_type"] != primitive_type:
            return row
    return None


def _rank_for_primitive(ranked: list[dict[str, object]], primitive_type: str) -> int:
    for index, row in enumerate(ranked, start=1):
        if row["primitive_type"] == primitive_type:
            return index
    raise ValueError(f"selected primitive {primitive_type!r} missing from candidate audit")


def _mean_or_none(values: list[float]) -> float | None:
    if not values:
        return None
    return float(sum(values) / len(values))


def _contact_or_mapping_gap(
    lane: NativeLaneArtifact,
    *,
    source_dir: str,
    device: str,
    claim_boundary: str,
) -> dict[str, object]:
    if not package_mapping_summary(lane.package)["fully_mapped"]:
        return _blocked_probe_payload(
            stage="newton_contact_smoke",
            status="mapping_gap",
            asset_id=lane.package.asset_id,
            package_id=lane.package.package_id,
            probe_type="contact_canary",
            claim_boundary=claim_boundary,
            fallback_reason="full_package_shape_coverage_required",
        )
    return run_newton_contact_smoke(
        lane.package,
        source_dir=source_dir,
        device=device,
        claim_boundary=claim_boundary,
    ).to_dict()


def _task_probe_payloads(
    lane: NativeLaneArtifact,
    *,
    source_dir: str,
    device: str,
    contact_claim_boundary: str,
    task_claim_boundary: str,
    drop_settle_options: DropSettleOptions,
    sphere_rain_options: SphereRainOptions,
) -> tuple[dict[str, object], dict[str, object]]:
    contact = _contact_or_mapping_gap(
        lane,
        source_dir=source_dir,
        device=device,
        claim_boundary=contact_claim_boundary,
    )
    if contact["status"] != "smoke_passed":
        tasks = {
            "drop_settle": _blocked_probe_payload(
                stage="newton_drop_settle",
                status="blocked_by_contact_canary",
                asset_id=lane.package.asset_id,
                package_id=lane.package.package_id,
                probe_type="drop_settle",
                claim_boundary=task_claim_boundary,
                fallback_reason=str(contact["status"]),
            ),
            "sphere_rain": _blocked_probe_payload(
                stage="newton_sphere_rain",
                status="blocked_by_contact_canary",
                asset_id=lane.package.asset_id,
                package_id=lane.package.package_id,
                probe_type="sphere_rain",
                claim_boundary=task_claim_boundary,
                fallback_reason=str(contact["status"]),
            ),
        }
        return contact, tasks

    return contact, {
        "drop_settle": run_newton_drop_settle(
            lane.package,
            source_dir=source_dir,
            device=device,
            options=drop_settle_options,
            claim_boundary=task_claim_boundary,
        ).to_dict(),
        "sphere_rain": run_newton_sphere_rain(
            lane.package,
            source_dir=source_dir,
            device=device,
            options=sphere_rain_options,
            claim_boundary=task_claim_boundary,
        ).to_dict(),
    }


def _blocked_probe_payload(
    *,
    stage: str,
    status: str,
    asset_id: str,
    package_id: str,
    probe_type: str,
    claim_boundary: str,
    fallback_reason: str,
) -> dict[str, object]:
    return NewtonDiagnosticReport(
        stage=stage,
        status=status,
        asset_id=asset_id,
        package_id=package_id,
        probe_type=probe_type,
        device="cpu",
        environment=None,
        primitive_count=0,
        type_counts={},
        shape_mappings=(),
        contact_canaries=(),
        claim_boundary=claim_boundary,
        fallback_reason=fallback_reason,
    ).to_dict()


def _aggregate_probe_status(statuses: list[str]) -> str:
    if statuses and all(status == "smoke_passed" for status in statuses):
        return "smoke_passed"
    if any(status == "runtime_failure" for status in statuses):
        return "runtime_failure"
    non_smoke = {status for status in statuses if status != "smoke_passed"}
    if non_smoke <= {"dependency_gap", "blocked_by_contact_canary"} and "dependency_gap" in non_smoke:
        return "dependency_gap"
    return "partial"
