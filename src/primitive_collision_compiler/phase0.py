from __future__ import annotations

from collections import Counter
from pathlib import Path
import math
import os
from typing import Any, Mapping

import numpy as np

from primitive_collision_compiler.assets.usd_smoke import (
    inspect_usd_asset,
    load_asset_manifest,
    resolve_asset_path,
)
from primitive_collision_compiler.baselines.convex_decomposition import (
    ConvexDecompositionUnavailable,
    build_convex_decomposition_package,
)
from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.objective import (
    CPDLikeObjectiveOptions,
    build_cpd_like_objective_report,
)
from primitive_collision_compiler.baselines.cpd_like.package import package_from_cpd_like_report
from primitive_collision_compiler.baselines.cpd_like.real_usd_comparison import (
    package_mapping_summary,
)
from primitive_collision_compiler.baselines.cpd_like.usd import USDMeshLoadError, load_first_mesh
from primitive_collision_compiler.config import load_compile_config
from primitive_collision_compiler.contracts import CollisionPackage, FallbackSpec, PrimitiveSpec
from primitive_collision_compiler.newton.diagnostics import run_newton_contact_smoke
from primitive_collision_compiler.newton.articulation_smoke import (
    ARTICULATION_SMOKE_CLAIM_BOUNDARY,
    GENERATED_PACKAGE_ROBOT_TASK_CLAIM_BOUNDARY,
    ArticulationSmokeOptions,
    run_newton_articulation_smoke,
    run_newton_generated_package_robot_task_probe,
)
from primitive_collision_compiler.newton.drop_settle import (
    DROP_SETTLE_CLAIM_BOUNDARY,
    DropSettleOptions,
    run_newton_drop_settle,
)
from primitive_collision_compiler.newton.sphere_rain import (
    SPHERE_RAIN_CLAIM_BOUNDARY,
    SphereRainOptions,
    run_newton_sphere_rain,
)
from primitive_collision_compiler.newton.stack_slide import (
    STACK_SLIDE_CLAIM_BOUNDARY,
    StackSlideOptions,
    run_newton_stack_slide,
)
from primitive_collision_compiler.robots.link_aware_package import (
    LINK_AWARE_PACKAGE_CLAIM_BOUNDARY,
    LINK_AWARE_PACKAGE_EVIDENCE_LEVEL,
    build_link_aware_robot_package,
)

PHASE0_STAGE = "phase0_asset_diagnostic_benchmark"
PHASE0_CLAIM_BOUNDARY = (
    "phase0_asset_diagnostic_benchmark_not_collision_quality_or_safety_validation"
)
PHASE0_EVIDENCE_LEVEL = "phase0_asset_simulation_checked_smoke"
PHASE0_CONTACT_CLAIM_BOUNDARY = (
    "phase0_contact_canary_preflight_not_collision_quality_or_safety_validation"
)
PHASE0_CPD_CLAIM_BOUNDARY = "phase0_cpd_style_candidate_not_cpd_reproduction_or_quality_claim"
PHASE0_CPD_EVIDENCE_LEVEL = "phase0_cpd_style_candidate_geometry_smoke"
PHASE0_LINK_BOUNDARY_CLAIM_BOUNDARY = (
    "phase0_link_boundary_audit_not_link_aware_robot_package_generation_or_whole_robot_validation"
)
PHASE0_LINK_BOUNDARY_EVIDENCE_LEVEL = "phase0_link_boundary_audit_smoke"
DEFAULT_CPD_PRIMITIVE_SUBSET = ("box", "sphere", "capsule")
OUTCOME_KEYS = ("accept", "fallback", "dependency_gap", "failure", "not_applicable")


def build_phase0_rigid_benchmark_report(config_path: str | Path) -> dict[str, object]:
    config = load_compile_config(config_path)
    phase0_section = _mapping_section(config.protocol.get("phase0_defaults"), "phase0_defaults")
    manifest_path = str(phase0_section.get("asset_manifest") or config.asset_path)
    baselines = _baseline_specs(phase0_section)
    assets = load_asset_manifest(manifest_path)
    if not assets:
        raise ValueError("Phase 0 asset manifest must contain at least one asset")

    diagnostic_section = _mapping_section(
        config.protocol.get("newton_diagnostic"),
        "newton_diagnostic",
        default={},
    )
    source_dir = _newton_source_dir(config.protocol.get("newton"))
    device = str(diagnostic_section.get("device", "cpu"))
    drop_options = _drop_settle_options(phase0_section, diagnostic_section)
    stack_options = _stack_slide_options(phase0_section, diagnostic_section)
    sphere_options = _sphere_rain_options(phase0_section, diagnostic_section)
    articulation_options = _articulation_smoke_options(phase0_section, diagnostic_section)
    generated_package_robot_task_options = _generated_package_robot_task_options(
        phase0_section,
        diagnostic_section,
        articulation_options,
    )

    cases: list[dict[str, object]] = []
    outcome_counter: Counter[str] = Counter({key: 0 for key in OUTCOME_KEYS})
    for asset in assets:
        case = _case_report(
            asset,
            baselines=baselines,
            config_max_primitives=config.max_primitives,
            phase0_section=phase0_section,
            source_dir=source_dir,
            device=device,
            drop_options=drop_options,
            stack_options=stack_options,
            sphere_options=sphere_options,
        )
        cases.append(case)
        outcome_counter.update(_case_outcomes(case))
    articulation_cases = _articulation_cases(
        phase0_section,
        source_dir=source_dir,
        device=device,
        options=articulation_options,
        generated_package_options=generated_package_robot_task_options,
    )
    for case in articulation_cases:
        outcome_counter.update(_articulation_case_outcomes(case))

    return _json_safe(
        {
            "stage": PHASE0_STAGE,
            "status": _aggregate_outcome_status(outcome_counter),
            "claim_boundary": PHASE0_CLAIM_BOUNDARY,
            "evidence_level": PHASE0_EVIDENCE_LEVEL,
            "config": str(config_path),
            "manifest": manifest_path,
            "asset_count": len(cases),
            "articulation_asset_count": len(articulation_cases),
            "roles": [str(case["asset_role"]) for case in cases],
            "baselines": baselines,
            "probes": list(config.verify),
            "source_dir": source_dir,
            "device": device,
            "report_scope": {
                "rigid_asset_diagnostic_cases": len(cases),
                "articulation_smoke_cases": len(articulation_cases),
                "link_aware_robot_package_generation": _has_link_aware_robot_package(
                    articulation_cases
                ),
                "generated_package_robot_task_checks": _has_generated_package_robot_task_check(
                    articulation_cases
                ),
                "whole_robot_collision_quality": False,
            },
            "run_semantics": "record_generation_not_validation_gate",
            "serialization_policy": "non_finite_diagnostic_values_are_serialized_as_null",
            "phase0_defaults": {
                "seeds": phase0_section.get("seeds"),
                "duration_seconds": phase0_section.get("duration_seconds"),
                "required_metrics": list(phase0_section.get("required_metrics", [])),
            },
            "outcome_counts": {key: int(outcome_counter.get(key, 0)) for key in OUTCOME_KEYS},
            "cases": cases,
            "articulation_cases": articulation_cases,
        }
    )


