"""
login.py - Login screen for the Asche Yiu Police Department application.

This module loads ``login.ui`` (designed in Qt Designer) and adds the behaviour
the .ui file cannot express: input validation, keyboard handling and signals
that tell the rest of the application what the user wants to do.

Design notes
------------
* The window does **not** authenticate anybody itself. It only collects the
  credentials and emits ``login_requested``. Whatever owns this window (a main
  controller, a database layer, a web API...) connects to that signal, checks
  the credentials and then calls ``show_error()`` or opens the next window.
  This keeps UI code and business logic separate and easy to test.
* Every window in this project uses the same signal-based approach, so they
  can be chained together without importing each other.

Widgets defined in login.ui
---------------------------
    edtName       QLineEdit    - the officer's name
    edtPassword   QLineEdit    - the password (characters are masked)
    btnLogin      QPushButton  - primary action, submits the credentials
    btnRegister   QPushButton  - secondary action, opens the registration form

Run this file directly to preview the window:

    python login.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
)

# The .ui file is expected to sit next to this script. Resolving the path from
# __file__ (instead of the current working directory) means the program works
# no matter where it is launched from.
from src.utils import UI_DIR
UI_FILE = UI_DIR / "login.ui"


class LoginWindow(QMainWindow):
    """The login screen.

    Signals
    -------
    login_requested(name, password)
        Emitted when the user presses *Log In* (or Enter) and both fields are
        filled in. Connect to this to perform the actual authentication.
    register_requested()
        Emitted when the user presses *Apply to Join*. Connect to this to show
        the registration window.
    """

    login_requested = pyqtSignal(str, str)
    register_requested = pyqtSignal()

    # Type annotations for the widgets that ``uic.loadUi`` creates at runtime.
    # They do not create attributes; they only help IDEs with auto-completion
    # and static type checkers understand ``self.edtName`` etc.
    edtName: QLineEdit
    edtPassword: QLineEdit
    btnLogin: QPushButton
    btnRegister: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Build the UI from the .ui file. Passing ``self`` makes every widget
        # in the file an attribute of this window (self.edtName, ...), and
        # also applies the shared dark/gold style sheet stored in the file.
        uic.loadUi(UI_FILE, self)

        self.setWindowTitle("Asche Yiu Police Department - Login")
        self._connect_signals()

    # ------------------------------------------------------------------ setup
    def _connect_signals(self) -> None:
        """Wire widget events to the handler methods below."""
        self.btnLogin.clicked.connect(self._on_login_clicked)
        self.btnRegister.clicked.connect(self.register_requested)

        # Keyboard convenience: Enter in the name field jumps to the password
        # field, Enter in the password field submits the form.
        self.edtName.returnPressed.connect(self.edtPassword.setFocus)
        self.edtPassword.returnPressed.connect(self._on_login_clicked)

    # --------------------------------------------------------------- handlers
    def _on_login_clicked(self) -> None:
        """Validate the form and, if it is complete, emit ``login_requested``."""
        name = self.edtName.text().strip()
        # The password is deliberately NOT stripped: spaces may be part of it.
        password = self.edtPassword.text()

        # Basic "is anything missing?" check. Rules about *valid* credentials
        # belong to whoever handles ``login_requested``.
        if not name:
            self.show_error("Please enter your name.")
            self.edtName.setFocus()
            return
        if not password:
            self.show_error("Please enter your password.")
            self.edtPassword.setFocus()
            return

        self.login_requested.emit(name, password)
        self.reset_form()

    # ---------------------------------------------------------- public helpers
    def show_error(self, message: str) -> None:
        """Show a warning dialog. Call this when a login attempt fails."""
        QMessageBox.warning(self, "Login", message)

    def clear_password(self) -> None:
        """Empty the password box and focus it (use after a failed attempt)."""
        self.edtPassword.clear()
        self.edtPassword.setFocus()

    def reset_form(self) -> None:
        """Clear both inputs, e.g. after logging out."""
        self.edtName.clear()
        self.edtPassword.clear()
        self.edtName.setFocus()


def main() -> None:
    """Preview the window on its own, with simple demo handlers attached."""
    app = QApplication(sys.argv)
    window = LoginWindow()

    # Demo handlers only. Never print passwords, even in demo code.
    window.login_requested.connect(lambda name, _pw: print(f"Login requested for: {name}"))
    window.register_requested.connect(lambda: print("Registration requested"))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
