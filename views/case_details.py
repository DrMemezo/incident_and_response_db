from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path
from typing import Iterable, Optional, Tuple, Union

from PyQt6 import uic
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from src.utils import UI_DIR, toi_to_str, format_caseid, TIME_FORMAT
from src.case_file_opener import open_with_default_app
UI_FILE = UI_DIR / "case_details_v2.ui"


STATUS_AWAITING = "Awaiting"
STATUS_ONGOING = "Ongoing"
STATUS_CLOSED = "Closed"

# Badge style per status.
STATUS_BADGES = {
    STATUS_ONGOING: "badgeGreen",
    STATUS_AWAITING: "badgeGold",
    STATUS_CLOSED: "badgeMuted",
}

# Colours used for table text.
COLOR_RED = QColor(207, 125, 114)
COLOR_GREEN = QColor(127, 176, 140)
COLOR_GOLD = QColor(195, 164, 89)
COLOR_MUTED = QColor(139, 148, 163)

TEXT_COLORS = {
    "Guilty": COLOR_RED,
    "At large": COLOR_RED,
    "Rejected": COLOR_RED,
    "Not guilty": COLOR_GREEN,
    "In custody": COLOR_GREEN,
    "Accepted": COLOR_GREEN,
    "Pending": COLOR_GOLD,
    "N/A": COLOR_MUTED,
    "\u2014": COLOR_MUTED,  # em dash
}


# Role used to store a case file's full path on its list item.
FILE_PATH_ROLE = Qt.ItemDataRole.UserRole

# (codename, guilty, apprehended)
SuspectRow = Tuple[str, str, str]
# (version, by, change, state)
UpdateRow = Tuple[Union[float, str], str, str, str]


def _set_variant(widget: QWidget, variant: str) -> None:
    """Change a widget's dynamic 'variant' property and re-apply the stylesheet."""
    widget.setProperty("variant", variant)
    widget.style().unpolish(widget) #type: ignore
    widget.style().polish(widget)#type: ignore


def _add_table_row(table: QTableWidget, values: Iterable[str]) -> None:
    """Append one row of text to ``table``, colouring known words."""
    row = table.rowCount()
    table.insertRow(row)
    for column, text in enumerate(values):
        item = QTableWidgetItem(text)
        if text in TEXT_COLORS:
            item.setForeground(TEXT_COLORS[text])
        table.setItem(row, column, item)


