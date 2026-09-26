"""Vertical navigator for the three primary DevPulse panels."""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QWidget


NAV_ITEMS = (
    ("monitor", "◎  System Monitor"),
    ("pomodoro", "◷  Pomodoro"),
    ("notes", "✎  Quick Notes"),
)


class Sidebar(QFrame):
    """Card-style sidebar that emits the selected panel id."""

    page_changed = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(176)
        self._buttons: dict[str, QPushButton] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 12, 10, 12)
        layout.setSpacing(6)

        for page_id, label in NAV_ITEMS:
            btn = QPushButton(label)
            btn.setObjectName("navBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("active", "false")
            btn.clicked.connect(lambda _checked=False, pid=page_id: self.select(pid))
            self._buttons[page_id] = btn
            layout.addWidget(btn)

        layout.addStretch()
        self.select("monitor")

    def select(self, page_id: str) -> None:
        """Mark a nav item as active and notify the stacked view."""
        for pid, btn in self._buttons.items():
            btn.setProperty("active", "true" if pid == page_id else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self.page_changed.emit(page_id)
