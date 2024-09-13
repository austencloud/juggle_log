from typing import TYPE_CHECKING
from typing import TYPE_CHECKING
from pattern_generator import PatternGenerator
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
    QGridLayout,
    QHeaderView,
)


if TYPE_CHECKING:
    from main import MainWindow

if TYPE_CHECKING:
    from main_widget import MainWidget


class PatternTableWidget(QTableWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.pattern_generator = self.main_widget.pattern_generator
        self.progress_tracker = self.main_widget.progress_tracker

        # Setup the table
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(
            ["#", "Pattern", "Max Catches", "Date Completed"]
        )
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def update_pattern_table(self, selected_throws, pattern_length):
        self.setRowCount(0)  # Clear previous rows

        if not selected_throws:
            return

        sorted_throws = sorted(selected_throws)
        patterns = self.pattern_generator.generate_patterns(
            sorted_throws, pattern_length
        )
        self.setRowCount(len(patterns))

        for i, pattern in enumerate(patterns, start=1):
            # Pattern number
            num_item = QTableWidgetItem(str(i))
            num_item.setFlags(num_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.setItem(i - 1, 0, num_item)

            # Pattern text
            pattern_item = QTableWidgetItem(pattern)
            pattern_item.setFlags(pattern_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.setItem(i - 1, 1, pattern_item)

            # Max catches spin box
            spin_box = QSpinBox(self)
            spin_box.setRange(self.progress_tracker.get_max_catches(pattern), 100)
            spin_box.setValue(self.progress_tracker.get_max_catches(pattern))
            spin_box.valueChanged.connect(
                lambda value, p=pattern: self.set_max_catches(p, value)
            )
            self.setCellWidget(i - 1, 2, spin_box)

            # Date completed
            date_completed = self.progress_tracker.get_completion_date(pattern)
            date_item = QTableWidgetItem(date_completed if date_completed else "N/A")
            date_item.setFlags(date_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.setItem(i - 1, 3, date_item)

            # Highlight completed rows
            if self.progress_tracker.is_completed(pattern):
                for col in [0, 1, 3]:
                    self.item(i - 1, col).setBackground(QColor(144, 238, 144))

    def set_max_catches(self, pattern, value):
        self.progress_tracker.set_max_catches(pattern, value)
        self.update_pattern_table(
            self.main_widget.control_panel.get_selected_throws(),
            self.main_widget.control_panel.get_pattern_length(),
        )
