from datetime import datetime, timedelta
from collections import Counter

class Habit:
    """Represents a habit."""

    def __init__(self, name, description, periodicity, created_date=None, completion_date=None, completion_time=None, streak=None, counter=None):
        """
        Initialize a habit.

        :param name: Name of the habit
        :param description: Description of the task
        :param periodicity: Periodicity of the habit (daily or weekly)
        :param created_date: Date when the habit was created (default is None)
        :param completion_date: Date when the habit was completed (default is None)
        :param completion_time: Time when the habit was completed (default is None)
        :param streak: Streak of the habit (default is None)
        :param counter: Counter of the habit (default is None)
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_date = created_date 
        self.completion_date = completion_date
        self.completion_time = completion_time
        self.streak = streak 
        self.counter = counter


  