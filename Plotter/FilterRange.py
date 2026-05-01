from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QTabWidget, QWidget, QPushButton, QLabel
from .QPlotly import QPlotly
from .DataComboBox import DataComboBox
from .AxisParameter import AxisParameter
from .PlotFunctions import histogram
from .DataLoader import load_data
from .AxisRange import AxisRange
from .BinTextEdit import BinTextEdit

class FilterRange(QWidget):
    def __init__(self, parameter='Parameter'):
        super().__init__()

        self.layout = QHBoxLayout()

        self.parameter_range = AxisRange()
        self.layout.add(self.parameter_range)

        self.setLayout(self.layout)