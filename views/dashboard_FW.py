from __future__ import annotations

import sys
from typing import Union

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from src.utils import UI_DIR
UI_FILE = UI_DIR / "dashboard_fieldworker.ui"
ROLE_TITLE = "Fieldworker"

# * The weird dot thing in between the title and staff id
ROLE_SEPARATOR = "  \u00b7  "  # "  ·  "


class FieldworkerDashboardWindow(QMainWindow):
    """The Fieldworkers's dashboard.

    Signals
    -------
    One no-argument signal per button, named after what the user wants to do:

        view_cases_requested            View Cases
        rqst_open_case_requested        Request to Open Case
        rqst_create_suspect_requested   Request to Create Suspect
        view_requests_requested         View Requests Submitted
        logout_requested                Log out
    """

    view_cases_requested = pyqtSignal()
    rqst_open_case_requested = pyqtSignal()
    rqst_create_suspect_requested = pyqtSignal()
    view_requests_requested = pyqtSignal()
    logout_requested = pyqtSignal()

    # Type hints for widgets created by ``uic.loadUi`` (auto-complete only).
    lblAvatar: QLabel
    lblStaffName: QLabel
    lblStaffRole: QLabel
    lblStatLabel: QLabel 
    lblStatValue: QLabel # How many case creation / suspect creation requests are unresolved
    btnViewCases: QPushButton 
    btnRequestCase: QPushButton
    btnRequestSuspect: QPushButton
    btnViewRequests: QPushButton
    btnLogout: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create all widgets from the .ui file and attach them to ``self``.
        uic.loadUi(UI_FILE, self)   # type: ignore

        self.setWindowTitle("Asche Yiu Police Department - Dashboard")

        # The role line shows "<title> · Staff ID <id>", but the name, ID and
        # count can be changed independently. The ID is therefore remembered
        # here so ``set_staff_id`` / ``set_staff_name`` can rebuild the label.
        # The initial value is the design-time sample data from the .ui file.
        self._staff_id = "PLACEHOLDER" 

        self._connect_signals()

    def _connect_signals(self) -> None:
        """Re-emit every button click as a meaningful, named signal."""
        # Passing a signal to ``connect`` forwards the call, so a click on the
        # button simply triggers the matching signal. ``clicked`` also carries
        # a ``checked`` bool, which is harmless for a no-argument signal.
        self.btnViewCases.clicked.connect(self.view_cases_requested)
        self.btnRequestCase.clicked.connect(self.rqst_open_case_requested)
        self.btnRequestSuspect.clicked.connect(self.rqst_create_suspect_requested)
        self.btnViewRequests.clicked.connect(self.view_requests_requested)
        self.btnLogout.clicked.connect(self.logout_requested)

    def update_info(
        self,
        name: str,
        staff_id: Union[int, str],
        num_of_open_requests: int
    ) -> None:
        """Update the whole staff card in one call.

        Parameters
        ----------
        name:
            Display name, e.g. ``"Ayesha Khan"``.
        staff_id:
            Staff ID. An ``int`` is zero-padded to four digits (``1`` ->
            ``"0001"``); a ``str`` is shown exactly as given.
        num_of_open_requests:
            How many cases, submitted by the FW, that are still pending
        """
        self.set_staff_name(name)
        self.set_staff_id(staff_id)
        self.set_open_requests(num_of_open_requests)


    def set_open_requests(self, num: int) -> None:
        if num < 0:
            raise ValueError("Number of pending cases cannot be negative")

        self.lblStatValue.setText(str(num))

    def set_staff_name(self, name: str) -> None:
        """Show ``name`` in the staff card and refresh the avatar initials."""
        name = name.strip()
        self.lblStaffName.setText(name)
        self.lblAvatar.setText(self._initials(name))

    def set_staff_id(self, staff_id: Union[int, str]) -> None:
        """Show ``staff_id`` in the role line ("Detective  ·  Staff ID 0001").

        An ``int`` is zero-padded to four digits; a ``str`` is used as given.
        """
        if isinstance(staff_id, int):
            staff_id = f"{staff_id:04d}"
        self._staff_id = str(staff_id).strip()
        self.lblStaffRole.setText(
            f"{ROLE_TITLE}{ROLE_SEPARATOR}Staff ID {self._staff_id}"
        )

    @staticmethod
    def _initials(name: str) -> str:
        """Turn "Sarah Yiu" into "SY" (first letters of the first two words).

        A single name gives one letter ("Madonna" -> "M"); an empty name gives
        "?" so the avatar is never blank.
        """
        parts = name.split()
        if not parts:
            return "?"
        return "".join(part[0] for part in parts[:2]).upper()


def main() -> None:
    """Preview the window on its own, printing every button press."""

    print("THIS IS FOR DEMONSTRATION PURPOSES ONLY")
    NAME = "Jingle Jongle"
    S_ID = 6767
    NUM_OF_CASES = 10
    
    app = QApplication(sys.argv)
    window = FieldworkerDashboardWindow()
    window.update_info(NAME, S_ID, NUM_OF_CASES)

    window.view_cases_requested.connect(lambda: print("View Cases"))
    window.rqst_open_case_requested.connect(lambda: print("Request to Open Case"))
    window.rqst_create_suspect_requested.connect(lambda: print("Request to Create Suspect"))
    window.view_requests_requested.connect(lambda: print("View My Requests"))
    window.logout_requested.connect(lambda: print("Log out"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()