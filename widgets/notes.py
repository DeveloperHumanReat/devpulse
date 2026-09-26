"""Quick Notes with a searchable list and debounced local persistence."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .paths import notes_path


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _title_from_body(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:72]
    return "Untitled"


class QuickNotesWidget(QFrame):
    """Local scratch notes: create, search, edit, auto-save."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self._path: Path = notes_path()
        self._notes: list[dict] = []
        self._selected_id: str | None = None
        self._loading = False

        title = QLabel("Quick Notes")
        title.setObjectName("cardTitle")
        self.status = QLabel("Ready")
        self.status.setObjectName("cardHint")

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search notes…")
        self.search.textChanged.connect(self._rebuild_list)

        self.add_btn = QPushButton("+")
        self.add_btn.setObjectName("ghostBtn")
        self.add_btn.setFixedWidth(36)
        self.add_btn.setToolTip("New note")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self._create_note)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("ghostBtn")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self._delete_selected)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)
        toolbar.addWidget(self.search, 1)
        toolbar.addWidget(self.add_btn)
        toolbar.addWidget(self.delete_btn)

        self.list = QListWidget()
        self.list.setObjectName("notesList")
        self.list.setMaximumHeight(110)
        self.list.currentItemChanged.connect(self._on_list_change)

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Capture a thought…")
        self.editor.textChanged.connect(self._on_editor_changed)

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(400)
        self._save_timer.timeout.connect(self.flush)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)
        layout.addWidget(title)
        layout.addWidget(self.status)
        layout.addLayout(toolbar)
        layout.addWidget(self.list)
        layout.addWidget(self.editor, 1)

        self._load()

    def _load(self) -> None:
        if self._path.exists():
            try:
                payload = json.loads(self._path.read_text(encoding="utf-8"))
                self._notes = list(payload.get("notes") or [])
                self._selected_id = payload.get("selected_id")
            except (OSError, json.JSONDecodeError):
                self._notes = []
                self._selected_id = None
        if not self._notes:
            self._notes = [self._blank_note()]
            self._selected_id = self._notes[0]["id"]
        if self._selected_id not in {note["id"] for note in self._notes}:
            self._selected_id = self._notes[0]["id"]
        self._rebuild_list()
        self._show_selected()
        self.status.setText("Loaded from disk")

    def _blank_note(self) -> dict:
        return {
            "id": uuid.uuid4().hex,
            "title": "Untitled",
            "body": "",
            "updated_at": _utc_now(),
        }

    def _note_by_id(self, note_id: str | None) -> dict | None:
        for note in self._notes:
            if note["id"] == note_id:
                return note
        return None

    def _rebuild_list(self) -> None:
        query = self.search.text().strip().lower()
        self.list.blockSignals(True)
        self.list.clear()
        selected_row = 0
        visible_index = 0
        for note in self._notes:
            haystack = f"{note.get('title', '')}\n{note.get('body', '')}".lower()
            if query and query not in haystack:
                continue
            item = QListWidgetItem(note.get("title") or "Untitled")
            item.setData(Qt.ItemDataRole.UserRole, note["id"])
            self.list.addItem(item)
            if note["id"] == self._selected_id:
                selected_row = visible_index
            visible_index += 1
        if self.list.count():
            self.list.setCurrentRow(min(selected_row, self.list.count() - 1))
        self.list.blockSignals(False)

    def _on_list_change(self, current: QListWidgetItem | None, _previous: QListWidgetItem | None) -> None:
        if current is None:
            return
        self.flush()
        self._selected_id = current.data(Qt.ItemDataRole.UserRole)
        self._show_selected()

    def _show_selected(self) -> None:
        note = self._note_by_id(self._selected_id)
        self._loading = True
        self.editor.setPlainText("" if note is None else note.get("body", ""))
        self._loading = False
        self.delete_btn.setEnabled(len(self._notes) > 1)

    def _on_editor_changed(self) -> None:
        if self._loading:
            return
        note = self._note_by_id(self._selected_id)
        if note is None:
            return
        note["body"] = self.editor.toPlainText()
        note["title"] = _title_from_body(note["body"])
        note["updated_at"] = _utc_now()
        current = self.list.currentItem()
        if current is not None:
            current.setText(note["title"])
        self.status.setText("Saving…")
        self._save_timer.start()

    def _create_note(self) -> None:
        self.flush()
        note = self._blank_note()
        self._notes.insert(0, note)
        self._selected_id = note["id"]
        self.search.clear()
        self._rebuild_list()
        self._show_selected()
        self.editor.setFocus()
        self.flush()

    def _delete_selected(self) -> None:
        if len(self._notes) <= 1:
            return
        self._notes = [note for note in self._notes if note["id"] != self._selected_id]
        self._selected_id = self._notes[0]["id"]
        self._rebuild_list()
        self._show_selected()
        self.flush()
        self.status.setText("Note deleted")

    def flush(self) -> None:
        """Write the current notebook to disk immediately."""
        self._save_timer.stop()
        payload = {"notes": self._notes, "selected_id": self._selected_id}
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        stamp = datetime.now().strftime("%H:%M:%S")
        self.status.setText(f"Saved  {stamp}")
