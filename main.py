import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    icon_path = Path(__file__).resolve().parent / "assets" / "icon.ico"

    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()