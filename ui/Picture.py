from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from io import BytesIO
import requests

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
    def __init__(self, logo_source: str, size, is_url=False, parent=None):
        super().__init__(parent)

        # Layout for the custom widget
        layout = QVBoxLayout(self)

        # Add the logo
        logo_label = QLabel(self)

        # Load the logo (either from a file path or a URL)
        pixmap = QPixmap()
        if is_url:
            # If the source is a URL, fetch the image data
            response = requests.get(logo_source)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                pixmap.loadFromData(image_data.read())
        else:
            # Otherwise, load from a local file path
            pixmap.load(logo_source)

        # Set the pixmap to the QLabel
        logo_label.setPixmap(pixmap)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(size[0], size[1])
        layout.addWidget(logo_label)

        # Set the layout
        self.setLayout(layout)