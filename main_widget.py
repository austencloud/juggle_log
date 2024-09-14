from typing import TYPE_CHECKING
from control_panel.control_panel import ControlPanel
from utils.pattern_generator import PatternGenerator
from pattern_table_widget import PatternTable
from utils.progress_tracker import ProgressTracker
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMainWindow

if TYPE_CHECKING:
    from main_window.main_window import MainWindow


class MainWidget(QWidget):
    def __init__(self, main_window: "MainWindow"):
        super().__init__()
        self.main_window = main_window
        self.pattern_generator = PatternGenerator(self)
        self.progress_tracker = ProgressTracker(self)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.pattern_table = PatternTable(self)
        self.control_panel = ControlPanel(self)
        layout.addWidget(self.pattern_table)
        layout.addWidget(self.control_panel)
        self.setLayout(layout)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self.main_window, event)
        self.control_panel.resize_control_panel_widget()
