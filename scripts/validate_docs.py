"""Repository documentation validation.

The checks are intentionally small and dependency-free so every reviewer can run them before
editing DeepDive material. They guard the current proposal against accidental safety or
deployment claims before the project has produced evidence.
"""

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse


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
