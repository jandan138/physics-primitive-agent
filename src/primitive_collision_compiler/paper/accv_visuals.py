from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np


PACKAGE_LANE_ORDER: tuple[str, ...] = (
    "bounding_primitive",
    "cpd_style_primitive_candidate_if_available",
    "coacd_or_vhacd_if_available",
    "vhacd_if_available",
)
MATRIX_LANE_ORDER: tuple[str, ...] = (
    "bounding_primitive",
    "single_convex_hull",
    "cpd_style_primitive_candidate_if_available",
    "coacd_or_vhacd_if_available",
    "vhacd_if_available",
)
LANE_LABELS: Mapping[str, str] = {
    "bounding_primitive": "BBox",
    "cpd_style_primitive_candidate_if_available": "CPD-style",
    "coacd_or_vhacd_if_available": "CoACD",
    "vhacd_if_available": "V-HACD",
    "single_convex_hull": "Single hull",
}
PROBE_ORDER: tuple[str, ...] = (
    "contact_canary",
    "body_state_drop_settle",
    "stack_or_slide",
    "sphere_rain",
)
PROBE_LABELS: Mapping[str, str] = {
    "contact_canary": "Contact",
    "body_state_drop_settle": "Drop",
    "stack_or_slide": "Stack",
    "sphere_rain": "Sphere",
}
OUTCOME_TO_VALUE: Mapping[str, int] = {
    "fallback": 0,
    "not_applicable": 1,
    "failure": 2,
    "accept": 3,
}
OUTCOME_COLORS: Mapping[str, str] = {
    "accept": "#2e7d59",
    "failure": "#b94b48",
    "fallback": "#8a8f98",
    "not_applicable": "#d5d8dc",
    "dependency_gap": "#a76f1b",
}
PDF_METADATA: Mapping[str, Any] = {
    "Creator": "primitive_collision_compiler.paper.accv_visuals",
    "Producer": "Matplotlib pdf backend",
    "CreationDate": datetime(2026, 5, 26, tzinfo=timezone.utc),
    "ModDate": datetime(2026, 5, 26, tzinfo=timezone.utc),
}
REPO_ROOT = Path(__file__).resolve().parents[3]
RESULTS_MANIFEST = REPO_ROOT / "paper/shared/evidence/results_manifest.yaml"
PHASE0_SOURCE_RECORDS: tuple[str, ...] = (
    "docs/records/2026-05-26-phase0-vhacd-runtime-followup.md",
    "docs/records/2026-05-26-phase0-paper-evidence-closure.md",
)
FRANKA_SOURCE_RECORDS: tuple[str, ...] = (
    "docs/records/2026-05-26-link-aware-robot-package-generation.md",
    "docs/records/2026-05-26-generated-package-robot-task-probe.md",
)


@dataclass(frozen=True)
class FigureOutput:
    figure_id: str
    path: Path
    evidence: str
    source_records: tuple[str, ...] = ()


def load_phase0_report(path: str | Path) -> dict[str, Any]:
    report_path = Path(path)
    with report_path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ValueError(f"phase0 report must be a JSON object: {report_path}")
    if "cases" not in payload:
        raise ValueError(f"phase0 report missing cases: {report_path}")
    return payload


def case_label(case: Mapping[str, Any]) -> str:
    role = str(case.get("asset_role", "asset")).replace("_", " ")
    asset_id = str(case.get("asset_id", "unknown"))
    if "bowl" in asset_id:
        name = "bowl"
    elif "cup" in asset_id:
        name = "cup"
    elif "tray" in asset_id:
        name = "tray"
    elif "keyboard" in asset_id:
        name = "keyboard"
    elif "box" in asset_id:
        name = "box"
    else:
        name = asset_id.split("_")[1] if "_" in asset_id else asset_id
    return f"{role}\n{name}"


def resolve_asset_path(case: Mapping[str, Any], asset_root: str | Path) -> Path:
    local_path = case.get("local_path") or case.get("asset_path")
    if not local_path:
        raise ValueError(f"case missing local_path: {case.get('asset_id')}")
    path = Path(str(local_path))
    if path.is_absolute():
        return path
    return Path(asset_root) / path


