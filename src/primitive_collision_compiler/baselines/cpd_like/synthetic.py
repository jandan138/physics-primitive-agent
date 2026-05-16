from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from primitive_collision_compiler.baselines.cpd_like.decompose import (
    CPDLikeDecompositionReport,
    MIN_NORMALIZATION_VOLUME,
    MERGE_SEARCH_COST_GUIDED_PAIRWISE,
    MERGE_SEARCH_TWO_STEP_LOOKAHEAD,
    decompose_mesh,
)
from primitive_collision_compiler.baselines.cpd_like.objective import (
    CPDLikeObjectiveOptions,
    build_cpd_like_objective_report,
)
from primitive_collision_compiler.baselines.cpd_like.package import package_from_cpd_like_report
from primitive_collision_compiler.baselines.cpd_like.primitives import (
    fit_primitive_candidates,
    rank_primitive_candidates_for_selection,
)
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
COST_GUIDED_LOOKAHEAD_MERGE_CLAIM_BOUNDARY = (
    "synthetic_two_step_lookahead_merge_not_collision_quality_or_merge_superiority"
)
COST_GUIDED_LOOKAHEAD_MERGE_EVIDENCE_LEVEL = (
    "offline_synthetic_two_step_lookahead_merge_smoke"
)
COST_GUIDED_LOOKAHEAD_MERGE_STATUS_SEMANTICS = (
    "synthetic_merge_search_lookahead_accounting_not_quality_success"
)
COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY = (
    "synthetic_cost_guided_lookahead_package_probe_not_default_or_newton_task"
)
COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_EVIDENCE_LEVEL = (
    "offline_synthetic_cost_guided_lookahead_package_probe_smoke"
)
COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_STATUS_SEMANTICS = (
    "opt_in_lookahead_package_probe_not_quality_success"
)
COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_CLAIM_BOUNDARY = (
    "synthetic_cost_guided_lookahead_newton_probe_not_quality_or_policy_ranking"
)
COST_GUIDED_LOOKAHEAD_NEWTON_CONTACT_CLAIM_BOUNDARY = (
    "synthetic_cost_guided_lookahead_contact_canary_not_quality"
)
COST_GUIDED_LOOKAHEAD_NEWTON_TASK_CLAIM_BOUNDARY = (
    "synthetic_cost_guided_lookahead_task_smoke_not_quality_or_policy_ranking"
)
COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_EVIDENCE_LEVEL = (
    "synthetic_cost_guided_lookahead_contact_gated_task_smoke"
)
COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_STATUS_SEMANTICS = (
    "synthetic_lookahead_newton_task_smoke_not_quality_or_policy_ranking"
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
NEAR_MISS_WORKBENCH_CLAIM_BOUNDARY = (
    "synthetic_near_miss_fixture_not_collision_quality_validation"
)
NEAR_MISS_WORKBENCH_EVIDENCE_LEVEL = "offline_synthetic_near_miss_fixture_smoke"
NEAR_MISS_WORKBENCH_STATUS_SEMANTICS = "near_miss_targets_reported_not_quality_success"
NEAR_MISS_RELATIVE_GAP_THRESHOLD = 0.25
CYLINDER_NEAR_MISS_FIT_ABLATION_CLAIM_BOUNDARY = (
    "synthetic_cylinder_fit_ablation_not_collision_quality_validation"
)
CYLINDER_NEAR_MISS_FIT_ABLATION_EVIDENCE_LEVEL = (
    "offline_synthetic_cylinder_near_miss_fit_ablation_smoke"
)
CYLINDER_NEAR_MISS_FIT_ABLATION_STATUS_SEMANTICS = (
    "fit_ablation_triage_not_quality_success"
)
CYLINDER_NEAR_MISS_SCORING_SENSITIVITY_CLAIM_BOUNDARY = (
    "synthetic_cylinder_scoring_sensitivity_not_collision_quality_validation"
)
CYLINDER_NEAR_MISS_SCORING_SENSITIVITY_EVIDENCE_LEVEL = (
    "offline_synthetic_cylinder_near_miss_scoring_sensitivity_smoke"
)
CYLINDER_NEAR_MISS_SCORING_SENSITIVITY_STATUS_SEMANTICS = (
    "scoring_sensitivity_triage_not_quality_success"
)
CYLINDER_NEAR_MISS_SCORING_POLICY_ABLATION_CLAIM_BOUNDARY = (
    "synthetic_cylinder_scoring_policy_ablation_not_default_or_collision_quality_validation"
)
CYLINDER_NEAR_MISS_SCORING_POLICY_ABLATION_EVIDENCE_LEVEL = (
    "offline_synthetic_cylinder_near_miss_scoring_policy_ablation_smoke"
)
CYLINDER_NEAR_MISS_SCORING_POLICY_ABLATION_STATUS_SEMANTICS = (
    "report_only_counterfactual_ablation_not_quality_success"
)
CYLINDER_NEAR_MISS_REPORT_ONLY_EXTENSION_MULTIPLIER = 0.88
CYLINDER_SCORING_POLICY_SELECTION_PROBE_CLAIM_BOUNDARY = (
    "synthetic_cylinder_scoring_policy_selection_probe_not_default_or_collision_quality_validation"
)
CYLINDER_SCORING_POLICY_SELECTION_PROBE_EVIDENCE_LEVEL = (
    "offline_synthetic_cylinder_scoring_policy_selection_probe_smoke"
)
CYLINDER_SCORING_POLICY_SELECTION_PROBE_STATUS_SEMANTICS = (
    "opt_in_selection_probe_not_quality_success"
)
CYLINDER_SCORING_POLICY_PACKAGE_PROBE_CLAIM_BOUNDARY = (
    "synthetic_cylinder_scoring_policy_package_probe_not_real_usd_or_newton_task"
)
CYLINDER_SCORING_POLICY_PACKAGE_PROBE_EVIDENCE_LEVEL = (
    "offline_synthetic_cylinder_scoring_policy_package_probe_smoke"
)
CYLINDER_SCORING_POLICY_PACKAGE_PROBE_STATUS_SEMANTICS = (
    "opt_in_synthetic_package_probe_not_quality_success"
)
CYLINDER_SCORING_POLICY_NEWTON_PROBE_CLAIM_BOUNDARY = (
    "synthetic_cylinder_scoring_policy_newton_probe_not_collision_quality_or_real_usd"
)
CYLINDER_SCORING_POLICY_NEWTON_CONTACT_CLAIM_BOUNDARY = (
    "synthetic_cylinder_scoring_policy_contact_canary_not_collision_quality"
)
CYLINDER_SCORING_POLICY_NEWTON_TASK_CLAIM_BOUNDARY = (
    "synthetic_cylinder_scoring_policy_task_smoke_not_collision_quality_or_safety"
)
CYLINDER_SCORING_POLICY_NEWTON_PROBE_EVIDENCE_LEVEL = (
    "synthetic_cylinder_scoring_policy_contact_gated_task_smoke"
)
CYLINDER_SCORING_POLICY_NEWTON_PROBE_STATUS_SEMANTICS = (
    "synthetic_newton_task_smoke_not_collision_quality"
)
CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_CLAIM_BOUNDARY = (
    "synthetic_controlled_merge_search_package_probe_not_default_or_newton_task"
)
CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_EVIDENCE_LEVEL = (
    "offline_synthetic_controlled_merge_search_package_probe_smoke"
)
CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_STATUS_SEMANTICS = (
    "opt_in_merge_search_package_probe_not_quality_success"
)
CONTROLLED_MERGE_SEARCH_NEWTON_PROBE_CLAIM_BOUNDARY = (
    "synthetic_controlled_merge_search_newton_probe_not_collision_quality_or_merge_superiority"
)
CONTROLLED_MERGE_SEARCH_NEWTON_CONTACT_CLAIM_BOUNDARY = (
    "synthetic_controlled_merge_search_contact_canary_not_collision_quality"
)
CONTROLLED_MERGE_SEARCH_NEWTON_TASK_CLAIM_BOUNDARY = (
    "synthetic_controlled_merge_search_task_smoke_not_collision_quality_or_merge_superiority"
)
CONTROLLED_MERGE_SEARCH_NEWTON_PROBE_EVIDENCE_LEVEL = (
    "synthetic_controlled_merge_search_contact_gated_task_smoke"
)
CONTROLLED_MERGE_SEARCH_NEWTON_PROBE_STATUS_SEMANTICS = (
    "synthetic_merge_search_newton_task_smoke_not_collision_quality"
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
NATIVE_SELECTION_POLICY = "support_aware_min_weighted_volume_surrogate_v1"
NATIVE_SELECTION_RULE = (
    "admissible_first_min_raw_weighted_primitive_volume_tie_break_by_subset_order"
)
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
FOUR_BLOCK_SLICE_REPORT_CLAIM_BOUNDARY = (
    "command_only_four_block_slice_report_not_new_runtime_or_quality_evidence"
)
FOUR_BLOCK_SLICE_REPORT_EVIDENCE_LEVEL = (
    "offline_four_block_slice_evidence_map_smoke"
)
FOUR_BLOCK_SLICE_REPORT_STATUS_SEMANTICS = (
    "record_map_status_not_experiment_success"
)
_FOUR_BLOCK_SUPPORTED_SLICE_IDS = ("cost_guided_lookahead",)
_FOUR_BLOCK_BLOCK_ORDER = (
    "primitive_fitting_selection",
    "merge_search",
    "offline_diagnostic_reports",
    "newton_task_comparison",
)
_FOUR_BLOCK_COST_GUIDED_LOOKAHEAD_RECORDS = {
    "primitive_fitting_selection": (
        "docs/records/2026-05-16-newton-cpd-workbench-four-block-status-audit.md",
    ),
    "merge_search": (
        "docs/records/2026-05-16-cost-guided-lookahead-merge.md",
    ),
    "offline_diagnostic_reports": (
        "docs/records/2026-05-16-cost-guided-lookahead-package-probe.md",
        "docs/records/2026-05-16-newton-cpd-workbench-four-block-status-audit.md",
    ),
    "newton_task_comparison": (
        "docs/records/2026-05-16-cost-guided-lookahead-newton-probe.md",
    ),
}


@dataclass(frozen=True)
class _PolicySpec:
    label: str
    component_merge: str
    merge_search_policy: str = "topology_then_virtual"
    excess_volume_threshold_fraction: float | None = None
    report_merge_trace: str = "summary"


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


def build_cpd_like_cost_guided_lookahead_merge_report() -> dict[str, object]:
    greedy = decompose_mesh(
        _lookahead_merge_trap_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy=MERGE_SEARCH_COST_GUIDED_PAIRWISE,
        report_merge_trace="steps",
    )
    lookahead = decompose_mesh(
        _lookahead_merge_trap_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy=MERGE_SEARCH_TWO_STEP_LOOKAHEAD,
        report_merge_trace="steps",
    )
    case_payload = _lookahead_merge_case_payload(greedy, lookahead)
    status = (
        "smoke_passed"
        if case_payload["decision"]["lookahead_decision_changed"]
        and case_payload["decision"]["projected_cost_improved"]
        else "partial"
    )
    return {
        "stage": "cpd_like_cost_guided_lookahead_merge_report",
        "status": status,
        "claim_boundary": COST_GUIDED_LOOKAHEAD_MERGE_CLAIM_BOUNDARY,
        "evidence_level": COST_GUIDED_LOOKAHEAD_MERGE_EVIDENCE_LEVEL,
        "status_semantics": COST_GUIDED_LOOKAHEAD_MERGE_STATUS_SEMANTICS,
        "default_pipeline_changed": False,
        "newton_task_comparison_triggered": False,
        "real_usd_rerun_triggered": False,
        "collision_quality_claim_supported": False,
        "merge_policy_superiority_claim_supported": False,
        "tiny_mesh_guard_applied": True,
        "cases": [case_payload],
    }


def build_cpd_like_cost_guided_lookahead_package_probe_report() -> dict[str, object]:
    greedy_decomposition, lookahead_decomposition = _lookahead_merge_decomposition_pair()
    greedy_package, lookahead_package = _lookahead_merge_package_pair(
        greedy_decomposition,
        lookahead_decomposition,
    )
    case_payload = _lookahead_package_probe_case_payload(
        greedy_decomposition=greedy_decomposition,
        lookahead_decomposition=lookahead_decomposition,
        greedy_package=greedy_package,
        lookahead_package=lookahead_package,
    )
    status = (
        "smoke_passed"
        if case_payload["expectation_status"] == "matched"
        else "partial"
    )
    return {
        "stage": "cpd_like_cost_guided_lookahead_package_probe",
        "status": status,
        "claim_boundary": COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY,
        "evidence_level": COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_EVIDENCE_LEVEL,
        "status_semantics": COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_STATUS_SEMANTICS,
        "synthetic_only": True,
        "command_only": True,
        "real_usd_scope": "not_run_synthetic_only",
        "default_pipeline_changed": False,
        "newton_task_comparison_triggered": False,
        "real_usd_rerun_triggered": False,
        "collision_quality_claim_supported": False,
        "merge_policy_superiority_claim_supported": False,
        "tiny_mesh_guard_applied": True,
        "cases": [case_payload],
    }


def build_cpd_like_cost_guided_lookahead_newton_probe_report(
    *,
    source_dir: str,
    device: str = "cpu",
    drop_settle_options: DropSettleOptions | None = None,
    sphere_rain_options: SphereRainOptions | None = None,
    claim_boundary: str = COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_CLAIM_BOUNDARY,
    contact_claim_boundary: str = COST_GUIDED_LOOKAHEAD_NEWTON_CONTACT_CLAIM_BOUNDARY,
    task_claim_boundary: str = COST_GUIDED_LOOKAHEAD_NEWTON_TASK_CLAIM_BOUNDARY,
    evidence_level: str = COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_EVIDENCE_LEVEL,
) -> dict[str, object]:
    drop_settle_options = drop_settle_options or DropSettleOptions()
    sphere_rain_options = sphere_rain_options or SphereRainOptions()
    case_payload = _lookahead_newton_probe_case_payload(
        source_dir=source_dir,
        device=device,
        drop_settle_options=drop_settle_options,
        sphere_rain_options=sphere_rain_options,
        contact_claim_boundary=contact_claim_boundary,
        task_claim_boundary=task_claim_boundary,
    )
    statuses = _lookahead_newton_probe_statuses(case_payload)
    decision = case_payload["decision"]
    expected_package_pair = bool(
        decision["package_pair_changed"] and decision["expected_package_faces"]
    )
    return {
        "stage": "cpd_like_cost_guided_lookahead_newton_probe",
        "status": _aggregate_probe_status(
            statuses,
            package_pair_changed=expected_package_pair,
        ),
        "status_semantics": COST_GUIDED_LOOKAHEAD_NEWTON_PROBE_STATUS_SEMANTICS,
        "claim_boundary": claim_boundary,
        "contact_claim_boundary": contact_claim_boundary,
        "task_claim_boundary": task_claim_boundary,
        "evidence_level": evidence_level,
        "source_dir": source_dir,
        "device": device,
        "real_usd_scope": "not_run_synthetic_only",
        "default_pipeline_changed": False,
        "newton_task_comparison_triggered": True,
        "real_usd_rerun_triggered": False,
        "cases": [case_payload],
    }


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _four_block_record_status(
    record_paths: tuple[str, ...],
) -> tuple[list[dict[str, object]], list[str]]:
    records = []
    missing = []
    root = _repo_root()
    for record_path in record_paths:
        exists = (root / record_path).exists()
        records.append({"path": record_path, "exists": exists})
        if not exists:
            missing.append(record_path)
    return records, missing


def _four_block_payload(
    *,
    block_id: str,
    status: str,
    summary: dict[str, object],
    record_paths: tuple[str, ...],
    command_surface: tuple[str, ...],
    claim_supported: tuple[str, ...],
    claim_not_supported: tuple[str, ...],
    recorded_task_smoke_available: bool | None = None,
) -> tuple[dict[str, object], list[str]]:
    evidence_records, missing_records = _four_block_record_status(record_paths)
    payload = {
        "block_id": block_id,
        "status": status,
        "summary": summary,
        "evidence_records": evidence_records,
        "command_surface": list(command_surface),
        "claim_boundary": FOUR_BLOCK_SLICE_REPORT_CLAIM_BOUNDARY,
        "claim_supported": list(claim_supported),
        "claim_not_supported": list(claim_not_supported),
    }
    if recorded_task_smoke_available is not None:
        payload["recorded_task_smoke_available"] = recorded_task_smoke_available
    return payload, missing_records


def _four_block_next_action() -> dict[str, object]:
    return {
        "next_recommended_slice": (
            "paper_aligned_objective_or_primitive_fitting_slice_before_real_asset_rerun"
        ),
        "blocked_real_asset_rerun": True,
        "requires_separate_real_package_change": True,
        "required_real_asset_gates": [
            "full_mapping",
            "contact_canary",
            "task_gate",
            "dated_record",
        ],
        "claim_boundary": FOUR_BLOCK_SLICE_REPORT_CLAIM_BOUNDARY,
    }


def _unsupported_four_block_slice_report(slice_id: str) -> dict[str, object]:
    return {
        "stage": "cpd_like_four_block_slice_report",
        "status": "partial",
        "claim_boundary": FOUR_BLOCK_SLICE_REPORT_CLAIM_BOUNDARY,
        "evidence_level": FOUR_BLOCK_SLICE_REPORT_EVIDENCE_LEVEL,
        "status_semantics": FOUR_BLOCK_SLICE_REPORT_STATUS_SEMANTICS,
        "slice_id": slice_id,
        "supported_slice_ids": list(_FOUR_BLOCK_SUPPORTED_SLICE_IDS),
        "fallback_reason": "unsupported_slice",
        "command_only": True,
        "synthetic_only": True,
        "real_usd_rerun_triggered": False,
        "newton_task_comparison_triggered": False,
        "report_newton_task_comparison_triggered": False,
        "blocks": [],
        "missing_evidence_records": [],
        "summary": {
            "four_block_record_map_complete": False,
            "record_map_only": True,
            "runtime_invoked_by_report": False,
            "real_asset_rerun_ready": False,
        },
        "next_action": _four_block_next_action(),
    }


def build_cpd_like_four_block_slice_report(
    slice_id: str = "cost_guided_lookahead",
) -> dict[str, object]:
    if slice_id != "cost_guided_lookahead":
        return _unsupported_four_block_slice_report(slice_id)

    records = _FOUR_BLOCK_COST_GUIDED_LOOKAHEAD_RECORDS
    block_specs = {
        "primitive_fitting_selection": {
            "status": "not_changed_for_this_slice",
            "summary": {
                "role": "records that this slice did not change primitive fitting",
                "changed_by_slice": False,
                "primitive_subset": "Newton-native policy unchanged for this slice",
            },
            "command_surface": (),
            "claim_supported": (
                "primitive fitting was not changed by the lookahead slice",
            ),
            "claim_not_supported": (
                "paper-faithful primitive fitting",
                "real-asset primitive quality",
            ),
            "recorded_task_smoke_available": False,
        },
        "merge_search": {
            "status": "complete",
            "summary": {
                "role": "recorded synthetic two-step lookahead merge-search evidence",
                "changed_by_slice": True,
                "default_pipeline_changed": False,
            },
            "command_surface": (
                "PYTHONPATH=src python -m primitive_collision_compiler.cli "
                "--run-cpd-like-cost-guided-lookahead-merge-report",
            ),
            "claim_supported": (
                "a controlled synthetic lookahead merge-search report exists",
            ),
            "claim_not_supported": (
                "merge-search superiority",
                "collision quality improvement",
            ),
            "recorded_task_smoke_available": False,
        },
        "offline_diagnostic_reports": {
            "status": "complete",
            "summary": {
                "role": "recorded package/mapping and workbench accounting evidence",
                "record_map_only": True,
                "raw_package_payload_embedded": False,
            },
            "command_surface": (
                "PYTHONPATH=src python -m primitive_collision_compiler.cli "
                "--run-cpd-like-cost-guided-lookahead-package-probe",
            ),
            "claim_supported": (
                "a synthetic package/mapping probe record exists",
            ),
            "claim_not_supported": (
                "new Newton task result",
                "real asset result",
            ),
            "recorded_task_smoke_available": False,
        },
        "newton_task_comparison": {
            "status": "complete",
            "summary": {
                "role": "recorded contact-gated Newton task-smoke evidence",
                "report_invokes_newton": False,
                "recorded_task_smoke_available": True,
            },
            "command_surface": (
                "NEWTON_SOURCE_DIR=/path/to/newton PYTHONPATH=src python -m "
                "primitive_collision_compiler.cli --config "
                "configs/experiments/cost_guided_lookahead_newton_probe.yaml "
                "--run-cpd-like-cost-guided-lookahead-newton-probe",
            ),
            "claim_supported": (
                "a recorded synthetic contact-gated Newton task-smoke exists",
            ),
            "claim_not_supported": (
                "new Newton task result from this report",
                "policy ranking",
                "collision quality improvement",
            ),
            "recorded_task_smoke_available": True,
        },
    }

    blocks = []
    missing_records = []
    for block_id in _FOUR_BLOCK_BLOCK_ORDER:
        spec = block_specs[block_id]
        block, missing = _four_block_payload(
            block_id=block_id,
            status=str(spec["status"]),
            summary=spec["summary"],
            record_paths=records.get(block_id, ()),
            command_surface=spec["command_surface"],
            claim_supported=spec["claim_supported"],
            claim_not_supported=spec["claim_not_supported"],
            recorded_task_smoke_available=bool(
                spec["recorded_task_smoke_available"]
            ),
        )
        if missing:
            block["status"] = "partial"
            block["claim_supported"] = []
            block["claim_not_supported"] = [
                *block["claim_not_supported"],
                "record-backed claim withheld until evidence records exist",
            ]
        blocks.append(block)
        missing_records.extend(missing)

    status = "smoke_passed" if not missing_records else "partial"
    return {
        "stage": "cpd_like_four_block_slice_report",
        "status": status,
        "claim_boundary": FOUR_BLOCK_SLICE_REPORT_CLAIM_BOUNDARY,
        "evidence_level": FOUR_BLOCK_SLICE_REPORT_EVIDENCE_LEVEL,
        "status_semantics": FOUR_BLOCK_SLICE_REPORT_STATUS_SEMANTICS,
        "slice_id": slice_id,
        "supported_slice_ids": list(_FOUR_BLOCK_SUPPORTED_SLICE_IDS),
        "command_only": True,
        "synthetic_only": True,
        "real_usd_rerun_triggered": False,
        "newton_task_comparison_triggered": False,
        "report_newton_task_comparison_triggered": False,
        "blocks": blocks,
        "missing_evidence_records": missing_records,
        "summary": {
            "four_block_record_map_complete": status == "smoke_passed",
            "record_map_only": True,
            "runtime_invoked_by_report": False,
            "real_asset_rerun_ready": False,
        },
        "next_action": _four_block_next_action(),
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


def build_cpd_like_near_miss_workbench_report(
    *,
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=NEAR_MISS_WORKBENCH_CLAIM_BOUNDARY,
        evidence_level=NEAR_MISS_WORKBENCH_EVIDENCE_LEVEL,
    )
    case_payloads = (
        _near_miss_case_payload(
            case_id="cylinder_near_miss_cluster",
            description=(
                "Supported cylinder-like synthetic cluster where box wins and cylinder is close "
                "under the current surrogate."
            ),
            mesh=_cylinder_near_miss_cluster_mesh(),
            selected_primitive="box",
            extension_primitive="cylinder",
        ),
    )
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_near_miss_fixture_workbench",
        "status": status,
        "status_semantics": NEAR_MISS_WORKBENCH_STATUS_SEMANTICS,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "near_miss_relative_gap_threshold": NEAR_MISS_RELATIVE_GAP_THRESHOLD,
        "cases": list(case_payloads),
    }


def build_cpd_like_cylinder_near_miss_fit_ablation_report(
    *,
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=CYLINDER_NEAR_MISS_FIT_ABLATION_CLAIM_BOUNDARY,
        evidence_level=CYLINDER_NEAR_MISS_FIT_ABLATION_EVIDENCE_LEVEL,
    )
    case_payloads = (
        _cylinder_near_miss_fit_ablation_case_payload(),
    )
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_cylinder_near_miss_fit_ablation",
        "status": status,
        "status_semantics": CYLINDER_NEAR_MISS_FIT_ABLATION_STATUS_SEMANTICS,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "cases": list(case_payloads),
    }


def build_cpd_like_cylinder_near_miss_scoring_sensitivity_report(
    *,
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=CYLINDER_NEAR_MISS_SCORING_SENSITIVITY_CLAIM_BOUNDARY,
        evidence_level=CYLINDER_NEAR_MISS_SCORING_SENSITIVITY_EVIDENCE_LEVEL,
    )
    case_payloads = (
        _cylinder_near_miss_scoring_sensitivity_case_payload(),
    )
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_cylinder_near_miss_scoring_sensitivity",
        "status": status,
        "status_semantics": CYLINDER_NEAR_MISS_SCORING_SENSITIVITY_STATUS_SEMANTICS,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "cases": list(case_payloads),
    }


