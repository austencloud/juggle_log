from typing import TYPE_CHECKING
from control_panel_widget import ControlPanelWidget
from pattern_generator import PatternGenerator
from pattern_table_widget import PatternTableWidget
from progress_tracker import ProgressTracker
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMainWindow
)

if TYPE_CHECKING:
    from main import MainWindow

class MainWidget(QWidget):
    def __init__(self, main_window: "MainWindow"):
        super().__init__()
        self.main_window = main_window
        self.pattern_generator = PatternGenerator(self)
        self.progress_tracker = ProgressTracker(self)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.pattern_table = PatternTableWidget(self)
        self.control_panel = ControlPanelWidget(self)
        layout.addWidget(self.pattern_table)
        layout.addWidget(self.control_panel)
        self.setLayout(layout)

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(max(12, self.main_window.width() // 100))
        for i in range(self.pattern_table.rowCount()):
            for j in range(self.pattern_table.columnCount()):
                item = self.pattern_table.item(i, j)
                if item:
                    item.setFont(font)
                widget = self.pattern_table.cellWidget(i, j)
                if widget:
                    widget.setFont(font)
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget:
                widget.setFont(font)
        QMainWindow.resizeEvent(self.main_window, event)
