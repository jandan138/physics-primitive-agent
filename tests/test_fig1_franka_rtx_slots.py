from __future__ import annotations

import json
import os
from pathlib import Path

from PIL import Image

from primitive_collision_compiler.paper.fig1_franka_rtx_slots import (
    FIG1_FRANKA_RTX_CLAIM_BOUNDARY,
    FIG1_FRANKA_RTX_SLOT_NAMES,
    _add_recorded_link_boxes,
    _apply_franka_display_pose,
    build_franka_rtx_worker_command,
    franka_case_summary,
    load_franka_rtx_slot_manifest,
    select_franka_articulation_case,
    source_artifact_path,
    write_franka_rtx_slot_manifest,
)


def _slot_png(path: Path, color: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (64, 48), color).save(path)


def _franka_report() -> dict[str, object]:
    return {
        "articulation_cases": [
            {
                "asset_id": "franka_import_smoke",
                "asset_role": "franka_import_smoke",
                "local_path": "assets/raw/mirrors/franka/franka.usd",
                "robot_package_result": {
                    "status": "generated",
                    "primitive_or_hull_count": 12,
                    "collision_package": {"primitives": [{"kind": "box"}] * 12},
                    "link_boundary_audit": {
                        "status": "smoke_passed",
                        "metrics": {
                            "link_count": 12,
                            "primitive_count": 12,
                            "cross_link_merge_count": 0,
                            "meshless_link_placeholder_count": 1,
                        },
                    },
                },
            }
        ]
    }


class _FakeWp:
    @staticmethod
    def vec3(*values: float) -> tuple[float, float, float]:
        return tuple(values)  # type: ignore[return-value]

    @staticmethod
    def quat_identity() -> tuple[float, float, float, float]:
        return (0.0, 0.0, 0.0, 1.0)

    @staticmethod
    def transform(*, p: object, q: object) -> tuple[object, object]:
        return (p, q)


class _FakeBuilder:
    def __init__(self, body_label: list[str]) -> None:
        self.body_label = body_label
        self.boxes: list[dict[str, object]] = []

    def add_shape_box(self, body: int, **kwargs: object) -> None:
        self.boxes.append({"body": body, **kwargs})


def test_worker_command_uses_shared_newton_and_source_artifact_root(tmp_path: Path) -> None:
    command, env = build_franka_rtx_worker_command(
        output_dir=tmp_path / "slots",
        source_artifact_root=Path("/source/root"),
        python_executable=Path("/env/bin/python"),
        newton_root=Path("/shared/newton"),
        phase0_report=Path("reports/generated/phase0.json"),
        asset_manifest=Path("assets/manifests/franka.yaml"),
    )

    assert command[:3] == [
        "/env/bin/python",
        "-m",
        "primitive_collision_compiler.paper.fig1_franka_rtx_slots",
    ]
    assert "--worker-render" in command
    assert str(tmp_path / "slots") in command
    assert env["PPA_FIG1_SOURCE_ARTIFACT_ROOT"] == "/source/root"
    pythonpath_parts = env["PYTHONPATH"].split(os.pathsep)
    assert pythonpath_parts[0] == "/shared/newton"
    assert str(Path(__file__).resolve().parents[1] / "src") in pythonpath_parts
    assert str(Path(__file__).resolve().parents[1]) in pythonpath_parts


def test_source_artifact_path_uses_explicit_root_for_report_artifacts() -> None:
    assert source_artifact_path(
        "reports/generated/phase0.json",
        source_artifact_root=Path("/cpfs/source"),
    ) == Path("/cpfs/source/reports/generated/phase0.json")


def test_select_franka_articulation_case_requires_link_aware_smoke() -> None:
    case = select_franka_articulation_case(_franka_report())
    summary = franka_case_summary(case)

    assert summary["asset_role"] == "franka_import_smoke"
    assert summary["link_count"] == 12
    assert summary["primitive_count"] == 12
    assert summary["cross_link_merge_count"] == 0
    assert summary["meshless_link_placeholder_count"] == 1
    assert summary["robot_package_status"] == "generated"
    assert summary["link_boundary_status"] == "smoke_passed"


def test_select_franka_articulation_case_rejects_missing_smoke_audit() -> None:
    report = _franka_report()
    case = report["articulation_cases"][0]  # type: ignore[index]
    robot_result = case["robot_package_result"]  # type: ignore[index]
    robot_result["link_boundary_audit"]["status"] = "runtime_failure"  # type: ignore[index]

    try:
        select_franka_articulation_case(report)
    except ValueError as exc:
        assert "link_boundary_audit" in str(exc)
    else:
        raise AssertionError("Franka report without smoke-passed link audit should be rejected")