def primitive_vertices(primitive: Mapping[str, Any]) -> np.ndarray:
    kind = str(primitive.get("kind", ""))
    dimensions = primitive.get("dimensions") or {}
    if kind == "box":
        half_extents = np.asarray(dimensions.get("half_extents", ()), dtype=float)
        if half_extents.shape != (3,):
            return np.empty((0, 3), dtype=float)
        center = np.asarray(primitive.get("center", (0.0, 0.0, 0.0)), dtype=float)
        if center.shape != (3,):
            center = np.zeros(3, dtype=float)
        axes = np.asarray(primitive.get("axes") or np.eye(3), dtype=float)
        if axes.shape != (3, 3):
            axes = np.eye(3, dtype=float)
        signs = np.asarray(
            [
                (-1, -1, -1),
                (1, -1, -1),
                (1, 1, -1),
                (-1, 1, -1),
                (-1, -1, 1),
                (1, -1, 1),
                (1, 1, 1),
                (-1, 1, 1),
            ],
            dtype=float,
        )
        local = signs * half_extents
        return center + local @ axes
    if kind == "convex_mesh":
        vertices = np.asarray(dimensions.get("vertices", ()), dtype=float)
        if vertices.ndim == 2 and vertices.shape[1] == 3:
            return vertices
    return np.empty((0, 3), dtype=float)


def package_vertices(package: Mapping[str, Any] | None) -> np.ndarray:
    if not package:
        return np.empty((0, 3), dtype=float)
    clouds = [
        primitive_vertices(primitive)
        for primitive in package.get("primitives", [])
        if isinstance(primitive, Mapping)
    ]
    clouds = [cloud for cloud in clouds if len(cloud)]
    if not clouds:
        return np.empty((0, 3), dtype=float)
    return np.concatenate(clouds, axis=0)


def package_for_lane(case: Mapping[str, Any], lane: str) -> Mapping[str, Any] | None:
    lane_result = (case.get("baseline_results") or {}).get(lane) or {}
    package = lane_result.get("collision_package")
    return package if isinstance(package, Mapping) else None


def probe_result(case: Mapping[str, Any], lane: str, probe: str) -> Mapping[str, Any] | None:
    lane_probes = ((case.get("probe_results") or {}).get(lane) or {})
    result = lane_probes.get(probe)
    return result if isinstance(result, Mapping) else None


def probe_failure_labels(result: Mapping[str, Any] | None) -> tuple[str, ...]:
    if not result:
        return ()
    labels: list[str] = []
    for run_key in ("drop_settle_runs", "stack_slide_runs", "sphere_rain_runs", "contact_canaries"):
        for run in result.get(run_key, []) or []:
            labels.extend(str(label) for label in run.get("failure_labels", []) or [])
    return tuple(dict.fromkeys(labels))


def outcome_matrix(report: Mapping[str, Any]) -> tuple[list[str], list[str], np.ndarray]:
    rows = [case_label(case) for case in report.get("cases", [])]
    columns: list[str] = []
    for lane in MATRIX_LANE_ORDER:
        for probe in PROBE_ORDER:
            columns.append(f"{LANE_LABELS[lane]}\n{PROBE_LABELS[probe]}")

    values = np.zeros((len(rows), len(columns)), dtype=int)
    for row_index, case in enumerate(report.get("cases", [])):
        col_index = 0
        for lane in MATRIX_LANE_ORDER:
            for probe in PROBE_ORDER:
                result = probe_result(case, lane, probe)
                outcome = str((result or {}).get("outcome", "not_applicable"))
                values[row_index, col_index] = OUTCOME_TO_VALUE.get(outcome, 1)
                col_index += 1
    return rows, columns, values


def summarize_probe_outcomes(report: Mapping[str, Any]) -> dict[str, int]:
    counts = {"accept": 0, "failure": 0, "fallback": 0, "not_applicable": 0, "dependency_gap": 0}
    for case in report.get("cases", []):
        for lane in MATRIX_LANE_ORDER:
            for probe in PROBE_ORDER:
                result = probe_result(case, lane, probe)
                outcome = str((result or {}).get("outcome", "not_applicable"))
                counts[outcome] = counts.get(outcome, 0) + 1
    return counts


