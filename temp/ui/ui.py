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

dg = DataGenerator()

class MainWindow(QMainWindow):
    clan_tag_received = Signal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setFixedSize(1280, 720)

        self.members_table_data = []
        self.chosen_member = None
        self.player_frame_data = []
        self.extra_panel_data = []

        self.on_startup()

    def on_startup(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setSpacing(10)
        self.startup_panel = StartupPanel(self.central_widget)
        self.main_layout.addWidget(self.startup_panel)
        self.startup_panel.clan_tag_entered.connect(self.on_clantag_entered)

    def on_clantag_entered(self, clantag):
        print(f"Получен тег клана: {clantag}")
        if self.check_clantag_existance(clantag):
            # ! ПОЛУЧЕНИЕ ВСЕХ ДАННЫХ ИЗ COCAPI
            #self.members_table_data = 
            #self.chosen_member = 
            #self.player_frame_data = 
            #self.extra_panel_data = 

            self.startup_panel.eliminate()
            self.setup_layouts(clantag)
        
        else:
            self.startup_panel.show_temporary_message(f"Не существует клана с тегом {clantag}")

    def check_clantag_existance(self, clantag):
        ...
        return True

    def on_member_selected(self, tag):
        print(f"Выбран участник с тегом: {tag}")
        self.chosen_member = tag
        self.player_frame.chosen_member = tag
        self.player_frame.fill_with_data()

    def setup_layouts(self, clantag):
        self.left_panel = QVBoxLayout()
        self.left_panel.setContentsMargins(0, 0, 0, 0)
        self.left_panel.setSpacing(0)
        self.create_members_table()

        self.members_table.member_selected.connect(self.on_member_selected)

        self.central_panel = QHBoxLayout()
        self.create_player_frame()

        self.right_panel = QHBoxLayout()
        #self.create_extra_frame()

        self.main_layout.addLayout(self.left_panel)
        self.main_layout.addLayout(self.central_panel)
        self.main_layout.addLayout(self.right_panel)

        self.left_panel.addWidget(self.members_table)

        self.central_panel.addWidget(self.player_frame)

        #self.right_panel.addWidget(self.extra_frame)

        #self.extra_frame.show_empty()

    def create_members_table(self):
        self.members_table_data = dg.create_members_table_data(50)
        self.members_table = MembersTable(self.members_table_data)

    def create_player_frame(self):
        self.player_frame_data = dg.create_player_frame_data()
        self.player_frame = PlayerFrame(self.player_frame_data, self.chosen_member)

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