def _case_report(
    asset: Mapping[str, object],
    *,
    baselines: tuple[dict[str, object], ...],
    config_max_primitives: int,
    phase0_section: Mapping[str, object],
    source_dir: str,
    device: str,
    drop_options: DropSettleOptions,
    stack_options: StackSlideOptions,
    sphere_options: SphereRainOptions,
) -> dict[str, object]:
    raw_asset = dict(asset)
    role = str(raw_asset.get("role") or raw_asset.get("id") or "asset")
    asset_id = str(raw_asset.get("id") or role)
    asset_sha256 = str(
        raw_asset.get("source_sha256")
        or raw_asset.get("sha256")
        or raw_asset.get("local_sha256")
        or ""
    )
    resolved = resolve_asset_path(raw_asset)
    smoke_report = inspect_usd_asset(raw_asset).to_dict()
    asset_gate = _asset_gate(smoke_report)

    baseline_results: dict[str, dict[str, object]] = {}
    packages: dict[str, CollisionPackage] = {}
    if asset_gate["outcome"] != "accept":
        for spec in baselines:
            baseline_id = str(spec["id"])
            baseline_results[baseline_id] = _baseline_blocked_by_asset(
                spec,
                asset_gate=asset_gate,
            )
    else:
        try:
            mesh = load_first_mesh(resolved.path)
        except USDMeshLoadError as exc:
            for spec in baselines:
                baseline_id = str(spec["id"])
                baseline_results[baseline_id] = _baseline_failure(
                    spec,
                    status=_dependency_or_failure_status(str(exc)),
                    reason=str(exc),
                )
        else:
            for spec in baselines:
                baseline_id = str(spec["id"])
                try:
                    result, package = _baseline_result(
                        spec,
                        role=role,
                        asset_id=asset_id,
                        asset_sha256=asset_sha256,
                        asset_path=resolved.path,
                        mesh=mesh,
                        max_primitives=config_max_primitives,
                        phase0_section=phase0_section,
                    )
                except (USDMeshLoadError, ValueError) as exc:
                    result = _baseline_failure(
                        spec,
                        status=_dependency_or_failure_status(str(exc)),
                        reason=str(exc),
                    )
                    package = None
                baseline_results[baseline_id] = result
                if package is not None:
                    packages[baseline_id] = package

    probe_results: dict[str, dict[str, object]] = {}
    for spec in baselines:
        baseline_id = str(spec["id"])
        package = packages.get(baseline_id)
        if package is None:
            probe_results[baseline_id] = _blocked_probe_set(
                baseline_results[baseline_id],
                role=role,
            )
            continue
        probe_results[baseline_id] = _probe_set(
            package,
            role=role,
            source_dir=source_dir,
            device=device,
            drop_options=drop_options,
            stack_options=stack_options,
            sphere_options=sphere_options,
        )

    return {
        "asset_id": asset_id,
        "asset_role": role,
        "asset_path": resolved.path,
        "asset_path_kind": resolved.path_kind,
        "configured_path": resolved.configured_path,
        "source_path": resolved.source_path,
        "local_path": resolved.local_path,
        "asset_hashes": {
            "source_sha256": str(raw_asset.get("source_sha256") or ""),
            "sha256": str(raw_asset.get("sha256") or ""),
            "local_sha256": str(raw_asset.get("local_sha256") or ""),
        },
        "asset_smoke": smoke_report,
        "asset_gate": asset_gate,
        "baseline_results": baseline_results,
        "probe_results": probe_results,
        "outcome_counts": _case_outcome_counts(
            baseline_results,
            probe_results,
            asset_gate=asset_gate,
        ),
    }


def _articulation_cases(
    phase0_section: Mapping[str, object],
    *,
    source_dir: str,
    device: str,
    options: ArticulationSmokeOptions,
    generated_package_options: ArticulationSmokeOptions,
) -> list[dict[str, object]]:
    manifest_path = str(phase0_section.get("articulated_robot_manifest") or "")
    if not manifest_path:
        return []
    roles = phase0_section.get("articulated_robot_roles", [])
    role_filter = {str(role) for role in roles} if isinstance(roles, list | tuple) else set()
    assets = load_asset_manifest(manifest_path)
    cases = []
    for asset in assets:
        role = str(asset.get("role") or "")
        if role_filter and role not in role_filter:
            continue
        cases.append(
            _articulation_case_report(
                asset,
                source_dir=source_dir,
                device=device,
                options=options,
                generated_package_options=generated_package_options,
            )
        )
    return cases


def _articulation_case_report(
    asset: Mapping[str, object],
    *,
    source_dir: str,
    device: str,
    options: ArticulationSmokeOptions,
    generated_package_options: ArticulationSmokeOptions,
) -> dict[str, object]:
    raw_asset = dict(asset)
    role = str(raw_asset.get("role") or raw_asset.get("id") or "articulated_robot")
    asset_id = str(raw_asset.get("id") or role)
    resolved = resolve_asset_path(raw_asset)
    smoke_report = inspect_usd_asset(raw_asset).to_dict()
    asset_gate = _asset_gate(smoke_report)
    if asset_gate["outcome"] == "accept":
        robot_package_result = _build_robot_package_result(
            resolved.path,
            asset_id=asset_id,
            source_sha256=str(
                raw_asset.get("source_sha256")
                or raw_asset.get("sha256")
                or raw_asset.get("local_sha256")
                or ""
            ),
        )
        link_boundary_audit = dict(robot_package_result["link_boundary_audit"])
        articulation = _run_articulation_smoke_probe(
            resolved.path,
            source_dir=source_dir,
            device=device,
            options=options,
        )
        if (
            robot_package_result.get("status") == "generated"
            and link_boundary_audit.get("status") == "smoke_passed"
        ):
            generated_package_robot_task = _run_generated_package_robot_task_probe(
                resolved.path,
                collision_package=robot_package_result.get("collision_package"),
                source_dir=source_dir,
                device=device,
                options=generated_package_options,
            )
        else:
            generated_package_robot_task = _blocked_probe(
                "generated_package_robot_task_if_robot",
                status="blocked_by_link_boundary_audit",
                reason=str(
                    link_boundary_audit.get("fallback_reason")
                    or robot_package_result.get("fallback_reason")
                    or link_boundary_audit.get("status")
                    or robot_package_result.get("status")
                ),
                outcome=str(
                    robot_package_result.get("outcome")
                    or link_boundary_audit.get("outcome")
                    or "failure"
                ),
            )
    else:
        robot_package_result = _robot_package_blocked_by_asset(asset_gate)
        link_boundary_audit = _robot_link_boundary_audit(role)
        articulation = _blocked_probe(
            "articulation_smoke_if_robot",
            status="blocked_by_asset_smoke",
            reason=str(asset_gate.get("fallback_reason") or asset_gate.get("status")),
            outcome=str(asset_gate.get("outcome", "failure")),
        )
        generated_package_robot_task = _blocked_probe(
            "generated_package_robot_task_if_robot",
            status="blocked_by_asset_smoke",
            reason=str(asset_gate.get("fallback_reason") or asset_gate.get("status")),
            outcome=str(asset_gate.get("outcome", "failure")),
        )
    return {
        "asset_id": asset_id,
        "asset_role": role,
        "asset_path": resolved.path,
        "asset_path_kind": resolved.path_kind,
        "configured_path": resolved.configured_path,
        "source_path": resolved.source_path,
        "local_path": resolved.local_path,
        "asset_hashes": {
            "source_sha256": str(raw_asset.get("source_sha256") or ""),
            "sha256": str(raw_asset.get("sha256") or ""),
            "local_sha256": str(raw_asset.get("local_sha256") or ""),
        },
        "asset_smoke": smoke_report,
        "asset_gate": asset_gate,
        "robot_package_result": robot_package_result,
        "probe_results": {
            "link_boundary_audit": link_boundary_audit,
            "articulation_smoke_if_robot": articulation,
            "generated_package_robot_task_if_robot": generated_package_robot_task,
        },
        "outcome_counts": _articulation_case_outcome_counts(
            asset_gate=asset_gate,
            robot_package_result=robot_package_result,
            probe_results={
                "link_boundary_audit": link_boundary_audit,
                "articulation_smoke_if_robot": articulation,
                "generated_package_robot_task_if_robot": generated_package_robot_task,
            },
        ),
    }


