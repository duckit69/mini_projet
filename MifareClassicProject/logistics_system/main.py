import sys
from PyQt5.QtWidgets import QApplication, QDialog
from core.database import DatabaseManager
from core.auth import AuthManager
from core.card_manager import CardManager
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion') # Modern look

    db_manager = DatabaseManager()
    auth_manager = AuthManager(db_manager)
    card_manager = CardManager()

    # Login Loop
    while True:
        login = LoginDialog(auth_manager)
        if login.exec_() == QDialog.Accepted:
            window = MainWindow(auth_manager, db_manager, card_manager)
            window.show()
            
            # Since exec_() blocks, when main window closes, we check if we should loop (logout) or exit
            # For simplicity in this structure, if MainWindow closes, we exit the app unless we implement specific signal
            app.exec_()
            
            if not auth_manager.current_user: # If logged out
                continue # Show login again
            else:
                break # Exit
        else:
            break

if __name__ == "__main__":
    main()
