from itertools import product
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox, QListWidget

if TYPE_CHECKING:
    from main_window.main_widget import MainWidget


class PatternGenerator:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def generate_patterns(self, throws, length):
        all_patterns = set("".join(p) for p in product(throws, repeat=length))

        unique_patterns = set()
        for pattern in all_patterns:
            if not any(
                pattern[i:] + pattern[:i] in unique_patterns
                for i in range(len(pattern))
            ):
                unique_patterns.add(pattern)
        return sorted(unique_patterns)