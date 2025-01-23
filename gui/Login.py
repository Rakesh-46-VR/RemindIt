import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt
from auth.Authorization import AuthManager
import pickle
import os
from ui.Picture import LogoWithText
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')  # Replace with your Supabase URL
SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY')
TOKEN_PATH = os.getenv('TOKEN_PATH')
LOGO_PATH = os.getenv('ICON')
GOOGLE_LOGO = os.getenv("GOOGLE_LOGO")

class Login(QWidget):
    def __init__(self, client, callback, parent=None):
        super().__init__(parent)

        self.supabase = client
        self.callback = callback

        self.windowPosSize = (200, 200, 400, 300)
        self.auth_manager = AuthManager(self.on_login)
        
        self.setGeometry(*self.windowPosSize)
        
        # Layout
        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_with_text = LogoWithText(LOGO_PATH, "Welcome, Lets set up your account.", [50,50])
        layout.addWidget(logo_with_text)
        
        self.login_button = QPushButton("\t\t\tLogin with Google")
        self.login_button.setIcon(QIcon(GOOGLE_LOGO))
        self.login_button.setIconSize(QSize(25,25))
        
        self.login_button.setFixedHeight(40)
        self.login_button.setFixedWidth(300)
        self.login_button.clicked.connect(self.login)

        layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)

    def on_login(self, is_loggedin):
        if(is_loggedin):
            self.login_button.setText("Authentication successfull")
            self.callback(is_loggedin)

    def login(self):
        try:
            self.login_button.setText("Authentication in progress...")
            if(os.path.exists(TOKEN_PATH)):
                with open(TOKEN_PATH, "rb") as file:
                    data  = pickle.load(file)
                    if(data.get("access_token") and data.get("refresh_token")):
                        self.auth_manager.access_token = data.get("access_token")
                        self.auth_manager.refresh_token = data.get("refresh_token")
                        self.supabase.auth.set_session(self.auth_manager.access_token , self.auth_manager.refresh_token)
                    else:
                        self.auth_manager.start_oauth_flow()
            else:
                self.auth_manager.start_oauth_flow()
        except Exception as e:
            print(e)

def main():
    app = QApplication(sys.argv)

    window = Login()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