class CaseDetails(QMainWindow):
    """Shows one case. Read-only by default; call ``set_editable(True)`` to edit.

    Populate the window with:
        set_case_info, set_detectives, set_filing_details,
        set_suspects, set_updates, set_case_files

    Signals
    -------
    back_requested
        Back pressed; the owner should close this window and show the previous one.
    link_suspect_requested
        Link Suspect pressed (only visible in editable mode).
    edit_case_requested
        Edit Case pressed (only visible in editable mode).
    """

    back_requested = pyqtSignal()
    link_suspect_requested = pyqtSignal()
    edit_case_requested = pyqtSignal()

    # Widgets defined in case_details.ui
    lblTitle: QLabel
    lblVersion: QLabel
    lblStatus: QLabel
    lblCodenameSubcode: QLabel
    
    lblCodename: QLabel
    lblIncidentTime: QLabel
    lstDetectives: QListWidget
    lblFiledBy: QLabel
    lblUpdated: QLabel
    lblSuspectCount: QLabel
    lstCaseFiles: QListWidget

    tblCaseSuspects: QTableWidget

    tblUpdates: QTableWidget

    btnBack: QPushButton
    btnLinkSuspect: QPushButton
    btnEditCase: QPushButton

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        uic.loadUi(UI_FILE, self)  # type: ignore

        self.setWindowTitle("Asche Yiu Police Department - Case Details")
        self._connect_signals()
        self.tblCaseSuspects.setEnabled(False)
        self.tblUpdates.setEnabled(False)

        self.set_editable(False)

    def _connect_signals(self) -> None:
        """Wire button clicks to the signals the owner listens to."""
        self.btnBack.clicked.connect(self.back_requested)
        self.btnLinkSuspect.clicked.connect(self.link_suspect_requested)
        self.btnEditCase.clicked.connect(self.edit_case_requested)
        self.lstCaseFiles.itemDoubleClicked.connect(
            lambda item: open_with_default_app(Path(item.data(FILE_PATH_ROLE)), self)
        )
    def set_editable(self, editable: bool) -> None:
        """Switch between the editable and read-only versions of the view.

        Editable:  Link Suspect and Edit Case buttons are shown
        Read-only: those buttons are hidden

        Case files stay enabled in both modes so they can still be opened.
        """
        self.btnLinkSuspect.setVisible(editable)
        self.btnEditCase.setVisible(editable)
        # self.tblCaseSuspects.setEnabled(editable)
        # self.tblUpdates.setEnabled(editable)

    def set_case_info(
        self,
        case_id: Union[int, str],
        codename: str,
        time_of_incident: Union[dt.datetime, str],
        version: Union[float, str],
        status: str,
    ) -> None:
        """Set the header (title, codename, incident time, version and status)."""
        self.lblTitle.setText(f"Case {format_caseid(case_id)}")
        self.lblCodenameSubcode.setText(codename)
        self.lblCodename.setText(codename)
        self.lblIncidentTime.setText(toi_to_str(time_of_incident))
        self.lblVersion.setText(f"Version {version}")

        self.lblStatus.setText(status)

        _set_variant(self.lblStatus, STATUS_BADGES.get(status, "badgeMuted"))

    def set_detectives(self, names: Iterable[str]) -> None:
        """Set every detective in charge of the case."""
        self.lstDetectives.clear()
        for name in names:
            if name.strip():
                self.lstDetectives.addItem(name.strip())
        if self.lstDetectives.count() == 0:
            self.lstDetectives.addItem("Unassigned")

    def set_filing_details(
        self, filed_by: str, last_updated: Union[dt.datetime, str]
    ) -> None:
        """Set who filed the case and when it was last updated."""
        self.lblFiledBy.setText(filed_by)
        self.lblUpdated.setText(toi_to_str(last_updated))

    def set_suspects(self, rows: Iterable[SuspectRow]) -> None:
        """Replace the suspects table. Also updates the suspect count."""
        table = self.tblCaseSuspects
        table.setRowCount(0)
        for row in rows:
            _add_table_row(table, row)
        self.lblSuspectCount.setText(str(table.rowCount()))

    def set_updates(self, rows: Iterable[UpdateRow]) -> None:
        """Replace the evidence and updates table."""
        table = self.tblUpdates
        table.setRowCount(0)
        for version, by, change, state in rows:
            _add_table_row(table, (str(version), by, change, state))

    def set_case_files(self, paths: Iterable[Union[str, Path]]) -> None:
        """Replace the case file list. Each item shows the file name and
        stores its full path, so it can be opened later."""
        self.lstCaseFiles.clear()
        for path in (Path(p) for p in paths):
            # Gets the final path name. So path/to/data/data.pdf becomes data.pdf
            item = QListWidgetItem(path.name) 
            item.setData(FILE_PATH_ROLE, str(path))
            item.setToolTip(str(path))
            self.lstCaseFiles.addItem(item)

    def selected_case_file(self) -> Optional[Path]:
        """Return the full path of the selected case file, or None."""
        item = self.lstCaseFiles.currentItem()
        if item is None:
            return None
        return Path(item.data(FILE_PATH_ROLE))


def main() -> None:
    """Preview the window. Run with ``--edit`` to see the editable version."""
    app = QApplication(sys.argv)
    window = CaseDetails()

    window.set_case_info(
        5, "Blue Harbor", dt.datetime(2026, 10, 18, 21, 30), 2.0, STATUS_ONGOING
    )
    window.set_detectives(["Rahim Malik", "Ayesha Khan"])
    window.set_filing_details(
        "Ayesha Khan (Fieldworker)", dt.datetime(2026, 10, 19, 10, 42)
    )
    window.set_suspects([
        ("Dock Worker X", "Guilty", "At large"),
        ("Great White (shark)", "Guilty", "N/A"),
        ("Harbor Master", "Not guilty", "\u2014"),
        ("Red Cap", "Guilty", "In custody"),
    ])
    window.set_updates([
        (2.1, "Ayesha Khan (FW)", "Added CCTV footage from dock 3", "Pending"),
        (2.0, "Rahim Malik", "Reviewed scene report, updated codename", "Accepted"),
        (1.0, "Rahim Malik", "Accepted case, took ownership", "Accepted"),
        (0.1, "Ayesha Khan (FW)", "Case filed", "Accepted"),
    ])
    window.set_case_files([
        "files/scene_report.pdf",
        "files/witness_statements.pdf",
        "files/cctv_dock3.mp4",
        R"D:\OneDrive - Habib University\Fall 2026\DB SYS --- CS 355\Project\incident_and_response_db\docs\incident_response_v3.pdf"
    ])

    window.set_editable("--edit" in sys.argv)

    window.back_requested.connect(lambda: print("Back requested"))
    window.link_suspect_requested.connect(lambda: print("Link suspect requested"))
    window.edit_case_requested.connect(lambda: print("Edit case requested"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
