from __future__ import annotations

import sys
from typing import Iterable, Optional, Tuple


from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)


# Resolve the .ui path relative to this file so the script works from any
# working directory.
from src.utils import UI_DIR
UI_FILE = UI_DIR / "appoint_v2.ui"

# One table row: (name, role applied for, human-readable submission time).
ApplicationRow = Tuple[str, str, str]

# Column indices in tblApplications - named constants beat "magic numbers".
COL_NAME = 0
COL_ROLE = 1
COL_SUBMITTED = 2


class AppointWindow(QMainWindow):
    """Review screen listing pending applications.

    Signals
    -------
    application_accepted(name, role)
        The Chief accepted the selected application.
    application_rejected(name, role)
        The Chief rejected the selected application.
    back_requested()
        The user pressed *Back*; the owner should close this window and show
        the previous one.

    The row is removed from the table as soon as a decision is made, so the
    list always shows only applications that are still undecided.
    """

    application_accepted = pyqtSignal(str, str)
    application_rejected = pyqtSignal(str, str)
    back_requested = pyqtSignal()

    # Type hints for widgets created by ``uic.loadUi`` (auto-complete only).
    lblTitle: QLabel
    lblPendingCount: QLabel
    tblApplications: QTableWidget
    btnAccept: QPushButton
    btnReject: QPushButton
    btnBack: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create all widgets from the .ui file and attach them to ``self``.
        uic.loadUi(UI_FILE, self) # type: ignore

        self.setWindowTitle("Asche Yiu Police Department - Incoming Applications")
        self._connect_signals()

        # Sync the count label and button states with whatever rows the
        # .ui file shipped with.
        self._refresh_state()

    # ------------------------------------------------------------------ setup
    def _connect_signals(self) -> None:
        """Wire widget events to the handler methods below."""
        self.btnAccept.clicked.connect(lambda: self._decide(accepted=True))
        self.btnReject.clicked.connect(lambda: self._decide(accepted=False))
        self.btnBack.clicked.connect(self.back_requested)

        # Accept/Reject only make sense while a row is selected, so keep the
        # buttons' enabled state in step with the selection.
        self.tblApplications.itemSelectionChanged.connect(self._refresh_state)


    def _clear_table(self) -> None: 
        """ Clears the applications table """
        self.tblApplications.clearContents()
        self.tblApplications.setRowCount(0)
    # ---------------------------------------------------------- public helpers
    def set_applications(self, rows: Iterable[ApplicationRow]) -> None:
        """Replace the table contents with ``rows``.

        Parameters
        ----------
        rows:
            Iterable of ``(name, role, submitted)`` tuples, for example
            ``("John Johnson", "Fieldworker", "Today, 09:12")``.
        """
        table = self.tblApplications
        table.clearContents()  # drop the design-time sample rows
        table.setRowCount(0)

        for name, role, submitted in rows:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, COL_NAME, QTableWidgetItem(name))
            table.setItem(row, COL_ROLE, QTableWidgetItem(role))
            table.setItem(row, COL_SUBMITTED, QTableWidgetItem(submitted))

        self._refresh_state()

    def pending_count(self) -> int:
        """Number of applications still waiting for a decision."""
        return self.tblApplications.rowCount()

    # --------------------------------------------------------------- internals
    def _selected_row(self) -> Optional[int]:
        """Return the selected row index, or ``None`` if nothing is selected.

        The table uses single-row selection (set in the .ui file), so at most
        one row can be selected at a time.
        """
        rows = self.tblApplications.selectionModel().selectedRows() # type: ignore
        return rows[0].row() if rows else None

    def _cell_text(self, row: int, column: int) -> str:
        """Safely read a cell's text (empty string if the cell has no item)."""
        item = self.tblApplications.item(row, column)
        return item.text() if item is not None else ""

    def _decide(self, accepted: bool) -> None:
        """Record the Chief's decision for the selected row.

        Emits the matching signal, then removes the row from the table.
        """
        row = self._selected_row()
        if row is None:
            return  # buttons are disabled in this case; guard anyway

        name = self._cell_text(row, COL_NAME)
        role = self._cell_text(row, COL_ROLE)

        response = QMessageBox.warning(
            self,
            "Confirmation Box",
            f"Are you sure you want to {"Accept" if accepted else "Reject"} this person?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel
        )

        # Emit first, so listeners see the application while it is still on
        # screen; then remove it from the pending list.
        if response == QMessageBox.StandardButton.Ok:
            if accepted :
                self.application_accepted.emit(name, role)
            else:
                self.application_rejected.emit(name, role)

            self.tblApplications.removeRow(row)
            self._refresh_state()
        self.tblApplications.clearSelection()

    def _refresh_state(self) -> None:
        """Update the "N awaiting" label and enable/disable the buttons."""
        count = self.pending_count()

        if count == 0:
            self.lblPendingCount.setText("No applications awaiting your decision")
        else:
            self.lblPendingCount.setText(f"{count} awaiting your decision")

        has_selection = self._selected_row() is not None
        self.btnAccept.setEnabled(has_selection)
        self.btnReject.setEnabled(has_selection)


def main() -> None:
    """Preview the window on its own, with simple demo handlers attached."""
    app = QApplication(sys.argv)
    window = AppointWindow()

    APPLICATIONS = [
        ("John", "Warden", "Today, 09:12"),
        ("Jngle", "Detective", "Yesterday 17:40")
    ]
    window.set_applications(APPLICATIONS)

    window.application_accepted.connect(lambda n, r: print(f"Accepted: {n} ({r})"))
    window.application_rejected.connect(lambda n, r: print(f"Rejected: {n} ({r})"))
    window.back_requested.connect(lambda: print("Back requested"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
