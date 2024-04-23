from datetime import datetime, timedelta
from collections import Counter


class Habit:
    """Represents a habit."""

    def __init__(self, name, description, periodicity, created_date=None):
        """
        Initialize a habit.

        :param name: Name of the habit
        :param description: Description of the task
        :param periodicity: Periodicity of the habit (daily or weekly)
        :param created_date: Date when the habit was created (default is None)
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_date = created_date or datetime.now().date()
        self.completed_tasks = []
        self.streak_counter = Counter()
        self.streak = 0
        self.last_completion_date = None  

    def complete_task(self):
        """
        Mark a task as completed.

        This method is called when a user completes a task associated with the habit.
        """
        completion_time = datetime.now()
        self.completed_tasks.append(completion_time)
        self.update_streak(completion_time)
        self.last_completion_date = completion_time  

    def update_streak(self, completion_time):
        """
        Update streak based on consecutive completions within the defined period.

        This method updates the streak based on consecutive completions of tasks within
        the defined period for the habit.
        """
        if self.check_if_streak_continues_within_period(completion_time):
            self.streak += 1
        else:
            self.streak = 1

    def check_if_streak_continues_within_period(self, completion_time):
        """
        Check if the streak continues based on consecutive completions within the defined period.

        This method checks if the current completion continues a streak by comparing
        the completion date with the date of the last completed task within the defined period.
        """
        if len(self.completed_tasks) > 0:
            last_completion_time = self.completed_tasks[-1]
            current_time = completion_time
                       
            if self.periodicity == 'Daily':
                periodicity_days = 1
            elif self.periodicity == 'Weekly':
                periodicity_days = 7
            else:
                raise ValueError("Invalid value for periodicity")

            period_start_time = current_time - timedelta(days=periodicity_days)
            return period_start_time <= last_completion_time < current_time
        return False