def generate_accv_visuals(
    *,
    report_path: str | Path,
    asset_root: str | Path,
    output_dir: str | Path,
) -> list[FigureOutput]:
    report = load_phase0_report(report_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    _configure_matplotlib(plt)

    figures = [
        _save_asset_package_overlays(report, Path(asset_root), output, plt),
        _save_collision_probe_scenes(report, output, plt),
        _save_outcome_matrix(report, output, plt),
        _save_mechanism_diagnostic(output, plt),
        _save_franka_task_scene(report, output, plt),
    ]
    _write_manifest(
        output / "accv_visuals_manifest.json",
        report_path=Path(report_path),
        asset_root=Path(asset_root),
        figures=figures,
    )
    return figures


def _configure_matplotlib(plt: Any) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "axes.titlesize": 8,
            "axes.labelsize": 7,
            "xtick.labelsize": 6,
            "ytick.labelsize": 6,
            "legend.fontsize": 7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def _save_asset_package_overlays(
    report: Mapping[str, Any],
    asset_root: Path,
    output: Path,
    plt: Any,
) -> FigureOutput:
    fig = plt.figure(figsize=(12.0, 10.8), constrained_layout=True)
    columns = ("Input mesh", "BBox", "CPD-style", "CoACD", "V-HACD")
    lanes = (None, *PACKAGE_LANE_ORDER)
    for row, case in enumerate(report.get("cases", [])):
        mesh = _load_mesh(resolve_asset_path(case, asset_root), max_faces=1000)
        for col, lane in enumerate(lanes):
            ax = fig.add_subplot(len(report.get("cases", [])), len(columns), row * len(columns) + col + 1, projection="3d")
            if row == 0:
                ax.set_title(columns[col], pad=0)
            if col == 0:
                ax.text2D(-0.08, 0.5, case_label(case), transform=ax.transAxes, ha="right", va="center")
            if mesh is not None:
                _draw_mesh(ax, mesh, alpha=0.20 if lane else 0.65)
                points = mesh.points
            else:
                points = np.empty((0, 3), dtype=float)
            if lane is not None:
                package = package_for_lane(case, lane)
                _draw_package(ax, package, color=_lane_color(lane), max_primitives=16)
                package_points = package_vertices(package)
                if len(package_points):
                    points = _combine_points(points, package_points)
                lane_result = ((case.get("baseline_results") or {}).get(lane) or {})
                ax.text2D(
                    0.02,
                    0.02,
                    f"{lane_result.get('outcome', 'n/a')} / {lane_result.get('primitive_or_hull_count', 0)}",
                    transform=ax.transAxes,
                    ha="left",
                    va="bottom",
                    color=_lane_color(lane),
                )
            _finish_3d_axis(ax, points)
    path = output / "phase0_asset_package_overlays.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "phase0_asset_package_overlays",
        path,
        "phase0 report + repo-local USD mirrors",
        PHASE0_SOURCE_RECORDS,
    )


def _save_collision_probe_scenes(
    report: Mapping[str, Any],
    output: Path,
    plt: Any,
) -> FigureOutput:
    selected_roles = ("container", "contact_affordance", "stackable")
    cases = [case for case in report.get("cases", []) if case.get("asset_role") in selected_roles]
    fig = plt.figure(figsize=(11.5, 6.8), constrained_layout=True)
    for row, case in enumerate(cases):
        package = package_for_lane(case, "vhacd_if_available")
        render_ax = fig.add_subplot(len(cases), 3, row * 3 + 1, projection="3d")
        _draw_package(render_ax, package, color=_lane_color("vhacd_if_available"), max_primitives=16)
        _finish_3d_axis(render_ax, package_vertices(package))
        render_ax.set_title("V-HACD package" if row == 0 else "")
        render_ax.text2D(-0.06, 0.5, case_label(case), transform=render_ax.transAxes, ha="right", va="center")

        drop_ax = fig.add_subplot(len(cases), 3, row * 3 + 2)
        _draw_drop_probe_panel(drop_ax, probe_result(case, "vhacd_if_available", "body_state_drop_settle"))
        if row == 0:
            drop_ax.set_title("Drop/settle probe")

        stack_ax = fig.add_subplot(len(cases), 3, row * 3 + 3)
        _draw_stack_probe_panel(stack_ax, probe_result(case, "vhacd_if_available", "stack_or_slide"))
        if row == 0:
            stack_ax.set_title("Stack/slide probe")
    path = output / "phase0_collision_probe_scenes.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "phase0_collision_probe_scenes",
        path,
        "phase0 Newton probe outcomes",
        PHASE0_SOURCE_RECORDS,
    )


