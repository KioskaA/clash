from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QTableWidget, QFrame,
                               QTableWidgetItem, QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QBrush



class ExtraPanel(QWidget):
    def __init__(self, extra_panel_data):
        super().__init__()
        
        self.chosen_member = None
        self.extra_panel_data = extra_panel_data
        # Создаем основной layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        
        # Добавляем заголовок (так как это больше не QGroupBox)
        self.title_label = QLabel("Подробная информация")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(10)
        self.title_label.setFont(title_font)
        self.main_layout.addWidget(self.title_label)
        
        # Добавляем разделительную линию (опционально)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)
        
        # Создаем контейнер для динамического содержимого
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignCenter)
        self.content_widget.setLayout(self.content_layout)
        
        # Добавляем контейнер в основной layout
        self.main_layout.addWidget(self.content_widget)
        
        # Добавляем растяжение внизу
        self.main_layout.addStretch()
        
        # Устанавливаем layout для виджета
        self.setLayout(self.main_layout)
        
        # По умолчанию показываем пустой виджет
        self.show_empty()

    def show_empty(self):
        self.clear_content()
    
    def show_cwl_extra(self):
        if self.chosen_member == None:
            return
        self.clear_content()
        player = self.find_player()
        if player == None:
            return
        if player["cwl"] == {}:
            label = QLabel("В ЛВК не участвовал")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 12))
            self.content_layout.addWidget(label)
            return
        
        title_text = f'ЛВК №__, _______'
        title_label = QLabel(title_text)
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(11)
        title_label.setFont(title_font)
        self.cwl_header_label = title_label
        self.content_layout.addWidget(self.cwl_header_label)
        
        # Таблица с днями
        self.cwl_table = QTableWidget()
        self.cwl_table.setColumnCount(2)
        self.cwl_table.setRowCount(0)
        
        headers = ["День", "Информация"]
        self.cwl_table.setHorizontalHeaderLabels(headers)
        
        header = self.cwl_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)      # День - фиксированная ширина
        header.setSectionResizeMode(1, QHeaderView.Stretch)    # Информация - растягивается
        
        self.cwl_table.setColumnWidth(0, 60)    # День
        
        self.cwl_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cwl_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.cwl_table.verticalHeader().setVisible(False)
        
        self.content_layout.addWidget(self.cwl_table)

        self.fill_cwl()
    
    def show_cw_extra(self):
        if self.chosen_member == None:
            return
        
        self.clear_content()

        self.cw_table = QTableWidget()

        self.cw_table.setColumnCount(4)
        self.cw_table.setRowCount(0)

        headers = ["id", "Дата", "Атаки", "Звезды"]
        self.cw_table.setHorizontalHeaderLabels(headers)

        header = self.cw_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)      # id - фиксированная ширина
        header.setSectionResizeMode(1, QHeaderView.Stretch)    # Дата - растягивается
        header.setSectionResizeMode(2, QHeaderView.Fixed)      # Атаки - фиксированная
        header.setSectionResizeMode(3, QHeaderView.Fixed)      # Звезды - фиксированная

        self.cw_table.setColumnWidth(0, 40)    # id
        self.cw_table.setColumnWidth(2, 60)    # Атаки
        self.cw_table.setColumnWidth(3, 60)    # Звезды

        self.cw_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cw_table.setSelectionMode(QAbstractItemView.NoSelection)

        self.cw_table.verticalHeader().setVisible(False)

        self.content_layout.addWidget(self.cw_table)

        self.fill_cw()
    
    def show_raids_extra(self):
        if self.chosen_member == None:
            return
        self.clear_content()

        self.raids_table = QTableWidget()

        self.raids_table.setColumnCount(4)
        self.raids_table.setRowCount(0)

        headers = ["id", "Дата", "Атаки", "Золото"]
        self.raids_table.setHorizontalHeaderLabels(headers)

        header = self.raids_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)      # id - фиксированная ширина
        header.setSectionResizeMode(1, QHeaderView.Stretch)    # Дата - растягивается
        header.setSectionResizeMode(2, QHeaderView.Fixed)      # Атаки - фиксированная
        header.setSectionResizeMode(3, QHeaderView.Fixed)      # Звезды - фиксированная

        self.raids_table.setColumnWidth(0, 40)    # id
        self.raids_table.setColumnWidth(2, 60)    # Атаки
        self.raids_table.setColumnWidth(3, 60)    # Звезды

        self.raids_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.raids_table.setSelectionMode(QAbstractItemView.NoSelection)

        self.raids_table.verticalHeader().setVisible(False)

        self.content_layout.addWidget(self.raids_table)

        self.fill_raids()

    def fill_cwl(self):
        if self.extra_panel_data == []:
            print(f"Нет данных!")
            return
        player = self.find_player()
        if player == None:
            return
        
        cwl_data = player.get("cwl", {})
        if not cwl_data:
            return
        
        title_text = f'ЛВК №{cwl_data.get("id", "?")}, {cwl_data.get("date", "Неизвестно")}'
        self.cwl_header_label.setText(title_text)
        
        days = cwl_data.get("days", [])
        self.cwl_table.setRowCount(len(days))

        for row, day in enumerate(days):
            day_number = day.get("day", row + 1)
            day_item = QTableWidgetItem(f"{day_number}")
            day_item.setTextAlignment(Qt.AlignCenter)

            attack = day.get("attack", False)
            replaced = day.get("replaced", False)

            if attack:
                stars = day.get("stars", 0)
                percentage = day.get("percentage", 0)
                info_text = f"Атаковал на {stars} звезды, {percentage}%"
            elif replaced:
                info_text = "Заменён"
            else:
                info_text = "Не атаковал"

            info_item = QTableWidgetItem(info_text)
            info_item.setTextAlignment(Qt.AlignCenter)

            background_color = None
            if attack and stars == 3:
                background_color = QColor(144, 238, 144)  # Светло-зеленый
            elif replaced:
                background_color = QColor(211, 211, 211)  # Светло-серый
            elif not attack and not replaced:
                background_color = QColor(255, 182, 193)  # Светло-красный

            if background_color:
                day_item.setBackground(background_color)
                info_item.setBackground(background_color)

            self.cwl_table.setItem(row, 0, day_item)
            self.cwl_table.setItem(row, 1, info_item)

    def fill_cw(self):
        if self.extra_panel_data == []:
            print(f"Нет данных!")
            return
        player = self.find_player()
        if player == None:
            return

        cw_data = player["cw"]
        self.cw_table.setRowCount(len(cw_data))

        for row, cw in enumerate(cw_data):
            background_color = None
            if not cw.get("participation", True):  # Если False - серый цвет
                background_color = QColor(211, 211, 211)  # Серый
                attacks_value = "-"
                stars_value = "-"
            else:
                result = cw.get("result", "")
                if result == "win":
                    background_color = QColor(144, 238, 144)  # Светло-зеленый
                elif result == "lose":
                    background_color = QColor(255, 182, 193)  # Светло-красный
                elif result == "tie":
                    background_color = QColor(255, 255, 224)  # Светло-желтый
                
                attacks_value = str(cw.get("attacks", "Н/Д"))
                stars_value = str(cw.get("stars", "Н/Д"))

            id_item = QTableWidgetItem(str(cw["id"]))
            id_item.setTextAlignment(Qt.AlignCenter)

            date_item = QTableWidgetItem(cw["date"])
            date_item.setTextAlignment(Qt.AlignCenter)

            attacks_item = QTableWidgetItem(attacks_value)
            attacks_item.setTextAlignment(Qt.AlignCenter)

            stars_item = QTableWidgetItem(stars_value)
            stars_item.setTextAlignment(Qt.AlignCenter)

            if background_color:
                brush = QBrush(background_color)
                id_item.setBackground(brush)
                date_item.setBackground(brush)
                attacks_item.setBackground(brush)
                stars_item.setBackground(brush)

            self.cw_table.setItem(row, 0, id_item)
            self.cw_table.setItem(row, 1, date_item)
            self.cw_table.setItem(row, 2, attacks_item)
            self.cw_table.setItem(row, 3, stars_item)

    def fill_raids(self):
        if self.extra_panel_data == []:
            print(f"Нет данных!")
            return
        player = self.find_player()
        if player == None:
            return

        raids_data = player["raids"]
        self.raids_table.setRowCount(len(raids_data))

        for row, raid in enumerate(raids_data):

            id_item = QTableWidgetItem(str(raid["id"]))
            id_item.setTextAlignment(Qt.AlignCenter)

            date_item = QTableWidgetItem(raid["date"])
            date_item.setTextAlignment(Qt.AlignCenter)

            attacks_item = QTableWidgetItem(str(f'{raid["attacks"]}/{raid["available_attacks"]}'))
            attacks_item.setTextAlignment(Qt.AlignCenter)

            gold_item = QTableWidgetItem(str(raid["gold_earned"]))
            gold_item.setTextAlignment(Qt.AlignCenter)

            self.raids_table.setItem(row, 0, id_item)
            self.raids_table.setItem(row, 1, date_item)
            self.raids_table.setItem(row, 2, attacks_item)
            self.raids_table.setItem(row, 3, gold_item)

            attacks = raid["attacks"]

            if attacks == 0:
                color = QColor(255, 200, 200)  # Красный
            elif attacks < 5:
                color = QColor(255, 255, 200)  # Желтый
            else:
                color = QColor(200, 255, 200)  # Зеленый

            for column in range(4):
                item = self.raids_table.item(row, column)
                if item:
                    item.setBackground(color)

    def find_player(self):
        if not self.chosen_member:
            print(f"Не выбран игрок!")
            return None
        
        player = None
        for data in self.extra_panel_data:
            if data["tag"] == self.chosen_member:
                player = data
                break

        return player

    def clear_content(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()