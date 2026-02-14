from core.database import DatabaseManager
from models.user import User

class AuthManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.current_user = None

    def login(self, username, password):
        """
        Authenticates a user and starts a session.
        Returns User object if successful, None otherwise.
        """
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        row = self.db.fetch_one(query, (username, password))
        
        if row:
            self.current_user = User.from_db_row(row)
            self._log_login()
            return self.current_user
        return None

    def logout(self):
        if self.current_user:
            self._log_logout()
            self.current_user = None

    def _log_login(self):
        if self.current_user:
            self.db.execute_query(
                "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
                (self.current_user.id, "LOGIN", f"User {self.current_user.username} logged in")
            )

    def _log_logout(self):
        if self.current_user:
            self.db.execute_query(
                "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
                (self.current_user.id, "LOGOUT", f"User {self.current_user.username} logged out")
            )
