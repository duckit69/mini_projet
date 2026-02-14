from core.database import DatabaseManager
from core.auth import AuthManager
from core.mission_manager import MissionManager

def test_system():
    print("Initializing DB...")
    db = DatabaseManager()
    
    print("Testing Auth...")
    auth = AuthManager(db)
    user = auth.login("validator_a", "pass123")
    if user and user.role == "validator_a":
        print("  [PASS] Login successful")
    else:
        print("  [FAIL] Login failed")
        
    print("Testing Mission Creation...")
    mm = MissionManager(db)
    driver_info = {"name": "John Doe", "license": "ABC-123", "id": "D001"}
    articles = [{"description": "Box", "quantity": 10}]
    
    try:
        m_id = mm.create_mission(user.id, driver_info, "WAREHOUSE_A", "WAREHOUSE_B", articles)
        print(f"  [PASS] Created Mission ID: {m_id}")
    except Exception as e:
        print(f"  [FAIL] Mission creation error: {e}")

    print("Testing Mission Retrieval...")
    m = mm.get_mission_by_id(m_id)
    if m and m.driver_name == "John Doe":
        print(f"  [PASS] Retrieved Mission matches")
    else:
        print(f"  [FAIL] Mission mismatch")

    print("Testing Audit Log...")
    logs = db.fetch_all("SELECT * FROM audit_logs WHERE user_id = ?", (user.id,))
    if len(logs) > 0:
        print(f"  [PASS] Audit logs found ({len(logs)} entries)")
    else:
        print("  [FAIL] No audit logs")

if __name__ == "__main__":
    test_system()
