"""Tests for :mod:`media_stt.transcribers`."""

from __future__ import annotations

import pytest

from media_stt.transcribers import (
    TranscriberError,
    create_transcriber,
    default_transcriber_name,
    is_installed,
    supported_transcribers,
)

_MODULES = {"mlx": "mlx_whisper", "faster-whisper": "faster_whisper"}


def test_default_transcriber_is_supported() -> None:
    assert default_transcriber_name() in supported_transcribers()


def test_unknown_transcriber_raises() -> None:
    with pytest.raises(TranscriberError):
        create_transcriber("does-not-exist", None, None)


def test_uninstalled_transcriber_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("media_stt.transcribers.is_installed", lambda module: False)
    with pytest.raises(TranscriberError):
        create_transcriber("faster-whisper", None, None)


def test_create_transcriber_resolves_default_model() -> None:
    name = default_transcriber_name()
    if not is_installed(_MODULES[name]):
        pytest.skip(f"{name} is not installed")

    transcriber = create_transcriber(name, None, None)

    assert transcriber.name == name
    assert transcriber.model


def test_explicit_model_overrides_default() -> None:
    name = default_transcriber_name()
    if not is_installed(_MODULES[name]):
        pytest.skip(f"{name} is not installed")

    transcriber = create_transcriber(name, "custom-model", None)

    assert transcriber.model == "custom-model"