def _save_outcome_matrix(report: Mapping[str, Any], output: Path, plt: Any) -> FigureOutput:
    rows, columns, values = outcome_matrix(report)
    fig, ax = plt.subplots(figsize=(12.0, 3.6), constrained_layout=True)
    colors = ["#8a8f98", "#d5d8dc", "#b94b48", "#2e7d59"]
    from matplotlib.colors import ListedColormap, BoundaryNorm

    cmap = ListedColormap(colors)
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)
    ax.imshow(values, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(np.arange(len(columns)))
    ax.set_xticklabels(columns, rotation=60, ha="right")
    ax.set_yticks(np.arange(len(rows)))
    ax.set_yticklabels(rows)
    ax.set_title("Phase 0 diagnostic outcomes")
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            label = {0: "Fbk", 1: "N/A", 2: "Fail", 3: "Pass"}[int(values[row, col])]
            ax.text(col, row, label, ha="center", va="center", fontsize=5.5, color="#111111")
    _draw_outcome_legend(ax)
    path = output / "phase0_outcome_matrix.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput("phase0_outcome_matrix", path, "phase0 report outcome labels", PHASE0_SOURCE_RECORDS)


def _save_mechanism_diagnostic(output: Path, plt: Any) -> FigureOutput:
    entry = _load_result_entry("bed_franka_cylinder_mechanism")
    metrics = entry.get("metrics") or {}
    source_records = tuple(_split_evidence_sources(entry.get("evidence_source", ""))) + (
        "paper/shared/evidence/results_manifest.yaml",
    )
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.5), constrained_layout=True)
    speeds = [
        float(metrics["bed_final_speed_mps"]),
        float(metrics["franka_final_speed_mps"]),
    ]
    labels = ["Capped bed\nfull package", "Capped Franka\npackage"]
    axes[0].bar(labels, speeds, color=["#b94b48", "#2e7d59"])
    axes[0].axhline(
        float(metrics["settle_gate_mps"]),
        color="#333333",
        linestyle="--",
        linewidth=1.0,
        label="settle gate",
    )
    axes[0].set_ylabel("final linear speed (m/s)")
    axes[0].set_title("Full-package body-state result")
    axes[0].legend(loc="upper right", frameon=False)
    axes[0].set_ylim(0, 0.09)
    mechanism_rows = metrics.get("audit_rows") or []
    if not mechanism_rows:
        raise RuntimeError(f"missing mechanism audit rows in {RESULTS_MANIFEST}")
    axes[1].axis("off")
    axes[1].set_title("Recorded mechanism audit")
    y = 0.92
    for row in mechanism_rows:
        left = str(row.get("label", ""))
        right = str(row.get("result", ""))
        color = _audit_status_color(str(row.get("status", right)))
        axes[1].text(0.02, y, left, ha="left", va="center", transform=axes[1].transAxes)
        axes[1].text(0.98, y, right, ha="right", va="center", color=color, transform=axes[1].transAxes)
        axes[1].plot([0.02, 0.98], [y - 0.055, y - 0.055], color="#d8d8d8", linewidth=0.6, transform=axes[1].transAxes)
        y -= 0.17
    path = output / "bed_franka_mechanism_diagnostic.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "bed_franka_mechanism_diagnostic",
        path,
        "2026-05-22 cylinder mechanism records",
        source_records,
    )


