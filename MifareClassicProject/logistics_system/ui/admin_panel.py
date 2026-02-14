from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView,
                             QDialog, QLabel, QLineEdit, QComboBox, QMessageBox)
from core.database import DatabaseManager

class AdminPanel(QWidget):
    def __init__(self, db_manager, user):
        super().__init__()
        self.db_manager = db_manager
        self.user = user
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        
        # Tab 1: Users
        self.user_tab = QWidget()
        self.init_user_tab()
        self.tabs.addTab(self.user_tab, "User Management")
        
        # Tab 2: Missions
        self.mission_tab = QWidget()
        self.init_mission_tab()
        self.tabs.addTab(self.mission_tab, "Missions")
        
        # Tab 3: Audit Logs
        self.audit_tab = QWidget()
        self.init_audit_tab()
        self.tabs.addTab(self.audit_tab, "Audit Logs")
        
        layout.addWidget(self.tabs)
        
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.clicked.connect(self.refresh_all)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)

    def refresh_all(self):
        self.load_users()
        self.load_missions()
        self.load_audits()

    # --- User Tab ---
    def init_user_tab(self):
        layout = QVBoxLayout()
        
        # Actions
        actions = QHBoxLayout()
        add_btn = QPushButton("Add User")
        add_btn.clicked.connect(self.show_add_user_dialog)
        actions.addWidget(add_btn)
        actions.addStretch()
        layout.addLayout(actions)
        
        # Table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Location", "Name"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.user_table)
        
        self.user_tab.setLayout(layout)
        self.load_users()

    def load_users(self):
        rows = self.db_manager.fetch_all("SELECT id, username, role, location, full_name FROM users")
        self.user_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.user_table.setItem(i, j, QTableWidgetItem(str(val)))

    def show_add_user_dialog(self):
        dialog = AddUserDialog(self.db_manager)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()

    # --- Mission Tab ---
    def init_mission_tab(self):
        layout = QVBoxLayout()
        self.mission_table = QTableWidget()
        self.mission_table.setColumnCount(7)
        self.mission_table.setHorizontalHeaderLabels(["ID", "Driver", "Origin", "Destination", "Status", "Created At", "Articles"])
        self.mission_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.mission_table)
        self.mission_tab.setLayout(layout)
        self.load_missions()

    def load_missions(self):
        query = '''
            SELECT m.mission_id, m.driver_name, m.origin, m.destination, m.status, m.created_at, COUNT(a.id)
            FROM missions m
            LEFT JOIN articles a ON m.mission_id = a.mission_id
            GROUP BY m.mission_id
            ORDER BY m.created_at DESC
        '''
        rows = self.db_manager.fetch_all(query)
        self.mission_table.setRowCount(len(rows))
        status_map = {0: "Formatting", 1: "Ready", 2: "Approved", 3: "Rejected"}
        
        for i, row in enumerate(rows):
            self.mission_table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.mission_table.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.mission_table.setItem(i, 2, QTableWidgetItem(str(row[2])))
            self.mission_table.setItem(i, 3, QTableWidgetItem(str(row[3])))
            
            status_text = status_map.get(row[4], str(row[4]))
            self.mission_table.setItem(i, 4, QTableWidgetItem(status_text))
            
            self.mission_table.setItem(i, 5, QTableWidgetItem(str(row[5])))
            self.mission_table.setItem(i, 6, QTableWidgetItem(f"{row[6]} Items"))

    # --- Audit Tab ---
    def init_audit_tab(self):
        layout = QVBoxLayout()
        self.audit_table = QTableWidget()
        self.audit_table.setColumnCount(4)
        self.audit_table.setHorizontalHeaderLabels(["Time", "User", "Action", "Details"])
        self.audit_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.audit_table)
        self.audit_tab.setLayout(layout)
        self.load_audits()

    def load_audits(self):
        query = '''
            SELECT a.timestamp, u.username, a.action, a.details
            FROM audit_logs a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.timestamp DESC
            LIMIT 100
        '''
        rows = self.db_manager.fetch_all(query)
        self.audit_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.audit_table.setItem(i, j, QTableWidgetItem(str(val)))


class AddUserDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Add User")
        self.setFixedSize(300, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Full Name")
        layout.addWidget(QLabel("Full Name:"))
        layout.addWidget(self.full_name)

        self.role = QComboBox()
        self.role.addItems(["validator_a", "validator_b", "admin"])
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.role)

        self.location = QComboBox()
        self.location.addItems(["HEADQUARTER", "WAREHOUSE_A", "WAREHOUSE_B", "DISTRIBUTION_CENTER"])
        layout.addWidget(QLabel("Location:"))
        layout.addWidget(self.location)

        btn = QPushButton("Create User")
        btn.clicked.connect(self.create_user)
        layout.addWidget(btn)

        self.setLayout(layout)

    def create_user(self):
        user = self.username.text()
        pwd = self.password.text()
        role = self.role.currentText()
        loc = self.location.currentText()
        name = self.full_name.text()
        
        if not user or not pwd:
            return

        try:
            query = "INSERT INTO users (username, password, role, location, full_name) VALUES (?, ?, ?, ?, ?)"
            self.db_manager.execute_query(query, (user, pwd, role, loc, name))
            QMessageBox.information(self, "Success", "User created")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
