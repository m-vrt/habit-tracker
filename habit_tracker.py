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

    def get_habits(self):
        """
        Get the list of habits being tracked.

        :return: List of Habit objects
        """
        return self.habits

    def get_streaks(self):
        """View streaks for habits."""
        streaks = self.habit_database.get_streaks()
        return streaks