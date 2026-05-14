import argparse
import contextlib
import json
import os
import sys
from pathlib import Path

from primitive_collision_compiler.assets.usd_smoke import inspect_usd_asset, load_asset_manifest
from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.package import package_from_cpd_like_report
from primitive_collision_compiler.baselines.cpd_like.usd import USDMeshLoadError, load_first_mesh
from primitive_collision_compiler.config import load_compile_config
from primitive_collision_compiler.contracts import CompileReport
from primitive_collision_compiler.newton.diagnostics import run_newton_contact_smoke
from primitive_collision_compiler.newton.env import inspect_newton_environment


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
        "--run-cpd-like",
        action="store_true",
        help="run the geometry-only CPD-like face-merge smoke path",
    )
    parser.add_argument(
        "--run-newton-contact-smoke",
        action="store_true",
        help="run CPD-like geometry plus the Newton contact-only canary smoke",
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
            )
        except (USDMeshLoadError, ValueError) as exc:
            print(
                json.dumps(
                    {
                        "stage": "cpd_like_face_merge",
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


def _run_cpd_like_report(config):
    cpd_like_section = config.protocol.get("cpd_like", {})
    if not isinstance(cpd_like_section, dict):
        cpd_like_section = {}
    primitive_subset = _cpd_like_primitive_subset(cpd_like_section)
    max_source_faces = _positive_int(cpd_like_section.get("max_source_faces"), default=256)
    source_path = _cpd_like_source_path(config, cpd_like_section)
    mesh = load_first_mesh(source_path, max_faces=max_source_faces)
    report = decompose_mesh(
        mesh,
        max_primitives=config.max_primitives,
        primitive_subset=primitive_subset,
    )
    return report, source_path, max_source_faces


def _cpd_like_primitive_subset(cpd_like_section):
    value = cpd_like_section.get("primitive_subset", ("box", "sphere", "capsule"))
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ValueError("cpd_like.primitive_subset must be a list of strings")
    result = tuple(str(item) for item in value)
    if not result or any(not item for item in result):
        raise ValueError("cpd_like.primitive_subset must be a list of strings")
    return result


def _cpd_like_source_path(config, cpd_like_section):
    asset_role = cpd_like_section.get("asset_role")
    asset_manifest = cpd_like_section.get("asset_manifest")
    if asset_role:
        manifest_path = asset_manifest or config.asset_path
        assets = load_asset_manifest(manifest_path)
        for asset in assets:
            if asset.get("role") == asset_role:
                path = asset.get("path")
                if not path:
                    raise ValueError(f"asset role {asset_role!r} has no path")
                return str(path)
        raise ValueError(f"asset role {asset_role!r} not found in manifest: {manifest_path}")
    return config.asset_path


def _positive_int(value, default):
    if value in (None, ""):
        return default
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
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


def _int_value(value, key):
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be an integer") from exc
    return result


def _newton_contact_error_status(message):
    if (
        "dependency_gap" in message
        or "newton.source_dir" in message
        or "unset environment variable" in message
    ):
        return "dependency_gap"
    return "smoke_failed"


def _expand_env_path(value, key):
    expanded = os.path.expandvars(value)
    if "$" in expanded:
        raise ValueError(f"{key} references an unset environment variable: {value}")
    return expanded


if __name__ == "__main__":
    raise SystemExit(main())
