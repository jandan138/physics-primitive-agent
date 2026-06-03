from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import yaml
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[3]
FIG1_NEWTON_SLOT_NAMES = ("asset_intake", "candidate_package", "newton_diagnostics")
DEFAULT_NEWTON_ROOT = Path("/cpfs/shared/simulation/zhuzihou/dev/newton")
DEFAULT_NEWTON_PYTHON = Path(
    "/cpfs/user/zhuzihou/conda-managed/envs/physics-primitive-newton-py310/bin/python"
)
DEFAULT_SOURCE_ARTIFACT_ROOT = Path(
    os.environ.get("PPA_FIG1_SOURCE_ARTIFACT_ROOT", str(REPO_ROOT))
)
DEFAULT_OUTPUT_DIR = REPO_ROOT / "paper/shared/figures/assets/fig1_newton_slots"
DEFAULT_PHASE0_REPORT = Path(
    "reports/generated/phase0_baseline/phase0_grscenes_rigid_plus_franka_newton_2026-05-26.json"
)
DEFAULT_PHASE0_ASSET_MANIFEST = Path("assets/manifests/phase0_assets.yaml")
FIG1_NEWTON_CLAIM_BOUNDARY = (
    "Newton-rendered Fig.1 slots are visual exposition only; not experimental evidence."
)
SLOT_IMAGE_SIZE = (640, 420)


