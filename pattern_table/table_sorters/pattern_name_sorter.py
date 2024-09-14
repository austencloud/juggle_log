from pattern_table.table_sorters.base_table_sorter import BaseTableSorter
from PyQt6.QtCore import Qt


class PatternNameSorter(BaseTableSorter):
    def sort(self, order: Qt.SortOrder):
        """Sort by the pattern (alphabetically)."""
        self.table.sortItems(0, order)
