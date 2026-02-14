from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QGroupBox, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from core.mission_manager import MissionManager

class ReceiveInterface(QWidget):
    def __init__(self, db_manager, card_manager, user):
        super().__init__()
        self.db_manager = db_manager
        self.card_manager = card_manager
        self.user = user
        self.mission_manager = MissionManager(self.db_manager)
        
        self.scanned_data = None
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left: Controls & Info
        left_layout = QVBoxLayout()
        
        # Reader Control
        read_group = QGroupBox("Card Reader")
        read_layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Ready to Scan")
        self.status_label.setStyleSheet("font-weight: bold; color: blue;")
        read_layout.addWidget(self.status_label)
        
        scan_btn = QPushButton("Read Card Mission")
        scan_btn.setMinimumHeight(50)
        scan_btn.clicked.connect(self.read_card)
        read_layout.addWidget(scan_btn)
        
        read_group.setLayout(read_layout)
        left_layout.addWidget(read_group)

        # Verification Status
        self.verify_group = QGroupBox("Verification")
        verify_layout = QVBoxLayout()
        self.verify_label = QLabel("Not Scanned")
        self.verify_label.setWordWrap(True)
        verify_layout.addWidget(self.verify_label)
        self.verify_group.setLayout(verify_layout)
        left_layout.addWidget(self.verify_group)

        # Actions
        action_group = QGroupBox("Actions")
        action_layout = QHBoxLayout()
        
        self.approve_btn = QPushButton("APPROVE")
        self.approve_btn.setStyleSheet("background-color: #d4edda; color: green; font-weight: bold;")
        self.approve_btn.setEnabled(False)
        self.approve_btn.clicked.connect(lambda: self.process_mission(2)) # 2 = Approved
        
        self.reject_btn = QPushButton("REJECT")
        self.reject_btn.setStyleSheet("background-color: #f8d7da; color: red; font-weight: bold;")
        self.reject_btn.setEnabled(False)
        self.reject_btn.clicked.connect(lambda: self.process_mission(3)) # 3 = Rejected

        action_layout.addWidget(self.approve_btn)
        action_layout.addWidget(self.reject_btn)
        action_group.setLayout(action_layout)
        left_layout.addWidget(action_group)
        
        left_layout.addStretch()
        main_layout.addLayout(left_layout, 35)

        # Right: Display Data
        right_layout = QVBoxLayout()
        
        # Driver Info
        info_group = QGroupBox("Driver & Route")
        info_layout = QVBoxLayout()
        self.info_text = QLabel("No Data")
        info_layout.addWidget(self.info_text)
        info_group.setLayout(info_layout)
        right_layout.addWidget(info_group)

        # Articles
        art_group = QGroupBox("Manifest")
        art_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Description", "Quantity"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        art_layout.addWidget(self.table)
        art_group.setLayout(art_layout)
        right_layout.addWidget(art_group)

        main_layout.addLayout(right_layout, 65)
        self.setLayout(main_layout)

    def read_card(self):
        try:
            self.card_manager.connect()
            data = self.card_manager.read_mission()
            self.card_manager.disconnect()
            
            self.scanned_data = data
            self.display_data(data)
            self.validate_mission(data)
            
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
            self.status_label.setStyleSheet("color: red;")
            try:
                self.card_manager.disconnect()
            except:
                pass

    def display_data(self, data):
        # Driver Info
        info = f"""
        <b>Driver:</b> {data.get('driver_name','')}<br>
        <b>License:</b> {data.get('license_plate','')}<br>
        <b>ID:</b> {data.get('driver_id','')}<br>
        <hr>
        <b>Origin:</b> {data.get('origin','')}<br>
        <b>Destination:</b> {data.get('destination','')}
        """
        self.info_text.setText(info)
        
        # Articles
        articles = data.get('articles', [])
        self.table.setRowCount(len(articles))
        for i, art in enumerate(articles):
            self.table.setItem(i, 0, QTableWidgetItem(art['description']))
            self.table.setItem(i, 1, QTableWidgetItem(str(art['quantity'])))

    def validate_mission(self, data):
        dest = data.get('destination', '').strip()
        current = self.user.location.strip()
        
        if dest == current:
            self.verify_label.setText(f"LOCATION MATCH\nDestination matches {current}")
            self.verify_label.setStyleSheet("color: green; font-size: 14px; font-weight: bold;")
            self.approve_btn.setEnabled(True)
            self.reject_btn.setEnabled(True)
        else:
            self.verify_label.setText(f"LOCATION MISMATCH\nCard says: {dest}\nYou are: {current}")
            self.verify_label.setStyleSheet("color: red; font-size: 14px; font-weight: bold;")
            self.approve_btn.setEnabled(False) # Maybe allow reject?
            self.reject_btn.setEnabled(True)

    def process_mission(self, status_code):
        # We need to find the mission in DB to update it.
        # Since we don't wonder Mission ID on card (my bad design choice in plan),
        # we will use Driver ID and "0" (Packaging) or "1" (Ready/InTransit) status match.
        # This is a heuristic for the POC.
        
        driver_id = self.scanned_data.get('driver_id')
        
        # Find active mission for this driver
        # Query: Select ID from missions where driver_id = ? AND status IN (0,1) ORDER BY created_at DESC LIMIT 1
        query = "SELECT mission_id FROM missions WHERE driver_id = ? AND status IN (0, 1) ORDER BY created_at DESC LIMIT 1"
        row = self.db_manager.fetch_one(query, (driver_id,))
        
        if row:
            mission_id = row[0]
            self.mission_manager.update_status(mission_id, status_code, self.user.id)
            status_str = "APPROVED" if status_code == 2 else "REJECTED"
            QMessageBox.information(self, "Processed", f"Mission {mission_id} marked as {status_str}")
            
            # Reset UI
            self.scanned_data = None
            self.approve_btn.setEnabled(False)
            self.reject_btn.setEnabled(False)
            self.info_text.setText("No Data")
            self.table.setRowCount(0)
            self.verify_label.setText("Not Scanned")
        else:
            QMessageBox.warning(self, "Warning", "Could not find an active mission in DB for this driver to update.")

