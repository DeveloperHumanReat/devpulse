"""Pomodoro focus / break timer with tray-ready completion signals."""

from __future__ import annotations

from enum import Enum

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class Phase(str, Enum):
    FOCUS = "focus"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


PHASE_SECONDS = {
    Phase.FOCUS: 25 * 60,
    Phase.SHORT_BREAK: 5 * 60,
    Phase.LONG_BREAK: 15 * 60,
}

PHASE_LABELS = {
    Phase.FOCUS: "Focus",
    Phase.SHORT_BREAK: "Short break",
    Phase.LONG_BREAK: "Long break",
}

CYCLES_BEFORE_LONG_BREAK = 4


class PomodoroWidget(QFrame):
    """Classic 25/5 pomodoro with pause, skip, and session tracking."""

    session_completed = pyqtSignal(str, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")

        self._phase = Phase.FOCUS
        self._remaining = PHASE_SECONDS[Phase.FOCUS]
        self._running = False
        self._completed = 0

        self._tick = QTimer(self)
        self._tick.setInterval(1000)
        self._tick.timeout.connect(self._on_tick)

        title = QLabel("Pomodoro Timer")
        title.setObjectName("cardTitle")
        self.hint = QLabel()
        self.hint.setObjectName("cardHint")

        self.phase_label = QLabel()
        self.phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phase_label.setObjectName("phaseBadge")

        self.clock = QLabel()
        self.clock.setObjectName("pomodoroClock")
        self.clock.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_btn = QPushButton("Start")
        self.start_btn.setObjectName("primaryBtn")
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.clicked.connect(self._toggle_run)

        self.skip_btn = QPushButton("Skip")
        self.skip_btn.setObjectName("ghostBtn")
        self.skip_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.skip_btn.clicked.connect(self._skip_phase)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setObjectName("ghostBtn")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self._reset)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        actions.addStretch()
        actions.addWidget(self.start_btn)
        actions.addWidget(self.skip_btn)
        actions.addWidget(self.reset_btn)
        actions.addStretch()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)
        layout.addWidget(title)
        layout.addWidget(self.hint)
        layout.addStretch()
        layout.addWidget(self.phase_label)
        layout.addWidget(self.clock)
        layout.addLayout(actions)
        layout.addStretch()
        self._refresh_labels()

    def _refresh_labels(self) -> None:
        minutes, seconds = divmod(self._remaining, 60)
        self.clock.setText(f"{minutes:02d}:{seconds:02d}")
        self.phase_label.setText(PHASE_LABELS[self._phase])
        done_word = "session" if self._completed == 1 else "sessions"
        self.hint.setText(
            f"{self._completed} focus {done_word} today  ·  long break every 4"
        )
        self.start_btn.setText("Pause" if self._running else "Start")

    def _toggle_run(self) -> None:
        self._running = not self._running
        if self._running:
            self._tick.start()
        else:
            self._tick.stop()
        self._refresh_labels()

    def _on_tick(self) -> None:
        if self._remaining <= 0:
            self._complete_phase()
            return
        self._remaining -= 1
        if self._remaining <= 0:
            self._complete_phase()
            return
        self._refresh_labels()

    def _complete_phase(self) -> None:
        self._tick.stop()
        self._running = False
        finished = PHASE_LABELS[self._phase]
        next_phase = self._advance_phase(count_focus=True)
        self.session_completed.emit(
            "DevPulse · Pomodoro",
            f"{finished} done. Next: {PHASE_LABELS[next_phase]}.",
        )
        self._refresh_labels()

    def _advance_phase(self, *, count_focus: bool) -> Phase:
        if self._phase == Phase.FOCUS:
            if count_focus:
                self._completed += 1
                if self._completed % CYCLES_BEFORE_LONG_BREAK == 0:
                    self._phase = Phase.LONG_BREAK
                else:
                    self._phase = Phase.SHORT_BREAK
            else:
                self._phase = Phase.SHORT_BREAK
        else:
            self._phase = Phase.FOCUS
        self._remaining = PHASE_SECONDS[self._phase]
        return self._phase

    def _skip_phase(self) -> None:
        self._tick.stop()
        self._running = False
        self._advance_phase(count_focus=False)
        self._refresh_labels()

    def _reset(self) -> None:
        self._tick.stop()
        self._running = False
        self._phase = Phase.FOCUS
        self._remaining = PHASE_SECONDS[Phase.FOCUS]
        self._refresh_labels()
