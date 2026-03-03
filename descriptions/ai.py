import sys
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Таблица с данными")
        self.setFixedSize(1280, 720)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной горизонтальный макет
        main_layout = QHBoxLayout(central_widget)
        
        # Создаем таблицу
        self.table = QTableWidget()
        
        # Устанавливаем количество строк и столбцов
        self.table.setRowCount(50)  # 50 строк
        self.table.setColumnCount(4)  # 4 столбца
        
        # Устанавливаем названия столбцов
        headers = ["№", "Тег", "Ник", "Активность"]
        self.table.setHorizontalHeaderLabels(headers)
        
        # Настройка поведения таблицы
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрет редактирования
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделение всей строки
        self.table.setAlternatingRowColors(True)  # Чередование цветов строк
        
        # Настройка растяжения столбцов
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # № по содержимому
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # Тег растягивается
        header.setSectionResizeMode(2, QHeaderView.Stretch)          # Ник растягивается
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # Активность по содержимому
        
        # Заполняем таблицу данными
        self.populate_table()
        
        # Создаем пустую правую область
        right_panel = QWidget()
        right_panel.setMinimumWidth(400)  # Минимальная ширина правой панели
        right_panel.setStyleSheet("background-color: #f0f0f0; border-left: 2px solid #ccc;")
        
        # Добавляем подсказку в правую панель (опционально)
        right_layout = QVBoxLayout(right_panel)
        right_layout.addStretch()
        
        # Добавляем виджеты в макет
        main_layout.addWidget(self.table, 1)  # Таблица занимает 2/3 пространства
        main_layout.addWidget(right_panel, 1)  # Правая панель занимает 1/3 пространства
        
        # Устанавливаем соотношение размеров
        main_layout.setStretch(0, 2)  # Таблица
        main_layout.setStretch(1, 1)  # Правая панель
    
    def populate_table(self):
        """Заполнение таблицы тестовыми данными"""
        # Списки для генерации случайных данных
        tags = ['user', 'admin', 'guest', 'moderator', 'vip', 'bot', 'tester', 'developer']
        nicks = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 
                'Ivy', 'Jack', 'Kevin', 'Lisa', 'Mona', 'Nick', 'Oliver']
        
        for row in range(50):
            # № (номер строки)
            item_num = QTableWidgetItem(str(row + 1))
            item_num.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item_num)
            
            # Тег (случайный тег)
            tag = random.choice(tags) + str(random.randint(1, 999))
            item_tag = QTableWidgetItem(tag)
            self.table.setItem(row, 1, item_tag)
            
            # Ник (случайный ник)
            nick = random.choice(nicks) + str(random.randint(1, 99))
            item_nick = QTableWidgetItem(nick)
            self.table.setItem(row, 2, item_nick)
            
            # Активность (число от 0 до 100)
            activity = random.randint(0, 100)
            item_activity = QTableWidgetItem(str(activity))
            item_activity.setTextAlignment(Qt.AlignCenter)
            
            # Добавляем цвет в зависимости от активности
            if activity < 30:
                item_activity.setBackground(QColor(255, 200, 200))  # Светло-красный
            elif activity < 70:
                item_activity.setBackground(QColor(255, 255, 200))  # Светло-желтый
            else:
                item_activity.setBackground(QColor(200, 255, 200))  # Светло-зеленый
            
            self.table.setItem(row, 3, item_activity)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль для более современного вида
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())