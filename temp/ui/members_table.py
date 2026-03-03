from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont




class MembersTable(QTableWidget):
    member_selected = Signal(str)

    def __init__(self, members_table_data = None):
        super().__init__()
        self.members_table_data = members_table_data
        self.setup()
        self.fill_with_data()

        self.itemSelectionChanged.connect(self.on_member_selected)

    def setup(self):
        self.style()
        self.props()
        self.cells()
        self.headers()

    def style(self):
        with open('ui/style.css', 'r') as file:
            style = file.read()
        self.setStyleSheet(style)

    def cells(self):
        self.setRowCount(50)
        self.setColumnCount(4)
        self.setColumnWidth(0, 25)
        self.setColumnWidth(1, 105)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 50)

    def props(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрет редактирования
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделение всей строки
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)  # Чередование цветов строк
        self.setFixedWidth(460)

    def headers(self):
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(20)

        headers = ["№", "Тег", "Ник", "Актив"]
        self.setHorizontalHeaderLabels(headers)        
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)

    def fill_with_data(self):
        if self.members_table_data == []:
            print(f"Нет данных для таблицы участников!")
            return
        
        tags = []
        nicks = []
        activity_pts = []
        for member in self.members_table_data:
            tags.append(member['tag'])
            nicks.append(member['name'])
            activity_pts.append(member["activity_points"])
        
        for row in range(len(tags)):
            number = QTableWidgetItem(str(row+1))
            number.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 0, number)

            tag = QTableWidgetItem(tags[row])
            self.setItem(row, 1, tag)

            nick = QTableWidgetItem(nicks[row])
            self.setItem(row, 2, nick)

            activity = QTableWidgetItem(str(activity_pts[row]))
            self.setItem(row, 3, activity)
            activity.setTextAlignment(Qt.AlignCenter)

    def on_member_selected(self):
        selected_rows = self.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()

            tag = self.item(row, 1).text()
            
            self.member_selected.emit(tag)