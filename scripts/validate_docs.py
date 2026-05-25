"""Repository documentation validation.

The checks are intentionally small so every reviewer can run them before editing DeepDive
material. They guard the current proposal against accidental safety or deployment claims before
the project has produced evidence.
"""

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

import yaml


@dataclass(frozen=True)
class ClaimIssue:
    term: str
    line_number: int
    line: str
    path: str = "<text>"

    def format(self) -> str:
        return f"{self.path}:{self.line_number}: unscoped claim term '{self.term}': {self.line}"


DANGEROUS_TERMS = (
    "certified safe",
    "proven safe",
    "deployment-ready",
    "fully replaces",
    "guarantees",
    "guarantee",
)

SCOPING_MARKERS = (
    "do not claim",
    "must not claim",
    "should not claim",
    "cannot claim",
    "not claim",
    "forbidden claim",
    "unsafe claim",
    "non-goal",
    "non-goals",
    "not yet",
    "does not",
    "do not",
    "must not",
    "cannot",
    "no ",
    "without evidence",
    "requires evidence",
    "requires phase",
    "requires successful",
)

REQUIRED_PATHS = (
    "AGENTS.md",
    "README.md",
    "paper/README.md",
    "paper/shared/evidence/claims.yaml",
    "paper/shared/evidence/results_manifest.yaml",
    "assets/manifests/phase0_assets.yaml",
    "configs/deepdive/mvp.yaml",
    "configs/experiments/phase0_baseline.yaml",
    "docs/index.md",
    "docs/deepdive/message-map.md",
    "docs/deepdive/application.md",
    "docs/deepdive/evidence-status.md",
    "docs/design/evaluation-plan.md",
    "docs/design/benchmark-protocol.md",
    "docs/reference/claim-boundaries.md",
    "docs/reference/literature-map.md",
    "docs/reference/newton-notes.md",
    "docs/reference/related-work-notes.md",
    "docs/records/README.md",
    "experiments/registry.yaml",
    "assets/README.md",
    "reports/README.md",
    "archive/README.md",
)

SCAN_PATHS = (
    Path("AGENTS.md"),
    Path("CONTRIBUTING.md"),
    Path("README.md"),
    Path("archive"),
    Path("assets"),
    Path("docs/deepdive"),
    Path("docs/design"),
    Path("docs/records"),
    Path("docs/reference"),
    Path("docs/superpowers"),
    Path("docs/index.md"),
    Path("experiments"),
    Path("reports"),
)

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def _strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]+`", "", line)


def _has_scoping_marker(line: str) -> bool:
    lower = line.lower()
    return any(marker in lower for marker in SCOPING_MARKERS)


def _find_term(line: str) -> str | None:
    lower = line.lower()
    for term in DANGEROUS_TERMS:
        pattern = re.compile(rf"(?<![\w-]){re.escape(term)}(?![\w-])")
        if pattern.search(lower):
            return term
    return None


def find_claim_boundary_issues(text: str, path: str = "<text>") -> list[ClaimIssue]:
    """Return unscoped dangerous claim terms from Markdown/plain text."""

    issues: list[ClaimIssue] = []
    in_fence = False

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        searchable = _strip_inline_code(line)
        term = _find_term(searchable)
        if term is None or _has_scoping_marker(searchable):
            continue
        issues.append(ClaimIssue(term=term, line_number=line_number, line=line.strip(), path=path))

    return issues


def validate_required_paths(root: Path) -> list[str]:
    """Return missing required documentation paths."""

    missing: list[str] = []
    for relative_path in REQUIRED_PATHS:
        if not (root / relative_path).exists():
            missing.append(f"missing required file: {relative_path}")
    return missing


def _strip_anchor(target: str) -> str:
    return target.split("#", 1)[0]


def _is_external_or_special_link(target: str) -> bool:
    parsed = urlparse(target)
    return bool(parsed.scheme) or target.startswith("#") or target.startswith("mailto:")


def validate_local_markdown_links(root: Path, files: list[Path]) -> list[str]:
    """Return missing local Markdown link targets for the given files."""

    issues: list[str] = []
    for path in sorted(files):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in MARKDOWN_LINK_RE.finditer(line):
                raw_target = match.group(1).strip()
                target = _strip_anchor(unquote(raw_target))
                if not target or _is_external_or_special_link(raw_target):
                    continue

                target_path = (path.parent / target).resolve()
                try:
                    target_path.relative_to(root.resolve())
                except ValueError:
                    issues.append(f"{relative}:{line_number}: local link escapes repo: {raw_target}")
                    continue

                if not target_path.exists():
                    issues.append(
                        f"{relative}:{line_number}: missing local link target: {raw_target}"
                    )
    return issues


def _record_status(text: str) -> str | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip().lower() != "## status":
            continue
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                return None
            return stripped
    return None


def validate_registry_records(root: Path) -> list[str]:
    """Return registry entries whose record or claim-boundary metadata is stale."""

    registry_path = root / "experiments" / "registry.yaml"
    if not registry_path.exists():
        return []

    relative_registry = registry_path.relative_to(root).as_posix()
    try:
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return [f"{relative_registry}: invalid YAML: {exc}"]

    experiments = registry.get("experiments")
    if not isinstance(experiments, list):
        return [f"{relative_registry}: expected top-level experiments list"]

    issues: list[str] = []
    for index, entry in enumerate(experiments):
        if not isinstance(entry, dict):
            issues.append(f"{relative_registry}: entry {index}: expected mapping")
            continue

        entry_id = str(entry.get("id", f"entry {index}"))
        status = entry.get("status")
        record = entry.get("record")
        claims_supported = entry.get("claims_supported")

        if not isinstance(record, str) or not record:
            issues.append(f"{relative_registry}: {entry_id}: missing record path")
            continue

        record_path = root / record
        if not record_path.exists():
            issues.append(
                f"{relative_registry}: {entry_id}: missing record target: {record}"
            )
            continue

        if status != "complete":
            continue

        record_text = record_path.read_text(encoding="utf-8")
        record_status = _record_status(record_text)
        if record_status is None or not record_status.startswith("Complete"):
            issues.append(
                f"{relative_registry}: {entry_id}: complete registry entry points to "
                f"non-complete record: {record}"
            )

        if not isinstance(claims_supported, list) or not claims_supported:
            issues.append(
                f"{relative_registry}: {entry_id}: complete registry entry needs "
                "claims_supported"
            )
            continue

        if not any(
            any(marker in str(claim).lower() for marker in ("no ", "not ", "without", "only"))
            for claim in claims_supported
        ):
            issues.append(
                f"{relative_registry}: {entry_id}: claims_supported needs an explicit "
                "claim boundary"
            )

    return issues


def _iter_scan_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for scan_path in SCAN_PATHS:
        path = root / scan_path
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
    return sorted(files)


def validate_repository(root: Path) -> list[str]:
    issues = validate_required_paths(root)
    files = _iter_scan_files(root)

    for path in files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root).as_posix()
        issues.extend(issue.format() for issue in find_claim_boundary_issues(text, relative))

    issues.extend(validate_local_markdown_links(root, files))
    issues.extend(validate_registry_records(root))

    return issues


def main():
    root = Path.cwd()
    issues = validate_repository(root)
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1

    print("docs validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
