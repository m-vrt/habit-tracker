from habit import Habit
from habit_tracker import HabitTracker
import questionary

class HabitCLI:
    """Command Line Interface for Habit Tracker."""

    def __init__(self):
        self.habit_tracker = HabitTracker()

    def main_menu(self):
        """Main menu for Habit Tracker."""
        while True:
            choice = questionary.select(
                "What would you like to do?",
                choices=[
                    "Add Habit",
                    "Remove Habit",
                    "View Habit List",
                    "Check Habit State",
                    "View Streaks",
                    "Quit"
                ]
            ).ask()
            
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
        habit_name = questionary.text("Enter the name of the habit:").ask()
        habit_description = questionary.text("Enter a description for the habit:").ask()
        
        # Create a Habit object with the provided name and description
        habit = Habit(habit_name, habit_description)
        
        # Add the habit to the habit tracker
        self.habit_tracker.add_habit(habit)
        print(f"Habit '{habit_name}' successfully added!\n")

    def remove_habit(self):
        """Remove an existing habit."""
        habit_names = [habit.name for habit in self.habit_tracker.get_habits()]
        if not habit_names:
            print("No habits to remove.")
            return
        
        habit_name = questionary.select(
            "Select the habit you want to remove:",
            choices=habit_names
        ).ask()
        
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
        habit_names = [habit.name for habit in self.habit_tracker.get_habits()]
        if not habit_names:
            print("No habits to check state.")
            return
        
        habit_name = questionary.select(
            "Select the habit to check its state:",
            choices=habit_names
        ).ask()
        
        state = self.habit_tracker.check_habit_state(habit_name)
        print(f"The state of habit '{habit_name}' is: {state}\n")

    def view_streaks(self):
        """View streaks for habits."""
        streaks = self.habit_tracker.view_streaks()
        print("Habit Streaks:")
        for habit, streak in streaks.items():
            print(f"- {habit}: {streak} days")
        print()
