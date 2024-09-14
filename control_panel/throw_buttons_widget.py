from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout

if TYPE_CHECKING:
    from control_panel import ControlPanel


class ThrowButtonsWidget(QWidget):
    THROW_BUTTONS = [
        ("S", "Single"),
        ("D", "Double"),
        ("L", "Lazy"),
        ("F", "Flat"),
        ("B", "Behind the back"),
        ("P", "Penguin"),
        ("O", "Over the top"),
        ("Od", "Over the top double"),
        ("Us", "Under same leg"),
        ("Uo", "Under opposite leg"),
    ]

    def __init__(self, control_panel: "ControlPanel"):
        super().__init__(control_panel)
        self.control_panel = control_panel
        self.main_widget = control_panel.main_widget
        self.selected_throws = set()
        self.buttons: dict[str, QPushButton] = {}
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        for index, (throw, tooltip) in enumerate(self.THROW_BUTTONS):
            button = QPushButton(throw, self)
            button.setCheckable(True)
            button.setToolTip(tooltip)
            button.clicked.connect(self.update_selected_throws)
            self.buttons[throw] = button
            row = index // 4
            col = index % 4
            layout.addWidget(button, row, col)

        self.setLayout(layout)

    def update_selected_throws(self):
        sender: QPushButton = self.sender()
        throw = sender.text()

        if sender.isChecked():
            self.selected_throws.add(throw)
        else:
            self.selected_throws.discard(throw)

        self.control_panel.main_widget.pattern_table.update_pattern_table(
            self.get_selected_throws(),
            self.control_panel.pattern_length_input.get_pattern_length(),
        )

    def get_selected_throws(self):
        return self.selected_throws

    def resize_throw_buttons_widget(self):
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(max(12, self.main_widget.width() // 60))
            button.setFont(font)
