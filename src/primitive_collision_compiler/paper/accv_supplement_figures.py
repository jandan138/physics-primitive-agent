from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "paper/shared/figures/generated/supplement"
CANVAS_SIZE = (1800, 1120)
PANEL_FILL = "#ffffff"
PANEL_STROKE = "#ccd5e3"
TEXT = "#172033"
MUTED = "#5e6a78"
BLUE = "#2767a6"
GREEN = "#2e7d59"
RED = "#b94b48"
GOLD = "#a76f1b"
PURPLE = "#6b4fa3"
TEAL = "#247f86"
CLAIM_BOUNDARY = (
    "Supplement tutorial visualization only; not benchmark superiority, not deployment "
    "readiness, not whole-robot collision quality, and not safety certification."
)


@dataclass(frozen=True)
class SupplementFigureSpec:
    figure_id: str
    title: str
    subtitle: str
    kind: str
    panels: tuple[str, ...]
    shows: str
    does_not_show: str
    source_records: tuple[str, ...]
    claim_boundary: str = CLAIM_BOUNDARY


FIGURE_SPECS: tuple[SupplementFigureSpec, ...] = (
    SupplementFigureSpec(
        figure_id="supplement_predicate_drop_settle",
        title="Drop/settle predicate anatomy",
        subtitle="Final speed, floor breach, and descent terms are checked together.",
        kind="drop_settle",
        panels=("initial height", "settle window", "accept terms"),
        shows="How one vertical probe becomes velocity, height, and descent clauses.",
        does_not_show="It does not certify behavior outside the recorded diagnostic scene.",
        source_records=("docs/records/diagnostic-predicate-design.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_predicate_stack_slide",
        title="Stack-or-slide predicate anatomy",
        subtitle="Terminal contact, lateral drift, support height, and speed form the gate.",
        kind="stack_slide",
        panels=("contact", "drift", "residual speed"),
        shows="Why a package can touch the probe yet still fail by sliding away.",
        does_not_show="It is not a manipulation-stability benchmark.",
        source_records=("configs/experiments/phase0_baseline.yaml",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_predicate_sphere_rain",
        title="Sphere-rain contact coverage",
        subtitle="Many lightweight probes reveal missing or overly permissive contact zones.",
        kind="sphere_rain",
        panels=("probe cloud", "contact bins", "diagnostic label"),
        shows="How repeated contact probes turn spatial coverage into a diagnostic symptom.",
        does_not_show="It is not exhaustive geometric coverage of every possible contact.",
        source_records=("docs/records/2026-05-26-phase0-paper-evidence-closure.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_generated_package_consumption",
        title="Generated-package consumption check",
        subtitle="The checker accounts for missing bodies, suppressed source shapes, and filters.",
        kind="package_consumption",
        panels=("source", "generated", "scene accounting"),
        shows="The bookkeeping that makes a package auditable before probe outcomes are read.",
        does_not_show="It is not whole-arm robot performance evidence.",
        source_records=("docs/records/2026-05-26-generated-package-robot-task-probe.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_compound_body_state_teaching",
        title="Compound body-state mechanism",
        subtitle="Local primitive plausibility can diverge from aggregate mass properties.",
        kind="compound",
        panels=("primitive COM", "package COM", "diagnostic gate"),
        shows="How COM and inertia aggregation enter the body-level diagnostic path.",
        does_not_show="It does not claim a general optimal primitive decomposition.",
        source_records=("docs/records/2026-05-26-accv-paper-visual-expansion-plan.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_franka_link_frames",
        title="Franka link ownership frames",
        subtitle="Each primitive keeps the source link owner before simulation consumption.",
        kind="franka_links",
        panels=("link graph", "body attachment", "merge violation"),
        shows="The structural reason cross-link primitive merges are rejected.",
        does_not_show="It is not a whole-robot collision-quality claim.",
        source_records=("docs/records/2026-05-26-link-aware-robot-package-generation.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_franka_source_suppression",
        title="Source-shape suppression accounting",
        subtitle="Generated shapes are inserted while source collision shapes are removed.",
        kind="source_suppression",
        panels=("before", "after", "accounting"),
        shows="Which scene counts must match before the generated package is trusted.",
        does_not_show="It is not deployment readiness for a robot application.",
        source_records=("docs/records/2026-05-26-generated-package-robot-task-probe.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_failure_storyboard_bowl",
        title="Bowl failure storyboard",
        subtitle="Initial state, terminal state, measured symptom, and label are separated.",
        kind="storyboard_bowl",
        panels=("initial", "final", "metric", "label"),
        shows="How a failure label is backed by a measured diagnostic symptom.",
        does_not_show="It is not a new quantitative result table.",
        source_records=("docs/records/2026-05-26-phase0-paper-evidence-closure.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_failure_storyboard_cup_tray",
        title="Cup and tray failure storyboards",
        subtitle="Two assets show different symptoms under the same audit template.",
        kind="storyboard_cup_tray",
        panels=("cup", "tray", "metric", "label"),
        shows="Why failure categories should be read as diagnostic labels, not rankings.",
        does_not_show="It does not compare methods beyond the recorded smoke settings.",
        source_records=("docs/records/2026-05-26-phase0-vhacd-runtime-followup.md",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_candidate_lane_anatomy",
        title="Candidate-lane anatomy",
        subtitle="Each generator lane produces candidates that pass through the same probes.",
        kind="candidate_lane",
        panels=("generator lane", "package", "diagnostic gate"),
        shows="The reviewer-facing path from candidate package to accepted or fallback label.",
        does_not_show="It is not a claim that one lane is broadly superior.",
        source_records=("paper/shared/evidence/results_manifest.yaml",),
    ),
    SupplementFigureSpec(
        figure_id="supplement_provenance_flow",
        title="Artifact and provenance flow",
        subtitle="Configs, records, generated figures, and LaTeX sources remain linked.",
        kind="provenance",
        panels=("config", "record", "manifest", "supplement"),
        shows="How the supplement avoids committing raw assets while preserving audit trails.",
        does_not_show="It is not an external-link dependency for ACCV review.",
        source_records=("docs/reference/claim-boundaries.md",),
    ),
)
SUPPLEMENT_FIGURE_IDS: tuple[str, ...] = tuple(spec.figure_id for spec in FIGURE_SPECS)


def generate_supplement_figures(output_dir: str | Path = DEFAULT_OUTPUT_DIR) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    figures: list[dict[str, Any]] = []
    for spec in FIGURE_SPECS:
        image = _compose_plate(spec)
        png_path = out / f"{spec.figure_id}.png"
        pdf_path = out / f"{spec.figure_id}.pdf"
        image.save(png_path)
        image.save(pdf_path, "PDF", resolution=180.0)
        spec_hash = _sha256_text(_canonical_spec(spec))
        figures.append(
            {
                "figure_id": spec.figure_id,
                "title": spec.title,
                "png": png_path.name,
                "pdf": pdf_path.name,
                "png_sha256": _sha256_file(png_path),
                "pdf_sha256": _sha256_file(pdf_path),
                "source_sha256": spec_hash,
                "source_records": list(spec.source_records),
                "composer": "primitive_collision_compiler.paper.accv_supplement_figures",
                "claim_boundary": spec.claim_boundary,
            }
        )
    manifest_path = out / "manifest.json"
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "manifest_path": str(manifest_path),
        "figure_count": len(figures),
        "figures": figures,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)
    manifest = generate_supplement_figures(output_dir=args.output_dir)
    print(manifest["manifest_path"])
    return 0


def _compose_plate(spec: SupplementFigureSpec) -> Image.Image:
    canvas = Image.new("RGB", CANVAS_SIZE, "#f7f9fc")
    draw = ImageDraw.Draw(canvas)
    _draw_background(draw)
    title_font = _font(54, bold=True)
    subtitle_font = _font(30)
    label_font = _font(25, bold=True)
    body_font = _font(24)
    small_font = _font(20)

    draw.text((78, 58), spec.title, font=title_font, fill=TEXT)
    draw.text((82, 126), spec.subtitle, font=subtitle_font, fill=MUTED)

    panel_boxes = _panel_boxes(len(spec.panels))
    for idx, (label, box) in enumerate(zip(spec.panels, panel_boxes)):
        _rounded(draw, box, 24, PANEL_FILL, PANEL_STROKE, 3)
        draw.text((box[0] + 28, box[1] + 24), label.upper(), font=label_font, fill=_palette(idx))
        _draw_panel_scene(draw, spec.kind, idx, box)

    show_box = (78, 846, 850, 1034)
    limit_box = (950, 846, 1722, 1034)
    _callout(draw, show_box, "What this shows", spec.shows, GREEN, body_font, small_font)
    _callout(draw, limit_box, "What this does not show", spec.does_not_show, RED, body_font, small_font)
    draw.text((78, 1060), spec.claim_boundary, font=small_font, fill="#6b7280")
    return canvas


def _draw_panel_scene(draw: ImageDraw.ImageDraw, kind: str, idx: int, box: tuple[int, int, int, int]) -> None:
    inner = (box[0] + 34, box[1] + 82, box[2] - 34, box[3] - 32)
    getattr(_PanelScenes(draw, inner), f"draw_{kind}")(idx)


class _PanelScenes:
    def __init__(self, draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
        self.draw = draw
        self.box = box
        self.font = _font(22)
        self.bold = _font(22, bold=True)

    def draw_drop_settle(self, idx: int) -> None:
        x0, y0, x1, y1 = self.box
        floor = y1 - 42
        self.draw.line((x0, floor, x1, floor), fill="#2f3946", width=5)
        cx = (x0 + x1) // 2
        if idx == 0:
            self._box((cx - 58, y0 + 38, cx + 58, y0 + 154), BLUE)
            self._arrow((cx, y0 + 174), (cx, floor - 34), RED)
            self.draw.text((x0 + 18, y0 + 18), "z0 > zf", font=self.bold, fill=TEXT)
        elif idx == 1:
            self._box((cx - 66, floor - 116, cx + 66, floor - 10), GREEN)
            self.draw.arc((cx - 92, floor - 150, cx + 92, floor + 34), 200, 340, fill=GREEN, width=6)
            self.draw.text((x0 + 18, y0 + 18), "||vT|| <= eps", font=self.bold, fill=TEXT)
        else:
            self._term_stack(("speed ok", "height ok", "descent ok"), (GREEN, GREEN, GREEN))

    def draw_stack_slide(self, idx: int) -> None:
        x0, y0, x1, y1 = self.box
        platform = (x0 + 60, y1 - 88, x1 - 60, y1 - 44)
        self._box(platform, "#6b7280")
        if idx == 0:
            self._box((x0 + 190, y1 - 190, x0 + 310, y1 - 90), GREEN)
            self.draw.text((x0 + 65, y0 + 30), "terminal contact", font=self.bold, fill=TEXT)
        elif idx == 1:
            self._box((x0 + 120, y1 - 190, x0 + 240, y1 - 90), RED)
            self._box((x0 + 330, y1 - 190, x0 + 450, y1 - 90), "#f5b14c")
            self._arrow((x0 + 248, y1 - 140), (x0 + 322, y1 - 140), RED)
            self.draw.text((x0 + 65, y0 + 30), "xy drift measured", font=self.bold, fill=TEXT)
        else:
            self._term_stack(("contact", "drift <= eps", "speed <= eps"), (GREEN, RED, GREEN))

    def draw_sphere_rain(self, idx: int) -> None:
        x0, y0, x1, y1 = self.box
        bowl = (x0 + 145, y1 - 160, x1 - 145, y1 - 24)
        self.draw.arc(bowl, 0, 180, fill=BLUE, width=8)
        if idx == 0:
            for n in range(20):
                px = x0 + 80 + (n * 37) % (x1 - x0 - 160)
                py = y0 + 32 + (n * 53) % 170
                self.draw.ellipse((px, py, px + 22, py + 22), fill="#9ed1f0", outline=BLUE, width=2)
        elif idx == 1:
            for n in range(8):
                px = x0 + 155 + n * 45
                self.draw.ellipse((px, y1 - 105, px + 26, y1 - 79), fill=GREEN, outline="#1f5e43", width=2)
            for n in range(4):
                px = x0 + 120 + n * 85
                self.draw.ellipse((px, y1 - 205, px + 24, y1 - 181), fill="#f2b8b5", outline=RED, width=2)
        else:
            self._term_stack(("hits counted", "gaps flagged", "label emitted"), (GREEN, GOLD, BLUE))

    def draw_package_consumption(self, idx: int) -> None:
        if idx == 0:
            self._robot_arm(source=True)
            self.draw.text((self.box[0] + 28, self.box[1] + 30), "source collision shapes", font=self.bold, fill=TEXT)
        elif idx == 1:
            self._robot_arm(source=False)
            self.draw.text((self.box[0] + 28, self.box[1] + 30), "generated primitives", font=self.bold, fill=TEXT)
        else:
            self._term_stack(("missing bodies = 0", "source shapes = 0", "filters recorded"), (GREEN, GREEN, BLUE))

    def draw_compound(self, idx: int) -> None:
        x0, y0, x1, y1 = self.box
        centers = ((x0 + 150, y0 + 145), (x0 + 310, y0 + 225), (x0 + 440, y0 + 120))
        colors = (BLUE, GREEN, GOLD)
        for center, color in zip(centers, colors):
            self.draw.ellipse((center[0] - 52, center[1] - 36, center[0] + 52, center[1] + 36), fill="#eef4fb", outline=color, width=5)
        if idx == 0:
            for center in centers:
                self.draw.ellipse((center[0] - 6, center[1] - 6, center[0] + 6, center[1] + 6), fill=RED)
            self.draw.text((x0 + 42, y1 - 68), "local primitive fits", font=self.bold, fill=TEXT)
        elif idx == 1:
            cx, cy = x0 + 305, y0 + 176
            self.draw.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=PURPLE)
            self.draw.line((x0 + 105, cy, x1 - 105, cy), fill=PURPLE, width=3)
            self.draw.text((x0 + 42, y1 - 68), "aggregate COM and inertia", font=self.bold, fill=TEXT)
        else:
            self._term_stack(("local plausible", "body state changed", "probe decides"), (GREEN, GOLD, BLUE))

    def draw_franka_links(self, idx: int) -> None:
        if idx == 0:
            self._link_chain(("base", "link2", "link4", "link6", "hand"))
        elif idx == 1:
            self._robot_arm(source=False)
            self.draw.text((self.box[0] + 36, self.box[1] + 250), "a(pi) = b_li", font=self.bold, fill=TEXT)
        else:
            self._term_stack(("owner link kept", "merge rejected", "sentinel noted"), (GREEN, RED, BLUE))

    def draw_source_suppression(self, idx: int) -> None:
        if idx == 0:
            self._robot_arm(source=True)
            self.draw.text((self.box[0] + 40, self.box[1] + 242), "source USD shapes present", font=self.bold, fill=TEXT)
        elif idx == 1:
            self._robot_arm(source=False)
            self.draw.text((self.box[0] + 40, self.box[1] + 242), "generated package inserted", font=self.bold, fill=TEXT)
        else:
            self._term_stack(("remove source", "insert generated", "count filters"), (RED, GREEN, BLUE))

    def draw_storyboard_bowl(self, idx: int) -> None:
        labels = ("start", "terminal", "metric", "label")
        if idx < 2:
            self._bowl_scene(tilted=idx == 1)
        elif idx == 2:
            self._gauge(0.72, RED, "breach")
        else:
            self._label_card("failure label", RED, "floor breach")
        self.draw.text((self.box[0] + 30, self.box[1] + 22), labels[idx], font=self.bold, fill=TEXT)

    def draw_storyboard_cup_tray(self, idx: int) -> None:
        if idx == 0:
            self._cup_scene()
        elif idx == 1:
            self._tray_scene()
        elif idx == 2:
            self._gauge(0.38, GOLD, "slide")
        else:
            self._label_card("diagnostic label", GOLD, "support lost")

    def draw_candidate_lane(self, idx: int) -> None:
        x0, y0, x1, y1 = self.box
        if idx == 0:
            lanes = ("BBox", "CPD-style", "V-HACD")
            for n, lane in enumerate(lanes):
                y = y0 + 52 + n * 76
                self._box((x0 + 50, y, x0 + 230, y + 46), _palette(n))
                self.draw.text((x0 + 260, y + 8), lane, font=self.bold, fill=TEXT)
        elif idx == 1:
            for n in range(5):
                px = x0 + 95 + n * 76
                self._box((px, y0 + 78 + (n % 2) * 50, px + 58, y0 + 170 + (n % 2) * 50), _palette(n))
            self.draw.text((x0 + 54, y1 - 65), "package, not isolated primitive", font=self.bold, fill=TEXT)
        else:
            self._term_stack(("probe", "accept", "fallback"), (BLUE, GREEN, GOLD))

    def draw_provenance(self, idx: int) -> None:
        steps = ("config", "record", "manifest", "supplement")
        x0, y0, x1, y1 = self.box
        for n, step in enumerate(steps):
            x = x0 + 42 + n * 118
            self._box((x, y0 + 98, x + 100, y0 + 170), _palette(n))
            self.draw.text((x, y0 + 188), step, font=self.font, fill=TEXT)
            if n < len(steps) - 1:
                self._arrow((x + 105, y0 + 134), (x + 148, y0 + 134), MUTED)
        if idx == 2:
            self.draw.text((x0 + 48, y1 - 70), "hashes bind generated figures", font=self.bold, fill=TEXT)
        elif idx == 3:
            self.draw.text((x0 + 48, y1 - 70), "raw assets stay out of git", font=self.bold, fill=TEXT)

    def _box(self, box: tuple[int, int, int, int], color: str) -> None:
        _rounded(self.draw, box, 14, "#f8fafc", color, 5)

    def _arrow(self, start: tuple[int, int], end: tuple[int, int], color: str) -> None:
        _arrow(self.draw, start, end, color)

    def _term_stack(self, labels: Iterable[str], colors: Iterable[str]) -> None:
        x0, y0, x1, _ = self.box
        for n, (label, color) in enumerate(zip(labels, colors)):
            y = y0 + 36 + n * 72
            _rounded(self.draw, (x0 + 55, y, x1 - 55, y + 52), 16, "#f8fafc", color, 4)
            self.draw.ellipse((x0 + 78, y + 15, x0 + 100, y + 37), fill=color)
            self.draw.text((x0 + 120, y + 12), label, font=self.bold, fill=TEXT)

    def _robot_arm(self, source: bool) -> None:
        x0, y0, _, _ = self.box
        joints = [(x0 + 92, y0 + 220), (x0 + 162, y0 + 150), (x0 + 255, y0 + 192), (x0 + 360, y0 + 110), (x0 + 455, y0 + 164)]
        for a, b in zip(joints, joints[1:]):
            self.draw.line((a, b), fill="#2f3946", width=18)
        for n, joint in enumerate(joints):
            color = "#cfd8e3" if source else _palette(n)
            self.draw.ellipse((joint[0] - 28, joint[1] - 28, joint[0] + 28, joint[1] + 28), fill=color, outline="#172033", width=3)
        if source:
            for joint in joints[1:4]:
                self.draw.rectangle((joint[0] - 42, joint[1] - 42, joint[0] + 42, joint[1] + 42), outline=RED, width=4)

    def _link_chain(self, labels: Sequence[str]) -> None:
        x0, y0, _, _ = self.box
        last = None
        for n, label in enumerate(labels):
            x = x0 + 48 + n * 105
            y = y0 + 132 + int(42 * math.sin(n))
            self.draw.ellipse((x, y, x + 72, y + 72), fill="#f8fafc", outline=_palette(n), width=5)
            self.draw.text((x + 5, y + 88), label, font=self.font, fill=TEXT)
            if last:
                self.draw.line((last[0] + 72, last[1] + 36, x, y + 36), fill=MUTED, width=5)
            last = (x, y)

    def _bowl_scene(self, tilted: bool) -> None:
        x0, y0, x1, y1 = self.box
        tilt = 30 if tilted else 0
        self.draw.arc((x0 + 130 + tilt, y0 + 130, x1 - 130 + tilt, y1 - 30), 0, 180, fill=BLUE, width=9)
        self.draw.line((x0 + 80, y1 - 42, x1 - 80, y1 - 42), fill="#2f3946", width=4)

    def _cup_scene(self) -> None:
        x0, y0, _, y1 = self.box
        self.draw.rectangle((x0 + 190, y0 + 82, x0 + 340, y1 - 48), fill="#eef4fb", outline=BLUE, width=7)
        self.draw.arc((x0 + 315, y0 + 140, x0 + 430, y0 + 230), 270, 90, fill=BLUE, width=7)

    def _tray_scene(self) -> None:
        x0, y0, x1, y1 = self.box
        self.draw.polygon(((x0 + 110, y1 - 78), (x1 - 80, y1 - 118), (x1 - 130, y1 - 40), (x0 + 80, y1 - 28)), fill="#eef4fb", outline=TEAL)
        self.draw.line((x0 + 120, y0 + 95, x1 - 120, y0 + 145), fill=GOLD, width=8)

    def _gauge(self, value: float, color: str, label: str) -> None:
        x0, y0, x1, y1 = self.box
        self.draw.arc((x0 + 120, y0 + 60, x1 - 120, y1 + 140), 190, 350, fill="#d7dee9", width=18)
        self.draw.arc((x0 + 120, y0 + 60, x1 - 120, y1 + 140), 190, 190 + int(160 * value), fill=color, width=18)
        self.draw.text((x0 + 185, y0 + 170), label, font=self.bold, fill=color)

    def _label_card(self, title: str, color: str, label: str) -> None:
        x0, y0, x1, y1 = self.box
        _rounded(self.draw, (x0 + 86, y0 + 86, x1 - 86, y1 - 70), 22, "#fff7ed", color, 5)
        self.draw.text((x0 + 122, y0 + 122), title, font=self.bold, fill=TEXT)
        self.draw.text((x0 + 122, y0 + 172), label, font=_font(32, bold=True), fill=color)


def _panel_boxes(count: int) -> list[tuple[int, int, int, int]]:
    top, bottom = 210, 812
    if count <= 3:
        width = 520
        gap = 40
        return [(78 + n * (width + gap), top, 78 + n * (width + gap) + width, bottom) for n in range(count)]
    width = 380
    gap = 36
    return [(78 + n * (width + gap), top, 78 + n * (width + gap) + width, bottom) for n in range(count)]


def _draw_background(draw: ImageDraw.ImageDraw) -> None:
    for x in range(0, CANVAS_SIZE[0], 48):
        draw.line((x, 0, x, CANVAS_SIZE[1]), fill="#edf1f6", width=1)
    for y in range(0, CANVAS_SIZE[1], 48):
        draw.line((0, y, CANVAS_SIZE[0], y), fill="#edf1f6", width=1)


def _callout(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    color: str,
    title_font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    body_font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
) -> None:
    _rounded(draw, box, 22, "#ffffff", "#d7dee9", 2)
    draw.rectangle((box[0], box[1], box[0] + 14, box[3]), fill=color)
    draw.text((box[0] + 36, box[1] + 24), title, font=title_font, fill=color)
    y = box[1] + 72
    for line in _wrap(body, 66):
        draw.text((box[0] + 36, y), line, font=body_font, fill=TEXT)
        y += 28


def _rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str,
    outline: str,
    width: int,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str) -> None:
    draw.line((start, end), fill=color, width=6)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 20
    p1 = (end[0] - size * math.cos(angle - 0.55), end[1] - size * math.sin(angle - 0.55))
    p2 = (end[0] - size * math.cos(angle + 0.55), end[1] - size * math.sin(angle + 0.55))
    draw.polygon((end, p1, p2), fill=color)


def _palette(index: int) -> str:
    colors = (BLUE, GREEN, GOLD, PURPLE, TEAL, RED)
    return colors[index % len(colors)]


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in (Path("/usr/share/fonts/truetype/dejavu"), Path("/usr/local/share/fonts")):
        path = base / name
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


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


def _canonical_spec(spec: SupplementFigureSpec) -> str:
    return json.dumps(asdict(spec), sort_keys=True, separators=(",", ":"))


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
