"""Media STT — local speech-to-text powered by Whisper MLX.

Transcribes any audio or video format that ffmpeg can decode, including
WhatsApp voice notes (``.opus`` / ``.ogg``). Everything runs offline on
Apple Silicon.

The command-line entry point lives in :func:`media_stt.cli.main`.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
