# Открывается при нажатии кнопки "список игроков" в меню
#
# Слева таблица игроков
# Справа фрейм игрока
#
# Кнопки "Меню", "Добавить игрока", "Удалить игрока"



from PySide6.QtWidgets import (QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QFont, QKeyEvent

from ui.custom_widgets import MockWidget, PlayerFrame, PlayersTable
from ui.dialogs import AddPlayersDialog



class PlayersSection(QWidget):
    goto_menu_requested = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.bottom_layout_widgets = []

        self.setup()

    def setup(self):
        main_layout = QVBoxLayout(self)

        top_area = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        bottom_area = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        self.players_table = PlayersTable(w=450, h=600)
        self.player_frame = PlayerFrame(self, w=750, h=600)
        #self.players_table = MockWidget(self, bgcolor="#BEE28E", width=450, height=600)
        #self.player_frame = MockWidget(self, bgcolor="#CF9D9D", width=750, height=600)
        self.create_add_player_button()
        self.create_goto_menu_button()

        top_area.addLayout(left_layout)
        top_area.addLayout(right_layout)
        bottom_area.addLayout(bottom_layout)

        main_layout.addLayout(top_area)
        main_layout.addLayout(bottom_area)

        left_layout.addWidget(self.players_table)
        right_layout.addWidget(self.player_frame)
        for widget in self.bottom_layout_widgets:
            bottom_layout.addWidget(widget)

        self.setFocus()

    def open_add_dialog(self):
        dialog = AddPlayersDialog(self)
        dialog.exec()

    def create_goto_menu_button(self):
        self.goto_menu_btn = QPushButton("Назад в меню")
        self.goto_menu_btn.setMinimumHeight(40)
        self.goto_menu_btn.setMaximumWidth(300)
        
        self.goto_menu_btn.clicked.connect(self.goto_menu_requested.emit)

        self.bottom_layout_widgets.append(self.goto_menu_btn)

    def create_add_player_button(self):
        self.add_player_btn = QPushButton("Добавить")
        self.add_player_btn.setMinimumHeight(40)
        self.add_player_btn.setMaximumWidth(300)
        
        self.add_player_btn.clicked.connect(self.open_add_dialog)

        self.bottom_layout_widgets.append(self.add_player_btn)
        