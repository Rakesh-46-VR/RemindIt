from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout

class OrderableList(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
          
        label = QLabel()
        label.setText(text)
        
        hbox = QVBoxLayout()
        hbox.addWidget(label)

        self.setLayout(hbox)
