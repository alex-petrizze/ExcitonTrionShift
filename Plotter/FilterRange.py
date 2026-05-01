from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QTabWidget, QWidget, QPushButton, QLabel
from .QPlotly import QPlotly
from .DataComboBox import DataComboBox
from .AxisParameter import AxisParameter
from .PlotFunctions import histogram
from .DataLoader import load_data
from .AxisRange import AxisRange
from .BinTextEdit import BinTextEdit
from PySide6.QtWidgets import QSizePolicy
import numpy as np

class FilterRange(QWidget):
    def __init__(self, parameter='Parameter'):
        super().__init__()

        self.layout = QHBoxLayout()

        self.parameter = parameter

        self.label = QLabel(parameter)
        self.layout.addWidget(self.label)

        self.parameter_range = AxisRange()
        self.layout.addWidget(self.parameter_range)

        self.delete_button = QPushButton('Delete')
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    def get_filter_info(self):
        low = self.parameter_range.low
        high = self.parameter_range.high

        return {
            'PARAMETER': self.parameter,
            'MIN': low if low is not None else -np.inf,
            'MAX': high if high is not None else np.inf
        }