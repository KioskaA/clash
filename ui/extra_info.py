from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QTableWidget, 
                               QTableWidgetItem, QWidget, QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class ExtraPanel(QGroupBox):
    def __init__(self):
        super().__init__("Подробная информация")
        self.setAlignment(Qt.AlignCenter)
        
        # Создаем основной layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        
        # Создаем контейнер для динамического содержимого
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignCenter)
        self.content_widget.setLayout(self.content_layout)
        
        # Добавляем контейнер в основной layout
        self.main_layout.addWidget(self.content_widget)
        
        # Устанавливаем layout для groupbox
        self.setLayout(self.main_layout)
        
        # По умолчанию показываем пустой виджет
        self.show_empty()
    
    def show_empty(self):
        """Очищает содержимое"""
        self.clear_content()
        label = QLabel("Выберите игрока")
        label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(label)
    
    def show_cwl_extra(self):
        """Показывает надпись 'запись 1'"""
        self.clear_content()
        label = QLabel("запись 1")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 14pt; padding: 20px;")
        self.content_layout.addWidget(label)
    
    def show_cw_extra(self):
        """Показывает таблицу с информацией о клановых войнах"""
        self.clear_content()

        table = QTableWidget()

        table.setColumnCount(4)
        table.setRowCount(0)  # Начнем с 0 строк, добавим позже

        headers = ["id", "Дата", "Атаки", "Звезды"]
        table.setHorizontalHeaderLabels(headers)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)      # id - фиксированная ширина
        header.setSectionResizeMode(1, QHeaderView.Stretch)    # Дата - растягивается
        header.setSectionResizeMode(2, QHeaderView.Fixed)      # Атаки - фиксированная
        header.setSectionResizeMode(3, QHeaderView.Fixed)      # Звезды - фиксированная

        table.setColumnWidth(0, 40)    # id
        table.setColumnWidth(2, 60)    # Атаки
        table.setColumnWidth(3, 60)    # Звезды

        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)

        table.verticalHeader().setVisible(False)

        self.content_layout.addWidget(table)
    
    def show_raids_extra(self):
        """Показывает таблицу 2x2 с текстом (а, б) (в, г)"""
        self.clear_content()
        
        # Создаем таблицу 2x2
        table = QTableWidget(2, 2)
        
        # Устанавливаем данные в ячейки
        table.setItem(0, 0, QTableWidgetItem("а"))
        table.setItem(0, 1, QTableWidgetItem("б"))
        table.setItem(1, 0, QTableWidgetItem("в"))
        table.setItem(1, 1, QTableWidgetItem("г"))
        
        # Настраиваем внешний вид таблицы
        table.setFixedSize(200, 100)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        
        # Растягиваем ячейки на весь размер
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setStretchLastSection(True)
        
        # Запрещаем редактирование
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Выравниваем текст по центру в ячейках
        for row in range(2):
            for col in range(2):
                item = table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
        
        self.content_layout.addWidget(table, alignment=Qt.AlignCenter)
    
    def clear_content(self):
        """Очищает динамическое содержимое"""
        # Удаляем все виджеты из content_layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()