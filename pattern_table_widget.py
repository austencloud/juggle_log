from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QSpinBox, QHeaderView

if TYPE_CHECKING:
    from main_widget import MainWidget


class PatternTable(QTableWidget):
    COLUMN_HEADERS = ["#", "Pattern", "Max Catches", "Date Completed"]
    DATE_NOT_AVAILABLE = ""
    COMPLETED_COLOR = QColor(144, 238, 144)

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.pattern_generator = self.main_widget.pattern_generator
        self.progress_tracker = self.main_widget.progress_tracker

        self.setup_table()

    def setup_table(self):
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(self.COLUMN_HEADERS)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def update_pattern_table(self, selected_throws, pattern_length):
        self.setRowCount(0)

        if not selected_throws:
            return

        sorted_throws = sorted(selected_throws)
        patterns = self.pattern_generator.generate_patterns(
            sorted_throws, pattern_length
        )
        self.setRowCount(len(patterns))

        for i, pattern in enumerate(patterns, start=1):
            self.add_pattern_row(i, pattern)

    def add_pattern_row(self, row_index, pattern):
        self.add_number_item(row_index)
        self.add_pattern_item(row_index, pattern)
        self.add_spin_box(row_index, pattern)
        self.add_date_item(row_index, pattern)
        self.highlight_completed_pattern(row_index, pattern)

    def add_number_item(self, row_index):
        num_item = QTableWidgetItem(str(row_index))
        num_item.setFlags(num_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_index - 1, 0, num_item)

    def add_pattern_item(self, row_index, pattern):
        pattern_item = QTableWidgetItem(pattern)
        pattern_item.setFlags(pattern_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_index - 1, 1, pattern_item)

    def add_spin_box(self, row_index, pattern):
        spin_box = QSpinBox(self)
        spin_box.setRange(self.progress_tracker.get_max_catches(pattern), 100)
        spin_box.setValue(self.progress_tracker.get_max_catches(pattern))
        spin_box.valueChanged.connect(
            lambda value, p=pattern: self.set_max_catches(p, value)
        )
        self.setCellWidget(row_index - 1, 2, spin_box)

    def add_date_item(self, row_index, pattern):
        date_completed = self.progress_tracker.get_completion_date(pattern)
        date_item = QTableWidgetItem(
            date_completed if date_completed else self.DATE_NOT_AVAILABLE
        )
        date_item.setFlags(date_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.setItem(row_index - 1, 3, date_item)

    def highlight_completed_pattern(self, row_index, pattern):
        if self.progress_tracker.is_completed(pattern):
            for col in [0, 1, 3]:
                self.item(row_index - 1, col).setBackground(self.COMPLETED_COLOR)

    def set_max_catches(self, pattern, value):
        self.progress_tracker.set_max_catches(pattern, value)
        self.update_pattern_table(
            self.main_widget.control_panel.get_selected_throws(),
            self.main_widget.control_panel.get_pattern_length(),
        )
