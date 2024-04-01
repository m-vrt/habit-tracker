from habit_tracker import HabitTracker
from questionary import prompt

class HabitCLI:
    """Command Line Interface for Habit Tracker."""

    def __init__(self):
        self.habit_tracker = HabitTracker()

    def main_menu(self):
        """Main menu for Habit Tracker."""
        while True:
            choice = prompt({
                "type": "list",
                "name": "action",
                "message": "What would you like to do?",
                "choices": [
                    "Add Habit",
                    "Remove Habit",
                    "View Habit List",
                    "Check Habit State",
                    "View Streaks",
                    "Quit"
                ]
            })["action"]
            if choice == "Add Habit":
                self.add_habit()
            elif choice == "Remove Habit":
                self.remove_habit()
            elif choice == "View Habit List":
                self.view_habit_list()
            elif choice == "Check Habit State":
                self.check_habit_state()
            elif choice == "View Streaks":
                self.view_streaks()
            elif choice == "Quit":
                break

    def add_habit(self):
        """Add a new habit."""
        # For later: Implementation details

    def remove_habit(self):
        """Remove an existing habit."""
        # For later: Implementation details

    def view_habit_list(self):
        """View the list of habits."""
        # For later: Implementation details

    def check_habit_state(self):
        """Check the state of a habit."""
        # For later: Implementation details

    def view_streaks(self):
        """View streaks for habits."""
        # For later: Implementation details
