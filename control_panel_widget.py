from typing import TYPE_CHECKING
from pattern_generator import PatternGenerator
from progress_tracker import ProgressTracker
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QMainWindow,
    QSizePolicy,
    QGridLayout,
    QHeaderView,
)


if TYPE_CHECKING:
    from main import MainWindow
    from main_widget import MainWidget


class ControlPanelWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.selected_throws = set()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Throw Buttons
        layout.addLayout(self.create_throw_buttons())

        # Pattern length input
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Pattern Length:"))
        self.length_input = QSpinBox(self)
        self.length_input.setRange(1, 10)
        self.length_input.setValue(3)
        length_layout.addWidget(self.length_input)
        length_layout.addStretch()
        layout.addLayout(length_layout)

        self.setLayout(layout)

    def create_throw_buttons(self):
        # Create a grid layout
        buttons_layout = QGridLayout()

        # Define the throws
        throws = ["S", "D", "L", "F", "B", "P", "Usl", "Uol"]

        # Add buttons to the grid layout with 4 columns
        for index, throw in enumerate(throws):
            button = QPushButton(throw, self)
            button.setCheckable(True)
            button.clicked.connect(self.update_selected_throws)
            row = index // 4
            col = index % 4
            buttons_layout.addWidget(button, row, col)

        return buttons_layout

    def update_selected_throws(self):
        sender = self.sender()
        throw = sender.text()

        if sender.isChecked():
            self.selected_throws.add(throw)
        else:
            self.selected_throws.discard(throw)

        self.main_widget.pattern_table.update_pattern_table(
            self.get_selected_throws(), self.get_pattern_length()
        )

    def get_selected_throws(self):
        return self.selected_throws

    def get_pattern_length(self):
        return self.length_input.value()
