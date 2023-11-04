import sys
import mne
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QColor
import pyqtgraph as pg
from layout import Ui_MainWindow



class EEGViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  

        #browse
        self.ui.browseButton.clicked.connect(self.load_and_plot_data)
        self.ui.filterButton.clicked.connect(self.filter_signals)
        self.filtered_data =None
        self.data = None

        self.default_colors = [
                    QColor(255, 0, 0),  # Red
                       QColor(0, 255, 0),  # Green
                       QColor(0, 0, 255),  # Blue
                       QColor(255, 255,0)]  # Magenta

        
    def load_and_plot_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Open TXT File", "", "TXT Files (*.txt);;All Files (*)", options=options)

        if file_name:
            self.ui.graph1.clear()
            df = pd.read_csv(file_name, sep=', ', usecols=[1, 2, 3, 4])  # Load specific columns from a tab-separated TXT file

            for i, column in enumerate(df.columns):
                color = self.default_colors[i % len(self.default_colors)]  # Use default colors in a loop
                pen = pg.mkPen(color=color)

                self.ui.graph1.plot(df.index, df[column] + 90 * i, name=f'Signal {column}', pen=pen)
                self.ui.graph1.autoRange()

                # Uncomment the next line if you want to set a specific Y-range
                # self.ui.graph1.getViewBox().setYRange(3500, 6000)

            self.data = df

    def filter_signals(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_name:
            df = pd.read_csv(file_name, usecols=[1, 2, 3, 4])

            
            self.ui.graph2.clear()

            for i, column in enumerate(df.columns):
                color = self.default_colors[i % len(self.default_colors)]  # Use default colors in a loop
                pen = pg.mkPen(color=color)

                self.ui.graph2.plot(df.index, df[column] + 90 * i, name=f'Signal {column}', pen=pen)
                self.ui.graph2.autoRange()
                # self.ui.graph2.getViewBox().setYRange(3500, 6000)

            self.filtered_data = df


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EEGViewer()
    window.setWindowTitle("EEG Viewer")
    window.resize(1250,900)
    window.show()
    sys.exit(app.exec_())