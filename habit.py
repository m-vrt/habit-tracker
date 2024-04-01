from datetime import datetime

class Habit:
    """Represents a habit."""

    def __init__(self, name, task, periodicity, created_date):
        self.name = name
        self.task = task
        self.periodicity = periodicity
        self.created_date = created_date
        self.completed_tasks = []
        self.streak_counter = Counter()
        self.streak = 0

    def complete_task(self):
        """Complete a task for the habit."""
        # For later: Implementation details

    def update_streak(self):
        """Update streak for the habit."""
        # For later: Implementation details
