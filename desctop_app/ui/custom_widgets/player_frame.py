# Фрейм игрока
# Содержимое будет описано позже
#


from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QStackedWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from .placeholders import EmptyPlaceholder
from .mock_widget import MockWidget



class PlayerFrame(QWidget):
    def __init__(self, parent, w=50, h=50):
        super().__init__(parent)
        self.width = w
        self.height = h
        self.setup()

    def setup(self):
        main_layout = QVBoxLayout(self)

        self.stacked = QStackedWidget()
        main_layout.addWidget(self.stacked)

        self.player_not_selected_placeholder = EmptyPlaceholder(self.stacked, type="select_player")
        self.player_not_selected_placeholder.setDescription("Нажмите на игрока в таблице, чтобы увидеть детали")

        self.create_info_panel(self.stacked)

        self.stacked.addWidget(self.player_not_selected_placeholder)
        self.stacked.setCurrentWidget(self.player_not_selected_placeholder)
        self.setFixedSize(self.width, self.height)
    
    def create_info_panel(self, stacked):
        self.info_panel = MockWidget(self.stacked, bgcolor="#B15757")
        stacked.addWidget(self.info_panel)