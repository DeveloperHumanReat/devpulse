"""Custom frameless title bar with drag support and window controls."""

from __future__ import annotations

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget


class TitleBar(QFrame):
    """Header that moves the parent window and hosts pin/min/close actions."""

    pin_toggled = pyqtSignal(bool)
    minimize_requested = pyqtSignal()
    close_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(52)
        self._drag_pos: QPoint | None = None
        self._pinned = False

        title = QLabel("DevPulse")
        title.setObjectName("appTitle")
        subtitle = QLabel("desktop pulse")
        subtitle.setObjectName("appSubtitle")

        text_col = QWidget()
        text_layout = QHBoxLayout(text_col)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(8)
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)
        text_layout.addStretch()

        self.pin_btn = self._make_btn("📌", "pinBtn", "Always on top")
        self.pin_btn.setProperty("pinned", "false")
        self.pin_btn.clicked.connect(self._toggle_pin)

        self.min_btn = self._make_btn("–", "windowBtn", "Minimize to tray")
        self.min_btn.clicked.connect(self.minimize_requested.emit)

        self.close_btn = self._make_btn("✕", "closeBtn", "Hide to tray")
        self.close_btn.clicked.connect(self.close_requested.emit)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 8, 12, 8)
        layout.setSpacing(6)
        layout.addWidget(text_col, 1)
        layout.addWidget(self.pin_btn)
        layout.addWidget(self.min_btn)
        layout.addWidget(self.close_btn)

    def _make_btn(self, text: str, object_name: str, tooltip: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName(object_name)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(28, 28)
        return btn

    def _toggle_pin(self) -> None:
        self._pinned = not self._pinned
        self.pin_btn.setProperty("pinned", "true" if self._pinned else "false")
        self.pin_btn.style().unpolish(self.pin_btn)
        self.pin_btn.style().polish(self.pin_btn)
        self.pin_toggled.emit(self._pinned)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            window = self.window()
            self._drag_pos = event.globalPosition().toPoint() - window.frameGeometry().topLeft()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if self._drag_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        self._drag_pos = None
        super().mouseReleaseEvent(event)
