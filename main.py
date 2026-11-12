import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget

from src.mode_base import Mode
from src.login_mode import LoginMode
from src.chief_mode import ChiefMode
from src.database.create_database import create_database

from src.utils import (CHIEF)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.mode: Mode | None = None
        self.enter_mode(LoginMode, self._after_login)


    def _after_login(self, result):
        if result is None:
            return
        if result["title"] == CHIEF:
            self.enter_mode(ChiefMode, lambda *x : print("idk"), 
                        name=result["name"], s_id=result["s_id"])
        else:
            raise NotImplementedError
        
    # TODO: Fix logout
    def _after_logout(self, *args):
        self.enter_mode(LoginMode, self._after_login)

    def enter_mode(self, mode_cls, on_finish, **kwargs):
        """mode_cls, which mage to switch to
        on_finish, callback function which runs when the mode finished,
        **kwargs keyword args"""
        if self.mode is not None:          # only one active mode at a time
            self.exit_mode()
        self.mode = mode_cls(self.stack, **kwargs)
        self.mode.finished.connect(lambda result : self.exit_mode(result, on_finish)) # type: ignore
        self.mode.start() # type: ignore

    def exit_mode(self, result=None, on_finished=lambda x : print("placeholder")):
        if self.mode is None:
            return
        self.mode.teardown()
        self.mode.deleteLater()
        self.mode = None
        on_finished(result)
        # self.stack.setCurrentWidget(self.menu)

def main():
    create_database()
    
    app = QApplication(sys.argv)
    win = MainWindow()

    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
