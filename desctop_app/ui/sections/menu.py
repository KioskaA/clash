# Показывается после авторизации
#
# Кнопки: "Список игроков", "Выход из аккаунта", "Выход из приложения"
# 
#
#
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QFont, QKeyEvent


class MenuSection(QWidget):
    goto_players_requested = Signal()
    change_acc_requested = Signal()
    closeapp_requested = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.widgets = []

        self.setup()

    def setup(self):
        main_layout = QVBoxLayout(self)
        main_layout.addStretch()

        center_layout = QHBoxLayout()
        center_layout.addStretch()

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)

        self.create_goto_players_button()
        self.create_change_acc_button()
        self.create_closeapp_button()

        for widget in self.widgets:
            content_layout.addWidget(widget)

        center_layout.addLayout(content_layout)
        center_layout.addStretch()

        main_layout.addLayout(center_layout)
        main_layout.addStretch()

        self.setFocus()

    def create_goto_players_button(self):
        self.goto_players_btn = QPushButton("Список игроков")
        self.goto_players_btn.setMinimumHeight(40)
        self.goto_players_btn.setMaximumWidth(300)
        
        self.goto_players_btn.clicked.connect(self.goto_players_requested.emit)

        self.widgets.append(self.goto_players_btn)

    def create_change_acc_button(self):
        self.change_acc_btn = QPushButton("Выход из аккаунта")
        self.change_acc_btn.setMinimumHeight(40)
        self.change_acc_btn.setMaximumWidth(300)
        
        self.change_acc_btn.clicked.connect(self.change_acc_requested.emit)

        self.widgets.append(self.change_acc_btn)

    def create_closeapp_button(self):
        self.closeapp_btn = QPushButton("Выход из приложения")
        self.closeapp_btn.setMinimumHeight(40)
        self.closeapp_btn.setMaximumWidth(300)
        
        self.closeapp_btn.clicked.connect(self.closeapp_requested.emit)

        self.widgets.append(self.closeapp_btn)