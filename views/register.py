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
    login_requested = pyqtSignal()

    # Type hints for widgets created by ``uic.loadUi`` (auto-complete only).
    edtName: QLineEdit
    edtPassword: QLineEdit
    cmbRole: QComboBox
    btnSubmitApplication: QPushButton
    btnLoginInstead: QPushButton

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create all widgets from the .ui file and attach them to ``self``.
        # The shared style sheet inside the file is applied at the same time.
        uic.loadUi(UI_FILE, self) #type:ignore

        self.setWindowTitle("Asche Yiu Police Department - Application")
        self._connect_signals()

    # ------------------------------------------------------------------ setup
    def _connect_signals(self) -> None:
        """Wire widget events to the handler methods below."""
        self.btnSubmitApplication.clicked.connect(self._on_submit_clicked)
        self.btnLoginInstead.clicked.connect(self.login_requested)

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
            self.show_error("Please enter your name.")
            self.edtName.setFocus()
            return
        if not password:
            self.show_error("Please choose a password.")
            self.edtPassword.setFocus()
            return

        #TODO: If there is any other rule needed to be added add them here

        self.edtName.clear()
        self.edtPassword.clear()

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

    def show_error(self, message: str) -> None:
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
