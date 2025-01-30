from PyQt6.QtCore import Qt, QTime
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTimeEdit, QLabel
)
import re


time_pattern = r"@([0]?[1-9]|1[0-2]):([0-5]?[0-9])\s([APap][Mm])"

class DragWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # "+" button with label for adding new task
        self.add_task_container = QWidget()
        add_task_layout = QHBoxLayout(self.add_task_container)
        add_task_layout.setContentsMargins(0, 5, 0, 5)
        
        add_task_button = QPushButton("+\t\tAdd new task", self)
        add_task_button.setFixedSize(400, 40)
        add_task_button.setStyleSheet(self.button_style())
        add_task_button.clicked.connect(self.toggle_input_visibility)
    
        add_task_layout.addWidget(add_task_button)

        self.main_layout.addWidget(self.add_task_container)

        # Main container for input fields
        self.container = QWidget()
        self.container.setFixedWidth(600)  # Max width for the container
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(0)  # Remove spacing between inputs
        self.container.setVisible(False)  # Initially hidden
        
        # Title input
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Title")
        self.title_input.setFixedHeight(35)  # Smaller height
        self.title_input.setStyleSheet(self.title_style())
        self.container_layout.addWidget(self.title_input)

        # Description input
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Description")
        self.description_input.setFixedHeight(35)
        self.description_input.setStyleSheet(self.input_style())
        self.container_layout.addWidget(self.description_input)

        # Schedule input
        schedule_task_container = QWidget()
        schedule_task_layout = QHBoxLayout(schedule_task_container)
        schedule_task_layout.setContentsMargins(0, 5, 0, 0)  # Reduce margins

        # Schedule input
        self.schedule_input = QTimeEdit(self)
        self.schedule_input.setDisplayFormat("hh:mm AP")
        self.schedule_input.setFixedWidth(100)  # Limited width
        self.schedule_input.setFixedHeight(35)
        self.schedule_input.setStyleSheet(self.schedule_style())
        schedule_task_layout.addWidget(self.schedule_input, alignment=Qt.AlignmentFlag.AlignLeft)

        # Submit button
        self.submit_button = QPushButton("Add Task", self)
        self.submit_button.clicked.connect(self.addTask)
        self.submit_button.setFixedHeight(35)
        self.submit_button.setStyleSheet(self.button_style())
        schedule_task_layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.container_layout.addWidget(schedule_task_container)

        self.main_layout.addWidget(self.container)
        self.setLayout(self.main_layout)

    def toggle_input_visibility(self):
        """Toggle visibility of the input fields when the + button is clicked."""
        self.container.setVisible(True)
        self.add_task_container.setVisible(False)

    def title_style(self):
        return """
            QLineEdit {
                background-color: #1a1a1a;
                color: white;
                font-size: 16px;
                font:bold;
                border: none;
                padding: 8px;
            }
        """

    def input_style(self):
        return """
            QLineEdit {
                background-color: #1a1a1a;
                color: white;
                font-size: 14px;
                border: none;
                padding: 8px;
            }
        """

    def schedule_style(self):
        return """
            QTimeEdit {
                background-color: #1a1a1a;
                color: white;
                font-size: 14px;
                padding: 5px;
                border: none;
            }
            QTimeEdit::up-button, QTimeEdit::down-button {
                width: 20px;
                color: #ffffff;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                padding : 10px;
                background-color: #1a1a1a;
                border: none;
                color: white;
                font-weight: bold;
            }
        """

    def on_text_changed(self, text):
        """Triggered whenever text in the QLineEdit changes."""
        matches = re.findall(time_pattern, text)
        if(matches):

            hours, minutes, am_pm = matches[0]
            hours = int(hours)
            minutes = int(minutes)

            # Convert to 24-hour format
            if am_pm == "AM" or am_pm == "am":
                if hours == 12:
                    hours = 0 
            elif am_pm == "PM" or am_pm == "pm":
                if hours != 12:
                    hours += 12

            time = QTime(hours, minutes)
            self.schedule_input.setTime(time)
        else:
            time = QTime(9, 0)
            self.schedule_input.setTime(time)

    def addTask(self):
        title = self.title_input.text()
        description = self.description_input.text()
        schedule = self.schedule_input.time().toString("hh:mm AP")
        print(f"Title: {title}\nDescription: {description}\nSchedule: {schedule}")

if __name__ == "__main__":
    app = QApplication([])
    w = DragWidget()
    w.setWindowTitle("To-Do List")
    w.show()
    app.exec()