def _baseline_result(
    spec: Mapping[str, object],
    *,
    role: str,
    asset_id: str,
    asset_sha256: str,
    asset_path: str,
    mesh: Any,
    max_primitives: int,
    phase0_section: Mapping[str, object],
) -> tuple[dict[str, object], CollisionPackage | None]:
    baseline_id = str(spec["id"])
    method = str(spec.get("method") or baseline_id)
    if baseline_id == "bounding_primitive":
        package = _bounding_primitive_package(
            role=role,
            baseline_id=baseline_id,
            source_sha256=asset_sha256,
            source_path=asset_path,
            mesh=mesh,
            method=method,
        )
        return _generated_baseline_payload(spec, package, status="generated"), package

    if baseline_id == "single_convex_hull":
        package = _convex_hull_fallback_package(
            role=role,
            baseline_id=baseline_id,
            source_sha256=asset_sha256,
            source_path=asset_path,
            mesh=mesh,
            method=method,
        )
        return (
            {
                **_baseline_header(spec),
                "status": "fallback",
                "outcome": "fallback",
                "fallback_reason": (
                    "single_convex_hull remains recorded as a simple convex_mesh fallback; "
                    "executable convex-decomposition baselines own generated convex hull probes"
                ),
                "primitive_or_hull_count": 1,
                "collision_package": package.to_dict(),
                "package_mapping": package_mapping_summary(package),
            },
            None,
        )

    if baseline_id in {
        "coacd_or_vhacd_if_available",
        "coacd_if_available",
        "vhacd_if_available",
    }:
        preferred_backends: tuple[str, ...] | None = None
        if baseline_id == "coacd_if_available" or method == "coacd":
            preferred_backends = ("coacd",)
        if baseline_id == "vhacd_if_available" or method == "vhacd":
            preferred_backends = ("vhacd",)
        try:
            package, executable = build_convex_decomposition_package(
                mesh,
                role=role,
                baseline_id=baseline_id,
                source_sha256=asset_sha256,
                source_path=asset_path,
                max_hulls=max_primitives,
                phase0_section=phase0_section,
                preferred_backends=preferred_backends,
            )
        except ConvexDecompositionUnavailable as exc:
            return (
                {
                    **_baseline_header(spec),
                    "status": "dependency_gap",
                    "outcome": "dependency_gap",
                    "fallback_reason": str(exc),
                    "primitive_or_hull_count": 0,
                },
                None,
            )
        payload = _generated_baseline_payload(spec, package, status="generated")
        payload["executable_baseline"] = executable
        return payload, package

    if baseline_id == "cpd_style_primitive_candidate_if_available":
        package, objective = _cpd_style_package(
            role=role,
            baseline_id=baseline_id,
            source_sha256=asset_sha256,
            source_path=asset_path,
            mesh=mesh,
            max_primitives=max_primitives,
            phase0_section=phase0_section,
        )
        status = "generated" if package.status == "smoke_passed" else package.status
        payload = _generated_baseline_payload(spec, package, status=status)
        payload["objective_report"] = objective
        return payload, package

    return (
        {
            **_baseline_header(spec),
            "status": "fallback",
            "outcome": "fallback",
            "fallback_reason": f"unknown Phase 0 baseline id: {baseline_id}",
            "primitive_or_hull_count": 0,
        },
        None,
    )


def _probe_set(
    package: CollisionPackage,
    *,
    role: str,
    source_dir: str,
    device: str,
    drop_options: DropSettleOptions,
    stack_options: StackSlideOptions,
    sphere_options: SphereRainOptions,
) -> dict[str, object]:
    contact = _run_contact_probe(package, source_dir=source_dir, device=device)
    if contact["status"] != "smoke_passed":
        drop = _blocked_probe(
            "body_state_drop_settle",
            status="blocked_by_contact_canary",
            reason=str(contact.get("fallback_reason") or contact["status"]),
            outcome=_outcome_for_status(str(contact["status"])),
        )
        stack = _blocked_probe(
            "stack_or_slide",
            status="blocked_by_contact_canary",
            reason=str(contact.get("fallback_reason") or contact["status"]),
            outcome=_outcome_for_status(str(contact["status"])),
        )
        sphere = _blocked_probe(
            "sphere_rain",
            status="blocked_by_contact_canary",
            reason=str(contact.get("fallback_reason") or contact["status"]),
            outcome=_outcome_for_status(str(contact["status"])),
        )
    else:
        drop = _run_drop_probe(
            package,
            source_dir=source_dir,
            device=device,
            options=drop_options,
        )
        stack = _run_stack_slide_probe(
            package,
            source_dir=source_dir,
            device=device,
            options=stack_options,
        )
        sphere = _run_sphere_probe(
            package,
            source_dir=source_dir,
            device=device,
            options=sphere_options,
        )

    return {
        "contact_canary": contact,
        "body_state_drop_settle": drop,
        "stack_or_slide": stack,
        "sphere_rain": sphere,
        "link_boundary_audit": _link_boundary_audit(package, role),
        "articulation_smoke_if_robot": _articulation_probe(role),
        "precision_rejection": _precision_rejection(role),
    }


def _blocked_probe_set(
    baseline_result: Mapping[str, object],
    *,
    role: str,
) -> dict[str, object]:
    outcome = str(baseline_result.get("outcome") or "fallback")
    reason = str(baseline_result.get("fallback_reason") or baseline_result.get("status"))
    blocked = {
        "contact_canary": _blocked_probe(
            "contact_canary",
            status="blocked_by_baseline",
            reason=reason,
            outcome=outcome,
        ),
        "body_state_drop_settle": _blocked_probe(
            "body_state_drop_settle",
            status="blocked_by_baseline",
            reason=reason,
            outcome=outcome,
        ),
        "stack_or_slide": _blocked_probe(
            "stack_or_slide",
            status="blocked_by_baseline",
            reason=reason,
            outcome=outcome,
        ),
        "sphere_rain": _blocked_probe(
            "sphere_rain",
            status="blocked_by_baseline",
            reason=reason,
            outcome=outcome,
        ),
        "link_boundary_audit": _link_boundary_audit(None, role),
        "articulation_smoke_if_robot": _articulation_probe(role),
        "precision_rejection": _precision_rejection(role),
    }
    return blocked


