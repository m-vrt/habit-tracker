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

        if self.habit_database.habit_exists(name):
            return False
        else:
            self.habit_database.add_habit(name, description, periodicity)
            self.habits.append(habit)
            return True

    def delete_habit(self, habit_name):
        """
        Delete an existing habit from the tracker.

        :param habit_name: Name of the habit to delete
        """
        if self.habit_database.habit_exists(habit_name):
            self.habit_database.delete_habit(habit_name)
            self.habits = self.habit_database.get_habits()
            return True
        else:
            return False

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
        if self.habit_database.habit_exists(habit_name):
            return "Habit exists"
        else:
            return "No habits tracked"

    def get_streaks(self):
        """View streaks for habits."""
        streaks = self.habit_database.get_streaks()
        return streaks

    def update_database(self):
        """Update the database with current habit data."""       
        for habit in self.habits:
            streak = self.habit_database.get_streak_for_habit(habit.name)
            self.habit_database.update_streak(habit.name, streak)

    def close_database(self):
        """Close the connection to the database."""
        self.habit_database.close()
