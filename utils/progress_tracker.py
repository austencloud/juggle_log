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

    MAX_PATTERN_LENGTH = 6  # Max length of repeating patterns

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

    def get_related_patterns(self, pattern: str):
        """
        Return all patterns that start with the same base sequence as the given pattern.
        Create patterns of increasing length up to MAX_PATTERN_LENGTH if they don't exist.
        """
        base_sequence = self.extract_repeating_base(pattern)
        related_patterns = []

        for length in range(1, self.MAX_PATTERN_LENGTH + 1):
            related_pattern = base_sequence * length  # Create patterns like 'D', 'DD', 'DDD', etc.
            related_patterns.append(related_pattern)

            # Ensure the pattern exists in max_catches, even if not already present
            if related_pattern not in self.max_catches:
                self.max_catches[related_pattern] = 0  # Default value of 0 catches

        return related_patterns

    def extract_repeating_base(self, pattern: str):
        """
        Extract the repeating base of a pattern, whether it's a single character or a substring.
        For example:
        - 'OdOdOd' returns 'Od'
        - 'DDD' returns 'D'
        """
        for length in range(1, len(pattern) // 2 + 1):  # Only check up to half the length
            base = pattern[:length]
            # Check if the pattern is just repetitions of this base
            if pattern == base * (len(pattern) // length):
                return base
        return pattern  # If no repeating base is found, return the full pattern

    def set_max_catches(self, pattern, catches):
        # If this is a repeating pattern (single character or substring), update all related patterns
        if self.is_repeating_pattern(pattern):  
            related_patterns = self.get_related_patterns(pattern)
            for related_pattern in related_patterns:
                self.max_catches[related_pattern] = catches
                if catches >= 100:
                    self.completed_patterns.add(related_pattern)
                else:
                    self.completed_patterns.discard(related_pattern)

                # Handle the completion date
                if catches == 0:
                    if related_pattern in self.completion_dates:
                        del self.completion_dates[related_pattern]
                        self.main_widget.pattern_table.remove_date_item(related_pattern)
                else:
                    self.completion_dates[related_pattern] = self.get_current_human_date()
                    self.main_widget.pattern_table.update_completion_date(related_pattern)
        else:
            self.max_catches[pattern] = catches
            if catches >= 100:
                self.completed_patterns.add(pattern)
            else:
                self.completed_patterns.discard(pattern)

            # Handle the completion date
            if catches == 0:
                if pattern in self.completion_dates:
                    del self.completion_dates[pattern]
                    self.main_widget.pattern_table.remove_date_item(pattern)
            else:
                self.completion_dates[pattern] = self.get_current_human_date()
                self.main_widget.pattern_table.update_completion_date(pattern)

        # Save the progress after making changes
        self.save_progress()

    def is_repeating_pattern(self, pattern):
        """
        Check if a pattern consists of repeating substrings.
        For example:
        - 'DDD' is repeating
        - 'OdOdOd' is repeating
        """
        base = self.extract_repeating_base(pattern)
        return len(pattern) > len(base) and pattern == base * (len(pattern) // len(base))

    def update_completion_date(self, pattern, date=None):
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
