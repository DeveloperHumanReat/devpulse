"""DevPulse entry point — launches the frameless desktop widget."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon

from widgets.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("DevPulse")
    app.setOrganizationName("DevPulse")
    app.setQuitOnLastWindowClosed(False)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray is not available; DevPulse will still run as a window.")

    window = MainWindow()
    window.show_animated()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
