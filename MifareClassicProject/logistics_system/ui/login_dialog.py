from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.user = None
        self.setWindowTitle("Logistics System Login")
        self.setFixedSize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user = self.auth_manager.login(username, password)
        if user:
            self.user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
            self.password_input.clear()
