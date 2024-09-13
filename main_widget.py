from typing import TYPE_CHECKING
from control_panel_widget import ControlPanelWidget
from pattern_generator import PatternGenerator
from pattern_table_widget import PatternTableWidget
from progress_tracker import ProgressTracker
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QMainWindow,
    QSizePolicy,
    QGridLayout, QHeaderView
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

        # Create pattern table
        self.pattern_table = PatternTableWidget(self)

        # Create control panel
        self.control_panel = ControlPanelWidget(self)

        # Add to layout
        layout.addWidget(self.pattern_table)
        layout.addWidget(self.control_panel)

        self.setLayout(layout)




    def resizeEvent(self, event):
        # Adjust font size based on a percentage of the window width
        font = self.font()
        
        # Increase the base size by modifying the divisor (e.g., using a lower divisor results in a larger font)
        font.setPointSize(max(12, self.main_window.width() // 100))  # Adjusted divisor for larger text

        # Resize all the items in the table and all the button font sizes
        for i in range(self.pattern_table.rowCount()):
            for j in range(self.pattern_table.columnCount()):
                item = self.pattern_table.item(i, j)
                if item:
                    item.setFont(font)
                widget = self.pattern_table.cellWidget(i, j)
                if widget:
                    widget.setFont(font)

        # Update button font size as well
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget:
                widget.setFont(font)

        # Call the base class resizeEvent
        QMainWindow.resizeEvent(self.main_window, event)
