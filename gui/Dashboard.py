from PyQt6.QtWidgets import (
    QApplication, QToolBar, QStatusBar, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel
)
from PyQt6.QtCore import QTimer
from ui.Picture import Logo
from supabase import Client

class Dashboard(QWidget):
    
    def __init__(self, client:Client, parent=None):
        super().__init__(parent)
        self.supabase = client
        self.windowPosSize = (200, 200, 800, 600)
        # Set main window title and size
        self.setGeometry(*self.windowPosSize)

        # Main layout (Vertical)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self.createTaskbar()
        self.createCentralArea()
        self.createStatusbar()
        self.createFloatingButton()
        
    def createCentralArea(self):
        # Central layout (Horizontal)
        self.central_layout = QHBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        # Add the central layout to the main layout
        self.main_layout.addLayout(self.central_layout)

        # Create the left sidebar
        self.createLeftSidebar()

        # Create a placeholder for the main content
        self.main_content = QWidget()
        self.main_content.setStyleSheet("""
            background-color: #272627;
        """)
        self.central_layout.addWidget(self.main_content)

    def createLeftSidebar(self):
        # Create a fixed left sidebar
        self.left_sidebar = QWidget(self)
        self.left_sidebar.setFixedWidth(200)
        self.left_sidebar.setStyleSheet("""
            background-color: #121212;
            border-right: 1px solid #585858;
        """)
        
        # Sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(10)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.left_sidebar.setLayout(sidebar_layout)

        sidebar_layout.addWidget(QPushButton("Task List"))
        sidebar_layout.addWidget(QPushButton("View Progress"))
        sidebar_layout.addStretch()

        # Add the sidebar to the central layout
        self.central_layout.addWidget(self.left_sidebar)

    def updateToggleButtonPosition(self):
        if self.left_sidebar.isVisible():
            # Position the button on the right border of the sidebar
            self.toggle_button.setText("<<")
            self.toggle_button.move(199, 41)
        else:
            # Position the button near the left border of the window
            self.toggle_button.setText(">>")
            self.toggle_button.move(0, 41)

    def createFloatingButton(self):
        # Create a toggle button that floats above other widgets
        self.toggle_button = QPushButton(">>", self)
        self.toggle_button.setToolTip("Toggle Sidebar")
        self.toggle_button.setFixedWidth(25)
        self.toggle_button.setFixedHeight(25)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                border: 1px solid #585858;
            }
        """)
        # Make it clickable
        self.toggle_button.clicked.connect(self.toggleLeftSidebar)
        QTimer.singleShot(0, self.updateToggleButtonPosition)

    def createTaskbar(self):
        # Create a toolbar for the taskbar
        taskbar = QToolBar("Taskbar", self)
        taskbar.setMovable(False)

        # Add left-aligned actions
        taskbar.addAction("Menu")
        taskbar.addAction("Edit")
        taskbar.addAction("Tools")
        
        # Add a spacer to push subsequent items to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        taskbar.addWidget(spacer)

        user = self.supabase.auth.get_user().user

        label = QLabel()
        label.setText(user.user_metadata['name'])

        # Add right-aligned widget (e.g., logo)
        url = user.user_metadata['avatar_url']
        logo = Logo(url, [20, 20], is_url=True)

        taskbar.addWidget(label)
        taskbar.addWidget(logo)

        # Style the toolbar
        taskbar.setStyleSheet("""
            QToolBar {
                background-color: #121212;
                border-top: 1px solid #585858;
                border-bottom: 1px solid #585858;
            }
        """)

        # Add the taskbar to the main layout
        self.main_layout.addWidget(taskbar)

    def createStatusbar(self):
        # Create a status bar at the bottom of the window
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #121212;
                border-top : 1px solid #585858;
            }
        """)
        self.status_bar.setFixedHeight(25)

        button1 = QPushButton(".")
        button1.setStyleSheet("""
            QPushButton {
                width : 5px;
                height: 5px;
                background-color: #4CAF50;
                padding: 3px;
                border-radius: 5px;
            }
        """)

        self.status_bar.addWidget(button1)
        self.status_bar.showMessage(f"\t\t\tReady")

        # Add the status bar to the main layout
        self.main_layout.addWidget(self.status_bar)

    def toggleLeftSidebar(self):
        if self.left_sidebar.isVisible():
            self.left_sidebar.hide()
        else:
            self.left_sidebar.show()
        
        # Update the toggle button text
        self.toggle_button.setText("<<")
        self.toggle_button.move(199, 41)

    def resizeEvent(self, event):
        super().resizeEvent(event)

# Application setup
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
