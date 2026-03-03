from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QWidget
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class PlayerFrame(QGroupBox):
    lwk_detail_clicked = Signal()
    cw_detail_clicked = Signal()
    raid_detail_clicked = Signal()
    data_saved = Signal(dict)
    def __init__(self):
        super().__init__("Информация об игроке")
        self.setFixedWidth(500)
        self.setAlignment(Qt.AlignCenter)

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
        level_layout = QHBoxLayout()

        self.label_level = QLabel("Уровень: ")
        self.label_level.setFont(QFont("Arial", 10, QFont.Bold))

        self.label_level_value = QLabel("Н\Д")
        self.label_level_value.setFont(QFont("Arial", 10, QFont.Bold))

        level_layout.addWidget(self.label_level)
        level_layout.addWidget(self.label_level_value)
        level_layout.addStretch()

        # Добавляем строку с надписью "Уровень ТХ" и значением "Н/Д"
        th_layout = QHBoxLayout()

        self.label_th = QLabel("Уровень ТХ:")
        self.label_th.setFont(QFont("Arial", 10, QFont.Bold))

        self.label_th_value = QLabel("Н/Д")
        self.label_th_value.setFont(QFont("Arial", 10, QFont.Bold))

        th_layout.addWidget(self.label_th)
        th_layout.addWidget(self.label_th_value)
        th_layout.addStretch()

        # Добавляем строку с уровнем в основной layout
        self.frame_layout.addLayout(level_layout)
        self.frame_layout.addLayout(th_layout)

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

        self.activity_labels_text = [
            ("Очки игр кланов: ", "Н/Д"), # 0
            ("Войска: ", "Н/Д"), # 1
            ("Получил войск: ", "Н/Д"), # 2
            ("Апгрейд деревень: ", "Н/Д"), # 3
            ("Дней оффлайн: ", "Н/Д"), # 4
            ("Золота столицы пожертвовано: ", "Н/Д"), # 5
        ]

        labels_data = [
            (0, "cg"),
            (1, "CCcontributions"),
            (3, "buildings_upgraded"),
            (4, "days_offline"),
            (5, "capital_contibutions")
        ]

        for index, attr_name in labels_data:
            # Создаем горизонтальный layout для пары
            row_layout = QHBoxLayout()

            # Создаем метку с текстом
            text_label = QLabel(f"{self.activity_labels_text[index][0]}")
            text_label.setFont(QFont("Arial", 8))

            # Создаем метку со значением "Н/Д"
            value_label = QLabel(f"{self.activity_labels_text[index][1]}")
            value_label.setFont(QFont("Arial", 8))
            value_label.setAlignment(Qt.AlignRight)

            # Добавляем метки в ряд
            row_layout.addWidget(text_label)
            row_layout.addWidget(value_label)
            row_layout.addStretch()

            # Сохраняем ссылки на метки
            setattr(self, attr_name, text_label)
            setattr(self, f"{attr_name}_value", value_label)
            self.activity_labels.append(text_label)
            self.activity_labels.append(value_label)

            # Добавляем ряд в основной layout
            self.frame_layout.addLayout(row_layout)

    def create_lwk_section(self):
        self.lwk_group = QGroupBox("ЛВК")
        lwk_layout = QHBoxLayout(self.lwk_group)
        lwk_layout.setSpacing(5)

        self.cwl_activity_labels_text = [
            ("Участие: ", "Н/Д"),
            ("Атаки: ", "Н/Д"),
            ("Звёзды: ", "Н/Д"),
        ]

        self.cwl_activity_labels = []

        labels_data = [
            (0, "cwl_participation"),
            (1, "cwl_attacks"),
            (2, "cwl_stars")
        ]

        for index, attr_name in labels_data:
            # Создаем горизонтальный layout для пары внутри группы ЛВК
            pair_layout = QHBoxLayout()
            pair_layout.setSpacing(0)

            text_label = QLabel(f"{self.cwl_activity_labels_text[index][0]}")
            text_label.setFont(QFont("Arial", 8))

            value_label = QLabel(f"{self.cwl_activity_labels_text[index][1]}")
            value_label.setFont(QFont("Arial", 8))

            pair_layout.addWidget(text_label)
            pair_layout.addWidget(value_label)
            pair_layout.addStretch()

            setattr(self, attr_name, text_label)
            setattr(self, f"{attr_name}_value", value_label)
            self.cwl_activity_labels.append(text_label)
            self.cwl_activity_labels.append(value_label)

            lwk_layout.addLayout(pair_layout)

        self.lwk_detail_button = QPushButton("Подробнее")
        self.lwk_detail_button.setFixedWidth(100)
        self.lwk_detail_button.clicked.connect(self.lwk_detail_clicked.emit)
        lwk_layout.addWidget(self.lwk_detail_button)

        self.frame_layout.addWidget(self.lwk_group)

    def create_cw_section(self):
        # Добавляем раздел "КВ"
        self.cw_group = QGroupBox("КВ")
        cw_layout = QHBoxLayout(self.cw_group)
        cw_layout.setSpacing(5)

        self.cw_activity_labels_text = [
            ("Участий: ", "Н/Д"),
            ("Без атак: ", "Н/Д"),
            ("С атаками: ", "Н/Д"),
        ]

        self.cw_activity_labels = []

        labels_data = [
            (0, "cw_participation"),
            (1, "cw_no_attacks"),
            (2, "cw_with_attacks")
        ]

        for index, attr_name in labels_data:
            pair_layout = QHBoxLayout()
            pair_layout.setSpacing(0)

            text_label = QLabel(f"{self.cw_activity_labels_text[index][0]}")
            text_label.setFont(QFont("Arial", 8))

            value_label = QLabel(f"{self.cw_activity_labels_text[index][1]}")
            value_label.setFont(QFont("Arial", 8))

            pair_layout.addWidget(text_label)
            pair_layout.addWidget(value_label)
            pair_layout.addStretch()

            setattr(self, attr_name, text_label)
            setattr(self, f"{attr_name}_value", value_label)
            self.cw_activity_labels.append(text_label)
            self.cw_activity_labels.append(value_label)

            cw_layout.addLayout(pair_layout)

        # Кнопка "Подробнее" для КВ
        self.cw_detail_button = QPushButton("Подробнее")
        self.cw_detail_button.setFixedWidth(100)
        self.cw_detail_button.clicked.connect(self.cw_detail_clicked.emit)
        cw_layout.addWidget(self.cw_detail_button)

        self.frame_layout.addWidget(self.cw_group)

    def create_raid_section(self):
        # Добавляем раздел "Рейды"
        self.raid_group = QGroupBox("Рейды")
        raid_layout = QHBoxLayout(self.raid_group)
        raid_layout.setSpacing(5)

        self.raid_activity_labels_text = [
            ("Участий: ", "Н/Д"),
            ("Атаки: ", "Н/Д"),
            ("Доступные атаки: ", "Н/Д"),
        ]

        self.raid_activity_labels = []

        labels_data = [
            (0, "raid_participation"),
            (1, "raid_attacks"),
            (2, "raid_available_attacks")
        ]

        for index, attr_name in labels_data:
            pair_layout = QHBoxLayout()
            pair_layout.setSpacing(0)

            text_label = QLabel(f"{self.raid_activity_labels_text[index][0]}")
            text_label.setFont(QFont("Arial", 8))

            value_label = QLabel(f"{self.raid_activity_labels_text[index][1]}")
            value_label.setFont(QFont("Arial", 8))

            pair_layout.addWidget(text_label)
            pair_layout.addWidget(value_label)
            pair_layout.addStretch()

            setattr(self, attr_name, text_label)
            setattr(self, f"{attr_name}_value", value_label)
            self.raid_activity_labels.append(text_label)
            self.raid_activity_labels.append(value_label)

            raid_layout.addLayout(pair_layout)

        # Кнопка "Подробнее" для Рейдов
        self.raid_detail_button = QPushButton("Подробнее")
        self.raid_detail_button.setFixedWidth(100)
        self.raid_detail_button.clicked.connect(self.raid_detail_clicked.emit)
        raid_layout.addWidget(self.raid_detail_button)

        self.frame_layout.addWidget(self.raid_group)

    def print_attrs(self):
        print("=== Все атрибуты PlayerFrame ===")
        print(vars(self))
        print("\n=== Только пользовательские атрибуты ===")
        for attr, value in self.__dict__.items():
            if not attr.startswith('_'):
                print(f"{attr}: {type(value).__name__}")