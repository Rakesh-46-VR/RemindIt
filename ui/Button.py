from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import (
    QPushButton, QDialog, QVBoxLayout, QLabel, QLineEdit, QTimeEdit, QDialogButtonBox, QSizePolicy, QApplication
)

class DragButton(QPushButton):
    def __init__(self, title, description, time, parent=None):
        super().__init__(parent)
        
        self.title = title
        self.description = description
        self.time = time
        
        self.updateText()

        self.setStyleSheet("""
            QPushButton {
                background-color: #121212;
                color: white;
                padding: 12px;
                border-radius: 6px;
                min-width: 550px;
                max-width: 550px;
                text-align: left;
                border: 1px solid #2c2c2c;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
                border: 1px solid #404040;
            }
        """)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.drag_start_position = None

    def updateText(self):
        """ Update the button text to display the title, description, and time. """
        self.setText(f"📌 {self.title}\n📝 {self.description}\n⏰ {self.time}")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position()

        elif event.button() == Qt.MouseButton.RightButton:
            self.openEditDialog()  # Open edit dialog on right-click

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if not self.drag_start_position:
            return

        if (event.position() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.title)  # Send title in drag operation
        drag.setMimeData(mime_data)

        # Create a semi-transparent preview
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.position().toPoint())

        self.hide()  # Hide the button while dragging
        result = drag.exec(Qt.DropAction.MoveAction)
        self.show()  # Show the button after drop

    def openEditDialog(self):
        """ Opens a dialog box to edit task details. """
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Task")
        layout = QVBoxLayout()

        # Title field
        title_label = QLabel("Title:")
        title_input = QLineEdit(self.title)
        layout.addWidget(title_label)
        layout.addWidget(title_input)

        # Description field
        desc_label = QLabel("Description:")
        desc_input = QLineEdit(self.description)
        layout.addWidget(desc_label)
        layout.addWidget(desc_input)

        # Scheduled time field
        time_label = QLabel("Scheduled Time:")
        time_input = QTimeEdit()
        time_input.setDisplayFormat("hh:mm AP")  # 12-hour format
        layout.addWidget(time_label)
        layout.addWidget(time_input)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        # Handle actions
        button_box.accepted.connect(lambda: self.saveChanges(title_input.text(), desc_input.text(), time_input.time().toString("hh:mm AP"), dialog))
        button_box.rejected.connect(dialog.reject)

        dialog.exec()

    def saveChanges(self, new_title, new_desc, new_time, dialog):
        """ Save edited details and update button text. """
        self.title = new_title
        self.description = new_desc
        self.time = new_time
        self.updateText()
        dialog.accept()