def build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report(
    *,
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=CYLINDER_NEAR_MISS_SCORING_POLICY_ABLATION_CLAIM_BOUNDARY,
        evidence_level=CYLINDER_NEAR_MISS_SCORING_POLICY_ABLATION_EVIDENCE_LEVEL,
    )
    case_payloads = (
        _cylinder_scoring_policy_ablation_case_payload(
            case_id="cylinder_near_miss_cluster",
            description=(
                "Report-only counterfactual scoring-policy ablation for the synthetic "
                "cylinder near miss."
            ),
            mesh=_cylinder_near_miss_cluster_mesh(),
            case_role="expected_counterfactual_flip",
            expected_counterfactual_primitive="cylinder",
            expected_counterfactual_selection_changed=True,
        ),
        _cylinder_scoring_policy_ablation_case_payload(
            case_id="boxy_cuboid_guardrail",
            description=(
                "Report-only counterfactual scoring-policy guardrail for a clearly boxy cuboid."
            ),
            mesh=_boxy_cuboid_guardrail_mesh(),
            case_role="boxy_no_flip_guardrail",
            expected_counterfactual_primitive="box",
            expected_counterfactual_selection_changed=False,
        ),
    )
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_cylinder_near_miss_scoring_policy_ablation",
        "status": status,
        "status_semantics": CYLINDER_NEAR_MISS_SCORING_POLICY_ABLATION_STATUS_SEMANTICS,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "cases": list(case_payloads),
    }


