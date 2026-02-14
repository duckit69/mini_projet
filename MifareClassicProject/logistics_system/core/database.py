import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="data/database.db"):
        self.db_path = db_path
        self._ensure_data_dir()
        self._create_tables()
        self._seed_data()

    def _ensure_data_dir(self):
        directory = os.path.dirname(self.db_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                location TEXT,
                full_name TEXT
            )
        ''')

        # Missions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missions (
                mission_id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_name TEXT,
                license_plate TEXT,
                driver_id TEXT,
                origin TEXT,
                destination TEXT,
                status INTEGER DEFAULT 0,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        ''')

         # Articles Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission_id INTEGER,
                description TEXT,
                quantity INTEGER,
                FOREIGN KEY (mission_id) REFERENCES missions(mission_id) ON DELETE CASCADE
            )
        ''')

        # Audit Logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()
        conn.close()

    def _seed_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Check if users exist
        cursor.execute("SELECT count(*) FROM users")
        if cursor.fetchone()[0] == 0:
            users = [
                ('admin', 'admin123', 'admin', 'HEADQUARTER', 'System Administrator'),
                ('validator_a', 'pass123', 'validator_a', 'WAREHOUSE_A', 'Alice Sender'),
                ('validator_b', 'pass123', 'validator_b', 'WAREHOUSE_B', 'Bob Receiver')
            ]
            cursor.executemany('''
                INSERT INTO users (username, password, role, location, full_name)
                VALUES (?, ?, ?, ?, ?)
            ''', users)
            print("Database seeded with default users.")
        
        conn.commit()
        conn.close()

    def execute_query(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except Exception as e:
            print(f"Database Error: {e}")
            raise
        finally:
            conn.close()

    def fetch_one(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result

    def fetch_all(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result

if __name__ == "__main__":
    db = DatabaseManager()
    print(f"Database initialized at {db.db_path}")
