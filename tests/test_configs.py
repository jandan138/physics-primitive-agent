from pathlib import Path
import subprocess

import yaml

from primitive_collision_compiler.config import load_compile_config


ROOT = Path(__file__).resolve().parents[1]


def test_deepdive_mvp_config_loads():
    config = load_compile_config(ROOT / "configs" / "deepdive" / "mvp.yaml")

    assert config.asset_id == "handle_gap_mvp"
    assert config.asset_path == "assets/examples/handle_gap.usda"
    assert config.task == "grasping"
    assert config.method == "simulation_checked_primitive_candidates"
    assert config.max_primitives == 16


def test_phase0_baseline_config_loads():
    config = load_compile_config(ROOT / "configs" / "experiments" / "phase0_baseline.yaml")

    assert config.asset_id == "phase0_asset_manifest"
    assert config.asset_path == "assets/manifests/phase0_assets.yaml"
    assert config.task == "phase0_simulation_checked_diagnostic"
    assert config.verify == (
        "body_state_drop_settle",
        "stack_or_slide",
        "sphere_rain",
        "link_boundary_audit",
        "articulation_smoke_if_robot",
        "precision_rejection",
    )
    assert config.protocol["phase0_defaults"]["seeds"] == 3


def test_phase0_config_references_existing_structured_manifest():
    config_path = ROOT / "configs" / "experiments" / "phase0_baseline.yaml"
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    manifest_path = ROOT / data["asset"]["path"]
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    assert manifest_path.exists()
    assert len(manifest["assets"]) >= 5
    assert {asset["role"] for asset in manifest["assets"]} >= {
        "rigid_prop",
        "stackable",
        "contact_affordance",
        "container",
        "precision_negative_control",
    }


def test_phase0_manifest_uses_repo_local_grscenes_mirrors():
    manifest_path = ROOT / "assets" / "manifests" / "phase0_assets.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    manifest_id = "phase0_grscenes_assets_2026_05_25"
    source_root = (
        "/cpfs/user/zhuzihou/assets/dedup_workspaces/"
        "test0_transitive_apply_parallel/dataset/GRScenes_assets/"
    )
    mirror_prefix = f"assets/raw/mirrors/{manifest_id}/"
    placeholder_ids = {
        "rigid_prop_01",
        "stackable_01",
        "contact_affordance_01",
        "container_01",
        "precision_negative_control_01",
    }

    assert manifest["manifest_id"] == manifest_id
    assert manifest["materialization_report"].endswith(".json")
    assert len(manifest["assets"]) >= 5
    assert not placeholder_ids & {asset["id"] for asset in manifest["assets"]}

    for asset in manifest["assets"]:
        materialization = asset["materialization"]
        dependency_summary = materialization["dependency_summary"]
        dependency_files = materialization["localized_dependency_files"]
        extensions = materialization["local_file_extensions"]

        assert asset["id"].startswith("grscenes_")
        assert asset["source_path"].startswith(source_root)
        assert asset["path"] == asset["local_path"]
        assert asset["path"].startswith(mirror_prefix)
        assert Path(asset["path"]).name == Path(asset["source_path"]).name
        assert not asset["path"].startswith(source_root)
        assert asset["provenance_status"] == "source_recorded_license_unreviewed"
        assert materialization["status"] == "materialized"
        assert materialization["method"] == "pxr_usdutils_localize_asset"
        assert materialization["local_file_count"] == len(dependency_files) + 1
        assert materialization["local_file_count"] >= dependency_summary["asset_count"] + 1
        assert dependency_summary["unresolved_count"] == 0
        assert materialization["unresolved_dependencies"] == []
        assert extensions[".usd"] == 1
        assert extensions[".mdl"] >= 1
        assert extensions[".png"] >= 1
        assert any(path.endswith(".mdl") for path in dependency_files)
        assert any(path.endswith(".png") for path in dependency_files)

        ignored = subprocess.run(
            ["git", "check-ignore", "--quiet", asset["path"]],
            cwd=ROOT,
            check=False,
        )
        assert ignored.returncode == 0

    ignored_report = subprocess.run(
        ["git", "check-ignore", "--quiet", manifest["materialization_report"]],
        cwd=ROOT,
        check=False,
    )
    assert ignored_report.returncode == 0

    tracked_raw_outputs = subprocess.run(
        ["git", "ls-files", "assets/raw", "reports/generated"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert tracked_raw_outputs.stdout == ""


def test_phase0_config_defines_baselines_probes_and_required_metrics():
    config_path = ROOT / "configs" / "experiments" / "phase0_baseline.yaml"
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    baselines = data["phase0_defaults"]["baselines"]
    cpd_like = data["phase0_defaults"]["cpd_like"]
    probes = data["phase0_defaults"]["probes"]
    required_metrics = set(data["phase0_defaults"]["required_metrics"])

    assert {baseline["id"] for baseline in baselines} >= {
        "bounding_primitive",
        "single_convex_hull",
        "coacd_or_vhacd_if_available",
        "cpd_style_primitive_candidate_if_available",
    }
    assert probes["body_state_drop_settle"]["initial_conditions"]["height_m"] == 0.25
    assert "body_state_delta" in probes["body_state_drop_settle"]["metrics"]
    assert probes["stack_or_slide"]["metrics"] == [
        "displacement",
        "contact_count_p95",
        "penetration_or_jitter",
    ]
    assert probes["sphere_rain"]["initial_conditions"]["sphere_count"] == 32
    assert probes["link_boundary_audit"]["pass_condition"] == "zero_cross_link_merges"
    assert (
        probes["articulation_smoke_if_robot"]["pass_condition"]
        == "complete_and_label_articulation_failures"
    )
    assert probes["precision_rejection"]["pass_condition"] == "reject_or_fallback"
    assert cpd_like["component_merge"] == "virtual_pairwise"
    assert cpd_like["max_source_faces_by_role"]["container"] == 256
    assert "displacement" in required_metrics
    assert "link_boundary_status" in required_metrics
