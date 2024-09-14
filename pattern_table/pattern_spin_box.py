from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSpinBox

if TYPE_CHECKING:
    from pattern_table.pattern_row import PatternRow


class PatternSpinBox(QSpinBox):
    def __init__(self, row: "PatternRow", pattern: str):
        super().__init__(row.table)
        self.row = row
        self.pattern = pattern
        self.table = row.table
        self.progress_tracker = self.table.progress_tracker

        self.setup_spin_box()

    def setup_spin_box(self):
        self.setRange(0, 100)
        self.setValue(self.progress_tracker.get_max_catches(self.pattern))
        self.valueChanged.connect(self.on_value_changed)

    def on_value_changed(self, value):
        self.progress_tracker.set_max_catches(self.pattern, value)
        self.row.highlight_if_completed(self.row.table.indexAt(self.pos()).row(), self.pattern)
        self.table.sorting_enabled = False  # Disable sorting

