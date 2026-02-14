class User:
    def __init__(self, id, username, role, location, full_name):
        self.id = id
        self.username = username
        self.role = role
        self.location = location
        self.full_name = full_name

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

    @staticmethod
    def from_db_row(row):
        if not row:
            return None
        # row structure: (id, username, password, role, location, full_name)
        return User(
            id=row[0],
            username=row[1],
            role=row[3],
            location=row[4],
            full_name=row[5]
        )
