import sys
from typing import Iterable, Optional, Tuple, Union, NamedTuple
import datetime as dt

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QComboBox
)

from src.utils import toi_to_str, format_caseid
# TODO: Make search feature functional

# Resolve the .ui path relative to this file so the script works from any
# working directory.
from src.utils import UI_DIR
UI_FILE = UI_DIR / "view_cases.ui"


# Column indices in tblApplications - named constants beat "magic numbers".
COL_CASEID = 0
COL_CODENAME = 1
COL_STATUS = 2
COL_VERSION = 3
COL_TIME_OF_INCIDENT = 4

STATUS_AWAITING = "Awaiting"
STATUS_ONGOING = "Ongoing"
STATUS_CLOSED = "Closed"
ALL_STATUSES = "All statuses"

STATUS_COLORS = {
    STATUS_ONGOING: QColor(127, 176, 140),
    STATUS_AWAITING: QColor(195, 164, 89),
    STATUS_CLOSED: QColor(139, 148, 163),
}

TIME_FORMAT = "%d/%m/%y %H:%M"

CaseRow = Tuple[Union[str, int],            # case Id
                 str,                       # codename
                 str,                       # status 
                 Union[float, str],         # version
                 Union[dt.datetime, str]]   # Time of incident

class CaseSummary(NamedTuple):
    """One case as read back from the table, as display strings.
    """
 
    case_id: str
    codename: str
    status: str
    version: str
    time_of_incident: str

