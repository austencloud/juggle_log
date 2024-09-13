import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from main_widget import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Juggling Pattern Tracker")

        # Get the screen geometry
        screen_geometry = QApplication.primaryScreen().availableGeometry()

        # Set window size as a percentage of screen size (e.g., 80% of screen width and 70% of screen height)
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.7)

        # Resize the window to the calculated dimensions
        self.resize(window_width, window_height)

        # Center the window on the screen
        self.centerWindow()

        # Set the main widget
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

    def centerWindow(self):
        frame = self.frameGeometry()
        center = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
