from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox, QWidget, QPushButton, QSlider, QLabel
from .QPlotly import QPlotly
from .DataComboBox import DataComboBox
from .DataLoader import load_data
from ExcitonFitting.Config import FIT_EXCITON_SHAPE_KEYS, ENERGY_RANGE_B
from .PlotFunctions import fit_plot
from .VariableSlider import VariableSlider

class Fit(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.plot = QPlotly()
        self.layout.addWidget(self.plot, stretch=5)

        self.options_layout = QVBoxLayout()

        self.data_combo_box = DataComboBox()
        self.data_combo_box.on_change(self.load_data)
        self.options_layout.addWidget(self.data_combo_box)

        self.lineshape_combo_box = QComboBox()
        self.lineshape_combo_box.addItems(FIT_EXCITON_SHAPE_KEYS)
        self.options_layout.addWidget(self.lineshape_combo_box)

        self.energy_slider = VariableSlider(label='True T Energy', slider_array=ENERGY_RANGE_B)
        self.options_layout.addWidget(self.energy_slider)

        self.update_plot_button = QPushButton('Plot')
        self.update_plot_button.clicked.connect(self.update_plot)
        self.options_layout.addWidget(self.update_plot_button)
        
        self.layout.addLayout(self.options_layout, stretch=1)

        self.setLayout(self.layout)

        self.load_data()
    
    def get_energy(self):
        i = self.energy_slider.value()
        return ENERGY_RANGE_B[i]

    def update_plot(self):
        fig = fit_plot(self.df, self.lineshape_combo_box.currentText(), self.energy_slider.get_value())
        self.plot.update_fig(fig)

    def load_data(self):
        name = self.data_combo_box.value
        self.df = load_data(name)

        