def source_artifact_path(path: str | Path, *, source_artifact_root: Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else Path(source_artifact_root) / candidate


def build_newton_slot_worker_command(
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    source_artifact_root: str | Path = DEFAULT_SOURCE_ARTIFACT_ROOT,
    python_executable: str | Path = DEFAULT_NEWTON_PYTHON,
    newton_root: str | Path = DEFAULT_NEWTON_ROOT,
    phase0_report: str | Path = DEFAULT_PHASE0_REPORT,
    asset_manifest: str | Path = DEFAULT_PHASE0_ASSET_MANIFEST,
) -> tuple[list[str], dict[str, str]]:
    env = os.environ.copy()
    newton_root_path = Path(newton_root)
    env["PPA_FIG1_SOURCE_ARTIFACT_ROOT"] = str(source_artifact_root)
    env["PYTHONPATH"] = _prepend_pythonpath(
        [newton_root_path, REPO_ROOT / "src", REPO_ROOT],
        env.get("PYTHONPATH", ""),
    )
    command = [
        str(python_executable),
        "-m",
        "primitive_collision_compiler.paper.fig1_newton_slots",
        "--worker-render",
        "--output-dir",
        str(output_dir),
        "--source-artifact-root",
        str(source_artifact_root),
        "--phase0-report",
        str(phase0_report),
        "--asset-manifest",
        str(asset_manifest),
        "--newton-root",
        str(newton_root_path),
    ]
    return command, env


def load_newton_slot_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if payload.get("mode") != "newton_render_slots":
        raise ValueError("Fig.1 Newton slot manifest must use mode: newton_render_slots")
    if payload.get("renderer") != "newton_sensor_tiled_camera":
        raise ValueError("Fig.1 Newton slot manifest must use renderer: newton_sensor_tiled_camera")
    slots = payload.get("slots")
    if not isinstance(slots, Mapping):
        raise ValueError("Fig.1 Newton slot manifest missing slots mapping")
    missing = [slot for slot in FIG1_NEWTON_SLOT_NAMES if slot not in slots]
    if missing:
        raise ValueError(f"Fig.1 Newton slot manifest missing slots: {', '.join(missing)}")
    for slot in FIG1_NEWTON_SLOT_NAMES:
        slot_record = slots.get(slot)
        if not isinstance(slot_record, Mapping):
            raise ValueError(f"Fig.1 Newton slot record must be a mapping: {slot}")
        for field in ("image", "sidecar"):
            resolved = _manifest_path_to_file(str(slot_record.get(field, "")))
            if not resolved.is_file():
                raise FileNotFoundError(resolved)
    return dict(payload)


def write_newton_slot_manifest(
    *,
    output_dir: str | Path,
    slot_artifacts: Mapping[str, Mapping[str, str | Path]],
    source_report: str | Path,
    source_manifest: str | Path,
    source_artifact_root: str | Path | None = None,
    newton_root: str | Path,
    newton_commit: str,
) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    missing = [slot for slot in FIG1_NEWTON_SLOT_NAMES if slot not in slot_artifacts]
    if missing:
        raise ValueError(f"missing Fig.1 Newton slots: {', '.join(missing)}")

    slots: dict[str, dict[str, Any]] = {}
    for slot in FIG1_NEWTON_SLOT_NAMES:
        record = slot_artifacts[slot]
        png = Path(record["png"])
        sidecar = Path(record["sidecar"])
        if not png.is_file():
            raise FileNotFoundError(png)
        if not sidecar.is_file():
            raise FileNotFoundError(sidecar)
        slots[slot] = {
            "image": _manifest_file_value(png),
            "sidecar": _manifest_file_value(sidecar),
            "image_sha256": _sha256_file(png),
            "sidecar_sha256": _sha256_file(sidecar),
        }

    manifest = {
        "schema_version": 1,
        "mode": "newton_render_slots",
        "renderer": "newton_sensor_tiled_camera",
        "slots": slots,
        "source_report": str(source_report),
        "source_report_sha256": _sha256_file(Path(source_report)) if Path(source_report).is_file() else "",
        "source_manifest": str(source_manifest),
        "source_manifest_sha256": (
            _sha256_file(Path(source_manifest)) if Path(source_manifest).is_file() else ""
        ),
        "source_artifact_root": str(source_artifact_root or ""),
        "newton": {
            "root": str(newton_root),
            "commit": newton_commit,
        },
        "claim_boundary": FIG1_NEWTON_CLAIM_BOUNDARY,
    }
    manifest_path = output / "manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return manifest_path


def render_newton_slots_via_worker(
    *,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    source_artifact_root: str | Path = DEFAULT_SOURCE_ARTIFACT_ROOT,
    python_executable: str | Path = DEFAULT_NEWTON_PYTHON,
    newton_root: str | Path = DEFAULT_NEWTON_ROOT,
    phase0_report: str | Path = DEFAULT_PHASE0_REPORT,
    asset_manifest: str | Path = DEFAULT_PHASE0_ASSET_MANIFEST,
) -> Path:
    command, env = build_newton_slot_worker_command(
        output_dir=output_dir,
        source_artifact_root=source_artifact_root,
        python_executable=python_executable,
        newton_root=newton_root,
        phase0_report=phase0_report,
        asset_manifest=asset_manifest,
    )
    subprocess.run(command, cwd=REPO_ROOT, env=env, check=True)
    return Path(output_dir) / "manifest.yaml"


def _worker_render_all(args: argparse.Namespace) -> int:
    # Worker-only heavy imports. Normal tests can import this module without Newton/Warp.
    import newton
    import warp as wp

    source_root = Path(args.source_artifact_root)
    report_path = source_artifact_path(args.phase0_report, source_artifact_root=source_root)
    asset_manifest_path = source_artifact_path(args.asset_manifest, source_artifact_root=source_root)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = json.loads(report_path.read_text(encoding="utf-8"))
    case = _select_case(report, preferred_role="contact_affordance")
    asset_path = source_artifact_path(str(case["local_path"]), source_artifact_root=source_root)
    newton_commit = _git_commit(Path(args.newton_root))

    slot_artifacts: dict[str, dict[str, Path]] = {}
    slot_artifacts["asset_intake"] = _render_asset_intake_slot(
        newton=newton,
        wp=wp,
        case=case,
        asset_path=asset_path,
        report_path=report_path,
        asset_manifest_path=asset_manifest_path,
        output_dir=output_dir,
        newton_root=Path(args.newton_root),
        newton_commit=newton_commit,
        source_artifact_root=source_root,
    )
    slot_artifacts["candidate_package"] = _render_candidate_package_slot(
        newton=newton,
        wp=wp,
        case=case,
        report_path=report_path,
        asset_manifest_path=asset_manifest_path,
        output_dir=output_dir,
        newton_root=Path(args.newton_root),
        newton_commit=newton_commit,
        source_artifact_root=source_root,
    )
    slot_artifacts["newton_diagnostics"] = _render_diagnostics_slot(
        newton=newton,
        wp=wp,
        case=case,
        report_path=report_path,
        asset_manifest_path=asset_manifest_path,
        output_dir=output_dir,
        newton_root=Path(args.newton_root),
        newton_commit=newton_commit,
        source_artifact_root=source_root,
    )
    manifest = write_newton_slot_manifest(
        output_dir=output_dir,
        slot_artifacts=slot_artifacts,
        source_report=report_path,
        source_manifest=asset_manifest_path,
        source_artifact_root=source_root,
        newton_root=Path(args.newton_root),
        newton_commit=newton_commit,
    )
    print(f"fig1_newton_slots: {manifest}")
    return 0


def _render_asset_intake_slot(
    *,
    newton: Any,
    wp: Any,
    case: Mapping[str, Any],
    asset_path: Path,
    report_path: Path,
    asset_manifest_path: Path,
    output_dir: Path,
    newton_root: Path,
    newton_commit: str,
    source_artifact_root: Path,
) -> dict[str, Path]:
    from primitive_collision_compiler.paper.accv_visuals import _load_mesh

    mesh = _load_mesh(asset_path, max_faces=900)
    points = _normalise_points(_y_up_points(np.asarray(mesh.points, dtype=np.float64)))
    faces = np.asarray(mesh.faces, dtype=np.int32)
    builder = _base_builder(newton)
    body = builder.add_body(label="asset_intake_mesh")
    render_mesh = newton.Mesh(
        points.astype(np.float32),
        faces.reshape(-1).astype(np.int32),
        compute_inertia=False,
        color=(0.44, 0.61, 0.82),
    )
    builder.add_shape_mesh(body, mesh=render_mesh, color=(0.44, 0.61, 0.82), label="source_usd_mesh")
    png = output_dir / "asset_intake_newton.png"
    _render_model(
        newton=newton,
        wp=wp,
        builder=builder,
        output=png,
        eye=(2.65, -3.1, 2.0),
        target=(0.0, 0.0, 0.7),
        fov_degrees=34.0,
        render_mode="asset_tint",
    )
    sidecar = output_dir / "asset_intake_newton.json"
    _write_sidecar(
        sidecar,
        slot="asset_intake",
        case=case,
        report_path=report_path,
        asset_manifest_path=asset_manifest_path,
        newton_root=newton_root,
        newton_commit=newton_commit,
        source_artifact_root=source_artifact_root,
        details={
            "source_asset": str(asset_path),
            "source_asset_sha256": _sha256_file(asset_path),
            "mesh_point_count": int(len(mesh.points)),
            "mesh_face_count": int(len(mesh.faces)),
            "recipe": "render_normalized_source_usd_mesh_with_silhouette_tint",
        },
    )
    return {"png": png, "sidecar": sidecar}


def _render_candidate_package_slot(
    *,
    newton: Any,
    wp: Any,
    case: Mapping[str, Any],
    report_path: Path,
    asset_manifest_path: Path,
    output_dir: Path,
    newton_root: Path,
    newton_commit: str,
    source_artifact_root: Path,
) -> dict[str, Path]:
    builder = _base_builder(newton)
    lanes = (
        ("bounding_primitive", (-1.72, 0.0, 0.0), (0.20, 0.45, 0.82), 1),
        ("cpd_style_primitive_candidate_if_available", (0.0, 0.0, 0.0), (0.22, 0.62, 0.40), 3),
        ("vhacd_if_available", (1.72, 0.0, 0.0), (0.82, 0.54, 0.20), 3),
    )
    lane_details: dict[str, Any] = {}
    for lane, offset, color, limit in lanes:
        package = _package_for_lane(case, lane)
        lane_details[lane] = {
            "primitive_count": len(package.get("primitives", [])) if package else 0,
            "rendered_primitive_count": min(limit, len(package.get("primitives", []))) if package else 0,
        }
        _add_package_primitives(
            newton=newton,
            wp=wp,
            builder=builder,
            package=package,
            offset=np.asarray(offset, dtype=np.float64),
            color=color,
            limit=limit,
            scale_override=0.88,
            convex_mode="aabb",
        )
        _add_lane_pad(wp=wp, builder=builder, offset=offset, color=(0.86, 0.88, 0.90))
    png = output_dir / "candidate_package_newton.png"
    _render_model(
        newton=newton,
        wp=wp,
        builder=builder,
        output=png,
        eye=(3.7, -4.25, 2.45),
        target=(0.0, 0.0, 0.45),
        fov_degrees=35.0,
        render_mode="color",
    )
    sidecar = output_dir / "candidate_package_newton.json"
    _write_sidecar(
        sidecar,
        slot="candidate_package",
        case=case,
        report_path=report_path,
        asset_manifest_path=asset_manifest_path,
        newton_root=newton_root,
        newton_commit=newton_commit,
        source_artifact_root=source_artifact_root,
        details={
            "recipe": "render_recorded_phase0_package_lanes",
            "convex_mesh_render_mode": "aabb_proxy_from_recorded_hull_vertices_for_slot_readability",
            "lanes": lane_details,
        },
    )
    return {"png": png, "sidecar": sidecar}


def _render_diagnostics_slot(
    *,
    newton: Any,
    wp: Any,
    case: Mapping[str, Any],
    report_path: Path,
    asset_manifest_path: Path,
    output_dir: Path,
    newton_root: Path,
    newton_commit: str,
    source_artifact_root: Path,
) -> dict[str, Path]:
    builder = _base_builder(newton)
    package = _package_for_lane(case, "vhacd_if_available")
    _add_package_primitives(
        newton=newton,
        wp=wp,
        builder=builder,
        package=package,
        offset=np.asarray((0.0, 0.0, 0.0), dtype=np.float64),
        color=(0.74, 0.52, 0.24),
        limit=3,
        scale_override=0.86,
        convex_mode="aabb",
    )
    for index, position in enumerate(
        (
            (-0.66, -0.34, 1.20),
            (-0.44, 0.46, 0.72),
            (0.62, -0.42, 1.04),
            (0.68, 0.42, 0.70),
        )
    ):
        body = builder.add_body(
            xform=wp.transform(p=wp.vec3(*position), q=wp.quat_identity()),
            label=f"diagnostic_probe_{index}",
        )
        color = (0.78, 0.24, 0.22) if index == 0 else (0.22, 0.50, 0.82)
        builder.add_shape_sphere(body, radius=0.085, color=color, label=f"probe_{index}")
    flag_body = builder.add_body(
        xform=wp.transform(p=wp.vec3(0.82, 0.08, 0.26), q=wp.quat_identity()),
        label="diagnostic_marker",
    )
    builder.add_shape_box(flag_body, hx=0.12, hy=0.12, hz=0.12, color=(0.80, 0.26, 0.23), label="review_marker")
    png = output_dir / "newton_diagnostics_newton.png"
    _render_model(
        newton=newton,
        wp=wp,
        builder=builder,
        output=png,
        eye=(3.15, -3.85, 2.85),
        target=(0.04, 0.02, 0.66),
        fov_degrees=39.0,
        render_mode="color",
    )
    sidecar = output_dir / "newton_diagnostics_newton.json"
    result = _probe_summary(case, "vhacd_if_available")
    _write_sidecar(
        sidecar,
        slot="newton_diagnostics",
        case=case,
        report_path=report_path,
        asset_manifest_path=asset_manifest_path,
        newton_root=newton_root,
        newton_commit=newton_commit,
        source_artifact_root=source_artifact_root,
        details={
            "recipe": "visual_reconstruction_from_recorded_phase0_package_and_probe_fields",
            "convex_mesh_render_mode": "aabb_proxy_from_recorded_hull_vertices_for_slot_readability",
            "lane": "vhacd_if_available",
            "recorded_probe_summary": result,
            "reconstruction_semantics": (
                "visual reconstruction from recorded report/package fields; not a new diagnostic run"
            ),
        },
    )
    return {"png": png, "sidecar": sidecar}


def _render_model(
    *,
    newton: Any,
    wp: Any,
    builder: Any,
    output: Path,
    eye: tuple[float, float, float],
    target: tuple[float, float, float],
    fov_degrees: float,
    render_mode: str,
) -> None:
    from newton.sensors import SensorTiledCamera

    output.parent.mkdir(parents=True, exist_ok=True)
    model = builder.finalize()
    state = model.state()
    newton.geometry.build_bvh_shape(model, state)
    newton.geometry.build_bvh_particle(model, state)
    sensor = SensorTiledCamera(
        model=model,
        config=SensorTiledCamera.RenderConfig(enable_ambient_lighting=True, enable_textures=True),
    )
    sensor.utils.create_default_light(enable_shadows=True)
    width, height = SLOT_IMAGE_SIZE
    rays = sensor.utils.compute_pinhole_camera_rays(width, height, math.radians(fov_degrees))
    color_image = sensor.utils.create_color_image_output(width, height, camera_count=1)
    shape_index_image = sensor.utils.create_shape_index_image_output(width, height, camera_count=1)
    q = _look_at_quat(wp, eye, target)
    camera_transforms = wp.array(
        [[wp.transformf(wp.vec3f(*eye), wp.quatf(q[0], q[1], q[2], q[3]))]],
        dtype=wp.transformf,
    )
    sensor.update(
        state,
        camera_transforms,
        rays,
        color_image=color_image,
        shape_index_image=shape_index_image,
        clear_data=SensorTiledCamera.GRAY_CLEAR_DATA,
    )
    if render_mode == "shape_index":
        rgba = sensor.utils.to_rgba_from_shape_index(shape_index_image).numpy()[0]
    else:
        rgba = sensor.utils.to_rgba_from_color(color_image).numpy()[0]
    image = Image.fromarray(rgba[:, :, :3]).convert("RGB")
    if render_mode == "shape_index":
        image = _replace_shape_index_background(image)
    elif render_mode == "asset_tint":
        image = _tint_rendered_silhouette(image)
    image.save(output)


def _base_builder(newton: Any) -> Any:
    builder = newton.ModelBuilder(up_axis=newton.Axis.Z)
    builder.add_ground_plane(color=(0.80, 0.82, 0.84))
    return builder


def _add_lane_pad(*, wp: Any, builder: Any, offset: tuple[float, float, float], color: tuple[float, float, float]) -> None:
    body = builder.add_body(
        xform=wp.transform(p=wp.vec3(float(offset[0]), float(offset[1]), 0.01), q=wp.quat_identity()),
        label="lane_pad",
    )
    builder.add_shape_box(body, hx=0.60, hy=0.42, hz=0.012, color=color, label="lane_pad_shape")


def _add_package_primitives(
    *,
    newton: Any,
    wp: Any,
    builder: Any,
    package: Mapping[str, Any] | None,
    offset: np.ndarray,
    color: tuple[float, float, float],
    limit: int,
    scale_override: float,
    convex_mode: str,
) -> None:
    if not package:
        return
    primitives = [primitive for primitive in package.get("primitives", []) if isinstance(primitive, Mapping)]
    if not primitives:
        return
    all_vertices = _package_vertices(primitives)
    if not len(all_vertices):
        return
    converted = _y_up_points(all_vertices)
    center = (converted.min(axis=0) + converted.max(axis=0)) / 2.0
    span = max(float((converted.max(axis=0) - converted.min(axis=0)).max()), 1e-6)
    scale = scale_override / span
    z_min = float(((converted - center) * scale)[:, 2].min())
    lift = -z_min + 0.055
    for index, primitive in enumerate(primitives[:limit]):
        vertices = _normalise_primitive_vertices(
            primitive,
            center=center,
            scale=scale,
            lift=lift,
            offset=offset,
        )
        if not len(vertices):
            continue
        kind = str(primitive.get("kind", ""))
        if kind == "convex_mesh" and convex_mode == "mesh":
            faces = np.asarray((primitive.get("dimensions") or {}).get("faces", []), dtype=np.int32)
            if faces.ndim != 2 or faces.shape[1] != 3 or len(faces) < 1:
                _add_aabb_box(wp=wp, builder=builder, vertices=vertices, color=color, label=f"box_proxy_{index}")
                continue
            body = builder.add_body(label=f"convex_primitive_{index}")
            mesh = newton.Mesh(
                vertices.astype(np.float32),
                faces.reshape(-1).astype(np.int32),
                compute_inertia=False,
                color=color,
            )
            builder.add_shape_mesh(body, mesh=mesh, color=color, label=f"convex_primitive_{index}")
        else:
            _add_aabb_box(wp=wp, builder=builder, vertices=vertices, color=color, label=f"box_primitive_{index}")


def _replace_shape_index_background(image: Image.Image) -> Image.Image:
    background = image.getpixel((0, 0))
    replacement = (235, 239, 245)
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if pixels[x, y] == background:
                pixels[x, y] = replacement
    return image


def _tint_rendered_silhouette(image: Image.Image) -> Image.Image:
    background = image.getpixel((0, 0))
    pixels = image.load()
    for y in range(image.height):
        shade = 0.86 + 0.14 * (1.0 - y / max(image.height - 1, 1))
        for x in range(image.width):
            if pixels[x, y] == background:
                pixels[x, y] = (235, 239, 245)
            else:
                pixels[x, y] = (
                    int(70 * shade),
                    int(105 * shade),
                    int(155 * shade),
                )
    return image


def _add_aabb_box(
    *,
    wp: Any,
    builder: Any,
    vertices: np.ndarray,
    color: tuple[float, float, float],
    label: str,
) -> None:
    mins = vertices.min(axis=0)
    maxs = vertices.max(axis=0)
    center = (mins + maxs) / 2.0
    half = np.maximum((maxs - mins) / 2.0, 0.025)
    body = builder.add_body(
        xform=wp.transform(p=wp.vec3(*center.tolist()), q=wp.quat_identity()),
        label=label,
    )
    builder.add_shape_box(
        body,
        hx=float(half[0]),
        hy=float(half[1]),
        hz=float(half[2]),
        color=color,
        label=f"{label}_shape",
    )


def _normalise_primitive_vertices(
    primitive: Mapping[str, Any],
    *,
    center: np.ndarray,
    scale: float,
    lift: float,
    offset: np.ndarray,
) -> np.ndarray:
    vertices = _primitive_vertices(primitive)
    if not len(vertices):
        return vertices
    converted = _y_up_points(vertices)
    normalised = (converted - center) * scale
    normalised[:, 2] += lift
    normalised += offset
    return normalised


def _normalise_points(points: np.ndarray) -> np.ndarray:
    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    center = (mins + maxs) / 2.0
    span = max(float((maxs - mins).max()), 1e-6)
    normalised = (points - center) * (1.62 / span)
    normalised[:, 2] -= normalised[:, 2].min()
    normalised[:, 2] += 0.045
    return normalised


def _primitive_vertices(primitive: Mapping[str, Any]) -> np.ndarray:
    kind = str(primitive.get("kind", ""))
    dimensions = primitive.get("dimensions") or {}
    if kind == "box":
        half_extents = np.asarray(dimensions.get("half_extents", ()), dtype=np.float64)
        if half_extents.shape != (3,):
            return np.empty((0, 3), dtype=np.float64)
        center = np.asarray(primitive.get("center", (0.0, 0.0, 0.0)), dtype=np.float64)
        if center.shape != (3,):
            center = np.zeros(3, dtype=np.float64)
        axes = np.asarray(primitive.get("axes") or np.eye(3), dtype=np.float64)
        if axes.shape != (3, 3):
            axes = np.eye(3, dtype=np.float64)
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
            dtype=np.float64,
        )
        return center + (signs * half_extents) @ axes
    if kind == "convex_mesh":
        vertices = np.asarray(dimensions.get("vertices", ()), dtype=np.float64)
        if vertices.ndim == 2 and vertices.shape[1] == 3:
            return vertices
    return np.empty((0, 3), dtype=np.float64)


