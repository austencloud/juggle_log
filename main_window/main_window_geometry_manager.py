from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_window import MainWindow


class MainWindowGeometryManager:
    def __init__(self, main_window: "MainWindow"):
        self.main_window = main_window
        self.app = main_window.app

    def set_geometry(self):
        screen_width, screen_height = self.get_screen_geometry()
        window_width, window_height = self.calculate_window_size(
            screen_width, screen_height
        )
        self.main_window.resize(window_width, window_height)
        self.center_window(self.main_window)

    def get_screen_geometry(self):
        """Get the screen geometry."""
        screen_geometry = self.app.primaryScreen().availableGeometry()
        return screen_geometry.width(), screen_geometry.height()

    def calculate_window_size(self, screen_width, screen_height):
        """Calculate the window size based on screen dimensions."""
        window_width = int(screen_width * 0.4)
        window_height = int(screen_height * 0.5)
        return window_width, window_height

    def center_window(self, window: "MainWindow"):
        """Center the window on the screen."""
        frame = window.frameGeometry()
        center = self.app.primaryScreen().availableGeometry().center()
        frame.moveCenter(center)
        window.move(frame.topLeft())
