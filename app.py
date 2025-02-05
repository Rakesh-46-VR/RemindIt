import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt, QTimer
from gui.Login import Login
from gui.Dashboard import Dashboard
from dotenv import load_dotenv
from supabase import create_client
from utils.session import existsSession

load_dotenv()

os.environ['QT_QPA_PLATFORM'] = 'xcb'

SUPABASE_URL = os.getenv('SUPABASE_URL')  # Replace with your Supabase URL
SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY')

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create supabase client
        self.supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
        
        existsSession(self.supabase)

        self.setWindowTitle("RemindIt")
        # Create the stacked widget
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Create login page and dashboard page
        self.login_page = Login(self.supabase, self.on_login, parent=self.stacked_widget)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.startFlow()

    def on_login(self, is_loggedin):
        if(is_loggedin):
            QTimer.singleShot(0, self.startFlow)

    def startFlow(self):

        if(existsSession(self.supabase)):
            self.dashboard_page = Dashboard(self.supabase, parent=self.stacked_widget)
            self.stacked_widget.addWidget(self.dashboard_page)
            self.setGeometry(*self.dashboard_page.windowPosSize)
            self.stacked_widget.setCurrentWidget(self.dashboard_page)
        else:
            self.setGeometry(*self.login_page.windowPosSize)
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
            self.stacked_widget.setCurrentWidget(self.login_page)

def main():
    app = QApplication(sys.argv)

    window = MainApp()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
