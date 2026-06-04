from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from primitive_collision_compiler.paper.fig1_franka_rtx_slots import REPO_ROOT


TUTORIAL_2D_RENDERER = "built_in_imagegen_academic_2d_panel_stitch"
TUTORIAL_2D_CLAIM_BOUNDARY_PHRASES = (
    "not experimental evidence",
    "not benchmark evidence",
    "not deployment readiness",
    "not manipulation evidence",
    "not whole-robot collision quality",
    "not safety certification",
)
TUTORIAL_2D_CLAIM_BOUNDARY = (
    "AI-generated 2D supplement tutorial slots are visual exposition only; "
    f"{', '.join(TUTORIAL_2D_CLAIM_BOUNDARY_PHRASES[:-1])}, and "
    f"{TUTORIAL_2D_CLAIM_BOUNDARY_PHRASES[-1]}."
)
SUPPLEMENT_2D_TUTORIAL_SLOT_IDS = (
    "supplement_candidate_lane_anatomy",
    "supplement_generated_package_consumption",
    "supplement_compound_body_state_teaching",
    "supplement_franka_link_frames",
    "supplement_franka_source_suppression",
    "supplement_provenance_flow",
)
DEFAULT_OUTPUT_DIR = REPO_ROOT / "paper/shared/figures/assets/supplement_ai_slots"


@dataclass(frozen=True)
class TutorialSlotSpec:
    figure_id: str
    title: str
    panel_count: int
    segment_bounds_x: tuple[float, ...]
    prompt_summary: str
    imagegen_source: str
    source_records: tuple[str, ...]


def write_supplement_ai_tutorial_sidecars(
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    figure_ids: Sequence[str] = SUPPLEMENT_2D_TUTORIAL_SLOT_IDS,
) -> list[Path]:
    out = Path(output_dir)
    specs = _slot_specs()
    unknown = [figure_id for figure_id in figure_ids if figure_id not in specs]
    if unknown:
        raise ValueError(f"unknown supplement AI tutorial slot id: {', '.join(unknown)}")
    outputs: list[Path] = []
    for figure_id in figure_ids:
        spec = specs[figure_id]
        slot_path = out / f"{figure_id}_slot.png"
        if not slot_path.is_file():
            raise FileNotFoundError(slot_path)
        sidecar = _write_sidecar(spec, slot_path)
        outputs.append(sidecar)
    return outputs


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--figure-id", action="append", dest="figure_id")
    args = parser.parse_args(argv)
    outputs = write_supplement_ai_tutorial_sidecars(
        output_dir=args.output_dir,
        figure_ids=tuple(args.figure_id or SUPPLEMENT_2D_TUTORIAL_SLOT_IDS),
    )
    for output in outputs:
        print(output)
    return 0


def _write_sidecar(spec: TutorialSlotSpec, slot_path: Path) -> Path:
    sidecar = slot_path.with_suffix(".json")
    payload = {
        "schema_version": 1,
        "figure_id": spec.figure_id,
        "title": spec.title,
        "renderer": TUTORIAL_2D_RENDERER,
        "style": "ai_generated_academic_2d_tutorial",
        "recipe": "built_in_imagegen_text_free_panel_strip_selected_by_visual_review",
        "imagegen_source": spec.imagegen_source,
        "prompt_summary": spec.prompt_summary,
        "slot_asset": _portable_path(slot_path),
        "slot_sha256": _sha256_file(slot_path),
        "slot_composition": {
            "layout": "AI-generated wide panel strip; paper composer splits semantic segments and contains each segment",
            "segment_bounds_x": list(spec.segment_bounds_x),
        },
        "panel_count": spec.panel_count,
        "panels": [
            {"index": index + 1, "role": "AI-generated text-free tutorial panel"}
            for index in range(spec.panel_count)
        ],
        "source_records": list(spec.source_records),
        "claim_boundary": TUTORIAL_2D_CLAIM_BOUNDARY,
    }
    sidecar.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sidecar


