from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont



class PlayerFrame(QGroupBox):
    detail_button_clicked = Signal(str)

    def __init__(self, player_frame_data, chosen_member):
        super().__init__("Информация об игроке")
        self.setFixedWidth(500)
        self.setAlignment(Qt.AlignCenter)

        self.player_frame_data = player_frame_data
        self.chosen_member = chosen_member
        self.active_detail_button = None

        # Создаем основной вертикальный layout для рамки
        self.frame_layout = QVBoxLayout(self)
        self.frame_layout.setSpacing(5)

        self.create_header_section()
        self.create_activity_labels()
        self.create_lwk_section()
        self.create_cw_section()
        self.create_raid_section()

        self.frame_layout.addStretch()


    def create_header_section(self):
        # Верхняя строка с двумя надписями
        top_row_layout = QHBoxLayout()
        top_row_layout.setSpacing(15)

        self.label_tag = QLabel("Тег")
        self.label_tag.setFont(QFont("Arial", 10, QFont.Bold))

        self.label_nick = QLabel("Никнейм")
        self.label_nick.setFont(QFont("Arial", 10, QFont.Bold))

        top_row_layout.addWidget(self.label_tag)
        top_row_layout.addWidget(self.label_nick)
        top_row_layout.addStretch()

        # Добавляем верхнюю строку в основной layout
        self.frame_layout.addLayout(top_row_layout)

        # Добавляем строку с надписью "Уровень"
        self.level_label = QLabel("Уровень: Н/Д")
        self.level_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.frame_layout.addWidget(self.level_label)

        # Добавляем строку с надписью "Уровень ТХ"
        self.th_label = QLabel("Уровень ТХ: Н/Д")
        self.th_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.frame_layout.addWidget(self.th_label)

        # Добавляем небольшой отступ
        self.frame_layout.addSpacing(10)

        # Добавляем небольшой отступ
        self.frame_layout.addSpacing(10)

    def create_activity_labels(self):
        # Надпись "За последние 30 дней:"
        self.label_last_30_days = QLabel("За последние 30 дней:")
        self.label_last_30_days.setFont(QFont("Arial", 9))
        self.frame_layout.addWidget(self.label_last_30_days)

        # Создаем надписи в столбик
        self.activity_labels = []
        self.edit_mode = False  # Флаг режима редактирования
        self.edited_values = {}  # Словарь для хранения измененных значений

        cg_widget = QWidget()
        cg_layout = QHBoxLayout(cg_widget)
        cg_layout.setContentsMargins(0, 0, 0, 0)

        self.cg_label = QLabel("Очки игр кланов: Н/Д")
        self.cg_label.setFont(QFont("Arial", 8))
        cg_layout.addWidget(self.cg_label)
        
        self.cg_button = QPushButton("...")
        self.cg_button.setFixedSize(14, 14)
        self.cg_button.setStyleSheet("margin-top: 1px;")
        self.cg_button.setToolTip("Изменить")
        cg_layout.addWidget(self.cg_button)
        cg_layout.addStretch()
        self.frame_layout.addWidget(cg_widget)
        self.activity_labels.append(self.cg_label)

        self.cc_label = QLabel("Войска: Н/Д")
        self.cc_label.setFont(QFont("Arial", 8))
        self.frame_layout.addWidget(self.cc_label)
        self.activity_labels.append(self.cc_label)

        self.buildings_label = QLabel("Апгрейд деревень: Н/Д")
        self.buildings_label.setFont(QFont("Arial", 8))
        self.frame_layout.addWidget(self.buildings_label)
        self.activity_labels.append(self.buildings_label)

        self.days_offline_label = QLabel("Дней оффлайн: Н/Д")
        self.days_offline_label.setFont(QFont("Arial", 8))
        self.frame_layout.addWidget(self.days_offline_label)
        self.activity_labels.append(self.days_offline_label)

        self.capital_label = QLabel("Золота столицы пожертвовано: Н/Д")
        self.capital_label.setFont(QFont("Arial", 8))
        self.frame_layout.addWidget(self.capital_label)
        self.activity_labels.append(self.capital_label)

    def create_lwk_section(self):
        self.lwk_group = QGroupBox("ЛВК")
        lwk_layout = QHBoxLayout(self.lwk_group)
        lwk_layout.setSpacing(5)

        self.cwl_participation_label = QLabel("Участие: Н/Д")
        self.cwl_participation_label.setFont(QFont("Arial", 8))
        lwk_layout.addWidget(self.cwl_participation_label)

        self.cwl_attacks_label = QLabel("Атаки: Н/Д")
        self.cwl_attacks_label.setFont(QFont("Arial", 8))
        lwk_layout.addWidget(self.cwl_attacks_label)

        self.cwl_stars_label = QLabel("Звёзды: Н/Д")
        self.cwl_stars_label.setFont(QFont("Arial", 8))
        lwk_layout.addWidget(self.cwl_stars_label)

        self.lwk_detail_button = QPushButton("Подробнее")
        self.lwk_detail_button.setFixedWidth(100)
        lwk_layout.addWidget(self.lwk_detail_button)

        self.lwk_detail_button.clicked.connect(lambda: self.on_detail_button_clicked("cwl", self.lwk_detail_button))

        self.frame_layout.addWidget(self.lwk_group)

    def create_cw_section(self):
                # Добавляем раздел "КВ"
        self.cw_group = QGroupBox("КВ")
        cw_layout = QHBoxLayout(self.cw_group)
        cw_layout.setSpacing(5)

        self.cw_participation_label = QLabel("Участий: Н/Д")
        self.cw_participation_label.setFont(QFont("Arial", 8))
        cw_layout.addWidget(self.cw_participation_label)

        self.cw_no_attacks_label = QLabel("Без атак: Н/Д")
        self.cw_no_attacks_label.setFont(QFont("Arial", 8))
        cw_layout.addWidget(self.cw_no_attacks_label)

        self.cw_with_attacks_label = QLabel("С атаками: Н/Д")
        self.cw_with_attacks_label.setFont(QFont("Arial", 8))
        cw_layout.addWidget(self.cw_with_attacks_label)

        self.cw_detail_button = QPushButton("Подробнее")
        self.cw_detail_button.setFixedWidth(100)
        cw_layout.addWidget(self.cw_detail_button)

        self.cw_detail_button.clicked.connect(lambda: self.on_detail_button_clicked("cw", self.cw_detail_button))

        self.frame_layout.addWidget(self.cw_group)

    def create_raid_section(self):
        # Добавляем раздел "Рейды"
        self.raid_group = QGroupBox("Рейды")
        raid_layout = QHBoxLayout(self.raid_group)
        raid_layout.setSpacing(5)

        self.raid_participation_label = QLabel("Участий: Н/Д")
        self.raid_participation_label.setFont(QFont("Arial", 8))
        raid_layout.addWidget(self.raid_participation_label)

        self.raid_attacks_label = QLabel("Атаки: Н/Д")
        self.raid_attacks_label.setFont(QFont("Arial", 8))
        raid_layout.addWidget(self.raid_attacks_label)

        self.raid_available_attacks_label = QLabel("Доступные атаки: Н/Д")
        self.raid_available_attacks_label.setFont(QFont("Arial", 8))
        raid_layout.addWidget(self.raid_available_attacks_label)

        self.raid_detail_button = QPushButton("Подробнее")
        self.raid_detail_button.setFixedWidth(100)
        raid_layout.addWidget(self.raid_detail_button)

        self.raid_detail_button.clicked.connect(lambda: self.on_detail_button_clicked("raids", self.raid_detail_button))

        self.frame_layout.addWidget(self.raid_group)

    def on_detail_button_clicked(self, section_name, button):
        # Возвращаем предыдущей активной кнопке исходный текст
        if self.active_detail_button and self.active_detail_button != button:
            self.active_detail_button.setText("Подробнее")
            self.active_detail_button.setEnabled(True)
        
        # Меняем текст нажатой кнопки на стрелку
        button.setText("→")
        button.setEnabled(False)
        self.active_detail_button = button
        
        # Испускаем сигнал с названием секции
        self.detail_button_clicked.emit(section_name)

    def fill_with_data(self):
        player = self.find_player()
        
        # Заполняем заголовок
        self.label_tag.setText(f"Тег: {player.get('tag', 'Н/Д')}")
        self.label_nick.setText(f"Никнейм: {player.get('name', 'Н/Д')}")
        self.level_label.setText(f"Уровень: {player.get('level', 'Н/Д')}")
        self.th_label.setText(f"Уровень ТХ: {player.get('th_level', 'Н/Д')}")
        
        # Заполняем активность за 30 дней
        self.cg_label.setText(f"Очки игр кланов: {player.get('cg_points', 'Н/Д')}")
        self.cc_label.setText(f"Войска: {player.get('CCcontributions', 'Н/Д')}")
        self.buildings_label.setText(f"Апгрейд деревень: {player.get('buildings_upgraded', 'Н/Д')}")
        self.days_offline_label.setText(f"Дней оффлайн: {player.get('days_offline', 'Н/Д')}")
        self.capital_label.setText(f"Золота столицы пожертвовано: {player.get('capital_contibutions', 'Н/Д')}")
        
        # Заполняем ЛВК
        cwl_data = player.get('cwl', {})
        self.cwl_participation_label.setText(f"Участие: {'Да' if cwl_data.get('participation') else 'Нет'}")
        self.cwl_attacks_label.setText(f"Атаки: {cwl_data.get('attacks', 'Н/Д')}")
        self.cwl_stars_label.setText(f"Звёзды: {cwl_data.get('stars', 'Н/Д')}")
        
        # Заполняем КВ
        cw_data = player.get('cw', {})
        self.cw_participation_label.setText(f"Участий: {cw_data.get('participation', 'Н/Д')}")
        self.cw_no_attacks_label.setText(f"Без атак: {cw_data.get('no_attacks', 'Н/Д')}")
        self.cw_with_attacks_label.setText(f"С атаками: {cw_data.get('with_attacks', 'Н/Д')}")
        
        # Заполняем Рейды
        raid_data = player.get('raids', {})
        self.raid_participation_label.setText(f"Участий: {raid_data.get('participation', 'Н/Д')}")
        self.raid_attacks_label.setText(f"Атаки: {raid_data.get('attacks', 'Н/Д')}")
        self.raid_available_attacks_label.setText(f"Доступные атаки: {raid_data.get('available_attacks', 'Н/Д')}")
        
    def find_player(self):
        if not self.chosen_member:
            print(f"Не выбран игрок!")
            return
        if self.player_frame_data == []:
            print(f"Нет данных для карточки участника!")
            return
        
        player = None
        for data in self.player_frame_data:
            if data["tag"] == self.chosen_member:
                player = data
                break

        return player