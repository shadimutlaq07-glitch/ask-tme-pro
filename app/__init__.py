from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

__all__ = ["BASE_DIR", "APP_DIR", "DATA_DIR", "LOGS_DIR"]
