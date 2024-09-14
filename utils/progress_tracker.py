import json
from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox, QListWidget, QTableWidgetItem

if TYPE_CHECKING:
    from main_window.main_widget import MainWidget

class ProgressTracker:
    filepath = "progress.json"
    # Use this format to store human-readable dates (M-D-YYYY)
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

                # Convert the existing date format (YYYY-MM-DD) to the new format (M-D-YYYY)
                formatted_dates = {
                    pattern: self.convert_to_human_date(date)
                    for pattern, date in completion_dates.items()
                }

                return completed_patterns, max_catches, formatted_dates
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
        
        # If catches is 0, remove the completion date from the JSON
        if catches == 0:
            if pattern in self.completion_dates:
                del self.completion_dates[pattern]
                # remove the date from the table and from the settings
                self.main_widget.pattern_table.remove_date_item(pattern)
        else:
            # Save the completion date using the human-readable format
            self.completion_dates[pattern] = self.get_current_human_date()
            # Update the completion date in the table
            self.main_widget.pattern_table.update_completion_date(pattern)
        if catches >= 100:
            self.completed_patterns.add(pattern)
        else:
            self.completed_patterns.discard(pattern)
        self.save_progress()

    def update_completion_date(self, pattern, date = None):
        # Update the date with the new human-readable format
        date = date or self.get_current_human_date()
        self.completion_dates[pattern] = date
        self.save_progress()
        return date

    def get_max_catches(self, pattern):
        return self.max_catches.get(pattern, 0)

    def get_completion_date(self, pattern):
        return self.completion_dates.get(pattern)

    def is_completed(self, pattern):
        return self.max_catches.get(pattern, 0) >= 100

    def get_current_human_date(self):
        # Use %m-%d-%Y and manually strip leading zeros for Windows compatibility
        now = datetime.now()
        return now.strftime("%m-%d-%Y").lstrip("0").replace("-0", "-")

    def convert_to_human_date(self, date_str):
        # Check if the date is already in the M-D-YYYY format (e.g., "9-13-2024")
        try:
            # If the date contains dashes and follows the human format, we leave it as-is
            if len(date_str.split('-')) == 3:
                month, day, year = date_str.split('-')
                if len(month) <= 2 and len(day) <= 2 and len(year) == 4:
                    return date_str
            
            # If it's not in the correct format, we assume it's in the YYYY-MM-DD format
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            return parsed_date.strftime("%m-%d-%Y").lstrip("0").replace("-0", "-")
        except ValueError:
            return date_str  # If the date isn't in the expected format, leave it unchanged
