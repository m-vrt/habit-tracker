from habit_tracker import *

def test_get_habit_data_from_database():   
    habit_data = get_habit_data_from_database()
    assert isinstance(habit_data, list)
    assert len(habit_data) > 0


def test_get_daily_habits_for_habit_tracker():    
    daily_habits = get_daily_habits_for_habit_tracker()
    assert isinstance(daily_habits, list)
    assert all(habit['periodicity'] == 'Daily' for habit in daily_habits)


def test_get_weekly_habits_for_habit_tracker():  
    weekly_habits = get_weekly_habits_for_habit_tracker()
    assert isinstance(weekly_habits, list)
    assert all(habit['periodicity'] == 'Weekly' for habit in weekly_habits)
