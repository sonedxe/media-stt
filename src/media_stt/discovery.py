"""Resolve user input (files and directories) into a list of media files."""

from __future__ import annotations

import logging
from collections.abc import Iterable
from pathlib import Path

from media_stt.config import MEDIA_EXTENSIONS

logger = logging.getLogger(__name__)


def collect_inputs(raw_inputs: Iterable[str], *, recursive: bool = False) -> list[Path]:
    """Expand files and directories into a sorted, de-duplicated file list.

    Directories are scanned for known media extensions (non-recursively unless
    ``recursive`` is set). Missing paths are logged and skipped.
    """
    files: list[Path] = []
    for item in raw_inputs:
        path = Path(item).expanduser()
        if path.is_dir():
            files.extend(_from_directory(path, recursive))
        elif path.is_file():
            files.append(path)
        else:
            logger.warning("Skipping (not found): %s", path)
    return _deduplicate(files)


def _from_directory(directory: Path, recursive: bool) -> list[Path]:
    iterator = directory.rglob("*") if recursive else directory.iterdir()
    found = sorted(entry for entry in iterator if entry.is_file() and entry.suffix.lower() in MEDIA_EXTENSIONS)
    if not found:
        logger.warning("No media files found in %s", directory)
    return found


def _deduplicate(files: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    unique: list[Path] = []
    for file in files:
        resolved = file.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(file)
    return unique
