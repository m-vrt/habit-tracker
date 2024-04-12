from database import HabitDatabase
from habit import Habit

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
    habits = habit_database.get_habits()
    return [habit for habit in habits if habit.periodicity == periodicity]

def get_longest_streak(habit_database):
    """
    Return the longest run streak of all defined habits.

    :param habit_database: Instance of HabitDatabase
    :return: Longest run streak
    """
    streaks = habit_database.view_streaks()
    return max(streaks.values())

def get_longest_streak_for_habit(habit_database, habit_name):
    """
    Return the longest run streak for a given habit.

    :param habit_database: Instance of HabitDatabase
    :param habit_name: Name of the habit to retrieve streak for
    :return: Longest run streak for the specified habit
    """
    streaks = habit_database.view_streaks()
    return streaks.get(habit_name, 0)
