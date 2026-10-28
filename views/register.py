"""
register_v2.py - Application (registration) form for the Asche Yiu Police
Department application.

Loads ``register_v2.ui`` and adds validation and a signal that hands the
completed application to the rest of the program.

How it fits in the application flow
-----------------------------------
    login.py  --(Apply to Join)-->  register_v2.py
                                        |
                                        | application_submitted(name, password, role)
                                        v
                          register_submitted.py  (confirmation screen)

After the Chief reviews the application (see ``appoint_v2.py``) the applicant
will eventually see either the "submitted" or the "denied" status screen.

Widgets defined in register_v2.ui
---------------------------------
    edtName               QLineEdit    - applicant's name
    edtPassword           QLineEdit    - chosen password (masked)
    cmbRole               QComboBox    - Fieldworker / Detective / Warden
    btnSubmitApplication  QPushButton  - primary action

Run this file directly to preview the window:

    python register_v2.py
"""

from __future__ import annotations

import sys

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
)

# Resolve the .ui path relative to this file so the script works from any
# working directory.
from src.utils import UI_DIR
UI_FILE = UI_DIR / "register_v2.ui"


class RegisterWindow(QMainWindow):
    """The application-submission form.

    Signals
    -------
    application_submitted(name, password, role)
        Emitted once the form passes validation. ``role`` is the text of the
        selected combo-box entry (e.g. ``"Detective"``). The receiver is
        responsible for storing the application - and for hashing the password
        before it is saved. Plain-text passwords must never be persisted.
    """

    application_submitted = pyqtSignal(str, str, str)

    # Type hints for widgets created by ``uic.loadUi`` (auto-complete only).
    edtName: QLineEdit
    edtPassword: QLineEdit
    cmbRole: QComboBox
    btnSubmitApplication: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create all widgets from the .ui file and attach them to ``self``.
        # The shared style sheet inside the file is applied at the same time.
        uic.loadUi(UI_FILE, self)

        self.setWindowTitle("Asche Yiu Police Department - Application")
        self._connect_signals()

    # ------------------------------------------------------------------ setup
    def _connect_signals(self) -> None:
        """Wire widget events to the handler methods below."""
        self.btnSubmitApplication.clicked.connect(self._on_submit_clicked)

        # Enter in the name field moves on to the password field; Enter in
        # the password field submits (the combo box is skipped on purpose,
        # because it already has a sensible default selection).
        self.edtName.returnPressed.connect(self.edtPassword.setFocus)
        self.edtPassword.returnPressed.connect(self._on_submit_clicked)

    # --------------------------------------------------------------- handlers
    def _on_submit_clicked(self) -> None:
        """Validate the form and emit ``application_submitted`` if it is complete."""
        name = self.edtName.text().strip()
        password = self.edtPassword.text()  # not stripped - spaces may be intentional
        role = self.selected_role()

        if not name:
            self._show_error("Please enter your name.")
            self.edtName.setFocus()
            return
        if not password:
            self._show_error("Please choose a password.")
            self.edtPassword.setFocus()
            return

        # Any further rules (minimum length, duplicate names, ...) are
        # business logic and belong to the code that receives the signal.
        self.application_submitted.emit(name, password, role)

    # ---------------------------------------------------------- public helpers
    def selected_role(self) -> str:
        """Return the role currently chosen in the "Applying as" drop-down."""
        return self.cmbRole.currentText()

    def reset_form(self) -> None:
        """Clear the inputs and restore the default role (call after submitting)."""
        self.edtName.clear()
        self.edtPassword.clear()
        self.cmbRole.setCurrentIndex(0)
        self.edtName.setFocus()

    def _show_error(self, message: str) -> None:
        """Show a validation warning dialog."""
        QMessageBox.warning(self, "Application", message)


def main() -> None:
    """Preview the window on its own, with a simple demo handler attached."""
    app = QApplication(sys.argv)
    window = RegisterWindow()

    # Demo handler only. Never print passwords, even in demo code.
    window.application_submitted.connect(
        lambda name, _pw, role: print(f"Application received: ( {name}, # {_pw} ) -> {role}")
    )

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
