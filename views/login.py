import sys

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
)

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

    # Type annotations 
    edtName: QLineEdit
    edtPassword: QLineEdit
    btnLogin: QPushButton
    btnRegister: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        uic.loadUi(UI_FILE, self) #type:ignore

        self.setWindowTitle("Asche Yiu Police Department - Login")
        self._connect_signals()

    def _connect_signals(self) -> None:
        """Wire widget events to the handler methods below."""
        self.btnLogin.clicked.connect(self._on_login_clicked)
        self.btnRegister.clicked.connect(self.register_requested)


    def _on_login_clicked(self) -> None:
        """Validate the form and, if it is complete, emit ``login_requested``."""
        name = self.edtName.text().strip()
        # The password is deliberately NOT stripped: spaces may be part of it.
        password = self.edtPassword.text()

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
