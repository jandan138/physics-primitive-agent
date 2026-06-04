from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence

from PIL import Image, ImageDraw, ImageFont

from primitive_collision_compiler.paper.fig1_franka_rtx_slots import REPO_ROOT
from primitive_collision_compiler.paper.supplement_newton_rtx_slots import SLOT_TILE_SIZE


TUTORIAL_2D_RENDERER = "deterministic_2d_tutorial_pil"
TUTORIAL_2D_CLAIM_BOUNDARY = (
    "Deterministic 2D supplement tutorial slots are visual exposition only; "
    "not experimental evidence, not benchmark evidence, not deployment readiness, "
    "not whole-robot collision quality, and not safety certification."
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

TEXT = "#172033"
MUTED = "#5e6a78"
BLUE = "#2868a8"
GREEN = "#2e7d59"
RED = "#b94b48"
GOLD = "#a76f1b"
PURPLE = "#6b4fa3"
TEAL = "#247f86"
PAPER = "#f8fafc"
CARD = "#ffffff"
GRID = "#e5ebf3"
STROKE = "#cbd5e1"


@dataclass(frozen=True)
class PanelSpec:
    label: str
    focus: str
    drawer: Callable[[ImageDraw.ImageDraw], None]


@dataclass(frozen=True)
class TutorialSlotSpec:
    figure_id: str
    title: str
    panels: tuple[PanelSpec, ...]
    recipe: str
    source_records: tuple[str, ...]


def generate_supplement_tutorial_2d_slots(
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    figure_ids: Sequence[str] = SUPPLEMENT_2D_TUTORIAL_SLOT_IDS,
) -> list[Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    specs = _slot_specs()
    unknown = [figure_id for figure_id in figure_ids if figure_id not in specs]
    if unknown:
        raise ValueError(f"unknown supplement tutorial 2D slot id: {', '.join(unknown)}")
    outputs: list[Path] = []
    for figure_id in figure_ids:
        spec = specs[figure_id]
        slot_path = out / f"{figure_id}_slot.png"
        image = _compose_slot(spec)
        image.save(slot_path)
        _write_sidecar(spec, slot_path)
        outputs.append(slot_path)
    return outputs


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--figure-id", action="append", dest="figure_id")
    args = parser.parse_args(argv)
    outputs = generate_supplement_tutorial_2d_slots(
        output_dir=args.output_dir,
        figure_ids=tuple(args.figure_id or SUPPLEMENT_2D_TUTORIAL_SLOT_IDS),
    )
    for output in outputs:
        print(output)
    return 0


def _compose_slot(spec: TutorialSlotSpec) -> Image.Image:
    width, height = SLOT_TILE_SIZE
    strip = Image.new("RGB", (width * len(spec.panels), height), "#ffffff")
    for index, panel in enumerate(spec.panels):
        tile = Image.new("RGB", SLOT_TILE_SIZE, PAPER)
        draw = ImageDraw.Draw(tile)
        _draw_grid(draw)
        _rounded(draw, (28, 26, width - 28, height - 26), 26, CARD, STROKE, 2)
        _panel_header(draw, panel.label, panel.focus, _palette(index))
        panel.drawer(draw)
        strip.paste(tile, (index * width, 0))
    return strip


def _write_sidecar(spec: TutorialSlotSpec, slot_path: Path) -> Path:
    sidecar = slot_path.with_suffix(".json")
    payload = {
        "schema_version": 1,
        "figure_id": spec.figure_id,
        "title": spec.title,
        "renderer": TUTORIAL_2D_RENDERER,
        "style": "academic_2d_tutorial",
        "recipe": spec.recipe,
        "slot_asset": _portable_path(slot_path),
        "slot_sha256": _sha256_file(slot_path),
        "slot_composition": {
            "tile_size": list(SLOT_TILE_SIZE),
            "layout": "fixed-width panel strip; each segment is contained by the paper composer",
        },
        "panel_count": len(spec.panels),
        "panels": [
            {"label": panel.label, "focus": panel.focus}
            for panel in spec.panels
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
            panels=(
                PanelSpec("Generator lane", "source support sets become lane-local candidates", _draw_candidate_lane),
                PanelSpec("Package manifest", "candidate rows carry owner, mass, and thresholds", _draw_package_manifest),
                PanelSpec("Diagnostic gate", "same probes assign accept, fallback, or fail labels", _draw_diagnostic_gate),
            ),
            recipe="2d_teaching_diagram_candidate_lane_manifest_gate",
            source_records=("paper/shared/evidence/results_manifest.yaml",),
        ),
        "supplement_generated_package_consumption": TutorialSlotSpec(
            figure_id="supplement_generated_package_consumption",
            title="Generated-package consumption check",
            panels=(
                PanelSpec("Source audit", "original collision shapes are inventoried before insertion", _draw_consumption_source),
                PanelSpec("Generated package", "the package creates the Newton bodies actually checked", _draw_consumption_package),
                PanelSpec("Runtime accounting", "missing bodies, filters, and source remnants are counted", _draw_consumption_accounting),
            ),
            recipe="2d_teaching_diagram_generated_package_consumption",
            source_records=("docs/records/2026-05-26-generated-package-robot-task-probe.md",),
        ),
        "supplement_compound_body_state_teaching": TutorialSlotSpec(
            figure_id="supplement_compound_body_state_teaching",
            title="Compound body-state mechanism",
            panels=(
                PanelSpec("Primitive states", "each primitive has local mass, COM, and inertia terms", _draw_compound_primitives),
                PanelSpec("Aggregate body", "parallel-axis aggregation changes body-level COM and inertia", _draw_compound_aggregate),
                PanelSpec("Gate consequence", "geometry-local plausibility can fail body-state checks", _draw_compound_gate),
            ),
            recipe="2d_teaching_diagram_compound_body_state",
            source_records=("docs/records/2026-05-26-accv-paper-visual-expansion-plan.md",),
        ),
        "supplement_franka_link_frames": TutorialSlotSpec(
            figure_id="supplement_franka_link_frames",
            title="Franka link ownership frames",
            panels=(
                PanelSpec("Link graph", "primitives stay attached to their source Franka link", _draw_link_graph),
                PanelSpec("Attachment table", "owner links map to Newton bodies before probing", _draw_attachment_table),
                PanelSpec("Merge violation", "cross-link primitive merges are rejected structurally", _draw_merge_violation),
            ),
            recipe="2d_teaching_diagram_franka_link_ownership",
            source_records=("docs/records/2026-05-26-link-aware-robot-package-generation.md",),
        ),
        "supplement_franka_source_suppression": TutorialSlotSpec(
            figure_id="supplement_franka_source_suppression",
            title="Source-shape suppression accounting",
            panels=(
                PanelSpec("USD inventory", "source collision prims are counted before rewrite", _draw_suppression_inventory),
                PanelSpec("Layer operation", "source shapes are muted while generated shapes are inserted", _draw_suppression_layer),
                PanelSpec("Audit diff", "remaining-source and generated-body counts must match", _draw_suppression_diff),
            ),
            recipe="2d_teaching_diagram_source_shape_suppression",
            source_records=("docs/records/2026-05-26-generated-package-robot-task-probe.md",),
        ),
        "supplement_provenance_flow": TutorialSlotSpec(
            figure_id="supplement_provenance_flow",
            title="Artifact and provenance flow",
            panels=(
                PanelSpec("Config inputs", "paper-visible settings come from repo-relative configs", _draw_provenance_config),
                PanelSpec("Records", "dated records bind claims to evidence status", _draw_provenance_records),
                PanelSpec("Figure manifest", "slot hashes and sidecars keep generated figures auditable", _draw_provenance_manifest),
                PanelSpec("Supplement PDF", "LaTeX consumes generated figures without raw asset commits", _draw_provenance_pdf),
            ),
            recipe="2d_teaching_diagram_artifact_provenance_flow",
            source_records=("docs/reference/claim-boundaries.md",),
        ),
    }


def _draw_candidate_lane(draw: ImageDraw.ImageDraw) -> None:
    y_values = (190, 330, 470)
    lane_colors = (BLUE, GREEN, GOLD)
    for idx, (y, color) in enumerate(zip(y_values, lane_colors)):
        _tag(draw, (70, y - 32, 170, y + 32), f"lane {idx + 1}", color)
        _arrow(draw, (186, y, 275, y), color)
        for n in range(3):
            x = 300 + n * 72
            _shape_token(draw, (x, y), n, color)
        _arrow(draw, (512, y, 558, y), color)
    _box(draw, (344, 96, 510, 150), "S_i support", BLUE)
    _box(draw, (350, 584, 525, 648), "no global\nwinner yet", RED)
    _bracket(draw, 292, 252, 545, "lane-local candidate set")


def _draw_package_manifest(draw: ImageDraw.ImageDraw) -> None:
    _table(
        draw,
        (68, 172, 552, 532),
        ("prim", "owner", "state", "probe"),
        (
            ("p01", "link3", "m,I,c", "drop"),
            ("p02", "link3", "pose", "stack"),
            ("p07", "link5", "filter", "sphere"),
            ("p09", "link6", "scale", "robot"),
        ),
    )
    _small_box(draw, (118, 574, 238, 638), "package id", PURPLE)
    _small_box(draw, (258, 574, 378, 638), "sha256", TEAL)
    _small_box(draw, (398, 574, 518, 638), "fallback", RED)
    _arrow(draw, (180, 552, 180, 574), MUTED)
    _arrow(draw, (320, 552, 320, 574), MUTED)
    _arrow(draw, (460, 552, 460, 574), MUTED)


def _draw_diagnostic_gate(draw: ImageDraw.ImageDraw) -> None:
    x_mid = 310
    _box(draw, (178, 136, 442, 210), "candidate package", BLUE)
    for idx, (label, color) in enumerate((("drop", BLUE), ("stack", GREEN), ("sphere", GOLD), ("robot", PURPLE))):
        y = 265 + idx * 78
        _box(draw, (92, y, 238, y + 52), label, color)
        _box(draw, (382, y, 528, y + 52), "metric row", color)
        _arrow(draw, (238, y + 26, 382, y + 26), color)
    _arrow(draw, (x_mid, 210, x_mid, 252), MUTED)
    _tag(draw, (175, 614, 295, 672), "ACCEPT", GREEN)
    _tag(draw, (325, 614, 445, 672), "FALLBACK", GOLD)
    _tag(draw, (475, 614, 575, 672), "FAIL", RED)


def _draw_consumption_source(draw: ImageDraw.ImageDraw) -> None:
    _box(draw, (70, 142, 246, 208), "source USD", BLUE)
    for idx, path in enumerate(("/link3/collision", "/link5/collision", "/link6/collision")):
        y = 260 + idx * 82
        _file_row(draw, (86, y, 530, y + 54), path, BLUE)
    _tag(draw, (134, 568, 272, 626), "source count", GOLD)
    _tag(draw, (300, 568, 410, 626), "12", GOLD)
    _arrow(draw, (246, 176, 365, 176), BLUE)
    _box(draw, (374, 142, 540, 208), "inventory", BLUE)


def _draw_consumption_package(draw: ImageDraw.ImageDraw) -> None:
    _box(draw, (68, 142, 226, 206), "manifest", PURPLE)
    _arrow(draw, (226, 174, 330, 174), PURPLE)
    _box(draw, (338, 142, 548, 206), "Newton bodies", PURPLE)
    for idx, (x, y, color) in enumerate(((170, 330, BLUE), (310, 330, GREEN), (450, 330, GOLD), (240, 470, PURPLE), (390, 470, TEAL))):
        _shape_token(draw, (x, y), idx, color)
        draw.line((x, y + 42, x, y + 94), fill=color, width=4)
        _small_box(draw, (x - 48, y + 96, x + 48, y + 146), f"body{idx}", color)
    _bracket(draw, 118, 594, 505, "generated package consumed by probes")


def _draw_consumption_accounting(draw: ImageDraw.ImageDraw) -> None:
    _table(
        draw,
        (72, 140, 552, 480),
        ("check", "value", "gate"),
        (
            ("missing generated bodies", "0", "pass"),
            ("source collisions left", "0", "pass"),
            ("self-collision filters", "66", "record"),
            ("owner-link mismatches", "0", "pass"),
        ),
    )
    _tag(draw, (84, 560, 242, 626), "read probes", BLUE)
    _arrow(draw, (242, 593, 346, 593), BLUE)
    _tag(draw, (350, 560, 536, 626), "only after audit", GREEN)


def _draw_compound_primitives(draw: ImageDraw.ImageDraw) -> None:
    for idx, (center, color, label) in enumerate(((180, BLUE, "p1"), (310, GREEN, "p2"), (440, GOLD, "p3"))):
        _primitive_body(draw, center, 334, idx, color, label)
        _small_box(draw, (center - 54, 496, center + 54, 548), f"m{idx + 1}", color)
    _box(draw, (112, 132, 508, 202), "local terms: m_i, c_i, I_i", PURPLE)
    _bracket(draw, 126, 588, 492, "locally plausible primitives")


def _draw_compound_aggregate(draw: ImageDraw.ImageDraw) -> None:
    _primitive_body(draw, 190, 330, 0, BLUE, "p1")
    _primitive_body(draw, 320, 330, 1, GREEN, "p2")
    _primitive_body(draw, 450, 330, 2, GOLD, "p3")
    _circle(draw, (320, 380), 18, RED)
    draw.line((320, 380, 320, 500), fill=RED, width=4)
    _box(draw, (88, 120, 532, 190), "M = sum_i m_i", BLUE)
    _box(draw, (88, 506, 532, 576), "c = M^-1 sum_i m_i c_i", GREEN)
    _box(draw, (88, 594, 532, 668), "I = sum_i (R I_i R^T + axis term)", GOLD)


def _draw_compound_gate(draw: ImageDraw.ImageDraw) -> None:
    _box(draw, (82, 138, 260, 200), "geometry pass", GREEN)
    _box(draw, (360, 138, 540, 200), "body-state row", BLUE)
    _arrow(draw, (260, 169, 360, 169), MUTED)
    _decision(draw, (220, 304), "COM\ninside?")
    _decision(draw, (420, 304), "I\nstable?")
    _arrow(draw, (285, 304, 355, 304), BLUE)
    _tag(draw, (102, 530, 248, 594), "ACCEPT", GREEN)
    _tag(draw, (372, 530, 530, 594), "BODY FAIL", RED)
    _arrow(draw, (220, 368, 178, 530), GREEN)
    _arrow(draw, (420, 368, 450, 530), RED)


def _draw_link_graph(draw: ImageDraw.ImageDraw) -> None:
    nodes = [(108, 360), (206, 280), (306, 360), (404, 280), (506, 360)]
    names = ("link0", "link2", "link3", "link5", "link7")
    for left, right in zip(nodes, nodes[1:]):
        draw.line((left[0], left[1], right[0], right[1]), fill="#94a3b8", width=8)
    for idx, (point, name) in enumerate(zip(nodes, names)):
        _circle(draw, point, 42, _palette(idx))
        _center_text(draw, name, (point[0] - 50, point[1] - 13, point[0] + 50, point[1] + 13), _font(22, bold=True), "#ffffff")
    _tag(draw, (180, 514, 292, 570), "p07", GREEN)
    _arrow(draw, (236, 514, 306, 402), GREEN)
    _tag(draw, (382, 514, 494, 570), "p11", PURPLE)
    _arrow(draw, (438, 514, 404, 322), PURPLE)


def _draw_attachment_table(draw: ImageDraw.ImageDraw) -> None:
    _table(
        draw,
        (74, 142, 548, 520),
        ("prim", "owner link", "body", "allowed"),
        (
            ("p03", "link2", "body2", "yes"),
            ("p07", "link3", "body3", "yes"),
            ("p11", "link5", "body5", "yes"),
            ("p12", "link7", "body7", "yes"),
        ),
    )
    _small_box(draw, (112, 580, 258, 638), "owner frame", BLUE)
    _arrow(draw, (258, 609, 360, 609), BLUE)
    _small_box(draw, (362, 580, 508, 638), "Newton body", GREEN)


def _draw_merge_violation(draw: ImageDraw.ImageDraw) -> None:
    _circle(draw, (176, 308), 44, BLUE)
    _circle(draw, (444, 308), 44, PURPLE)
    _center_text(draw, "link3", (126, 294, 226, 322), _font(22, bold=True), "#ffffff")
    _center_text(draw, "link5", (394, 294, 494, 322), _font(22, bold=True), "#ffffff")
    _shape_token(draw, (250, 448), 0, BLUE)
    _shape_token(draw, (370, 448), 1, PURPLE)
    draw.line((250, 448, 370, 448), fill=RED, width=10)
    _cross(draw, (310, 448), 42, RED)
    _box(draw, (118, 128, 502, 194), "owner(p_a) != owner(p_b)", RED)
    _tag(draw, (166, 594, 452, 652), "reject cross-link merge", RED)


def _draw_suppression_inventory(draw: ImageDraw.ImageDraw) -> None:
    _box(draw, (72, 132, 260, 196), "source layer", BLUE)
    for idx, item in enumerate(("convexHull", "capsule", "meshProxy", "sphere")):
        y = 248 + idx * 72
        _file_row(draw, (108, y, 510, y + 48), f"/collision/{item}", BLUE if idx < 3 else GOLD)
    _tag(draw, (142, 580, 298, 636), "before: 12", GOLD)
    _tag(draw, (326, 580, 476, 636), "audit list", BLUE)


def _draw_suppression_layer(draw: ImageDraw.ImageDraw) -> None:
    _box(draw, (74, 130, 252, 194), "mute source", RED)
    _box(draw, (370, 130, 548, 194), "insert gen", GREEN)
    for y in (290, 380, 470):
        draw.line((120, y, 500, y), fill="#cbd5e1", width=10)
        _cross(draw, (210, y), 24, RED)
        _circle(draw, (412, y), 18, GREEN)
    _arrow(draw, (252, 162, 370, 162), MUTED)
    _bracket(draw, 112, 574, 510, "one layer operation before probing")


def _draw_suppression_diff(draw: ImageDraw.ImageDraw) -> None:
    _table(
        draw,
        (76, 138, 548, 500),
        ("field", "before", "after"),
        (
            ("source collision prims", "12", "0"),
            ("generated bodies", "0", "12"),
            ("orphan prims", "0", "0"),
            ("local-path leaks", "0", "0"),
        ),
    )
    _tag(draw, (86, 568, 252, 628), "scene OK", GREEN)
    _arrow(draw, (252, 598, 358, 598), GREEN)
    _tag(draw, (360, 568, 540, 628), "read metrics", BLUE)


def _draw_provenance_config(draw: ImageDraw.ImageDraw) -> None:
    _file_stack(
        draw,
        (92, 180),
        ("configs/deepdive", "phase0_baseline", "claims.yaml"),
        BLUE,
    )
    _box(draw, (306, 246, 536, 324), "repo-relative\ninputs only", GREEN)
    _arrow(draw, (248, 284, 306, 284), BLUE)
    _small_box(draw, (118, 560, 500, 626), "no private paths in review artifacts", RED)


def _draw_provenance_records(draw: ImageDraw.ImageDraw) -> None:
    _timeline(draw, (110, 190), ("2026-05-14", "2026-05-26", "2026-06-04"))
    _box(draw, (120, 438, 500, 510), "claim boundary\nupdated with evidence", PURPLE)
    _tag(draw, (164, 584, 456, 642), "diagnostic checker wording", GREEN)


def _draw_provenance_manifest(draw: ImageDraw.ImageDraw) -> None:
    _table(
        draw,
        (74, 138, 548, 482),
        ("artifact", "renderer", "hash"),
        (
            ("slot png", "2D/RTX", "sha"),
            ("sidecar", "json", "sha"),
            ("figure pdf", "PIL", "sha"),
            ("manifest", "json", "sha"),
        ),
    )
    _tag(draw, (120, 560, 300, 624), "portable paths", BLUE)
    _tag(draw, (332, 560, 500, 624), "audit trail", GREEN)


def _draw_provenance_pdf(draw: ImageDraw.ImageDraw) -> None:
    _box(draw, (102, 134, 518, 224), "ACCV supplement.tex", BLUE)
    _arrow(draw, (310, 224, 310, 300), BLUE)
    _box(draw, (122, 300, 498, 430), "generated figures\n+ captions + tables", GREEN)
    _arrow(draw, (310, 430, 310, 512), GREEN)
    _box(draw, (150, 512, 470, 626), "supplement.pdf\n20+ pages", PURPLE)


def _primitive_body(draw: ImageDraw.ImageDraw, x: int, y: int, variant: int, color: str, label: str) -> None:
    _shape_token(draw, (x, y), variant, color)
    _circle(draw, (x + 28, y - 18), 10, RED)
    _center_text(draw, label, (x - 44, y + 44, x + 44, y + 76), _font(23, bold=True), color)


def _draw_grid(draw: ImageDraw.ImageDraw) -> None:
    width, height = SLOT_TILE_SIZE
    for x in range(0, width, 44):
        draw.line((x, 0, x, height), fill=GRID, width=1)
    for y in range(0, height, 44):
        draw.line((0, y, width, y), fill=GRID, width=1)


def _panel_header(draw: ImageDraw.ImageDraw, label: str, focus: str, color: str) -> None:
    _tag(draw, (60, 58, 306, 112), label, color)
    y = 126
    focus_font = _font(21)
    for line in _wrap_pixels(draw, focus, focus_font, 500)[:3]:
        draw.text((64, y), line, font=focus_font, fill=MUTED)
        y += 27


def _table(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    headers: tuple[str, ...],
    rows: tuple[tuple[str, ...], ...],
) -> None:
    _rounded(draw, box, 16, "#ffffff", STROKE, 2)
    x0, y0, x1, y1 = box
    col_w = (x1 - x0) / len(headers)
    row_h = (y1 - y0) / (len(rows) + 1)
    draw.rectangle((x0, y0, x1, int(y0 + row_h)), fill="#e8f0fb", outline=STROKE)
    for idx, header in enumerate(headers):
        _center_text(
            draw,
            header,
            (round(x0 + idx * col_w), y0, round(x0 + (idx + 1) * col_w), round(y0 + row_h)),
            _font(18, bold=True),
            TEXT,
        )
    for row_idx, row in enumerate(rows):
        y = round(y0 + (row_idx + 1) * row_h)
        if row_idx % 2:
            draw.rectangle((x0, y, x1, round(y + row_h)), fill="#f8fafc")
        for col_idx, value in enumerate(row):
            cell = (
                round(x0 + col_idx * col_w),
                y,
                round(x0 + (col_idx + 1) * col_w),
                round(y + row_h),
            )
            _center_text(draw, value, cell, _font(17), TEXT if value != "0" else GREEN)
    for idx in range(1, len(headers)):
        x = round(x0 + idx * col_w)
        draw.line((x, y0, x, y1), fill=STROKE, width=2)
    for idx in range(1, len(rows) + 1):
        y = round(y0 + idx * row_h)
        draw.line((x0, y, x1, y), fill=STROKE, width=2)


def _shape_token(draw: ImageDraw.ImageDraw, center: tuple[int, int], variant: int, color: str) -> None:
    x, y = center
    if variant % 3 == 0:
        _rounded(draw, (x - 38, y - 38, x + 38, y + 38), 14, color, color, 2)
    elif variant % 3 == 1:
        _circle(draw, (x, y), 42, color)
    else:
        points = [(x, y - 46), (x + 48, y + 34), (x - 48, y + 34)]
        draw.polygon(points, fill=color, outline=color)


def _file_row(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, color: str) -> None:
    _rounded(draw, box, 12, "#ffffff", STROKE, 2)
    draw.rectangle((box[0], box[1], box[0] + 14, box[3]), fill=color)
    draw.text((box[0] + 28, box[1] + 14), label, font=_font(19), fill=TEXT)


def _file_stack(draw: ImageDraw.ImageDraw, origin: tuple[int, int], labels: tuple[str, ...], color: str) -> None:
    x, y = origin
    for idx, label in enumerate(labels):
        box = (x + idx * 16, y + idx * 70, x + 250 + idx * 16, y + 54 + idx * 70)
        _file_row(draw, box, label, color if idx % 2 == 0 else GREEN)


def _timeline(draw: ImageDraw.ImageDraw, origin: tuple[int, int], labels: tuple[str, ...]) -> None:
    x0, y = origin
    x1 = x0 + 390
    draw.line((x0, y, x1, y), fill=BLUE, width=6)
    for idx, label in enumerate(labels):
        x = x0 + idx * 195
        _circle(draw, (x, y), 20, _palette(idx))
        _center_text(draw, label, (x - 84, y + 32, x + 84, y + 62), _font(18, bold=True), TEXT)


def _decision(draw: ImageDraw.ImageDraw, center: tuple[int, int], label: str) -> None:
    x, y = center
    points = [(x, y - 64), (x + 72, y), (x, y + 64), (x - 72, y)]
    draw.polygon(points, fill="#fff7e6", outline=GOLD)
    for line_y, line in enumerate(label.split("\n")):
        _center_text(draw, line, (x - 58, y - 25 + line_y * 28, x + 58, y + 2 + line_y * 28), _font(21, bold=True), TEXT)


def _box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, color: str) -> None:
    _rounded(draw, box, 16, _tint(color), color, 3)
    lines = label.split("\n")
    total_height = len(lines) * 26
    y0 = (box[1] + box[3] - total_height) // 2
    for idx, line in enumerate(lines):
        _center_text(draw, line, (box[0] + 8, y0 + idx * 27, box[2] - 8, y0 + idx * 27 + 26), _font(21, bold=True), TEXT)


def _small_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, color: str) -> None:
    _rounded(draw, box, 14, _tint(color), color, 2)
    _center_fit_text(draw, label, box, 19, TEXT)


