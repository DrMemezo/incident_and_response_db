from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QMessageBox,
    QWidget,
)

FILE_PATH_ROLE = Qt.ItemDataRole.UserRole


# * This is more recommended
def open_with_default_app(path: Path, parent: QWidget | None = None) -> bool:
    """Open ``path`` in whatever application the OS associates with its extension."""

    if not path.is_file():
        QMessageBox.warning(parent, "File not found", f"Could not find:\n{path}")
        return False

    if QDesktopServices.openUrl(QUrl.fromLocalFile(str(path.resolve()))):
        return True

    QMessageBox.warning(
        parent, "Could not open file",
        f"No application is set up to open:\n{path.name}",
    )
    return False


def open_with_os_native(path: Path) -> None:
    """The same thing done by hand, without Qt. Shown for reference only."""
    if sys.platform.startswith("win"):
        import os
        os.startfile(path)  # type: ignore[attr-defined]  # Windows only
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=True)
    else:  # Linux and other Unix-like systems
        subprocess.run(["xdg-open", str(path)], check=True)



if __name__ == "__main__":
    pass