class ViewCases(QMainWindow):
    """ View all cases in the database

    Signals
    -------
    edit_case_requested         
        Edit Case pressed 
    see_case_details_requested  
        See Case Details pressed
    back_requested
        The user pressed *Back*; the owner should close this window and show
        the previous one.
    """

    back_requested = pyqtSignal()
    edit_case_requested = pyqtSignal(object)
    see_case_details_requested = pyqtSignal(object)

    edtSearch: QLineEdit
    cmbStatus: QComboBox

    tblCases: QTableWidget
    btnCaseDetails: QPushButton
    btnEditCase: QPushButton
    btnBack: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create all widgets from the .ui file and attach them to ``self``.
        uic.loadUi(UI_FILE, self) # type: ignore

        self._all_rows: list[CaseRow] = []

        self.setWindowTitle("Asche Yiu Police Department - View Cases")
        self._connect_signals()

        self._update_action_buttons()

    def _connect_signals(self) -> None:
        """Wire widget events to the handler methods below."""
        self.btnCaseDetails.clicked.connect(self._on_case_details_clicked)
        self.btnEditCase.clicked.connect(self._on_edit_case_clicked)
        self.btnBack.clicked.connect(self.back_requested)

        self.tblCases.itemSelectionChanged.connect(self._update_action_buttons)

        self.edtSearch.textChanged.connect(self._apply_filters)
        self.cmbStatus.currentIndexChanged.connect(self._apply_filters)


    def _update_action_buttons(self) -> None:
        """Enable the action buttons based on the current selection."""
        case = self.selected_case()
        self.btnCaseDetails.setEnabled(case is not None)
        # Closed cases can still be viewed, but not edited.
        self.btnEditCase.setEnabled(case is not None and case.status != STATUS_CLOSED)
 
    def _on_case_details_clicked(self) -> None:
        case = self.selected_case()
        if case is not None:
            self.see_case_details_requested.emit(case)
 
    def _on_edit_case_clicked(self) -> None:
        case = self.selected_case()
        if case is not None and case.status != STATUS_CLOSED:
            self.edit_case_requested.emit(case)

    def _clear_table(self) -> None: 
        """ Clears the applications table """
        self.tblCases.clearContents()
        self.tblCases.setRowCount(0)

    def set_cases(self, rows: Iterable[CaseRow]) -> None:
        self._all_rows = list(rows)
        self._apply_filters()

    def _apply_filters(self) -> None:
        search = self.edtSearch.text().strip().lower()
        status = self.cmbStatus.currentText()

        matches = [x for x in self._all_rows if self._row_matches(x, search, status)]

        self._populate_cases_table(matches)

    @staticmethod
    def _row_matches(row: CaseRow, search: str, status: str) -> bool:
        """Checks if the row passes the search and status filters"""

        caseid, codename, row_status, _, _ = row
        if status != ALL_STATUSES and row_status != status:
            return False 

        return ( search == '' 
                or str(caseid).find(search) != -1 
                or codename.casefold().find(search.casefold()) != -1 )

    def _populate_cases_table(self, rows: Iterable[CaseRow]) -> None:
        """Replace the table contents with ``rows``.

        Parameters
        ----------
        rows:
            Iterable of {CaseID, Codename, Status, Version, Time of Incident}
        """


        table = self.tblCases
        self._clear_table()

        for caseid, codename, status, vers, toi in rows:

            row = table.rowCount()
            table.insertRow(row)

            table.setItem(row, COL_CASEID, QTableWidgetItem(format_caseid(caseid)))

            table.setItem(row, COL_CODENAME, QTableWidgetItem(codename))
 
            status_item = QTableWidgetItem(status)

            if status in STATUS_COLORS:
                status_item.setForeground(STATUS_COLORS[status])

            table.setItem(row, COL_STATUS, status_item)
 
            table.setItem(row, COL_VERSION, QTableWidgetItem(str(vers)))
            table.setItem(row, COL_TIME_OF_INCIDENT, QTableWidgetItem(toi_to_str(toi)))


    def _selected_row(self) -> Optional[int]:
        """Return the selected row index, or ``None`` if nothing is selected.

        The table uses single-row selection (set in the .ui file), so at most
        one row can be selected at a time.
        """
        rows = self.tblCases.selectionModel().selectedRows() # type: ignore
        return rows[0].row() if rows else None

    def _cell_text(self, row: int, column: int) -> str:
        """Safely read a cell's text (empty string if the cell has no item)."""
        item = self.tblCases.item(row, column)
        return item.text() if item is not None else ""

    def selected_case(self) -> Optional[CaseSummary]:
        """Return the selected case, or ``None`` if no row is selected."""
        row = self._selected_row()

        if row is None:
            return None

        return CaseSummary(
            case_id=self._cell_text(row, COL_CASEID),
            codename=self._cell_text(row, COL_CODENAME),
            status=self._cell_text(row, COL_STATUS),
            version=self._cell_text(row, COL_VERSION),
            time_of_incident=self._cell_text(row, COL_TIME_OF_INCIDENT),
        )


DEMO_ROWS: list[CaseRow] = [
    ("0005", "Blue Harbor", STATUS_ONGOING, 2.0, dt.datetime(2026, 10, 18, 21, 30)),
    ("0007", "Night Heron", STATUS_AWAITING, 0.1, dt.datetime(2026, 10, 19, 2, 15)),
    ("0003", "Glass Orchid", STATUS_CLOSED, 4.0, dt.datetime(2026, 9, 2, 14, 0)),
    ("0009", "Paper Lantern", STATUS_ONGOING, 1.0, dt.datetime(2026, 10, 11, 8, 45)),
    ("0010", "Red Kestrel", STATUS_AWAITING, 0.1, dt.datetime(2026, 10, 19, 11, 20)),
]

def main() -> None:
    """Preview the window on its own, with simple demo handlers attached."""
    app = QApplication(sys.argv)
    window = ViewCases()

    window.set_cases(DEMO_ROWS)

    window.see_case_details_requested.connect(
        lambda case: print(f"See details: {case.case_id} ({case.codename}), status: {case.status}")
    )
    window.edit_case_requested.connect(
        lambda case: print(f"Edit case: {case.case_id} ({case.codename})")
    )
    window.back_requested.connect(lambda: print("Back requested"))
 
    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()
