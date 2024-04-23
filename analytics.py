from datetime import datetime, timedelta
from database import HabitDatabase

def get_longest_streak_from_completions(habit_database: HabitDatabase, periodicity=None) -> int:
    """Get the longest streak from completions."""
    cursor = habit_database.connection.cursor()
    if periodicity:
        cursor.execute("""
            SELECT MAX(streak) 
            FROM (
                SELECT habit_name, COUNT(*) as streak
                FROM completions
                WHERE strftime('%Y-%m-%d', completion_date) >= date('now', '-7 days')
                GROUP BY habit_name
            )
            JOIN habits ON completions.habit_name = habits.name
            WHERE habits.periodicity = ?
        """, (periodicity,))
    else:
        cursor.execute("""
            SELECT MAX(streak) 
            FROM (
                SELECT habit_name, COUNT(*) as streak
                FROM completions
                WHERE strftime('%Y-%m-%d', completion_date) >= date('now', '-7 days')
                GROUP BY habit_name
            )
        """)
    result = cursor.fetchone()
    return result[0] if result else 0

def view_longest_streak_menu(habit_database: HabitDatabase, periodicity=None):
    """View the longest streak."""
    if periodicity == "All":
        longest_streak_habit, longest_streak = get_longest_streak(habit_database)
        streak_count = get_longest_streak_from_completions(habit_database, longest_streak_habit)
        print(f"Habit ('{longest_streak_habit}') has the longest streak out of all the habits! (Streak count: {streak_count})\n")
    else:
        longest_streak_habit, longest_streak = get_longest_streak(habit_database, periodicity)
        streak_count = get_longest_streak_from_completions(habit_database, longest_streak_habit, periodicity)
        print(f"Habit ('{longest_streak_habit}') has the longest streak among {periodicity.lower()} habits! (Streak count: {streak_count})\n")

def get_longest_streak(habit_database, periodicity=None):
    """Get the longest streak."""
    return habit_database.get_longest_streak_from_completions(periodicity)

def calculate_streaks(habit_database: HabitDatabase) -> None:
    """Calculate and update streaks for all habits."""
    habits = habit_database.get_habits()

    for habit in habits:
        if 'periodicity' in habit:
            if habit['periodicity'] == 'Daily':
                streak = calculate_daily_streak(habit_database, habit['name'])
            elif habit['periodicity'] == 'Weekly':
                streak = calculate_weekly_streak(habit_database, habit['name'])
        else:
            streak = 0 
    else:
        streak = 0  

    habit_database.update_streak(habit['name'], streak)

def calculate_daily_streak(habit_database: HabitDatabase, habit_name: str) -> int:
    """Calculate daily streak for a habit."""
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    if habit_database.check_habit_done_today(habit_name, str(today)):
        return habit_database.get_streak_for_habit(habit_name) + 1
    elif habit_database.check_habit_done_today(habit_name, str(yesterday)):
        return habit_database.get_streak_for_habit(habit_name)
    else:
        return 0

def calculate_weekly_streak(habit_database: HabitDatabase, habit_name: str) -> int:
    """Calculate weekly streak for a habit."""
    today = datetime.now().date()
    last_week_start = today - timedelta(days=today.weekday())  

    streak = 0
    while habit_database.check_habit_done_today(habit_name, str(last_week_start)):
        streak += 1
        last_week_start -= timedelta(weeks=1) 

    return streak
