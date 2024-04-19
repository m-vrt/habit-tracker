from datetime import datetime
from database import HabitDatabase

def get_tracked_habits(habit_database):
    """
    Return a list of all currently tracked habits.

    :param habit_database: Instance of HabitDatabase
    :return: List of tracked habit names
    """
    return habit_database.get_habits()

def get_habits_by_periodicity(habit_database, periodicity):
    """
    Return a list of habits with the same periodicity.

    :param habit_database: Instance of HabitDatabase
    :param periodicity: Periodicity of habits to retrieve
    :return: List of habit names with the specified periodicity
    """
    return habit_database.get_habits_by_periodicity(periodicity)

def get_longest_streak(habit_database, periodicity=None):
    """
    Return the longest run streak of all defined habits.

    :param habit_database: Instance of HabitDatabase
    :param periodicity: Periodicity of habits to consider (None for all habits)
    :return: Tuple containing the habit name and longest run streak
    """
    if periodicity:
        habits = habit_database.get_habits_by_periodicity(periodicity)
    else:
        habits = habit_database.get_habits()

    longest_streak = 0
    longest_streak_habit = None

    for habit in habits:
        streak = habit_database.get_streak_for_habit(habit['name'])
        if streak > longest_streak:
            longest_streak = streak
            longest_streak_habit = habit['name']

    return longest_streak_habit, longest_streak

def get_longest_streak_for_habit(habit_database, habit_name):
    """
    Return the longest run streak for a given habit.

    :param habit_database: Instance of HabitDatabase
    :param habit_name: Name of the habit to retrieve streak for
    :return: Longest run streak for the specified habit
    """
    return habit_database.get_longest_streak_for_habit(habit_name)

def view_predefined_habits_status(habit_database):
    """View the status of predefined habits."""
    print("\nPredefined Habits:")
    predefined_habits = habit_database.get_predefined_habits()

    for habit in predefined_habits:
        status, last_completion_date, streak = habit_database.check_habit_status(habit['name'])
        print(f"{habit['name']}: {status}")
        if status != "not_started":
            days_since_last_completion = (datetime.now() - last_completion_date).days
            print(f"Days since last completion: {days_since_last_completion}")
            print(f"Latest streak count: {streak}")
        print()
