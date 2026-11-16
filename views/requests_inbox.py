import sys
from typing import Optional, Sequence
from dataclasses import dataclass

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
)

from src.utils import UI_DIR
UI_FILE = UI_DIR / "requests_inbox.ui"


@dataclass
class RequestRow():
    """One request as read back from the table, as display strings."""

    table: str               # objectName of the table, e.g. "tblNewCases"
    fields: dict[str, str]   # column header -> cell text


class RequestsInbox(QMainWindow):
    """Pending requests, one table per tab.

    Signals
    -------
    review_requested
        Review pressed; carries a RequestRow for the selected row.
    back_requested
        The user pressed *Back*; the owner should close this window and show
        the previous one.
    """

    back_requested = pyqtSignal()
    review_requested = pyqtSignal(object)

    tabRequests: QTabWidget
    btnBack: QPushButton
    btnReview: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create all widgets from the .ui file and attach them to ``self``.
        uic.loadUi(UI_FILE, self) # type: ignore

        self.setWindowTitle("Asche Yiu Police Department - Pending Requests")
        self._connect_signals()
        self._update_review_button()

    def _connect_signals(self) -> None:
        """Wire widget events to the handler methods below."""
        self.btnReview.clicked.connect(self._on_review_clicked)
        self.btnBack.clicked.connect(self.back_requested)

        self.tabRequests.currentChanged.connect(self._update_review_button)
        for table in self._tables():
            table.itemSelectionChanged.connect(self._update_review_button)

    def _tables(self) -> list[QTableWidget]:
        """Every table in the tab widget."""
        return [
            self.tabRequests.widget(i).findChild(QTableWidget) #type:ignore
            for i in range(self.tabRequests.count())
        ]

    def _current_table(self) -> QTableWidget:
        return self.tabRequests.currentWidget().findChild(QTableWidget)#type:ignore

    def _selected_row(self, table: QTableWidget) -> Optional[int]:
        """Return the selected row index, or ``None`` if nothing is selected."""
        rows = table.selectionModel().selectedRows() #type:ignore
        return rows[0].row() if rows else None

    def _update_review_button(self) -> None:
        """Enable Review only when a row is selected in the visible table."""
        self.btnReview.setEnabled(self._selected_row(self._current_table()) is not None)

    def selected_request(self) -> Optional[RequestRow]:
        """Return the selected request in the visible table, or ``None``."""
        table = self._current_table()
        row = self._selected_row(table)
        if row is None:
            return None

        fields = {}
        for column in range(table.columnCount()):
            header = table.horizontalHeaderItem(column).text() #type:ignore
            item = table.item(row, column)
            fields[header] = item.text() if item else ""
        return RequestRow(table=table.objectName(), fields=fields)

    def _on_review_clicked(self) -> None:
        request = self.selected_request()
        if request is not None:
            self.review_requested.emit(request)

    
    def add_request(self, table_name: str, values: Sequence[str]) -> None:
        """Append a row to the named table. ``values`` is one string per column."""
        table = self.findChild(QTableWidget, table_name)
        row = table.rowCount()
        table.insertRow(row)
        for column, value in enumerate(values):
            table.setItem(row, column, QTableWidgetItem(str(value)))

    def clear_requests(self, table_name: str) -> None:
        """Remove every row from the named table."""
        table = self.findChild(QTableWidget, table_name)
        table.clearContents()
        table.setRowCount(0)


def main() -> None:
    """Preview the window on its own, with simple demo handlers attached."""
    app = QApplication(sys.argv)
    window = RequestsInbox()
    CASE_CHANGES = [
        ("0005", "Blue Harbor", "2.0", "2  (2.1, 2.2)", "Ayesha Khan"),
        ("0009", "Paper Lantern", "1.0", "1  (1.1)", "Bilal Raza"),
    ]
    NEW_CASES = [
        ("Night Heron", "Ayesha Khan", "19/10/2026 02:15", "Today, 02:20"),
    ]
    SUSPECT_REQUESTS = [
        ("Red Cap", "0005  Blue Harbor", "Ayesha Khan", "Yesterday, 16:05"),
        ("Night Janitor", "0009  Paper Lantern", "Bilal Raza", "Yesterday, 12:30"),
    ]
    TABLES = {
        "tblCaseChanges": CASE_CHANGES,
        "tblNewCases": NEW_CASES,
        "tblSuspectRequests": SUSPECT_REQUESTS,
    }
    for tbl_name in TABLES.keys():
        window.clear_requests(tbl_name)

    for tbl_name, ui_rows in TABLES.items():
        new_row = ui_rows[0]
        window.add_request(tbl_name, new_row)
 
    window.review_requested.connect(
        lambda r: print(f"Review in {r.table}: {r.fields}")
    )
    window.back_requested.connect(lambda: print("Back requested"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()