def _package_vertices(primitives: Sequence[Mapping[str, Any]]) -> np.ndarray:
    clouds = [_primitive_vertices(primitive) for primitive in primitives]
    clouds = [cloud for cloud in clouds if len(cloud)]
    if not clouds:
        return np.empty((0, 3), dtype=np.float64)
    return np.concatenate(clouds, axis=0)


def _y_up_points(points: np.ndarray) -> np.ndarray:
    return points[:, [0, 2, 1]]


def _look_at_quat(wp: Any, eye: tuple[float, float, float], target: tuple[float, float, float]) -> Any:
    eye_np = np.asarray(eye, dtype=np.float32)
    target_np = np.asarray(target, dtype=np.float32)
    up_np = np.asarray((0.0, 0.0, 1.0), dtype=np.float32)
    forward = target_np - eye_np
    forward = forward / np.linalg.norm(forward)
    right = np.cross(forward, up_np)
    right = right / np.linalg.norm(right)
    up = np.cross(right, forward)
    up = up / np.linalg.norm(up)
    return wp.quat_from_matrix(
        wp.matrix_from_cols(
            wp.vec3(*right.tolist()),
            wp.vec3(*up.tolist()),
            wp.vec3(*(-forward).tolist()),
        )
    )


def _select_case(report: Mapping[str, Any], *, preferred_role: str) -> Mapping[str, Any]:
    for case in report.get("cases", []) or []:
        if isinstance(case, Mapping) and case.get("asset_role") == preferred_role:
            return case
    raise ValueError(f"Phase0 report missing case with asset_role={preferred_role}")