def _tag(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, color: str) -> None:
    _rounded(draw, box, 18, color, color, 2)
    _center_fit_text(draw, label, box, 20, "#ffffff")


def _bracket(draw: ImageDraw.ImageDraw, left: int, y: int, right: int, label: str) -> None:
    draw.line((left, y, right, y), fill=MUTED, width=4)
    draw.line((left, y - 18, left, y + 18), fill=MUTED, width=4)
    draw.line((right, y - 18, right, y + 18), fill=MUTED, width=4)
    _center_text(draw, label, (left, y + 24, right, y + 58), _font(19), MUTED)


def _arrow(draw: ImageDraw.ImageDraw, line: tuple[int, int, int, int], color: str) -> None:
    x0, y0, x1, y1 = line
    draw.line(line, fill=color, width=5)
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy):
        direction = 1 if dx >= 0 else -1
        points = [(x1, y1), (x1 - direction * 18, y1 - 11), (x1 - direction * 18, y1 + 11)]
    else:
        direction = 1 if dy >= 0 else -1
        points = [(x1, y1), (x1 - 11, y1 - direction * 18), (x1 + 11, y1 - direction * 18)]
    draw.polygon(points, fill=color)


def _circle(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int, color: str) -> None:
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color, outline=color)


def _cross(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int, color: str) -> None:
    x, y = center
    draw.line((x - radius, y - radius, x + radius, y + radius), fill=color, width=8)
    draw.line((x - radius, y + radius, x + radius, y - radius), fill=color, width=8)


