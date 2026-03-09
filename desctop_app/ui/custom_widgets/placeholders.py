from PySide6.QtWidgets import (QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QFont, QKeyEvent

class EmptyPlaceholder(QWidget):
    def __init__(self, parent, type: str = "select_player"):
        super().__init__(parent)
        self.type = type
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.main_label = QLabel()
        self.main_label.setAlignment(Qt.AlignCenter)
        self.main_label.setFont(QFont("Arial", 14, QFont.Bold))

        self.desc_label = QLabel()
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setFont(QFont("Arial", 10))
        self.desc_label.setWordWrap(True)

        # Устанавливаем текст в зависимости от type
        if self.type == "select_player":
            self.main_label.setText("Выберите игрока")
        else:
            self.main_label.setText("Нет данных")  # Заглушка для других типов

        layout.addWidget(self.main_label)
        layout.addWidget(self.desc_label)

    def setDescription(self, text: str):
        self.desc_label.setText(text)