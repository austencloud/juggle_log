from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
from .throw_buttons_widget import ThrowButtonsWidget

if TYPE_CHECKING:
    from .control_panel import ControlPanel


class PatternLengthInputWidget(QWidget):
    PATTERN_LENGTH_LABEL = "Pattern Length:"

    def __init__(self, control_panel: "ControlPanel"):
        super().__init__(control_panel)
        self.control_panel = control_panel
        self.main_widget = control_panel.main_widget
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        self.length_label = QLabel(self.PATTERN_LENGTH_LABEL)
        self.length_input = QSpinBox(self)
        self.length_input.setRange(1, 10)
        self.length_input.setValue(3)

        layout.addWidget(self.length_label)
        layout.addWidget(self.length_input)
        layout.addStretch()

        self.setLayout(layout)

    def get_pattern_length(self):
        return self.length_input.value()

    def resize_pattern_length_input_widget(self):
        # set the font size of the label and the input text
        font_size = self.main_widget.width() // 60
        font = self.length_label.font()
        font.setPointSize(font_size)
        self.length_label.setFont(font)
        self.length_input.setFont(font)
