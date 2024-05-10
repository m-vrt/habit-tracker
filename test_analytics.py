from analytics import (
    get_habit_hall_of_fame_daily,
    get_habit_hall_of_fame_weekly,    
    calculate_longest_streak_for_habit_predefined_daily,
    calculate_longest_streak_for_habit_predefined_weekly
)

def test_get_habit_hall_of_fame_daily_with_data():
    streak = get_habit_hall_of_fame_daily()
    assert streak > 0

def test_get_habit_hall_of_fame_weekly_with_data():
    streak = get_habit_hall_of_fame_weekly()
    assert streak > 0

def test_calculate_longest_streak_for_habit_predefined_daily():
    assert calculate_longest_streak_for_habit_predefined_daily("Study") == 31
    assert calculate_longest_streak_for_habit_predefined_daily("Code") == 6
    assert calculate_longest_streak_for_habit_predefined_daily("Research") == 5
 
def test_calculate_longest_streak_for_habit_predefined_weekly():
    assert calculate_longest_streak_for_habit_predefined_weekly("Clean House") == 3
    assert calculate_longest_streak_for_habit_predefined_weekly("Call Family") == 4

