# Таблица игроков
# Содержимое будет описано позже
#
#


from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont



class PlayersTable(QTableWidget):
        
    def __init__(self, w=100, h=100):
        super().__init__()
        self.width = w
        self.height = h
        self.setup()

    def setup(self):
        self.style()
        self.properties()
        self.cells()
        self.headers()
        self.setFixedSize(self.width, self.height)

    def style(self):
        self.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: #a1a1a1;
                color: black;
                padding: 0px;
                border: 1px solid #000000;
                font-weight: bold;
        }}
        """)
    
    def properties(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрет редактирования
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделение всей строки
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        #self.setAlternatingRowColors(True)  # Чередование цветов строк
        self.setFixedWidth(460)

    def cells(self):
        self.setRowCount(0)
        self.setColumnCount(4)
        self.setColumnWidth(0, 25)
        self.setColumnWidth(1, 105)
        self.setColumnWidth(2, 50)
        self.setColumnWidth(3, 90)

    def headers(self):
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(20)

        headers = ["№", "Тег", "Ник", "Добавлен"]
        self.setHorizontalHeaderLabels(headers)        
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
