# Секция регистрации
#
#
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QFont, QKeyEvent


class RegistrationSection(QWidget):
    back_to_login_requested = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.widgets = []

        self.setup()

    def setup(self):
        main_layout = QVBoxLayout(self)
        main_layout.addStretch()

        center_layout = QHBoxLayout()
        center_layout.addStretch()

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)

        self.create_login_input()
        self.create_password_input()
        self.create_reppassword_input()
        self.create_signup_button()
        self.create_back_button()

        for widget in self.widgets:
            content_layout.addWidget(widget)

        center_layout.addLayout(content_layout)
        center_layout.addStretch()

        main_layout.addLayout(center_layout)
        main_layout.addStretch()

        self.setFocus()

    def create_login_input(self):
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Придумайте логин")
        self.login_input.setMaxLength(15)
        self.login_input.setAlignment(Qt.AlignCenter)
        self.login_input.setMaximumWidth(300)
        
        self.widgets.append(self.login_input)

    def create_password_input(self):
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Придумайте пароль")
        self.password_input.setMaxLength(15)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setMaximumWidth(300)
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.widgets.append(self.password_input)

    def create_reppassword_input(self):
        self.reppassword_input = QLineEdit()
        self.reppassword_input.setPlaceholderText("Повторите пароль")
        self.reppassword_input.setMaxLength(15)
        self.reppassword_input.setAlignment(Qt.AlignCenter)
        self.reppassword_input.setMaximumWidth(300)
        self.reppassword_input.setEchoMode(QLineEdit.Password)
        
        self.widgets.append(self.reppassword_input)

    def create_signup_button(self):
        self.signup_btn = QPushButton("Зарегестрироваться")
        self.signup_btn.setMinimumHeight(40)
        self.signup_btn.setMaximumWidth(300)

        self.widgets.append(self.signup_btn)

    def create_back_button(self):
        self.back_btn = QPushButton("Назад")
        self.back_btn.setMinimumHeight(40)
        self.back_btn.setMaximumWidth(300)

        self.back_btn.clicked.connect(self.back_to_login_requested.emit)

        self.widgets.append(self.back_btn)