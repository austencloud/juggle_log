import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from main_widget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app: QApplication = app
        self.setWindowTitle("Juggle Log")
        screen_width, screen_height = self.get_screen_geometry()
        window_width, window_height = self.calculate_window_size(screen_width, screen_height)
        self.resize(window_width, window_height)
        self.center_window()
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

    def get_screen_geometry(self):
        """Get the screen geometry."""
        screen_geometry = self.app.primaryScreen().availableGeometry()
        return screen_geometry.width(), screen_geometry.height()

    def calculate_window_size(self, screen_width, screen_height):
        """Calculate the window size based on screen dimensions."""
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.7)
        return window_width, window_height

    def center_window(self):
        """Center the window on the screen."""
        frame = self.frameGeometry()
        center = self.app.primaryScreen().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

def main():
    """Main entry point of the application."""
    app = QApplication(sys.argv)
    try:
        main_window = MainWindow(app)
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
