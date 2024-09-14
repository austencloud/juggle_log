import sys
from PyQt6.QtWidgets import QApplication
from main_window.main_window import MainWindow



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
