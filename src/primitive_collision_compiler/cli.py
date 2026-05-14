import argparse
import sys


def build_parser():
    parser = argparse.ArgumentParser(
        prog="npc-compile",
        description="Newton Primitive Collision Compiler",
    )
    parser.add_argument("args", nargs="*", metavar="ARG")
    return parser


def main(argv=None):
    parser = build_parser()
    argv = sys.argv[1:] if argv is None else argv
    args, unknown = parser.parse_known_args(argv)

    if not argv:
        parser.print_help()
        return 0

    if args.args or unknown:
        parser.exit(
            2,
            "npc-compile: operational arguments are not implemented in this bootstrap.\n",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
