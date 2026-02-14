from datetime import datetime

class Article:
    def __init__(self, id, mission_id, description, quantity):
        self.id = id
        self.mission_id = mission_id
        self.description = description
        self.quantity = quantity

    def to_dict(self):
        return {
            "description": self.description,
            "quantity": self.quantity
        }

class Mission:
    def __init__(self, mission_id, driver_name, license_plate, driver_id, origin, destination, status, created_by, created_at, updated_at, articles=None):
        self.mission_id = mission_id
        self.driver_name = driver_name
        self.license_plate = license_plate
        self.driver_id = driver_id
        self.origin = origin
        self.destination = destination
        self.status = status # 0: Packaging, 1: Ready, 2: In Transit, 3: Delivered, 4: Rejected
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.articles = articles if articles else []

    @staticmethod
    def from_db_row(row, articles=None):
        if not row:
            return None
        return Mission(
            mission_id=row[0],
            driver_name=row[1],
            license_plate=row[2],
            driver_id=row[3],
            origin=row[4],
            destination=row[5],
            status=row[6],
            created_by=row[7],
            created_at=row[8],
            updated_at=row[9],
            articles=articles
        )