def build_cpd_like_cylinder_scoring_policy_selection_probe_report(
    *,
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=CYLINDER_SCORING_POLICY_SELECTION_PROBE_CLAIM_BOUNDARY,
        evidence_level=CYLINDER_SCORING_POLICY_SELECTION_PROBE_EVIDENCE_LEVEL,
    )
    case_payloads = (
        _cylinder_scoring_policy_selection_probe_case_payload(
            case_id="cylinder_near_miss_cluster",
            description=(
                "Opt-in cylinder scoring-policy selection probe for the synthetic "
                "cylinder near miss."
            ),
            mesh=_cylinder_near_miss_cluster_mesh(),
            case_role="expected_opt_in_flip",
            expected_opt_in_primitive="cylinder",
            expected_opt_in_selection_changed=True,
        ),
        _cylinder_scoring_policy_selection_probe_case_payload(
            case_id="boxy_cuboid_guardrail",
            description=(
                "Opt-in cylinder scoring-policy selection guardrail for a clearly boxy cuboid."
            ),
            mesh=_boxy_cuboid_guardrail_mesh(),
            case_role="boxy_no_flip_guardrail",
            expected_opt_in_primitive="box",
            expected_opt_in_selection_changed=False,
        ),
    )
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_cylinder_scoring_policy_selection_probe",
        "status": status,
        "status_semantics": CYLINDER_SCORING_POLICY_SELECTION_PROBE_STATUS_SEMANTICS,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "cases": list(case_payloads),
    }


def build_cpd_like_cylinder_scoring_policy_package_probe_report(
    *,
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=CYLINDER_SCORING_POLICY_PACKAGE_PROBE_CLAIM_BOUNDARY,
        evidence_level=CYLINDER_SCORING_POLICY_PACKAGE_PROBE_EVIDENCE_LEVEL,
    )
    case_payloads = (
        _cylinder_scoring_policy_package_probe_case_payload(
            case_id="cylinder_near_miss_cluster",
            description=(
                "Explicit opt-in package probe for the synthetic cylinder near miss."
            ),
            mesh=_cylinder_near_miss_cluster_mesh(),
            case_role="expected_opt_in_package_change",
            expected_opt_in_primitive="cylinder",
            expected_opt_in_package_changed=True,
            options=options,
        ),
        _cylinder_scoring_policy_package_probe_case_payload(
            case_id="boxy_cuboid_guardrail",
            description=(
                "Explicit opt-in package guardrail for a clearly boxy cuboid."
            ),
            mesh=_boxy_cuboid_guardrail_mesh(),
            case_role="boxy_no_package_change_guardrail",
            expected_opt_in_primitive="box",
            expected_opt_in_package_changed=False,
            options=options,
        ),
    )
    status = (
        "smoke_passed"
        if all(case["expectation_status"] == "matched" for case in case_payloads)
        else "partial"
    )
    return {
        "stage": "cpd_like_cylinder_scoring_policy_package_probe",
        "status": status,
        "status_semantics": CYLINDER_SCORING_POLICY_PACKAGE_PROBE_STATUS_SEMANTICS,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "selection_policy_applied_to_default_pipeline": False,
        "default_pipeline_changed": any(
            bool(case["default_behavior_changed"]) for case in case_payloads
        ),
        "cases": list(case_payloads),
    }


def build_cpd_like_controlled_merge_search_package_probe_report(
    *,
    objective_options: CPDLikeObjectiveOptions | None = None,
) -> dict[str, object]:
    options = objective_options or CPDLikeObjectiveOptions(
        claim_boundary=CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_CLAIM_BOUNDARY,
        evidence_level=CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_EVIDENCE_LEVEL,
    )
    case_payload = _controlled_merge_search_package_probe_case_payload(
        case_id="cost_guided_pair_choice",
        description=(
            "Explicit opt-in package probe for the controlled cost-guided merge-search "
            "fixture."
        ),
        mesh=_cost_guided_pair_choice_mesh(),
        options=options,
    )
    status = (
        "smoke_passed"
        if case_payload["expectation_status"] == "matched"
        else "partial"
    )
    return {
        "stage": "cpd_like_controlled_merge_search_package_probe",
        "status": status,
        "status_semantics": CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_STATUS_SEMANTICS,
        "claim_boundary": options.claim_boundary,
        "evidence_level": options.evidence_level,
        "objective_version": options.objective_version,
        "synthetic_only": True,
        "command_only": True,
        "real_usd_scope": "not_run_synthetic_only",
        "merge_search_policy_applied_to_default_pipeline": False,
        "default_pipeline_changed": False,
        "newton_task_comparison_triggered": False,
        "cases": [case_payload],
    }


def build_cpd_like_cylinder_scoring_policy_newton_probe_report(
    *,
    source_dir: str,
    device: str = "cpu",
    drop_settle_options: DropSettleOptions | None = None,
    sphere_rain_options: SphereRainOptions | None = None,
    claim_boundary: str = CYLINDER_SCORING_POLICY_NEWTON_PROBE_CLAIM_BOUNDARY,
    contact_claim_boundary: str = CYLINDER_SCORING_POLICY_NEWTON_CONTACT_CLAIM_BOUNDARY,
    task_claim_boundary: str = CYLINDER_SCORING_POLICY_NEWTON_TASK_CLAIM_BOUNDARY,
    evidence_level: str = CYLINDER_SCORING_POLICY_NEWTON_PROBE_EVIDENCE_LEVEL,
) -> dict[str, object]:
    drop_settle_options = drop_settle_options or DropSettleOptions()
    sphere_rain_options = sphere_rain_options or SphereRainOptions()
    case_payload = _cylinder_scoring_policy_newton_probe_case_payload(
        source_dir=source_dir,
        device=device,
        drop_settle_options=drop_settle_options,
        sphere_rain_options=sphere_rain_options,
        contact_claim_boundary=contact_claim_boundary,
        task_claim_boundary=task_claim_boundary,
    )
    statuses = _newton_probe_statuses(case_payload)
    decision = case_payload["decision"]
    return {
        "stage": "cpd_like_cylinder_scoring_policy_newton_probe",
        "status": _aggregate_probe_status(
            statuses,
            package_pair_changed=bool(decision["package_pair_changed"]),
        ),
        "status_semantics": CYLINDER_SCORING_POLICY_NEWTON_PROBE_STATUS_SEMANTICS,
        "claim_boundary": claim_boundary,
        "contact_claim_boundary": contact_claim_boundary,
        "task_claim_boundary": task_claim_boundary,
        "evidence_level": evidence_level,
        "source_dir": source_dir,
        "device": device,
        "real_usd_scope": "not_run_synthetic_only",
        "default_pipeline_changed": False,
        "cases": [case_payload],
    }


