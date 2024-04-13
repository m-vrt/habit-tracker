import pytest
from unittest.mock import patch
from io import StringIO
from main import main
from database import HabitDatabase

@pytest.fixture
def habit_database():
    """Fixture for creating an instance of HabitDatabase."""
    return HabitDatabase()

def test_integration_add_habit(habit_database):
    with patch('builtins.input', side_effect=['1', 'New Habit', 'Description', 'daily', '9']):  
        main()
        assert len(habit_database.get_habits()) == 1

def test_integration_delete_habit(habit_database):
    with patch('builtins.input', side_effect=['2', 'Exercise', '9']):  
        main()
        assert len(habit_database.get_habits()) == 0

def test_integration_view_habit_list(habit_database, capsys):
    with patch('builtins.input', side_effect=['3', 'no', '9']):  
        main()
        captured = capsys.readouterr()
        assert "Habit List:" in captured.out

def test_integration_check_habit_state_with_habits_tracked(habit_database, capsys):
    with patch('builtins.input', side_effect=['4', 'Exercise', '9']): 
        main()
        captured = capsys.readouterr()
        assert "Habit exists" in captured.out

def test_integration_check_habit_state_when_no_habits_tracked(habit_database, capsys):
    with patch('builtins.input', side_effect=['4', 'Non-existent Habit', '9']):  
        main()
        captured = capsys.readouterr()
        assert "No habits tracked" in captured.out

def test_integration_view_streaks_with_habits_completed(habit_database, capsys):
    with patch('builtins.input', side_effect=['6', '9']): 
        habit_database.add_habit("Exercise", "Do workout for 30 minutes", "daily")
        habit_database.complete_habit("Exercise")
        main()
        captured = capsys.readouterr()
        assert "Habit Streaks:" in captured.out

def test_integration_view_streaks_when_no_habits_completed(habit_database, capsys):
    with patch('builtins.input', side_effect=['6', '9']):  
        habit_database.add_habit("Exercise", "Do workout for 30 minutes", "daily")
        main()
        captured = capsys.readouterr()
        assert "No habits tracked" in captured.out
