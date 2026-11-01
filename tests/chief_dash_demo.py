"""
dashboard_demo.py - Demo: Chief dashboard <-> "Review Requests" screen.

Flow implemented here
---------------------

    +------------------+    review_requests_requested    +-----------------+
    | ChiefDashboard   | ------------------------------> |  AppointWindow  |
    | Window           | <------------------------------ |                 |
    +------------------+          back_requested         +-----------------+
          ^                                                      |
          |        pending_count_changed(count)                  |
          +------------------------------------------------------+
            keeps the dashboard's "Pending applications" number in sync

Every other dashboard tile (View Cases, Open Case, ...) and the accept /
reject decisions are only **printed to the terminal** for now - they are the
places where you would later open further screens or save to a database.

It uses the same pattern as ``flow_demo.py``: the windows only emit signals,
and one controller (``DashboardController``) owns them and decides what is
shown. All transitions are listed in ``_connect_signals()``.

Run it with:

    python dashboard_demo.py

(dashboard_chief.py and appoint_v2_1.py, plus their .ui files, must be in the
same folder.)
"""

# TODO: Remove slop for demo

from __future__ import annotations

import sys
from datetime import datetime, timedelta

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow

from views.appoint import AppointWindow
from views.dashboard_chief import ChiefDashboardWindow

# Seconds until the demo simulates a brand-new application arriving, to show
# ``add_row()`` and the live counter in action. Set to ``None`` to disable.

APPLICATIONS = [
            ("John Johnson", "Fieldworker", "Today, 07:14"),
            ("J Robert Oppenheimer", "Detective", "Today, 07:14"),
            ("Ada Lovelace", "Warden", "Today, 07:14"),
        ]

class DashboardController:
    """Owns the dashboard and the review screen and connects them."""

    def __init__(self) -> None:
        # Create both windows once; they stay alive (hidden) for the whole run.
        self.dashboard = ChiefDashboardWindow()
        self.review = AppointWindow()

        # The window that is currently visible (None until start() is called).
        self._current: QMainWindow | None = None

        # Staff card first. The pending count starts at 0 and is filled in
        # automatically when the review screen is populated below.

        self._connect_signals()
        self._load_sample_applications()

    # ------------------------------------------------------------------ flow
    def _connect_signals(self) -> None:
        """The whole demo flow, in one place.

        Read as: "when <window> emits <signal>, call <handler>".
        """
        # --- Real navigation -------------------------------------------------
        self.dashboard.review_requests_requested.connect(self._show_review)
        self.review.back_requested.connect(self._show_dashboard)


        # --- Decisions: print for now ----------------------------------------
        self.review.application_accepted.connect(
            lambda name, role: print(f"[accepted] {name} -> {role}")
        )
        self.review.application_rejected.connect(
            lambda name, role: print(f"[rejected] {name} -> {role}")
        )

        # --- Other dashboard tiles: print for now ----------------------------
        # (signal, text to print). Replace a print with real navigation as the
        # corresponding screen gets built.
        placeholders = [
            (self.dashboard.view_cases_requested, "View Cases"),
            (self.dashboard.open_case_requested, "Open Case"),
            (self.dashboard.create_suspect_requested, "Create Suspect"),
            (self.dashboard.assign_case_requested, "Assign Case"),
            (self.dashboard.appoint_staff_requested, "Appoint Staff"),
            (self.dashboard.close_case_requested, "Close Case"),
            (self.dashboard.logout_requested, "Log out"),
        ]
        for signal, label in placeholders:
            # ``text=label`` binds the *current* label to each lambda. Without
            # it every lambda would print the last label in the list (a classic
            # Python closure pitfall in loops).
            signal.connect(lambda *_args, text=label: print(f"[tile] {text}"))

    def _load_sample_applications(self) -> None:
        """Fill the review table with sample data (a real app would query a DB)."""
        self.review.set_applications(
            APPLICATIONS
        )

    # ------------------------------------------------------------ navigation
    def start(self) -> None:
        """Show the first screen. Call once after creating the controller."""
        self._show(self.dashboard)


    def _show(self, target: QMainWindow) -> None:
        """Hide the current window and show ``target``, centred on the old one."""
        previous = self._current

        if previous is not None:
            geometry = target.geometry()
            geometry.moveCenter(previous.geometry().center())
            target.setGeometry(geometry)
            previous.hide()

        target.show()
        target.raise_()
        target.activateWindow()
        self._current = target

    def _show_review(self) -> None:
        """Dashboard -> Review screen."""
        self._show(self.review)

    def _show_dashboard(self) -> None:
        """Review screen -> Dashboard."""
        self._show(self.dashboard)



def main() -> None:
    app = QApplication(sys.argv)

    NAME = "JINGLE SLIMER JIMER"
    S_ID = 3
    NUM_APPLICATIONS = len(APPLICATIONS)

    # Keep a reference for the lifetime of the program; if the controller were
    # garbage-collected, its signal connections would disappear.
    controller = DashboardController()
    controller.dashboard.update_info(NAME, S_ID, NUM_APPLICATIONS)
    controller.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()