#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from primitive_collision_compiler.environment.readiness import pick_report_status, run_readiness_check


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emit local Newton environment readiness JSON.")
    parser.add_argument(
        "--output",
        type=Path,
        help="report path; defaults to $NPC_OUTPUT_DIR/environment-readiness.json",
    )
    parser.add_argument(
        "--include-assets",
        action="store_true",
        help="also run configured USD asset smoke diagnostics when possible",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_readiness_check(os.environ, include_assets=args.include_assets)

    output_path = args.output
    if output_path is None and os.environ.get("NPC_OUTPUT_DIR"):
        output_path = Path(os.environ["NPC_OUTPUT_DIR"]) / "environment-readiness.json"
    if output_path is not None:
        output_status = _write_report(output_path, report)
        report["report_output"] = output_status
        report["status"] = pick_report_status([str(report["status"]), str(output_status["status"])])

    payload = json.dumps(report, sort_keys=True)
    print(payload)
    return 0 if report["status"] == "smoke_passed" else 1


def _write_report(output_path: Path, report: dict[str, object]) -> dict[str, object]:
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            {
                **report,
                "report_output": {
                    "status": "smoke_passed",
                    "path": str(output_path),
                    "realpath": str(output_path.resolve()),
                },
            },
            sort_keys=True,
        )
        output_path.write_text(payload + "\n", encoding="utf-8")
    except OSError as exc:
        return {
            "status": "runtime_failure",
            "path": str(output_path),
            "realpath": None,
            "detail": f"{type(exc).__name__}: {exc}",
        }

    return {
        "status": "smoke_passed",
        "path": str(output_path),
        "realpath": str(output_path.resolve()),
    }


if __name__ == "__main__":
    raise SystemExit(main())