def _rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str | None,
    outline: str,
    width: int,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _center_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: str,
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = box[0] + max((box[2] - box[0] - width) // 2, 0)
    y = box[1] + max((box[3] - box[1] - height) // 2, 0)
    draw.text((x, y), text, font=font, fill=fill)


def _center_fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    max_size: int,
    fill: str,
) -> None:
    max_width = max(box[2] - box[0] - 16, 20)
    max_height = max(box[3] - box[1] - 12, 14)
    for size in range(max_size, 10, -1):
        font = _font(size, bold=True)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width and bbox[3] - bbox[1] <= max_height:
            _center_text(draw, text, box, font, fill)
            return
    _center_text(draw, text, box, _font(10, bold=True), fill)


def _wrap_pixels(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in (Path("/usr/share/fonts/truetype/dejavu"), Path("/usr/local/share/fonts")):
        path = base / name
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _palette(index: int) -> str:
    return (BLUE, GREEN, GOLD, PURPLE, TEAL, RED)[index % 6]


def _tint(color: str) -> str:
    tints: Mapping[str, str] = {
        BLUE: "#e8f0fb",
        GREEN: "#e8f5ef",
        RED: "#fbeaea",
        GOLD: "#fff3da",
        PURPLE: "#f0ebfb",
        TEAL: "#e6f4f5",
        MUTED: "#eef2f7",
    }
    return tints.get(color, "#f8fafc")


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
