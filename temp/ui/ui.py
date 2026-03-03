import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

if __name__ == "__main__":
    from members_table import MembersTable
    from player_frame import PlayerFrame
    from extra_info_panel import ExtraPanel
    from data_generator import DataGenerator
    from startup_panel import StartupPanel
else:
    from .members_table import MembersTable
    from .player_frame import PlayerFrame
    from .extra_info_panel import ExtraPanel
    from .data_generator import DataGenerator
    from .startup_panel import StartupPanel

dg = DataGenerator

class MainWindow(QMainWindow):
    clan_tag_received = Signal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setFixedSize(1280, 720)

        self.is_clan_selected = False

        self.on_startup()

    def on_startup(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.startup_panel = StartupPanel(central_widget)
        layout.addWidget(self.startup_panel)
        self.startup_panel.clan_tag_entered.connect(self.on_clantag_entered)

    def on_clantag_entered(self, clantag):
        print(f"Получен тег клана: {clantag}")
        self.startup_panel.eliminate()
        self.setup_layouts(clantag)

    def on_player_selected(self):
        ...

    def setup_layouts(self, clantag):
        ...

    def create_members_table(self):
        self.members_table = MembersTable()

    def create_player_frame(self):
        self.player_frame = PlayerFrame()

    def create_extra_panel(self):
        self.extra_panel = ExtraPanel()


def main():
    app = QApplication(sys.argv)
    print(QApplication.instance())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()