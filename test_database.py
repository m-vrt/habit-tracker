import pytest
import sqlite3
from datetime import datetime
from database import HabitDatabase

@pytest.fixture
def test_db():
    db = HabitDatabase(":memory:")
    yield db
    db.close()

@pytest.fixture(autouse=True)
def reset_db(test_db):
    test_db.clear_database()

def test_add_habit(test_db):
    test_db.add_habit("Test Habit", "Test Description")
    habits = test_db.get_habits()
    assert "Test Habit" in habits

def test_remove_habit(test_db):
    test_db.add_habit("Test Habit", "Test Description")
    test_db.remove_habit("Test Habit")
    habits = test_db.get_habits()
    assert "Test Habit" not in habits

def test_increment_counter(test_db):
    test_db.add_habit("Test Habit", "Test Description")
    test_db.increment_counter("Test Habit")
    data = test_db.get_counter_data("Test Habit")
    assert len(data) == 1
    assert data[0][1] == "Test Habit"

def test_get_habits(test_db):
    test_db.add_habit("Test Habit", "Test Description")
    habits = test_db.get_habits()
    assert "Test Habit" in habits

def test_get_streaks(test_db):
    test_db.add_habit("Test Habit", "Test Description")
    test_db.increment_counter("Test Habit")
    streaks = test_db.get_streaks()
    assert streaks.get("Test Habit", 0) == 1

def test_calculate_streak(test_db):
    test_db.add_habit("Test Habit", "Test Description")
    test_db.increment_counter("Test Habit", datetime.now().strftime("%Y-%m-%d"))
    streak = test_db.calculate_streak([datetime.now().strftime("%Y-%m-%d")]) 
    assert streak == 1

def test_duplicate_habit(test_db):
    test_db.add_habit("Test Habit", "Test Description")
    with pytest.raises(ValueError):
        test_db.add_habit("Test Habit", "Duplicate Habit Description")

def test_invalid_remove_habit(test_db):
    with pytest.raises(sqlite3.IntegrityError):
        test_db.remove_habit("Nonexistent Habit")

def test_increment_counter_no_habit(test_db):
    with pytest.raises(sqlite3.IntegrityError):
        test_db.increment_counter("Nonexistent Habit")

def test_get_habit_data(test_db):
    test_db.add_habit("Test Habit", "Test Description")
    habit_data = test_db.get_habit_data("Test Habit")
    assert habit_data[0] == "Test Habit"
    assert habit_data[1] == "Test Description"

def test_get_habits_empty(test_db):
    habits = test_db.get_habits()
    assert len(habits) == 0

def test_get_streaks_empty(test_db):
    streaks = test_db.get_streaks()
    assert len(streaks) == 0
