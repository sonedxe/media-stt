"""Backend registry and platform-aware selection."""

from __future__ import annotations

import importlib.util
import platform
import sys

from media_stt.backends.base import Backend
from media_stt.backends.faster_whisper_backend import FasterWhisperBackend
from media_stt.backends.mlx_backend import MlxBackend
from media_stt.config import DEFAULT_MODELS


class BackendError(RuntimeError):
    """Raised when a backend cannot be selected or is not installed."""


_REGISTRY = {
    "mlx": (MlxBackend, "mlx_whisper"),
    "faster-whisper": (FasterWhisperBackend, "faster_whisper"),
}


def is_apple_silicon() -> bool:
    return sys.platform == "darwin" and platform.machine() == "arm64"


def default_backend_name() -> str:
    return "mlx" if is_apple_silicon() else "faster-whisper"


def supported_backends() -> tuple[str, ...]:
    return tuple(_REGISTRY)


def is_installed(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def create_backend(name: str | None = None, model: str | None = None, language: str | None = None) -> Backend:
    """Instantiate a backend, defaulting to the platform-appropriate one."""
    name = name or default_backend_name()
    if name not in _REGISTRY:
        raise BackendError(f"Unknown backend '{name}'. Choose one of: {', '.join(_REGISTRY)}")

    backend_class, module = _REGISTRY[name]
    if not is_installed(module):
        raise BackendError(
            f"Backend '{name}' is not installed. Install it with: pip install {module.replace('_', '-')}"
        )

    return backend_class(model=model or DEFAULT_MODELS[name], language=language)
