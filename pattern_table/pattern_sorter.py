from pattern_table.table_sorter import TableSorter
from PyQt6.QtCore import Qt

class PatternSorter(TableSorter):
    def sort(self, order: Qt.SortOrder):
        """Sort by the pattern (alphabetically)."""
        self.table.sortItems(0, order)
