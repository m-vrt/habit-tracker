from database import HabitDatabase
from habit import Habit 

class HabitTracker:
    """Tracks habits and their states."""

    def __init__(self, habit_database: HabitDatabase):
        """Initialize HabitTracker."""
        self.habit_database = habit_database
        self.habits = self.habit_database.get_habits()

    def add_habit(self, habit):
        """
        Add a new habit to the tracker.

        :param habit: Habit object to add to the tracker
        """
        if habit.name not in self.habit_database.get_habits():
            self.habit_database.add_habit(habit.name, habit.task_specification)
            self.habits.append(habit)
        else:
            raise ValueError(f"Habit with name '{habit.name}' already exists.")

    def remove_habit(self, habit_name):
        """
        Remove an existing habit from the tracker.

        :param habit_name: Name of the habit to remove
        """
        if habit_name in self.habit_database.get_habits():
            self.habit_database.remove_habit(habit_name)
            self.habits = self.habit_database.get_habits()  
            print(f"Habit {habit_name} removed successfully.")
        else:
            raise ValueError(f"No habit with name '{habit_name}' found.")

    def get_habits(self):
        """
        Get the list of habits being tracked.

        :return: List of Habit objects
        """
        return self.habits

    def check_habit_state(self, habit_name):
        """
        Check the state of a habit.

        :param habit_name: Name of the habit to check
        :return: State of the habit
        """
        if habit_name in self.habit_database.get_habits():
            return "Habit exists"
        else:
            return "No habits tracked"

    def view_streaks(self):
        """View streaks for habits."""
        streaks = self.habit_database.get_streaks()
        return streaks

    def update_database(self):
        """Update the database with current habit data."""
        self.habit_database.update_database()

    def close_database(self):
        """Close the connection to the database."""
        self.habit_database.close()