import pytest
from datetime import datetime, timedelta
from database import HabitDatabase
from main import add_habit, delete_habit, view_habits, check_habit_status, complete_habit, view_streaks, view_longest_streak_for_habit, view_longest_streak

@pytest.fixture
def test_db():
    db = HabitDatabase(":memory:")
    yield db
    db.close()

@pytest.fixture(autouse=True)
def reset_db(test_db):
    test_db.clear_database()

def test_add_habit(test_db):
    add_habit(test_db)
    habits = test_db.get_habits()
    assert len(habits) == 1
    assert habits[0]['name'] == "Test Habit"

def test_delete_habit(test_db):
    add_habit(test_db)
    delete_habit(test_db)
    habits = test_db.get_habits()
    assert len(habits) == 0

def test_check_habit_status_no_habit(test_db, capsys):
    check_habit_status(test_db)
    captured = capsys.readouterr()
    assert "does not exist" in captured.out

def test_check_habit_status_existing_habit(test_db, capsys):
    add_habit(test_db)
    check_habit_status(test_db)
    captured = capsys.readouterr()
    assert "consistently_followed" in captured.out or "inconsistent" in captured.out

def test_complete_habit_no_habit(test_db, capsys):
    complete_habit(test_db)
    captured = capsys.readouterr()
    assert "does not exist" in captured.out

def test_complete_habit_existing_habit_no_streak(test_db, capsys):
    add_habit(test_db)
    complete_habit(test_db)
    captured = capsys.readouterr()
    assert "marked as completed" in captured.out

def test_complete_habit_existing_habit_with_streak(test_db, capsys):
    add_habit(test_db)
    test_db.complete_habit("Test Habit")
    complete_habit(test_db)
    captured = capsys.readouterr()
    assert "Keep it up!" in captured.out

def test_view_streaks_empty(test_db, capsys):
    view_streaks(test_db)
    captured = capsys.readouterr()
    assert "Habit Streaks" in captured.out

def test_view_longest_streak_for_habit_existing(test_db, capsys):
    add_habit(test_db)
    test_db.complete_habit("Test Habit")
    view_longest_streak_for_habit(test_db)
    captured = capsys.readouterr()
    assert "longest streak" in captured.out

def test_view_longest_streak_for_habit_nonexistent(test_db, capsys):
    view_longest_streak_for_habit(test_db)
    captured = capsys.readouterr()
    assert "does not exist" in captured.out

def test_view_longest_streak_empty(test_db, capsys):
    view_longest_streak(test_db)
    captured = capsys.readouterr()
    assert "Habit Hall of Fame" in captured.out
