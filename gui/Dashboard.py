from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QStatusBar, QWidget, QVBoxLayout, QPushButton, QGroupBox
)
from PyQt6.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set main window title and size
        self.setWindowTitle("RemindIt")
        self.resize(800, 600)

        # Create a central widget
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
        
        # Add a left sidebar (Dock Widget)
        self.createLeftSidebar()

        # Add a taskbar (Toolbar)
        self.createTaskbar()

        # Add a bottom status bar
        self.createStatusbar()

    def createLeftSidebar(self):
        # Create a fixed left sidebar
        self.left_sidebar = QWidget(self)
        self.left_sidebar.setFixedWidth(200)
        self.left_sidebar.setStyleSheet("""
            border-right: 1px solid #cccccc;
        """)
        # Add content to the sidebar
        sidebar_layout = QVBoxLayout()
        self.left_sidebar.setLayout(sidebar_layout)

        sidebar_layout.setSpacing(10)

        sidebar_layout.addWidget(QPushButton("Task List"))
        sidebar_layout.addWidget(QPushButton("View Progress"))

        sidebar_layout.addStretch()
        
        # Add the sidebar to the central layout
        self.centralWidget().layout().addWidget(self.left_sidebar)

        # Create a toggle button
        self.toggle_button = QPushButton(">>", self)
        self.toggle_button.setToolTip("Sidebar")
        self.toggle_button.setFixedWidth(22)  # Narrow button width
        self.toggle_button.setStyleSheet("""             
            border: 1px solid #cccccc
        """)
        self.setStyleSheet("""
            QToolTip {
                background-color: #ffffff;
                color: black;
                border: 4px solid #000000;
                font-size: 10px;
                padding: 3px;
            }
        """)
        self.toggle_button.clicked.connect(self.toggleLeftSidebar)
        QTimer.singleShot(0, self.updateToggleButtonPosition)

    def updateToggleButtonPosition(self):
        if self.left_sidebar.isVisible():
            # Position the button on the right border of the sidebar
            self.toggle_button.move(199, 30)
        else:
            # Position the button near the left border of the window
            self.toggle_button.move(0, 30)

    def createTaskbar(self):
        # Create a toolbar for the taskbar
        taskbar = QToolBar("Taskbar", self)
        taskbar.addAction("Menu")
        taskbar.addAction("Edit")
        taskbar.addAction("Tools")
        taskbar.setMovable(False)
        self.addToolBar(taskbar)

    def createStatusbar(self):
        # Create a status bar at the bottom of the window
        status_bar = QStatusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                border-top : 1px solid #cccccc;
            }
        """)

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

        self.setStatusBar(status_bar)
        status_bar.addWidget(button1)
        status_bar.showMessage(f"\t\t\tReady")

    def toggleLeftSidebar(self):
        if self.left_sidebar.isVisible():
            self.left_sidebar.hide()
        else:
            self.left_sidebar.show()
        
        # Update the position of the toggle button
        self.updateToggleButtonPosition()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateToggleButtonPosition()

# Application setup
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
