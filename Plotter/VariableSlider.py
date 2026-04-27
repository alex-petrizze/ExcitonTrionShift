from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QComboBox, QWidget, QPushButton, QSlider, QLabel
from PySide6.QtCore import Qt
import numpy as np

class VariableSlider(QWidget):
    def __init__(self, label='Variable Slider', slider_array=np.arange(0, 100)):
        super().__init__()

        self.layout = QHBoxLayout()

        self.slider_array = slider_array

        self.label = QLabel(text=label)
        self.layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(slider_array) - 1)
        self.slider.setValue(0)
        self.layout.addWidget(self.slider)

        self.display_label = QLabel()
        self.layout.addWidget(self.display_label)

        self.setLayout(self.layout)

        self.slider.valueChanged.connect(self.update_label)

    def get_value(self):
        i = self.slider.value()
        return self.slider_array[i]
    
    def update_label(self):
        value = self.get_value()
        self.display_label.setText(f'{value:0.3f}')