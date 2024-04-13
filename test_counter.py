import pytest
from unittest.mock import MagicMock
from counter import HabitCounter

@pytest.fixture
def habit_database():
    return MagicMock()

def test_add_habit(habit_database):
    counter = HabitCounter(habit_database)
    habit_database.get_habits.return_value = []
    counter.add_habit("Exercise", "Do workout for 30 minutes", "daily")
    habit_database.add_habit.assert_called_once_with("Exercise", "Do workout for 30 minutes", "daily")

def test_delete_habit(habit_database):
    counter = HabitCounter(habit_database)
    habit_database.get_habits.return_value = [{"name": "Exercise"}]
    counter.delete_habit("Exercise")
    habit_database.delete_habit.assert_called_once_with("Exercise")

def test_view_habits(habit_database, capsys):
    counter = HabitCounter(habit_database)
    habit_database.get_habits.return_value = [{"name": "Exercise", "description": "Do workout"}]
    counter.view_habits()
    captured = capsys.readouterr()
    assert captured.out == "Habit List (All):\n- Exercise: Do workout\n\n"

def test_filter_by_periodicity(habit_database, capsys):
    counter = HabitCounter(habit_database)
    habit_database.get_habits_by_periodicity.return_value = [{"name": "Exercise", "description": "Do workout"}]
    counter.filter_by_periodicity("daily")
    captured = capsys.readouterr()
    assert captured.out == "Habit List (Daily):\n- Exercise: Do workout\n\n"

def test_check_habit_status_existing_habit(habit_database, capsys):
    counter = HabitCounter(habit_database)
    habit_database.check_habit_status.return_value = "consistently_followed"
    counter.check_habit_status("Exercise")
    captured = capsys.readouterr()
    assert captured.out == "'Exercise' is consistently followed. Keep it up!\n"

def test_check_habit_status_non_existing_habit(habit_database, capsys):
    counter = HabitCounter(habit_database)
    habit_database.check_habit_status.return_value = None
    counter.check_habit_status("Exercise")
    captured = capsys.readouterr()
    assert captured.out == "'Exercise' does not exist.\n"

def test_complete_habit(habit_database):
    counter = HabitCounter(habit_database)
    habit_database.get_streak_for_habit.return_value = 5
    counter.complete_habit("Exercise")
    habit_database.complete_habit.assert_called_once_with("Exercise")
    habit_database.update_streak.assert_called_once_with("Exercise", 6)

def test_complete_habit_reset_streak(habit_database):
    counter = HabitCounter(habit_database)
    habit_database.get_streak_for_habit.return_value = None
    counter.complete_habit("Exercise")
    habit_database.complete_habit.assert_called_once_with("Exercise")
    habit_database.update_streak.assert_called_once_with("Exercise", 0)

def test_view_streaks(habit_database, capsys):
    counter = HabitCounter(habit_database)
    habit_database.view_streaks.return_value = {"Exercise": 5}
    counter.view_streaks()
    captured = capsys.readouterr()
    assert captured.out == "Habit Streaks:\n- Exercise: 5 days\n\n"

def test_view_longest_streak(habit_database, capsys):
    counter = HabitCounter(habit_database)
    habit_database.get_longest_streak.return_value = ("Exercise", 10)
    counter.view_longest_streak()
    captured = capsys.readouterr()
    assert captured.out == "Exercise earns a spot in the Habit Hall of Fame with the longest streak of 10 days!\n"

def test_view_longest_streak_for_habit(habit_database, capsys):
    counter = HabitCounter(habit_database)
    habit_database.get_longest_streak_for_habit.return_value = 10
    counter.view_longest_streak_for_habit("Exercise")
    captured = capsys.readouterr()
    assert captured.out == "The longest streak for habit 'Exercise' is 10 days.\n"
