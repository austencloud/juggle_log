from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox

from .pattern_length_input_widget import PatternLengthInputWidget
from .throw_buttons_widget import ThrowButtonsWidget

if TYPE_CHECKING:
    from main_window.main_widget import MainWidget


class ControlPanel(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget

        self.setup_widgets()
        self.setup_layout()

    def setup_widgets(self):
        self.throw_buttons_widget = ThrowButtonsWidget(self)
        self.pattern_length_input = PatternLengthInputWidget(self)

    def setup_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.throw_buttons_widget)
        layout.addWidget(self.pattern_length_input)
        self.setLayout(layout)

    def resize_control_panel_widget(self):
        self.throw_buttons_widget.resize_throw_buttons_widget()
        self.pattern_length_input.resize_pattern_length_input_widget()
