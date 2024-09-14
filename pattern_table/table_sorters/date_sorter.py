from datetime import datetime
from pattern_table.table_sorters.base_table_sorter import BaseTableSorter
from PyQt6.QtCore import Qt


class DateSorter(BaseTableSorter):
    def sort(self, order: Qt.SortOrder):
        """Sort by date (most recent to least recent)."""
        self.table.setSortingEnabled(False)

        rows = []
        for row in range(self.table.rowCount()):
            date_item = self.table.item(row, 2)
            date_str = date_item.text()
            if date_str != self.table.DATE_NOT_AVAILABLE:
                try:
                    parsed_date = datetime.strptime(date_str, "%m-%d-%Y")
                    rows.append((parsed_date, row))
                except ValueError:
                    rows.append((None, row))
            else:
                rows.append((None, row))

        rows.sort(
            key=lambda x: (x[0] is None, x[0]),
            reverse=(order == Qt.SortOrder.DescendingOrder),
        )

        for i, (_, row_index) in enumerate(rows):
            self.table.insertRow(i)
            for col in range(self.table.columnCount()):
                self.table.setItem(i, col, self.table.takeItem(row_index + 1, col))
                widget = self.table.cellWidget(row_index + 1, col)
                if widget:
                    self.table.setCellWidget(i, col, widget)

        self.table.setSortingEnabled(True)