def build_cpd_like_controlled_merge_search_newton_probe_report(
    *,
    source_dir: str,
    device: str = "cpu",
    drop_settle_options: DropSettleOptions | None = None,
    sphere_rain_options: SphereRainOptions | None = None,
    claim_boundary: str = CONTROLLED_MERGE_SEARCH_NEWTON_PROBE_CLAIM_BOUNDARY,
    contact_claim_boundary: str = CONTROLLED_MERGE_SEARCH_NEWTON_CONTACT_CLAIM_BOUNDARY,
    task_claim_boundary: str = CONTROLLED_MERGE_SEARCH_NEWTON_TASK_CLAIM_BOUNDARY,
    evidence_level: str = CONTROLLED_MERGE_SEARCH_NEWTON_PROBE_EVIDENCE_LEVEL,
) -> dict[str, object]:
    drop_settle_options = drop_settle_options or DropSettleOptions()
    sphere_rain_options = sphere_rain_options or SphereRainOptions()
    case_payload = _controlled_merge_search_newton_probe_case_payload(
        source_dir=source_dir,
        device=device,
        drop_settle_options=drop_settle_options,
        sphere_rain_options=sphere_rain_options,
        contact_claim_boundary=contact_claim_boundary,
        task_claim_boundary=task_claim_boundary,
    )
    statuses = _newton_probe_statuses(case_payload)
    decision = case_payload["decision"]
    return {
        "stage": "cpd_like_controlled_merge_search_newton_probe",
        "status": _aggregate_probe_status(
            statuses,
            package_pair_changed=bool(decision["package_pair_changed"]),
        ),
        "status_semantics": CONTROLLED_MERGE_SEARCH_NEWTON_PROBE_STATUS_SEMANTICS,
        "claim_boundary": claim_boundary,
        "contact_claim_boundary": contact_claim_boundary,
        "task_claim_boundary": task_claim_boundary,
        "evidence_level": evidence_level,
        "source_dir": source_dir,
        "device": device,
        "real_usd_scope": "not_run_synthetic_only",
        "default_pipeline_changed": False,
        "newton_task_comparison_triggered": True,
        "real_usd_rerun_triggered": False,
        "cases": [case_payload],
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
                    report_merge_trace="steps",
                ),
                _PolicySpec(
                    label="cost_guided_pairwise",
                    component_merge="virtual_pairwise",
                    merge_search_policy="cost_guided_pairwise",
                    report_merge_trace="steps",
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


def _near_miss_case_payload(
    *,
    case_id: str,
    description: str,
    mesh: TriangleMesh,
    selected_primitive: str,
    extension_primitive: str,
) -> dict[str, object]:
    face_ids = frozenset(range(mesh.face_count))
    ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        fit_primitive_candidates(mesh, face_ids, (selected_primitive, extension_primitive)),
    )
    candidate_rows = [
        {
            "primitive_type": row.primitive_type,
            "rank": rank,
            "raw_cost_rank": row.raw_cost_rank,
            "weighted_volume": row.candidate.weighted_volume,
            "selection_admissible": row.selection_admissible,
            "selection_admissibility_reason": row.selection_admissibility_reason,
            "selection_support": row.support,
        }
        for rank, row in enumerate(ranked, start=1)
    ]
    selected_row = candidate_rows[0]
    extension_row = next(
        row for row in candidate_rows if row["primitive_type"] == extension_primitive
    )
    selected_cost = float(selected_row["weighted_volume"])
    extension_cost = float(extension_row["weighted_volume"])
    relative_gap = float(
        (extension_cost - selected_cost) / max(selected_cost, MIN_NORMALIZATION_VOLUME)
    )
    matched = (
        selected_row["primitive_type"] == selected_primitive
        and extension_row["primitive_type"] == extension_primitive
        and bool(extension_row["selection_admissible"])
        and int(extension_row["raw_cost_rank"]) == 2
        and 0.0 < relative_gap <= NEAR_MISS_RELATIVE_GAP_THRESHOLD
    )
    return {
        "case_id": case_id,
        "description": description,
        "scope": "single_fixture_primitive_ranking",
        "primitive_subset": [selected_primitive, extension_primitive],
        "expectation_status": "matched" if matched else "mismatched",
        "selected_primitive_type": selected_row["primitive_type"],
        "best_extension_candidate": extension_row,
        "candidate_ranking": candidate_rows,
        "near_miss": {
            "selected_primitive_type": selected_row["primitive_type"],
            "best_extension_primitive_type": extension_row["primitive_type"],
            "relative_extension_gap": relative_gap,
            "near_miss_relative_gap_threshold": NEAR_MISS_RELATIVE_GAP_THRESHOLD,
        },
        "fixture_geometry": {
            "face_count": mesh.face_count,
            "unique_point_count": int(mesh.points.shape[0]),
        },
        "recommended_next_slice": {
            "target_type": "primitive_fitting_or_merge_search_near_miss",
            "extension_kind": extension_primitive,
            "suggested_synthetic_fixture": case_id,
            "claim_boundary": "diagnostic_triage_not_collision_quality",
        },
    }


def _cylinder_near_miss_fit_ablation_case_payload() -> dict[str, object]:
    case_id = "cylinder_near_miss_cluster"
    selected_primitive = "box"
    extension_primitive = "cylinder"
    mesh = _cylinder_near_miss_cluster_mesh()
    face_ids = frozenset(range(mesh.face_count))
    ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        fit_primitive_candidates(mesh, face_ids, (selected_primitive, extension_primitive)),
    )
    candidate_rows = [
        {
            "primitive_type": row.primitive_type,
            "rank": rank,
            "raw_cost_rank": row.raw_cost_rank,
            "weighted_volume": row.candidate.weighted_volume,
            "selection_admissible": row.selection_admissible,
            "selection_admissibility_reason": row.selection_admissibility_reason,
            "selection_support": row.support,
            "contains_assigned_points": row.candidate.contains_assigned_points,
            "dimensions": row.candidate.dimensions,
        }
        for rank, row in enumerate(ranked, start=1)
    ]
    selected_row = candidate_rows[0]
    cylinder_selection = next(row for row in ranked if row.primitive_type == extension_primitive)
    cylinder = cylinder_selection.candidate
    selected_cost = float(selected_row["weighted_volume"])
    lower_bound = _cylinder_pairwise_radial_lower_bound(mesh, cylinder)
    current_radius = float(cylinder.dimensions["radius"])
    half_height = float(cylinder.dimensions["half_height"])
    lower_bound_volume = float(np.pi * lower_bound**2 * (half_height * 2.0))
    current_volume = float(cylinder.weighted_volume)
    relative_gap_after_lower_bound = float(
        (lower_bound_volume - selected_cost) / max(selected_cost, MIN_NORMALIZATION_VOLUME)
    )
    radius_matches_lower_bound = bool(
        np.isclose(current_radius, lower_bound, rtol=0.0, atol=1e-12)
    )
    lower_bound_beats_selected = bool(lower_bound_volume < selected_cost)
    default_behavior_changed = selected_row["primitive_type"] != selected_primitive
    newton_task_comparison_gate = (
        "not_triggered_ablation_mismatched_default_behavior_changed"
        if default_behavior_changed
        else "not_triggered_default_package_unchanged"
    )
    matched = (
        not default_behavior_changed
        and cylinder_selection.raw_cost_rank == 2
        and cylinder_selection.selection_admissible
        and cylinder.contains_assigned_points
        and radius_matches_lower_bound
        and not lower_bound_beats_selected
        and relative_gap_after_lower_bound > 0.0
    )
    return {
        "case_id": case_id,
        "description": (
            "Diagnostic lower-bound ablation for the supported synthetic cylinder near miss."
        ),
        "scope": "single_fixture_radial_fit_ablation",
        "expectation_status": "matched" if matched else "mismatched",
        "default_behavior_changed": default_behavior_changed,
        "selected_primitive_type": selected_row["primitive_type"],
        "extension_primitive_type": extension_primitive,
        "candidate_ranking": candidate_rows,
        "ablation": {
            "kind": "pairwise_radial_lower_bound",
            "axis_index": int(cylinder.dimensions["axis_index"]),
            "current_cylinder_radius": current_radius,
            "pairwise_radius_lower_bound": lower_bound,
            "radius_matches_lower_bound": radius_matches_lower_bound,
            "current_cylinder_half_height": half_height,
            "current_cylinder_weighted_volume": current_volume,
            "lower_bound_cylinder_weighted_volume": lower_bound_volume,
            "selected_weighted_volume": selected_cost,
            "relative_gap_after_lower_bound": relative_gap_after_lower_bound,
            "lower_bound_volume_beats_selected": lower_bound_beats_selected,
            "current_cylinder_contains_assigned_points": cylinder.contains_assigned_points,
        },
        "decision": {
            "diagnostic_conclusion": (
                "radial_center_refinement_cannot_flip_selection_under_containment"
            ),
            "recommended_next_component": (
                "scoring_or_merge_search_not_radial_center_refinement"
            ),
            "newton_task_comparison_triggered": False,
            "newton_task_comparison_gate": newton_task_comparison_gate,
            "claim_boundary": "diagnostic_triage_not_collision_quality",
        },
    }


def _cylinder_pairwise_radial_lower_bound(
    mesh: TriangleMesh,
    cylinder,
) -> float:
    axis_index = int(cylinder.dimensions["axis_index"])
    axis = np.asarray(cylinder.axes[axis_index], dtype=np.float64)
    axis = axis / max(float(np.linalg.norm(axis)), MIN_NORMALIZATION_VOLUME)
    radial_points = mesh.points - np.outer(mesh.points @ axis, axis)
    max_distance = 0.0
    for left_index in range(radial_points.shape[0]):
        deltas = radial_points[left_index + 1 :] - radial_points[left_index]
        if deltas.size == 0:
            continue
        max_distance = max(
            max_distance,
            float(np.linalg.norm(deltas, axis=1).max(initial=0.0)),
        )
    return max(max_distance * 0.5, MIN_NORMALIZATION_VOLUME)


def _cylinder_near_miss_scoring_sensitivity_case_payload() -> dict[str, object]:
    case_id = "cylinder_near_miss_cluster"
    selected_primitive = "box"
    extension_primitive = "cylinder"
    mesh = _cylinder_near_miss_cluster_mesh()
    face_ids = frozenset(range(mesh.face_count))
    ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        fit_primitive_candidates(mesh, face_ids, (selected_primitive, extension_primitive)),
    )
    candidate_rows = [
        {
            "primitive_type": row.primitive_type,
            "rank": rank,
            "raw_cost_rank": row.raw_cost_rank,
            "weighted_volume": row.candidate.weighted_volume,
            "selection_admissible": row.selection_admissible,
            "selection_admissibility_reason": row.selection_admissibility_reason,
            "selection_support": row.support,
            "contains_assigned_points": row.candidate.contains_assigned_points,
            "dimensions": row.candidate.dimensions,
        }
        for rank, row in enumerate(ranked, start=1)
    ]
    selected_row = candidate_rows[0]
    extension_row = next(
        row for row in candidate_rows if row["primitive_type"] == extension_primitive
    )
    selected_cost = float(selected_row["weighted_volume"])
    extension_cost = float(extension_row["weighted_volume"])
    absolute_gap = float(extension_cost - selected_cost)
    normalizer = max(selected_cost, MIN_NORMALIZATION_VOLUME)
    extension_normalizer = max(extension_cost, MIN_NORMALIZATION_VOLUME)
    relative_gap = float(absolute_gap / normalizer)
    extension_multiplier_to_tie = float(selected_cost / extension_normalizer)
    extension_reduction_fraction = float(1.0 - extension_multiplier_to_tie)
    selection_flips_under_default = bool(extension_cost < selected_cost)
    default_behavior_changed = selected_row["primitive_type"] != selected_primitive
    newton_task_comparison_gate = (
        "not_triggered_sensitivity_mismatched_default_behavior_changed"
        if default_behavior_changed
        else "not_triggered_default_package_unchanged"
    )
    matched = (
        not default_behavior_changed
        and extension_row["raw_cost_rank"] == 2
        and bool(extension_row["selection_admissible"])
        and absolute_gap > 0.0
        and 0.0 < extension_multiplier_to_tie < 1.0
        and not selection_flips_under_default
    )
    return {
        "case_id": case_id,
        "description": (
            "Offline counterfactual scoring sensitivity for the synthetic cylinder near miss."
        ),
        "scope": "single_fixture_scoring_sensitivity",
        "expectation_status": "matched" if matched else "mismatched",
        "default_behavior_changed": default_behavior_changed,
        "selection_policy_changed": False,
        "selected_primitive_type": selected_row["primitive_type"],
        "extension_primitive_type": extension_primitive,
        "extension_candidate": extension_row,
        "candidate_ranking": candidate_rows,
        "scoring_sensitivity": {
            "selected_weighted_volume": selected_cost,
            "extension_weighted_volume": extension_cost,
            "absolute_cost_gap": absolute_gap,
            "relative_gap_selected_denominator": relative_gap,
            "selected_score_multiplier_for_extension_to_tie": float(
                extension_cost / normalizer
            ),
            "extension_score_multiplier_to_tie": extension_multiplier_to_tie,
            "extension_score_multiplier_to_beat_condition": (
                "multiplier_below_extension_score_multiplier_to_tie"
            ),
            "extension_cost_reduction_fraction_to_tie": extension_reduction_fraction,
            "extension_cost_reduction_absolute_to_tie": absolute_gap,
            "current_extension_multiplier": 1.0,
            "current_raw_cost_flips_under_default_multiplier": selection_flips_under_default,
        },
        "decision": {
            "diagnostic_conclusion": "scoring_change_required_to_flip_current_surrogate",
            "recommended_next_component": "scoring_policy_or_merge_search_sensitivity",
            "default_selection_changed": default_behavior_changed,
            "newton_task_comparison_triggered": False,
            "newton_task_comparison_gate": newton_task_comparison_gate,
            "claim_boundary": "diagnostic_triage_not_collision_quality",
        },
    }


