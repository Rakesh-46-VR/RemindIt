from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class LogoWithText(QWidget):
    def __init__(self, logo_path: str, text: str, size, parent=None):
        super().__init__(parent)

        # Layout for the custom widget
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_container = QHBoxLayout()
        logo_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the logo
        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap(logo_path))
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(size[0], size[1])
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_container.addWidget(logo_label)
        
        # Add the text
        text_label = QLabel(text, self)
        text_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(logo_container)
        layout.addWidget(text_label)

        # Set the layout
        self.setLayout(layout)

class Logo(QWidget):
    def __init__(self, logo_path: str, size, parent=None):
        super().__init__(parent)

        # Layout for the custom widget
        layout = QVBoxLayout(self)

        # Add the logo
        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap(logo_path))
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(size[0], size[1])
        layout.addWidget(logo_label)

        # Set the layout
        self.setLayout(layout)