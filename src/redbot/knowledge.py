from __future__ import annotations

from pathlib import Path

from redbot.store import RedbotStore

SUPPORTED_EXTENSIONS = {".md", ".markdown", ".txt"}


def import_path(store: RedbotStore, path: str | Path) -> int:
    target = Path(path)
    files = _iter_supported_files(target)
    imported = 0
    for file_path in files:
        content = file_path.read_text(encoding="utf-8", errors="replace").strip()
        if not content:
            continue
        store.add_document(title=file_path.name, content=content, source=str(file_path))
        imported += 1
    return imported


def _iter_supported_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in SUPPORTED_EXTENSIONS else []
    if path.is_dir():
        return [
            child
            for child in sorted(path.rglob("*"))
            if child.is_file() and child.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
    raise FileNotFoundError(f"Knowledge import path does not exist: {path}")
