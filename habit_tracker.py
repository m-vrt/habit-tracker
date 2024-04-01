from database import HabitDatabase

class HabitTracker:
    """Tracks habits and their states."""

    def __init__(self):
        """Initialize HabitTracker."""
        self.habit_database = HabitDatabase()
        self.habits = self.habit_database.get_habits()

    def add_habit(self, habit):
        """Add a new habit."""
        # For later: Implementation details

    def remove_habit(self, habit_name):
        """Remove an existing habit."""
        # For later: Implementation details

    def get_habits(self):
        """Get the list of habits."""
        # For later: Implementation details
        return self.habits

    def check_habit_state(self, habit_name):
        """Check the state of a habit."""
        # For later: Implementation details

    def view_streaks(self):
        """View streaks for habits."""
        # For later: Implementation details

    def update_database(self):
        """Update the database with current habit data."""
        # For later: Implementation details
