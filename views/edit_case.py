import datetime as dt
import sys
from enum import Enum
from pathlib import Path
from typing import Iterable, List, Optional, Union
from dataclasses import dataclass

from PyQt6 import uic
from PyQt6.QtCore import QDateTime, Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QDateTimeEdit,
    QFileDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QWidget,
)

from src.utils import UI_DIR, format_caseid

UI_FILE = UI_DIR / "edit_case.ui"

APP_NAME = "Asche Yiu Police Department"

# Role used to store a case file's full path on its list item.
FILE_PATH_ROLE = Qt.ItemDataRole.UserRole


class CaseMode(Enum):
    """Whether the window is opening a case or editing one."""

    OPEN = "Open"
    EDIT = "Edit"

@dataclass
class CaseData:
    """Everything entered in the window, handed over on submit."""

    case_id: Union[int, str]
    codename: str
    time_of_incident: dt.datetime
    case_files: List[Path]
    change_summary: str


class CaseEdit(QMainWindow):
    """Open or edit one case. Use ``set_mode`` to switch between the two.

    Populate the window with:
        set_case_info, set_case_files, set_change_summary,
        set_version_info, set_submit_text, set_mode

    Signals
    -------
    submit_requested(CaseData)
        Submit pressed; carries every value entered in the window.
    cancel_requested
        Cancel pressed; the owner should close this window.
    """

    submit_requested = pyqtSignal(object)
    cancel_requested = pyqtSignal()

    # Widgets defined in edit_case.ui
    lblTitle: QLabel
    frameVersionNotice: QFrame
    lblVersionInfo: QLabel
    edtCodename: QLineEdit
    dteIncident: QDateTimeEdit
    lstCaseFiles: QListWidget
    btnAddFile: QPushButton
    txtChangeSummary: QPlainTextEdit
    btnCancel: QPushButton
    btnSubmit: QPushButton

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        uic.loadUi(UI_FILE, self)  # type: ignore

        self._case_id: Union[int, str] = 0
        self._mode = CaseMode.EDIT

        # The .ui ships with placeholder file names; start from an empty list.
        self.lstCaseFiles.clear()

        self._connect_signals()
        self._refresh_title()

    def _connect_signals(self) -> None:
        """Wire button clicks and shortcuts to their handlers."""
        self.btnAddFile.clicked.connect(self._on_add_file)
        self.btnCancel.clicked.connect(self.cancel_requested)
        self.btnSubmit.clicked.connect(self._on_submit)

        # Delete removes the selected file(s) from the list.
        self._delete_shortcut = QShortcut(
            QKeySequence(Qt.Key.Key_Delete), self.lstCaseFiles
        )
        self._delete_shortcut.setContext(Qt.ShortcutContext.WidgetShortcut)
        self._delete_shortcut.activated.connect(self.remove_selected_case_files)

    # ------------------------------------------------------------------
    # Mode and title
    # ------------------------------------------------------------------
    def set_mode(self, mode: CaseMode) -> None:
        """Switch between 'Open' and 'Edit'. Updates the title and lblTitle."""
        self._mode = mode
        self._refresh_title()

    def mode(self) -> CaseMode:
        """Return the current mode."""
        return self._mode

    def _refresh_title(self) -> None:
        heading = f"{self._mode.value} Case {format_caseid(self._case_id)}"
        self.lblTitle.setText(heading)
        self.setWindowTitle(f"{APP_NAME} - {heading}")

    # ------------------------------------------------------------------
    # Case info
    # ------------------------------------------------------------------
    def set_case_info(
        self,
        case_id: Union[int, str],
        codename: str,
        time_of_incident: dt.datetime,
    ) -> None:
        """Set the case id, codename and time of incident."""
        self._case_id = case_id
        self.set_codename(codename)
        self.set_time_of_incident(time_of_incident)
        self._refresh_title()

    def set_codename(self, codename: str) -> None:
        self.edtCodename.setText(codename)

    def codename(self) -> str:
        return self.edtCodename.text().strip()

    def set_time_of_incident(self, time_of_incident: dt.datetime) -> None:
        self.dteIncident.setDateTime(QDateTime(time_of_incident))

    def time_of_incident(self) -> dt.datetime:
        return self.dteIncident.dateTime().toPyDateTime()

    # ------------------------------------------------------------------
    # Case files
    # ------------------------------------------------------------------
    def set_case_files(self, paths: Iterable[Union[str, Path]]) -> None:
        """Replace the case file list. Duplicates are skipped."""
        self.lstCaseFiles.clear()
        for path in paths:
            self._add_case_file(Path(path))

    def case_files(self) -> List[Path]:
        """Return the full path of every file in the list, in order."""
        files: List[Path] = []
        for row in range(self.lstCaseFiles.count()):
            data = self.lstCaseFiles.item(row).data(FILE_PATH_ROLE) #type:ignore
            if data:
                files.append(Path(data))
        return files

    def _add_case_file(self, path: Path) -> None:
        """Add one file. Shows the file name and stores the full path."""
        if path in self.case_files():
            return
        item = QListWidgetItem(path.name)
        item.setData(FILE_PATH_ROLE, str(path))
        item.setToolTip(str(path))
        self.lstCaseFiles.addItem(item)

    def remove_selected_case_files(self) -> None:
        """Remove every selected file from the list (does not touch disk)."""
        for item in self.lstCaseFiles.selectedItems():
            self.lstCaseFiles.takeItem(self.lstCaseFiles.row(item))

    def _on_add_file(self) -> None:
        """Open the OS file explorer and add whatever the user picks."""
        filenames, _ = QFileDialog.getOpenFileNames(
            self, "Add Case Files", "", "All Files (*)"
        )
        for filename in filenames:
            self._add_case_file(Path(filename))

    # ------------------------------------------------------------------
    # Change summary
    # ------------------------------------------------------------------
    def set_change_summary(self, text: str) -> None:
        self.txtChangeSummary.setPlainText(text)

    def change_summary(self) -> str:
        return self.txtChangeSummary.toPlainText().strip()

    # ------------------------------------------------------------------
    # Version notice (lblVersionInfo)
    # ------------------------------------------------------------------
    def set_version_info(self, text: Optional[str]) -> None:
        """Show ``text`` in the version notice, or hide the notice if None."""
        visible = text is not None
        self.frameVersionNotice.setVisible(visible)
        self.lblVersionInfo.setVisible(visible)
        if text is not None:
            self.lblVersionInfo.setText(text)

    # ------------------------------------------------------------------
    # Submit button (btnSubmit)
    # ------------------------------------------------------------------
    def set_submit_text(self, text: str) -> None:
        self.btnSubmit.setText(text)

    # ------------------------------------------------------------------
    # Data out
    # ------------------------------------------------------------------
    def case_data(self) -> CaseData:
        """Return everything currently entered in the window."""
        return CaseData(
            case_id=self._case_id,
            codename=self.codename(),
            time_of_incident=self.time_of_incident(),
            case_files=self.case_files(),
            change_summary=self.change_summary(),
        )

    def _on_submit(self) -> None:
        self.submit_requested.emit(self.case_data())


def main() -> None:
    """Preview the window. Run with ``--open`` to see the Open version."""
    app = QApplication(sys.argv)
    window = CaseEdit()

    window.set_case_info(5, "Blue Harbor", dt.datetime(2026, 10, 18, 21, 30))
    window.set_case_files([
        "files/scene_report.pdf",
        "files/witness_statements.pdf",
        "files/cctv_dock3.mp4",
    ])
    window.set_change_summary("")
    if "--open" in sys.argv:
        window.set_version_info(
            "Saving will create version 0.1"
        )
    else:
        window.set_version_info(
            "Saving creates version 2.1 and sends it for review. Current version: 2.0."
        )

    window.set_submit_text("Submit for Review")
    window.set_mode(CaseMode.OPEN if "--open" in sys.argv else CaseMode.EDIT)

    window.submit_requested.connect(lambda data: print("Submitted:", data))
    window.cancel_requested.connect(lambda: print("Cancel requested"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()