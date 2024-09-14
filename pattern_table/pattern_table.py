from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt

from pattern_table.table_sorters.date_sorter import DateSorter
from pattern_table.table_sorters.max_catches_sorter import MaxCatchesSorter
from pattern_table.pattern_row import PatternRow
from pattern_table.table_sorters.pattern_name_sorter import PatternNameSorter
from pattern_table.pattern_spin_box import PatternSpinBox

if TYPE_CHECKING:
    from main_window.main_widget import MainWidget

from datetime import datetime


class PatternTable(QTableWidget):
    COLUMN_HEADERS = ["Pattern", "Max Catches", "Date"]
    COMPLETED_COLOR = QColor(144, 238, 144)  # Green for completed
    ROW_STRIPE_COLOR = QColor(240, 240, 240)  # Alternating row color (grayish)
    DATE_NOT_AVAILABLE = ""

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.pattern_generator = self.main_widget.pattern_generator
        self.progress_tracker = self.main_widget.progress_tracker

        self.sort_order = [
            Qt.SortOrder.AscendingOrder,
            Qt.SortOrder.AscendingOrder,
            Qt.SortOrder.AscendingOrder,
        ]
        self.sorting_enabled = True

        # Initialize sorters
        self.pattern_name_sorter = PatternNameSorter(self)
        self.max_catches_sorter = MaxCatchesSorter(self)
        self.date_sorter = DateSorter(self)

        self.setup_table()

    def setup_table(self):
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(self.COLUMN_HEADERS)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionsClickable(True)
        self.horizontalHeader().sectionClicked.connect(self.handle_header_click)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.verticalHeader().setVisible(False)

        header = self.horizontalHeader()
        header_font = header.font()
        header_font.setBold(False)
        header.setFont(header_font)

        # Set alternating row colors for better readability
        self.setAlternatingRowColors(True)

    def handle_header_click(self, logical_index):
        """Handle sorting when a header is clicked."""
        if logical_index == 0:  # Pattern Column
            self.pattern_name_sorter.sort(self.sort_order[0])
        elif logical_index == 1:  # Max Catches Column
            self.max_catches_sorter.sort(self.sort_order[1])
        elif logical_index == 2:  # Date Column
            self.date_sorter.sort(self.sort_order[2])

        # Toggle the sort order for next time
        self.sort_order[logical_index] = (
            Qt.SortOrder.DescendingOrder
            if self.sort_order[logical_index] == Qt.SortOrder.AscendingOrder
            else Qt.SortOrder.AscendingOrder
        )

    def update_pattern_table(self, selected_throws, pattern_length):
        # Clear the table first
        self.setRowCount(0)
        
        if not selected_throws:
            return

        sorted_throws = sorted(selected_throws)
        patterns = self.pattern_generator.generate_patterns(sorted_throws, pattern_length)
        
        # Set the row count to match the number of patterns
        self.setRowCount(len(patterns))

        # Add each pattern row and highlight if completed
        for i, pattern in enumerate(patterns):
            self.add_pattern_row(i, pattern)

            # Check if the pattern has max catches of 100 and highlight accordingly
            if self.progress_tracker.is_completed(pattern):
                row = PatternRow(self)
                row.highlight_if_completed(i, pattern)
        self.resize_pattern_table()

    def add_pattern_row(self, row_index, pattern):
        row = PatternRow(self)
        row.add_row_items(row_index, pattern)
        row.highlight_if_completed(row_index, pattern)

        # Apply alternating row colors
        if row_index % 2 == 0:
            for col in range(self.columnCount()):
                item = self.item(row_index, col)
                if item:
                    item.setBackground(self.ROW_STRIPE_COLOR)

    def remove_highlight(self, row_index):
        """Remove the green highlight from a row if it no longer meets the criteria."""
        for col in range(self.columnCount()):
            item = self.item(row_index, col)
            if item:
                if row_index % 2 == 0:
                    item.setBackground(self.ROW_STRIPE_COLOR)  # Even row: stripe color
                else:
                    item.setBackground(Qt.GlobalColor.white)  # Odd row: white background

    def remove_date_item(self, pattern):
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == pattern:
                date_item = self.item(row, 2)
                if date_item:
                    self.removeCellWidget(row, 2)
                    self.takeItem(row, 2)

    def update_completion_date(self, pattern):
        # Locate the row based on the pattern
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == pattern:
                date_completed = self.progress_tracker.get_completion_date(pattern)
                if date_completed:
                    date_item = QTableWidgetItem(date_completed)
                    date_item.setFlags(date_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
                    self.setItem(row, 2, date_item)
                break
        # Update it in the progress tracker too
        self.progress_tracker.update_completion_date(pattern)

    def resize_pattern_table(self):
        # Set the font size of all the items in each row and the spinbox font to be relative to the main widget's size
        font = self.main_widget.font()
        font.setPointSize(self.main_widget.width() // 50)
        self.setFont(font)

        # Calculate the appropriate row height based on the font size
        font_metrics = self.fontMetrics()
        padding = (
            self.main_widget.width() // 150
        )
        row_height = font_metrics.height() + padding  # Adding some padding

        for row in range(self.rowCount()):
            self.setRowHeight(row, row_height)
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item:
                    item.setFont(font)
                widget = self.cellWidget(row, col)
                if widget:
                    widget.setFont(font)

        # Resize the header too
        header = self.horizontalHeader()
        header_font = header.font()
        header_font.setPointSize(self.main_widget.width() // 50)
        header_font.setBold(False)  # Ensure header is not bold
        header.setFont(header_font)

