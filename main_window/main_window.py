import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from main_widget import MainWidget
from .main_window_geometry_manager import MainWindowGeometryManager


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app: QApplication = app
        self.setWindowTitle("Juggle Log")

        self.geometry_manager = MainWindowGeometryManager(self)
        self.geometry_manager.set_geometry()

        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

