from __future__ import annotations

from pathlib import Path
import re
import sys

SITE_ROOTS = (
    Path("site/src/layouts"),
    Path("site/src/pages/paper"),
    Path("site/src/content/paper"),
    Path("site/src/data"),
)
REQUIRED_BANNER = "The English paper text and translated text describe the CPD paper."
UNSUPPORTED_PERMISSION_WORDS = (
    "Authorized bilingual companion",
    "Authorized bilingual CPD paper companion",
    "authorized bilingual paper companion",
    "authorized_bilingual_companion",
)
STALE_PUBLICATION_GATING_COPY = (
    "Public full-text expansion should wait for the private permission record"
)
PERMISSION_RECORD_GLOB = "docs/records/*cpd-paper-permission*.md"
PERMISSION_EVIDENCE_MARKERS = (
    "permission has been granted",
    "permission_status: user_confirmed_private_permission",
    "permission_status: user_asserted_permission_record_pending",
)
READER_VISIBLE_INTERNAL_PAPER_LABEL_RE = re.compile(
    r'\b(?:label|title)="[^"]+ / '
    r'(?:figure\*?|wrapfigure|SCfigure|table\*?|algorithm\*?|align|equation) / '
    r'[^"]+"'
)
UNRESOLVED_PAPER_REFERENCE_RE = re.compile(
    r"\b(?:Fig|Tab|Alg|Eq|Sec)\.\s+[a-z][A-Za-z0-9_-]*\b"
    r"|(?:图|表|算法|式)\s+[a-z][A-Za-z0-9_-]*\b"
    r"|第\s+[a-z][A-Za-z0-9_-]*\s+节"
)


def validate_site_text(path: str, text: str, has_permission_record: bool = False) -> list[str]:
    issues: list[str] = []
    for phrase in UNSUPPORTED_PERMISSION_WORDS:
        if phrase in text:
            issues.append(f"{path}: permission wording must stay record-pending until evidence is attached")
    if STALE_PUBLICATION_GATING_COPY in text:
        issues.append(f"{path}: stale publication gating copy conflicts with current publication state")
    if re.search(r"href=\{?`?[\"']?/paper/", text):
        issues.append(f"{path}: hardcoded root-relative paper href; use BASE_URL-aware links")
    if '"/physics-primitive-agent/' in text or "'/physics-primitive-agent/" in text:
        issues.append(f"{path}: hardcoded GitHub Pages base path; use BASE_URL-aware paths")
    unsupported_reproduction = re.findall(r'reproductionStatus="([^"]+)"', text)
    for status in unsupported_reproduction:
        if status != "not_started":
            issues.append(f"{path}: reproduction status {status!r} requires a dated reproduction record")
    if 'translation=""' in text:
        issues.append(f"{path}: empty draft translation is not allowed in generated paper content")
    if (
        "paper-assets/" in text
        and "withheld until the permission record" not in text
        and not has_permission_record
    ):
        issues.append(f"{path}: paper asset publication requires attached permission evidence")
    if "<LatexBlock" in text and "/ control /" in text:
        issues.append(f"{path}: reader-visible LaTeX control should be omitted from generated content")
    if path.startswith("site/src/content/paper/") and "<LatexBlock" in text:
        issues.append(f"{path}: reader-visible LaTeX source block should be rendered or omitted")
    if (
        path.startswith("site/src/content/paper/")
        and READER_VISIBLE_INTERNAL_PAPER_LABEL_RE.search(text)
    ):
        issues.append(f"{path}: reader-visible internal paper block label should use paper numbering")
    if path.startswith("site/src/content/paper/") and 'label="Display equation"' in text:
        issues.append(f"{path}: reader-visible generic equation label should be omitted or numbered")
    if path.startswith("site/src/content/paper/") and 'title="Figure"' in text:
        issues.append(f"{path}: reader-visible generic figure label should be omitted or named")
    if path.startswith("site/src/content/paper/") and 'caption="Source-paper figure."' in text:
        issues.append(f"{path}: reader-visible placeholder figure caption should be omitted")
    if path.startswith("site/src/content/paper/") and UNRESOLVED_PAPER_REFERENCE_RE.search(text):
        issues.append(f"{path}: unresolved paper reference token should be numbered")
    if "site/src/pages/paper" in path and REQUIRED_BANNER not in text and "PaperLayout" not in text:
        issues.append(f"{path}: missing source namespace banner")
    if "PaperBlock" in text and 'sourceNamespace="cpd_paper_source_text"' not in text:
        issues.append(f"{path}: PaperBlock missing cpd_paper_source_text namespace")
    if "translationStatus=" in text and 'translationStatus="draft_ai_assisted"' not in text:
        issues.append(f"{path}: unexpected translation status in MVP")
    return issues


def has_paper_asset_permission_evidence(root: Path) -> bool:
    for record_path in root.glob(PERMISSION_RECORD_GLOB):
        text = record_path.read_text(encoding="utf-8")
        if any(marker in text for marker in PERMISSION_EVIDENCE_MARKERS):
            return True
    return False


def validate_site(root: Path) -> list[str]:
    issues: list[str] = []
    has_permission_record = has_paper_asset_permission_evidence(root)
    layout_path = root / "site/src/layouts/PaperLayout.astro"
    if layout_path.exists() and REQUIRED_BANNER not in layout_path.read_text(encoding="utf-8"):
        issues.append("site/src/layouts/PaperLayout.astro: missing source namespace banner")
    for site_root in SITE_ROOTS:
        path = root / site_root
        if not path.exists():
            continue
        for file_path in sorted(path.rglob("*")):
            if file_path.suffix not in {".astro", ".mdx", ".json"}:
                continue
            relative = file_path.relative_to(root).as_posix()
            issues.extend(
                validate_site_text(
                    relative,
                    file_path.read_text(encoding="utf-8"),
                    has_permission_record=has_permission_record,
                )
            )
    return issues


def main() -> int:
    issues = validate_site(Path.cwd())
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        return 1
    print("site claim validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
