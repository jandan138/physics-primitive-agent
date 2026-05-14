import argparse
import json
import sys
from pathlib import Path

from primitive_collision_compiler.config import load_compile_config
from primitive_collision_compiler.contracts import CompileReport


def build_parser():
    parser = argparse.ArgumentParser(
        prog="npc-compile",
        description="Newton Primitive Collision Compiler",
    )
    parser.add_argument("--config", type=Path, help="path to a compile configuration YAML file")
    parser.add_argument("--dry-run", action="store_true", help="validate config and emit a report")
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
