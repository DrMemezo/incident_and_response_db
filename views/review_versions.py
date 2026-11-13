import sys
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple

from PyQt6 import uic
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from src.utils import UI_DIR, DOT

UI_FILE = UI_DIR / "review_versions.ui"

APP_NAME = "Asche Yiu Police Department"

# Role used to store a version number on its list item.
VERSION_ROLE = Qt.ItemDataRole.UserRole

# Badge style per state shown in lblState.
STATE_BADGES = {
    "Pending": "badgeGold",
    "Accepted": "badgeGreen",
    "Rejected": "badgeRed",
}

# (field, current, proposed)
DiffRow = Tuple[str, str, str]


@dataclass
class VersionEntry:
    """One minor version in the list on the left."""

    version: str
    author: str
    summary: str


def _set_variant(widget: QWidget, variant: str) -> None:
    """Change a widget's dynamic 'variant' property and re-apply the stylesheet."""
    widget.setProperty("variant", variant)
    widget.style().unpolish(widget)  # type: ignore
    widget.style().polish(widget)  # type: ignore


class ReviewVersions(QMainWindow):
    """Review the minor versions of a case and accept or reject them.

    Populate the window with:
        set_title, set_subtitle, set_minor_versions, set_version_details,
        set_changes, set_diff_headers, set_outcome_hint

    Signals
    -------
    version_selected(int)
        The user picked a different version in the list. Carries the row index.
        Not emitted for programmatic changes (set_minor_versions, select_version).
    back_requested
        Back pressed.
    reject_requested
        Reject pressed.
    accept_requested
        Accept Change pressed.
    """

    version_selected = pyqtSignal(int)
    back_requested = pyqtSignal()
    reject_requested = pyqtSignal()
    accept_requested = pyqtSignal()

    # Widgets defined in review_versions.ui
    lblTitle: QLabel
    lblSubtitle: QLabel
    lstMinorVersions: QListWidget
    frameDetail: QFrame
    lblVersion: QLabel
    lblState: QLabel
    lblSubmittedBy: QLabel
    txtSummary: QPlainTextEdit
    tblDiff: QTableWidget
    lblOutcomeHint: QLabel
    btnBack: QPushButton
    btnReject: QPushButton
    btnAccept: QPushButton

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        uic.loadUi(UI_FILE, self)  # type: ignore

        # The .ui ships with sample versions and changes; start empty.
        self.lstMinorVersions.clear()
        self.tblDiff.setRowCount(0)

        # Set while populating the list so no signal fires for it.
        self._loading = False

        self._connect_signals()

    def _connect_signals(self) -> None:
        """Wire the list and buttons to the signals the owner listens to."""
        self.lstMinorVersions.currentRowChanged.connect(self._on_row_changed)
        self.btnBack.clicked.connect(self.back_requested)
        self.btnReject.clicked.connect(self.reject_requested)
        self.btnAccept.clicked.connect(self.accept_requested)

    def _on_row_changed(self, row: int) -> None:
        if self._loading or row < 0:
            return
        self.version_selected.emit(row)

    # ------------------------------------------------------------------
    # Title and subtitle
    # ------------------------------------------------------------------
    def set_title(self, title: str) -> None:
        """Set lblTitle and the window title."""
        self.lblTitle.setText(title)
        self.setWindowTitle(f"{APP_NAME} - {title}")

    def set_subtitle(self, subtitle: str) -> None:
        """Set lblSubtitle."""
        self.lblSubtitle.setText(subtitle)

    # ------------------------------------------------------------------
    # Minor versions list
    # ------------------------------------------------------------------
    def set_minor_versions(self, entries: Iterable[VersionEntry]) -> None:
        """Replace the version list. Nothing is selected afterwards."""
        self._loading = True
        try:
            self.lstMinorVersions.clear()
            for entry in entries:
                item = QListWidgetItem(
                    f"{entry.version}   \u00b7   {entry.author}\n{entry.summary}"
                )
                item.setData(VERSION_ROLE, entry.version)
                self.lstMinorVersions.addItem(item)
        finally:
            self._loading = False

    def select_version(self, row: int) -> None:
        """Select a row without emitting version_selected."""
        self._loading = True
        try:
            self.lstMinorVersions.setCurrentRow(row)
        finally:
            self._loading = False

    def selected_row(self) -> int:
        """Return the selected row index, or -1 if nothing is selected."""
        return self.lstMinorVersions.currentRow()

    def selected_version(self) -> Optional[str]:
        """Return the selected version number, or None."""
        item = self.lstMinorVersions.currentItem()
        if item is None:
            return None
        return item.data(VERSION_ROLE)

    # ------------------------------------------------------------------
    # Version detail card
    # ------------------------------------------------------------------
    def set_detail_visible(self, visible: bool) -> None:
        """Show or hide the whole detail card on the right."""
        self.frameDetail.setVisible(visible)

    def set_version_details(
        self, version: str, state: str, submitted_by: str, summary: str
    ) -> None:
        """Fill the detail card for one version."""
        self.lblVersion.setText(f"Version {version}")
        self.set_state(state)
        self.lblSubmittedBy.setText(submitted_by)
        self.txtSummary.setPlainText(summary)

    def set_state(self, state: str) -> None:
        """Set lblState's text and badge colour."""
        self.lblState.setText(state)
        _set_variant(self.lblState, STATE_BADGES.get(state, "badgeMuted"))

    # ------------------------------------------------------------------
    # Summary of changes table
    # ------------------------------------------------------------------
    def set_diff_headers(self, field: str, current: str, proposed: str) -> None:
        """Set the three column headers of tblDiff."""
        self.tblDiff.setHorizontalHeaderLabels([field, current, proposed])

    def set_changes(self, rows: Iterable[DiffRow]) -> None:
        """Replace the rows of tblDiff. Each row is (field, current, proposed)."""
        table = self.tblDiff
        table.setRowCount(0)
        for values in rows:
            row = table.rowCount()
            table.insertRow(row)
            for column, text in enumerate(values):
                table.setItem(row, column, QTableWidgetItem(str(text)))

    def clear_changes(self) -> None:
        """Remove every row from tblDiff. Headers are kept."""
        self.tblDiff.setRowCount(0)

    # ------------------------------------------------------------------
    # Outcome hint and buttons
    # ------------------------------------------------------------------
    def set_outcome_hint(self, text: Optional[str]) -> None:
        """Set lblOutcomeHint's text, or hide it if None."""
        self.lblOutcomeHint.setVisible(text is not None)
        if text is not None:
            self.lblOutcomeHint.setText(text)

    def set_back_text(self, text: str) -> None:
        self.btnBack.setText(text)

    def set_reject_text(self, text: str) -> None:
        self.btnReject.setText(text)

    def set_accept_text(self, text: str) -> None:
        self.btnAccept.setText(text)


