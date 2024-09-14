from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSpinBox,
    QGridLayout,
)


if TYPE_CHECKING:
    from main_widget import MainWidget


class ControlPanelWidget(QWidget):
    THROW_BUTTONS = ["S", "D", "L", "F", "B", "P", "Usl", "Uol"]
    PATTERN_LENGTH_LABEL = "Pattern Length:"

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
        length_layout.addWidget(QLabel(self.PATTERN_LENGTH_LABEL))
        self.length_input = QSpinBox(self)
        self.length_input.setRange(1, 10)
        self.length_input.setValue(3)
        length_layout.addWidget(self.length_input)
        length_layout.addStretch()
        layout.addLayout(length_layout)

        self.setLayout(layout)

    def create_throw_buttons(self):
        buttons_layout = QGridLayout()

        for index, throw in enumerate(self.THROW_BUTTONS):
            button = QPushButton(throw, self)
            button.setCheckable(True)
            button.clicked.connect(self.update_selected_throws)
            row = index // 4
            col = index % 4
            buttons_layout.addWidget(button, row, col)

        return buttons_layout

    def update_selected_throws(self):
        sender: QPushButton = self.sender()
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
