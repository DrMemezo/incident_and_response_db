
from __future__ import annotations

import sys
from typing import Union

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from src.utils import UI_DIR
UI_FILE = UI_DIR / "dashboard_detective.ui"
ROLE_TITLE = "Detective"

# * The weird dot thing in between the title and staff id
ROLE_SEPARATOR = "  \u00b7  "  # "  ·  "


class DetectiveDashboardWindow(QMainWindow):
    """The Detective's dashboard.

    Signals
    -------
    One no-argument signal per button, named after what the user wants to do:

        view_cases_requested        View Cases
        open_case_requested         Open Case
        create_suspect_requested    Create Suspect
        review_requests_requested   Review Requests
        logout_requested            Log out
    """

    view_cases_requested = pyqtSignal()
    open_case_requested = pyqtSignal()
    create_suspect_requested = pyqtSignal()
    review_requests_requested = pyqtSignal()
    logout_requested = pyqtSignal()

    # Type hints for widgets created by ``uic.loadUi`` (auto-complete only).
    lblAvatar: QLabel
    lblStaffName: QLabel
    lblStaffRole: QLabel
    lblStatLabel: QLabel
    lblStatValue: QLabel
    btnViewCases: QPushButton
    btnOpenCase: QPushButton
    btnCreateSuspect: QPushButton
    btnReviewRequests: QPushButton
    btnLogout: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create all widgets from the .ui file and attach them to ``self``.
        uic.loadUi(UI_FILE, self) # type: ignore

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
        self.btnOpenCase.clicked.connect(self.open_case_requested)
        self.btnCreateSuspect.clicked.connect(self.create_suspect_requested)
        self.btnReviewRequests.clicked.connect(self.review_requests_requested)
        self.btnLogout.clicked.connect(self.logout_requested)

    def update_info(
        self,
        name: str,
        staff_id: Union[int, str],
        cases: list[str]
    ) -> None:
        """Update the whole staff card in one call.

        Parameters
        ----------
        name:
            Display name, e.g. ``"Rahim Malik"``.
        staff_id:
            Staff ID. An ``int`` is zero-padded to four digits (``1`` ->
            ``"0001"``); a ``str`` is shown exactly as given.
        cases:
            List of case codenames. Example: ["Blue Harbor", "Shibuya Incident"]
        """
        self.set_staff_name(name)
        self.set_staff_id(staff_id)
        self.set_current_case(cases)

    def set_current_case(self, cases: list[str]) -> None:
        """Takes in a list of cases that the detective is currently
        handling. Raises an error if it's > 2 """
        if len(cases) > 2:
            raise ValueError("A Detective cannot have more than 2 cases assigned.")
        
        if cases == []: 
            self.lblStatValue.setText("No Case Assigned")
        else:
            self.lblStatValue.setText(", ".join(cases))       

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
    CASES = ["The Bite of '87", "What is the dog doing?"]
    
    app = QApplication(sys.argv)
    window = DetectiveDashboardWindow()
    window.update_info(NAME, S_ID, CASES)

    window.view_cases_requested.connect(lambda: print("View Cases"))
    window.open_case_requested.connect(lambda: print("Open Case"))
    window.create_suspect_requested.connect(lambda: print("Create Suspect"))
    window.review_requests_requested.connect(lambda: print("Review Requests"))
    window.logout_requested.connect(lambda: print("Log out"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()