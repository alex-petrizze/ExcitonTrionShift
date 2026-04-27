from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QTabWidget, QWidget, QLabel, QComboBox


data_names = ['Gaussian', 'Lorentzian', '5050']

class DataComboBox(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()

        self.label = QLabel('Dataset:')
        self.combo_box = QComboBox()
        self.combo_box.addItems(data_names)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo_box)

        self.setLayout(self.layout)

    @property
    def value(self):
        return self.combo_box.currentText()
    
    def on_change(self, function):
        self.combo_box.currentTextChanged.connect(function)