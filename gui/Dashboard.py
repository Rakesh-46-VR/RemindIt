from PyQt6.QtWidgets import (
    QApplication, QToolBar, QStatusBar, QListWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel, QStackedWidget
)
from ui.Picture import Logo
from supabase import Client
from ui.ScrollableWidget import OrderableList
from gui.ToDo import DailyTasks

class Dashboard(QWidget):
    
    def __init__(self, client:Client, parent=None):
        super().__init__(parent)
        self.supabase = client
        self.windowPosSize = (2020, 300, 880, 600)
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

        # Stacked layout for various functions
        
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
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)

        dw = DailyTasks()
        self.stacked_widget.addWidget(dw)
        self.stacked_widget.addWidget(OrderableList("Task Reporting"))

        hbox = QHBoxLayout()
        hbox.addWidget(self.stacked_widget)

        self.main_content = QWidget()        
        self.main_content.setStyleSheet("""
            background-color: #121212;
        """)

        self.main_content.setLayout(hbox)
        self.central_layout.addWidget(self.main_content)

    def createLeftSidebar(self):
        # Create a fixed left sidebar
        self.left_sidebar = QListWidget(self)
        self.left_sidebar.setFixedWidth(200)

        self.left_sidebar.insertItem(0, "Edit Daily Tasks")
        self.left_sidebar.insertItem(1, "Report Tasks")
        self.left_sidebar.setCurrentRow(0)
        self.left_sidebar.setStyleSheet("""
            QListWidget {
                background-color: #121212;
                border-right: 2px solid #ffffff;
                margin-right:2px;
            }
            QListWidget::item {
                color: white;
                padding: 10px;
                border-bottom: 1px solid #303030;
            }
            QListWidget::item:selected {
                background-color: #2c2c2c;
                border-left: 4px solid #ff9800;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #1a1a1a;
            }
        """)

        self.left_sidebar.currentRowChanged.connect(self.display)
        
        self.central_layout.addWidget(self.left_sidebar)
    
    def display(self, i):
        self.stacked_widget.setCurrentIndex(i)

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

    def resizeEvent(self, event):
        super().resizeEvent(event)

# Application setup
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())