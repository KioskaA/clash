from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QFont, QKeyEvent



class StartupPanel(QWidget):
    clan_tag_entered = Signal(str)
    def __init__(self, parent):
        super().__init__(parent)
        self.setup()

    def setup(self):
        main_layout = QVBoxLayout(self)
        main_layout.addStretch()

        center_layout = QHBoxLayout()
        center_layout.addStretch()

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)

        self.cr_label()
        self.cr_input_area()
        self.cr_button()

        content_layout.addWidget(self.label)
        content_layout.addWidget(self.clan_tag_input)
        content_layout.addWidget(self.input_btn)

        center_layout.addLayout(content_layout)
        center_layout.addStretch()

        main_layout.addLayout(center_layout)
        main_layout.addStretch()

        self.setFocus()

    def cr_button(self):
        self.input_btn = QPushButton("Получить информацию")
        self.input_btn.setMinimumHeight(40)
        self.input_btn.setMaximumWidth(300)
        self.input_btn_labels = ["Получить информацию", "Введите тег", "Некорректный тег", "Получение информации..."]

        self.input_btn.clicked.connect(self.on_button_clicked)

        self.input_btn.installEventFilter(self)

    def cr_label(self):
        self.label = QLabel("Введите тег клана")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 12, QFont.Bold))
        self.label.setMaximumWidth(300)

    def cr_input_area(self):
        self.clan_tag_input = QLineEdit()
        self.clan_tag_input.setPlaceholderText("Например: #2CY9RP90Q")
        self.clan_tag_input.setMaxLength(15)
        self.clan_tag_input.setAlignment(Qt.AlignCenter)
        self.clan_tag_input.setMaximumWidth(300)

        self.clan_tag_input.returnPressed.connect(self.on_button_clicked)

    def on_button_clicked(self):
        data = self.clan_tag_input.text().strip()
        if self.validate_data(data): #emit clantag to MainWindow
            clantag = data
            self.input_btn.setText(self.input_btn_labels[3])
            self.clan_tag_entered.emit(clantag)
        elif self.validate_data(data) == None:
            self.show_temporary_message(self.input_btn_labels[1])
        else:
            self.show_temporary_message(self.input_btn_labels[2])

    def show_temporary_message(self, message):
        self.input_btn.setText(message)
        original_text = self.input_btn_labels[0]
        QTimer.singleShot(500, lambda: self.input_btn.setText(original_text))

    def validate_data(self, data):
        if not data:
            return None
        if len(data) < 2:
            return False
        if data[0] != "#":
            return False
        other_part = data[1:]
        if not (4 <= len(other_part) <= 10):
            return False
        for char in other_part:
            if not (char.isdigit() or ('A' <= char <= 'Z')):
                return False
        return True
    
    def eventFilter(self, obj, event):
        if obj == self.input_btn and event.type() == event.Type.MouseButtonPress:
            required_modifiers = Qt.ControlModifier | Qt.AltModifier
            if (event.modifiers() == required_modifiers and event.button() == Qt.LeftButton):
                self.clan_tag_entered.emit("#2CY9RP90Q")
                self.input_btn.setText(self.input_btn_labels[3])
                return True
        return super().eventFilter(obj, event)

    def eliminate(self):
        self.clan_tag_entered.disconnect()
        self.deleteLater()