def _save_franka_task_scene(report: Mapping[str, Any], output: Path, plt: Any) -> FigureOutput:
    articulation = (report.get("articulation_cases") or [{}])[0]
    robot_result = articulation.get("robot_package_result") or {}
    links = robot_result.get("links", []) or []
    metrics = ((articulation.get("probe_results") or {}).get("generated_package_robot_task_if_robot") or {}).get(
        "metrics", {}
    )
    package_consumption = metrics.get("package_consumption") or {}
    audit_metrics = ((robot_result.get("link_boundary_audit") or {}).get("metrics") or {})

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 3.9), constrained_layout=True)
    axes[0].set_title("Link-aware package coverage")
    axes[0].set_xlim(-0.5, max(len(links) - 0.5, 0.5))
    axes[0].set_ylim(-0.2, 1.2)
    axes[0].axis("off")
    for index, link in enumerate(links):
        is_placeholder = int(link.get("placeholder_primitive_count", 0)) > 0
        color = "#a76f1b" if is_placeholder else "#2e7d59"
        rect = plt.Rectangle((index - 0.35, 0.35), 0.7, 0.35, facecolor=color, edgecolor="#222222", linewidth=0.8)
        axes[0].add_patch(rect)
        label = str(link.get("link_path", f"link{index}")).split("/")[-1].replace("panda_", "")
        axes[0].text(index, 0.78, label, ha="center", va="bottom", rotation=45, fontsize=6)
        axes[0].text(index, 0.52, str(link.get("primitive_count", 0)), ha="center", va="center", color="white")
        if index < len(links) - 1:
            axes[0].plot([index + 0.35, index + 0.65], [0.525, 0.525], color="#444444", linewidth=0.8)
    axes[0].text(0.02, 0.08, "green: mesh-backed link box; amber: meshless sentinel", transform=axes[0].transAxes)

    axes[1].axis("off")
    axes[1].set_title("Generated-package task smoke")
    rows = [
        ("detected links", audit_metrics.get("link_count", len(links))),
        ("generated primitives", robot_result.get("primitive_or_hull_count", 0)),
        ("missing body links", package_consumption.get("missing_body_link_count", 0)),
        ("source USD shapes", package_consumption.get("source_usd_shape_count", 0)),
        ("self-collision filters", package_consumption.get("generated_self_collision_filter_pair_count", 0)),
        ("task outcome", ((articulation.get("probe_results") or {}).get("generated_package_robot_task_if_robot") or {}).get("outcome", "n/a")),
    ]
    y = 0.88
    for left, right in rows:
        color = "#2e7d59" if str(right) in {"0", "accept", "True"} or left != "source USD shapes" else "#333333"
        axes[1].text(0.04, y, left, ha="left", va="center", transform=axes[1].transAxes)
        axes[1].text(0.96, y, str(right), ha="right", va="center", color=color, transform=axes[1].transAxes)
        axes[1].plot([0.04, 0.96], [y - 0.06, y - 0.06], color="#d8d8d8", linewidth=0.6, transform=axes[1].transAxes)
        y -= 0.14
    path = output / "franka_link_aware_task_scene.pdf"
    _save_pdf(fig, path)
    plt.close(fig)
    return FigureOutput(
        "franka_link_aware_task_scene",
        path,
        "link-aware package and generated-package robot task records",
        FRANKA_SOURCE_RECORDS,
    )


def _load_mesh(path: Path, *, max_faces: int) -> Any:
    try:
        from primitive_collision_compiler.baselines.cpd_like.usd import load_first_mesh

        return load_first_mesh(path, max_faces=max_faces)
    except Exception as exc:
        raise RuntimeError(f"failed to load source mesh for paper figure: {path}") from exc


def _draw_mesh(ax: Any, mesh: Any, *, alpha: float) -> None:
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    faces = mesh.faces
    if len(faces) > 700:
        step = max(1, math.ceil(len(faces) / 700))
        faces = faces[::step]
    polygons = mesh.points[faces]
    collection = Poly3DCollection(
        polygons,
        facecolor="#c9cdd2",
        edgecolor="#7b838c",
        linewidth=0.12,
        alpha=alpha,
        rasterized=True,
    )
    ax.add_collection3d(collection)


def _draw_package(ax: Any, package: Mapping[str, Any] | None, *, color: str, max_primitives: int) -> None:
    if not package:
        ax.text2D(0.5, 0.5, "fallback", transform=ax.transAxes, ha="center", va="center", color="#777777")
        return
    primitives = [p for p in package.get("primitives", []) if isinstance(p, Mapping)]
    if not primitives:
        ax.text2D(0.5, 0.5, "no mapped\nprimitive", transform=ax.transAxes, ha="center", va="center", color="#777777")
        return
    for primitive in primitives[:max_primitives]:
        _draw_primitive(ax, primitive, color=color)
    if len(primitives) > max_primitives:
        ax.text2D(0.98, 0.02, f"+{len(primitives)-max_primitives}", transform=ax.transAxes, ha="right", va="bottom", color=color)