def _asset_gate(smoke_report: Mapping[str, object]) -> dict[str, object]:
    status = str(smoke_report.get("status") or "unknown")
    return {
        "stage": "phase0_asset_gate",
        "status": status,
        "outcome": _asset_gate_outcome(status),
        "fallback_reason": None if status == "smoke_passed" else status,
        "claim_boundary": PHASE0_CLAIM_BOUNDARY,
        "evidence_level": PHASE0_EVIDENCE_LEVEL,
    }


def _asset_gate_outcome(status: str) -> str:
    if status == "smoke_passed":
        return "accept"
    if status in {"dependency_gap", "missing_asset"}:
        return "dependency_gap"
    return "failure"


def _baseline_blocked_by_asset(
    spec: Mapping[str, object],
    *,
    asset_gate: Mapping[str, object],
) -> dict[str, object]:
    return {
        **_baseline_header(spec),
        "status": "blocked_by_asset_smoke",
        "outcome": str(asset_gate.get("outcome", "failure")),
        "fallback_reason": str(asset_gate.get("fallback_reason") or asset_gate.get("status")),
        "primitive_or_hull_count": 0,
    }


def _run_contact_probe(
    package: CollisionPackage,
    *,
    source_dir: str,
    device: str,
) -> dict[str, object]:
    if not source_dir:
        return _blocked_probe(
            "contact_canary",
            status="dependency_gap",
            reason="newton.source_dir or NEWTON_SOURCE_DIR is not configured",
            outcome="dependency_gap",
        )
    report = run_newton_contact_smoke(
        package,
        source_dir=source_dir,
        device=device,
        claim_boundary=PHASE0_CONTACT_CLAIM_BOUNDARY,
    ).to_dict()
    return _probe_payload(report)


def _run_drop_probe(
    package: CollisionPackage,
    *,
    source_dir: str,
    device: str,
    options: DropSettleOptions,
) -> dict[str, object]:
    report = run_newton_drop_settle(
        package,
        source_dir=source_dir,
        device=device,
        options=options,
        claim_boundary=DROP_SETTLE_CLAIM_BOUNDARY,
    ).to_dict()
    return _probe_payload(report)


def _run_stack_slide_probe(
    package: CollisionPackage,
    *,
    source_dir: str,
    device: str,
    options: StackSlideOptions,
) -> dict[str, object]:
    report = run_newton_stack_slide(
        package,
        source_dir=source_dir,
        device=device,
        options=options,
        claim_boundary=STACK_SLIDE_CLAIM_BOUNDARY,
    ).to_dict()
    return _probe_payload(report)


def _run_sphere_probe(
    package: CollisionPackage,
    *,
    source_dir: str,
    device: str,
    options: SphereRainOptions,
) -> dict[str, object]:
    report = run_newton_sphere_rain(
        package,
        source_dir=source_dir,
        device=device,
        options=options,
        claim_boundary=SPHERE_RAIN_CLAIM_BOUNDARY,
    ).to_dict()
    return _probe_payload(report)


def _run_articulation_smoke_probe(
    asset_path: str,
    *,
    source_dir: str,
    device: str,
    options: ArticulationSmokeOptions,
) -> dict[str, object]:
    return run_newton_articulation_smoke(
        asset_path=asset_path,
        source_dir=source_dir,
        device=device,
        options=options,
        claim_boundary=ARTICULATION_SMOKE_CLAIM_BOUNDARY,
    )


def _run_generated_package_robot_task_probe(
    asset_path: str,
    *,
    collision_package: Mapping[str, object] | None,
    source_dir: str,
    device: str,
    options: ArticulationSmokeOptions,
) -> dict[str, object]:
    return run_newton_generated_package_robot_task_probe(
        asset_path=asset_path,
        collision_package=collision_package,
        source_dir=source_dir,
        device=device,
        options=options,
        claim_boundary=GENERATED_PACKAGE_ROBOT_TASK_CLAIM_BOUNDARY,
    )


def _probe_payload(report: Mapping[str, object]) -> dict[str, object]:
    status = str(report.get("status", "smoke_failed"))
    return {
        **dict(report),
        "outcome": _outcome_for_status(status),
    }


def _blocked_probe(
    probe_id: str,
    *,
    status: str,
    reason: str,
    outcome: str,
) -> dict[str, object]:
    return {
        "stage": f"phase0_{probe_id}",
        "status": status,
        "probe_type": probe_id,
        "outcome": outcome,
        "fallback_reason": reason,
        "claim_boundary": PHASE0_CLAIM_BOUNDARY,
        "evidence_level": PHASE0_EVIDENCE_LEVEL,
    }


def _link_boundary_audit(package: CollisionPackage | None, role: str) -> dict[str, object]:
    primitive_count = 0 if package is None else len(package.primitives)
    return {
        "stage": "phase0_link_boundary_audit",
        "status": "not_applicable",
        "probe_type": "link_boundary_audit",
        "outcome": "not_applicable",
        "metrics": {
            "asset_role": role,
            "cross_link_merge_count": 0,
            "per_link_primitive_count": {},
            "rigid_asset_no_link_tree": True,
            "primitive_count": primitive_count,
        },
        "claim_boundary": PHASE0_CLAIM_BOUNDARY,
        "evidence_level": PHASE0_EVIDENCE_LEVEL,
        "fallback_reason": "rigid_asset_no_articulation_links",
    }


def _build_robot_package_result(
    asset_path: str,
    *,
    asset_id: str,
    source_sha256: str,
) -> dict[str, object]:
    try:
        return build_link_aware_robot_package(
            asset_path=asset_path,
            asset_id=asset_id,
            source_sha256=source_sha256,
        ).to_dict()
    except Exception as exc:
        return {
            "stage": "phase0_link_aware_robot_package_generation",
            "status": _dependency_or_failure_status(str(exc)),
            "outcome": _outcome_for_status(_dependency_or_failure_status(str(exc))),
            "primitive_or_hull_count": 0,
            "collision_package": None,
            "links": [],
            "joint_edges": [],
            "link_boundary_audit": {
                "stage": "phase0_link_boundary_audit",
                "status": _dependency_or_failure_status(str(exc)),
                "probe_type": "link_boundary_audit",
                "outcome": _outcome_for_status(_dependency_or_failure_status(str(exc))),
                "metrics": {
                    "link_aware_package_generated": False,
                    "link_count": 0,
                    "primitive_count": 0,
                    "cross_link_merge_count": None,
                    "links_without_primitive_count": None,
                    "links_without_primitives": [],
                    "meshless_link_placeholder_count": 0,
                    "per_link_primitive_count": {},
                },
                "failure_labels": ["link_aware_package_generation_failed"],
                "claim_boundary": PHASE0_LINK_BOUNDARY_CLAIM_BOUNDARY,
                "evidence_level": PHASE0_LINK_BOUNDARY_EVIDENCE_LEVEL,
                "fallback_reason": f"{type(exc).__name__}: {exc}",
            },
            "claim_boundary": LINK_AWARE_PACKAGE_CLAIM_BOUNDARY,
            "evidence_level": LINK_AWARE_PACKAGE_EVIDENCE_LEVEL,
            "fallback_reason": f"{type(exc).__name__}: {exc}",
        }


