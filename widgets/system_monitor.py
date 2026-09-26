"""System Monitor panel — live CPU and RAM occupancy (Step 1)."""

from __future__ import annotations

import psutil
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QFrame, QLabel, QProgressBar, QVBoxLayout, QWidget


class SystemMonitorWidget(QFrame):
    """Lightweight live gauges for CPU and RAM usage."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")

        title = QLabel("System Monitor")
        title.setObjectName("cardTitle")
        hint = QLabel("CPU and memory sampled every second.")
        hint.setObjectName("cardHint")

        self.cpu_label = QLabel("CPU  —")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setTextVisible(False)

        self.ram_label = QLabel("RAM  —")
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setTextVisible(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)
        layout.addWidget(title)
        layout.addWidget(hint)
        layout.addSpacing(8)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addSpacing(6)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_bar)
        layout.addStretch()

        # Prime psutil so the first non-blocking reading is meaningful.
        psutil.cpu_percent(interval=None)

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._refresh)
        self._timer.start()
        self._refresh()

    def _refresh(self) -> None:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        self.cpu_bar.setValue(int(cpu))
        self.ram_bar.setValue(int(ram.percent))
        self.cpu_label.setText(f"CPU  {cpu:.0f}%")
        used_gb = ram.used / (1024**3)
        total_gb = ram.total / (1024**3)
        self.ram_label.setText(f"RAM  {ram.percent:.0f}%  ·  {used_gb:.1f} / {total_gb:.1f} GB")
