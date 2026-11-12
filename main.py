import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget

from src.mode_base import Mode
from src.login_mode import LoginMode
from src.database.create_database import create_database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.mode: Mode | None = None
        self.enter_mode(LoginMode)

    def enter_mode(self, mode_cls):
        if self.mode is not None:          # only one active mode at a time
            self.exit_mode()
        self.mode = mode_cls(self.stack)
        self.mode.finished.connect(self.exit_mode) # type: ignore
        self.mode.start() # type: ignore

    def exit_mode(self):
        if self.mode is None:
            return
        self.mode.teardown()
        self.mode.deleteLater()
        self.mode = None
        # self.stack.setCurrentWidget(self.menu)

def main():
    create_database()
    
    app = QApplication(sys.argv)
    win = MainWindow()

    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