def _robot_package_blocked_by_asset(asset_gate: Mapping[str, object]) -> dict[str, object]:
    outcome = str(asset_gate.get("outcome", "failure"))
    reason = str(asset_gate.get("fallback_reason") or asset_gate.get("status"))
    return {
        "stage": "phase0_link_aware_robot_package_generation",
        "status": "blocked_by_asset_smoke",
        "outcome": outcome,
        "primitive_or_hull_count": 0,
        "collision_package": None,
        "links": [],
        "joint_edges": [],
        "link_boundary_audit": {
            "stage": "phase0_link_boundary_audit",
            "status": "blocked_by_asset_smoke",
            "probe_type": "link_boundary_audit",
            "outcome": outcome,
            "metrics": {
                "link_aware_package_generated": False,
                "link_count": 0,
                "primitive_count": 0,
                "cross_link_merge_count": None,
                "links_without_primitive_count": None,
                "links_without_primitives": [],
                "meshless_link_placeholder_count": 0,
                "per_link_primitive_count": {},
            },
            "failure_labels": ["asset_smoke_blocked_link_package_generation"],
            "claim_boundary": PHASE0_LINK_BOUNDARY_CLAIM_BOUNDARY,
            "evidence_level": PHASE0_LINK_BOUNDARY_EVIDENCE_LEVEL,
            "fallback_reason": reason,
        },
        "claim_boundary": LINK_AWARE_PACKAGE_CLAIM_BOUNDARY,
        "evidence_level": LINK_AWARE_PACKAGE_EVIDENCE_LEVEL,
        "fallback_reason": reason,
    }


def _robot_link_boundary_audit(role: str) -> dict[str, object]:
    return {
        "stage": "phase0_link_boundary_audit",
        "status": "not_run",
        "probe_type": "link_boundary_audit",
        "outcome": "fallback",
        "metrics": {
            "asset_role": role,
            "cross_link_merge_count": None,
            "links_without_primitive_count": None,
            "links_without_primitives": [],
            "meshless_link_placeholder_count": 0,
            "per_link_primitive_count": {},
            "link_aware_package_generated": False,
        },
        "claim_boundary": PHASE0_LINK_BOUNDARY_CLAIM_BOUNDARY,
        "evidence_level": PHASE0_LINK_BOUNDARY_EVIDENCE_LEVEL,
        "fallback_reason": "asset_smoke_blocked_link_package_generation",
    }


def _articulation_probe(role: str) -> dict[str, object]:
    return {
        "stage": "phase0_articulation_smoke",
        "status": "not_applicable",
        "probe_type": "articulation_smoke_if_robot",
        "outcome": "not_applicable",
        "metrics": {"asset_role": role, "rigid_asset_no_joint_tree": True},
        "claim_boundary": PHASE0_CLAIM_BOUNDARY,
        "evidence_level": PHASE0_EVIDENCE_LEVEL,
        "fallback_reason": "rigid_asset_not_robot",
    }


def _precision_rejection(role: str) -> dict[str, object]:
    if role != "precision_negative_control":
        return {
            "stage": "phase0_precision_rejection",
            "status": "not_applicable",
            "probe_type": "precision_rejection",
            "outcome": "not_applicable",
            "metrics": {"asset_role": role, "precision_negative_control": False},
            "claim_boundary": PHASE0_CLAIM_BOUNDARY,
            "evidence_level": PHASE0_EVIDENCE_LEVEL,
            "fallback_reason": "asset_role_not_precision_negative_control",
        }
    return {
        "stage": "phase0_precision_rejection",
        "status": "manual_review_required",
        "probe_type": "precision_rejection",
        "outcome": "fallback",
        "metrics": {
            "asset_role": role,
            "precision_negative_control": True,
            "rejection_or_fallback_decision": "manual_review_required",
        },
        "claim_boundary": PHASE0_CLAIM_BOUNDARY,
        "evidence_level": PHASE0_EVIDENCE_LEVEL,
        "fallback_reason": (
            "precision negative control requires a task-specific tolerance before "
            "primitive-only acceptance"
        ),
    }


def _bounding_primitive_package(
    *,
    role: str,
    baseline_id: str,
    source_sha256: str,
    source_path: str,
    mesh: Any,
    method: str,
) -> CollisionPackage:
    bounds_min = np.min(mesh.points, axis=0)
    bounds_max = np.max(mesh.points, axis=0)
    half_extents = np.maximum((bounds_max - bounds_min) * 0.5, 1.0e-6)
    center = (bounds_min + bounds_max) * 0.5
    volume = float(8.0 * half_extents[0] * half_extents[1] * half_extents[2])
    package_asset_id = f"{role}_{baseline_id}"
    primitive = PrimitiveSpec(
        primitive_id=f"{package_asset_id}:primitive:0",
        kind="box",
        dimensions={"half_extents": [float(value) for value in half_extents]},
        center=tuple(float(value) for value in center),
        source_faces=tuple(range(int(mesh.face_count))),
        volume=volume,
        weighted_volume=volume,
        conversion_status="candidate",
    )
    return CollisionPackage(
        package_id=f"{package_asset_id}:phase0_bbox",
        asset_id=package_asset_id,
        source_path=source_path,
        method=method,
        stage="phase0_bounding_primitive",
        status="smoke_passed",
        claim_boundary=PHASE0_CLAIM_BOUNDARY,
        mesh_point_count=int(len(mesh.points)),
        mesh_face_count=int(mesh.face_count),
        max_source_faces=int(mesh.face_count),
        primitive_subset=("box",),
        primitives=(primitive,),
        source_sha256=source_sha256,
    )


def _convex_hull_fallback_package(
    *,
    role: str,
    baseline_id: str,
    source_sha256: str,
    source_path: str,
    mesh: Any,
    method: str,
) -> CollisionPackage:
    package_asset_id = f"{role}_{baseline_id}"
    return CollisionPackage(
        package_id=f"{package_asset_id}:phase0_convex_hull_fallback",
        asset_id=package_asset_id,
        source_path=source_path,
        source_sha256=source_sha256,
        method=method,
        stage="phase0_single_convex_hull",
        status="fallback",
        claim_boundary=PHASE0_CLAIM_BOUNDARY,
        mesh_point_count=int(len(mesh.points)),
        mesh_face_count=int(mesh.face_count),
        max_source_faces=int(mesh.face_count),
        primitive_subset=(),
        primitives=(),
        fallback=FallbackSpec(
            method="convex_mesh",
            reason="convex hull package is not Newton primitive-mappable in this runner",
        ),
    )


