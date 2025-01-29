from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication, QScrollArea, QVBoxLayout, QWidget, QLineEdit, QPushButton, QFrame, QLabel, QSpacerItem, QSizePolicy
)
from ui.Button import DragButton

class DragWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setup_ui()
        # Timer for auto-scrolling
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.auto_scroll)
        self.scroll_direction = 0  # -1 for up, 1 for down
        self.setMaximumWidth(600)

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        label = QLabel("Your Daily To-Do List", self)
        label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                margin-bottom: 20px;
            }
        """)
        self.main_layout.addWidget(label)

        # Scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #404040;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(10)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.blayout = QVBoxLayout()
        self.blayout.setSpacing(8)
        self.blayout.setContentsMargins(0, 5, 0, 5)
        self.blayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addLayout(self.blayout)

        # Input area
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setSpacing(10)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Add a new task...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background-color: #1a1a1a;
                border: 1px solid #2c2c2c;
                border-radius: 6px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #404040;
            }
        """)

        self.submit_button = QPushButton("Add Task", self)
        self.submit_button.clicked.connect(self.addTask)
        self.submit_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background-color: #2c2c2c;
                border: none;
                border-radius: 6px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)
        container_layout.addWidget(input_container)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        container_layout.addItem(spacer)

        self.scroll_area.setWidget(container)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        # Placeholder for drag and drop
        self.placeholder = QFrame()
        self.placeholder.setFixedHeight(50)
        self.placeholder.setStyleSheet("""
            QFrame {
                background-color: #2c2c2c;
                border: 2px dashed #505050;
                border-radius: 4px;
                margin: 5px 0;
            }
        """)
        self.placeholder.hide()

        # Tracking variables
        self.dragged_widget = None
        self.last_insert_index = -1

        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
            }
        """)

    def auto_scroll(self):
        """Simplified auto-scroll function"""
        if self.scroll_direction != 0:
            scroll_bar = self.scroll_area.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.value() + (10 * self.scroll_direction))

    def dragEnterEvent(self, e):
        if isinstance(e.source(), DragButton):
            self.dragged_widget = e.source()
            e.accept()
        else:
            e.ignore()

    def find_insert_position(self, pos):
        """Find insertion position with improved stability"""
        # Add hysteresis - only update position if mouse has moved significantly
        HYSTERESIS = 30  # pixels of movement required before position change
        
        # If we have a last position, check if movement is significant
        if hasattr(self, '_last_y') and abs(pos.y() - self._last_y) < HYSTERESIS:
            return self.last_insert_index
        
        self._last_y = pos.y()
        
        # Calculate positions with dead zones
        for i in range(self.blayout.count()):
            widget = self.blayout.itemAt(i).widget()
            if not widget or widget is self.placeholder:
                continue

            widget_pos = widget.mapToGlobal(widget.rect().topLeft())
            widget_pos = self.mapFromGlobal(widget_pos)
            widget_height = widget.height()
            
            # Create three zones: top (30%), middle (40%), bottom (30%)
            top_zone = widget_pos.y() + (widget_height * 0.3)
            bottom_zone = widget_pos.y() + (widget_height * 0.7)
            
            if pos.y() < top_zone:
                return i
            elif pos.y() < bottom_zone:
                # Middle zone - maintain current position
                return self.last_insert_index if self.last_insert_index != -1 else i

        return self.blayout.count()

    def dragMoveEvent(self, e):
        if not self.dragged_widget:
            return

        pos = e.position()
        source_index = self.blayout.indexOf(self.dragged_widget)
        insert_index = self.find_insert_position(pos)

        # Handle auto-scrolling
        self.handle_auto_scroll(pos.y())

        # Don't update if we're in the same position
        if insert_index == self.last_insert_index and self.placeholder.isVisible():
            e.accept()
            return

        # Always remove placeholder before inserting at new position
        if self.placeholder.parent():
            self.blayout.removeWidget(self.placeholder)

        # Adjust insert index if needed
        if insert_index > source_index:
            insert_index -= 1

        self.blayout.insertWidget(insert_index, self.placeholder)
        self.placeholder.show()

        self.last_insert_index = insert_index
        e.accept()

    def handle_auto_scroll(self, y_pos):
        """Optimized auto-scroll detection"""
        threshold = 40
        
        # Determine scroll direction
        if y_pos < threshold:
            self.scroll_direction = -1
        elif y_pos > self.height() - threshold:
            self.scroll_direction = 1
        else:
            self.scroll_direction = 0

        # Simplified timer management
        if self.scroll_direction != 0:
            if not self.scroll_timer.isActive():
                self.scroll_timer.start(30)
        else:
            self.scroll_timer.stop()

    def dropEvent(self, e):
        if not isinstance(e.source(), DragButton):
            e.ignore()
            return

        source_widget = e.source()
        source_index = self.blayout.indexOf(source_widget)
        target_index = self.blayout.indexOf(self.placeholder)

        if source_index == -1 or target_index == -1:
            self.dragLeaveEvent(e)
            e.ignore()
            return

        self.blayout.removeWidget(self.placeholder)
        self.placeholder.hide()
        self.blayout.removeWidget(source_widget)

        if target_index > source_index:
            target_index -= 1

        self.blayout.insertWidget(target_index, source_widget)

        # Stop scrolling when dropping
        self.scroll_direction = 0
        self.scroll_timer.stop()

        self.dragged_widget = None
        self.last_insert_index = -1
        if hasattr(self, '_last_y'):
            del self._last_y
        e.accept()

    def dragLeaveEvent(self, e):
        """
        Handle drag leave event without depending on position
        """
        # Simply clean up the placeholder
        if self.placeholder.parent():
            self.blayout.removeWidget(self.placeholder)
        self.placeholder.hide()
        self.last_insert_index = -1
        if hasattr(self, '_last_y'):
            del self._last_y
        e.accept()

    def addTask(self):
        text = self.input_field.text()
        if text.strip():
            btn = DragButton(text)
            self.blayout.addWidget(btn)
            self.input_field.clear()

if __name__ == "__main__":
    app = QApplication([])
    w = DragWidget()
    w.setWindowTitle("To-Do List")
    w.resize(400, 600)
    w.show()
    app.exec()