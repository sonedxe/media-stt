"""Transcriber registry and platform-aware selection."""

from __future__ import annotations

import importlib.util
import platform
import sys

from media_stt.config import DEFAULT_MODELS
from media_stt.transcribers.base import Transcriber
from media_stt.transcribers.faster_whisper import FasterWhisperTranscriber
from media_stt.transcribers.mlx import MlxTranscriber


class TranscriberError(RuntimeError):
    """Raised when a transcriber cannot be selected or is not installed."""


_REGISTRY = {
    "mlx": (MlxTranscriber, "mlx_whisper"),
    "faster-whisper": (FasterWhisperTranscriber, "faster_whisper"),
}


def is_apple_silicon() -> bool:
    return sys.platform == "darwin" and platform.machine() == "arm64"


def default_transcriber_name() -> str:
    return "mlx" if is_apple_silicon() else "faster-whisper"


def supported_transcribers() -> tuple[str, ...]:
    return tuple(_REGISTRY)


def is_installed(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def create_transcriber(
    name: str | None = None,
    model: str | None = None,
    language: str | None = None,
) -> Transcriber:
    """Instantiate a transcriber, defaulting to the platform-appropriate one."""
    name = name or default_transcriber_name()
    if name not in _REGISTRY:
        raise TranscriberError(f"Unknown transcriber '{name}'. Choose one of: {', '.join(_REGISTRY)}")

    transcriber_class, module = _REGISTRY[name]
    if not is_installed(module):
        raise TranscriberError(
            f"Transcriber '{name}' is not installed. Install it with: pip install {module.replace('_', '-')}"
        )

    return transcriber_class(model=model or DEFAULT_MODELS[name], language=language)