def _cpd_style_package(
    *,
    role: str,
    baseline_id: str,
    source_sha256: str,
    source_path: str,
    mesh: Any,
    max_primitives: int,
    phase0_section: Mapping[str, object],
) -> tuple[CollisionPackage, dict[str, object]]:
    cpd_options = _cpd_like_options(phase0_section)
    max_source_faces = _max_source_faces_for_role(phase0_section, role)
    cpd_mesh = (
        load_first_mesh(source_path, max_faces=max_source_faces)
        if max_source_faces is not None
        else mesh
    )
    decomposition = decompose_mesh(
        cpd_mesh,
        max_primitives=max_primitives,
        primitive_subset=tuple(cpd_options["primitive_subset"]),
        component_merge=str(cpd_options["component_merge"]),
        merge_search_policy=str(cpd_options["merge_search_policy"]),
        excess_volume_threshold_fraction=cpd_options["excess_volume_threshold_fraction"],
        report_merge_trace=str(cpd_options["report_merge_trace"]),
    )
    package_asset_id = f"{role}_{baseline_id}"
    objective_options = CPDLikeObjectiveOptions(
        claim_boundary=PHASE0_CPD_CLAIM_BOUNDARY,
        evidence_level=PHASE0_CPD_EVIDENCE_LEVEL,
    )
    # Keep objective generation in the report path so paper-aligned geometry metrics are recorded
    # next to the simulation gate outputs.
    objective = build_cpd_like_objective_report(
        decomposition,
        asset_id=package_asset_id,
        source_path=source_path,
        max_source_faces=max_source_faces or int(cpd_mesh.face_count),
        options=objective_options,
    ).to_dict()
    package = package_from_cpd_like_report(
        decomposition,
        asset_id=package_asset_id,
        source_path=source_path,
        source_sha256=source_sha256,
        claim_boundary=PHASE0_CPD_CLAIM_BOUNDARY,
        max_source_faces=max_source_faces or int(cpd_mesh.face_count),
    )
    return _with_package_status(package, objective), objective


def _with_package_status(package: CollisionPackage, objective: Mapping[str, object]) -> CollisionPackage:
    # CollisionPackage is frozen; reconstruct with the objective status only when it exposes a
    # stronger failure state than the decomposition adapter.
    status = str(objective.get("status") or package.status)
    if status == package.status:
        return package
    return CollisionPackage(
        asset_id=package.asset_id,
        primitives=package.primitives,
        fallback=package.fallback,
        package_id=package.package_id,
        source_path=package.source_path,
        source_sha256=package.source_sha256,
        method=package.method,
        stage=package.stage,
        status=status,
        claim_boundary=package.claim_boundary,
        mesh_point_count=package.mesh_point_count,
        mesh_face_count=package.mesh_face_count,
        max_source_faces=package.max_source_faces,
        primitive_subset=package.primitive_subset,
        unsupported_primitives=package.unsupported_primitives,
    )


def _generated_baseline_payload(
    spec: Mapping[str, object],
    package: CollisionPackage,
    *,
    status: str,
) -> dict[str, object]:
    mapping = package_mapping_summary(package)
    package_status = str(status)
    outcome = "accept" if mapping["fully_mapped"] and package_status in {"generated", "smoke_passed"} else "fallback"
    return {
        **_baseline_header(spec),
        "status": package_status,
        "outcome": outcome,
        "primitive_or_hull_count": len(package.primitives),
        "collision_package": package.to_dict(),
        "package_mapping": mapping,
        "fallback_reason": None if outcome == "accept" else "package_not_fully_mapped",
    }


def _baseline_failure(
    spec: Mapping[str, object],
    *,
    status: str,
    reason: str,
) -> dict[str, object]:
    return {
        **_baseline_header(spec),
        "status": status,
        "outcome": _outcome_for_status(status),
        "fallback_reason": reason,
        "primitive_or_hull_count": 0,
    }


def _baseline_header(spec: Mapping[str, object]) -> dict[str, object]:
    return {
        "id": str(spec.get("id")),
        "method": str(spec.get("method") or spec.get("id")),
        "required": bool(spec.get("required", False)),
    }


def _baseline_specs(phase0_section: Mapping[str, object]) -> tuple[dict[str, object], ...]:
    raw = phase0_section.get("baselines", [])
    if not isinstance(raw, list) or not raw:
        raise ValueError("phase0_defaults.baselines must be a non-empty list")
    result: list[dict[str, object]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"phase0_defaults.baselines[{index}] must be a mapping")
        baseline_id = str(item.get("id") or "")
        if not baseline_id:
            raise ValueError(f"phase0_defaults.baselines[{index}].id must be non-empty")
        result.append(dict(item))
    return tuple(result)


def _max_source_faces_for_role(phase0_section: Mapping[str, object], role: str) -> int | None:
    cpd_like = phase0_section.get("cpd_like", {})
    if not isinstance(cpd_like, Mapping):
        return None
    raw_by_role = cpd_like.get("max_source_faces_by_role", {})
    if isinstance(raw_by_role, Mapping) and role in raw_by_role:
        return int(raw_by_role[role])
    raw_default = cpd_like.get("max_source_faces")
    if raw_default in (None, ""):
        return None
    return int(raw_default)


def _cpd_like_options(phase0_section: Mapping[str, object]) -> dict[str, object]:
    raw = phase0_section.get("cpd_like", {})
    if not isinstance(raw, Mapping):
        raw = {}
    primitive_subset = raw.get("primitive_subset", DEFAULT_CPD_PRIMITIVE_SUBSET)
    if isinstance(primitive_subset, str) or not isinstance(primitive_subset, (list, tuple)):
        raise ValueError("phase0_defaults.cpd_like.primitive_subset must be a list of strings")
    return {
        "primitive_subset": tuple(str(item) for item in primitive_subset),
        "component_merge": str(raw.get("component_merge", "virtual_pairwise")),
        "merge_search_policy": str(raw.get("merge_search_policy", "topology_then_virtual")),
        "excess_volume_threshold_fraction": _optional_float(
            raw.get("excess_volume_threshold_fraction")
        ),
        "report_merge_trace": str(raw.get("report_merge_trace", "summary")),
    }


def _drop_settle_options(
    phase0_section: Mapping[str, object],
    diagnostic_section: Mapping[str, object],
) -> DropSettleOptions:
    probe = _probe_config(phase0_section, "body_state_drop_settle")
    initial = _mapping_section(probe.get("initial_conditions"), "body_state_drop_settle", default={})
    drop_section = _mapping_section(
        diagnostic_section.get("drop_settle"),
        "newton_diagnostic.drop_settle",
        default={},
    )
    frames = int(drop_section.get("frames") or _duration_frames(phase0_section, probe))
    return DropSettleOptions(
        height_m=float(drop_section.get("height_m", initial.get("height_m", 0.25))),
        frames=frames,
        substeps=int(drop_section.get("substeps", 4)),
        frame_dt_seconds=float(drop_section.get("frame_dt_seconds", 1.0 / 60.0)),
        iterations=int(drop_section.get("iterations", 2)),
        friction=float(drop_section.get("friction", 0.5)),
        max_floor_breach_m=float(drop_section.get("max_floor_breach_m", 0.05)),
        max_settle_linear_speed_mps=float(
            drop_section.get("max_settle_linear_speed_mps", 0.05)
        ),
    )


