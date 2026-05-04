from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QIntValidator
import json

PLOT_DIRECTORY = 'Out\\Plots'


class QPlotly(QWidget):
    def __init__(self):
        super().__init__()

        self.view = QWebEngineView()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        self.option_layout = QHBoxLayout()

        self.save_button = QPushButton('Save Fig')
        self.save_button.clicked.connect(self.save_fig)
        self.option_layout.addWidget(self.save_button)

        validator = QIntValidator()
        self.option_layout.addWidget(QLabel('Name:'))
        self.line_edit_name = QLineEdit()
        self.option_layout.addWidget(self.line_edit_name)

        self.option_layout.addWidget(QLabel('Width:'))
        self.line_edit_width = QLineEdit()
        self.line_edit_width.setText('1920')
        self.option_layout.addWidget(self.line_edit_width)
        self.line_edit_width.setValidator(validator)

        self.option_layout.addWidget(QLabel('Height:'))
        self.line_edit_height= QLineEdit()
        self.line_edit_height.setText('1080')
        self.option_layout.addWidget(self.line_edit_height)
        self.line_edit_height.setValidator(validator)

        layout.addLayout(self.option_layout)

        # blank comment

        self.filename = 'fig'

        self.fig = None

        self._ready = False
        self._init_page()

    def _init_page(self):
        html = """
        <html style="height:100%; width:100%;">
        <head>
            <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
        </head>

        <body style="margin:0; padding:0; overflow:hidden; height:100%;">
            <div id="plot" style="width:100%; height:100%;"></div>

            <script>
                window._plot_initialized = false;

                window.updatePlot = function(fig) {
                    fig.layout.autosize = true;

                    if (!window._plot_initialized) {
                        Plotly.newPlot(
                            'plot',
                            fig.data,
                            fig.layout,
                            {responsive: true}
                        );
                        window._plot_initialized = true;
                    } else {
                        Plotly.react(
                            'plot',
                            fig.data,
                            fig.layout,
                            {responsive: true}
                        );
                    }
                };

                // 🔥 Force resize when window changes
                window.addEventListener('resize', function() {
                    var plot = document.getElementById('plot');
                    if (plot) {
                        Plotly.Plots.resize(plot);
                    }
                });
            </script>
        </body>
        </html>
        """

        self.view.setHtml(html)
        self.view.loadFinished.connect(self._on_load)

    def _on_load(self):
        self._ready = True

    def update_fig(self, fig):
        if not self._ready:
            return
        
        self.fig = fig

        # 🔥 ensure layout is resizable from Python side too
        fig.update_layout(
            autosize=True,
            margin=dict(l=0, r=0, t=30, b=30)
        )

        fig_json = fig.to_json()

        js = f"""
        window.updatePlot(JSON.parse(`{fig_json}`));
        """

        self.view.page().runJavaScript(js)

    def save_fig(self):
        filename = PLOT_DIRECTORY + self.filename + '.png'
        print(f'Saving {filename}...')
        self.fig.update_layout(font=dict(size=24))
        self.fig.update_layout(margin=dict(t=100, l=100, r=100, b=100))
        
        with open(filename + ".json", "w") as f:
            json.dump(self.fig.to_dict(), f)

        width = int(self.line_edit_width.text())
        height = int(self.line_edit_height.text())

        self.fig.write_image(filename, height=height, width=width)

        import os
        os.startfile(filename)
