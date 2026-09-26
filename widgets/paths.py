"""Local application data paths for DevPulse."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QStandardPaths


def app_data_dir() -> Path:
    """Return (and create) the per-user DevPulse data folder."""
    root = Path(
        QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
    )
    root.mkdir(parents=True, exist_ok=True)
    return root


def notes_path() -> Path:
    return app_data_dir() / "notes.json"
