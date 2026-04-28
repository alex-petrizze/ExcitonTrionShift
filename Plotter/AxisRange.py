from PySide6.QtWidgets import QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QDoubleValidator

class AxisRange(QWidget):
    def __init__(self, label='Range:'):
        super().__init__()
        
        self.label = label

        self.layout = QHBoxLayout()

        self.min_input = QLineEdit()
        self.max_input = QLineEdit()

        validator = QDoubleValidator()
        self.min_input.setValidator(validator)
        self.max_input.setValidator(validator)

        self.layout.addWidget(QLabel(f'{label} Min:'))
        self.layout.addWidget(self.min_input)
        self.layout.addWidget(QLabel(f'{label} Max:'))
        self.layout.addWidget(self.max_input)

        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear)
        self.layout.addWidget(self.clear_button)


        self.setLayout(self.layout)

    def clear(self):
        self.min_input.setText('')
        self.max_input.setText('')

    @property
    def low(self):
        if self.min_input.text() == '':
            return None
        return float(self.min_input.text())

    @property
    def high(self):
        if self.max_input.text() == '':
            return None
        return float(self.max_input.text())

        