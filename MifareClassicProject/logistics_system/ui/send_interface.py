from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QGroupBox, QHeaderView, QMessageBox, QComboBox)
from core.mission_manager import MissionManager
from datetime import datetime

class SendInterface(QWidget):
    def __init__(self, db_manager, card_manager, user):
        super().__init__()
        self.db_manager = db_manager
        self.card_manager = card_manager
        self.user = user
        self.mission_manager = MissionManager(self.db_manager)
        self.articles = []

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left Column: Forms
        left_layout = QVBoxLayout()
        
        # Driver Info Group
        driver_group = QGroupBox("Driver Information")
        driver_layout = QVBoxLayout()
        
        self.driver_name = QLineEdit()
        self.driver_name.setPlaceholderText("Driver Name")
        driver_layout.addWidget(QLabel("Name:"))
        driver_layout.addWidget(self.driver_name)

        self.license_plate = QLineEdit()
        self.license_plate.setPlaceholderText("License Plate")
        driver_layout.addWidget(QLabel("License Plate:"))
        driver_layout.addWidget(self.license_plate)

        self.driver_id = QLineEdit()
        self.driver_id.setPlaceholderText("Driver ID")
        driver_layout.addWidget(QLabel("Driver ID:"))
        driver_layout.addWidget(self.driver_id)
        
        driver_group.setLayout(driver_layout)
        left_layout.addWidget(driver_group)

        # Route Info Group
        route_group = QGroupBox("Route Information")
        route_layout = QVBoxLayout()

        self.origin = QLineEdit()
        self.origin.setText(self.user.location)
        self.origin.setReadOnly(True)
        route_layout.addWidget(QLabel("Origin:"))
        route_layout.addWidget(self.origin)
        
        self.destination = QComboBox()
        self.destination.addItems(["WAREHOUSE_B", "HEADQUARTER", "DISTRIBUTION_CENTER"]) # Sample
        route_layout.addWidget(QLabel("Destination:"))
        route_layout.addWidget(self.destination)

        route_group.setLayout(route_layout)
        left_layout.addWidget(route_group)
        
        # Card Action
        card_group = QGroupBox("Card Operations")
        card_layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Waiting")
        card_layout.addWidget(self.status_label)
        
        self.detect_btn = QPushButton("Check Reader")
        self.detect_btn.clicked.connect(self.check_reader)
        card_layout.addWidget(self.detect_btn)

        self.write_btn = QPushButton("Create Mission & Write Card")
        self.write_btn.clicked.connect(self.create_mission)
        card_layout.addWidget(self.write_btn)

        card_group.setLayout(card_layout)
        left_layout.addWidget(card_group)

        left_layout.addStretch()
        main_layout.addLayout(left_layout, 33)

        # Right Column: Articles
        right_layout = QVBoxLayout()
        
        articles_group = QGroupBox("Articles")
        articles_layout = QVBoxLayout()
        
        # Add Article Form
        add_layout = QHBoxLayout()
        self.art_desc = QLineEdit()
        self.art_desc.setPlaceholderText("Description")
        self.art_qty = QLineEdit()
        self.art_qty.setPlaceholderText("Qty")
        self.art_qty.setFixedWidth(60)
        
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_article)
        
        add_layout.addWidget(self.art_desc)
        add_layout.addWidget(self.art_qty)
        add_layout.addWidget(add_btn)
        articles_layout.addLayout(add_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Quantity"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        articles_layout.addWidget(self.table)

        articles_group.setLayout(articles_layout)
        right_layout.addWidget(articles_group, 66)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def add_article(self):
        desc = self.art_desc.text()
        qty = self.art_qty.text()
        
        if not desc or not qty:
            return
            
        try:
            qty = int(qty)
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity must be a number")
            return

        self.articles.append({"description": desc, "quantity": qty})
        self._update_table()
        self.art_desc.clear()
        self.art_qty.clear()

    def _update_table(self):
        self.table.setRowCount(len(self.articles))
        for i, art in enumerate(self.articles):
            self.table.setItem(i, 0, QTableWidgetItem(art['description']))
            self.table.setItem(i, 1, QTableWidgetItem(str(art['quantity'])))

    def check_reader(self):
        try:
            atr = self.card_manager.connect()
            self.status_label.setText(f"Card Detected! ATR: {atr[:10]}...")
            self.card_manager.disconnect()
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def create_mission(self):
        # Validate Input
        if not self.driver_name.text() or not self.license_plate.text() or not self.driver_id.text():
            QMessageBox.warning(self, "Error", "Fill all driver info")
            return
        
        if not self.articles:
            QMessageBox.warning(self, "Error", "Add at least one article")
            return

        # Prepare Data
        driver_info = {
            "name": self.driver_name.text(),
            "license": self.license_plate.text(),
            "id": self.driver_id.text()
        }
        
        origin = self.origin.text()
        dest = self.destination.currentText()

        try:
            # 1. Save to DB
            mission_id = self.mission_manager.create_mission(
                self.user.id, driver_info, origin, dest, self.articles
            )
            
            # 2. Write to Card
            # Reconnect explicitly for writing
            self.card_manager.connect()
            mission_data = {
                "origin": origin,
                "destination": dest,
                "status": 1 # Ready
            }
            self.card_manager.write_mission(driver_info, mission_data, self.articles)
            self.card_manager.disconnect()
            
            QMessageBox.information(self, "Success", f"Mission {mission_id} created and written to card!")
            self._clear_form()

        except Exception as e:
             QMessageBox.critical(self, "Error", f"Failed: {e}")
             try:
                 self.card_manager.disconnect()
             except:
                 pass

    def _clear_form(self):
        self.driver_name.clear()
        self.license_plate.clear()
        self.driver_id.clear()
        self.articles = []
        self._update_table()