def _cylinder_scoring_policy_ablation_case_payload(
    *,
    case_id: str,
    description: str,
    mesh: TriangleMesh,
    case_role: str,
    expected_counterfactual_primitive: str,
    expected_counterfactual_selection_changed: bool,
) -> dict[str, object]:
    selected_primitive = "box"
    extension_primitive = "cylinder"
    face_ids = frozenset(range(mesh.face_count))
    ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        fit_primitive_candidates(mesh, face_ids, (selected_primitive, extension_primitive)),
    )
    default_rows = [
        {
            "primitive_type": row.primitive_type,
            "rank": rank,
            "raw_cost_rank": row.raw_cost_rank,
            "weighted_volume": row.candidate.weighted_volume,
            "selection_admissible": row.selection_admissible,
            "selection_admissibility_reason": row.selection_admissibility_reason,
            "selection_support": row.support,
            "contains_assigned_points": row.candidate.contains_assigned_points,
            "dimensions": row.candidate.dimensions,
        }
        for rank, row in enumerate(ranked, start=1)
    ]
    default_selected = default_rows[0]
    extension_row = next(
        row for row in default_rows if row["primitive_type"] == extension_primitive
    )
    selected_cost = float(default_selected["weighted_volume"])
    extension_cost = float(extension_row["weighted_volume"])
    tie_multiplier = float(extension_cost and selected_cost / extension_cost)
    fixed_multiplier = CYLINDER_NEAR_MISS_REPORT_ONLY_EXTENSION_MULTIPLIER
    counterfactual_rows = _counterfactual_scoring_rows(
        default_rows,
        extension_primitive=extension_primitive,
        extension_multiplier=fixed_multiplier,
    )
    counterfactual_selected = counterfactual_rows[0]
    default_behavior_changed = default_selected["primitive_type"] != selected_primitive
    counterfactual_selection_changed = (
        counterfactual_selected["primitive_type"] != default_selected["primitive_type"]
    )
    multiplier_flips = fixed_multiplier < tie_multiplier
    newton_task_comparison_gate = (
        "not_triggered_ablation_mismatched_default_behavior_changed"
        if default_behavior_changed
        else "not_triggered_report_only_ablation"
    )
    diagnostic_conclusion = (
        "report_only_counterfactual_ablation_mismatched_default_behavior_changed"
        if default_behavior_changed
        else (
            "report_only_counterfactual_multiplier_flips_synthetic_near_miss"
            if multiplier_flips and counterfactual_selection_changed
            else "report_only_counterfactual_multiplier_preserves_boxy_guardrail"
        )
    )
    matched = (
        not default_behavior_changed
        and extension_row["raw_cost_rank"] == 2
        and bool(extension_row["selection_admissible"])
        and default_selected["primitive_type"] == selected_primitive
        and counterfactual_selected["primitive_type"] == expected_counterfactual_primitive
        and counterfactual_selection_changed == expected_counterfactual_selection_changed
    )
    return {
        "case_id": case_id,
        "description": description,
        "case_role": case_role,
        "scope": "single_fixture_report_only_scoring_policy_ablation",
        "expectation_status": "matched" if matched else "mismatched",
        "selection_policy_applied_to_default_pipeline": False,
        "counterfactual_policy_scope": "report_only_synthetic_fixed_multiplier",
        "default_behavior_changed": default_behavior_changed,
        "default_selection_changed": default_behavior_changed,
        "counterfactual_selection_changed": counterfactual_selection_changed,
        "default_selected_primitive_type": default_selected["primitive_type"],
        "counterfactual_selected_primitive_type": counterfactual_selected["primitive_type"],
        "default_candidate_ranking": default_rows,
        "counterfactual_candidate_ranking": counterfactual_rows,
        "counterfactual_ablation": {
            "report_only_extension_primitive": extension_primitive,
            "report_only_extension_multiplier": fixed_multiplier,
            "extension_score_multiplier_to_tie": tie_multiplier,
            "selected_weighted_volume": selected_cost,
            "extension_weighted_volume": extension_cost,
            "extension_counterfactual_score": float(extension_cost * fixed_multiplier),
            "fixed_multiplier_below_tie_threshold": multiplier_flips,
            "default_package_changed": False,
        },
        "decision": {
            "diagnostic_conclusion": diagnostic_conclusion,
            "recommended_next_component": "scoring_policy_design_or_merge_search_diagnostic",
            "default_selection_changed": default_behavior_changed,
            "newton_task_comparison_triggered": False,
            "newton_task_comparison_gate": newton_task_comparison_gate,
            "claim_boundary": "diagnostic_triage_not_collision_quality",
        },
    }


