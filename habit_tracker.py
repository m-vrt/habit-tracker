from datetime import datetime
from database import HabitDatabase
from habit import Habit


class HabitTracker:
    """Tracks habits and their status."""

    def __init__(self, habit_database: HabitDatabase):
        """Initialize HabitTracker."""
        self.habit_database = habit_database
        self.habits = self.habit_database.get_habits()

    def add_habit(self, name, description, periodicity):
        """
        Add a new habit to the tracker.

        :param name: Name of the habit
        :param description: Description of the habit
        :param periodicity: Periodicity of the habit
        """
       
        habit = Habit(name, description, periodicity)
      
        if habit.name in [h.name for h in self.habits]:
            raise ValueError(f"Habit with name '{habit.name}' already exists.")

        self.habit_database.add_habit(habit)

        self.habits.append(habit)

    def delete_habit(self, habit_name):
        """
        Delete an existing habit from the tracker.

        :param habit_name: Name of the habit to delete
        """
        if habit_name in [habit.name for habit in self.habits]:
            self.habit_database.delete_habit(habit_name)
            self.habits = self.habit_database.get_habits()
            print(f"Habit {habit_name} deleted successfully.")
        else:
            raise ValueError(f"No habit with name '{habit_name}' found.")

    def get_habits(self):
        """
        Get the list of habits being tracked.

        :return: List of Habit objects
        """
        return self.habits

    def check_habit_status(self, habit_name):
        """
        Check the status of a habit.

        :param habit_name: Name of the habit to check
        :return: Status of the habit
        """
        if habit_name in [habit.name for habit in self.habits]:
            return "Habit exists"
        else:
            return "No habits tracked"

    def view_streaks(self):
        """View streaks for habits."""
        streaks = self.habit_database.view_streaks()
        return streaks

    def update_database(self):
        """Update the database with current habit data."""
        self.habit_database.update_database()

    def close_database(self):
        """Close the connection to the database."""
        self.habit_database.close()
