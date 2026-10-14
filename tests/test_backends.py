"""Tests for :mod:`media_stt.backends`."""

from __future__ import annotations

import pytest

from media_stt.backends import (
    BackendError,
    create_backend,
    default_backend_name,
    is_installed,
    supported_backends,
)

_MODULES = {"mlx": "mlx_whisper", "faster-whisper": "faster_whisper"}


def test_default_backend_is_supported() -> None:
    assert default_backend_name() in supported_backends()


def test_unknown_backend_raises() -> None:
    with pytest.raises(BackendError):
        create_backend("does-not-exist", None, None)


def test_uninstalled_backend_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("media_stt.backends.is_installed", lambda module: False)
    with pytest.raises(BackendError):
        create_backend("faster-whisper", None, None)


def test_create_backend_resolves_default_model() -> None:
    name = default_backend_name()
    if not is_installed(_MODULES[name]):
        pytest.skip(f"{name} is not installed")

    backend = create_backend(name, None, None)

    assert backend.name == name
    assert backend.model


def test_explicit_model_overrides_default() -> None:
    name = default_backend_name()
    if not is_installed(_MODULES[name]):
        pytest.skip(f"{name} is not installed")

    backend = create_backend(name, "custom-model", None)

    assert backend.model == "custom-model"
