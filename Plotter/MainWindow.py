from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMainWindow, QTabWidget, QWidget
from .Scatter import Scatter
from .Histogram import Histogram
from .Ternary import Ternary
from .Fit import Fit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("My App")

        self.main_layout = QHBoxLayout()
        container = QWidget()
        container.setLayout(self.main_layout)

        self.tabs = QTabWidget()

        self.scatter_widget = Scatter()
        self.tabs.addTab(self.scatter_widget, 'Scatter Plot')

        self.scatter_widget = Histogram()
        self.tabs.addTab(self.scatter_widget, 'Histogram')

        self.scatter_widget = Fit()
        self.tabs.addTab(self.scatter_widget, 'Fit')

        self.main_layout.addWidget(self.tabs)

        self.setCentralWidget(container)