def main() -> None:
    """Preview the window with sample data."""
    app = QApplication(sys.argv)
    window = ReviewVersions()

    window.set_title("Review Changes")
    window.set_subtitle(f"Case 0005  {DOT}  Blue Harbor  {DOT}  current version 2.0")
    window.set_minor_versions([
        VersionEntry("2.1", "Ayesha Khan", "Added CCTV footage"),
        VersionEntry("2.2", "Bilal Raza", "Corrected incident time"),
    ])
    window.set_version_details(
        "2.1",
        "Pending",
        f"Submitted by Ayesha Khan (Fieldworker)  {DOT}  today, 10:42",
        "Added CCTV footage from dock 3. It shows the second person near the pier at 21:25.",
    )
    window.set_diff_headers("Field", "Current (2.0)", "Proposed (2.1)")
    window.set_changes([
        ("Codename", "Blue Harbor", "Blue Harbor"),
        ("Time of incident", "18/10/2026 21:30", "18/10/2026 21:30"),
        ("Case files", "2 files", "3 files  (+ cctv_dock3.mp4)"),
    ])
    window.set_outcome_hint(
        "Accepting creates version 3.0. Rejecting leaves the case at version 2.0."
    )

    window.version_selected.connect(
        lambda row: print("Selected row:", row, "version:", window.selected_version())
    )
    window.back_requested.connect(lambda: print("Back requested"))
    window.reject_requested.connect(lambda: print("Reject requested"))
    window.accept_requested.connect(lambda: print("Accept requested"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()