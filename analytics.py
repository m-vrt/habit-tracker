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
        completion_history = habit_database.get_completion_history(habit['name'])
        if completion_history:
            total_completions = len(completion_history)
            average_completion_rate = total_completions / (len(completion_history) / 28)  
            longest_streak = calculate_longest_streak(completion_history)
            average_streak_length = calculate_average_streak_length(completion_history)
            
            print(f"{habit['name']}:")
            print(f"Total completions: {total_completions}")
            print(f"Average completion rate (per week): {average_completion_rate:.2f}")
            print(f"Longest streak: {longest_streak}")
            print(f"Average streak length: {average_streak_length:.2f}")
            print()
        else:
            print(f"{habit['name']}: No historical data available\n")

def calculate_longest_streak(completion_history):
    """Calculate the longest streak from completion history."""
    longest_streak = 0
    current_streak = 0
    for i in range(1, len(completion_history)):
        if (completion_history[i] - completion_history[i - 1]).days == 1:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 0
    return longest_streak

def calculate_average_streak_length(completion_history):
    """Calculate the average streak length from completion history."""
    streak_lengths = []
    current_streak = 0
    for i in range(1, len(completion_history)):
        if (completion_history[i] - completion_history[i - 1]).days == 1:
            current_streak += 1
        else:
            streak_lengths.append(current_streak)
            current_streak = 0
    if streak_lengths:
        return sum(streak_lengths) / len(streak_lengths)
    else:
        return 0
