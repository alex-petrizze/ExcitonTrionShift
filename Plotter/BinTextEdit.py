from PySide6.QtWidgets import QHBoxLayout, QSpinBox, QWidget, QLabel
from PySide6.QtGui import QIntValidator

class BinTextEdit(QWidget):
    def __init__(self, label='N Bins:'):
        super().__init__()

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.layout.addWidget(self.label)
        self.text_edit = QSpinBox()
        self.addWidget(self.text_edit)

        self.setLayout(self.layout)

    def value(self):
        text = self.text_edit.toPlainText()
        if len(text) > 0:
            return int(text)
        else:
            return None
        