def test_recorded_link_boxes_fail_if_any_recorded_frame_is_missing() -> None:
    report = _franka_report()
    case = report["articulation_cases"][0]  # type: ignore[index]
    package = case["robot_package_result"]["collision_package"]  # type: ignore[index]
    package["primitives"] = [  # type: ignore[index]
        {
            "kind": "box",
            "frame": "/panda/panda_link0",
            "center": [0.0, 0.0, 0.0],
            "dimensions": {"half_extents": [0.1, 0.1, 0.1]},
        },
        {
            "kind": "box",
            "frame": "/panda/missing_link",
            "center": [0.0, 0.0, 0.0],
            "dimensions": {"half_extents": [0.1, 0.1, 0.1]},
        },
    ]
    builder = _FakeBuilder(body_label=["/panda/panda_link0"])

    try:
        _add_recorded_link_boxes(
            wp=_FakeWp,
            builder=builder,
            case=case,  # type: ignore[arg-type]
            color=(0.1, 0.2, 0.3),
            slot="candidate_package",
        )
    except ValueError as exc:
        assert "/panda/missing_link" in str(exc)
    else:
        raise AssertionError("missing recorded link-aware box frame should fail the worker")


def test_franka_display_pose_is_traceable_and_writes_first_nine_joint_coordinates() -> None:
    class _Builder:
        def __init__(self) -> None:
            self.joint_q = [0.0] * 9

    builder = _Builder()

    details = _apply_franka_display_pose(builder)

    assert len(details["joint_q"]) == 9
    assert builder.joint_q == details["joint_q"]
    assert details["source"] == "newton_examples_franka_ready_pose"
    assert "not manipulation evidence" in details["claim_boundary"]


def test_write_franka_rtx_slot_manifest_requires_three_rendered_slots(tmp_path: Path) -> None:
    slot_artifacts = {}
    colors = ("#6d8fbd", "#6aa27a", "#c58a45")
    for slot, color in zip(FIG1_FRANKA_RTX_SLOT_NAMES, colors):
        png = tmp_path / f"{slot}_franka_rtx.png"
        _slot_png(png, color)
        sidecar = tmp_path / f"{slot}_franka_rtx.json"
        sidecar.write_text(
            json.dumps(
                {
                    "slot": slot,
                    "renderer": "newton_viewer_rtx_ovrtx",
                    "claim_boundary": FIG1_FRANKA_RTX_CLAIM_BOUNDARY,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        slot_artifacts[slot] = {"png": png, "sidecar": sidecar}

    manifest_path = write_franka_rtx_slot_manifest(
        output_dir=tmp_path,
        slot_artifacts=slot_artifacts,
        source_report=Path("/source/report.json"),
        source_manifest=Path("/source/franka.yaml"),
        source_artifact_root=Path("/source"),
        newton_root=Path("/shared/newton"),
        newton_commit="abc123def456",
        ovrtx_version="0.3.0.312915",
    )

    manifest = load_franka_rtx_slot_manifest(manifest_path)
    assert manifest["mode"] == "newton_rtx_franka_render_slots"
    assert manifest["renderer"] == "newton_viewer_rtx_ovrtx"
    assert set(manifest["slots"]) == set(FIG1_FRANKA_RTX_SLOT_NAMES)
    assert manifest["newton"]["commit"] == "abc123def456"
    assert manifest["rtx"]["ovrtx_version"] == "0.3.0.312915"
    assert manifest["source_artifact_root"] == "/source"
    assert "not whole-robot collision quality" in manifest["claim_boundary"]
    for slot in FIG1_FRANKA_RTX_SLOT_NAMES:
        assert Path(manifest["slots"][slot]["image"]).is_file()
        assert Path(manifest["slots"][slot]["sidecar"]).is_file()


def test_write_franka_rtx_slot_manifest_rejects_missing_slot(tmp_path: Path) -> None:
    png = tmp_path / "asset_intake_franka_rtx.png"
    _slot_png(png, "#6d8fbd")
    sidecar = tmp_path / "asset_intake_franka_rtx.json"
    sidecar.write_text('{"renderer": "newton_viewer_rtx_ovrtx"}\n', encoding="utf-8")

    try:
        write_franka_rtx_slot_manifest(
            output_dir=tmp_path,
            slot_artifacts={"asset_intake": {"png": png, "sidecar": sidecar}},
            source_report=Path("/source/report.json"),
            source_manifest=Path("/source/franka.yaml"),
            newton_root=Path("/shared/newton"),
            newton_commit="abc123def456",
            ovrtx_version="0.3.0.312915",
        )
    except ValueError as exc:
        assert "candidate_package" in str(exc)
        assert "newton_diagnostics" in str(exc)
    else:
        raise AssertionError("missing Fig.1 Franka RTX slots should be rejected")
