"""
register_submitted.py - "Application Submitted" confirmation screen.

Shown right after an applicant submits the form in ``register_v2.py``. It is a
simple status screen: a gold check-mark, a title, an explanatory message and a
single *Back to Login* button.

Widgets defined in register_submitted.ui
----------------------------------------
    lblIcon         QLabel       - the gold check-mark badge
    lblTitle        QLabel       - "Application Submitted"
    lblMessage      QLabel       - explanatory text (word-wrapped)
    btnBackToLogin  QPushButton  - primary action, returns to the login screen

Its sibling screen is ``register_denied.py``, which uses the same layout with
a red cross and a rejection message.

Run this file directly to preview the window:

    python register_submitted.py
"""

from __future__ import annotations

import sys

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

# Resolve the .ui path relative to this file so the script works from any
# working directory.
from src.utils import UI_DIR
UI_FILE = UI_DIR / "register_submitted.ui"


class RegisterSubmittedWindow(QMainWindow):
    """Confirmation screen shown after an application has been submitted.

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

        self.setWindowTitle("Asche Yiu Police Department - Application Submitted")

        # Re-emit the button click as a semantic signal, so listeners do not
        # need to know which widget triggered it.
        self.btnBackToLogin.clicked.connect(self.back_to_login_requested)

    # ---------------------------------------------------------- public helpers
    def set_message(self, text: str) -> None:
        """Replace the explanatory text, e.g. to mention the applicant by name."""
        self.lblMessage.setText(text)


def main() -> None:
    """Preview the window on its own, with a simple demo handler attached."""
    app = QApplication(sys.argv)
    window = RegisterSubmittedWindow()
    window.back_to_login_requested.connect(lambda: print("Back to login requested"))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
