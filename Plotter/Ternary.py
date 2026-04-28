from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QTabWidget, QWidget, QPushButton
from .QPlotly import QPlotly
from .DataComboBox import DataComboBox
from .AxisParameter import AxisParameter
from .PlotFunctions import ternary
from .DataLoader import load_data
from .AxisRange import AxisRange
from .BinTextEdit import BinTextEdit

class Ternary(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.plot = QPlotly()
        self.layout.addWidget(self.plot, stretch=5)

        self.options_layout = QVBoxLayout()

        self.data_combo_box = DataComboBox()
        self.data_combo_box.on_change(self.load_data)
        self.options_layout.addWidget(self.data_combo_box)
        
        self.parameter_widget_x = AxisParameter('X Parameter:')
        self.options_layout.addWidget(self.parameter_widget_x)
        self.parameter_widget_y = AxisParameter('T Parameter:')
        self.options_layout.addWidget(self.parameter_widget_y)
        self.parameter_widget_z = AxisParameter('Z Parameter:')
        self.options_layout.addWidget(self.parameter_widget_z)

        self.x_range = AxisRange('X:')
        self.options_layout.addWidget(self.x_range)
        self.y_range = AxisRange('Y:')
        self.options_layout.addWidget(self.y_range)
        self.z_range = AxisRange('Z:')
        self.options_layout.addWidget(self.z_range)

        self.update_plot_button = QPushButton('Plot')
        self.update_plot_button.clicked.connect(self.update_plot)
        self.options_layout.addWidget(self.update_plot_button)
        
        self.layout.addLayout(self.options_layout, stretch=1)

        self.setLayout(self.layout)

        self.load_data()

    @staticmethod
    def filter_range_data(df, parameter, ran):
        low = ran.low
        high = ran.high

        if not None in [low, high]:
            plotted_df = df[(df[parameter] <= high) & (df[parameter] > low)]
        else:
            plotted_df = df
        return plotted_df

    def update_plot(self):
        parameter_x = self.parameter_widget_x.value()
        parameter_y = self.parameter_widget_y.value()
        parameter_z= self.parameter_widget_z.value()

        plotted_df = self.df
        plotted_df = self.filter_range_data(plotted_df, parameter_x, self.x_range)
        plotted_df = self.filter_range_data(plotted_df, parameter_y, self.y_range)
        plotted_df = self.filter_range_data(plotted_df, parameter_z, self.z_range)

        fig = ternary(plotted_df, 
                        parameter_x,
                        parameter_y,
                        parameter_z)
        
        self.plot.update_fig(fig)


    def load_data(self):
        name = self.data_combo_box.value
        self.df = load_data(name)
        parameters = self.df.columns

        self.parameter_widget_x.add_items(parameters)
        self.parameter_widget_y.add_items(parameters)
        self.parameter_widget_z.add_items(parameters)