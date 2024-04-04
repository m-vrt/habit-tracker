from datetime import datetime, timedelta
from collections import Counter


class Habit:
    """Represents a habit."""

    def __init__(self, name, task_specification, periodicity, created_date):
        """
        Initialize a habit.

        :param name: Name of the habit
        :param task_specification: Description of the task
        :param periodicity: Periodicity of the habit (daily or weekly)
        :param created_date: Date when the habit was created
        """
        self.name = name
        self.task_specification = task_specification
        self.periodicity = periodicity
        self.created_date = created_date
        self.completed_tasks = []
        self.streak_counter = Counter()
        self.streak = 0
        self.last_completed_date = None  # Track the last completed date

    def complete_task(self):
        """
        Mark a task as completed.

        This method is called when a user completes a task associated with the habit.
        """
        self.completed_tasks.append(datetime.now().date())
        self.update_streak()

    def update_streak(self):
        """
        Update streak based on consecutive completions within the defined period.

        This method updates the streak based on consecutive completions of tasks within
        the defined period for the habit.
        """
        if self.check_if_streak_continues_within_period():
            self.streak += 1
        else:
            self.streak = 1

    def check_if_streak_continues_within_period(self):
        """
        Check if the streak continues based on consecutive completions within the defined period.

        This method checks if the current completion continues a streak by comparing
        the completion date with the date of the last completed task within the defined period.
        """
        if len(self.completed_tasks) > 0:
            last_completed_date = self.completed_tasks[-1]
            current_date = datetime.now().date()
            
            # Handle periodicity string ('daily' or 'weekly')
            if isinstance(self.periodicity, str):
                if self.periodicity == 'daily':
                    periodicity_days = 1
                elif self.periodicity == 'weekly':
                    periodicity_days = 7
                else:
                    raise ValueError("Invalid value for periodicity")
            else:
                periodicity_days = int(self.periodicity)
                
            period_start_date = current_date - timedelta(days=periodicity_days)
            return period_start_date <= last_completed_date < current_date
        return False

    def is_task_completed_within_period(self, period):
        """
        Check if a task has been completed within the defined period.

        :param period: The period to check within (in days)
        :return: True if task is completed within the period, False otherwise
        """
        if not self.completed_tasks:
            return False
        
        last_completed_date = self.completed_tasks[-1]
        current_date = datetime.now().date()
        return (current_date - last_completed_date).days <= period

    def update_streak_within_period(self, period):
        """
        Update streak within the specified period.

        This method checks if the habit has been completed within the specified period,
        and resets the streak if the period has elapsed.
        """
        if not self.is_task_completed_within_period(period):
            self.streak = 0  # Reset streak if the task is not completed within the period
