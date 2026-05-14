from pathlib import Path

import yaml

from primitive_collision_compiler.config import load_compile_config


ROOT = Path(__file__).resolve().parents[1]


def test_deepdive_mvp_config_loads():
    config = load_compile_config(ROOT / "configs" / "deepdive" / "mvp.yaml")

    assert config.asset_id == "handle_gap_mvp"
    assert config.asset_path == "assets/examples/handle_gap.usda"
    assert config.task == "grasping"
    assert config.method == "primitive_first"
    assert config.max_primitives == 16


def test_phase0_baseline_config_loads():
    config = load_compile_config(ROOT / "configs" / "experiments" / "phase0_baseline.yaml")

    assert config.asset_id == "phase0_asset_manifest"
    assert config.asset_path == "assets/manifests/phase0_assets.yaml"
    assert config.task == "phase0_diagnostic"
    assert config.verify == ("drop", "stack_or_slide", "sphere_rain", "precision_rejection")
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


def test_phase0_config_defines_baselines_probes_and_required_metrics():
    config_path = ROOT / "configs" / "experiments" / "phase0_baseline.yaml"
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    baselines = data["phase0_defaults"]["baselines"]
    probes = data["phase0_defaults"]["probes"]
    required_metrics = set(data["phase0_defaults"]["required_metrics"])

    assert {baseline["id"] for baseline in baselines} >= {
        "bounding_primitive",
        "single_convex_hull",
        "coacd_or_vhacd_if_available",
    }
    assert probes["drop"]["initial_conditions"]["height_m"] == 0.25
    assert probes["stack_or_slide"]["metrics"] == [
        "displacement",
        "contact_count_p95",
        "penetration_or_jitter",
    ]
    assert probes["sphere_rain"]["initial_conditions"]["sphere_count"] == 32
    assert probes["precision_rejection"]["pass_condition"] == "reject_or_fallback"
    assert "displacement" in required_metrics
