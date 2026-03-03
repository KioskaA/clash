import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, 
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

if __name__ == "__main__":
    from player_frame import PlayerFrame
    from extra_info import ExtraPanel
else:
    from .player_frame import PlayerFrame
    from .extra_info import ExtraPanel

import random

class MainWindow(QMainWindow):
    member_selected = Signal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setFixedSize(1280, 720)

        self.memberslist = []
        self.chosen_member = None

        self.chosen_extra_info = None # * "cw" | "cwl" | "raids"
        self.cw_list = []
        self.cwl_list = []
        self.raids_list = []

        self.setup_ui()


    def create_widgets(self): # Создание виджетов, иерархия лаяутов
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
        #self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.left_panel = QVBoxLayout()
        self.left_panel.setContentsMargins(0, 0, 0, 0)
        self.left_panel.setSpacing(0)
        self.create_members_table()

        self.central_panel = QHBoxLayout()
        self.create_player_frame()

        self.right_panel = QHBoxLayout()
        self.create_extra_frame()

    def create_members_table(self):
        self.members_table = QTableWidget()
        with open('ui/style.css', 'r') as file:
            style = file.read()
        self.members_table.setStyleSheet(style)

        self.members_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.members_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.members_table.setRowCount(50)
        self.members_table.setColumnCount(4)

        self.members_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Запрет редактирования
        self.members_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Выделение всей строки
        self.members_table.setAlternatingRowColors(True)  # Чередование цветов строк
        self.members_table.setFixedWidth(460)

        self.members_table.itemSelectionChanged.connect(self.on_member_selected)

        headers = ["№", "Тег", "Ник", "Актив"]
        self.members_table.setHorizontalHeaderLabels(headers)        
        header = self.members_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)

        self.members_table.setColumnWidth(0, 25)
        self.members_table.setColumnWidth(1, 105)
        self.members_table.setColumnWidth(2, 200)
        self.members_table.setColumnWidth(3, 50)

        self.members_table.verticalHeader().setVisible(False)
        self.members_table.verticalHeader().setDefaultSectionSize(20)

    def populate_members_table(self, members=None, mbrs_activity=None):
        if members == None or mbrs_activity == None:
            return None

        tags = []
        nicks = []
        for member in members:
            tags.append(member['tag'])
            nicks.append(member['name'])
        
        activity_pts = []
        for member in mbrs_activity:
            activity_pts.append(member["activity_points"])
        
        for row in range(len(tags)):
            number = QTableWidgetItem(str(row+1))
            number.setTextAlignment(Qt.AlignCenter)
            self.members_table.setItem(row, 0, number)

            tag = QTableWidgetItem(tags[row])
            self.members_table.setItem(row, 1, tag)

            nick = QTableWidgetItem(nicks[row])
            self.members_table.setItem(row, 2, nick)

            activity = QTableWidgetItem(str(activity_pts[row]))
            self.members_table.setItem(row, 3, activity)
            activity.setTextAlignment(Qt.AlignCenter)

    def _populate_members_table_rnd(self):
        tags = ['user', 'admin', 'guest', 'moderator', 'vip', 'bot', 'tester', 'developer']
        nicks = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 
                'Ivy', 'Jack', 'Kevin', 'Lisa', 'Mona', 'Nick', 'Oliver']
        
        for row in range(50):
            item_num = QTableWidgetItem(str(row + 1))
            item_num.setTextAlignment(Qt.AlignCenter)
            self.members_table.setItem(row, 0, item_num)
            
            tag = random.choice(tags) + str(random.randint(1, 999))
            item_tag = QTableWidgetItem(tag)
            self.members_table.setItem(row, 1, item_tag)
            
            nick = random.choice(nicks) + str(random.randint(1, 99))
            item_nick = QTableWidgetItem(nick)
            self.members_table.setItem(row, 2, item_nick)
            
            activity = random.randint(0, 100)
            item_activity = QTableWidgetItem(str(activity))
            item_activity.setTextAlignment(Qt.AlignCenter)
            self.members_table.setItem(row, 3, item_activity)

    def on_member_selected(self):
        # Получаем выделенные строки
        selected_rows = self.members_table.selectedItems()

        if selected_rows:
            # Берем первую выделенную ячейку и получаем её строку
            first_item = selected_rows[0]
            selected_row = first_item.row()

            # Получаем тег из второго столбца (индекс 1)
            tag_item = self.members_table.item(selected_row, 1)
            # Получаем ник из третьего столбца (индекс 2)
            nick_item = self.members_table.item(selected_row, 2)
            # Получаем номер из первого столбца (индекс 0)
            if tag_item and nick_item:
                # Сохраняем словарь с тегом и ником
                self.chosen_member = {
                    "tag": str(tag_item.text()),
                    "nick": str(nick_item.text())
                }
                self.member_selected.emit(self.chosen_member["tag"])
                if __name__ == "__main__":
                    self._populate_player_frame_rnd()
                    self._populate_extra_frame_rnd()
                    return

        else:
            self.chosen_member = None
            self.chosen_extra_info = None
            self.extra_frame.show_empty()  # Очищаем ExtraPanel при снятии выделения
            print("Выделение снято")
    
    def create_player_frame(self):
        self.player_frame = PlayerFrame()

        self.player_frame.lwk_detail_clicked.connect(self.show_cwl_info)
        self.player_frame.cw_detail_clicked.connect(self.show_cw_info)
        self.player_frame.raid_detail_clicked.connect(self.show_raids_info)

    def show_cwl_info(self):
        """Показывает информацию о ЛВК в ExtraPanel"""
        if self.chosen_member:
            # Здесь можно передавать реальные данные о ЛВК
            self.extra_frame.show_cwl_extra()  # Показываем "запись 1" как пример
        else:
            self.extra_frame.show_empty()

    def show_cw_info(self):
        """Показывает информацию о КВ в ExtraPanel"""
        if self.chosen_member:
            # Здесь можно передавать реальные данные о клановых войнах
            self.extra_frame.show_cw_extra()  # Показываем кнопку "инфо" как пример
        else:
            self.extra_frame.show_empty()

    def show_raids_info(self):
        """Показывает информацию о Рейдах в ExtraPanel"""
        if self.chosen_member:
            # Здесь можно передавать реальные данные о рейдах
            self.extra_frame.show_raids_extra()  # Показываем таблицу как пример
        else:
            self.extra_frame.show_empty()

    def populate_player_frame(self, player_data):
        self.player_frame.label_tag.setText(f"{player_data["tag"]}")
        self.player_frame.label_nick.setText(f"{player_data["name"]}")

        self.player_frame.label_level_value.setText((f"{player_data["level"]}"))
        self.player_frame.label_th_value.setText((f"{player_data["th_level"]}"))

        self.player_frame.cg_value.setText(f"{player_data["cg_value"]}")
        self.player_frame.CCcontributions_value.setText(f"{player_data["CCcontributions_value"]}")
        self.player_frame.buildings_upgraded_value.setText(f"{player_data["buildings_upgraded_value"]}")
        self.player_frame.days_offline_value.setText(f"{player_data["days_offline_value"]}")
        self.player_frame.capital_contibutions_value.setText(f"{player_data["capital_contibutions_value"]}")
        
        self.player_frame.cwl_participation_value.setText(f"{player_data["cwl_participation_value"]}")
        self.player_frame.cwl_attacks_value.setText(f"{player_data["cwl_attacks_value"]}")
        self.player_frame.cwl_stars_value.setText(f"{player_data["cwl_stars_value"]}")
        
        self.player_frame.cw_participation_value.setText(f"{player_data["cw_participation_value"]}")
        self.player_frame.cw_no_attacks_value.setText(f"{player_data["cw_no_attacks_value"]}")
        self.player_frame.cw_with_attacks_value.setText(f"{player_data["cw_with_attacks_value"]}")
    
        self.player_frame.raid_participation_value.setText(f"{player_data["raid_participation_value"]}")
        self.player_frame.raid_attacks_value.setText(f"{player_data["raid_attacks_value"]}")
        self.player_frame.raid_available_attacks_value.setText(f"{player_data["raid_available_attacks_value"]}")
    
    def _populate_player_frame_rnd(self):
        player_data = {
            "tag": self.chosen_member["tag"],
            "nick": self.chosen_member["nick"],
            "level": random.randint(0, 200),
            "th_level": random.randint(7, 12),
            "cg_value": random.randint(0, 10000),
            "CCcontributions_value": f"{random.randint(0, 1500)}/{random.randint(0, 1500)}",
            "buildings_upgraded_value": random.randint(0, 30),
            "days_offline_value": random.randint(0, 5),
            "capital_contibutions_value": random.randint(0, 100000),
            "cwl_participation_value": "Да" if random.randint(0, 1)==1 else "Нет",
            "cwl_attacks_value": random.randint(4, 7),
            "cwl_stars_value": random.randint(8, 21),
            "cw_participation_value": random.randint(0, 10),
            "cw_no_attacks_value": random.randint(0, 1),
            "cw_with_attacks_value": random.randint(0, 10),
            "raid_participation_value": random.randint(0, 4),
            "raid_attacks_value": random.randint(0, 24),
            "raid_available_attacks_value": random.randint(0, 24),
        }
        # Изменяем надписи тег и никнейм
        self.player_frame.label_tag.setText(f"{player_data["tag"]}")  # меняем текст тега
        self.player_frame.label_nick.setText(f"{player_data["nick"]}")  # меняем текст никнейма

        self.player_frame.label_level_value.setText((f"{player_data["level"]}"))
        self.player_frame.label_th_value.setText((f"{player_data["th_level"]}"))

        # Надписи в разделе "За последние 30 дней"
        self.player_frame.cg_value.setText(f"{player_data["cg_value"]}")  # Очки игр кланов
        self.player_frame.CCcontributions_value.setText(f"{player_data["CCcontributions_value"]}")  # Пожертвовал войск
        self.player_frame.buildings_upgraded_value.setText(f"{player_data["buildings_upgraded_value"]}")  # Апгрейд деревень
        self.player_frame.days_offline_value.setText(f"{player_data["days_offline_value"]}")  # Дней оффлайн
        self.player_frame.capital_contibutions_value.setText(f"{player_data["capital_contibutions_value"]}")  # Золота столицы пожертвовано
        
        # Надписи в разделе "ЛВК"
        self.player_frame.cwl_participation_value.setText(f"{player_data["cwl_participation_value"]}")  # Участие
        self.player_frame.cwl_attacks_value.setText(f"{player_data["cwl_attacks_value"]}")  # Атаки
        self.player_frame.cwl_stars_value.setText(f"{player_data["cwl_stars_value"]}")  # Звёзды
        
        # Надписи в разделе "КВ"
        self.player_frame.cw_participation_value.setText(f"{player_data["cw_participation_value"]}")  # Участий
        self.player_frame.cw_no_attacks_value.setText(f"{player_data["cw_no_attacks_value"]}")  # Без атак
        self.player_frame.cw_with_attacks_value.setText(f"{player_data["cw_with_attacks_value"]}")  # С атаками
        
        # Надписи в разделе "Рейды"
        self.player_frame.raid_participation_value.setText(f"{player_data["raid_participation_value"]}")  # Участий
        self.player_frame.raid_attacks_value.setText(f"{player_data["raid_attacks_value"]}")  # Атаки
        self.player_frame.raid_available_attacks_value.setText(f"{player_data["raid_available_attacks_value"]}")  # Доступные атаки

    def create_extra_frame(self):
        self.extra_frame = ExtraPanel()

    def _populate_extra_frame_rnd(self):
        """Заполняет ExtraPanel случайными данными для демонстрации"""
        if not self.chosen_member:
            self.extra_frame.show_empty()
            return

        # Случайно выбираем, что показать (для демонстрации)
        choice = random.randint(1, 3)
        if choice == 1:
            self.extra_frame.show_cwl_extra()
        elif choice == 2:
            self.extra_frame.show_cw_extra()
        else:
            self.extra_frame.show_raids_extra()

    def populate_extra_frame(self, player_data):
        pass

    def setup_ui(self): # .addWidget .addLayout
        self.create_widgets()

        self.main_layout.addLayout(self.left_panel)
        self.main_layout.addLayout(self.central_panel)
        self.main_layout.addLayout(self.right_panel)

        self.left_panel.addWidget(self.members_table)

        self.central_panel.addWidget(self.player_frame)

        self.right_panel.addWidget(self.extra_frame)

        self.extra_frame.show_empty()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()

    window._populate_members_table_rnd()
    
    sys.exit(app.exec())