from PyQt6.QtWidgets import QStackedWidget, QWidget, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal



class Mode(QObject):
    finished = pyqtSignal()        # emitted when the flow ends (done or cancelled)

    def __init__(self, stack: QStackedWidget):
        super().__init__()
        self.stack = stack
        self._views = []

    def add_view(self, widget: QWidget) -> QWidget:
        self.stack.addWidget(widget)
        self._views.append(widget)
        return widget

    def show(self, widget: QWidget):
        self.stack.setCurrentWidget(widget)

    def start(self):
        raise NotImplementedError

    def teardown(self):
        # Removing and deleting the views also drops their signal connections.
        for w in self._views:
            self.stack.removeWidget(w)
            w.deleteLater()
        self._views.clear()
