from pathlib import Path

from primitive_collision_compiler.config import load_compile_config


ROOT = Path(__file__).resolve().parents[1]


def test_deepdive_mvp_config_loads():
    config = load_compile_config(ROOT / "configs" / "deepdive" / "mvp.yaml")

    assert config.asset_path == "assets/examples/handle_gap.usda"
    assert config.task == "grasping"
    assert config.method == "primitive_first"
    assert config.max_primitives == 16


def test_phase0_baseline_config_loads():
    config = load_compile_config(ROOT / "configs" / "experiments" / "phase0_baseline.yaml")

    assert config.asset_path == "assets/manifests/phase0_assets.yaml"
    assert config.task == "phase0_diagnostic"
    assert config.verify == ("drop", "stack_or_slide", "sphere_rain", "precision_rejection")
