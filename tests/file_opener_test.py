import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
)

from src.case_file_opener import *

class FileListDemo(QMainWindow):
    """Minimal window: double-click a file to open it in its default app."""

    def __init__(self, paths: list[str]) -> None:
        super().__init__()
        self.setWindowTitle("Case file opener - sample")
        self.resize(500, 300)

        self.list_widget = QListWidget()
        for p in paths:
            item = QListWidgetItem(Path(p).name)
            item.setData(FILE_PATH_ROLE, str(p))
            item.setToolTip(str(p))
            self.list_widget.addItem(item)

        self.list_widget.itemDoubleClicked.connect(self._open_item)
        self.setCentralWidget(self.list_widget)

    def _open_item(self, item: QListWidgetItem) -> None:
        open_with_default_app(Path(item.data(FILE_PATH_ROLE)), self)


def main() -> None:
    paths = sys.argv[1:]
    if not paths:
        print("Usage: python case_file_opener_sample.py <file> [<file> ...]")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = FileListDemo(paths)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()