def _slot_specs() -> dict[str, TutorialSlotSpec]:
    return {
        "supplement_candidate_lane_anatomy": TutorialSlotSpec(
            figure_id="supplement_candidate_lane_anatomy",
            title="Candidate-lane anatomy",
            panel_count=3,
            segment_bounds_x=(0.0, 0.3547, 0.6757, 1.0),
            prompt_summary=(
                "AI-generated text-free academic tutorial strip: candidate lanes, abstract package "
                "manifest, and diagnostic gate outcomes."
            ),
            imagegen_source="built_in_imagegen:ig_0b45743eae151d4e016a212c5fde108197aef0ac2b4daef3d0",
            source_records=("paper/shared/evidence/results_manifest.yaml",),
        ),
        "supplement_generated_package_consumption": TutorialSlotSpec(
            figure_id="supplement_generated_package_consumption",
            title="Generated-package consumption check",
            panel_count=3,
            segment_bounds_x=(0.0, 0.3457, 0.6515, 1.0),
            prompt_summary=(
                "AI-generated text-free academic robotics tutorial strip: source inventory, "
                "generated package replacement, and audit accounting."
            ),
            imagegen_source="built_in_imagegen:ig_0b45743eae151d4e016a212d1dbfa08197bf8769011abfd480",
            source_records=("docs/records/2026-05-26-generated-package-robot-task-probe.md",),
        ),
        "supplement_compound_body_state_teaching": TutorialSlotSpec(
            figure_id="supplement_compound_body_state_teaching",
            title="Compound body-state mechanism",
            panel_count=3,
            segment_bounds_x=(0.0, 0.3524, 0.7038, 1.0),
            prompt_summary=(
                "AI-generated text-free academic tutorial strip: primitive body states, aggregate "
                "body COM/inertia, and diagnostic consequence."
            ),
            imagegen_source="built_in_imagegen:ig_0b45743eae151d4e016a212c9beff081978949fca1a9528fc0",
            source_records=("docs/records/2026-05-26-accv-paper-visual-expansion-plan.md",),
        ),
        "supplement_franka_link_frames": TutorialSlotSpec(
            figure_id="supplement_franka_link_frames",
            title="Franka link ownership frames",
            panel_count=3,
            segment_bounds_x=(0.0, 0.3535, 0.7019, 1.0),
            prompt_summary=(
                "AI-generated text-free academic robotics tutorial strip: link-owned primitives, "
                "body attachment cards, and cross-link merge rejection."
            ),
            imagegen_source="built_in_imagegen:ig_0b45743eae151d4e016a212cd138488197b992c741d10dcb16",
            source_records=("docs/records/2026-05-26-link-aware-robot-package-generation.md",),
        ),
        "supplement_franka_source_suppression": TutorialSlotSpec(
            figure_id="supplement_franka_source_suppression",
            title="Source-shape suppression accounting",
            panel_count=3,
            segment_bounds_x=(0.0, 0.3223, 0.7044, 1.0),
            prompt_summary=(
                "AI-generated text-free academic tutorial strip: source layer inventory, source "
                "shape suppression, and before/after audit diff."
            ),
            imagegen_source="built_in_imagegen:ig_0b45743eae151d4e016a212da5df088197b677a29f33e0fae5",
            source_records=("docs/records/2026-05-26-generated-package-robot-task-probe.md",),
        ),
        "supplement_provenance_flow": TutorialSlotSpec(
            figure_id="supplement_provenance_flow",
            title="Artifact and provenance flow",
            panel_count=4,
            segment_bounds_x=(0.0, 0.2928, 0.5023, 0.7440, 1.0),
            prompt_summary=(
                "AI-generated text-free academic tutorial strip: config inputs, evidence records, "
                "figure manifest provenance, and supplement PDF output."
            ),
            imagegen_source="built_in_imagegen:ig_0b45743eae151d4e016a212deb2c708197b80f60f71b9dd38f",
            source_records=("docs/reference/claim-boundaries.md",),
        ),
    }


def _portable_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return resolved.name


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
