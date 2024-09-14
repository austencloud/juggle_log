from pattern_table.table_sorter import TableSorter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem
from pattern_table.pattern_spin_box import PatternSpinBox
from pattern_table.pattern_row import PatternRow  # Import PatternRow


class MaxCatchesSorter(TableSorter):
    def sort(self, order: Qt.SortOrder):
        """Sort by max catches."""
        self.table.setSortingEnabled(False)

        rows = []
        for row in range(self.table.rowCount()):
            spin_box = self.table.cellWidget(row, 1)
            if spin_box is not None:
                pattern_item = self.table.item(row, 0)
                date_item = self.table.item(row, 2)
                rows.append(
                    (
                        spin_box.value(),
                        pattern_item.text(),
                        spin_box,
                        date_item.text(),
                        row,
                    )
                )

        # Sort the rows based on the max catches values
        rows.sort(reverse=(order == Qt.SortOrder.DescendingOrder))

        # Clear the table content and prepare to reinsert rows
        self.table.setRowCount(0)
        self.table.setRowCount(len(rows))

        for new_index, (
            catch_value,
            pattern_text,
            spin_box,
            date_text,
            original_row,
        ) in enumerate(rows):
            # Create and insert a new QTableWidgetItem for pattern
            pattern_item = QTableWidgetItem(pattern_text)
            pattern_item.setFlags(pattern_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(new_index, 0, pattern_item)

            # Create a new PatternRow object
            new_pattern_row = PatternRow(self.table)
            
            # Pass the new row to the PatternSpinBox
            new_spin_box = PatternSpinBox(new_pattern_row, pattern_text)
            new_spin_box.setRange(0, 100)
            new_spin_box.setValue(spin_box.value())
            self.table.setCellWidget(new_index, 1, new_spin_box)

            # Create and insert a new QTableWidgetItem for the date
            date_item = QTableWidgetItem(date_text)
            date_item.setFlags(date_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(new_index, 2, date_item)

            # Highlight row if max catches is 100
            if new_spin_box.value() == 100:
                new_pattern_row.highlight_if_completed(new_index, pattern_text)

        self.table.setSortingEnabled(True)
