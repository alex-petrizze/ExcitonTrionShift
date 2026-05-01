from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QTabWidget, QWidget, QPushButton, QScrollArea
from .QPlotly import QPlotly
from .DataComboBox import DataComboBox
from .AxisParameter import AxisParameter
from .PlotFunctions import histogram
from .DataLoader import load_data
from .AxisRange import AxisRange
from .BinTextEdit import BinTextEdit

class FilterRangeScroller(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()


        self.parameter_choice = AxisParameter()
        self.layout.addWidget(self.parameter_choice)
        self.add_parameter_button = QPushButton('Add Filter')
        self.layout.addWidget(self.add_parameter_button)

        self.scroller = QScrollArea()
        self.layout.addWidget(self.scroller)

        self.setLayout(self.layout)

    