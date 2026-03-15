# Виджет для добавления нового игрока/игроков
#
# Поле "Тег/теги через пробел"
# Кнопка "Добавить"
#
# Надписи в формате f"Игрок с тегом {тег} добавлен" или f"Игрок с тегом {тег} не найден"
#

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt

class AddPlayersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить игроков")
        self.setModal(True)                # модальный режим
        self.resize(400, 200)

        # Основной вертикальный layout
        layout = QVBoxLayout(self)

        # Поле ввода тегов
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите теги игроков через пробел")
        layout.addWidget(self.input_field)

        # Кнопка "Добавить" (пока без логики)
        self.add_button = QPushButton("Добавить")
        layout.addWidget(self.add_button)

        # Кнопка "Назад" – закрывает диалог
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.reject)  # reject закрывает диалог с кодом Rejected
        layout.addWidget(self.back_button)

        # Можно добавить метку для сообщений (опционально)
        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        self.message_label.hide()  # пока скрыта