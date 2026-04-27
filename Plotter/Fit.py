from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QTabWidget, QWidget
from .QPlotly import QPlotly


class Fit(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.plot = QPlotly()
        self.layout.addWidget(self.plot)

        self.options_layout = QVBoxLayout()
        
        self.layout.addLayout(self.options_layout)

        self.setLayout(self.layout)