def _package_for_lane(case: Mapping[str, Any], lane: str) -> Mapping[str, Any] | None:
    lane_result = (case.get("baseline_results") or {}).get(lane) or {}
    package = lane_result.get("collision_package")
    return package if isinstance(package, Mapping) else None


def _probe_summary(case: Mapping[str, Any], lane: str) -> dict[str, Any]:
    probes = (case.get("probe_results") or {}).get(lane) or {}
    summary: dict[str, Any] = {}
    for probe in ("contact_canary", "body_state_drop_settle", "sphere_rain"):
        result = probes.get(probe) or {}
        if isinstance(result, Mapping):
            summary[probe] = {
                "outcome": result.get("outcome", "unknown"),
                "status": result.get("status", "unknown"),
            }
    return summary


def _write_sidecar(
    path: Path,
    *,
    slot: str,
    case: Mapping[str, Any],
    report_path: Path,
    asset_manifest_path: Path,
    newton_root: Path,
    newton_commit: str,
    source_artifact_root: Path,
    details: Mapping[str, Any],
) -> None:
    payload = {
        "schema_version": 1,
        "slot": slot,
        "renderer": "newton_sensor_tiled_camera",
        "image_size_px": list(SLOT_IMAGE_SIZE),
        "asset_id": case.get("asset_id", ""),
        "asset_role": case.get("asset_role", ""),
        "source_report": str(report_path),
        "source_report_sha256": _sha256_file(report_path),
        "source_manifest": str(asset_manifest_path),
        "source_manifest_sha256": _sha256_file(asset_manifest_path),
        "source_artifact_root": str(source_artifact_root),
        "newton": {
            "root": str(newton_root),
            "commit": newton_commit,
        },
        "claim_boundary": FIG1_NEWTON_CLAIM_BOUNDARY,
        "details": dict(details),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _git_commit(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--short=12", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "unknown"
    return result.stdout.strip()


def _prepend_pythonpath(paths: Sequence[Path], existing: str) -> str:
    parts = [str(path) for path in paths]
    if existing:
        parts.extend(part for part in existing.split(os.pathsep) if part)
    return os.pathsep.join(parts)


def _manifest_file_value(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _manifest_path_to_file(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate ACCV Fig.1 Newton-rendered slot images.")
    parser.add_argument("--worker-render", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--source-artifact-root", type=Path, default=DEFAULT_SOURCE_ARTIFACT_ROOT)
    parser.add_argument("--phase0-report", type=Path, default=DEFAULT_PHASE0_REPORT)
    parser.add_argument("--asset-manifest", type=Path, default=DEFAULT_PHASE0_ASSET_MANIFEST)
    parser.add_argument("--newton-root", type=Path, default=DEFAULT_NEWTON_ROOT)
    parser.add_argument("--python-executable", type=Path, default=DEFAULT_NEWTON_PYTHON)
    args = parser.parse_args(argv)
    if args.worker_render:
        return _worker_render_all(args)
    manifest = render_newton_slots_via_worker(
        output_dir=args.output_dir,
        source_artifact_root=args.source_artifact_root,
        python_executable=args.python_executable,
        newton_root=args.newton_root,
        phase0_report=args.phase0_report,
        asset_manifest=args.asset_manifest,
    )
    print(f"fig1_newton_slots: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
