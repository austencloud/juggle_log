from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem
from pattern_table.pattern_spin_box import PatternSpinBox

if TYPE_CHECKING:
    from pattern_table.pattern_table import PatternTable


class PatternRow:
    def __init__(self, table: "PatternTable"):
        self.table = table

    def add_row_items(self, row_index: int, pattern: str):
        self.add_pattern_name(row_index, pattern)
        self.add_spin_box(row_index, pattern)
        self.add_date_item(row_index, pattern)

    def add_pattern_name(self, row_index: int, pattern: str):
        pattern_item = QTableWidgetItem(pattern)
        pattern_item.setFlags(pattern_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_index, 0, pattern_item)

    def add_spin_box(self, row_index: int, pattern: str):
        # Pass the pattern directly to PatternSpinBox
        spin_box = PatternSpinBox(self, pattern)
        self.table.setCellWidget(row_index, 1, spin_box)

    def add_date_item(self, row_index: int, pattern: str):
        date_completed = self.table.progress_tracker.get_completion_date(pattern)
        date_item = QTableWidgetItem(
            date_completed if date_completed else self.table.DATE_NOT_AVAILABLE
        )
        date_item.setFlags(date_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_index, 2, date_item)

    def highlight_if_completed(self, row_index: int, pattern: str):
        """Highlight the row if completed, otherwise remove the highlight."""
        if self.table.progress_tracker.is_completed(pattern):
            for col in [0, 2]:
                item = self.table.item(row_index, col)
                if item:
                    item.setBackground(self.table.COMPLETED_COLOR)
        else:
            # If not completed, remove the highlight and restore the original colors
            self.table.remove_highlight(row_index)
