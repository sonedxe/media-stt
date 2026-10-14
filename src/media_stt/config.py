"""Project-wide constants and defaults."""

from __future__ import annotations

DEFAULT_OUTPUT_DIR = "output"

# Default model per backend. MLX uses Hugging Face repos; faster-whisper uses
# its own size names (tiny, base, small, medium, large-v3, ...).
DEFAULT_MODELS = {
    "mlx": "mlx-community/whisper-medium-mlx",
    "faster-whisper": "medium",
}

# Whisper models are trained on 16 kHz mono PCM audio.
SAMPLE_RATE = 16_000
CHANNELS = 1

# Extensions accepted when a directory is scanned for media.
AUDIO_EXTENSIONS = frozenset(
    {
        ".opus",
        ".ogg",
        ".oga",
        ".m4a",
        ".mp3",
        ".wav",
        ".aac",
        ".flac",
        ".wma",
        ".amr",
        ".aiff",
        ".aif",
    }
)

VIDEO_EXTENSIONS = frozenset({".mp4", ".mkv", ".mov", ".webm", ".m4v", ".avi"})

MEDIA_EXTENSIONS = AUDIO_EXTENSIONS | VIDEO_EXTENSIONS
