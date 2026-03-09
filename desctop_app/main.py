import sys
from PySide6.QtWidgets import QApplication

from ui import MainWindow


def main():
    app = QApplication(sys.argv)
    print(QApplication.instance())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())




main()