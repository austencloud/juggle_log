from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox

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

        # Connect the valueChanged signal of the QSpinBox to reload the table
        self.length_input.valueChanged.connect(self.on_pattern_length_changed)

    def get_pattern_length(self):
        return self.length_input.value()

    def on_pattern_length_changed(self):
        """Reload the pattern table when the length changes."""
        selected_throws = self.control_panel.throw_buttons_widget.get_selected_throws()
        pattern_length = self.get_pattern_length()

        # Reload the pattern table with the new pattern length
        self.main_widget.pattern_table.update_pattern_table(selected_throws, pattern_length)

    def resize_pattern_length_input_widget(self):
        # Set the font size of the label and the input text
        font_size = self.main_widget.width() // 60
        font = self.length_label.font()
        font.setPointSize(font_size)
        self.length_label.setFont(font)
        self.length_input.setFont(font)
