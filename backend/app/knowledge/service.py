import hashlib
import re


def chunk_document(content: str, max_chars: int = 1200) -> list[str]:
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", content) if item.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > max_chars:
            chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}".strip()
    if current:
        chunks.append(current)
    return chunks or [content[:max_chars]]


def terms(content: str) -> list[str]:
    return sorted(set(re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{3,}", content.lower())))[:100]


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()
