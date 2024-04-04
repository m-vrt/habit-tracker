from database import HabitDatabase


class HabitTracker:
    """Tracks habits and their states."""

    def __init__(self):
        """Initialize HabitTracker."""
        self.habit_database = HabitDatabase()
        self.habits = self.habit_database.get_habits()

    def add_habit(self, habit):
        """
        Add a new habit to the tracker.

        :param habit: Habit object to add to the tracker
        """
        self.habit_database.add_habit(habit)
        self.habits = self.habit_database.get_habits()

    def remove_habit(self, habit_name):
        """
        Remove an existing habit from the tracker.

        :param habit_name: Name of the habit to remove
        """
        self.habit_database.remove_habit(habit_name)
        self.habits = self.habit_database.get_habits()

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
        habit_data = self.habit_database.get_habit_data(habit_name)
        if habit_data:
            return "Habit exists"
        else:
            return "No habits tracked"

    def view_streaks(self):
        """View streaks for habits."""
        streaks = self.habit_database.get_streaks()
        return streaks

    def update_database(self):
        """Update the database with current habit data."""
        self.habit_database.update_data()