def _stack_slide_options(
    phase0_section: Mapping[str, object],
    diagnostic_section: Mapping[str, object],
) -> StackSlideOptions:
    probe = _probe_config(phase0_section, "stack_or_slide")
    initial = _mapping_section(probe.get("initial_conditions"), "stack_or_slide", default={})
    stack_section = _mapping_section(
        diagnostic_section.get("stack_or_slide"),
        "newton_diagnostic.stack_or_slide",
        default={},
    )
    raw_probe_half_extents = stack_section.get("probe_half_extents_m", (0.05, 0.05, 0.05))
    if isinstance(raw_probe_half_extents, list | tuple):
        probe_half_extents = tuple(float(value) for value in raw_probe_half_extents)
    else:
        raise ValueError("newton_diagnostic.stack_or_slide.probe_half_extents_m must be a list")
    if len(probe_half_extents) != 3:
        raise ValueError("newton_diagnostic.stack_or_slide.probe_half_extents_m must have length 3")
    return StackSlideOptions(
        probe_half_extents_m=probe_half_extents,  # type: ignore[arg-type]
        lateral_velocity_mps=float(
            stack_section.get(
                "lateral_velocity_mps",
                initial.get("lateral_velocity_mps", 0.1),
            )
        ),
        spawn_clearance_m=float(stack_section.get("spawn_clearance_m", 0.01)),
        frames=int(stack_section.get("frames") or _duration_frames(phase0_section, probe)),
        substeps=int(stack_section.get("substeps", 4)),
        frame_dt_seconds=float(stack_section.get("frame_dt_seconds", 1.0 / 60.0)),
        iterations=int(stack_section.get("iterations", 4)),
        friction=float(stack_section.get("friction", 0.7)),
        max_slide_distance_m=float(stack_section.get("max_slide_distance_m", 0.25)),
        max_drop_below_support_m=float(stack_section.get("max_drop_below_support_m", 0.05)),
        max_settle_linear_speed_mps=float(
            stack_section.get("max_settle_linear_speed_mps", 0.25)
        ),
        rigid_contact_max=int(stack_section.get("rigid_contact_max", 4096)),
    )


def _sphere_rain_options(
    phase0_section: Mapping[str, object],
    diagnostic_section: Mapping[str, object],
) -> SphereRainOptions:
    probe = _probe_config(phase0_section, "sphere_rain")
    initial = _mapping_section(probe.get("initial_conditions"), "sphere_rain", default={})
    sphere_section = _mapping_section(
        diagnostic_section.get("sphere_rain"),
        "newton_diagnostic.sphere_rain",
        default={},
    )
    sphere_count = int(sphere_section.get("sphere_count") or initial.get("sphere_count", 9))
    count_x, count_y = _grid_counts(sphere_count)
    return SphereRainOptions(
        sphere_count_x=int(sphere_section.get("sphere_count_x", count_x)),
        sphere_count_y=int(sphere_section.get("sphere_count_y", count_y)),
        sphere_radius_m=float(
            sphere_section.get("sphere_radius_m", initial.get("sphere_radius_m", 0.025))
        ),
        spawn_height_m=float(sphere_section.get("spawn_height_m", 1.0)),
        frames=int(sphere_section.get("frames") or _duration_frames(phase0_section, probe)),
        substeps=int(sphere_section.get("substeps", 4)),
        frame_dt_seconds=float(sphere_section.get("frame_dt_seconds", 1.0 / 60.0)),
        iterations=int(sphere_section.get("iterations", 4)),
        friction=float(sphere_section.get("friction", 0.5)),
        min_contact_density=float(sphere_section.get("min_contact_density", 0.05)),
        require_final_contact=bool(sphere_section.get("require_final_contact", False)),
        rigid_contact_max=int(sphere_section.get("rigid_contact_max", 4096)),
    )


def _articulation_smoke_options(
    phase0_section: Mapping[str, object],
    diagnostic_section: Mapping[str, object],
) -> ArticulationSmokeOptions:
    probe = _probe_config(phase0_section, "articulation_smoke_if_robot")
    initial = _mapping_section(
        probe.get("initial_conditions"),
        "articulation_smoke_if_robot.initial_conditions",
        default={},
    )
    solver = _mapping_section(
        probe.get("solver"),
        "articulation_smoke_if_robot.solver",
        default={},
    )
    articulation_section = _mapping_section(
        diagnostic_section.get("articulation_smoke_if_robot"),
        "newton_diagnostic.articulation_smoke_if_robot",
        default={},
    )
    return ArticulationSmokeOptions(
        hold_frames=int(
            articulation_section.get("hold_frames")
            or _duration_frames(phase0_section, probe)
        ),
        trajectory_delta_rad=float(articulation_section.get("trajectory_delta_rad", 0.05)),
        max_gravity_hold_joint_drift=float(
            articulation_section.get("max_gravity_hold_joint_drift", 0.01)
        ),
        min_end_effector_pose_delta_m=float(
            articulation_section.get("min_end_effector_pose_delta_m", 1.0e-6)
        ),
        substeps=int(articulation_section.get("substeps", solver.get("substeps", 4))),
        frame_dt_seconds=float(
            articulation_section.get("frame_dt_seconds", solver.get("frame_dt_seconds", 1.0 / 60.0))
        ),
        iterations=int(articulation_section.get("iterations", solver.get("iterations", 2))),
        mesh_approximation=str(
            articulation_section.get(
                "mesh_approximation",
                initial.get("mesh_approximation", "bounding_box"),
            )
        ),
        collapse_fixed_joints=bool(
            articulation_section.get(
                "collapse_fixed_joints",
                initial.get("collapse_fixed_joints", True),
            )
        ),
        enable_self_collisions=bool(
            articulation_section.get(
                "enable_self_collisions",
                initial.get("enable_self_collisions", False),
            )
        ),
        load_visual_shapes=bool(articulation_section.get("load_visual_shapes", False)),
        hide_collision_shapes=bool(articulation_section.get("hide_collision_shapes", True)),
    )


def _generated_package_robot_task_options(
    phase0_section: Mapping[str, object],
    diagnostic_section: Mapping[str, object],
    base_options: ArticulationSmokeOptions,
) -> ArticulationSmokeOptions:
    probe = _probe_config(phase0_section, "generated_package_robot_task_if_robot")
    initial = _mapping_section(
        probe.get("initial_conditions"),
        "generated_package_robot_task_if_robot.initial_conditions",
        default={},
    )
    solver = _mapping_section(
        probe.get("solver"),
        "generated_package_robot_task_if_robot.solver",
        default={},
    )
    generated_section = _mapping_section(
        diagnostic_section.get("generated_package_robot_task_if_robot"),
        "newton_diagnostic.generated_package_robot_task_if_robot",
        default={},
    )
    return ArticulationSmokeOptions(
        hold_frames=int(
            generated_section.get("hold_frames")
            or (
                _duration_frames(phase0_section, probe)
                if probe
                else base_options.hold_frames
            )
        ),
        trajectory_delta_rad=float(
            generated_section.get(
                "trajectory_delta_rad",
                base_options.trajectory_delta_rad,
            )
        ),
        max_gravity_hold_joint_drift=float(
            generated_section.get(
                "max_gravity_hold_joint_drift",
                base_options.max_gravity_hold_joint_drift,
            )
        ),
        min_end_effector_pose_delta_m=float(
            generated_section.get(
                "min_end_effector_pose_delta_m",
                base_options.min_end_effector_pose_delta_m,
            )
        ),
        substeps=int(
            generated_section.get(
                "substeps",
                solver.get("substeps", base_options.substeps),
            )
        ),
        frame_dt_seconds=float(
            generated_section.get(
                "frame_dt_seconds",
                solver.get("frame_dt_seconds", base_options.frame_dt_seconds),
            )
        ),
        iterations=int(
            generated_section.get(
                "iterations",
                solver.get("iterations", base_options.iterations),
            )
        ),
        mesh_approximation=str(
            generated_section.get(
                "mesh_approximation",
                initial.get("mesh_approximation", ""),
            )
        ),
        collapse_fixed_joints=bool(
            generated_section.get(
                "collapse_fixed_joints",
                initial.get("collapse_fixed_joints", False),
            )
        ),
        enable_self_collisions=bool(
            generated_section.get(
                "enable_self_collisions",
                initial.get("enable_self_collisions", base_options.enable_self_collisions),
            )
        ),
        load_visual_shapes=bool(generated_section.get("load_visual_shapes", False)),
        hide_collision_shapes=bool(generated_section.get("hide_collision_shapes", True)),
    )


