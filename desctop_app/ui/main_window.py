# Собирает интерфейс воедино, описывает логику взаимодействия элементов интерфейса.
# Вызывается в main.py
#
from PySide6.QtWidgets import (QMainWindow, QWidget, QStackedWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

from .sections import AuthSection, MenuSection, PlayersSection, RegistrationSection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setFixedSize(1280, 720)

        self.setup()

        #self.show_auth()
        #self.show_registration()
        #self.show_menu()
        self.show_players()

        self.setFocus()

    def setup(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stacked = QStackedWidget()
        layout.addWidget(self.stacked)

        self.auth_section = AuthSection(self.stacked)
        self.registration_section = RegistrationSection(self.stacked)
        self.menu_section = MenuSection(self.stacked)
        self.players_section = PlayersSection(self.stacked)

        self.connect_signals()
        
        self.stacked.addWidget(self.auth_section)
        self.stacked.addWidget(self.registration_section)
        self.stacked.addWidget(self.menu_section)
        self.stacked.addWidget(self.players_section)

    def connect_signals(self):
        self.auth_section.register_requested.connect(self.show_registration)
        self.registration_section.back_to_login_requested.connect(self.show_auth)

        self.menu_section.closeapp_requested.connect(self.closeapp)
        self.menu_section.goto_players_requested.connect(self.show_players)

        self.players_section.goto_menu_requested.connect(self.show_menu)

    def show_auth(self):
        self.stacked.setCurrentWidget(self.auth_section)

    def show_registration(self):
        self.stacked.setCurrentWidget(self.registration_section)

    def show_menu(self):
        self.stacked.setCurrentWidget(self.menu_section)

    def show_players(self):
        self.stacked.setCurrentWidget(self.players_section)

    def closeapp(self):
        self.close()