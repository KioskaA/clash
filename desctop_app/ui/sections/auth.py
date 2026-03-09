# Эта секция - Первое что видит пользователь
# Так же вновь отображается если в меню нажата кнопка "Выход из аккаунта"
#
# Внутри секции:
# Поля ввода "логин", "пароль"
# Кнопки "войти", "зарегестрироваться"
#
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QGroupBox, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                               QVBoxLayout, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QFont, QKeyEvent



class AuthSection(QWidget):
    register_requested = Signal()

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
        self.create_login_button()
        self.create_signup_button()

        for widget in self.widgets:
            content_layout.addWidget(widget)

        center_layout.addLayout(content_layout)
        center_layout.addStretch()

        main_layout.addLayout(center_layout)
        main_layout.addStretch()

    def create_login_input(self):
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.login_input.setMaxLength(15)
        self.login_input.setAlignment(Qt.AlignCenter)
        self.login_input.setMaximumWidth(300)
        
        self.widgets.append(self.login_input)

    def create_password_input(self):
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setMaxLength(15)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setMaximumWidth(300)
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.widgets.append(self.password_input)

    def create_login_button(self):
        self.login_btn = QPushButton("Войти в аккаунт")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setMaximumWidth(300)

        self.widgets.append(self.login_btn)

    def create_signup_button(self):
        self.signup_btn = QPushButton("Зарегестрироваться")
        self.signup_btn.setMinimumHeight(40)
        self.signup_btn.setMaximumWidth(300)
        
        self.signup_btn.clicked.connect(self.register_requested.emit)

        self.widgets.append(self.signup_btn)