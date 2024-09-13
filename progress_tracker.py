import json
from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox, QListWidget, QTableWidgetItem

if TYPE_CHECKING:
    from main_widget import MainWidget


class ProgressTracker:
    def __init__(self, main_widget: "MainWidget"):
        self.filepath = "progress.json"
        self.completed_patterns, self.max_catches, self.completion_dates = self.load_progress()
        self.main_widget = main_widget

    def load_progress(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                completed_patterns = set(data.get("completed_patterns", []))
                max_catches = data.get("max_catches", {})
                completion_dates = data.get("completion_dates", {})
                return completed_patterns, max_catches, completion_dates
        except FileNotFoundError:
            return set(), {}, {}

    def save_progress(self):
        data = {
            "completed_patterns": list(self.completed_patterns),
            "max_catches": self.max_catches,
            "completion_dates": self.completion_dates,
        }
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def set_max_catches(self, pattern, catches):
        # Ensure catches can only increase or stay the same
        previous_catches = self.max_catches.get(pattern, 0)
        if catches >= previous_catches:
            self.max_catches[pattern] = catches
            self.save_progress()

            # Record completion date if catches reach a new record
            if catches > previous_catches:
                self.completion_dates[pattern] = datetime.now().strftime("%Y-%m-%d")
            if catches >= 100:
                self.completed_patterns.add(pattern)
            self.save_progress()

    def update_completion_date(self, pattern):
        # Set the current date as the new completion date
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.completion_dates[pattern] = current_date
        self.save_progress()  # Save the updated date
        return current_date


    def get_max_catches(self, pattern):
        return self.max_catches.get(pattern, 0)

    def get_completion_date(self, pattern):
        return self.completion_dates.get(pattern)

    def is_completed(self, pattern):
        return self.max_catches.get(pattern, 0) >= 100

    def extract_pattern(self, text):
        return text.split(" - Completed")[0]
