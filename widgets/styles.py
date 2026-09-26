"""Shared Qt Style Sheets for the DevPulse glassmorphism theme."""

ACCENT = "#7C6CFF"
ACCENT_SOFT = "rgba(124, 108, 255, 0.18)"
BG_DARK = "#121212"
BORDER = "#2A2A2A"
TEXT = "#F2F2F2"
MUTED = "#9A9A9A"

APP_QSS = f"""
QWidget#glassRoot {{
    background-color: rgba(18, 18, 18, 230);
    border: 1px solid {BORDER};
    border-radius: 16px;
}}

QLabel {{
    color: {TEXT};
    background: transparent;
}}

QPushButton {{
    background: transparent;
    border: none;
    color: {TEXT};
}}

QFrame#titleBar {{
    background: transparent;
    border: none;
}}

QLabel#appTitle {{
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.6px;
    color: {TEXT};
}}

QLabel#appSubtitle {{
    font-size: 11px;
    color: {MUTED};
}}

QPushButton#windowBtn, QPushButton#closeBtn, QPushButton#pinBtn {{
    min-width: 28px;
    max-width: 28px;
    min-height: 28px;
    max-height: 28px;
    border-radius: 8px;
    font-size: 13px;
    color: {MUTED};
}}

QPushButton#windowBtn:hover, QPushButton#pinBtn:hover {{
    background-color: rgba(255, 255, 255, 0.08);
    color: {TEXT};
}}

QPushButton#closeBtn:hover {{
    background-color: rgba(232, 88, 88, 0.22);
    color: #FF8A8A;
}}

QPushButton#pinBtn[pinned="true"] {{
    background-color: {ACCENT_SOFT};
    color: {ACCENT};
}}

QFrame#sidebar {{
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid {BORDER};
    border-radius: 12px;
}}

QPushButton#navBtn {{
    text-align: left;
    padding: 10px 12px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    color: {MUTED};
}}

QPushButton#navBtn:hover {{
    background-color: rgba(255, 255, 255, 0.06);
    color: {TEXT};
}}

QPushButton#navBtn[active="true"] {{
    background-color: {ACCENT_SOFT};
    color: {ACCENT};
}}

QFrame#card {{
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid {BORDER};
    border-radius: 14px;
}}

QLabel#cardTitle {{
    font-size: 16px;
    font-weight: 700;
}}

QLabel#cardHint {{
    font-size: 12px;
    color: {MUTED};
}}

QProgressBar {{
    background-color: rgba(255, 255, 255, 0.06);
    border: 1px solid {BORDER};
    border-radius: 8px;
    min-height: 12px;
    max-height: 12px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {ACCENT};
    border-radius: 8px;
}}

QTextEdit {{
    background-color: rgba(0, 0, 0, 0.28);
    border: 1px solid {BORDER};
    border-radius: 10px;
    color: {TEXT};
    padding: 10px;
    font-size: 13px;
}}

QPushButton#primaryBtn {{
    background-color: {ACCENT};
    color: white;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 700;
}}

QPushButton#primaryBtn:hover {{
    background-color: #8B7DFF;
}}

QPushButton#ghostBtn {{
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
    color: {TEXT};
}}

QPushButton#ghostBtn:hover {{
    background-color: rgba(255, 255, 255, 0.10);
}}

QLabel#pomodoroClock {{
    font-size: 42px;
    font-weight: 700;
    letter-spacing: 2px;
}}

QLabel#phaseBadge {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.2px;
    color: {ACCENT};
    text-transform: uppercase;
}}

QLineEdit {{
    background-color: rgba(0, 0, 0, 0.28);
    border: 1px solid {BORDER};
    border-radius: 10px;
    color: {TEXT};
    padding: 8px 10px;
    font-size: 13px;
    selection-background-color: {ACCENT};
}}

QLineEdit:focus, QTextEdit:focus {{
    border: 1px solid {ACCENT};
}}

QListWidget#notesList {{
    background-color: rgba(0, 0, 0, 0.28);
    border: 1px solid {BORDER};
    border-radius: 10px;
    color: {TEXT};
    padding: 4px;
    outline: none;
}}

QListWidget#notesList::item {{
    padding: 8px 10px;
    border-radius: 8px;
}}

QListWidget#notesList::item:selected {{
    background-color: {ACCENT_SOFT};
    color: {ACCENT};
}}

QListWidget#notesList::item:hover {{
    background-color: rgba(255, 255, 255, 0.06);
}}
"""
