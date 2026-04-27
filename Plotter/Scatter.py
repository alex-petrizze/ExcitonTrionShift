from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QWidget
from .QPlotly import QPlotly
from .DataComboBox import DataComboBox
from .DataLoader import load_data
from .AxisParameter import AxisParameter
from .XYRange import XYRange
from PetrizzeTheme import petrizze_template_go
from .PlotFunctions import quad_plot


petrizze_template_go()

import plotly.graph_objects as go

class Scatter(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.plot = QPlotly()
        self.layout.addWidget(self.plot, stretch=5)

        self.options_layout = QVBoxLayout()

        self.data_combo_box = DataComboBox()
        self.data_combo_box.on_change(self.load_data)
        self.options_layout.addWidget(self.data_combo_box)

        self.x_parameter = AxisParameter('X Axis:')
        self.y_parameter = AxisParameter('Y Axis:')
        self.options_layout.addWidget(self.x_parameter)
        self.options_layout.addWidget(self.y_parameter)

        self.xy_range = XYRange()
        self.options_layout.addWidget(self.xy_range)

        self.plot_button = QPushButton(text='Plot')
        self.plot_button.clicked.connect(self.update_plot)
        self.options_layout.addWidget(self.plot_button)

        self.layout.addLayout(self.options_layout, stretch=1)

        self.setLayout(self.layout)

        self.load_data()
    
    def load_data(self):
        name = self.data_combo_box.value
        self.df = load_data(name)
        parameters = self.df.columns
        self.x_parameter.add_items(parameters)
        self.y_parameter.add_items(parameters)

    def update_plot(self):
        
        x_range, y_range = self.xy_range.get_bounds()

        fig = quad_plot(self.df, 
                        parameter_x=self.x_parameter.value(),
                        parameter_y=self.y_parameter.value(),
                        x_range=x_range,
                        y_range=y_range)

        self.plot.update_fig(fig)