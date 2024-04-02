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
        habit_name = prompt({
            "type": "input",
            "name": "habit_name",
            "message": "Enter the name of the habit:"
        })["habit_name"]
        
        habit_description = prompt({
            "type": "input",
            "name": "habit_description",
            "message": "Enter a description for the habit:"
        })["habit_description"]
        
        self.habit_tracker.add_habit(habit_name, habit_description)
        print(f"Habit '{habit_name}' successfully added!\n")

    def remove_habit(self):
        """Remove an existing habit."""
        habit_name = prompt({
            "type": "select",
            "name": "habit_name",
            "message": "Select the habit you want to remove:",
            "choices": [habit.name for habit in self.habit_tracker.get_habits()]
        })["habit_name"]
        
        self.habit_tracker.remove_habit(habit_name)
        print(f"Habit '{habit_name}' successfully removed!\n")

    def view_habit_list(self):
        """View the list of habits."""
        habits = self.habit_tracker.get_habits()
        print("Habit List:")
        for habit in habits:
            print(f"- {habit.name}: {habit.description}")
        print()

    def check_habit_state(self):
        """Check the state of a habit."""
        habit_name = prompt({
            "type": "select",
            "name": "habit_name",
            "message": "Select the habit to check its state:",
            "choices": [habit.name for habit in self.habit_tracker.get_habits()]
        })["habit_name"]
        
        state = self.habit_tracker.check_habit_state(habit_name)
        print(f"The state of habit '{habit_name}' is: {state}\n")

    def view_streaks(self):
        """View streaks for habits."""
        streaks = self.habit_tracker.view_streaks()
        print("Habit Streaks:")
        for habit, streak in streaks.items():
            print(f"- {habit}: {streak} days")
        print()