def _counterfactual_scoring_rows(
    default_rows: list[dict[str, object]],
    *,
    extension_primitive: str,
    extension_multiplier: float,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in default_rows:
        multiplier = (
            extension_multiplier
            if row["primitive_type"] == extension_primitive
            else 1.0
        )
        default_rank = int(row["rank"])
        counterfactual_row = {key: value for key, value in row.items() if key != "rank"}
        rows.append(
            {
                **counterfactual_row,
                "default_rank": default_rank,
                "report_only_multiplier": multiplier,
                "counterfactual_score": float(float(row["weighted_volume"]) * multiplier),
            }
        )
    ranked = sorted(
        rows,
        key=lambda row: (
            not bool(row["selection_admissible"]),
            float(row["counterfactual_score"]),
            int(row["default_rank"]),
        ),
    )
    return [
        {
            **row,
            "counterfactual_rank": rank,
        }
        for rank, row in enumerate(ranked, start=1)
    ]


def _cylinder_scoring_policy_selection_probe_case_payload(
    *,
    case_id: str,
    description: str,
    mesh: TriangleMesh,
    case_role: str,
    expected_opt_in_primitive: str,
    expected_opt_in_selection_changed: bool,
) -> dict[str, object]:
    selected_primitive = "box"
    extension_primitive = "cylinder"
    face_ids = frozenset(range(mesh.face_count))
    candidates = fit_primitive_candidates(
        mesh,
        face_ids,
        (selected_primitive, extension_primitive),
    )
    default_ranked = rank_primitive_candidates_for_selection(mesh, face_ids, candidates)
    opt_in_ranked = rank_primitive_candidates_for_selection(
        mesh,
        face_ids,
        candidates,
        primitive_score_multipliers={
            extension_primitive: CYLINDER_NEAR_MISS_REPORT_ONLY_EXTENSION_MULTIPLIER
        },
    )
    default_rows = [
        _selection_probe_row(row, rank_key="rank", rank=rank)
        for rank, row in enumerate(default_ranked, start=1)
    ]
    default_rank_by_type = {
        str(row["primitive_type"]): int(row["rank"]) for row in default_rows
    }
    opt_in_rows = [
        {
            **_selection_probe_row(row, rank_key="opt_in_rank", rank=rank),
            "default_rank": default_rank_by_type[str(row.primitive_type)],
        }
        for rank, row in enumerate(opt_in_ranked, start=1)
    ]
    default_selected = default_rows[0]
    opt_in_selected = opt_in_rows[0]
    default_behavior_changed = default_selected["primitive_type"] != selected_primitive
    opt_in_selection_changed = (
        opt_in_selected["primitive_type"] != default_selected["primitive_type"]
    )
    matched = (
        not default_behavior_changed
        and default_selected["primitive_type"] == selected_primitive
        and opt_in_selected["primitive_type"] == expected_opt_in_primitive
        and opt_in_selection_changed == expected_opt_in_selection_changed
    )
    return {
        "case_id": case_id,
        "description": description,
        "case_role": case_role,
        "scope": "single_fixture_opt_in_scoring_policy_selection_probe",
        "expectation_status": "matched" if matched else "mismatched",
        "selection_policy_applied_to_default_pipeline": False,
        "opt_in_policy_applied_to_probe": True,
        "opt_in_policy_scope": "synthetic_candidate_selection_probe_only",
        "primitive_score_multipliers": {
            extension_primitive: CYLINDER_NEAR_MISS_REPORT_ONLY_EXTENSION_MULTIPLIER
        },
        "default_behavior_changed": default_behavior_changed,
        "default_selected_primitive_type": default_selected["primitive_type"],
        "opt_in_selected_primitive_type": opt_in_selected["primitive_type"],
        "opt_in_selection_changed": opt_in_selection_changed,
        "default_candidate_ranking": default_rows,
        "opt_in_candidate_ranking": opt_in_rows,
        "decision": {
            "diagnostic_conclusion": (
                "opt_in_scoring_policy_flips_synthetic_near_miss"
                if opt_in_selection_changed
                else "opt_in_scoring_policy_preserves_boxy_guardrail"
            ),
            "default_package_changed": False,
            "newton_task_comparison_triggered": False,
            "newton_task_comparison_gate": "not_triggered_default_package_unchanged",
            "recommended_next_component": "merge_search_diagnostic_or_opt_in_package_probe",
            "claim_boundary": "diagnostic_triage_not_collision_quality",
        },
    }


def _cylinder_scoring_policy_package_probe_case_payload(
    *,
    case_id: str,
    description: str,
    mesh: TriangleMesh,
    case_role: str,
    expected_opt_in_primitive: str,
    expected_opt_in_package_changed: bool,
    options: CPDLikeObjectiveOptions,
) -> dict[str, object]:
    default_package, opt_in_package = _cylinder_scoring_policy_package_pair(
        case_id=case_id,
        mesh=mesh,
        options=options,
    )
    default_selected = default_package.primitives[0].kind
    opt_in_selected = opt_in_package.primitives[0].kind
    default_behavior_changed = default_selected != "box"
    opt_in_package_changed = opt_in_selected != default_selected
    opt_in_mapping = _package_mapping_summary(opt_in_package)
    matched = (
        not default_behavior_changed
        and opt_in_selected == expected_opt_in_primitive
        and opt_in_package_changed == expected_opt_in_package_changed
        and bool(opt_in_mapping["fully_mapped"])
    )
    return {
        "case_id": case_id,
        "description": description,
        "case_role": case_role,
        "scope": "single_fixture_opt_in_scoring_policy_package_probe",
        "expectation_status": "matched" if matched else "mismatched",
        "selection_policy_applied_to_default_pipeline": False,
        "opt_in_policy_applied_to_package_probe": True,
        "opt_in_policy_scope": "synthetic_decomposition_and_package_probe_only",
        "primitive_score_multipliers": {
            "cylinder": CYLINDER_NEAR_MISS_REPORT_ONLY_EXTENSION_MULTIPLIER
        },
        "default_behavior_changed": default_behavior_changed,
        "default_selected_primitive_type": default_selected,
        "opt_in_selected_primitive_type": opt_in_selected,
        "opt_in_package_changed": opt_in_package_changed,
        "default_package": _package_probe_package_summary(default_package),
        "opt_in_package": _package_probe_package_summary(opt_in_package),
        "default_package_mapping": _package_mapping_summary(default_package),
        "opt_in_package_mapping": opt_in_mapping,
        "decision": {
            "diagnostic_conclusion": (
                "opt_in_scoring_policy_changes_synthetic_package"
                if opt_in_package_changed
                else "opt_in_scoring_policy_preserves_boxy_package_guardrail"
            ),
            "default_package_changed": False,
            "newton_mapping_summary_recorded": True,
            "newton_task_comparison_triggered": False,
            "newton_task_comparison_gate": "not_triggered_synthetic_package_probe_only",
            "recommended_next_component": "opt_in_newton_task_probe_or_merge_search_change",
            "claim_boundary": "diagnostic_triage_not_collision_quality",
        },
    }


def _cylinder_scoring_policy_newton_probe_case_payload(
    *,
    source_dir: str,
    device: str,
    drop_settle_options: DropSettleOptions,
    sphere_rain_options: SphereRainOptions,
    contact_claim_boundary: str,
    task_claim_boundary: str,
) -> dict[str, object]:
    options = CPDLikeObjectiveOptions(
        claim_boundary=CYLINDER_SCORING_POLICY_PACKAGE_PROBE_CLAIM_BOUNDARY,
        evidence_level=CYLINDER_SCORING_POLICY_PACKAGE_PROBE_EVIDENCE_LEVEL,
    )
    default_package, opt_in_package = _cylinder_scoring_policy_package_pair(
        case_id="cylinder_near_miss_cluster",
        mesh=_cylinder_near_miss_cluster_mesh(),
        options=options,
    )
    default_contact, default_tasks = _synthetic_task_probe_payloads(
        default_package,
        source_dir=source_dir,
        device=device,
        contact_claim_boundary=contact_claim_boundary,
        task_claim_boundary=task_claim_boundary,
        drop_settle_options=drop_settle_options,
        sphere_rain_options=sphere_rain_options,
    )
    opt_in_contact, opt_in_tasks = _synthetic_task_probe_payloads(
        opt_in_package,
        source_dir=source_dir,
        device=device,
        contact_claim_boundary=contact_claim_boundary,
        task_claim_boundary=task_claim_boundary,
        drop_settle_options=drop_settle_options,
        sphere_rain_options=sphere_rain_options,
    )
    default_payload = _package_collision_payload(default_package)
    opt_in_payload = _package_collision_payload(opt_in_package)
    package_pair_changed = default_payload != opt_in_payload
    return {
        "case_id": "cylinder_near_miss_cluster",
        "description": (
            "Explicit opt-in synthetic Newton probe over the package changed by the "
            "cylinder scoring-policy multiplier."
        ),
        "scope": "single_synthetic_near_miss_default_vs_opt_in_package",
        "primitive_score_multipliers": {
            "cylinder": CYLINDER_NEAR_MISS_REPORT_ONLY_EXTENSION_MULTIPLIER
        },
        "default_package": _package_probe_package_summary(default_package),
        "opt_in_package": _package_probe_package_summary(opt_in_package),
        "default_contact": default_contact,
        "opt_in_contact": opt_in_contact,
        "default_tasks": default_tasks,
        "opt_in_tasks": opt_in_tasks,
        "decision": {
            "default_package_changed": False,
            "opt_in_package_changed": package_pair_changed,
            "package_pair_changed": package_pair_changed,
            "primitive_kind_changed": _package_primitive_kinds(default_package)
            != _package_primitive_kinds(opt_in_package),
            "status_gate": (
                "newton_tasks_smoke_passed"
                if package_pair_changed
                else "opt_in_package_did_not_change"
            ),
            "real_usd_rerun_triggered": False,
            "collision_quality_claim_supported": False,
            "claim_boundary": "synthetic_task_smoke_not_collision_quality",
        },
    }


def _controlled_merge_search_package_probe_case_payload(
    *,
    case_id: str,
    description: str,
    mesh: TriangleMesh,
    options: CPDLikeObjectiveOptions,
) -> dict[str, object]:
    default_decomposition, opt_in_decomposition = _controlled_merge_search_decomposition_pair(mesh)
    default_package, opt_in_package = _controlled_merge_search_package_pair(
        case_id=case_id,
        mesh=mesh,
        options=options,
    )
    default_payload = _package_collision_payload(default_package)
    opt_in_payload = _package_collision_payload(opt_in_package)
    package_pair_changed = default_payload != opt_in_payload
    default_mapping = _package_mapping_summary(default_package)
    opt_in_mapping = _package_mapping_summary(opt_in_package)
    default_excess = float(
        default_decomposition.merge_cost_summary["accepted_normalized_excess_sum"]
    )
    opt_in_excess = float(
        opt_in_decomposition.merge_cost_summary["accepted_normalized_excess_sum"]
    )
    matched = (
        default_decomposition.topology_merge_count == 1
        and default_decomposition.virtual_component_merge_count == 0
        and opt_in_decomposition.topology_merge_count == 0
        and opt_in_decomposition.virtual_component_merge_count == 1
        and package_pair_changed
        and bool(default_mapping["fully_mapped"])
        and bool(opt_in_mapping["fully_mapped"])
        and opt_in_excess < default_excess
    )
    return {
        "case_id": case_id,
        "description": description,
        "scope": "single_fixture_opt_in_merge_search_package_probe",
        "synthetic_only": True,
        "real_usd_scope": "not_run_synthetic_only",
        "expectation_status": "matched" if matched else "mismatched",
        "default_merge_search_policy": "topology_then_virtual",
        "opt_in_merge_search_policy": "cost_guided_pairwise",
        "opt_in_policy_applied_to_package_probe": True,
        "opt_in_policy_scope": "synthetic_decomposition_and_package_probe_only",
        "default_behavior_changed": False,
        "merge_search_behavior_changed": package_pair_changed,
        "package_pair_changed": package_pair_changed,
        "opt_in_package_changed": package_pair_changed,
        "default_package": _package_probe_package_summary(default_package),
        "opt_in_package": _package_probe_package_summary(opt_in_package),
        "default_package_mapping": default_mapping,
        "opt_in_package_mapping": opt_in_mapping,
        "merge_trace": {
            "default": list(default_decomposition.merge_trace),
            "opt_in": list(opt_in_decomposition.merge_trace),
        },
        "comparison": {
            "default_topology_merge_count": default_decomposition.topology_merge_count,
            "default_virtual_component_merge_count": (
                default_decomposition.virtual_component_merge_count
            ),
            "opt_in_topology_merge_count": opt_in_decomposition.topology_merge_count,
            "opt_in_virtual_component_merge_count": (
                opt_in_decomposition.virtual_component_merge_count
            ),
            "default_accepted_normalized_excess_sum": default_excess,
            "opt_in_accepted_normalized_excess_sum": opt_in_excess,
            "accepted_normalized_excess_delta": float(opt_in_excess - default_excess),
        },
        "decision": {
            "diagnostic_conclusion": (
                "opt_in_cost_guided_merge_search_changes_synthetic_package"
                if package_pair_changed
                else "opt_in_cost_guided_merge_search_preserves_synthetic_package"
            ),
            "default_package_changed": False,
            "newton_mapping_summary_recorded": True,
            "newton_task_comparison_triggered": False,
            "newton_task_comparison_gate": "not_triggered_synthetic_package_probe_only",
            "recommended_next_component": "opt_in_merge_search_newton_task_probe_or_real_usd_gate",
            "claim_boundary": CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_CLAIM_BOUNDARY,
        },
    }


def _controlled_merge_search_newton_probe_case_payload(
    *,
    source_dir: str,
    device: str,
    drop_settle_options: DropSettleOptions,
    sphere_rain_options: SphereRainOptions,
    contact_claim_boundary: str,
    task_claim_boundary: str,
) -> dict[str, object]:
    options = CPDLikeObjectiveOptions(
        claim_boundary=CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_CLAIM_BOUNDARY,
        evidence_level=CONTROLLED_MERGE_SEARCH_PACKAGE_PROBE_EVIDENCE_LEVEL,
    )
    default_package, opt_in_package = _controlled_merge_search_package_pair(
        case_id="cost_guided_pair_choice",
        mesh=_cost_guided_pair_choice_mesh(),
        options=options,
    )
    default_contact, default_tasks = _synthetic_task_probe_payloads(
        default_package,
        source_dir=source_dir,
        device=device,
        contact_claim_boundary=contact_claim_boundary,
        task_claim_boundary=task_claim_boundary,
        drop_settle_options=drop_settle_options,
        sphere_rain_options=sphere_rain_options,
    )
    opt_in_contact, opt_in_tasks = _synthetic_task_probe_payloads(
        opt_in_package,
        source_dir=source_dir,
        device=device,
        contact_claim_boundary=contact_claim_boundary,
        task_claim_boundary=task_claim_boundary,
        drop_settle_options=drop_settle_options,
        sphere_rain_options=sphere_rain_options,
    )
    default_payload = _package_collision_payload(default_package)
    opt_in_payload = _package_collision_payload(opt_in_package)
    package_pair_changed = default_payload != opt_in_payload
    statuses = _newton_probe_statuses(
        {
            "default_contact": default_contact,
            "opt_in_contact": opt_in_contact,
            "default_tasks": default_tasks,
            "opt_in_tasks": opt_in_tasks,
        }
    )
    tasks_smoke_passed = package_pair_changed and all(
        status == "smoke_passed" for status in statuses
    )
    return {
        "case_id": "cost_guided_pair_choice",
        "description": (
            "Synthetic Newton task-smoke probe over the package pair changed by "
            "the opt-in cost-guided merge-search lane."
        ),
        "scope": "single_synthetic_merge_search_default_vs_opt_in_package",
        "default_merge_search_policy": "topology_then_virtual",
        "opt_in_merge_search_policy": "cost_guided_pairwise",
        "default_package": _package_probe_package_summary(default_package),
        "opt_in_package": _package_probe_package_summary(opt_in_package),
        "default_contact": default_contact,
        "opt_in_contact": opt_in_contact,
        "default_tasks": default_tasks,
        "opt_in_tasks": opt_in_tasks,
        "decision": {
            "default_package_changed": False,
            "opt_in_package_changed": package_pair_changed,
            "package_pair_changed": package_pair_changed,
            "merge_search_behavior_changed": package_pair_changed,
            "status_gate": (
                "newton_tasks_smoke_passed"
                if tasks_smoke_passed
                else "opt_in_package_did_not_change"
                if not package_pair_changed
                else "newton_tasks_blocked_or_failed"
            ),
            "newton_task_comparison_triggered": True,
            "real_usd_rerun_triggered": False,
            "collision_quality_claim_supported": False,
            "merge_policy_superiority_claim_supported": False,
            "claim_boundary": task_claim_boundary,
        },
    }


def _controlled_merge_search_package_pair(
    *,
    case_id: str,
    mesh: TriangleMesh,
    options: CPDLikeObjectiveOptions,
):
    default_decomposition, opt_in_decomposition = _controlled_merge_search_decomposition_pair(mesh)
    default_package = package_from_cpd_like_report(
        default_decomposition,
        asset_id=f"{case_id}_topology_then_virtual",
        source_path=f"synthetic://{case_id}/topology_then_virtual",
        claim_boundary=options.claim_boundary,
    )
    opt_in_package = package_from_cpd_like_report(
        opt_in_decomposition,
        asset_id=f"{case_id}_cost_guided_pairwise",
        source_path=f"synthetic://{case_id}/cost_guided_pairwise",
        claim_boundary=options.claim_boundary,
    )
    return default_package, opt_in_package


def _controlled_merge_search_decomposition_pair(
    mesh: TriangleMesh,
) -> tuple[CPDLikeDecompositionReport, CPDLikeDecompositionReport]:
    default_decomposition = decompose_mesh(
        mesh,
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="topology_then_virtual",
        report_merge_trace="steps",
    )
    opt_in_decomposition = decompose_mesh(
        mesh,
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy="cost_guided_pairwise",
        report_merge_trace="steps",
    )
    return default_decomposition, opt_in_decomposition


def _cylinder_scoring_policy_package_pair(
    *,
    case_id: str,
    mesh: TriangleMesh,
    options: CPDLikeObjectiveOptions,
):
    default_decomposition = decompose_mesh(
        mesh,
        max_primitives=1,
        primitive_subset=("box", "cylinder"),
    )
    opt_in_decomposition = decompose_mesh(
        mesh,
        max_primitives=1,
        primitive_subset=("box", "cylinder"),
        primitive_score_multipliers={
            "cylinder": CYLINDER_NEAR_MISS_REPORT_ONLY_EXTENSION_MULTIPLIER
        },
    )
    default_package = package_from_cpd_like_report(
        default_decomposition,
        asset_id=f"{case_id}_default",
        source_path=f"synthetic://{case_id}/default",
        claim_boundary=options.claim_boundary,
    )
    opt_in_package = package_from_cpd_like_report(
        opt_in_decomposition,
        asset_id=f"{case_id}_opt_in",
        source_path=f"synthetic://{case_id}/opt_in_scoring_policy",
        claim_boundary=options.claim_boundary,
    )
    return default_package, opt_in_package


def _synthetic_task_probe_payloads(
    package,
    *,
    source_dir: str,
    device: str,
    contact_claim_boundary: str,
    task_claim_boundary: str,
    drop_settle_options: DropSettleOptions,
    sphere_rain_options: SphereRainOptions,
) -> tuple[dict[str, object], dict[str, object]]:
    contact = run_newton_contact_smoke(
        package,
        source_dir=source_dir,
        device=device,
        claim_boundary=contact_claim_boundary,
    ).to_dict()
    if contact["status"] != "smoke_passed":
        tasks = {
            "drop_settle": _blocked_newton_probe_payload(
                package,
                stage="newton_drop_settle",
                status="blocked_by_contact_canary",
                probe_type="drop_settle",
                device=device,
                claim_boundary=task_claim_boundary,
                fallback_reason=str(contact["status"]),
            ),
            "sphere_rain": _blocked_newton_probe_payload(
                package,
                stage="newton_sphere_rain",
                status="blocked_by_contact_canary",
                probe_type="sphere_rain",
                device=device,
                claim_boundary=task_claim_boundary,
                fallback_reason=str(contact["status"]),
            ),
        }
        return contact, tasks

    return contact, {
        "drop_settle": run_newton_drop_settle(
            package,
            source_dir=source_dir,
            device=device,
            options=drop_settle_options,
            claim_boundary=task_claim_boundary,
        ).to_dict(),
        "sphere_rain": run_newton_sphere_rain(
            package,
            source_dir=source_dir,
            device=device,
            options=sphere_rain_options,
            claim_boundary=task_claim_boundary,
        ).to_dict(),
    }


def _blocked_newton_probe_payload(
    package,
    *,
    stage: str,
    status: str,
    probe_type: str,
    device: str,
    claim_boundary: str,
    fallback_reason: str,
) -> dict[str, object]:
    return NewtonDiagnosticReport(
        stage=stage,
        status=status,
        asset_id=package.asset_id,
        package_id=package.package_id,
        probe_type=probe_type,
        device=device,
        environment=None,
        primitive_count=len(package.primitives),
        type_counts=dict(Counter(primitive.kind for primitive in package.primitives)),
        shape_mappings=(),
        contact_canaries=(),
        claim_boundary=claim_boundary,
        fallback_reason=fallback_reason,
    ).to_dict()


def _newton_probe_statuses(case_payload: dict[str, object]) -> list[str]:
    statuses = [
        str(case_payload["default_contact"]["status"]),
        str(case_payload["opt_in_contact"]["status"]),
    ]
    for lane in ("default_tasks", "opt_in_tasks"):
        tasks = case_payload[lane]
        statuses.extend(
            [
                str(tasks["drop_settle"]["status"]),
                str(tasks["sphere_rain"]["status"]),
            ]
        )
    return statuses


def _lookahead_newton_probe_statuses(case_payload: dict[str, object]) -> list[str]:
    statuses = [
        str(case_payload["greedy_contact"]["status"]),
        str(case_payload["lookahead_contact"]["status"]),
    ]
    for lane in ("greedy_tasks", "lookahead_tasks"):
        tasks = case_payload[lane]
        statuses.extend(
            [
                str(tasks["drop_settle"]["status"]),
                str(tasks["sphere_rain"]["status"]),
            ]
        )
    return statuses


def _aggregate_probe_status(
    statuses: list[str],
    *,
    package_pair_changed: bool = True,
) -> str:
    if any(status == "runtime_failure" for status in statuses):
        return "runtime_failure"
    non_smoke = {status for status in statuses if status != "smoke_passed"}
    if (
        non_smoke <= {"dependency_gap", "blocked_by_contact_canary"}
        and "dependency_gap" in non_smoke
    ):
        return "dependency_gap"
    if not package_pair_changed:
        return "partial"
    if statuses and all(status == "smoke_passed" for status in statuses):
        return "smoke_passed"
    return "partial"


def _package_primitive_kinds(package) -> tuple[str, ...]:
    return tuple(primitive.kind for primitive in package.primitives)


def _package_collision_payload(package) -> dict[str, object]:
    primitive_payloads = []
    for primitive in package.primitives:
        payload = primitive.to_dict()
        payload.pop("primitive_id", None)
        primitive_payloads.append(payload)
    return {
        "method": package.method,
        "stage": package.stage,
        "status": package.status,
        "mesh_point_count": package.mesh_point_count,
        "mesh_face_count": package.mesh_face_count,
        "max_source_faces": package.max_source_faces,
        "primitive_subset": list(package.primitive_subset),
        "unsupported_primitives": list(package.unsupported_primitives),
        "fallback": package.fallback.to_dict() if package.fallback else None,
        "primitives": primitive_payloads,
    }


def _package_probe_package_summary(package) -> dict[str, object]:
    return {
        "package_id": package.package_id,
        "status": package.status,
        "primitive_count": len(package.primitives),
        "primitive_kinds": [primitive.kind for primitive in package.primitives],
        "primitive_source_faces": [
            list(primitive.source_faces) for primitive in package.primitives
        ],
        "claim_boundary": package.claim_boundary,
    }


def _selection_probe_row(row, *, rank_key: str, rank: int) -> dict[str, object]:
    return {
        "primitive_type": row.primitive_type,
        rank_key: rank,
        "raw_cost_rank": row.raw_cost_rank,
        "weighted_volume": row.candidate.weighted_volume,
        "score_multiplier": row.score_multiplier,
        "effective_score": row.effective_score,
        "selection_admissible": row.selection_admissible,
        "selection_admissibility_reason": row.selection_admissibility_reason,
        "selection_support": row.support,
        "contains_assigned_points": row.candidate.contains_assigned_points,
        "dimensions": row.candidate.dimensions,
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
    ranked_candidates = rank_primitive_candidates_for_selection(
        mesh,
        frozenset(range(mesh.face_count)),
        candidates,
    )
    rows: list[tuple[float, float, int, dict[str, object]]] = []
    for candidate_order, ranked_candidate in enumerate(ranked_candidates):
        candidate = ranked_candidate.candidate
        normalized_weighted_volume = float(candidate.weighted_volume / normalizer)
        rows.append(
            (
                0.0 if ranked_candidate.selection_admissible else 1.0,
                candidate.weighted_volume,
                candidate_order,
                {
                    "primitive_type": candidate.primitive_type,
                    "candidate_order": ranked_candidate.candidate_order,
                    "raw_cost_rank": ranked_candidate.raw_cost_rank,
                    "selection_objective": NATIVE_SELECTION_COST_NAME,
                    "selection_objective_units": "raw_weighted_primitive_volume_proxy",
                    "selection_admissible": ranked_candidate.selection_admissible,
                    "selection_admissibility_reason": (
                        ranked_candidate.selection_admissibility_reason
                    ),
                    "selection_support": ranked_candidate.support,
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
        for rank, (_, _, _, row) in enumerate(
            sorted(rows, key=lambda item: (item[0], item[1], item[2])),
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
        "fully_mapped": bool(
            package.primitives
            and status_counts.get("mapped", 0) == len(package.primitives)
        ),
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


def _cylinder_near_miss_cluster_mesh() -> TriangleMesh:
    height = 0.6
    cross_section = (
        (1.15, 0.0),
        (0.4625, 0.8010735),
        (-0.4625, 0.8010735),
        (-1.15, 0.0),
        (-0.4625, -0.8010735),
        (0.4625, -0.8010735),
    )
    points: list[list[float]] = []
    for z in (-height * 0.5, height * 0.5):
        for x, y in cross_section:
            points.append([x, y, z])

    faces: list[list[int]] = []
    ring_size = len(cross_section)
    for index in range(ring_size):
        next_index = (index + 1) % ring_size
        bottom_left = index
        bottom_right = next_index
        top_left = ring_size + index
        top_right = ring_size + next_index
        faces.append([bottom_left, bottom_right, top_right])
        faces.append([bottom_left, top_right, top_left])
    for index in range(1, ring_size - 1):
        faces.append([0, index + 1, index])
        faces.append([ring_size, ring_size + index, ring_size + index + 1])
    return TriangleMesh(points=np.asarray(points, dtype=float), faces=np.asarray(faces, dtype=int))


def _boxy_cuboid_guardrail_mesh() -> TriangleMesh:
    half_x = 1.0
    half_y = 0.5
    half_z = 0.5
    points = np.asarray(
        [
            [-half_x, -half_y, -half_z],
            [half_x, -half_y, -half_z],
            [half_x, half_y, -half_z],
            [-half_x, half_y, -half_z],
            [-half_x, -half_y, half_z],
            [half_x, -half_y, half_z],
            [half_x, half_y, half_z],
            [-half_x, half_y, half_z],
        ],
        dtype=float,
    )
    faces = np.asarray(
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
        dtype=int,
    )
    return TriangleMesh(points=points, faces=faces)


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
        report_merge_trace=policy.report_merge_trace,
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
    decomposition_payload = decomposition.to_dict()
    merge_trace = decomposition_payload.get("merge_trace", [])
    if merge_trace:
        summary["merge_trace"] = merge_trace
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


def _lookahead_merge_case_payload(
    greedy: CPDLikeDecompositionReport,
    lookahead: CPDLikeDecompositionReport,
) -> dict[str, object]:
    greedy_summary = _lookahead_lane_summary(greedy)
    lookahead_summary = _lookahead_lane_summary(lookahead)
    greedy_faces = greedy_summary["primitive_source_faces"]
    lookahead_faces = lookahead_summary["primitive_source_faces"]
    greedy_projected_total = _first_step_projected_total(greedy_summary)
    lookahead_projected_total = _first_step_projected_total(lookahead_summary)
    return {
        "case_id": "lookahead_merge_trap",
        "description": (
            "Four-component synthetic fixture where a locally cheapest first merge leaves a "
            "more expensive second merge, while two-step lookahead chooses a lower projected "
            "two-merge path."
        ),
        "scope": "single_synthetic_merge_search_greedy_vs_two_step_lookahead",
        "greedy": greedy_summary,
        "lookahead": lookahead_summary,
        "decision": {
            "lookahead_decision_changed": greedy_faces != lookahead_faces,
            "projected_cost_improved": lookahead_projected_total < greedy_projected_total,
            "greedy_projected_total_normalized_excess": greedy_projected_total,
            "lookahead_projected_total_normalized_excess": lookahead_projected_total,
            "default_pipeline_changed": False,
            "newton_task_comparison_triggered": False,
            "real_usd_rerun_triggered": False,
            "collision_quality_claim_supported": False,
            "merge_policy_superiority_claim_supported": False,
            "claim_boundary": COST_GUIDED_LOOKAHEAD_MERGE_CLAIM_BOUNDARY,
        },
    }


def _lookahead_package_probe_case_payload(
    *,
    greedy_decomposition: CPDLikeDecompositionReport,
    lookahead_decomposition: CPDLikeDecompositionReport,
    greedy_package,
    lookahead_package,
) -> dict[str, object]:
    greedy_payload = _package_collision_payload(greedy_package)
    lookahead_payload = _package_collision_payload(lookahead_package)
    package_pair_changed = greedy_payload != lookahead_payload
    greedy_mapping = _package_mapping_summary(greedy_package)
    lookahead_mapping = _package_mapping_summary(lookahead_package)
    greedy_summary = _lookahead_lane_summary(greedy_decomposition)
    lookahead_summary = _lookahead_lane_summary(lookahead_decomposition)
    greedy_projected = _first_step_projected_total(greedy_summary)
    lookahead_projected = _first_step_projected_total(lookahead_summary)
    greedy_faces = _package_probe_package_summary(greedy_package)["primitive_source_faces"]
    lookahead_faces = _package_probe_package_summary(lookahead_package)["primitive_source_faces"]
    expected_faces = (
        greedy_faces == [[0, 2, 3], [1]]
        and lookahead_faces == [[0, 1], [2, 3]]
    )
    matched = (
        package_pair_changed
        and expected_faces
        and bool(greedy_mapping["fully_mapped"])
        and bool(lookahead_mapping["fully_mapped"])
        and lookahead_projected < greedy_projected
    )
    return {
        "case_id": "lookahead_merge_trap",
        "scope": "single_fixture_lookahead_merge_search_package_probe",
        "expectation_status": "matched" if matched else "mismatched",
        "greedy_merge_search_policy": MERGE_SEARCH_COST_GUIDED_PAIRWISE,
        "lookahead_merge_search_policy": MERGE_SEARCH_TWO_STEP_LOOKAHEAD,
        "opt_in_policy_applied_to_package_probe": True,
        "opt_in_policy_scope": "synthetic_decomposition_and_package_probe_only",
        "package_pair_changed": package_pair_changed,
        "lookahead_package_changed": package_pair_changed,
        "merge_search_behavior_changed": package_pair_changed,
        "greedy_package": _package_probe_package_summary(greedy_package),
        "lookahead_package": _package_probe_package_summary(lookahead_package),
        "greedy_package_mapping": greedy_mapping,
        "lookahead_package_mapping": lookahead_mapping,
        "merge_trace": {
            "greedy": greedy_summary["merge_trace"],
            "lookahead": lookahead_summary["merge_trace"],
        },
        "comparison": {
            "greedy_accepted_normalized_excess_sum": greedy_summary[
                "accepted_normalized_excess_sum"
            ],
            "lookahead_accepted_normalized_excess_sum": lookahead_summary[
                "accepted_normalized_excess_sum"
            ],
            "accepted_normalized_excess_delta": float(
                lookahead_summary["accepted_normalized_excess_sum"]
                - greedy_summary["accepted_normalized_excess_sum"]
            ),
            "greedy_projected_total_normalized_excess": greedy_projected,
            "lookahead_projected_total_normalized_excess": lookahead_projected,
            "projected_total_normalized_excess_delta": float(
                lookahead_projected - greedy_projected
            ),
        },
        "decision": {
            "newton_mapping_summary_recorded": True,
            "newton_task_comparison_triggered": False,
            "newton_task_comparison_gate": "not_triggered_synthetic_package_probe_only",
            "recommended_next_component": (
                "lookahead_merge_search_newton_task_probe_or_real_usd_gate"
            ),
            "real_usd_rerun_triggered": False,
            "collision_quality_claim_supported": False,
            "merge_policy_superiority_claim_supported": False,
            "claim_boundary": COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY,
        },
    }


def _lookahead_newton_probe_case_payload(
    *,
    source_dir: str,
    device: str,
    drop_settle_options: DropSettleOptions,
    sphere_rain_options: SphereRainOptions,
    contact_claim_boundary: str,
    task_claim_boundary: str,
) -> dict[str, object]:
    greedy_decomposition, lookahead_decomposition = _lookahead_merge_decomposition_pair()
    greedy_package, lookahead_package = _lookahead_merge_package_pair(
        greedy_decomposition,
        lookahead_decomposition,
    )
    greedy_contact, greedy_tasks = _synthetic_task_probe_payloads(
        greedy_package,
        source_dir=source_dir,
        device=device,
        contact_claim_boundary=contact_claim_boundary,
        task_claim_boundary=task_claim_boundary,
        drop_settle_options=drop_settle_options,
        sphere_rain_options=sphere_rain_options,
    )
    lookahead_contact, lookahead_tasks = _synthetic_task_probe_payloads(
        lookahead_package,
        source_dir=source_dir,
        device=device,
        contact_claim_boundary=contact_claim_boundary,
        task_claim_boundary=task_claim_boundary,
        drop_settle_options=drop_settle_options,
        sphere_rain_options=sphere_rain_options,
    )
    greedy_payload = _package_collision_payload(greedy_package)
    lookahead_payload = _package_collision_payload(lookahead_package)
    package_pair_changed = greedy_payload != lookahead_payload
    greedy_faces = _package_probe_package_summary(greedy_package)["primitive_source_faces"]
    lookahead_faces = _package_probe_package_summary(lookahead_package)["primitive_source_faces"]
    expected_package_faces = (
        greedy_faces == [[0, 2, 3], [1]]
        and lookahead_faces == [[0, 1], [2, 3]]
    )
    statuses = _lookahead_newton_probe_statuses(
        {
            "greedy_contact": greedy_contact,
            "lookahead_contact": lookahead_contact,
            "greedy_tasks": greedy_tasks,
            "lookahead_tasks": lookahead_tasks,
        }
    )
    tasks_smoke_passed = (
        package_pair_changed
        and expected_package_faces
        and all(status == "smoke_passed" for status in statuses)
    )
    return {
        "case_id": "lookahead_merge_trap",
        "description": (
            "Synthetic Newton task-smoke probe over the package pair changed by "
            "the opt-in two-step lookahead merge-search lane."
        ),
        "scope": "single_synthetic_lookahead_greedy_vs_two_step_package",
        "greedy_merge_search_policy": MERGE_SEARCH_COST_GUIDED_PAIRWISE,
        "lookahead_merge_search_policy": MERGE_SEARCH_TWO_STEP_LOOKAHEAD,
        "greedy_package": _package_probe_package_summary(greedy_package),
        "lookahead_package": _package_probe_package_summary(lookahead_package),
        "greedy_contact": greedy_contact,
        "lookahead_contact": lookahead_contact,
        "greedy_tasks": greedy_tasks,
        "lookahead_tasks": lookahead_tasks,
        "decision": {
            "default_pipeline_changed": False,
            "lookahead_package_changed": package_pair_changed,
            "package_pair_changed": package_pair_changed,
            "expected_package_faces": expected_package_faces,
            "merge_search_behavior_changed": package_pair_changed,
            "status_gate": (
                "newton_tasks_smoke_passed"
                if tasks_smoke_passed
                else "lookahead_package_did_not_change"
                if not package_pair_changed
                else "lookahead_package_faces_unexpected"
                if not expected_package_faces
                else "newton_tasks_blocked_or_failed"
            ),
            "newton_task_comparison_triggered": True,
            "real_usd_rerun_triggered": False,
            "collision_quality_claim_supported": False,
            "merge_policy_superiority_claim_supported": False,
            "claim_boundary": task_claim_boundary,
        },
    }


def _first_step_projected_total(lane_summary: dict[str, object]) -> float:
    trace = lane_summary["merge_trace"]
    if not trace:
        return float(lane_summary["accepted_normalized_excess_sum"])
    first_step = trace[0]
    if "projected_total_normalized_excess_volume" in first_step:
        return float(first_step["projected_total_normalized_excess_volume"])
    return float(lane_summary["accepted_normalized_excess_sum"])


def _lookahead_lane_summary(report: CPDLikeDecompositionReport) -> dict[str, object]:
    merge_trace = _lookahead_report_merge_trace(report)
    return {
        "status": report.status,
        "stage": report.stage,
        "merge_search_policy": report.merge_search_policy,
        "primitive_count": report.primitive_count,
        "primitive_source_faces": _primitive_source_faces(report),
        "topology_merge_count": report.topology_merge_count,
        "virtual_component_merge_count": report.virtual_component_merge_count,
        "blocked_merge_count": report.blocked_merge_count,
        "accepted_normalized_excess_sum": float(
            report.merge_cost_summary["accepted_normalized_excess_sum"]
        ),
        "failure_labels": _decomposition_failure_labels(report),
        "merge_trace": merge_trace,
    }


def _lookahead_report_merge_trace(report: CPDLikeDecompositionReport) -> list[dict[str, object]]:
    trace = [dict(step) for step in report.merge_trace]
    if trace and "projected_total_normalized_excess_volume" not in trace[0]:
        followup_cost = sum(
            float(step["normalized_excess_volume"]) for step in trace[1:]
        )
        if trace[1:]:
            trace[0]["projected_followup_normalized_excess_volume"] = float(followup_cost)
        trace[0]["projected_total_normalized_excess_volume"] = float(
            float(trace[0]["normalized_excess_volume"]) + followup_cost
        )
    return trace


def _primitive_source_faces(report: CPDLikeDecompositionReport) -> list[list[int]]:
    return [list(primitive.source_faces) for primitive in report.primitives]


def _decomposition_failure_labels(report: CPDLikeDecompositionReport) -> list[str]:
    labels = []
    if report.fallback_reason:
        labels.append(report.fallback_reason)
    if report.primitive_count > report.max_primitives:
        labels.append("primitive_budget_not_met")
    return labels


def _lookahead_merge_decomposition_pair() -> tuple[
    CPDLikeDecompositionReport,
    CPDLikeDecompositionReport,
]:
    greedy = decompose_mesh(
        _lookahead_merge_trap_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy=MERGE_SEARCH_COST_GUIDED_PAIRWISE,
        report_merge_trace="steps",
    )
    lookahead = decompose_mesh(
        _lookahead_merge_trap_mesh(),
        max_primitives=2,
        primitive_subset=("box",),
        component_merge="virtual_pairwise",
        merge_search_policy=MERGE_SEARCH_TWO_STEP_LOOKAHEAD,
        report_merge_trace="steps",
    )
    return greedy, lookahead


def _lookahead_merge_package_pair(
    greedy_decomposition: CPDLikeDecompositionReport,
    lookahead_decomposition: CPDLikeDecompositionReport,
):
    greedy_package = package_from_cpd_like_report(
        greedy_decomposition,
        asset_id="lookahead_merge_trap_cost_guided_pairwise",
        source_path="synthetic://lookahead_merge_trap/cost_guided_pairwise",
        claim_boundary=COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY,
    )
    lookahead_package = package_from_cpd_like_report(
        lookahead_decomposition,
        asset_id="lookahead_merge_trap_two_step_lookahead",
        source_path="synthetic://lookahead_merge_trap/two_step_lookahead",
        claim_boundary=COST_GUIDED_LOOKAHEAD_PACKAGE_PROBE_CLAIM_BOUNDARY,
    )
    return greedy_package, lookahead_package


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


def _lookahead_merge_trap_mesh() -> TriangleMesh:
    centers = [
        (8.444218515250482, 7.579544029403024, 1.261714742492535),
        (2.5891675029296337, 5.112747213686085, 1.2148024123512429),
        (7.837985890347726, 3.0331272607892745, 1.4297908624570674),
        (5.833820394550312, 9.081128851953352, 1.5140605674521708),
    ]
    points = []
    faces = []
    for x, y, z in centers:
        base = len(points)
        points.extend(
            [
                (x, y, z),
                (x + 0.05, y, z),
                (x, y + 0.05, z),
            ]
        )
        faces.append((base, base + 1, base + 2))
    return TriangleMesh(points=np.asarray(points), faces=np.asarray(faces))


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
