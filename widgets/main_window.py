"""Frameless glassmorphism shell that hosts the DevPulse panels."""

from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .notes import QuickNotesWidget
from .pomodoro import PomodoroWidget
from .sidebar import Sidebar
from .styles import APP_QSS
from .system_monitor import SystemMonitorWidget
from .title_bar import TitleBar
from .tray import TrayController


class MainWindow(QWidget):
    """Root window: rounded glass body, custom chrome, tray, and stacked cards."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DevPulse")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(720, 460)
        self.setMinimumSize(640, 420)

        self._quitting = False
        self._pinned = False

        self._root = QFrame(self)
        self._root.setObjectName("glassRoot")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._root)

        self.title_bar = TitleBar(self._root)
        self.sidebar = Sidebar(self._root)
        self.stack = QStackedWidget(self._root)

        self.pages = {
            "monitor": SystemMonitorWidget(),
            "pomodoro": PomodoroWidget(),
            "notes": QuickNotesWidget(),
        }
        for widget in self.pages.values():
            self.stack.addWidget(widget)

        body = QHBoxLayout()
        body.setContentsMargins(16, 0, 16, 16)
        body.setSpacing(12)
        body.addWidget(self.sidebar)
        body.addWidget(self.stack, 1)

        inner = QVBoxLayout(self._root)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(0)
        inner.addWidget(self.title_bar)
        inner.addLayout(body)

        self.setStyleSheet(APP_QSS)

        self.title_bar.pin_toggled.connect(self._set_always_on_top)
        self.title_bar.minimize_requested.connect(self.hide_to_tray)
        self.title_bar.close_requested.connect(self.hide_to_tray)
        self.sidebar.page_changed.connect(self._show_page)

        self.tray = TrayController(self)
        self.tray.show()
        self.pages["pomodoro"].session_completed.connect(self._notify_tray)

        self._fade = QGraphicsOpacityEffect(self._root)
        self._root.setGraphicsEffect(self._fade)
        self._anim = QPropertyAnimation(self._fade, b"opacity", self)
        self._anim.setDuration(260)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def _show_page(self, page_id: str) -> None:
        widget = self.pages.get(page_id)
        if widget is not None:
            self.stack.setCurrentWidget(widget)

    def _set_always_on_top(self, pinned: bool) -> None:
        self._pinned = pinned
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, pinned)
        self.show()

    def show_animated(self) -> None:
        """Fade the glass body in when restoring from the tray."""
        self.show()
        self._anim.stop()
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(1.0)
        self._anim.start()

    def hide_to_tray(self) -> None:
        """Fade out, then keep running from the system tray."""
        if not QApplication.instance() or not self.tray.isVisible():
            self.hide()
            return

        def _hide() -> None:
            notes = self.pages.get("notes")
            if notes is not None:
                notes.flush()
            self.hide()
            self._anim.finished.disconnect(_hide)
            self.tray.showMessage(
                "DevPulse",
                "Still running in the tray. Click the icon to restore.",
                self.tray.MessageIcon.Information,
                1800,
            )

        self._anim.stop()
        try:
            self._anim.finished.disconnect()
        except TypeError:
            pass
        self._anim.finished.connect(_hide)
        self._anim.setStartValue(1.0)
        self._anim.setEndValue(0.0)
        self._anim.start()

    def _notify_tray(self, title: str, message: str) -> None:
        if self.tray.isVisible():
            self.tray.showMessage(title, message, self.tray.MessageIcon.Information, 2500)

    def request_quit(self) -> None:
        """True application exit, used by the tray Quit action."""
        self._quitting = True
        self._anim.stop()
        notes = self.pages.get("notes")
        if notes is not None:
            notes.flush()
        QApplication.instance().quit()

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        if self._quitting:
            event.accept()
            return
        event.ignore()
        self.hide_to_tray()
