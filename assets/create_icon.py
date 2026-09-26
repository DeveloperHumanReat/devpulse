"""Generate the Windows .ico used by the packaged DevPulse executable."""

from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image
from PyQt6.QtGui import QColor, QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from widgets.tray import build_tray_icon


def main() -> None:
    app = QApplication([])
    assets = Path(__file__).resolve().parent
    assets.mkdir(parents=True, exist_ok=True)

    icon = build_tray_icon()
    pixmap = icon.pixmap(256, 256)
    if pixmap.isNull():
        pixmap = QPixmap(256, 256)
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#7C6CFF"))
        painter.setPen(QColor("#2A2A2A"))
        painter.drawRoundedRect(16, 16, 224, 224, 48, 48)
        painter.end()

    png_path = assets / "devpulse.png"
    pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32).save(str(png_path), "PNG")

    image = Image.open(png_path).convert("RGBA")
    ico_path = assets / "devpulse.ico"
    image.save(
        ico_path,
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"Wrote {ico_path}")
    app.quit()


if __name__ == "__main__":
    main()
