"""System tray icon and context menu for background operation."""

from __future__ import annotations

from PyQt6.QtGui import QAction, QColor, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QWidget


def build_tray_icon() -> QIcon:
    """Draw a simple pulse mark so the app does not depend on image assets."""
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(0, 0, 0, 0))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor("#7C6CFF"))
    painter.setPen(QColor("#2A2A2A"))
    painter.drawRoundedRect(8, 8, 48, 48, 14, 14)
    painter.setPen(QColor("#F2F2F2"))
    painter.drawArc(18, 22, 28, 20, 30 * 16, 120 * 16)
    painter.drawArc(18, 28, 28, 20, -30 * 16, -120 * 16)
    painter.end()
    return QIcon(pixmap)


class TrayController(QSystemTrayIcon):
    """Keeps DevPulse reachable after the window is hidden."""

    def __init__(self, window: QWidget) -> None:
        super().__init__(build_tray_icon(), window)
        self._window = window
        self.setToolTip("DevPulse")

        menu = QMenu()
        show_action = QAction("Show DevPulse", menu)
        show_action.triggered.connect(self.show_window)
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(show_action)
        menu.addSeparator()
        menu.addAction(quit_action)
        self.setContextMenu(menu)
        self.activated.connect(self._on_activated)

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window()

    def show_window(self) -> None:
        self._window.show_animated()
        self._window.raise_()
        self._window.activateWindow()

    def quit_app(self) -> None:
        self._window.request_quit()
