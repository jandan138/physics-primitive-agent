import argparse
import contextlib
import json
import math
import os
import sys
from pathlib import Path

from primitive_collision_compiler.assets.materialization import build_asset_materialization_report
from primitive_collision_compiler.assets.usd_smoke import (
    inspect_usd_asset,
    load_asset_manifest,
    resolve_asset_path,
)
from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.objective import (
    CPDLikeObjectiveOptions,
    build_cpd_like_objective_report,
)
from primitive_collision_compiler.baselines.cpd_like.package import package_from_cpd_like_report
from primitive_collision_compiler.baselines.cpd_like.primitives import (
    normalize_primitive_selection_guard,
    normalize_primitive_selection_support_thresholds,
)
from primitive_collision_compiler.baselines.cpd_like.real_usd_comparison import (
    REAL_USD_CANDIDATE_LOSS_CLAIM_BOUNDARY,
    REAL_USD_CANDIDATE_LOSS_EVIDENCE_LEVEL,
    REAL_USD_NATIVE_FITTING_CLAIM_BOUNDARY,
    REAL_USD_NATIVE_FITTING_EVIDENCE_LEVEL,
    build_real_usd_candidate_loss_diagnosis_report,
    build_real_usd_native_contact_comparison_report,
    build_real_usd_native_fitting_comparison_report,
    build_real_usd_native_task_comparison_report,
)
from primitive_collision_compiler.baselines.cpd_like.synthetic import (
    NEWTON_NATIVE_EXTENDED_SUBSET,
    NEWTON_NATIVE_FITTING_COMPARISON_CLAIM_BOUNDARY,
    NEWTON_NATIVE_FITTING_COMPARISON_EVIDENCE_LEVEL,
    NEWTON_NATIVE_LEGACY_SUBSET,
    build_cpd_like_cylinder_near_miss_fit_ablation_report,
    build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report,
    build_cpd_like_cylinder_near_miss_scoring_sensitivity_report,
    build_cpd_like_cylinder_scoring_policy_newton_probe_report,
    build_cpd_like_cylinder_scoring_policy_package_probe_report,
    build_cpd_like_cylinder_scoring_policy_selection_probe_report,
    build_cpd_like_controlled_merge_search_package_probe_report,
    build_cpd_like_controlled_merge_search_newton_probe_report,
    build_cpd_like_cost_guided_lookahead_merge_report,
    build_cpd_like_cost_guided_lookahead_newton_probe_report,
    build_cpd_like_cost_guided_lookahead_package_probe_report,
    build_cpd_like_cost_guided_synthetic_comparison_report,
    build_cpd_like_expected_failure_synthetic_workbench_report,
    build_cpd_like_four_block_slice_report,
    build_cpd_like_near_miss_workbench_report,
    build_cpd_like_synthetic_comparison_report,
    build_newton_native_fitting_comparison_report,
)
from primitive_collision_compiler.baselines.cpd_like.usd import USDMeshLoadError, load_first_mesh
from primitive_collision_compiler.baselines.cpd_paper.offline import (
    build_cpd_paper_offline_report,
)
from primitive_collision_compiler.config import load_compile_config
from primitive_collision_compiler.contracts import CompileReport
from primitive_collision_compiler.newton.diagnostics import run_newton_contact_smoke
from primitive_collision_compiler.newton.drop_settle import (
    DROP_SETTLE_CLAIM_BOUNDARY,
    DropSettleOptions,
    run_newton_drop_settle,
)
from primitive_collision_compiler.newton.env import inspect_newton_environment
from primitive_collision_compiler.newton.sphere_rain import (
    SPHERE_RAIN_CLAIM_BOUNDARY,
    SphereRainOptions,
    run_newton_sphere_rain,
)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="npc-compile",
        description="Newton Primitive Collision Compiler",
    )
    parser.add_argument("--config", type=Path, help="path to a compile configuration YAML file")
    parser.add_argument("--dry-run", action="store_true", help="validate config and emit a report")
    parser.add_argument("--check-newton", action="store_true", help="emit Newton environment diagnostics")
    parser.add_argument("--check-assets", action="store_true", help="emit USD asset smoke diagnostics")
    parser.add_argument(
        "--materialize-assets",
        action="store_true",
        help="copy/localize manifest USD dependency closures into ignored repo-local mirrors",
    )
    parser.add_argument(
        "--run-cpd-like",
        action="store_true",
        help="run the geometry-only CPD-like face-merge smoke path",
    )
    parser.add_argument(
        "--run-cpd-like-objective-report",
        action="store_true",
        help="run CPD-like geometry and emit an offline paper-aligned surrogate objective report",
    )
    parser.add_argument(
        "--run-cpd-like-synthetic-comparison",
        action="store_true",
        help="run offline synthetic topology/component-merge objective comparison",
    )
    parser.add_argument(
        "--run-cpd-like-cost-guided-synthetic-comparison",
        action="store_true",
        help="run offline synthetic objective comparison for the cost-guided merge-search smoke",
    )
    parser.add_argument(
        "--run-cpd-like-expected-failure-workbench",
        action="store_true",
        help="run offline synthetic expected-failure workbench for known CPD-like gaps",
    )
    parser.add_argument(
        "--run-cpd-like-near-miss-workbench",
        action="store_true",
        help="run offline synthetic near-miss primitive-ranking fixture workbench",
    )
    parser.add_argument(
        "--run-cpd-like-cylinder-near-miss-fit-ablation",
        action="store_true",
        help="run offline synthetic cylinder near-miss radial fit-ablation diagnostics",
    )
    parser.add_argument(
        "--run-cpd-like-cylinder-near-miss-scoring-sensitivity",
        action="store_true",
        help="run offline synthetic cylinder near-miss scoring sensitivity diagnostics",
    )
    parser.add_argument(
        "--run-cpd-like-cylinder-near-miss-scoring-policy-ablation",
        action="store_true",
        help="run offline synthetic report-only cylinder near-miss scoring-policy ablation",
    )
    parser.add_argument(
        "--run-cpd-like-cylinder-scoring-policy-selection-probe",
        action="store_true",
        help="run offline synthetic opt-in cylinder scoring-policy selection probe",
    )
    parser.add_argument(
        "--run-cpd-like-cylinder-scoring-policy-package-probe",
        action="store_true",
        help="run offline synthetic opt-in cylinder scoring-policy package probe",
    )
    parser.add_argument(
        "--run-cpd-like-cylinder-scoring-policy-newton-probe",
        action="store_true",
        help="run synthetic opt-in cylinder scoring-policy Newton contact/task probe",
    )
    parser.add_argument(
        "--run-cpd-like-controlled-merge-search-package-probe",
        action="store_true",
        help="run synthetic opt-in controlled merge-search package probe",
    )
    parser.add_argument(
        "--run-cpd-like-controlled-merge-search-newton-probe",
        action="store_true",
        help="run synthetic controlled merge-search Newton contact/task probe",
    )
    parser.add_argument(
        "--run-cpd-like-cost-guided-lookahead-merge-report",
        action="store_true",
        help="run synthetic two-step lookahead merge-search diagnostic report",
    )
    parser.add_argument(
        "--run-cpd-like-cost-guided-lookahead-package-probe",
        action="store_true",
        help="run synthetic two-step lookahead package/mapping probe",
    )
    parser.add_argument(
        "--run-cpd-like-cost-guided-lookahead-newton-probe",
        action="store_true",
        help="run synthetic two-step lookahead Newton contact/task probe",
    )
    parser.add_argument(
        "--run-cpd-like-four-block-slice-report",
        action="store_true",
        help="emit a command-only four-block report for a recorded synthetic slice",
    )
    parser.add_argument(
        "--run-cpd-paper-offline-report",
        action="store_true",
        help="run fixture-scoped offline CPD paper mechanics audit",
    )
    parser.add_argument(
        "--run-newton-native-fitting-comparison",
        action="store_true",
        help=(
            "run offline synthetic comparison between legacy and six-kind "
            "Newton-native primitive fitting"
        ),
    )
    parser.add_argument(
        "--run-real-usd-native-fitting-comparison",
        action="store_true",
        help="run real-USD old/new Newton-native primitive fitting comparison",
    )
    parser.add_argument(
        "--run-real-usd-candidate-loss-diagnosis",
        action="store_true",
        help="run real-USD per-cluster candidate-loss diagnosis for native primitive lanes",
    )
    parser.add_argument(
        "--run-real-usd-native-contact-comparison",
        action="store_true",
        help="run real-USD old/new Newton contact-canary comparison",
    )
    parser.add_argument(
        "--run-real-usd-native-task-comparison",
        action="store_true",
        help="run gated real-USD old/new Newton drop/settle and sphere-rain comparison",
    )
    parser.add_argument(
        "--run-newton-contact-smoke",
        action="store_true",
        help="run CPD-like geometry plus the Newton contact-only canary smoke",
    )
    parser.add_argument(
        "--run-newton-drop-settle",
        action="store_true",
        help="run CPD-like geometry plus the Newton drop/settle task smoke",
    )
    parser.add_argument(
        "--run-newton-sphere-rain",
        action="store_true",
        help="run CPD-like geometry plus the Newton sphere-rain contact-density proxy smoke",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    argv = sys.argv[1:] if argv is None else argv
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        if exc.code == 0:
            return 0
        raise

    if not argv:
        parser.print_help()
        return 0

    if args.check_newton and args.config:
        try:
            config = load_compile_config(args.config)
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2

        newton_section = config.protocol.get("newton", {})
        source_dir = newton_section.get("source_dir") if isinstance(newton_section, dict) else None
        if not source_dir:
            print("npc-compile: --check-newton requires config key newton.source_dir.", file=sys.stderr)
            return 2
        source_dir = _expand_env_path(str(source_dir), "newton.source_dir")

        report = inspect_newton_environment(source_dir)
        print(json.dumps(report.to_dict(), sort_keys=True))
        return 2 if report.status == "missing_source" else 0

    if args.check_newton:
        print("npc-compile: --check-newton requires --config.", file=sys.stderr)
        return 2

    if args.check_assets and args.config:
        try:
            config = load_compile_config(args.config)
            assets = load_asset_manifest(_asset_manifest_path(config))
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2

        reports = [inspect_usd_asset(asset) for asset in assets]
        status = (
            "smoke_passed"
            if reports and all(report.status == "smoke_passed" for report in reports)
            else "smoke_failed"
        )
        print(
            json.dumps(
                {
                    "stage": "asset_usd_open",
                    "status": status,
                    "reports": [report.to_dict() for report in reports],
                },
                sort_keys=True,
            )
        )
        return 0 if status == "smoke_passed" else 2

    if args.check_assets:
        print("npc-compile: --check-assets requires --config.", file=sys.stderr)
        return 2

    if args.materialize_assets and args.config:
        try:
            config = load_compile_config(args.config)
            with contextlib.redirect_stdout(sys.stderr):
                report = build_asset_materialization_report(_asset_manifest_path(config))
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2

        print(json.dumps(report, sort_keys=True))
        return 2 if report["status"] == "failed" else 0

    if args.materialize_assets:
        print("npc-compile: --materialize-assets requires --config.", file=sys.stderr)
        return 2

    if args.run_cpd_like and args.config:
        try:
            config = load_compile_config(args.config)
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2

        cpd_like_section = config.protocol.get("cpd_like", {})
        if not isinstance(cpd_like_section, dict):
            cpd_like_section = {}
        try:
            primitive_subset = _cpd_like_primitive_subset(cpd_like_section)
            component_merge_options = _cpd_like_component_merge_options(cpd_like_section)
            max_source_faces = _positive_int(cpd_like_section.get("max_source_faces"), default=256)
            source_path = _cpd_like_source_path(config, cpd_like_section)
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2
        try:
            mesh = load_first_mesh(source_path, max_faces=max_source_faces)
            report = decompose_mesh(
                mesh,
                max_primitives=config.max_primitives,
                primitive_subset=primitive_subset,
                **component_merge_options,
            )
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": _cpd_like_stage(component_merge_options["component_merge"]),
                        "status": "dependency_gap"
                        if "dependency_gap" in str(exc)
                        else "smoke_failed",
                        "asset_id": config.asset_id or Path(config.asset_path).stem,
                        "source_path": source_path,
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2

        payload = report.to_dict()
        payload["asset_id"] = config.asset_id or Path(config.asset_path).stem
        payload["source_path"] = source_path
        payload["claim_boundary"] = cpd_like_section.get(
            "claim_boundary",
            "internal_baseline_not_reproduction_claim",
        )
        print(json.dumps(payload, sort_keys=True))
        return 0 if report.status == "smoke_passed" else 2

    if args.run_cpd_like:
        print("npc-compile: --run-cpd-like requires --config.", file=sys.stderr)
        return 2

    if args.run_cpd_like_objective_report and args.config:
        try:
            config = load_compile_config(args.config)
            objective_section = config.protocol.get("cpd_like_objective", {})
            if objective_section is None:
                objective_section = {}
            if not isinstance(objective_section, dict):
                raise ValueError("cpd_like_objective must be a mapping")
            objective_options = _cpd_like_objective_options(objective_section)
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2

        try:
            cpd_like_report, source_path, max_source_faces = _run_cpd_like_report(config)
            report = build_cpd_like_objective_report(
                cpd_like_report,
                asset_id=config.asset_id or Path(config.asset_path).stem,
                source_path=source_path,
                max_source_faces=max_source_faces,
                options=objective_options,
            )
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": "cpd_like_offline_objective",
                        "status": "dependency_gap"
                        if "dependency_gap" in str(exc)
                        else "smoke_failed",
                        "asset_id": config.asset_id or Path(config.asset_path).stem,
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2

        try:
            print(json.dumps(report.to_dict(), sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                f"npc-compile: cpd_like_objective report contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report.status == "smoke_passed" else 2

    if args.run_cpd_like_objective_report:
        print("npc-compile: --run-cpd-like-objective-report requires --config.", file=sys.stderr)
        return 2

    if args.run_cpd_like_synthetic_comparison:
        report = build_cpd_like_synthetic_comparison_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_synthetic_comparison report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cost_guided_synthetic_comparison:
        report = build_cpd_like_cost_guided_synthetic_comparison_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cost_guided_synthetic_comparison report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cost_guided_lookahead_merge_report:
        report = build_cpd_like_cost_guided_lookahead_merge_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cost_guided_lookahead_merge_report "
                f"contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cost_guided_lookahead_package_probe:
        report = build_cpd_like_cost_guided_lookahead_package_probe_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cost_guided_lookahead_package_probe "
                f"contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_four_block_slice_report:
        report = build_cpd_like_four_block_slice_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_four_block_slice_report "
                f"contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_paper_offline_report:
        report = build_cpd_paper_offline_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_paper_offline_report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["report_generation_status"] == "smoke_passed" else 2

    if args.run_cpd_like_expected_failure_workbench:
        report = build_cpd_like_expected_failure_synthetic_workbench_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_expected_failure_workbench report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_near_miss_workbench:
        report = build_cpd_like_near_miss_workbench_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_near_miss_workbench report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cylinder_near_miss_fit_ablation:
        report = build_cpd_like_cylinder_near_miss_fit_ablation_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cylinder_near_miss_fit_ablation report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cylinder_near_miss_scoring_sensitivity:
        report = build_cpd_like_cylinder_near_miss_scoring_sensitivity_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cylinder_near_miss_scoring_sensitivity "
                f"report contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cylinder_near_miss_scoring_policy_ablation:
        report = build_cpd_like_cylinder_near_miss_scoring_policy_ablation_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cylinder_near_miss_scoring_policy_ablation "
                f"report contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cylinder_scoring_policy_selection_probe:
        report = build_cpd_like_cylinder_scoring_policy_selection_probe_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cylinder_scoring_policy_selection_probe "
                f"report contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cylinder_scoring_policy_package_probe:
        report = build_cpd_like_cylinder_scoring_policy_package_probe_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cylinder_scoring_policy_package_probe "
                f"report contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_controlled_merge_search_package_probe:
        report = build_cpd_like_controlled_merge_search_package_probe_report()
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_controlled_merge_search_package_probe "
                f"report contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_controlled_merge_search_newton_probe and args.config:
        try:
            config = load_compile_config(args.config)
            _validate_controlled_merge_search_newton_probe_config(config)
            newton_section = config.protocol.get("newton", {})
            if not isinstance(newton_section, dict):
                newton_section = {}
            source_dir = newton_section.get("source_dir")
            if not source_dir:
                raise ValueError(
                    "--run-cpd-like-controlled-merge-search-newton-probe requires "
                    "config key newton.source_dir"
                )
            source_dir = _expand_env_path(str(source_dir), "newton.source_dir")
            diagnostic_section = config.protocol.get("newton_diagnostic", {})
            if not isinstance(diagnostic_section, dict):
                diagnostic_section = {}
            device = str(diagnostic_section.get("device", "cpu"))
            top_claim_boundary = str(
                diagnostic_section.get(
                    "synthetic_newton_probe_claim_boundary",
                    (
                        "synthetic_controlled_merge_search_newton_probe_not_"
                        "collision_quality_or_merge_superiority"
                    ),
                )
            )
            contact_claim_boundary = str(
                diagnostic_section.get(
                    "contact_claim_boundary",
                    "synthetic_controlled_merge_search_contact_canary_not_collision_quality",
                )
            )
            task_claim_boundary = str(
                diagnostic_section.get(
                    "claim_boundary",
                    (
                        "synthetic_controlled_merge_search_task_smoke_not_"
                        "collision_quality_or_merge_superiority"
                    ),
                )
            )
            drop_options = _newton_drop_settle_options(
                {**diagnostic_section, "probe_type": "drop_settle"}
            )["options"]
            sphere_options = _newton_sphere_rain_options(
                {**diagnostic_section, "probe_type": "sphere_rain"}
            )["options"]
            with contextlib.redirect_stdout(sys.stderr):
                report = build_cpd_like_controlled_merge_search_newton_probe_report(
                    source_dir=source_dir,
                    device=device,
                    drop_settle_options=drop_options,
                    sphere_rain_options=sphere_options,
                    claim_boundary=top_claim_boundary,
                    contact_claim_boundary=contact_claim_boundary,
                    task_claim_boundary=task_claim_boundary,
                )
        except ValueError as exc:
            print(
                json.dumps(
                    {
                        "stage": "cpd_like_controlled_merge_search_newton_probe",
                        "status": _controlled_merge_search_newton_probe_error_status(
                            str(exc)
                        ),
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_controlled_merge_search_newton_probe "
                f"report contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cost_guided_lookahead_newton_probe and args.config:
        try:
            config = load_compile_config(args.config)
            _validate_cost_guided_lookahead_newton_probe_config(config)
            newton_section = config.protocol.get("newton", {})
            if not isinstance(newton_section, dict):
                newton_section = {}
            source_dir = newton_section.get("source_dir")
            if not source_dir:
                raise ValueError(
                    "--run-cpd-like-cost-guided-lookahead-newton-probe requires "
                    "config key newton.source_dir"
                )
            source_dir = _expand_env_path(str(source_dir), "newton.source_dir")
            diagnostic_section = config.protocol.get("newton_diagnostic", {})
            if not isinstance(diagnostic_section, dict):
                diagnostic_section = {}
            device = str(diagnostic_section.get("device", "cpu"))
            top_claim_boundary = str(
                diagnostic_section.get(
                    "synthetic_newton_probe_claim_boundary",
                    (
                        "synthetic_cost_guided_lookahead_newton_probe_not_"
                        "quality_or_policy_ranking"
                    ),
                )
            )
            contact_claim_boundary = str(
                diagnostic_section.get(
                    "contact_claim_boundary",
                    "synthetic_cost_guided_lookahead_contact_canary_not_quality",
                )
            )
            task_claim_boundary = str(
                diagnostic_section.get(
                    "claim_boundary",
                    (
                        "synthetic_cost_guided_lookahead_task_smoke_not_"
                        "quality_or_policy_ranking"
                    ),
                )
            )
            drop_options = _newton_drop_settle_options(
                {**diagnostic_section, "probe_type": "drop_settle"}
            )["options"]
            sphere_options = _newton_sphere_rain_options(
                {**diagnostic_section, "probe_type": "sphere_rain"}
            )["options"]
            with contextlib.redirect_stdout(sys.stderr):
                report = build_cpd_like_cost_guided_lookahead_newton_probe_report(
                    source_dir=source_dir,
                    device=device,
                    drop_settle_options=drop_options,
                    sphere_rain_options=sphere_options,
                    claim_boundary=top_claim_boundary,
                    contact_claim_boundary=contact_claim_boundary,
                    task_claim_boundary=task_claim_boundary,
                )
        except ValueError as exc:
            print(
                json.dumps(
                    {
                        "stage": "cpd_like_cost_guided_lookahead_newton_probe",
                        "status": _cost_guided_lookahead_newton_probe_error_status(
                            str(exc)
                        ),
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cost_guided_lookahead_newton_probe "
                f"report contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cylinder_scoring_policy_newton_probe and args.config:
        try:
            config = load_compile_config(args.config)
            _validate_cylinder_scoring_policy_newton_probe_config(config)
            newton_section = config.protocol.get("newton", {})
            if not isinstance(newton_section, dict):
                newton_section = {}
            source_dir = newton_section.get("source_dir")
            if not source_dir:
                raise ValueError(
                    "--run-cpd-like-cylinder-scoring-policy-newton-probe requires "
                    "config key newton.source_dir"
                )
            source_dir = _expand_env_path(str(source_dir), "newton.source_dir")
            diagnostic_section = config.protocol.get("newton_diagnostic", {})
            if not isinstance(diagnostic_section, dict):
                diagnostic_section = {}
            device = str(diagnostic_section.get("device", "cpu"))
            top_claim_boundary = str(
                diagnostic_section.get(
                    "synthetic_newton_probe_claim_boundary",
                    "synthetic_cylinder_scoring_policy_newton_probe_not_collision_quality_or_real_usd",
                )
            )
            contact_claim_boundary = str(
                diagnostic_section.get(
                    "contact_claim_boundary",
                    "synthetic_cylinder_scoring_policy_contact_canary_not_collision_quality",
                )
            )
            task_claim_boundary = str(
                diagnostic_section.get(
                    "claim_boundary",
                    "synthetic_cylinder_scoring_policy_task_smoke_not_collision_quality_or_safety",
                )
            )
            drop_options = _newton_drop_settle_options(
                {**diagnostic_section, "probe_type": "drop_settle"}
            )["options"]
            sphere_options = _newton_sphere_rain_options(
                {**diagnostic_section, "probe_type": "sphere_rain"}
            )["options"]
            with contextlib.redirect_stdout(sys.stderr):
                report = build_cpd_like_cylinder_scoring_policy_newton_probe_report(
                    source_dir=source_dir,
                    device=device,
                    drop_settle_options=drop_options,
                    sphere_rain_options=sphere_options,
                    claim_boundary=top_claim_boundary,
                    contact_claim_boundary=contact_claim_boundary,
                    task_claim_boundary=task_claim_boundary,
                )
        except ValueError as exc:
            print(
                json.dumps(
                    {
                        "stage": "cpd_like_cylinder_scoring_policy_newton_probe",
                        "status": _cylinder_scoring_policy_newton_probe_error_status(
                            str(exc)
                        ),
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: cpd_like_cylinder_scoring_policy_newton_probe "
                f"report contains non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_cpd_like_cylinder_scoring_policy_newton_probe:
        print(
            "npc-compile: --run-cpd-like-cylinder-scoring-policy-newton-probe requires --config.",
            file=sys.stderr,
        )
        return 2

    if args.run_cpd_like_controlled_merge_search_newton_probe:
        print(
            "npc-compile: --run-cpd-like-controlled-merge-search-newton-probe requires --config.",
            file=sys.stderr,
        )
        return 2

    if args.run_cpd_like_cost_guided_lookahead_newton_probe:
        print(
            "npc-compile: --run-cpd-like-cost-guided-lookahead-newton-probe requires --config.",
            file=sys.stderr,
        )
        return 2

    if args.run_newton_native_fitting_comparison:
        try:
            report = _run_newton_native_fitting_comparison(args.config)
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: newton_native_fitting_comparison report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_real_usd_native_fitting_comparison and args.config:
        try:
            report = _run_real_usd_native_fitting_comparison(args.config)
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": "cpd_like_real_usd_native_fitting_comparison",
                        "status": "dependency_gap"
                        if "dependency_gap" in str(exc)
                        else "smoke_failed",
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: real_usd_native_fitting_comparison report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_real_usd_native_fitting_comparison:
        print(
            "npc-compile: --run-real-usd-native-fitting-comparison requires --config.",
            file=sys.stderr,
        )
        return 2

    if args.run_real_usd_candidate_loss_diagnosis and args.config:
        try:
            report = _run_real_usd_candidate_loss_diagnosis(args.config)
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": "cpd_like_real_usd_candidate_loss_diagnosis",
                        "status": "dependency_gap"
                        if "dependency_gap" in str(exc)
                        else "smoke_failed",
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: real_usd_candidate_loss_diagnosis report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_real_usd_candidate_loss_diagnosis:
        print(
            "npc-compile: --run-real-usd-candidate-loss-diagnosis requires --config.",
            file=sys.stderr,
        )
        return 2

    if args.run_real_usd_native_contact_comparison and args.config:
        try:
            config = load_compile_config(args.config)
            options = _real_usd_native_comparison_options(config)
            newton_section = config.protocol.get("newton", {})
            if not isinstance(newton_section, dict):
                newton_section = {}
            source_dir = newton_section.get("source_dir")
            if not source_dir:
                raise ValueError(
                    "--run-real-usd-native-contact-comparison requires config key newton.source_dir"
                )
            source_dir = _expand_env_path(str(source_dir), "newton.source_dir")
            diagnostic_section = config.protocol.get("newton_diagnostic", {})
            if not isinstance(diagnostic_section, dict):
                diagnostic_section = {}
            diagnostic_options = _newton_diagnostic_options(diagnostic_section)
            with contextlib.redirect_stdout(sys.stderr):
                report = build_real_usd_native_contact_comparison_report(
                    **options,
                    source_dir=source_dir,
                    device=diagnostic_options["device"],
                    claim_boundary=diagnostic_options["claim_boundary"],
                )
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": "newton_real_usd_native_contact_comparison",
                        "status": _newton_contact_error_status(str(exc)),
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: real_usd_native_contact_comparison report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_real_usd_native_contact_comparison:
        print(
            "npc-compile: --run-real-usd-native-contact-comparison requires --config.",
            file=sys.stderr,
        )
        return 2

    if args.run_real_usd_native_task_comparison and args.config:
        try:
            config = load_compile_config(args.config)
            options = _real_usd_native_comparison_options(config)
            newton_section = config.protocol.get("newton", {})
            if not isinstance(newton_section, dict):
                newton_section = {}
            source_dir = newton_section.get("source_dir")
            if not source_dir:
                raise ValueError(
                    "--run-real-usd-native-task-comparison requires config key newton.source_dir"
                )
            source_dir = _expand_env_path(str(source_dir), "newton.source_dir")
            diagnostic_section = config.protocol.get("newton_diagnostic", {})
            if not isinstance(diagnostic_section, dict):
                diagnostic_section = {}
            device = str(diagnostic_section.get("device", "cpu"))
            task_claim_boundary = str(
                diagnostic_section.get(
                    "claim_boundary",
                    "real_usd_native_task_smoke_not_collision_quality_or_safety",
                )
            )
            drop_options = _newton_drop_settle_options(
                {**diagnostic_section, "probe_type": "drop_settle"}
            )["options"]
            sphere_options = _newton_sphere_rain_options(
                {**diagnostic_section, "probe_type": "sphere_rain"}
            )["options"]
            with contextlib.redirect_stdout(sys.stderr):
                report = build_real_usd_native_task_comparison_report(
                    **options,
                    source_dir=source_dir,
                    device=device,
                    drop_settle_options=drop_options,
                    sphere_rain_options=sphere_options,
                    claim_boundary=task_claim_boundary,
                    contact_claim_boundary=task_claim_boundary,
                )
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": "newton_real_usd_native_task_comparison",
                        "status": _newton_sphere_rain_error_status(str(exc)),
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2
        try:
            print(json.dumps(report, sort_keys=True, allow_nan=False))
        except ValueError as exc:
            print(
                "npc-compile: real_usd_native_task_comparison report contains "
                f"non-finite JSON values: {exc}",
                file=sys.stderr,
            )
            return 2
        return 0 if report["status"] == "smoke_passed" else 2

    if args.run_real_usd_native_task_comparison:
        print(
            "npc-compile: --run-real-usd-native-task-comparison requires --config.",
            file=sys.stderr,
        )
        return 2

    if args.run_newton_contact_smoke and args.config:
        try:
            config = load_compile_config(args.config)
            cpd_like_section = config.protocol.get("cpd_like", {})
            if not isinstance(cpd_like_section, dict):
                cpd_like_section = {}
            newton_section = config.protocol.get("newton", {})
            if not isinstance(newton_section, dict):
                newton_section = {}
            source_dir = newton_section.get("source_dir")
            if not source_dir:
                raise ValueError("--run-newton-contact-smoke requires config key newton.source_dir")
            source_dir = _expand_env_path(str(source_dir), "newton.source_dir")
            diagnostic_section = config.protocol.get("newton_diagnostic", {})
            if not isinstance(diagnostic_section, dict):
                diagnostic_section = {}
            diagnostic_options = _newton_diagnostic_options(diagnostic_section)
            cpd_like_report, source_path, max_source_faces = _run_cpd_like_report(config)
            package = package_from_cpd_like_report(
                cpd_like_report,
                asset_id=config.asset_id or Path(config.asset_path).stem,
                source_path=source_path,
                claim_boundary=cpd_like_section.get(
                    "claim_boundary",
                    "internal_baseline_not_reproduction_claim",
                ),
                max_source_faces=max_source_faces,
            )
            with contextlib.redirect_stdout(sys.stderr):
                report = run_newton_contact_smoke(
                    package,
                    source_dir=source_dir,
                    device=diagnostic_options["device"],
                    claim_boundary=diagnostic_options["claim_boundary"],
                )
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": "newton_contact_smoke",
                        "status": _newton_contact_error_status(str(exc)),
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2

        print(json.dumps(report.to_dict(), sort_keys=True))
        return 0 if report.status == "smoke_passed" else 2

    if args.run_newton_contact_smoke:
        print("npc-compile: --run-newton-contact-smoke requires --config.", file=sys.stderr)
        return 2

    if args.run_newton_drop_settle and args.config:
        try:
            config = load_compile_config(args.config)
            cpd_like_section = config.protocol.get("cpd_like", {})
            if not isinstance(cpd_like_section, dict):
                cpd_like_section = {}
            newton_section = config.protocol.get("newton", {})
            if not isinstance(newton_section, dict):
                newton_section = {}
            source_dir = newton_section.get("source_dir")
            if not source_dir:
                raise ValueError("--run-newton-drop-settle requires config key newton.source_dir")
            source_dir = _expand_env_path(str(source_dir), "newton.source_dir")
            diagnostic_section = config.protocol.get("newton_diagnostic", {})
            if not isinstance(diagnostic_section, dict):
                diagnostic_section = {}
            diagnostic_options = _newton_drop_settle_options(diagnostic_section)
            cpd_like_report, source_path, max_source_faces = _run_cpd_like_report(config)
            package = package_from_cpd_like_report(
                cpd_like_report,
                asset_id=config.asset_id or Path(config.asset_path).stem,
                source_path=source_path,
                claim_boundary=cpd_like_section.get(
                    "claim_boundary",
                    "internal_baseline_not_reproduction_claim",
                ),
                max_source_faces=max_source_faces,
            )
            with contextlib.redirect_stdout(sys.stderr):
                report = run_newton_drop_settle(
                    package,
                    source_dir=source_dir,
                    device=diagnostic_options["device"],
                    options=diagnostic_options["options"],
                    claim_boundary=diagnostic_options["claim_boundary"],
                )
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": "newton_drop_settle",
                        "status": _newton_drop_settle_error_status(str(exc)),
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2

        print(json.dumps(report.to_dict(), sort_keys=True))
        return 0 if report.status == "smoke_passed" else 2

    if args.run_newton_drop_settle:
        print("npc-compile: --run-newton-drop-settle requires --config.", file=sys.stderr)
        return 2

    if args.run_newton_sphere_rain and args.config:
        try:
            config = load_compile_config(args.config)
            cpd_like_section = config.protocol.get("cpd_like", {})
            if not isinstance(cpd_like_section, dict):
                cpd_like_section = {}
            newton_section = config.protocol.get("newton", {})
            if not isinstance(newton_section, dict):
                newton_section = {}
            source_dir = newton_section.get("source_dir")
            if not source_dir:
                raise ValueError("--run-newton-sphere-rain requires config key newton.source_dir")
            source_dir = _expand_env_path(str(source_dir), "newton.source_dir")
            diagnostic_section = config.protocol.get("newton_diagnostic", {})
            if not isinstance(diagnostic_section, dict):
                diagnostic_section = {}
            diagnostic_options = _newton_sphere_rain_options(diagnostic_section)
            cpd_like_report, source_path, max_source_faces = _run_cpd_like_report(config)
            package = package_from_cpd_like_report(
                cpd_like_report,
                asset_id=config.asset_id or Path(config.asset_path).stem,
                source_path=source_path,
                claim_boundary=cpd_like_section.get(
                    "claim_boundary",
                    "internal_baseline_not_reproduction_claim",
                ),
                max_source_faces=max_source_faces,
            )
            with contextlib.redirect_stdout(sys.stderr):
                report = run_newton_sphere_rain(
                    package,
                    source_dir=source_dir,
                    device=diagnostic_options["device"],
                    options=diagnostic_options["options"],
                    claim_boundary=diagnostic_options["claim_boundary"],
                )
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": "newton_sphere_rain",
                        "status": _newton_sphere_rain_error_status(str(exc)),
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2

        print(json.dumps(report.to_dict(), sort_keys=True))
        return 0 if report.status == "smoke_passed" else 2

    if args.run_newton_sphere_rain:
        print("npc-compile: --run-newton-sphere-rain requires --config.", file=sys.stderr)
        return 2

    if args.dry_run and args.config:
        try:
            config = load_compile_config(args.config)
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2

        asset_id = config.asset_id or Path(config.asset_path).stem
        report = CompileReport(
            asset_id=asset_id,
            task=config.task,
            dry_run=True,
            compiled=False,
            method=config.method,
        )
        print(json.dumps(report.to_dict(), sort_keys=True))
        return 0

    if args.dry_run:
        print("npc-compile: --dry-run requires --config.", file=sys.stderr)
        return 2

    print("npc-compile: non-dry-run compilation is not implemented yet.", file=sys.stderr)
    return 2


def _asset_manifest_path(config):
    cpd_like_section = config.protocol.get("cpd_like", {})
    if isinstance(cpd_like_section, dict):
        asset_manifest = cpd_like_section.get("asset_manifest")
        if asset_manifest:
            return str(asset_manifest)
    return config.asset_path


def _run_newton_native_fitting_comparison(config_path):
    if not config_path:
        return build_newton_native_fitting_comparison_report()

    config = load_compile_config(config_path)
    cpd_like_section = config.protocol.get("cpd_like", {})
    if not isinstance(cpd_like_section, dict):
        cpd_like_section = {}
    comparison_section = config.protocol.get("native_fitting_comparison", {})
    if comparison_section is None:
        comparison_section = {}
    if not isinstance(comparison_section, dict):
        raise ValueError("native_fitting_comparison must be a mapping")

    legacy_subset = _cpd_like_named_primitive_subset(
        cpd_like_section,
        "legacy_primitive_subset",
        NEWTON_NATIVE_LEGACY_SUBSET,
    )
    native_subset = _cpd_like_named_primitive_subset(
        cpd_like_section,
        "native_primitive_subset",
        NEWTON_NATIVE_EXTENDED_SUBSET,
    )
    objective_options = CPDLikeObjectiveOptions(
        objective_version=str(
            comparison_section.get(
                "objective_version",
                "cpd_paper_aligned_surrogate_v0",
            )
        ),
        claim_boundary=str(
            comparison_section.get(
                "claim_boundary",
                NEWTON_NATIVE_FITTING_COMPARISON_CLAIM_BOUNDARY,
            )
        ),
        evidence_level=str(
            comparison_section.get(
                "evidence_level",
                NEWTON_NATIVE_FITTING_COMPARISON_EVIDENCE_LEVEL,
            )
        ),
    )
    return build_newton_native_fitting_comparison_report(
        legacy_subset=legacy_subset,
        native_subset=native_subset,
        objective_options=objective_options,
    )


def _run_real_usd_native_fitting_comparison(config_path):
    config = load_compile_config(config_path)
    return build_real_usd_native_fitting_comparison_report(
        **_real_usd_native_comparison_options(config)
    )


def _run_real_usd_candidate_loss_diagnosis(config_path):
    config = load_compile_config(config_path)
    return build_real_usd_candidate_loss_diagnosis_report(
        **_real_usd_candidate_loss_diagnosis_options(config)
    )


def _real_usd_candidate_loss_diagnosis_options(config):
    options = _real_usd_native_comparison_options(config)
    comparison_section = config.protocol.get("candidate_loss_diagnosis", {})
    if comparison_section is None:
        comparison_section = {}
    if not isinstance(comparison_section, dict):
        raise ValueError("candidate_loss_diagnosis must be a mapping")
    options["objective_options"] = CPDLikeObjectiveOptions(
        objective_version=str(
            comparison_section.get(
                "objective_version",
                "cpd_paper_aligned_surrogate_v0",
            )
        ),
        claim_boundary=str(
            comparison_section.get(
                "claim_boundary",
                REAL_USD_CANDIDATE_LOSS_CLAIM_BOUNDARY,
            )
        ),
        evidence_level=str(
            comparison_section.get(
                "evidence_level",
                REAL_USD_CANDIDATE_LOSS_EVIDENCE_LEVEL,
            )
        ),
    )
    return options


def _real_usd_native_comparison_options(config):
    cpd_like_section = config.protocol.get("cpd_like", {})
    if not isinstance(cpd_like_section, dict):
        cpd_like_section = {}
    comparison_section = config.protocol.get("native_fitting_comparison", {})
    if comparison_section is None:
        comparison_section = {}
    if not isinstance(comparison_section, dict):
        raise ValueError("native_fitting_comparison must be a mapping")

    manifest_path = str(cpd_like_section.get("asset_manifest") or config.asset_path)
    roles = _string_tuple_option(
        cpd_like_section.get("asset_roles")
        or comparison_section.get("real_usd_roles"),
        "cpd_like.asset_roles",
    )
    legacy_subset = _cpd_like_named_primitive_subset(
        cpd_like_section,
        "legacy_primitive_subset",
        NEWTON_NATIVE_LEGACY_SUBSET,
    )
    native_subset = _cpd_like_named_primitive_subset(
        cpd_like_section,
        "native_primitive_subset",
        NEWTON_NATIVE_EXTENDED_SUBSET,
    )
    objective_options = CPDLikeObjectiveOptions(
        objective_version=str(
            comparison_section.get(
                "objective_version",
                "cpd_paper_aligned_surrogate_v0",
            )
        ),
        claim_boundary=str(
            comparison_section.get(
                "claim_boundary",
                REAL_USD_NATIVE_FITTING_CLAIM_BOUNDARY,
            )
        ),
        evidence_level=str(
            comparison_section.get(
                "evidence_level",
                REAL_USD_NATIVE_FITTING_EVIDENCE_LEVEL,
            )
        ),
    )
    return {
        "manifest_path": manifest_path,
        "roles": roles,
        "max_primitives": config.max_primitives,
        "legacy_subset": legacy_subset,
        "native_subset": native_subset,
        "max_source_faces_by_role": _max_source_faces_by_role(
            cpd_like_section.get("max_source_faces_by_role")
        ),
        "component_merge_options": _cpd_like_component_merge_options(cpd_like_section),
        "objective_options": objective_options,
        "native_opt_in_score_multipliers": _primitive_score_multipliers_option(
            cpd_like_section.get("native_opt_in_primitive_score_multipliers"),
            "cpd_like.native_opt_in_primitive_score_multipliers",
        ),
        "native_opt_in_selection_guard": _primitive_selection_guard_option(
            cpd_like_section.get("native_opt_in_selection_guard"),
            "cpd_like.native_opt_in_selection_guard",
        ),
        "native_opt_in_support_thresholds": _primitive_selection_support_thresholds_option(
            cpd_like_section.get("native_opt_in_extension_support_thresholds"),
            "cpd_like.native_opt_in_extension_support_thresholds",
        ),
    }


def _run_cpd_like_report(config):
    cpd_like_section = config.protocol.get("cpd_like", {})
    if not isinstance(cpd_like_section, dict):
        cpd_like_section = {}
    primitive_subset = _cpd_like_primitive_subset(cpd_like_section)
    component_merge_options = _cpd_like_component_merge_options(cpd_like_section)
    max_source_faces = _positive_int(cpd_like_section.get("max_source_faces"), default=256)
    source_path = _cpd_like_source_path(config, cpd_like_section)
    mesh = load_first_mesh(source_path, max_faces=max_source_faces)
    report = decompose_mesh(
        mesh,
        max_primitives=config.max_primitives,
        primitive_subset=primitive_subset,
        **component_merge_options,
    )
    return report, source_path, max_source_faces


def _cpd_like_primitive_subset(cpd_like_section):
    return _cpd_like_named_primitive_subset(
        cpd_like_section,
        "primitive_subset",
        ("box", "sphere", "capsule"),
    )


def _cpd_like_named_primitive_subset(cpd_like_section, key, default):
    value = cpd_like_section.get(key, default)
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ValueError(f"cpd_like.{key} must be a list of strings")
    result = tuple(str(item) for item in value)
    if not result or any(not item for item in result):
        raise ValueError(f"cpd_like.{key} must be a list of strings")
    return result


def _string_tuple_option(value, key):
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ValueError(f"{key} must be a list of strings")
    result = tuple(str(item) for item in value)
    if not result or any(not item for item in result):
        raise ValueError(f"{key} must be a list of strings")
    return result


def _max_source_faces_by_role(value):
    if value in (None, ""):
        return {}
    if not isinstance(value, dict):
        raise ValueError("cpd_like.max_source_faces_by_role must be a mapping")
    result = {}
    for role, raw_count in value.items():
        role_name = str(role)
        if not role_name:
            raise ValueError("cpd_like.max_source_faces_by_role keys must be non-empty")
        result[role_name] = _positive_int(
            raw_count,
            default=256,
        )
    return result


def _cpd_like_component_merge_options(cpd_like_section):
    return {
        "component_merge": str(cpd_like_section.get("component_merge", "topology_only")),
        "merge_search_policy": str(
            cpd_like_section.get("merge_search_policy", "topology_then_virtual")
        ),
        "excess_volume_threshold_fraction": _optional_float_value(
            cpd_like_section.get("excess_volume_threshold_fraction"),
            "cpd_like.excess_volume_threshold_fraction",
        ),
        "report_merge_trace": str(cpd_like_section.get("report_merge_trace", "summary")),
    }


def _primitive_score_multipliers_option(value, key):
    if value in (None, ""):
        return None
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be a mapping")
    result = {}
    for primitive_type, raw_multiplier in value.items():
        primitive_name = str(primitive_type)
        if not primitive_name:
            raise ValueError(f"{key} keys must be non-empty")
        multiplier = _float_value(raw_multiplier, key)
        if multiplier <= 0.0:
            raise ValueError(f"{key} values must be finite positive numbers")
        result[primitive_name] = multiplier
    return result


def _primitive_selection_guard_option(value, key):
    try:
        return normalize_primitive_selection_guard(value)
    except ValueError as exc:
        raise ValueError(f"{key}: {exc}") from exc


def _primitive_selection_support_thresholds_option(value, key):
    try:
        return normalize_primitive_selection_support_thresholds(value)
    except ValueError as exc:
        raise ValueError(f"{key}: {exc}") from exc


def _cpd_like_objective_options(objective_section):
    return CPDLikeObjectiveOptions(
        objective_version=str(
            objective_section.get(
                "objective_version",
                "cpd_paper_aligned_surrogate_v0",
            )
        ),
        primitive_type_weights=_primitive_type_weights(
            objective_section.get("primitive_type_weights")
        ),
        claim_boundary=str(
            objective_section.get(
                "claim_boundary",
                "offline_objective_report_not_collision_quality_validation",
            )
        ),
        evidence_level=str(
            objective_section.get(
                "evidence_level",
                "offline_cpd_like_objective_smoke",
            )
        ),
    )


def _primitive_type_weights(value):
    if value in (None, ""):
        return None
    if not isinstance(value, dict):
        raise ValueError("cpd_like_objective.primitive_type_weights must be a mapping")
    result = {}
    for primitive_type, raw_weight in value.items():
        primitive_name = str(primitive_type)
        if not primitive_name:
            raise ValueError("cpd_like_objective.primitive_type_weights keys must be non-empty")
        weight = _float_value(raw_weight, "cpd_like_objective.primitive_type_weights")
        if weight < 0.0:
            raise ValueError(
                "cpd_like_objective.primitive_type_weights values must be finite non-negative numbers"
            )
        result[primitive_name] = weight
    return result


def _cpd_like_stage(component_merge):
    if component_merge == "virtual_pairwise":
        return "cpd_like_component_merge_gate"
    return "cpd_like_face_merge"


def _cpd_like_source_path(config, cpd_like_section):
    asset_role = cpd_like_section.get("asset_role")
    asset_manifest = cpd_like_section.get("asset_manifest")
    if asset_role:
        manifest_path = asset_manifest or config.asset_path
        assets = load_asset_manifest(manifest_path)
        for asset in assets:
            if asset.get("role") == asset_role:
                resolved = resolve_asset_path(asset)
                if not resolved.path:
                    raise ValueError(f"asset role {asset_role!r} has no path")
                return resolved.path
        raise ValueError(f"asset role {asset_role!r} not found in manifest: {manifest_path}")
    return config.asset_path


def _positive_int(value, default):
    if value in (None, ""):
        return default
    try:
        result = int(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError("cpd_like.max_source_faces must be an integer") from exc
    if result < 1:
        raise ValueError("cpd_like.max_source_faces must be at least 1")
    return result


def _newton_diagnostic_options(section):
    probe_type = str(section.get("probe_type", "contact_canary"))
    if probe_type != "contact_canary":
        raise ValueError("newton_diagnostic.probe_type currently supports only contact_canary")
    max_canaries = _int_value(
        section.get("max_canaries_per_type", 1),
        "newton_diagnostic.max_canaries_per_type",
    )
    if max_canaries != 1:
        raise ValueError("newton_diagnostic.max_canaries_per_type currently supports only 1")
    return {
        "device": str(section.get("device", "cpu")),
        "claim_boundary": str(
            section.get(
                "claim_boundary",
                "contact_canary_only_not_collision_quality",
            )
        ),
    }


def _newton_drop_settle_options(section):
    probe_type = str(section.get("probe_type", "drop_settle"))
    if probe_type != "drop_settle":
        raise ValueError("newton_diagnostic.probe_type must be drop_settle for --run-newton-drop-settle")
    drop_section = section.get("drop_settle", {})
    if drop_section is None:
        drop_section = {}
    if not isinstance(drop_section, dict):
        raise ValueError("newton_diagnostic.drop_settle must be a mapping")
    options = DropSettleOptions(
        height_m=_float_value(drop_section.get("height_m", 0.25), "newton_diagnostic.drop_settle.height_m"),
        frames=_int_value(drop_section.get("frames", 360), "newton_diagnostic.drop_settle.frames"),
        substeps=_int_value(drop_section.get("substeps", 8), "newton_diagnostic.drop_settle.substeps"),
        frame_dt_seconds=_float_value(
            drop_section.get("frame_dt_seconds", 1.0 / 60.0),
            "newton_diagnostic.drop_settle.frame_dt_seconds",
        ),
        iterations=_int_value(
            drop_section.get("iterations", 2),
            "newton_diagnostic.drop_settle.iterations",
        ),
        gravity_mps2=_float_value(
            drop_section.get("gravity_mps2", -9.81),
            "newton_diagnostic.drop_settle.gravity_mps2",
        ),
        ground_height_m=_float_value(
            drop_section.get("ground_height_m", 0.0),
            "newton_diagnostic.drop_settle.ground_height_m",
        ),
        friction=_float_value(
            drop_section.get("friction", 0.5),
            "newton_diagnostic.drop_settle.friction",
        ),
        max_floor_breach_m=_float_value(
            drop_section.get("max_floor_breach_m", 0.05),
            "newton_diagnostic.drop_settle.max_floor_breach_m",
        ),
        max_settle_linear_speed_mps=_float_value(
            drop_section.get("max_settle_linear_speed_mps", 0.05),
            "newton_diagnostic.drop_settle.max_settle_linear_speed_mps",
        ),
    )
    return {
        "device": str(section.get("device", "cpu")),
        "claim_boundary": str(section.get("claim_boundary", DROP_SETTLE_CLAIM_BOUNDARY)),
        "options": options,
    }


def _newton_sphere_rain_options(section):
    probe_type = str(section.get("probe_type", "sphere_rain"))
    if probe_type != "sphere_rain":
        raise ValueError("newton_diagnostic.probe_type must be sphere_rain for --run-newton-sphere-rain")
    sphere_rain_section = section.get("sphere_rain", {})
    if sphere_rain_section is None:
        sphere_rain_section = {}
    if not isinstance(sphere_rain_section, dict):
        raise ValueError("newton_diagnostic.sphere_rain must be a mapping")
    options = SphereRainOptions(
        sphere_count_x=_int_value(
            sphere_rain_section.get("sphere_count_x", 3),
            "newton_diagnostic.sphere_rain.sphere_count_x",
        ),
        sphere_count_y=_int_value(
            sphere_rain_section.get("sphere_count_y", 3),
            "newton_diagnostic.sphere_rain.sphere_count_y",
        ),
        sphere_radius_m=_float_value(
            sphere_rain_section.get("sphere_radius_m", 0.5),
            "newton_diagnostic.sphere_rain.sphere_radius_m",
        ),
        spawn_height_m=_float_value(
            sphere_rain_section.get("spawn_height_m", 2.0),
            "newton_diagnostic.sphere_rain.spawn_height_m",
        ),
        grid_spacing_m=_optional_float_value(
            sphere_rain_section.get("grid_spacing_m"),
            "newton_diagnostic.sphere_rain.grid_spacing_m",
        ),
        frames=_int_value(
            sphere_rain_section.get("frames", 240),
            "newton_diagnostic.sphere_rain.frames",
        ),
        substeps=_int_value(
            sphere_rain_section.get("substeps", 4),
            "newton_diagnostic.sphere_rain.substeps",
        ),
        frame_dt_seconds=_float_value(
            sphere_rain_section.get("frame_dt_seconds", 1.0 / 60.0),
            "newton_diagnostic.sphere_rain.frame_dt_seconds",
        ),
        iterations=_int_value(
            sphere_rain_section.get("iterations", 4),
            "newton_diagnostic.sphere_rain.iterations",
        ),
        gravity_mps2=_float_value(
            sphere_rain_section.get("gravity_mps2", -9.81),
            "newton_diagnostic.sphere_rain.gravity_mps2",
        ),
        friction=_float_value(
            sphere_rain_section.get("friction", 0.5),
            "newton_diagnostic.sphere_rain.friction",
        ),
        min_contact_density=_float_value(
            sphere_rain_section.get("min_contact_density", 0.05),
            "newton_diagnostic.sphere_rain.min_contact_density",
        ),
        require_final_contact=_bool_value(
            sphere_rain_section.get("require_final_contact", False),
            "newton_diagnostic.sphere_rain.require_final_contact",
        ),
        rigid_contact_max=_int_value(
            sphere_rain_section.get("rigid_contact_max", 4096),
            "newton_diagnostic.sphere_rain.rigid_contact_max",
        ),
    )
    return {
        "device": str(section.get("device", "cpu")),
        "claim_boundary": str(section.get("claim_boundary", SPHERE_RAIN_CLAIM_BOUNDARY)),
        "options": options,
    }


def _int_value(value, key):
    try:
        result = int(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be an integer") from exc
    return result


def _float_value(value, key):
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be a number") from exc
    if not math.isfinite(result):
        raise ValueError(f"{key} must be finite")
    return result


def _optional_float_value(value, key):
    if value in (None, ""):
        return None
    return _float_value(value, key)


def _bool_value(value, key):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    raise ValueError(f"{key} must be a boolean")


def _newton_contact_error_status(message):
    if (
        "dependency_gap" in message
        or "newton.source_dir" in message
        or "unset environment variable" in message
    ):
        return "dependency_gap"
    return "smoke_failed"


def _newton_drop_settle_error_status(message):
    if (
        "dependency_gap" in message
        or "newton.source_dir" in message
        or "unset environment variable" in message
    ):
        return "dependency_gap"
    return "runtime_failure"


def _newton_sphere_rain_error_status(message):
    if (
        "dependency_gap" in message
        or "newton.source_dir" in message
        or "unset environment variable" in message
    ):
        return "dependency_gap"
    return "runtime_failure"


def _validate_cylinder_scoring_policy_newton_probe_config(config):
    if config.asset_path != "synthetic://cylinder_near_miss_cluster":
        raise ValueError(
            "--run-cpd-like-cylinder-scoring-policy-newton-probe requires "
            "asset.path synthetic://cylinder_near_miss_cluster"
        )
    if config.task != "synthetic_cylinder_scoring_policy_newton_probe":
        raise ValueError(
            "--run-cpd-like-cylinder-scoring-policy-newton-probe requires "
            "task.primary synthetic_cylinder_scoring_policy_newton_probe"
        )
    if "cpd_like_cylinder_scoring_policy_newton_probe" not in config.verify:
        raise ValueError(
            "--run-cpd-like-cylinder-scoring-policy-newton-probe requires "
            "compile.verify to include cpd_like_cylinder_scoring_policy_newton_probe"
        )


def _validate_controlled_merge_search_newton_probe_config(config):
    if config.asset_path != "synthetic://cost_guided_pair_choice":
        raise ValueError(
            "--run-cpd-like-controlled-merge-search-newton-probe requires "
            "asset.path synthetic://cost_guided_pair_choice"
        )
    if config.task != "synthetic_controlled_merge_search_newton_probe":
        raise ValueError(
            "--run-cpd-like-controlled-merge-search-newton-probe requires "
            "task.primary synthetic_controlled_merge_search_newton_probe"
        )
    if "cpd_like_controlled_merge_search_newton_probe" not in config.verify:
        raise ValueError(
            "--run-cpd-like-controlled-merge-search-newton-probe requires "
            "compile.verify to include cpd_like_controlled_merge_search_newton_probe"
        )


def _validate_cost_guided_lookahead_newton_probe_config(config):
    if config.asset_path != "synthetic://lookahead_merge_trap":
        raise ValueError(
            "--run-cpd-like-cost-guided-lookahead-newton-probe requires "
            "asset.path synthetic://lookahead_merge_trap"
        )
    if config.task != "synthetic_cost_guided_lookahead_newton_probe":
        raise ValueError(
            "--run-cpd-like-cost-guided-lookahead-newton-probe requires "
            "task.primary synthetic_cost_guided_lookahead_newton_probe"
        )
    if "cpd_like_cost_guided_lookahead_newton_probe" not in config.verify:
        raise ValueError(
            "--run-cpd-like-cost-guided-lookahead-newton-probe requires "
            "compile.verify to include cpd_like_cost_guided_lookahead_newton_probe"
        )


def _cylinder_scoring_policy_newton_probe_error_status(message):
    if "requires asset.path" in message or "requires task.primary" in message:
        return "config_error"
    if "requires compile.verify" in message:
        return "config_error"
    return _newton_sphere_rain_error_status(message)


def _controlled_merge_search_newton_probe_error_status(message):
    if "requires asset.path" in message or "requires task.primary" in message:
        return "config_error"
    if "requires compile.verify" in message:
        return "config_error"
    return _newton_sphere_rain_error_status(message)


def _cost_guided_lookahead_newton_probe_error_status(message):
    if "requires asset.path" in message or "requires task.primary" in message:
        return "config_error"
    if "requires compile.verify" in message:
        return "config_error"
    return _newton_sphere_rain_error_status(message)


def _expand_env_path(value, key):
    expanded = os.path.expandvars(value)
    if "$" in expanded:
        raise ValueError(f"{key} references an unset environment variable: {value}")
    return expanded


if __name__ == "__main__":
    raise SystemExit(main())
