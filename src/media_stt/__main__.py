"""Allow running the CLI with ``python -m media_stt``."""

from __future__ import annotations

import sys

from media_stt.cli import main

if __name__ == "__main__":
    sys.exit(main())
