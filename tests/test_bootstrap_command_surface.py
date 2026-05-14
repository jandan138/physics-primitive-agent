import importlib
import importlib.util
from pathlib import Path


def test_package_imports():
    package = importlib.import_module("primitive_collision_compiler")

    assert package.__version__ == "0.1.0"


def test_docs_validation_stub_returns_success():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "validate_docs.py"
    spec = importlib.util.spec_from_file_location("validate_docs", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.main() in (0, None)


def test_cli_help_mentions_project(capsys):
    cli = importlib.import_module("primitive_collision_compiler.cli")

    assert cli.main([]) == 0

    output = capsys.readouterr().out
    assert "Newton Primitive Collision Compiler" in output


def test_cli_rejects_non_dry_run_compile(capsys):
    cli = importlib.import_module("primitive_collision_compiler.cli")

    try:
        cli.main(["--config", "tests/fixtures/dry_run_mvp.yaml"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("non-dry-run compilation should exit")

    error = capsys.readouterr().err
    assert "non-dry-run compilation is not implemented yet" in error
