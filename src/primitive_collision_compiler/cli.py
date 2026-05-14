import argparse
import json
import sys
from pathlib import Path

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


if __name__ == "__main__":
    raise SystemExit(main())
