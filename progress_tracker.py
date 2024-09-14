import json
from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox, QListWidget, QTableWidgetItem

if TYPE_CHECKING:
    from main_widget import MainWidget


class ProgressTracker:
    filepath = "progress.json"
    date_format = "%Y-%m-%d"
    completed_key = "completed_patterns"
    max_catches_key = "max_catches"
    completion_dates_key = "completion_dates"

    def __init__(self, main_widget: "MainWidget"):
        self.completed_patterns, self.max_catches, self.completion_dates = (
            self.load_progress()
        )
        self.main_widget = main_widget

    def load_progress(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                completed_patterns = set(data.get(self.completed_key, []))
                max_catches = data.get(self.max_catches_key, {})
                completion_dates = data.get(self.completion_dates_key, {})
                return completed_patterns, max_catches, completion_dates
        except FileNotFoundError:
            return set(), {}, {}

    def save_progress(self):
        data = {
            self.completed_key: list(self.completed_patterns),
            self.max_catches_key: self.max_catches,
            self.completion_dates_key: self.completion_dates,
        }
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def set_max_catches(self, pattern, catches):
        self.max_catches[pattern] = catches
        self.save_progress()

        self.completion_dates[pattern] = datetime.now().strftime(self.date_format)
        if catches >= 100:
            self.completed_patterns.add(pattern)
        else:
            self.completed_patterns.discard(pattern)
        self.save_progress()

    def update_completion_date(self, pattern):
        current_date = datetime.now().strftime(self.date_format)
        self.completion_dates[pattern] = current_date
        self.save_progress()
        return current_date

    def get_max_catches(self, pattern):
        return self.max_catches.get(pattern, 0)

    def get_completion_date(self, pattern):
        return self.completion_dates.get(pattern)

    def is_completed(self, pattern):
        return self.max_catches.get(pattern, 0) >= 100
