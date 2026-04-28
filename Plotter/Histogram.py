from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QTabWidget, QWidget, QPushButton
from .QPlotly import QPlotly
from .DataComboBox import DataComboBox
from .AxisParameter import AxisParameter
from .PlotFunctions import histogram
from .DataLoader import load_data
from .AxisRange import AxisRange

class Histogram(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.plot = QPlotly()
        self.layout.addWidget(self.plot, stretch=5)

        self.options_layout = QVBoxLayout()

        self.data_combo_box = DataComboBox()
        self.data_combo_box.on_change(self.load_data)
        self.options_layout.addWidget(self.data_combo_box)
        
        self.parameter_widget = AxisParameter('Parameter:')
        self.options_layout.addWidget(self.parameter_widget)

        self.x_range = AxisRange()
        self.options_layout.addWidget(self.x_range)

        self.update_plot_button = QPushButton('Plot')
        self.update_plot_button.clicked.connect(self.update_plot)
        self.options_layout.addWidget(self.update_plot_button)
        
        self.layout.addLayout(self.options_layout, stretch=1)

        self.setLayout(self.layout)

        self.load_data()

    def update_plot(self):
        parameter = self.parameter_widget.value()

        low = self.x_range.low
        high = self.x_range.high

        if not None in [low, high]:
            plotted_df = self.df[(self.df[parameter] <= high) & (self.df[parameter] > low)]
        else:
            plotted_df = self.df

        fig = histogram(plotted_df, parameter)
        self.plot.update_fig(fig)


    def load_data(self):
        name = self.data_combo_box.value
        self.df = load_data(name)
        parameters = self.df.columns
        self.parameter_widget.add_items(parameters)