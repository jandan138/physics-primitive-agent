import argparse
import json
import sys
from pathlib import Path

from primitive_collision_compiler.assets.usd_smoke import inspect_usd_asset, load_asset_manifest
from primitive_collision_compiler.baselines.cpd_like.decompose import decompose_mesh
from primitive_collision_compiler.baselines.cpd_like.usd import USDMeshLoadError, load_first_mesh
from primitive_collision_compiler.config import load_compile_config
from primitive_collision_compiler.contracts import CompileReport
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
        except ValueError as exc:
            print(f"npc-compile: {exc}", file=sys.stderr)
            return 2
        try:
            mesh = load_first_mesh(config.asset_path, max_faces=max_source_faces)
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
                        "source_path": config.asset_path,
                        "fallback_reason": str(exc),
                    },
                    sort_keys=True,
                )
            )
            return 2

        payload = report.to_dict()
        payload["asset_id"] = config.asset_id or Path(config.asset_path).stem
        payload["source_path"] = config.asset_path
        payload["claim_boundary"] = cpd_like_section.get(
            "claim_boundary",
            "internal_baseline_not_reproduction_claim",
        )
        print(json.dumps(payload, sort_keys=True))
        return 0 if report.status == "smoke_passed" else 2

    if args.run_cpd_like:
        print("npc-compile: --run-cpd-like requires --config.", file=sys.stderr)
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


def _cpd_like_primitive_subset(cpd_like_section):
    value = cpd_like_section.get("primitive_subset", ("box", "sphere", "capsule"))
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ValueError("cpd_like.primitive_subset must be a list of strings")
    result = tuple(str(item) for item in value)
    if not result or any(not item for item in result):
        raise ValueError("cpd_like.primitive_subset must be a list of strings")
    return result


def _positive_int(value, default):
    if value in (None, ""):
        return default
    result = int(value)
    if result < 1:
        raise ValueError("cpd_like.max_source_faces must be at least 1")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
