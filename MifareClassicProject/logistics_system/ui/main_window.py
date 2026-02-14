from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QStackedWidget, QAction, QMessageBox)
from ui.send_interface import SendInterface
from ui.receive_interface import ReceiveInterface
from ui.admin_panel import AdminPanel

from core.card_manager import CardManager

class MainWindow(QMainWindow):
    def __init__(self, auth_manager, db_manager, card_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.db_manager = db_manager
        self.card_manager = card_manager
        self.current_user = self.auth_manager.current_user
        
        self.setWindowTitle(f"Logistics System - {self.current_user.full_name} ({self.current_user.role})")
        self.resize(1024, 768)
        
        self.init_ui()

    def init_ui(self):
        # Menu Bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.handle_logout)
        file_menu.addAction(logout_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Central Widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Load appropriate interface based on role
        self.load_interface()

    def load_interface(self):
        role = self.current_user.role
        
        if role == 'validator_a':
            self.interface = SendInterface(self.db_manager, self.card_manager, self.current_user)
            self.central_widget.addWidget(self.interface)
        elif role == 'validator_b':
            self.interface = ReceiveInterface(self.db_manager, self.card_manager, self.current_user)
            self.central_widget.addWidget(self.interface)
        elif role == 'admin':
            self.interface = AdminPanel(self.db_manager, self.current_user)
            self.central_widget.addWidget(self.interface)
        else:
            self.central_widget.addWidget(QLabel("Unknown Role"))

    def handle_logout(self):
        self.auth_manager.logout()
        self.close()
