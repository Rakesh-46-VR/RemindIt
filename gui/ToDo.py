from PyQt6.QtCore import QMimeData, Qt, QTimer
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import QApplication, QScrollArea, QVBoxLayout, QWidget, QLineEdit, QPushButton, QFrame, QLabel, QSpacerItem, QSizePolicy


class DragButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #121212;
                padding: 5px;
                min-width: 300px;
                max-width: 300px;
            }
        """)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(self.text())
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.setHotSpot(e.position().toPoint())
            drag.exec(Qt.DropAction.MoveAction)


class DragWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Label at the top
        label = QLabel("Your Daily To-Do List", self)
        label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        self.main_layout.addWidget(label)

        # Scroll area containing input, buttons, and draggable layout
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Container widget inside scroll area
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(10)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Draggable buttons layout
        self.blayout = QVBoxLayout()
        self.blayout.setSpacing(5)
        self.blayout.setContentsMargins(0, 5, 0, 5)
        self.blayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        container_layout.addLayout(self.blayout)

        # Input field
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Add a new task...")
        self.input_field.setFixedHeight(30)
        container_layout.addWidget(self.input_field)

        # Submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.addTask)
        container_layout.addWidget(self.submit_button)

        # Spacer at the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        container_layout.addItem(spacer)

        self.scroll_area.setWidget(container)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        # Create placeholder widget for drop target
        self.placeholder = QFrame()
        self.placeholder.setFixedHeight(40)
        self.placeholder.setStyleSheet("""
            QFrame {
                background-color: #2c2c2c;
                border: 2px dashed #505050;
                border-radius: 4px;
                margin: 5px 0;
            }
        """)
        self.placeholder.hide()

        # Track the dragged widget and last position
        self.dragged_widget = None
        self.last_insert_index = -1
        self.drag_start_pos = None

    def dragEnterEvent(self, e):
        if isinstance(e.source(), DragButton):
            self.dragged_widget = e.source()
            self.drag_start_pos = e.position()
            e.accept()
        else:
            e.ignore()

    def find_insert_position(self, pos):
        """Find the insertion position with reduced sensitivity"""
        for i in range(self.blayout.count()):
            widget = self.blayout.itemAt(i).widget()
            if not widget or widget is self.placeholder:
                continue

            widget_pos = widget.mapToGlobal(widget.rect().topLeft())
            widget_pos = self.mapFromGlobal(widget_pos)
            widget_height = widget.height()
            
            # Define a "dead zone" in the middle of each button (40% of height)
            dead_zone_start = widget_pos.y() + (widget_height * 0.3)
            dead_zone_end = widget_pos.y() + (widget_height * 0.7)
            
            if pos.y() < dead_zone_start:
                return i
            elif pos.y() < dead_zone_end:
                # If in dead zone, maintain last position
                return self.last_insert_index

        return self.blayout.count()

    def dragMoveEvent(self, e):
        if not self.dragged_widget:
            return

        pos = e.position()
        insert_index = self.find_insert_position(pos)
        
        # Only update if position has changed
        if insert_index != self.last_insert_index:
            # Remove placeholder from current position
            if self.placeholder.parent():
                self.blayout.removeWidget(self.placeholder)

            # Don't insert at the dragged widget's position
            if insert_index > self.blayout.indexOf(self.dragged_widget):
                insert_index -= 1

            # Insert placeholder at new position
            if insert_index >= 0 and insert_index <= self.blayout.count():
                self.blayout.insertWidget(insert_index, self.placeholder)
                self.last_insert_index = insert_index
                
            self.placeholder.show()

        e.accept()

    def dragLeaveEvent(self, e):
        if self.placeholder.parent():
            self.blayout.removeWidget(self.placeholder)
        self.placeholder.hide()
        self.last_insert_index = -1
        e.accept()

    def dropEvent(self, e):
        if not isinstance(e.source(), DragButton):
            e.ignore()
            return

        source_widget = e.source()
        source_index = self.blayout.indexOf(source_widget)
        target_index = self.blayout.indexOf(self.placeholder)

        # Handle invalid indices
        if source_index == -1 or target_index == -1:
            self.dragLeaveEvent(e)
            e.ignore()
            return

        # Remove placeholder
        self.blayout.removeWidget(self.placeholder)
        self.placeholder.hide()

        # Remove widget from old position
        self.blayout.removeWidget(source_widget)

        # Adjust target index if needed
        if target_index > source_index:
            target_index -= 1

        # Insert at new position
        self.blayout.insertWidget(target_index, source_widget)
        
        # Reset tracking variables
        self.dragged_widget = None
        self.last_insert_index = -1
        self.drag_start_pos = None
        
        e.accept()

    def addTask(self):
        text = self.input_field.text()
        if text.strip():
            btn = DragButton(text)
            btn.setAcceptDrops(True)
            self.blayout.addWidget(btn)
            self.input_field.clear()


if __name__ == "__main__":
    app = QApplication([])
    w = DragWidget()
    w.setWindowTitle("To-Do List")
    w.resize(400, 400)
    w.show()
    app.exec()