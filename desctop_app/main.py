import sys
from PySide6.QtWidgets import QApplication

from ui import MainWindow
from config import settings
from utils import AppState, Logger, MockApiClient
from api import ApiClient

def main():
    app = QApplication(sys.argv)
    print(QApplication.instance())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())




main()