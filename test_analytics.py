from analytics import (
    get_habit_hall_of_fame_daily,
    get_habit_hall_of_fame_weekly,
    get_habits_with_longest_streaks
)


def test_get_habit_hall_of_fame_daily_with_data():
    streak = get_habit_hall_of_fame_daily()
    assert streak > 0

def test_get_habit_hall_of_fame_weekly_with_data():
    streak = get_habit_hall_of_fame_weekly()
    assert streak > 0

def test_get_habits_with_longest_streaks_daily():
    habits = get_habits_with_longest_streaks("Daily")
    assert len(habits) > 0

def test_get_habits_with_longest_streaks_weekly():
    habits = get_habits_with_longest_streaks("Weekly")
    assert len(habits) > 0
