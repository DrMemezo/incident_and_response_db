"""
dashboard_chief.py - Main dashboard shown to the Police Chief after logging in.

Loads ``dashboard_chief.ui``. The screen has two parts:

* a **staff card** at the top (avatar with initials, name, role + Staff ID, and
  a "Pending applications" counter), and
* a grid of **action tiles** (View Cases, Open Case, Review Requests, ...).

This module adds
----------------
* Methods to change what the staff card shows::

      dashboard.set_staff_name("Sarah Yiu")       # also updates the avatar initials
      dashboard.set_staff_id(1)                   # shown as "0001"
      dashboard.set_pending_applications(3)

  or all three at once::

      dashboard.update_info("Sarah Yiu", 1, 3)

* One signal per button. The dashboard never opens other windows itself; it
  only announces what the user clicked. Whatever owns the dashboard (see
  ``dashboard_demo.py``) connects to those signals and decides what to show.

Widgets defined in dashboard_chief.ui
-------------------------------------
    lblAvatar          QLabel   - round badge with the staff member's initials
    lblStaffName       QLabel   - e.g. "Sarah Yiu"
    lblStaffRole       QLabel   - e.g. "Police Chief  ·  Staff ID 0001"
    lblStatLabel       QLabel   - "Pending applications" (static caption)
    lblStatValue       QLabel   - the big gold number
    btnViewCases, btnOpenCase, btnCreateSuspect,
    btnReviewRequests, btnAssignCase, btnAppointStaff,
    btnCloseCase       QPushButton - action tiles
    btnLogout          QPushButton - log out

Run this file directly to preview the window:

    python dashboard_chief.py
"""

from __future__ import annotations

import sys
from typing import Union

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

# Resolve the .ui path relative to this file so the script works from any
# working directory.
from src.utils import UI_DIR
UI_FILE = UI_DIR / "dashboard_chief.ui"

# The title printed before the Staff ID. It is fixed for this dashboard
# (it is the *Chief's* dashboard), so it is a constant rather than a parameter.
ROLE_TITLE = "Police Chief"

# The role line in the .ui file separates title and ID with a middle dot
# surrounded by two spaces on each side. Keeping it in one place means the
# format can be changed easily.
ROLE_SEPARATOR = "  \u00b7  "  # "  ·  "


class ChiefDashboardWindow(QMainWindow):
    """The Chief's dashboard.

    Signals
    -------
    One no-argument signal per button, named after what the user wants to do:

        view_cases_requested        View Cases
        open_case_requested         Open Case
        create_suspect_requested    Create Suspect
        review_requests_requested   Review Requests
        assign_case_requested       Assign Case
        appoint_staff_requested     Appoint Staff
        close_case_requested        Close Case
        logout_requested            Log out
    """

    view_cases_requested = pyqtSignal()
    open_case_requested = pyqtSignal()
    create_suspect_requested = pyqtSignal()
    review_requests_requested = pyqtSignal()
    assign_case_requested = pyqtSignal()
    appoint_staff_requested = pyqtSignal()
    close_case_requested = pyqtSignal()
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
    btnAssignCase: QPushButton
    btnAppointStaff: QPushButton
    btnCloseCase: QPushButton
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
        self._staff_id = "0001"

        self._connect_signals()

    # ------------------------------------------------------------------ setup
    def _connect_signals(self) -> None:
        """Re-emit every button click as a meaningful, named signal."""
        # Passing a signal to ``connect`` forwards the call, so a click on the
        # button simply triggers the matching signal. ``clicked`` also carries
        # a ``checked`` bool, which is harmless for a no-argument signal.
        self.btnViewCases.clicked.connect(self.view_cases_requested)
        self.btnOpenCase.clicked.connect(self.open_case_requested)
        self.btnCreateSuspect.clicked.connect(self.create_suspect_requested)
        self.btnReviewRequests.clicked.connect(self.review_requests_requested)
        self.btnAssignCase.clicked.connect(self.assign_case_requested)
        self.btnAppointStaff.clicked.connect(self.appoint_staff_requested)
        self.btnCloseCase.clicked.connect(self.close_case_requested)
        self.btnLogout.clicked.connect(self.logout_requested)

    # --------------------------------------------------- public update methods
    def update_info(
        self,
        name: str,
        staff_id: Union[int, str],
        pending_applications: int,
    ) -> None:
        """Update the whole staff card in one call.

        Parameters
        ----------
        name:
            Display name, e.g. ``"Sarah Yiu"``.
        staff_id:
            Staff ID. An ``int`` is zero-padded to four digits (``1`` ->
            ``"0001"``); a ``str`` is shown exactly as given.
        pending_applications:
            Number of applications waiting for the Chief (``>= 0``).
        """
        self.set_staff_name(name)
        self.set_staff_id(staff_id)
        self.set_pending_applications(pending_applications)

    def set_staff_name(self, name: str) -> None:
        """Show ``name`` in the staff card and refresh the avatar initials."""
        name = name.strip()
        self.lblStaffName.setText(name)
        self.lblAvatar.setText(self._initials(name))

    def set_staff_id(self, staff_id: Union[int, str]) -> None:
        """Show ``staff_id`` in the role line ("Police Chief  ·  Staff ID 0001").

        An ``int`` is zero-padded to four digits; a ``str`` is used as given.
        """
        if isinstance(staff_id, int):
            staff_id = f"{staff_id:04d}"
        self._staff_id = str(staff_id).strip()
        self.lblStaffRole.setText(
            f"{ROLE_TITLE}{ROLE_SEPARATOR}Staff ID {self._staff_id}"
        )

    def set_pending_applications(self, count: int) -> None:
        """Show how many applications are waiting for the Chief.

        Raises
        ------
        ValueError
            If ``count`` is negative.
        """
        if count < 0:
            raise ValueError(f"count must be >= 0, got {count}")
        self.lblStatValue.setText(str(count))

    # --------------------------------------------------------------- read-back
    def pending_applications(self) -> int:
        """The number currently displayed in the counter."""
        return int(self.lblStatValue.text())

    # --------------------------------------------------------------- internals
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

    NAME = "JINGLE SLIMER JIMER"
    S_ID = 3
    NUM_APPLICATIONS = 10
    
    app = QApplication(sys.argv)
    window = ChiefDashboardWindow()
    window.update_info(NAME, S_ID, NUM_APPLICATIONS)

    window.view_cases_requested.connect(lambda: print("View Cases"))
    window.open_case_requested.connect(lambda: print("Open Case"))
    window.create_suspect_requested.connect(lambda: print("Create Suspect"))
    window.review_requests_requested.connect(lambda: print("Review Requests"))
    window.assign_case_requested.connect(lambda: print("Assign Case"))
    window.appoint_staff_requested.connect(lambda: print("Appoint Staff"))
    window.close_case_requested.connect(lambda: print("Close Case"))
    window.logout_requested.connect(lambda: print("Log out"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()