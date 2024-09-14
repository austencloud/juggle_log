from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from pattern_table.pattern_table import PatternTable


class TableSorter:
    def __init__(self, table: "PatternTable"):
        self.table = table

    def sort(self, order: Qt.SortOrder):
        """Base method for sorting."""
        raise NotImplementedError("Sort method must be implemented by subclasses.")
