import re
from PyQt6.QtCore import QMimeData, Qt
from PyQt6.QtGui import QDrag, QPixmap, QIcon
from PyQt6.QtWidgets import (
    QPushButton, QDialog, QVBoxLayout, QLabel, QLineEdit, QTimeEdit, QDialogButtonBox, QSizePolicy, QApplication, QHBoxLayout
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
                background-color: #1e1e1e;
                color: white;
                padding: 12px;
                border-radius: 6px;
                min-width: 550px;
                max-width: 550px;
                text-align: left;
                border: 1px solid #2c2c2c;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border: 1px solid #505050;
            }
        """)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.drag_start_position = None

    def updateText(self):
        """ Update the button text to display the title, description, and time. """
        self.setText(f"📌 {self.title}\n📝 {self.description}\n⏰ {self.time}")

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.openEditDialog()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position()
        super().mousePressEvent(event)

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
        self.show() 

    def openEditDialog(self):
        """ Opens a dialog box to edit task details. """
        dialog = QDialog(self)
        dialog.setFixedWidth(500)
        dialog.setWindowTitle("Edit Task")
        layout = QVBoxLayout()

        title_label = QLabel("Title:")
        title_input = QLineEdit(self.title)
        layout.addWidget(title_label)
        layout.addWidget(title_input)

        desc_label = QLabel("Description:")
        desc_input = QLineEdit(self.description)
        layout.addWidget(desc_label)
        layout.addWidget(desc_input)

        time_label = QLabel("Scheduled Time:")
        time_input = QTimeEdit()
        time_input.setDisplayFormat("hh:mm AP")
        layout.addWidget(time_label)
        layout.addWidget(time_input)
        
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.setFixedWidth(50)
        save_button.setIcon(QIcon("/home/rakesh/Desktop/Git Hub Projects/RemindIt/public/edit_icon.png"))
        save_button.setStyleSheet("border: none; padding: 6px; background-color: #2e7d32; color: white; border-radius: 4px; margin: 0 5px;")
        button_layout.addWidget(save_button)
        
        delete_button = QPushButton("Delete")
        delete_button.setFixedWidth(50)
        delete_button.setIcon(QIcon("/home/rakesh/Desktop/Git Hub Projects/RemindIt/public/delete_icon.png"))
        delete_button.setStyleSheet("border: none; padding: 6px; background-color: #c62828; color: white; border-radius: 4px; margin: 0 5px;")
        button_layout.addWidget(delete_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setFixedWidth(50)
        cancel_button.setStyleSheet("border: none; padding: 6px; background-color: #616161; color: white; border-radius: 4px; margin: 0 5px;")
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        save_button.clicked.connect(lambda: self.saveChanges(title_input.text(), desc_input.text(), time_input.time().toString("hh:mm AP"), dialog))
        delete_button.clicked.connect(lambda: self.deleteTask(dialog))
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec()

    def saveChanges(self, new_title, new_desc, new_time, dialog):
        """ Save edited details and update button text. """
        self.title = new_title
        self.description = new_desc
        self.time = new_time
        self.updateText()
        dialog.accept()

    def deleteTask(self, dialog):
        """ Deletes the task from the layout. """
        self.deleteLater()
        dialog.accept()