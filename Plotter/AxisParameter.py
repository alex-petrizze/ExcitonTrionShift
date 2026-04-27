from PySide6.QtWidgets import QHBoxLayout, QWidget, QLabel, QComboBox

class AxisParameter(QWidget):
    def __init__(self, label='Axis Parameter:'):
        super().__init__()

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.combo_box = QComboBox()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo_box)

        self.setLayout(self.layout)

    def set_text(self, text):
        self.label.setText(text)

    def add_items(self, items):
        self.combo_box.addItems(items)

    def value(self):
        return self.combo_box.currentText()