def _probe_config(phase0_section: Mapping[str, object], probe_id: str) -> Mapping[str, object]:
    probes = _mapping_section(phase0_section.get("probes"), "phase0_defaults.probes", default={})
    return _mapping_section(probes.get(probe_id), probe_id, default={})


def _duration_frames(
    phase0_section: Mapping[str, object],
    probe_config: Mapping[str, object],
) -> int:
    solver = _mapping_section(probe_config.get("solver"), "probe.solver", default={})
    duration = float(solver.get("duration_seconds") or phase0_section.get("duration_seconds") or 2.0)
    return max(1, int(round(duration * 60.0)))


def _grid_counts(sphere_count: int) -> tuple[int, int]:
    if sphere_count < 1:
        return (1, 1)
    count_x = int(math.ceil(math.sqrt(sphere_count)))
    count_y = int(math.ceil(float(sphere_count) / float(count_x)))
    return count_x, count_y


def _newton_source_dir(raw_newton_section: object) -> str:
    section = _mapping_section(raw_newton_section, "newton", default={})
    raw_source = section.get("source_dir") or os.environ.get("NEWTON_SOURCE_DIR", "")
    if not raw_source:
        return ""
    expanded = os.path.expanduser(os.path.expandvars(str(raw_source)))
    if "$" in expanded:
        return ""
    return expanded


def _mapping_section(
    value: object,
    name: str,
    *,
    default: Mapping[str, object] | None = None,
) -> Mapping[str, object]:
    if value in (None, ""):
        return {} if default is None else default
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")
    return value


def _optional_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _dependency_or_failure_status(message: str) -> str:
    lowered = message.lower()
    if "dependency_gap" in lowered or "pxr" in lowered or "missing" in lowered:
        return "dependency_gap"
    return "failure"


def _outcome_for_status(status: str) -> str:
    if status in {"smoke_passed", "generated"}:
        return "accept"
    if status == "not_applicable":
        return "not_applicable"
    if status == "dependency_gap":
        return "dependency_gap"
    if status in {
        "fallback",
        "mapping_gap",
        "blocked_by_contact_canary",
        "blocked_by_baseline",
        "manual_review_required",
        "unsupported_probe",
        "partial",
    }:
        return "fallback"
    return "failure"


def _case_outcomes(case: Mapping[str, object]) -> list[str]:
    outcomes: list[str] = []
    asset_gate = case.get("asset_gate", {})
    if isinstance(asset_gate, Mapping):
        outcomes.append(str(asset_gate.get("outcome", "failure")))
    baseline_results = case.get("baseline_results", {})
    if isinstance(baseline_results, Mapping):
        outcomes.extend(
            str(result.get("outcome", "failure"))
            for result in baseline_results.values()
            if isinstance(result, Mapping)
        )
    probe_results = case.get("probe_results", {})
    if isinstance(probe_results, Mapping):
        for by_probe in probe_results.values():
            if not isinstance(by_probe, Mapping):
                continue
            outcomes.extend(
                str(result.get("outcome", "failure"))
                for result in by_probe.values()
                if isinstance(result, Mapping)
            )
    return outcomes


def _articulation_case_outcomes(case: Mapping[str, object]) -> list[str]:
    outcomes: list[str] = []
    asset_gate = case.get("asset_gate", {})
    if isinstance(asset_gate, Mapping):
        outcomes.append(str(asset_gate.get("outcome", "failure")))
    robot_package_result = case.get("robot_package_result", {})
    if isinstance(robot_package_result, Mapping):
        outcomes.append(str(robot_package_result.get("outcome", "failure")))
    probe_results = case.get("probe_results", {})
    if isinstance(probe_results, Mapping):
        outcomes.extend(
            str(result.get("outcome", "failure"))
            for result in probe_results.values()
            if isinstance(result, Mapping)
        )
    return outcomes


def _case_outcome_counts(
    baseline_results: Mapping[str, object],
    probe_results: Mapping[str, object],
    asset_gate: Mapping[str, object] | None = None,
) -> dict[str, int]:
    counter: Counter[str] = Counter({key: 0 for key in OUTCOME_KEYS})
    if asset_gate is not None:
        counter.update([str(asset_gate.get("outcome", "failure"))])
    counter.update(
        str(result.get("outcome", "failure"))
        for result in baseline_results.values()
        if isinstance(result, Mapping)
    )
    for by_probe in probe_results.values():
        if not isinstance(by_probe, Mapping):
            continue
        counter.update(
            str(result.get("outcome", "failure"))
            for result in by_probe.values()
            if isinstance(result, Mapping)
        )
    return {key: int(counter.get(key, 0)) for key in OUTCOME_KEYS}


def _articulation_case_outcome_counts(
    *,
    asset_gate: Mapping[str, object],
    robot_package_result: Mapping[str, object],
    probe_results: Mapping[str, Mapping[str, object]],
) -> dict[str, int]:
    counter: Counter[str] = Counter({key: 0 for key in OUTCOME_KEYS})
    counter.update([str(asset_gate.get("outcome", "failure"))])
    counter.update([str(robot_package_result.get("outcome", "failure"))])
    counter.update(
        str(result.get("outcome", "failure"))
        for result in probe_results.values()
        if isinstance(result, Mapping)
    )
    return {key: int(counter.get(key, 0)) for key in OUTCOME_KEYS}


def _has_link_aware_robot_package(cases: list[dict[str, object]]) -> bool:
    for case in cases:
        robot_package_result = case.get("robot_package_result", {})
        probe_results = case.get("probe_results", {})
        link_audit = (
            probe_results.get("link_boundary_audit", {})
            if isinstance(probe_results, Mapping)
            else {}
        )
        if (
            isinstance(robot_package_result, Mapping)
            and isinstance(link_audit, Mapping)
            and robot_package_result.get("status") == "generated"
            and link_audit.get("status") == "smoke_passed"
        ):
            return True
    return False


def _has_generated_package_robot_task_check(cases: list[dict[str, object]]) -> bool:
    for case in cases:
        probe_results = case.get("probe_results", {})
        generated_probe = (
            probe_results.get("generated_package_robot_task_if_robot", {})
            if isinstance(probe_results, Mapping)
            else {}
        )
        metrics = (
            generated_probe.get("metrics", {})
            if isinstance(generated_probe, Mapping)
            else {}
        )
        if (
            isinstance(generated_probe, Mapping)
            and isinstance(metrics, Mapping)
            and generated_probe.get("status") == "smoke_passed"
            and metrics.get("generated_package_consumed") is True
        ):
            return True
    return False


def _aggregate_outcome_status(outcomes: Counter[str]) -> str:
    if outcomes.get("failure", 0) > 0:
        return "completed_with_recorded_failures"
    if outcomes.get("fallback", 0) > 0 or outcomes.get("dependency_gap", 0) > 0:
        return "partial"
    return "smoke_passed"


def _json_safe(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value
