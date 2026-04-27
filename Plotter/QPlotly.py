from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtWebEngineWidgets import QWebEngineView
import json

PLOT_DIRECTORY = 'Out\\Plots'


class QPlotly(QWidget):
    def __init__(self):
        super().__init__()

        self.view = QWebEngineView()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        self.save_button = QPushButton('Save Fig')
        self.save_button.clicked.connect(self.save_fig)
        layout.addWidget(self.save_button)

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
        self.fig.write_image(filename, height=1080, width=1080)

        import os
        os.startfile(filename)
