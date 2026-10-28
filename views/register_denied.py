"""
register_denied.py - "Application Rejected" screen.

Shown to an applicant whose application the Chief declined (see the *Reject*
button in ``appoint_v2.py``). It mirrors ``register_submitted.py``: same
layout, but with a red cross badge and a rejection message.

Widgets defined in register_denied.ui
-------------------------------------
    lblIcon         QLabel       - the red cross badge
    lblTitle        QLabel       - "Application Rejected"
    lblMessage      QLabel       - explanatory text (word-wrapped)
    btnBackToLogin  QPushButton  - secondary-style button, returns to login

Note: unlike the "submitted" screen, this button deliberately has no
``variant="primary"`` property, so it is drawn in the neutral button style
instead of the gold highlight - there is no positive action to encourage.

Run this file directly to preview the window:

    python register_denied.py
"""

from __future__ import annotations

import sys

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

# Resolve the .ui path relative to this file so the script works from any
# working directory.
from src.utils import UI_DIR
UI_FILE = UI_DIR / "register_denied.ui"


class RegisterDeniedWindow(QMainWindow):
    """Screen telling an applicant that their application was rejected.

    Signals
    -------
    back_to_login_requested()
        Emitted when the user presses *Back to Login*. The owner of this
        window should close it and show the login window.
    """

    back_to_login_requested = pyqtSignal()

    # Type hints for widgets created by ``uic.loadUi`` (auto-complete only).
    lblIcon: QLabel
    lblTitle: QLabel
    lblMessage: QLabel
    btnBackToLogin: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create all widgets from the .ui file and attach them to ``self``.
        uic.loadUi(UI_FILE, self)

        self.setWindowTitle("Asche Yiu Police Department - Application Rejected")

        # Re-emit the button click as a semantic signal.
        self.btnBackToLogin.clicked.connect(self.back_to_login_requested)

    # ---------------------------------------------------------- public helpers
    def set_message(self, text: str) -> None:
        """Replace the explanatory text, e.g. to include a reason for the rejection."""
        self.lblMessage.setText(text)


def main() -> None:
    """Preview the window on its own, with a simple demo handler attached."""
    app = QApplication(sys.argv)
    window = RegisterDeniedWindow()
    window.back_to_login_requested.connect(lambda: print("Back to login requested"))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
