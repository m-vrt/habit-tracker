import pytest
from analytics import *
from database import HabitDatabase
from habit import Habit
from datetime import datetime

@pytest.fixture
def habit_database():
    return MockHabitDatabase()

def test_get_tracked_habits(habit_database):
    tracked_habits = get_tracked_habits(habit_database)
    assert len(tracked_habits) == 5

def test_get_habits_by_periodicity(habit_database):
    daily_habits = get_habits_by_periodicity(habit_database, "daily")
    assert len(daily_habits) == 4

def test_get_longest_streak(habit_database):
    longest_streak = get_longest_streak(habit_database)
    assert longest_streak == 28

def test_get_longest_streak_for_habit(habit_database):
    longest_streak = get_longest_streak_for_habit(habit_database, "Exercise")
    assert longest_streak == 28

def test_get_tracked_habits_empty():
    empty_habit_database = MockEmptyHabitDatabase()
    tracked_habits = get_tracked_habits(empty_habit_database)
    assert len(tracked_habits) == 0

def test_get_habits_by_nonexistent_periodicity():
    habit_database = MockHabitDatabase()
    non_existent_periodicity_habits = get_habits_by_periodicity(habit_database, "nonexistent_periodicity")
    assert len(non_existent_periodicity_habits) == 0

def test_get_longest_streak_empty():
    empty_habit_database = MockEmptyHabitDatabase()
    longest_streak = get_longest_streak(empty_habit_database)
    assert longest_streak == 0

class MockHabitDatabase:
    def get_habits(self):
        return [
            Habit("Exercise", "Exercise description", "daily", datetime.now()),
            Habit("Read", "Read description", "daily", datetime.now()),
            Habit("Meditate", "Meditate description", "daily", datetime.now()),
            Habit("Weekly Review", "Weekly Review description", "weekly", datetime.now()),
            Habit("Learn Language", "Learn Language description", "daily", datetime.now())
        ]

    def view_streaks(self):
        return {"Exercise": 28, "Read": 28, "Meditate": 28, "Weekly Review": 28, "Learn Language": 28}

class MockEmptyHabitDatabase:
    def get_habits(self):
        return []

    def view_streaks(self):
        return {"Exercise": 0}
