from core.database import DatabaseManager
from models.mission import Mission, Article
import json

class MissionManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_mission(self, user_id, driver_data, origin, destination, articles_list):
        """
        Creates a new mission and its associated articles.
        driver_data: dict with name, license, id
        articles_list: list of dicts {'description': '...', 'quantity': ...}
        """
        # Insert Mission
        query = '''
            INSERT INTO missions (driver_name, license_plate, driver_id, origin, destination, status, created_by)
            VALUES (?, ?, ?, ?, ?, 0, ?)
        '''
        params = (
            driver_data['name'],
            driver_data['license'],
            driver_data['id'],
            origin,
            destination,
            user_id
        )
        
        cursor = self.db.execute_query(query, params)
        mission_id = cursor.lastrowid

        # Insert Articles
        for article in articles_list:
            a_query = '''
                INSERT INTO articles (mission_id, description, quantity)
                VALUES (?, ?, ?)
            '''
            self.db.execute_query(a_query, (mission_id, article['description'], article['quantity']))
            
        self._log_action(user_id, "CREATE_MISSION", f"Created mission {mission_id} for {destination}")
        return mission_id

    def update_status(self, mission_id, new_status, user_id):
        query = "UPDATE missions SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE mission_id = ?"
        self.db.execute_query(query, (new_status, mission_id))
        self._log_action(user_id, "UPDATE_STATUS", f"Updated mission {mission_id} status to {new_status}")

    def get_mission_by_id(self, mission_id):
        query = "SELECT * FROM missions WHERE mission_id = ?"
        row = self.db.fetch_one(query, (mission_id,))
        if row:
            articles = self.get_mission_articles(mission_id)
            return Mission.from_db_row(row, articles)
        return None

    def get_mission_articles(self, mission_id):
        query = "SELECT id, mission_id, description, quantity FROM articles WHERE mission_id = ?"
        rows = self.db.fetch_all(query, (mission_id,))
        return [Article(r[0], r[1], r[2], r[3]) for r in rows]

    def get_all_missions(self):
        query = "SELECT * FROM missions ORDER BY created_at DESC"
        rows = self.db.fetch_all(query)
        return [Mission.from_db_row(row) for row in rows]

    def _log_action(self, user_id, action, details):
        self.db.execute_query(
            "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, action, details)
        )