def _draw_primitive(ax: Any, primitive: Mapping[str, Any], *, color: str) -> None:
    kind = str(primitive.get("kind", ""))
    vertices = primitive_vertices(primitive)
    if not len(vertices):
        return
    if kind == "box":
        for start, end in _BOX_EDGES:
            ax.plot(*zip(vertices[start], vertices[end]), color=color, linewidth=0.8, alpha=0.95)
        return
    faces = ((primitive.get("dimensions") or {}).get("faces") or [])[:24]
    for face in faces:
        if len(face) < 3:
            continue
        cycle = list(face[:3]) + [face[0]]
        pts = vertices[np.asarray(cycle, dtype=int)]
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=color, linewidth=0.45, alpha=0.72)


_BOX_EDGES: tuple[tuple[int, int], ...] = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
)


def _combine_points(*arrays: np.ndarray) -> np.ndarray:
    valid = [array for array in arrays if isinstance(array, np.ndarray) and len(array)]
    if not valid:
        return np.empty((0, 3), dtype=float)
    return np.concatenate(valid, axis=0)


def _finish_3d_axis(ax: Any, points: np.ndarray) -> None:
    ax.view_init(elev=20, azim=-55)
    ax.set_axis_off()
    if not len(points):
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        return
    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    center = (mins + maxs) / 2.0
    radius = float(np.max(maxs - mins) / 2.0)
    if radius <= 0:
        radius = 1.0
    ax.set_xlim(center[0] - radius, center[0] + radius)
    ax.set_ylim(center[1] - radius, center[1] + radius)
    ax.set_zlim(center[2] - radius, center[2] + radius)
    try:
        ax.set_box_aspect((1, 1, 1))
    except Exception:
        pass


def _draw_drop_probe_panel(ax: Any, result: Mapping[str, Any] | None) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.15, 1.05)
    ax.axis("off")
    run = _first_run(result, "drop_settle_runs")
    initial = float(((result or {}).get("initial_conditions") or {}).get("height_m", 0.25))
    final = float((run or {}).get("final_height", 0.0))
    min_height = float((run or {}).get("min_height", min(final, 0.0)))
    status = str((result or {}).get("outcome", "not_applicable"))
    labels = probe_failure_labels(result)
    ax.plot([0.15, 0.85], [0.15, 0.15], color="#222222", linewidth=1.0)
    ax.scatter([0.35], [_scaled_height(initial)], s=80, color="#7b838c", label="initial")
    ax.scatter([0.65], [_scaled_height(final)], s=80, color=OUTCOME_COLORS.get(status, "#777777"), label="final")
    ax.plot([0.35, 0.65], [_scaled_height(initial), _scaled_height(final)], color="#777777", linestyle="--", linewidth=0.8)
    ax.text(0.5, 0.93, f"outcome: {status}", ha="center", va="top", color=OUTCOME_COLORS.get(status, "#333333"))
    ax.text(0.5, 0.03, f"final z {final:.3f}, min z {min_height:.3f}", ha="center", va="bottom", fontsize=6)
    if labels:
        ax.text(0.5, 0.80, "\n".join(labels[:3]), ha="center", va="top", fontsize=6, color="#b94b48")


def _draw_stack_probe_panel(ax: Any, result: Mapping[str, Any] | None) -> None:
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.05, 1.05)
    ax.axis("off")
    run = _first_run(result, "stack_slide_runs")
    status = str((result or {}).get("outcome", "not_applicable"))
    support = float((run or {}).get("support_top_height", 0.55))
    initial = (run or {}).get("initial_probe_position", [0.2, 0.2, support + 0.06])
    final = (run or {}).get("final_probe_position", [0.75, 0.55, support + 0.03])
    horizontal = float((run or {}).get("horizontal_displacement_m", 0.0))
    labels = probe_failure_labels(result)
    ax.add_patch(plt_rectangle((0.12, 0.15), 0.76, 0.18, "#c9cdd2"))
    start = (0.28, 0.62)
    end_x = min(1.02, 0.28 + horizontal / max(horizontal, 0.25) * 0.55) if horizontal else 0.68
    end = (end_x, 0.47 if status == "failure" else 0.62)
    ax.add_patch(plt_rectangle((start[0] - 0.055, start[1] - 0.055), 0.11, 0.11, "#7b838c"))
    ax.add_patch(plt_rectangle((end[0] - 0.055, end[1] - 0.055), 0.11, 0.11, OUTCOME_COLORS.get(status, "#777777")))
    ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "lw": 0.8, "color": "#555555"})
    ax.text(0.5, 0.96, f"outcome: {status}", ha="center", va="top", color=OUTCOME_COLORS.get(status, "#333333"))
    ax.text(0.5, 0.04, f"slide {horizontal:.3f} m, support z {support:.2f}", ha="center", va="bottom", fontsize=6)
    if labels:
        ax.text(0.5, 0.82, "\n".join(labels[:3]), ha="center", va="top", fontsize=6, color="#b94b48")
    _ = initial, final


