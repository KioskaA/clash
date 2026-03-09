# Виджет- заглушка
# Используется для заполнения пространства, в котором будет еще не разработанный виджет


from PySide6.QtWidgets import (QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QFont, QKeyEvent

class MockWidget(QWidget):
    def __init__(self, parent, text="MOCK", bgcolor="#76ee5e", width=50, height=50):
        super().__init__(parent)
        self.text = text
        self.color = bgcolor
        self.width = width
        self.height = height
        self.setup()

    def setup(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(self.text)
        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.color};
                border: 2px solid #aaa;
                border-radius: 0px;
                padding: 3px;
                font-weight: bold;
                font-size: 12px;
                color: #666;
            }}
        """)

        layout.addWidget(label)

        self.setFixedSize(self.width, self.height)