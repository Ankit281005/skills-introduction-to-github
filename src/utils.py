"""Utility helpers for the hospital data pipeline."""

from __future__ import annotations

from pathlib import Path


REQUIRED_DIRS = ["data", "bronze", "silver", "gold", "visualizations"]


def ensure_directories(project_root: Path) -> None:
    """Create all required pipeline directories if they do not exist."""
    for dir_name in REQUIRED_DIRS:
        (project_root / dir_name).mkdir(parents=True, exist_ok=True)


def log_step(message: str) -> None:
    """Print a consistently formatted pipeline step log message."""
    print(f"[pipeline] {message}")
