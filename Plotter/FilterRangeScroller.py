from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QTabWidget, QWidget, QPushButton, QScrollArea
from .QPlotly import QPlotly
from .DataComboBox import DataComboBox
from .AxisParameter import AxisParameter
from .PlotFunctions import histogram
from .DataLoader import load_data
from .AxisRange import AxisRange
from .BinTextEdit import BinTextEdit
from .FilterRange import FilterRange

class FilterRangeScroller(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.parameter_choice = AxisParameter()
        self.layout.addWidget(self.parameter_choice)
        self.add_parameter_button = QPushButton('Add Filter')
        self.add_parameter_button.pressed.connect(self.add_parameter)
        self.layout.addWidget(self.add_parameter_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_container = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_container)
        self.scroll_area.setWidget(self.scroll_container)
        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)

    def add_parameter(self):
        parameter = self.parameter_choice.value()
        
        print(parameter)

        new_filter_range = FilterRange(parameter)
        self.scroll_layout.addWidget(new_filter_range)

        print(self.get_filters)

    def get_filters(self):
        filters = []
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            widget = item.widget()
            
            if widget is not None:
                filters.append(widget.get_filter_info())

        return filters

    