def _first_run(result: Mapping[str, Any] | None, key: str) -> Mapping[str, Any] | None:
    runs = (result or {}).get(key) or []
    return runs[0] if runs and isinstance(runs[0], Mapping) else None


def _scaled_height(height: float) -> float:
    return max(0.18, min(0.88, 0.15 + height * 1.8))


def plt_rectangle(xy: tuple[float, float], width: float, height: float, color: str) -> Any:
    from matplotlib.patches import Rectangle

    return Rectangle(xy, width, height, facecolor=color, edgecolor="#222222", linewidth=0.8)


def _draw_outcome_legend(ax: Any) -> None:
    from matplotlib.patches import Patch

    handles = [
        Patch(facecolor="#2e7d59", label="accept"),
        Patch(facecolor="#b94b48", label="failure"),
        Patch(facecolor="#8a8f98", label="fallback"),
        Patch(facecolor="#d5d8dc", label="not applicable"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=4, frameon=False)


def _lane_color(lane: str) -> str:
    return {
        "bounding_primitive": "#2d6cdf",
        "cpd_style_primitive_candidate_if_available": "#7a5195",
        "coacd_or_vhacd_if_available": "#ef7d00",
        "vhacd_if_available": "#b94b48",
    }.get(lane, "#333333")


def _write_manifest(
    path: Path,
    *,
    report_path: Path,
    asset_root: Path,
    figures: Sequence[FigureOutput],
) -> None:
    source_records = tuple(dict.fromkeys(record for figure in figures for record in figure.source_records))
    payload = {
        "schema_version": 1,
        "report_path": str(report_path),
        "report_sha256": _sha256_file(report_path),
        "asset_root": str(asset_root),
        "generation": "deterministic_matplotlib_diagnostic_visualization",
        "claim_boundary": "diagnostic_visualization_not_photorealistic_render_or_new_experiment",
        "source_record_hashes": _source_record_hashes(source_records),
        "figures": [
            {
                "id": figure.figure_id,
                "path": str(figure.path),
                "evidence": figure.evidence,
                "source_records": list(figure.source_records),
            }
            for figure in figures
        ],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _save_pdf(fig: Any, path: Path) -> None:
    fig.savefig(path, bbox_inches="tight", metadata=dict(PDF_METADATA))


def _load_result_entry(result_id: str) -> Mapping[str, Any]:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to load paper evidence manifests") from exc
    payload = yaml.safe_load(RESULTS_MANIFEST.read_text(encoding="utf-8")) or {}
    for entry in payload.get("results", []) or []:
        if entry.get("id") == result_id:
            return entry
    raise RuntimeError(f"missing result entry {result_id!r} in {RESULTS_MANIFEST}")


def _split_evidence_sources(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(";") if part.strip())


def _audit_status_color(status: str) -> str:
    return "#2e7d59" if status in {"supported", "bed passes"} else "#b94b48"


def _source_record_hashes(records: Sequence[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for record in records:
        path = Path(record)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists():
            raise RuntimeError(f"missing source record for paper figure manifest: {record}")
        hashes[record] = _sha256_file(path)
    return hashes


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate ACCV Phase 0 paper visuals.")
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--asset-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    figures = generate_accv_visuals(
        report_path=args.report,
        asset_root=args.asset_root,
        output_dir=args.output_dir,
    )
    for figure in figures:
        print(f"{figure.figure_id}: {figure.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
