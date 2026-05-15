from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TranslationEntry:
    paragraph_id: str
    original: str
    translation: str
    status: str = "draft_ai_assisted"
    source_hash: str = ""
    translated_at: str = "2026-05-15"
    translator: str = "codex"
    prompt_policy: str = "faithful_technical_draft_translation"


def entries_to_dict(entries: tuple[TranslationEntry, ...]) -> dict[str, str]:
    return {entry.paragraph_id: entry.translation for entry in entries}
