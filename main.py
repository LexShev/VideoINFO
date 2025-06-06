from __future__ import annotations
import sys
import qdarktheme
from PySide6.QtWidgets import QApplication

from modules.windows.main_window import VideoInfo


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = VideoInfo()
    window.show()
    sys.exit(app.exec())