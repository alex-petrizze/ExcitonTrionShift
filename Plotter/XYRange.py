from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QTextEdit
from .AxisRange import AxisRange

class XYRange(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.x_range = AxisRange('X')
        self.y_range = AxisRange('Y')

        self.layout.addWidget(self.x_range)
        self.layout.addWidget(self.y_range)

        self.setLayout(self.layout)

    def get_bounds(self):
        x_range = [self.x_range.low, self.x_range.high]
        y_range = [self.y_range.low, self.y_range.high]

        if None in x_range:
            x_range = None
        if None in y_range:
            y_range = None

        return x_range, y_range


        